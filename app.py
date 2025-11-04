"""
AWS Resource Explorer and Service Management App
Uses provided AWS credentials to query and manage AWS resources across multiple services.
"""

import streamlit as st
import boto3
import json
import os
import pandas as pd
from botocore.exceptions import ClientError
from datetime import datetime

# AWS Credentials
AWS_ACCESS_KEY_ID = "ASIARWZIDBVY2EOD7I3R"
AWS_SECRET_ACCESS_KEY = "SIZ8Iy5cG9CfwsFlfCxcdPRFnSxpfbrU7o1qfJBw"
AWS_SESSION_TOKEN = "IQoJb3JpZ2luX2VjEIz//////////wEaCXVzLXdlc3QtMiJHMEUCIDT2a22GYK1S2c9Evb/HRVIAhQdWsjq2MBwBfzAylVhQAiEAv6NkbuznXhH3mf+sPasM0ojPCxXfxBb9P5KnM6jv1zIqoQIIVRACGgwxMTc2NTg4MTU4NTciDBtVacVPB2/lHgCluSr+AVkerK75BUCg9TnsJYsI/uzBJXt7irBP5VCcU/yE4Q6z9BivLXBiCZaYzFY6JfVcR9ixulvzLtRjXVpudO3nY9L2iT+KxsuLufhJh6Mo2Pt2VrQSWD/R/df94KUesARECQvex27IziFo0gCoGK1+Fot/YBrykHsL8Ojs4Efk1zHWmdSUsdXtVIZKLmj7WgLZGbT4KyQZcGWXjdFFAEyv8ecNOpro3c9ZrO4afYsJ2v9F9/oX4yeo+f/0sSjrajVVFH6EkxNo+YetKlCqBwhk6x50ny7rU+FPnl2Pz5IFLL2tCepW7R1Za5l/jFqN1HwoB5H+MsBzZGcp+9fm61cVMIDGoMgGOp0BOBK0OMAmAA++i/W4A7RPqe9e+6xvVG81d65uNVRIyzzk/wK4JgUHSTd1+yQDCbUJMX2qVfAxEq6pdPUHW4Hu0rdeR0GoEUT37wHbBQRH/qbNfNky+xhBVw+D5UD7RPtzypOdRx6txTkb704YmuL+V5KgbwMyt3NXXChg9o6MhMqeGuu1bqMSe/j3yNYbKN3ZQeWG1vGrPWwBORpprA=="

# Source URL
SOURCE_URL = "https://signin.aws.amazon.com/federation?Action=login&SigninToken=b9tfFOb9EYmMF31IDVfN1TM0uoCxODllCjc4iMTzJwQxXPyzdV8hWV3AEYG1dAt8F_3_tChWO7PiMhEDjeJdPmu5cbp0KcAiafyao8OhZ4Ms3_jVHW2KluC287n3lc8V0igiUY3-2qdbkEEaGxibCmiJeWPvtJqNAqX9VIgCc88Y3oiCKZ0lpReAUOuJAdLCKxTFre3-fuvPSNKitb5H5IrD0DJGwPVGNtkDtSTk2mzD9x1_KGsJHAiw2FUWJyKGTaNILyp88eChLyQPN8dNUQpVqNm9DPgex7m_WqlaKx0FHnc_3Xb8AMFsMO0JHOEGffjGxc7Y_EaEzSfhOgCZwW6jCUKMxNR5m4Q3kxvv5XKOtiLeV_u73f5f4GxGstfAW_xrEpwP8h6jIFrlN7fuy7eoLopJcP5_loShchE1uqVfRJozQ8IqSJqtFo9c7DLI5RGfB20Brx-ovhLTo73MG1LIxXzY4VB1AnW3Uv0fGo7-4Rzp62anU44XO9egs2nVUDvmmT8UMAUYr6efdxgDIV-4yjE3qKL4g41nWMdI7HGFdWsGuE5OGV452tX6b53X-g_3zadDTS9JiHSQ9X8OEExq43k9AhZGzeA-owSP9ucgpwLE2y95gqZVnkI3hg5C8dtMu63kS9fuzsGeqCpk_BSLoSg9McFfjvFCXW2F2OOEyIhFc9sAJz73AsEg8JgYEeGXXzx57HwTAjFRYX2vyrI1pbj8zqHj6kNKthSGx6aGzLupWA2vLcZFeHpkA1yCwP9A2LllErdhsMoro-ntOq8DI6bBlYZh4WzMGy0jKbmth7_ycD4okag0I9GWXZOgn9dao3vWuX2H2I7LNI495gvmqdUxBNphqcaKbRAjhvwd1heibmTx-LjOPJRQ6aUh6Qp7SpDpaZ-E3qw36GTVmRfIZLISgcKZ-nLhexEetHVku-rLXsQgaYm6NoFy5uF6qCgEWh5NCkzFNF5RX4hZWFbqqWpo3JVxaCIKVPTQX7AIl3n6ijIZZLldR58q2zLMbVooQ_7MkO4kc9KeiLTI_18ePfmcDP5nBmhP3cYrwXXqWdaByL8dK4zoQiLHjkVbbPWoxTPoRSDF8ailv5_JOTCta9zFRcWT7yYB6FmhXUa6a0WkuhrDLfGP8KAbLKaQxA0yqHCs_FyM215T7L7Meu-klh0-JFl6Ht0QqBlCrKWnhXbKGcfUgSCI-iARq2Tb6tIHjgQwz0ssGn7hykK8hsJuxunfYqdkgEHU-klY3225J49o2TpXteJFfSfBloQQleKdk4uVpAYfv_voAnkscalbGCPFMa--tN322kxAdUxOrKLSg02pvEIimq5CADbhFWbtWG-sQMDmF8HtArOvV9si0UAqSxb5DJN9CnEa1gPKyNTw75gOt4CXTyXRi0KW6TIxIPkdXvfK_2f6HkfZHKwFhkxSzfWLFxmybIMxkLblKp33ugna56U5Gk3H&Issuer=https%3A%2F%2Fnvidia.vocareum.com&Destination=https%3A%2F%2Fconsole.aws.amazon.com%2Fconsole%2Fhome%3Fregion%3Dus-east-1"

