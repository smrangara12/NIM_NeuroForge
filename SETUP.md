# Setup Guide

Quick setup instructions for AWS Resource Explorer & Service Manager.

## Quick Start

### 1. Environment Setup

```bash
# Navigate to project directory
cd C:\Users\sriha\nvidia

# Create virtual environment (if not exists)
python -m venv venv310

# Activate virtual environment
# Windows:
.\venv310\Scripts\Activate
# Linux/Mac:
source venv310/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

Edit `app.py` and update lines 15-17:

```python
AWS_ACCESS_KEY_ID = "YOUR_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_KEY"
AWS_SESSION_TOKEN = "YOUR_SESSION_TOKEN"  # Required for STS
```

### 3. Run Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Getting AWS Credentials

### Method 1: AWS SSO

```bash
aws sso login
```

Then retrieve credentials from AWS Console or CLI.

### Method 2: STS Assume Role

```bash
aws sts assume-role \
    --role-arn arn:aws:iam::ACCOUNT:role/ROLE_NAME \
    --role-session-name MySession
```

Copy the `AccessKeyId`, `SecretAccessKey`, and `SessionToken` from the output.

### Method 3: AWS Console

1. Sign in to AWS Console
2. Navigate to IAM → Security credentials
3. Create or use existing access keys
4. For temporary credentials, use the federation URL provided in the app

## Verifying Setup

1. Check credential status in the sidebar (should show ✅)
2. Try a simple search in Resource Explorer tab
3. Verify you can see resources in your account

## Troubleshooting

- **Credentials expired**: See README.md "AWS Credentials Management" section
- **No resources found**: Check Resource Explorer is enabled in your region
- **Import errors**: Ensure virtual environment is activated and dependencies installed

