"""
config.py
----------
Central configuration file for the S3 Static Website Automation project.
"""

# ----------------------------------------------------------------------
# AWS CONFIGURATION
# ----------------------------------------------------------------------

# Must be globally unique across ALL AWS accounts.
# Example:
# clouddeploy-xyz-2026-12345
BUCKET_NAME = "my-static-website-bucket-change-me-123"

# Your AWS Region
AWS_REGION = "ap-south-1"

# AWS CLI Profile
AWS_PROFILE = "default"

# ----------------------------------------------------------------------
# WEBSITE HOSTING CONFIGURATION
# ----------------------------------------------------------------------

INDEX_DOCUMENT = "index.html"

ERROR_DOCUMENT = "index.html"

# ----------------------------------------------------------------------
# LOCAL PROJECT CONFIGURATION
# ----------------------------------------------------------------------

WEBSITE_SOURCE_DIR = "website"

EXCLUDED_FILES = {
    ".DS_Store",
    "Thumbs.db",
    ".gitkeep",
}

# ----------------------------------------------------------------------
# LOGGING CONFIGURATION
# ----------------------------------------------------------------------

LOG_FILE = "upload_log.log"

LOG_LEVEL = "INFO"