# Known Resources from provided list
KNOWN_RESOURCES = [
    {"identifier": "subnet-0a74afb326ddda367", "service": "ec2", "resource_type": "ec2:subnet", "region": "sa-east-1"},
    {"identifier": "primary", "service": "athena", "resource_type": "athena:workgroup", "region": "ap-northeast-1"},
    {"identifier": "AwsDataCatalog", "service": "athena", "resource_type": "athena:datacatalog", "region": "us-east-1"},
    {"identifier": "default", "service": "elasticache", "resource_type": "elasticache:user", "region": "us-east-1"},
    {"identifier": "sgr-0d30f10d25579c376", "service": "ec2", "resource_type": "ec2:security-group-rule", "region": "eu-west-2"},
    {"identifier": "default", "service": "memorydb", "resource_type": "memorydb:user", "region": "ca-central-1"},
    {"identifier": "458b928a-9f6f-43bf-bb2a-2cbacb524c54", "service": "resource-explorer-2", "resource_type": "resource-explorer-2:index", "region": "eu-central-1"},
    {"identifier": "f70c26f6-b4e7-496b-a011-0ad8817eea66", "service": "resource-explorer-2", "resource_type": "resource-explorer-2:index", "region": "eu-west-2"},
    {"identifier": "default.memorydb-redis6", "service": "memorydb", "resource_type": "memorydb:parametergroup", "region": "ap-northeast-2"},
    {"identifier": "default.memorydb-valkey7.search", "service": "memorydb", "resource_type": "memorydb:parametergroup", "region": "eu-central-1"},
    {"identifier": "subnet-02906706a6d2312b8", "service": "ec2", "resource_type": "ec2:subnet", "region": "us-east-1"},
    {"identifier": "default", "service": "elasticache", "resource_type": "elasticache:user", "region": "eu-west-3"},
    {"identifier": "default", "service": "memorydb", "resource_type": "memorydb:user", "region": "us-west-2"},
    {"identifier": "sgr-079efc7555f0e6f87", "service": "ec2", "resource_type": "ec2:security-group-rule", "region": "ap-south-1"},
    {"identifier": "subnet-04f1356619a14565e", "service": "ec2", "resource_type": "ec2:subnet", "region": "us-west-2"},
    {"identifier": "sg-0c3ad842304a0c8ae", "service": "ec2", "resource_type": "ec2:security-group", "region": "eu-west-2"},
    {"identifier": "dopt-0f48d4a6f3aa90ab5", "service": "ec2", "resource_type": "ec2:dhcp-options", "region": "ap-southeast-2"},
]

st.set_page_config(page_title="AWS Resource Manager", layout="wide")
st.title("AWS Resource Explorer & Service Manager")
st.markdown("**Using provided AWS credentials to query and manage AWS resources**")

# Initialize AWS session with provided credentials
@st.cache_resource
def get_aws_session(region_name="us-east-1"):
    """Create boto3 session with provided credentials"""
    try:
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=region_name
        )
        return session
    except Exception as e:
        st.error(f"Failed to create AWS session: {e}")
        return None

# Sidebar configuration
st.sidebar.header("Configuration")
default_region = st.sidebar.selectbox(
    "Default Region",
    options=["us-east-1", "us-west-2", "eu-west-2", "ap-northeast-1", "sa-east-1", "eu-central-1", "ca-central-1", "ap-south-1", "ap-southeast-2", "eu-west-3", "ap-northeast-2"],
    index=0
)

session = get_aws_session(default_region)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Source URL:** [AWS Console]({SOURCE_URL})")
st.sidebar.markdown(f"**Session Region:** {default_region}")

# Credential Refresh Section
st.sidebar.markdown("---")
st.sidebar.header("🔑 Credential Management")

# Check if credentials are expired
try:
    if session:
        sts_client = session.client("sts", region_name=default_region)
        identity = sts_client.get_caller_identity()
        st.sidebar.success("✅ Credentials are valid")
        st.sidebar.caption(f"Account: {identity.get('Account', 'Unknown')}")
