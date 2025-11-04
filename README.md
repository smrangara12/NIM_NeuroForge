# AWS Resource Explorer & Service Manager

A comprehensive Streamlit web application for exploring, querying, and managing AWS resources across multiple services. Includes integrated support for NVIDIA NIM microservices documentation and deployment guides.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [AWS Credentials Management](#aws-credentials-management)
- [Troubleshooting](#troubleshooting)
- [Dependencies](#dependencies)
- [NVIDIA NIM Integration](#nvidia-nim-integration)

## 🎯 Overview

This application provides a user-friendly interface for:
- **AWS Resource Explorer**: Search and discover AWS resources across multiple regions
- **Service Management**: Query and manage resources from EC2, Athena, ElastiCache, MemoryDB, and more
- **NVIDIA NIM Integration**: Access documentation and search queries for deploying NVIDIA NIM microservices
- **Credential Management**: Built-in support for STS (Security Token Service) credentials with expiration handling

## ✨ Features

### 1. Resource Explorer Tab
- **Pre-defined Query Dropdown**: Quick access to common resource searches
  - All Resources
  - EC2 Resources
  - SageMaker Endpoints
  - ECS Services
  - EKS Clusters
  - Athena Workgroups
  - ElastiCache & MemoryDB
  - Load Balancers
  - Security Groups & Subnets
  - NVIDIA NIM Resources
  - Custom Query option
- **Multi-region Support**: Search across multiple AWS regions
- **Resource Index Listing**: View available Resource Explorer indexes
- **Detailed Resource Display**: View resources in tabular format with full details

### 2. Service Details Tab
- Query specific AWS services:
  - **EC2**: Subnets, Security Groups, DHCP Options
  - **Athena**: Workgroups, Data Catalogs
  - **ElastiCache**: Users, Cache Clusters
  - **MemoryDB**: Users, Parameter Groups
  - **Resource Explorer**: Indexes, Views

### 3. Known Resources Tab
- View all pre-configured resources from your account
- Visualize resource distribution by service and region
- Query specific known resources for detailed information

### 4. Resource Search Tab
- **Advanced Search Options**:
  - Resource Explorer search
  - Resource Groups Tagging API
  - Service-specific queries
- Pre-defined query dropdown with same options as Resource Explorer

### 5. NVIDIA NIM Search Tab
- **Resource Links**: Documentation links organized by category
  - Reasoning Models
  - Retrieval & Embedding
  - Deployment Guides
  - Overview Documentation
- **Pre-defined Search Queries**: 6 NIM-related search queries
- **AWS Resource Search**: Find AWS resources related to NIM deployments
- **Quick Reference**: Common AWS resource types and tag queries
- **Docker & Kubernetes Guides**: Deployment commands and examples

### 6. Credential Management
- **Real-time Credential Validation**: Check if credentials are valid
- **STS Credential Support**: Handles temporary credentials from:
  - AWS SSO
  - STS Assume Role
  - Federated Login
- **Expiration Handling**: Clear error messages and refresh instructions
- **Automatic Error Detection**: Detects expired tokens and provides solutions

## 🔧 Prerequisites

- Python 3.10 or higher
- AWS Account with appropriate IAM permissions
- AWS credentials (Access Key, Secret Key, Session Token)
- Required IAM permissions:
  - `resource-explorer:Search`
  - `resource-explorer:ListIndexes`
  - `resource-explorer:ListViews`
  - `tag:GetResources`
  - Service-specific permissions (ec2:Describe*, athena:List*, etc.)

## 📦 Installation

### 1. Clone or Navigate to Project Directory
```bash
cd C:\Users\sriha\nvidia
```

### 2. Create Virtual Environment
```bash
python -m venv venv310
```

### 3. Activate Virtual Environment

**Windows:**
```bash
.\venv310\Scripts\Activate
```

**Linux/Mac:**
```bash
source venv310/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure AWS Credentials
Edit `app.py` and update lines 15-17 with your AWS credentials:
```python
AWS_ACCESS_KEY_ID = "your_access_key"
AWS_SECRET_ACCESS_KEY = "your_secret_key"
AWS_SESSION_TOKEN = "your_session_token"  # Required for STS credentials
```

## ⚙️ Configuration

### AWS Credentials

The application uses AWS credentials configured directly in the code. Update the following variables in `app.py`:

```python
AWS_ACCESS_KEY_ID = "ASIARWZIDBVY2EOD7I3R"
AWS_SECRET_ACCESS_KEY = "SIZ8Iy5cG9CfwsFlfCxcdPRFnSxpfbrU7o1qfJBw"
AWS_SESSION_TOKEN = "IQoJb3JpZ2luX2VjEIz..."  # Required for temporary credentials
```

**Note**: For security, consider using environment variables or AWS credentials file instead of hardcoding.

### Source URL

The `SOURCE_URL` variable contains the AWS Console federation URL for quick access to the AWS Management Console.

### Known Resources

The `KNOWN_RESOURCES` list contains pre-configured resources that can be queried directly. You can add or modify resources in this list.

## 🚀 Usage

### Starting the Application

1. Activate your virtual environment:
   ```bash
   .\venv310\Scripts\Activate
   ```

2. Run Streamlit:
   ```bash
   streamlit run app.py
   ```

3. The application will open in your default web browser at `http://localhost:8501`

### Using the Application

1. **Check Credentials**: The sidebar shows credential status. If expired, follow the refresh instructions.

2. **Select Region**: Choose your default AWS region from the sidebar dropdown.

3. **Navigate Tabs**: Use the tabs to access different features:
   - **Resource Explorer**: Search AWS resources
   - **Service Details**: Query specific services
   - **Known Resources**: View pre-configured resources
   - **Resource Search**: Advanced search options
   - **NVIDIA NIM Search**: NIM documentation and resources

4. **Execute Queries**: Select queries from dropdowns or enter custom queries, then click search buttons.

## 📁 Project Structure

```
nvidia/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── venv310/              # Virtual environment (created during setup)
```

## 🔐 AWS Credentials Management

### STS Credentials Overview

This application is designed to work with **AWS Security Token Service (STS)** temporary credentials. These credentials are obtained through:

- **AWS SSO (Single Sign-On)**
- **STS Assume Role**
- **Federated Login**

### Credential Expiration

Temporary credentials expire after:
- **SSO**: 1-12 hours (configurable)
- **Assume Role**: 1 hour (default, configurable)
- **Federated Login**: Varies by provider

### Refreshing Expired Credentials

When credentials expire, the application provides clear error messages and instructions. Refresh options:

#### Option 1: AWS SSO
```bash
aws sso login
```
Then retrieve new credentials and update `app.py` lines 15-17.

#### Option 2: STS Assume Role
```bash
aws sts assume-role \
    --role-arn arn:aws:iam::ACCOUNT:role/ROLE_NAME \
    --role-session-name MySession
```
Copy the output credentials to `app.py`.

#### Option 3: Federated Login
Use the Source URL in the sidebar to sign in and get new credentials from the AWS Console.

#### Option 4: Verify Credentials
```bash
aws sts get-caller-identity
```

### Credential Status Indicator

The sidebar shows credential status:
- ✅ **Green**: Credentials are valid
- ⚠️ **Red**: Credentials are expired or invalid

## 🔍 Troubleshooting

### Common Issues

#### 1. ExpiredTokenException
**Error**: `The security token included in the request is expired`

**Solution**: 
- Check the sidebar for credential status
- Follow the refresh instructions in the "Credential Management" section
- Update credentials in `app.py` lines 15-17
- Restart the Streamlit app

#### 2. AccessDeniedException
**Error**: `Access denied when calling [Service]`

**Solution**:
- Verify IAM permissions for the required services
- Check that your role has necessary permissions
- Ensure Resource Explorer is enabled in your region

#### 3. No Resources Found
**Solution**:
- Try a broader query (e.g., `*` instead of specific service)
- Check different regions
- Verify Resource Explorer indexes are created in your region
- Check resource tagging if using tag-based queries

#### 4. ModuleNotFoundError
**Error**: `No module named 'boto3'`

**Solution**:
```bash
pip install -r requirements.txt
```

#### 5. Streamlit Not Starting
**Solution**:
- Ensure virtual environment is activated
- Check Python version (3.10+)
- Verify Streamlit is installed: `pip show streamlit`

## 📚 Dependencies

### Core Dependencies

- **streamlit** (>=1.28.0): Web application framework
- **boto3** (>=1.28.0): AWS SDK for Python
- **pandas** (>=2.0.0): Data manipulation and display
- **botocore** (>=1.31.0): Low-level AWS service access

### Installation

All dependencies are listed in `requirements.txt`. Install with:
```bash
pip install -r requirements.txt
```

## 🚀 NVIDIA NIM Integration

### Overview

The application includes comprehensive support for NVIDIA NIM microservices, including:

- **Documentation Links**: Access to official NVIDIA NIM documentation
- **Search Queries**: Pre-defined queries for finding NIM-related AWS resources
- **Deployment Guides**: Docker and Kubernetes/Helm deployment examples

### Available Resources

#### Documentation Categories

1. **Reasoning Models**
   - Use Reasoning Models with NVIDIA NIM for LLMs
   - Chain-of-thought vs concise reasoning modes

2. **Retrieval & Embedding**
   - Retriever NIMs (NeMo Retriever text embedding NIM)
   - Semantic search and retrieval capabilities

3. **Deployment**
   - Deploy NIM Microservices
   - Deployment Guide for NVIDIA NIM for LLMs

4. **Overview**
   - NVIDIA NIM Microservices for Accelerated AI Inference

### Pre-defined Search Queries

1. "NVIDIA NIM reasoning mode large language models"
2. "NVIDIA NIM reasoning model chain of thought prompt NIM for LLMs"
3. "NeMo Retriever Text Embedding NIM semantic search retrieval NIM API"
4. "Deploy NVIDIA NIM microservice Helm Kubernetes NIMPipeline NIMService"
5. "NVIDIA NIM text embedding NIM NV-EmbedQA-4 model"
6. "NVIDIA NIM inference microservice large language model Docker run nvcr.io/nim"

### Docker Commands

Example commands for running NIM containers:
```bash
# LLM Container
docker run --gpus all -it --rm \
    -p 8000:8000 \
    -v $(pwd)/models:/models \
    nvcr.io/nim/meta/llama-3-70b-instruct:latest

# Embedding Container
docker run --gpus all -it --rm \
    -p 8000:8000 \
    -v $(pwd)/models:/models \
    nvcr.io/nim/nvidia/nv-embedqa-4:latest
```

### Kubernetes/Helm Deployment

```bash
# Add NVIDIA Helm repository
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update

# Install NIM Service
helm install nim-service nvidia/nim \
    --set service.type=LoadBalancer \
    --set service.port=8000 \
    --namespace nvidia-nim
```

## 📝 Code Structure

### Main Components

1. **AWS Session Management** (`get_aws_session()`)
   - Creates boto3 session with provided credentials
   - Cached for performance

2. **Credential Validation**
   - Real-time credential checking using STS
   - Status display in sidebar

3. **Resource Explorer Integration**
   - Search functionality across multiple regions
   - Index listing and management
   - Pagination support

4. **Service-Specific Queries**
   - Individual service clients
   - Error handling per service
   - Resource type-specific operations

5. **NVIDIA NIM Integration**
   - Resource links management
   - Search query definitions
   - Documentation access

## 🔒 Security Considerations

1. **Credentials**: Currently hardcoded in `app.py`. For production:
   - Use environment variables
   - Implement AWS credentials file
   - Consider AWS Secrets Manager

2. **Session Tokens**: Temporary credentials expire - implement refresh mechanism

3. **IAM Permissions**: Follow principle of least privilege

4. **Network**: If deploying, ensure proper network security

## 📖 Additional Resources

### AWS Documentation
- [AWS Resource Explorer](https://docs.aws.amazon.com/resource-explorer/)
- [AWS STS](https://docs.aws.amazon.com/STS/)
- [AWS SSO](https://docs.aws.amazon.com/singlesignon/)

### NVIDIA NIM Documentation
- [NVIDIA NIM Overview](https://docs.api.nvidia.com/nim/overview)
- [NIM Deployment Guide](https://docs.nvidia.com/nim/llm/deployment-guide/index.html)
- [NeMo Retriever NIM](https://docs.api.nvidia.com/nim/retriever/overview)

## 🤝 Contributing

To contribute to this project:

1. Update credentials in `app.py`
2. Test functionality across different regions
3. Document any new features or changes
4. Ensure error handling is comprehensive

## 📄 License

This project is for internal use. Ensure compliance with AWS and NVIDIA usage policies.

## 🆘 Support

For issues or questions:

1. Check the **Troubleshooting** section
2. Review credential status in the sidebar
3. Verify AWS permissions
4. Check Resource Explorer is enabled in your region

## 📅 Version History

- **v1.0**: Initial release with Resource Explorer, Service Management, and NVIDIA NIM integration
- Includes STS credential management and expiration handling

---

**Last Updated**: 2025-11-03

**Maintained by**: NVIDIA Project Team

