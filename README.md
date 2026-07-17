# 🚀 CloudDeploy – Automated Static Website Hosting on Amazon S3

![AWS](https://img.shields.io/badge/AWS-S3-orange)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![boto3](https://img.shields.io/badge/boto3-AWS_SDK-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📌 Overview

CloudDeploy is a Python automation project that deploys a static website to Amazon S3 using the AWS SDK for Python (boto3).

Instead of manually creating buckets, configuring permissions, enabling website hosting, and uploading files through the AWS Console, everything is completed automatically using a single Python command.

This project demonstrates Infrastructure Automation using Python and AWS Free Tier services.

---

# ✨ Features

- Automatic S3 bucket creation
- Bucket existence check
- Public access configuration
- Public bucket policy attachment
- Static website hosting configuration
- Automatic website file upload
- MIME type detection
- Structured logging
- Error handling
- Safe re-deployment
- Responsive demo website

---

# 🏗 AWS Services Used

- Amazon S3
- IAM
- AWS CLI
- boto3 SDK

---

# 🛠 Technologies

- Python
- boto3
- HTML5
- CSS3
- JavaScript
- AWS CLI

---

# 📂 Project Structure

```
StaticWebsiteAutomation/

│
├── website/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── assets/
│
├── upload_website.py
├── config.py
├── requirements.txt
├── upload_log.log
├── README.md
└── .gitignore
```

---

# ⚙ Workflow

Developer

↓

Python Script

↓

AWS boto3 SDK

↓

Amazon S3 Bucket

↓

Website Files Uploaded

↓

Static Website Hosting Enabled

↓

Live Website URL

---

# 🚀 Deployment

Clone repository

```bash
git clone https://github.com/yourusername/StaticWebsiteAutomation.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure

```python
BUCKET_NAME="your-bucket-name"
AWS_REGION="ap-south-1"
```

Run

```bash
python upload_website.py
```


---

# 📊 Project Flow

1. Connect to AWS
2. Verify credentials
3. Create bucket
4. Configure public access
5. Attach bucket policy
6. Enable website hosting
7. Upload website files
8. Generate website URL

---

# 🎯 Learning Outcomes

- AWS SDK (boto3)
- Amazon S3 Automation
- Static Website Hosting
- IAM Permissions
- Bucket Policies
- MIME Types
- Python Logging
- AWS CLI Integration
- Infrastructure Automation


---

# 🔮 Future Enhancements

- CloudFront CDN
- HTTPS with ACM
- Route53 Domain Integration
- GitHub Actions CI/CD
- Multi-environment deployment
- Automatic bucket cleanup

---

# 📷 Project Screenshots

---

## 1️⃣ Project Folder

**Description**

Complete project structure containing the Python automation script, website files, configuration file, requirements, logging, and supporting assets.

Screenshot

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/caacb188-2825-45c2-b89c-a04a3b44390b" />

---

## 2️⃣ Amazon S3 Bucket

**Description**

Amazon S3 bucket created automatically by the Python automation script. The bucket contains website files and the assets directory.

Screenshot

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c8992724-b69f-47ba-aba7-f03012206624" />


---

## 3️⃣ Live Website

**Description**

Homepage of the deployed CloudDeploy application hosted on Amazon S3 Static Website Hosting.

Screenshot

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1aa39dd6-c233-4275-9aaf-6eaeb71f2589" />

---

## 4️⃣ Project Workflow

**Description**

Illustrates the automated deployment workflow from local development to the live S3 website.

Screenshot

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9c7cdef4-5541-45f1-971f-8867c48ffb09" />


---

## 5️⃣ AWS Architecture

**Description**

Shows how the developer interacts with the Python script, boto3 SDK, Amazon S3, and static website hosting.

Screenshot

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ebe5b27b-0e6c-46b0-a8fa-d0c7b902c827" />

---

## 6️⃣ Deployment Guide

**Description**

Displays the commands required to clone the repository, install dependencies, and deploy the website automatically.

Screenshot

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/584d37bd-d12b-44b9-a22c-7d0ec7eb71fc" />

---

---

# Result

After executing

```bash
python upload_website.py
```
<img width="1370" height="651" alt="image" src="https://github.com/user-attachments/assets/830b46a6-f12e-439f-80c8-7328bc3343f5" />

the automation:

- Connects to AWS
- Creates an S3 bucket
- Configures public access
- Enables static website hosting
- Uploads all website files
- Generates the live website URL