except ClientError as e:
    error_code = e.response.get('Error', {}).get('Code', '')
    if error_code in ['ExpiredTokenException', 'AccessDeniedException']:
        st.sidebar.error("⚠️ **Credentials Expired**")
    else:
        st.sidebar.warning(f"⚠️ Credential check failed: {error_code}")

with st.sidebar.expander("📋 How to Refresh STS Credentials"):
    st.markdown("""
    ### **🔑 STS Credentials Refresh Options**
    
    **Your credentials are temporary and expire after 1-12 hours** (depending on how they were obtained).
    
    ---
    
    ### **Option 1: AWS SSO (Single Sign-On)**
    If using AWS SSO, refresh your session:
    ```bash
    aws sso login
    ```
    Then get new temporary credentials:
    ```bash
    aws sso get-role-credentials \\
        --role-name YOUR_ROLE \\
        --account-id YOUR_ACCOUNT \\
        --access-token $(aws sso get-credential-process-output)
    ```
    Or simply use the AWS Console URL to get new credentials.
    
    ---
    
    ### **Option 2: Assume Role (STS)**
    If using `sts assume-role`, run again:
    ```bash
    aws sts assume-role \\
        --role-arn arn:aws:iam::ACCOUNT:role/ROLE_NAME \\
        --role-session-name MySession
    ```
    
    Copy the output and update in `app.py`:
    ```python
    AWS_ACCESS_KEY_ID = "ASIA..."
    AWS_SECRET_ACCESS_KEY = "..."
    AWS_SESSION_TOKEN = "..."
    ```
    
    ---
    
    ### **Option 3: Federated Login**
    If using federated login (e.g., via AWS Console URL):
    1. Click the **Source URL** link above
    2. Sign in via the federation URL
    3. Get new temporary credentials from the console
    4. Update lines 15-17 in `app.py`
    
    ---
    
    ### **Option 4: Update Credentials in Code**
    1. Get new STS credentials from:
       - AWS Console (after signing in)
       - `aws sts assume-role` command
       - `aws sso login` followed by credential retrieval
    2. Update `app.py` lines 15-17:
       ```python
       AWS_ACCESS_KEY_ID = "new_access_key"
       AWS_SECRET_ACCESS_KEY = "new_secret_key"
       AWS_SESSION_TOKEN = "new_session_token"
       ```
    3. **Restart the Streamlit app** (important!)
    
    ---
    
    ### **Option 5: Verify Credentials**
    Check if your credentials are valid:
    ```bash
    aws sts get-caller-identity
    ```
    
    If expired, you'll see:
    ```
    An error occurred (ExpiredTokenException) when calling the GetCallerIdentity operation
    ```
    
    ---
    
    **💡 Tip**: Temporary credentials typically expire after:
    - SSO: 1-12 hours
    - Assume Role: 1 hour (default)
    - Federated Login: Varies by provider
    """)

st.sidebar.markdown("---")

# NVIDIA NIM Resource Links and Search Queries
NVIDIA_NIM_RESOURCES = [
    {
        "title": "Use Reasoning Models with NVIDIA NIM for LLMs",
        "description": "Describes how NIM supports reasoning-mode prompts (chain-of-thought vs concise) for LLMs",
        "category": "Reasoning Models",
        "url": "https://docs.nvidia.com/nim/llm/guides/reasoning-mode.html"
    },
    {
        "title": "Retriever NIMs (NeMo Retriever text embedding NIM)",
        "description": "Describes embedding + reranking NIM services for retrieval/semantic-search",
        "category": "Retrieval & Embedding",
        "url": "https://docs.api.nvidia.com/nim/retriever/overview"
    },
    {
        "title": "Deploy NIM Microservices",
        "description": "Gives steps and deployment environments for NIM",
        "category": "Deployment",
        "url": "https://docs.nvidia.com/nim/llm/deployment-guide/index.html"
    },
    {
        "title": "Deployment Guide for NVIDIA NIM for LLMs",
        "description": "Comprehensive deployment guide for NIM LLM microservices",
        "category": "Deployment",
        "url": "https://docs.nvidia.com/nim/llm/deployment-guide/index.html"
    },
    {
        "title": "NVIDIA NIM Microservices for Accelerated AI Inference",
        "description": "Overview of NIM, models, APIs, and deployment",
        "category": "Overview",
        "url": "https://docs.api.nvidia.com/nim/overview"
    }
]

NVIDIA_NIM_SEARCH_QUERIES = [
    "NVIDIA NIM reasoning mode large language models",
    "NVIDIA NIM reasoning model chain of thought prompt NIM for LLMs",
    "NeMo Retriever Text Embedding NIM semantic search retrieval NIM API",
    "Deploy NVIDIA NIM microservice Helm Kubernetes NIMPipeline NIMService",
    "NVIDIA NIM text embedding NIM NV-EmbedQA-4 model",
    "NVIDIA NIM inference microservice large language model Docker run nvcr.io/nim"
]

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Resource Explorer", "Service Details", "Known Resources", "Resource Search", "NVIDIA NIM Search"])

