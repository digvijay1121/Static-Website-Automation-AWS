#!/usr/bin/env python3
"""
upload_website.py
------------------
Automates deployment of a static website to Amazon S3 using boto3.

Steps:
1. Connect to AWS
2. Create Bucket
3. Disable Block Public Access
4. Attach Bucket Policy
5. Enable Static Website Hosting
6. Upload Website Files
7. Print Website URL
"""

import os
import sys
import logging
import mimetypes
from pathlib import Path

import boto3

from botocore.exceptions import (
    ClientError,
    NoCredentialsError,
    ProfileNotFound,
)

import config

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(config.LOG_FILE, mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# HELPER FUNCTION
# ----------------------------------------------------------------------
def banner(text: str) -> None:
    """
    Prints a formatted banner in the console.
    """

    line = "=" * 60

    logger.info(line)
    logger.info(text)
    logger.info(line)

# ----------------------------------------------------------------------
# STEP 1 : CONNECT TO AWS
# ----------------------------------------------------------------------
def get_s3_client():
    """
    Create a boto3 S3 client using the AWS profile
    configured in config.py.
    """

    try:

        session = boto3.Session(
            profile_name=config.AWS_PROFILE,
            region_name=config.AWS_REGION
        )

        client = session.client("s3")

        # Verify credentials
        client.list_buckets()

        logger.info(
            "Connected to AWS successfully (region: %s)",
            config.AWS_REGION
        )

        return client

    except ProfileNotFound:

        logger.error(
            "AWS Profile '%s' not found.",
            config.AWS_PROFILE
        )

        sys.exit(1)

    except NoCredentialsError:

        logger.error(
            "AWS credentials not found. Run 'aws configure'."
        )

        sys.exit(1)

    except ClientError as err:

        logger.error(
            "Failed to connect to AWS : %s",
            err
        )

        sys.exit(1)

# ----------------------------------------------------------------------
# STEP 2: CREATE BUCKET IF IT DOES NOT EXIST
# ----------------------------------------------------------------------
def create_bucket_if_not_exists(client, bucket_name: str, region: str) -> None:
    """Create the S3 bucket only if it doesn't already exist."""
    try:
        client.head_bucket(Bucket=bucket_name)
        logger.info("Bucket '%s' already exists. Reusing it.", bucket_name)

    except ClientError as err:
        error_code = int(err.response["Error"]["Code"])

        if error_code == 404:

            logger.info(
                "Bucket '%s' not found. Creating it...",
                bucket_name,
            )

            try:

                if region == "us-east-1":

                    client.create_bucket(
                        Bucket=bucket_name
                    )

                else:

                    client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={
                            "LocationConstraint": region
                        },
                    )

                logger.info(
                    "Bucket '%s' created successfully.",
                    bucket_name,
                )

            except ClientError as create_err:

                logger.error(
                    "Could not create bucket: %s",
                    create_err,
                )

                sys.exit(1)

        elif error_code == 403:

            logger.error(
                "Bucket name '%s' is already taken by another AWS account. "
                "Choose another globally unique bucket name.",
                bucket_name,
            )

            sys.exit(1)

        else:

            logger.error(
                "Unexpected error checking bucket: %s",
                err,
            )

            sys.exit(1)

# ----------------------------------------------------------------------
# STEP 3: ALLOW PUBLIC ACCESS
# ----------------------------------------------------------------------
def disable_block_public_access(client, bucket_name: str) -> None:
    """
    Disable Block Public Access so the bucket can host
    a public static website.
    """

    try:

        client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": False,
                "IgnorePublicAcls": False,
                "BlockPublicPolicy": False,
                "RestrictPublicBuckets": False,
            },
        )

        logger.info(
            "Public access block disabled for '%s'.",
            bucket_name,
        )

    except ClientError as err:

        logger.error(
            "Failed to update public access block settings: %s",
            err,
        )

        sys.exit(1)

# ----------------------------------------------------------------------
# STEP 4: ATTACH PUBLIC READ POLICY
# ----------------------------------------------------------------------
def set_bucket_policy(client, bucket_name: str) -> None:
    """
    Allow everyone to read files in the bucket.
    """

    import json

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
            }
        ],
    }

    try:

        client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(policy),
        )

        logger.info("Public read-only bucket policy attached.")

    except ClientError as err:

        logger.error(
            "Failed to attach bucket policy: %s",
            err,
        )

        sys.exit(1)