# Tab 1: Resource Explorer
with tab1:
    st.header("AWS Resource Explorer")
    
    if session:
        col1, col2 = st.columns(2)
        
        with col1:
            re_region = st.selectbox(
                "Resource Explorer Region",
                options=["us-east-1", "eu-west-2", "eu-central-1"],
                index=0,
                key="re_region"
            )
        
        with col2:
            view_name = st.text_input("View Name (optional)", value="")
        
        # Default queries for dropdown
        DEFAULT_QUERIES = {
            "All Resources": "*",
            "EC2 Resources": "ec2",
            "SageMaker Endpoints": "sagemaker endpoint",
            "ECS Services": "ecs service",
            "EKS Clusters": "eks cluster",
            "Athena Workgroups": "athena workgroup",
            "ElastiCache": "elasticache",
            "MemoryDB": "memorydb",
            "Load Balancers": "elasticloadbalancing loadbalancer",
            "Security Groups": "ec2 security-group",
            "Subnets": "ec2 subnet",
            "NVIDIA NIM Resources": "tag:Application=*NIM* OR tag:Application=*nvidia* OR sagemaker endpoint",
            "NeuroForge Application": "tag:Application=NeuroForge",
            "Custom Query": "CUSTOM"
        }
        
        query_option = st.selectbox(
            "Select Search Query",
            options=list(DEFAULT_QUERIES.keys()),
            index=0,
            help="Select a predefined query or choose 'Custom Query' to enter your own"
        )
        
        if query_option == "Custom Query":
            search_query = st.text_input(
                "Custom Search Query",
                value="*",
                help="Enter your custom query (e.g., 'ec2', 'tag:Application=NeuroForge', etc.)"
            )
        else:
            search_query = DEFAULT_QUERIES[query_option]
            st.info(f"Using query: **{search_query}**")
        
        if st.button("Search Resources", key="search_re"):
            try:
                re_client = session.client("resource-explorer-2", region_name=re_region)
                
                # List indexes first
                try:
                    indexes = re_client.list_indexes()
                    st.info(f"Found {len(indexes.get('Indexes', []))} Resource Explorer index(es)")
                    
                    if indexes.get('Indexes'):
                        index_arns = [idx['Arn'] for idx in indexes['Indexes']]
                        st.json(indexes)
                except ClientError as e:
                    error_code = e.response.get('Error', {}).get('Code', '')
                    if error_code in ['ExpiredTokenException', 'AccessDeniedException']:
                        st.error("⚠️ **STS Credentials Expired**")
                        st.warning("Your AWS Security Token Service (STS) credentials have expired. These temporary credentials from assume-role, SSO, or federated login typically expire after 1-12 hours.")
                        with st.expander("🔧 How to Refresh STS Credentials"):
                            st.markdown("""
                            **Quick Fix Options:**
                            
                            **1. AWS SSO**
                            ```bash
                            aws sso login
                            ```
                            Then get new credentials and update `app.py` lines 15-17.
                            
                            **2. Assume Role (STS)**
                            ```bash
                            aws sts assume-role \\
                                --role-arn arn:aws:iam::ACCOUNT:role/ROLE \\
                                --role-session-name Session
                            ```
                            Copy the new credentials from the output.
                            
                            **3. Federated Login**
                            Use the Source URL in the sidebar to sign in and get new credentials.
                            
                            **4. Update Credentials in Code**
                            - Update lines 15-17 in `app.py` with new credentials
                            - Restart the Streamlit app
                            
                            **📋 See Sidebar**: "Credential Management" section has detailed instructions for all methods.
                            """)
                    else:
                        st.warning(f"Could not list indexes: {e}")
                
                # Search resources
                try:
                    paginator = re_client.get_paginator("search")
                    resources = []
                    
                    kwargs = {"QueryString": search_query, "MaxResults": 50}
                    if view_name:
                        kwargs["ViewArn"] = view_name
                    
                    for page in paginator.paginate(**kwargs):
                        items = page.get("Items", [])
                        if items:
                            resources.extend(items)
                    
                    if resources:
                        st.success(f"Found {len(resources)} resource(s)")
                        
                        # Display as DataFrame
                        df_data = []
                        for r in resources:
                            df_data.append({
                                "ARN": r.get("Arn", ""),
                                "Service": r.get("Service", ""),
                                "Resource Type": r.get("ResourceType", ""),
                                "Region": r.get("Region", ""),
                                "Account ID": r.get("AccountId", ""),
                                "Title": r.get("Title", "")
                            })
                        
                        if df_data:
                            df = pd.DataFrame(df_data)
                            st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No resources found for the query.")
                        
                except ClientError as e:
                    error_code = e.response.get('Error', {}).get('Code', '')
                    if error_code in ['ExpiredTokenException', 'AccessDeniedException']:
                        st.error("⚠️ **STS Credentials Expired**")
                        st.warning("Your AWS Security Token Service (STS) credentials have expired. These temporary credentials from assume-role, SSO, or federated login typically expire after 1-12 hours.")
                        with st.expander("🔧 How to Refresh STS Credentials"):
                            st.markdown("""
                            **Quick Fix Options:**
                            
                            **1. AWS SSO**
                            ```bash
                            aws sso login
                            ```
                            Then get new credentials and update `app.py` lines 15-17.
                            
                            **2. Assume Role (STS)**
                            ```bash
                            aws sts assume-role \\
                                --role-arn arn:aws:iam::ACCOUNT:role/ROLE \\
                                --role-session-name Session
                            ```
                            Copy the new credentials from the output.
                            
                            **3. Federated Login**
                            Use the Source URL in the sidebar to sign in and get new credentials.
                            
                            **4. Update Credentials in Code**
                            - Update lines 15-17 in `app.py` with new credentials
                            - Restart the Streamlit app
                            
                            **📋 See Sidebar**: "Credential Management" section has detailed instructions for all methods.
                            """)
                    else:
                        st.error(f"Resource Explorer search failed: {e}")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("AWS session not available")

# Tab 2: Service Details
with tab2:
    st.header("Service Details")
    
    if session:
        service = st.selectbox(
            "Select Service",
            options=["EC2", "Athena", "ElastiCache", "MemoryDB", "Resource Explorer"],
            index=0
        )
        
        service_region = st.selectbox(
            "Service Region",
            options=["us-east-1", "us-west-2", "eu-west-2", "ap-northeast-1", "sa-east-1"],
            index=0,
            key="service_region"
        )
        
        if st.button("Get Service Details"):
            try:
                if service == "EC2":
                    ec2_client = session.client("ec2", region_name=service_region)
                    
                    # Get subnets
                    subnets = ec2_client.describe_subnets()
                    st.subheader("Subnets")
                    if subnets.get("Subnets"):
                        st.json(subnets["Subnets"][:5])  # Show first 5
                    
                    # Get security groups
                    sgs = ec2_client.describe_security_groups()
                    st.subheader("Security Groups")
                    if sgs.get("SecurityGroups"):
                        st.json(sgs["SecurityGroups"][:5])
                    
                    # Get DHCP options
                    dhcp_opts = ec2_client.describe_dhcp_options()
                    st.subheader("DHCP Options")
                    if dhcp_opts.get("DhcpOptions"):
                        st.json(dhcp_opts["DhcpOptions"])
                
                elif service == "Athena":
                    athena_client = session.client("athena", region_name=service_region)
                    
                    # List workgroups
                    workgroups = athena_client.list_work_groups()
                    st.subheader("Athena Workgroups")
                    st.json(workgroups)
                    
                    # List data catalogs
                    catalogs = athena_client.list_data_catalogs()
                    st.subheader("Data Catalogs")
                    st.json(catalogs)
                
                elif service == "ElastiCache":
                    elasticache_client = session.client("elasticache", region_name=service_region)
                    
                    # List users
                    try:
                        users = elasticache_client.describe_users()
                        st.subheader("ElastiCache Users")
                        st.json(users)
                    except ClientError as e:
                        st.warning(f"Could not list users: {e}")
                    
                    # List clusters
                    try:
                        clusters = elasticache_client.describe_cache_clusters()
                        st.subheader("Cache Clusters")
                        if clusters.get("CacheClusters"):
                            st.json(clusters["CacheClusters"][:5])
                    except ClientError as e:
                        st.warning(f"Could not list clusters: {e}")
                
                elif service == "MemoryDB":
                    memorydb_client = session.client("memorydb", region_name=service_region)
                    
                    # List users
                    try:
                        users = memorydb_client.describe_users()
                        st.subheader("MemoryDB Users")
                        st.json(users)
                    except ClientError as e:
                        st.warning(f"Could not list users: {e}")
                    
                    # List parameter groups
                    try:
                        param_groups = memorydb_client.describe_parameter_groups()
                        st.subheader("Parameter Groups")
                        st.json(param_groups)
                    except ClientError as e:
                        st.warning(f"Could not list parameter groups: {e}")
                
                elif service == "Resource Explorer":
                    re_client = session.client("resource-explorer-2", region_name=service_region)
                    
                    # List indexes
                    indexes = re_client.list_indexes()
                    st.subheader("Resource Explorer Indexes")
                    st.json(indexes)
                    
                    # List views
                    try:
                        views = re_client.list_views()
                        st.subheader("Views")
                        st.json(views)
                    except ClientError as e:
                        st.warning(f"Could not list views: {e}")
                        
            except ClientError as e:
                st.error(f"Service API call failed: {e}")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("AWS session not available")