# ----------------------------------------------------------------------
# STEP 5: ENABLE STATIC WEBSITE HOSTING
# ----------------------------------------------------------------------
def enable_static_website_hosting(client, bucket_name: str) -> None:
    """
    Enable static website hosting.
    """

    try:

        client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                "IndexDocument": {
                    "Suffix": config.INDEX_DOCUMENT
                },
                "ErrorDocument": {
                    "Key": config.ERROR_DOCUMENT
                },
            },
        )

        logger.info(
            "Static website hosting enabled."
        )

    except ClientError as err:

        logger.error(
            "Failed to enable static website hosting: %s",
            err,
        )

        sys.exit(1)

# ----------------------------------------------------------------------
# STEP 6: UPLOAD WEBSITE FILES
# ----------------------------------------------------------------------
def upload_directory(client, bucket_name: str, source_dir: str) -> int:
    """
    Upload every file inside the website folder to Amazon S3.
    """

    source_path = Path(source_dir)

    if not source_path.is_dir():
        logger.error(
            "Website source folder '%s' not found.",
            source_dir,
        )
        sys.exit(1)

    uploaded_count = 0

    banner("UPLOADING WEBSITE FILES")

    for file_path in sorted(source_path.rglob("*")):

        if file_path.is_dir():
            continue

        if file_path.name in config.EXCLUDED_FILES:
            logger.info(
                "Skipping excluded file: %s",
                file_path.name,
            )
            continue

        relative_key = file_path.relative_to(
            source_path
        ).as_posix()

        content_type, _ = mimetypes.guess_type(
            str(file_path)
        )

        if content_type is None:
            content_type = "application/octet-stream"

        try:

            client.upload_file(
                Filename=str(file_path),
                Bucket=bucket_name,
                Key=relative_key,
                ExtraArgs={
                    "ContentType": content_type
                },
            )

            uploaded_count += 1

            logger.info(
                "Uploaded: %-40s (%s)",
                relative_key,
                content_type,
            )

        except ClientError as err:

            logger.error(
                "Failed to upload %s : %s",
                relative_key,
                err,
            )

    return uploaded_count

# ----------------------------------------------------------------------
# STEP 7: BUILD WEBSITE URL
# ----------------------------------------------------------------------
def get_website_url(bucket_name: str, region: str) -> str:
    """
    Build the Amazon S3 static website URL.
    """

    if region == "us-east-1":
        return (
            f"http://{bucket_name}.s3-website-{region}.amazonaws.com"
        )

    return (
        f"http://{bucket_name}.s3-website.{region}.amazonaws.com"
    )

# ----------------------------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------------------------
def main():

    banner("AWS S3 STATIC WEBSITE DEPLOYMENT - STARTING")

    logger.info("Connecting to AWS...")

    client = get_s3_client()

    banner("STEP 1/5: BUCKET SETUP")

    create_bucket_if_not_exists(
        client,
        config.BUCKET_NAME,
        config.AWS_REGION,
    )

    banner("STEP 2/5: PUBLIC ACCESS CONFIGURATION")

    disable_block_public_access(
        client,
        config.BUCKET_NAME,
    )

    banner("STEP 3/5: BUCKET POLICY")

    set_bucket_policy(
        client,
        config.BUCKET_NAME,
    )

    banner("STEP 4/5: STATIC WEBSITE HOSTING")

    enable_static_website_hosting(
        client,
        config.BUCKET_NAME,
    )

    banner("STEP 5/5: FILE UPLOAD")

    uploaded = upload_directory(
        client,
        config.BUCKET_NAME,
        config.WEBSITE_SOURCE_DIR,
    )

    website_url = get_website_url(
        config.BUCKET_NAME,
        config.AWS_REGION,
    )

    banner("DEPLOYMENT SUCCESSFUL")

    logger.info("Files uploaded : %d", uploaded)
    logger.info("Bucket name    : %s", config.BUCKET_NAME)
    logger.info("Region         : %s", config.AWS_REGION)
    logger.info("Website URL    : %s", website_url)
    logger.info(
        "Open the URL above in your browser."
    )

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        logger.warning(
            "Deployment cancelled by user."
        )

        sys.exit(1)

    except Exception as unexpected_error:

        logger.exception(
            "Unexpected error during deployment: %s",
            unexpected_error,
        )

        sys.exit(1)