# Tab 3: Known Resources
with tab3:
    st.header("Known Resources from Provided List")
    
    # Display known resources as DataFrame
    df_known = pd.DataFrame(KNOWN_RESOURCES)
    st.dataframe(df_known, use_container_width=True)
    
    # Group by service
    st.subheader("Resources by Service")
    service_counts = df_known.groupby("service").size().reset_index(name="Count")
    st.bar_chart(service_counts.set_index("service"))
    
    # Group by region
    st.subheader("Resources by Region")
    region_counts = df_known.groupby("region").size().reset_index(name="Count")
    st.bar_chart(region_counts.set_index("region"))
    
    # Allow querying specific known resources
    st.subheader("Query Specific Known Resource")
    resource_identifier = st.selectbox(
        "Select Resource",
        options=[r["identifier"] for r in KNOWN_RESOURCES],
        key="known_resource"
    )
    
    selected_resource = next((r for r in KNOWN_RESOURCES if r["identifier"] == resource_identifier), None)
    
    if selected_resource and st.button("Get Resource Details"):
        try:
            service = selected_resource["service"]
            region = selected_resource["region"]
            identifier = selected_resource["identifier"]
            
            client = session.client(service, region_name=region)
            
            if service == "ec2":
                if "subnet" in selected_resource["resource_type"]:
                    result = client.describe_subnets(SubnetIds=[identifier])
                    st.json(result)
                elif "security-group" in selected_resource["resource_type"]:
                    if "rule" in selected_resource["resource_type"]:
                        # For security group rules, need to describe the security group
                        st.info("Security group rule details require parent security group info")
                    else:
                        result = client.describe_security_groups(GroupIds=[identifier])
                        st.json(result)
                elif "dhcp-options" in selected_resource["resource_type"]:
                    result = client.describe_dhcp_options(DhcpOptionsIds=[identifier])
                    st.json(result)
            
            elif service == "athena":
                if "workgroup" in selected_resource["resource_type"]:
                    result = client.get_work_group(WorkGroup=identifier)
                    st.json(result)
                elif "datacatalog" in selected_resource["resource_type"]:
                    result = client.get_data_catalog(Name=identifier)
                    st.json(result)
            
            elif service == "elasticache":
                if "user" in selected_resource["resource_type"]:
                    result = client.describe_users(UserId=identifier)
                    st.json(result)
            
            elif service == "memorydb":
                if "user" in selected_resource["resource_type"]:
                    result = client.describe_users(UserName=identifier)
                    st.json(result)
                elif "parametergroup" in selected_resource["resource_type"]:
                    result = client.describe_parameter_groups(ParameterGroupName=identifier)
                    st.json(result)
            
            elif service == "resource-explorer-2":
                if "index" in selected_resource["resource_type"]:
                    result = client.get_index(Arn=identifier)
                    st.json(result)
                    
        except ClientError as e:
            st.error(f"Failed to get resource details: {e}")
        except Exception as e:
            st.error(f"Error: {e}")

# Tab 4: Resource Search
with tab4:
    st.header("Advanced Resource Search")
    
    if session:
        search_type = st.radio(
            "Search Type",
            options=["Resource Explorer", "Resource Groups Tagging API", "Service-Specific"],
            index=0
        )
        
        if search_type == "Resource Explorer":
            # Default queries for dropdown
            DEFAULT_QUERIES_ADV = {
                "All Resources": "*",
                "EC2 Resources": "ec2",
                "SageMaker Endpoints": "sagemaker endpoint",
                "ECS Services": "ecs service",
                "EKS Clusters": "eks cluster",
                "Athena Workgroups": "athena workgroup",
                "ElastiCache": "elasticache",
                "MemoryDB": "memorydb",
                "Load Balancers": "elasticloadbalancing loadbalancer",
                "Security Groups": "ec2 security-group",
                "Subnets": "ec2 subnet",
                "NVIDIA NIM Resources": "tag:Application=*NIM* OR tag:Application=*nvidia* OR sagemaker endpoint",
                "NeuroForge Application": "tag:Application=NeuroForge",
                "Custom Query": "CUSTOM"
            }
            
            query_option_adv = st.selectbox(
                "Select Search Query",
                options=list(DEFAULT_QUERIES_ADV.keys()),
                index=0,
                key="adv_query_option",
                help="Select a predefined query or choose 'Custom Query' to enter your own"
            )
            
            if query_option_adv == "Custom Query":
                re_query = st.text_input("Custom Query String", value="*", key="re_query_custom")
            else:
                re_query = DEFAULT_QUERIES_ADV[query_option_adv]
                st.info(f"Using query: **{re_query}**")
            
            re_reg = st.selectbox("Region", options=["us-east-1", "eu-west-2", "eu-central-1"], key="re_reg")
            
            if st.button("Search", key="adv_search"):
                try:
                    re_client = session.client("resource-explorer-2", region_name=re_reg)
                    paginator = re_client.get_paginator("search")
                    
                    all_resources = []
                    for page in paginator.paginate(QueryString=re_query, MaxResults=100):
                        all_resources.extend(page.get("Items", []))
                    
                    if all_resources:
                        st.success(f"Found {len(all_resources)} resources")
                        st.json(all_resources[:10])  # Show first 10
                    else:
                        st.info("No resources found")
                except Exception as e:
                    st.error(f"Search failed: {e}")
        
        elif search_type == "Resource Groups Tagging API":
            tag_key = st.text_input("Tag Key (optional)", value="")
            tag_value = st.text_input("Tag Value (optional)", value="")
            
            if st.button("Search Tags"):
                try:
                    rt_client = session.client("resourcegroupstaggingapi", region_name=default_region)
                    paginator = rt_client.get_paginator("get_resources")
                    
                    all_resources = []
                    for page in paginator.paginate():
                        all_resources.extend(page.get("ResourceTagMappingList", []))
                    
                    if all_resources:
                        st.success(f"Found {len(all_resources)} tagged resources")
                        
                        # Filter by tag if provided
                        if tag_key:
                            filtered = [r for r in all_resources 
                                       if any(t.get("Key") == tag_key and (not tag_value or t.get("Value") == tag_value)
                                             for t in r.get("Tags", []))]
                            all_resources = filtered if filtered else all_resources
                        
                        st.json(all_resources[:10])  # Show first 10
                    else:
                        st.info("No tagged resources found")
                except Exception as e:
                    st.error(f"Tag search failed: {e}")
        
        elif search_type == "Service-Specific":
            svc = st.selectbox("Service", options=["ec2", "athena", "elasticache", "memorydb"], key="svc_search")
            svc_reg = st.selectbox("Region", options=["us-east-1", "us-west-2", "eu-west-2"], key="svc_reg")
            
            if st.button("List Resources"):
                try:
                    client = session.client(svc, region_name=svc_reg)
                    
                    if svc == "ec2":
                        result = client.describe_instances()
                        st.json(result)
                    elif svc == "athena":
                        result = client.list_work_groups()
                        st.json(result)
                    elif svc == "elasticache":
                        result = client.describe_cache_clusters()
                        st.json(result)
                    elif svc == "memorydb":
                        result = client.describe_clusters()
                        st.json(result)
                except Exception as e:
                    st.error(f"Service query failed: {e}")
    else:
        st.error("AWS session not available")

# Tab 5: NVIDIA NIM Search
with tab5:
    st.header("🔍 NVIDIA NIM Microservices Search")
    st.markdown("**Search artifacts and resources for deploying LLM reasoning models and retrieval/embedding models using NVIDIA NIM**")
    
    # Resource Links Section
    st.subheader("📚 Resource Links")
    
    categories = list(set([r["category"] for r in NVIDIA_NIM_RESOURCES]))
    selected_category = st.selectbox("Filter by Category", options=["All"] + sorted(categories), index=0)
    
    filtered_resources = NVIDIA_NIM_RESOURCES
    if selected_category != "All":
        filtered_resources = [r for r in NVIDIA_NIM_RESOURCES if r["category"] == selected_category]
    
    for resource in filtered_resources:
        with st.expander(f"📖 {resource['title']} - {resource['category']}"):
            st.markdown(f"**Description:** {resource['description']}")
            st.markdown(f"**Link:** [{resource['url']}]({resource['url']})")
    
    st.markdown("---")
    
    # Search Queries Section
    st.subheader("🔎 Pre-defined Search Queries")
    st.markdown("Use these queries to search AWS resources related to NVIDIA NIM deployments:")
    
    # Display search queries in a more interactive way
    selected_query_idx = st.selectbox(
        "Select a Search Query",
        options=range(len(NVIDIA_NIM_SEARCH_QUERIES)),
        format_func=lambda x: NVIDIA_NIM_SEARCH_QUERIES[x],
        index=0
    )
    
    selected_query = NVIDIA_NIM_SEARCH_QUERIES[selected_query_idx]
    st.code(selected_query, language=None)
    
    # Copy to clipboard option
    if st.button("📋 Copy Query to Clipboard"):
        st.code(selected_query)
        st.success("Query copied! (You can manually copy it)")

    st.markdown("---")

    # AWS Resource Search with NIM-related queries
    st.subheader("🔍 Search AWS Resources for NVIDIA NIM")
    st.markdown("Search your AWS infrastructure for resources related to NVIDIA NIM deployments:")
    
    if session:
        col1, col2 = st.columns(2)
        
        with col1:
            nim_search_region = st.selectbox(
                "Search Region",
                options=["us-east-1", "us-west-2", "eu-west-2", "eu-central-1", "ap-northeast-1"],
                index=0,
                key="nim_region"
            )
        
        with col2:
            nim_search_type = st.radio(
                "Search Type",
                options=["Use Selected Query", "Custom Query"],
                index=0,
                key="nim_search_type"
            )
        
        if nim_search_type == "Use Selected Query":
            # Convert NIM query to AWS Resource Explorer compatible query
            nim_query = st.text_input(
                "AWS Resource Query (converted from NIM query)",
                value=f"sagemaker endpoint OR ecs service OR eks cluster OR tag:Application=*NIM* OR tag:Application=*nvidia*",
                key="nim_query_converted"
            )
        else:
            nim_query = st.text_input(
                "Custom AWS Resource Query",
                value="sagemaker endpoint OR ecs service OR eks cluster",
                key="nim_query_custom"
            )
        
        st.info("💡 **Tip:** Try queries like: 'sagemaker endpoint', 'ecs service', 'eks cluster', 'tag:Application=NIM', or 'ec2 instance'")
        
        if st.button("🔍 Search AWS Resources", key="nim_search"):
            try:
                re_client = session.client("resource-explorer-2", region_name=nim_search_region)
                paginator = re_client.get_paginator("search")
                
                resources = []
                try:
                    for page in paginator.paginate(QueryString=nim_query, MaxResults=100):
                        items = page.get("Items", [])
                        if items:
                            resources.extend(items)
                    
                    if resources:
                        st.success(f"✅ Found {len(resources)} resource(s) related to NVIDIA NIM deployment")
                        
                        # Display as DataFrame
                        df_data = []
                        for r in resources:
                            tags = r.get("Tags", {})
                            tag_str = ", ".join([f"{k}={v}" for k, v in tags.items()]) if tags else ""
                            
                            df_data.append({
                                "ARN": r.get("Arn", ""),
                                "Service": r.get("Service", ""),
                                "Resource Type": r.get("ResourceType", ""),
                                "Region": r.get("Region", ""),
                                "Tags": tag_str[:100] + "..." if len(tag_str) > 100 else tag_str
                            })
                        
                        if df_data:
                            df = pd.DataFrame(df_data)
                            st.dataframe(df, use_container_width=True)
                            
                            # Show resource details
                            if st.checkbox("Show Detailed Resource Information"):
                                for idx, r in enumerate(resources[:10]):  # Show first 10
                                    with st.expander(f"Resource {idx+1}: {r.get('Arn', 'Unknown')[:80]}..."):
                                        st.json(r)
                    else:
                        st.info("ℹ️ No resources found. Try a broader query or check different regions.")
                        
                except ClientError as e:
                    error_code = e.response.get('Error', {}).get('Code', '')
                    if error_code in ['ExpiredTokenException', 'AccessDeniedException']:
                        st.error("⚠️ **STS Credentials Expired**")
                        st.warning("Your AWS Security Token Service (STS) credentials have expired. These temporary credentials from assume-role, SSO, or federated login typically expire after 1-12 hours.")
                        with st.expander("🔧 How to Refresh STS Credentials"):
                            st.markdown("""
                            **Quick Fix Options:**
                            
                            **1. AWS SSO**
                            ```bash
                            aws sso login
                            ```
                            Then get new credentials and update `app.py` lines 15-17.
                            
                            **2. Assume Role (STS)**
                            ```bash
                            aws sts assume-role \\
                                --role-arn arn:aws:iam::ACCOUNT:role/ROLE \\
                                --role-session-name Session
                            ```
                            Copy the new credentials from the output.
                            
                            **3. Federated Login**
                            Use the Source URL in the sidebar to sign in and get new credentials.
                            
                            **4. Update Credentials in Code**
                            - Update lines 15-17 in `app.py` with new credentials
                            - Restart the Streamlit app
                            
                            **📋 See Sidebar**: "Credential Management" section has detailed instructions for all methods.
                            """)
                    else:
                        st.error(f"❌ Resource Explorer search failed: {e}")
            except Exception as e:
                st.error(f"❌ Error during search: {e}")
    
    st.markdown("---")
    
    # Quick Reference Section
    st.subheader("📝 Quick Reference")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Common AWS Resource Types for NIM:**
        - `sagemaker:endpoint` - SageMaker endpoints
        - `ecs:service` - ECS services
        - `eks:cluster` - EKS clusters
        - `ec2:instance` - EC2 instances
        - `ec2:security-group` - Security groups
        - `elasticloadbalancing:loadbalancer` - Load balancers
        """)
    
    with col2:
        st.markdown("""
        **Useful Tag Queries:**
        - `tag:Application=*NIM*`
        - `tag:Application=*nvidia*`
        - `tag:Environment=production`
        - `tag:Service=*llm*`
        - `tag:Service=*embedding*`
        """)
    
    st.markdown("---")
    
    # Docker Commands Reference
    st.subheader("🐳 Docker Commands Reference")
    
    with st.expander("NVIDIA NIM Docker Commands"):
        st.code("""
# Run NVIDIA NIM LLM container
docker run --gpus all -it --rm \\
    -p 8000:8000 \\
    -v $(pwd)/models:/models \\
    nvcr.io/nim/meta/llama-3-70b-instruct:latest

# Run NVIDIA NIM Embedding container
docker run --gpus all -it --rm \\
    -p 8000:8000 \\
    -v $(pwd)/models:/models \\
    nvcr.io/nim/nvidia/nv-embedqa-4:latest

# With API key (if required)
docker run --gpus all -it --rm \\
    -p 8000:8000 \\
    -e NGC_API_KEY=your_api_key \\
    nvcr.io/nim/meta/llama-3-70b-instruct:latest
        """, language="bash")
    
    st.markdown("---")
    
    # Kubernetes/Helm Reference
    st.subheader("☸️ Kubernetes/Helm Deployment Reference")
    
    with st.expander("Helm Chart Commands"):
        st.code("""
# Add NVIDIA Helm repository
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update

# Install NIM Service
helm install nim-service nvidia/nim \\
    --set service.type=LoadBalancer \\
    --set service.port=8000 \\
    --namespace nvidia-nim

# Install NIM Pipeline
helm install nim-pipeline nvidia/nim-pipeline \\
    --namespace nvidia-nim
        """, language="bash")

# Footer
st.markdown("---")
st.markdown("**AWS Resource Manager** - Using provided credentials and services")
st.caption(f"Session initialized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
