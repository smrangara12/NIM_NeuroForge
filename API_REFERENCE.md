# API Reference & Usage Guide

Quick reference for using the AWS Resource Explorer & Service Manager application.

## Application Tabs

### Tab 1: Resource Explorer

**Purpose**: Search and discover AWS resources using Resource Explorer API

**Features**:
- Pre-defined query dropdown (14 options)
- Custom query input
- Multi-region support
- Resource index listing
- Detailed resource display

**Usage**:
1. Select a query from dropdown or enter custom query
2. Choose region
3. Click "Search Resources"
4. View results in table format

**Query Examples**:
```
*                                    # All resources
ec2                                 # EC2 resources
sagemaker endpoint                  # SageMaker endpoints
tag:Application=NeuroForge          # Tagged resources
sagemaker endpoint OR ecs service   # Multiple resource types
```

### Tab 2: Service Details

**Purpose**: Query specific AWS services for detailed information

**Supported Services**:
- EC2 (Subnets, Security Groups, DHCP Options)
- Athena (Workgroups, Data Catalogs)
- ElastiCache (Users, Clusters)
- MemoryDB (Users, Parameter Groups)
- Resource Explorer (Indexes, Views)

**Usage**:
1. Select service from dropdown
2. Choose region
3. Click "Get Service Details"
4. View service-specific information

### Tab 3: Known Resources

**Purpose**: View and query pre-configured resources

**Features**:
- Resource list display
- Visualization by service and region
- Direct resource querying

**Usage**:
1. View resource list
2. Select a resource from dropdown
3. Click "Get Resource Details"
4. View detailed resource information

### Tab 4: Resource Search

**Purpose**: Advanced search with multiple methods

**Search Types**:
1. **Resource Explorer**: Query using Resource Explorer API
2. **Resource Groups Tagging API**: Search by tags
3. **Service-Specific**: Direct service queries

**Usage**:
1. Select search type
2. Configure query parameters
3. Execute search
4. Review results

### Tab 5: NVIDIA NIM Search

**Purpose**: Access NVIDIA NIM documentation and search resources

**Features**:
- Documentation links by category
- Pre-defined NIM search queries
- AWS resource search for NIM deployments
- Docker and Kubernetes deployment guides

**Usage**:
1. Browse documentation by category
2. Select search queries
3. Search AWS for NIM-related resources
4. Reference deployment guides

## Query Syntax

### Resource Explorer Queries

**Basic Syntax**:
```
service:resource-type
tag:Key=Value
region:us-east-1
```

**Wildcards**:
```
*                                    # Match all
tag:Application=*NIM*               # Wildcard in tag value
ec2:*                               # All EC2 resources
```

**Operators**:
```
service1 OR service2                # Logical OR
tag:Key=Value AND region:us-east-1  # Logical AND (implied)
```

**Examples**:
```
sagemaker endpoint
ec2 subnet
tag:Application=NeuroForge
sagemaker endpoint OR ecs service
tag:Application=*NIM* OR tag:Application=*nvidia*
```

### Tag Queries

**Format**: `tag:Key=Value`

**Wildcards**:
```
tag:Application=*NIM*               # Contains NIM
tag:Environment=production          # Exact match
tag:Service=*llm*                   # Contains llm
```

## AWS Service Queries

### EC2 Resources
```
ec2
ec2 subnet
ec2 security-group
ec2 instance
ec2:subnet
ec2:security-group
```

### SageMaker
```
sagemaker endpoint
sagemaker:endpoint
```

### Container Services
```
ecs service
eks cluster
```

### Database Services
```
elasticache
memorydb
athena workgroup
```

### Networking
```
elasticloadbalancing loadbalancer
ec2 subnet
ec2 security-group
```

## Error Handling

### ExpiredTokenException

**Trigger**: STS credentials expired

**Resolution**:
1. Check sidebar credential status
2. Follow refresh instructions
3. Update credentials in app.py
4. Restart application

### AccessDeniedException

**Trigger**: Insufficient IAM permissions

**Resolution**:
1. Verify IAM permissions
2. Check Resource Explorer is enabled
3. Ensure service-specific permissions

### No Resources Found

**Possible Causes**:
- Query too specific
- Wrong region
- Resource Explorer not enabled
- No matching resources

**Resolution**:
- Try broader query (*)
- Check different regions
- Verify Resource Explorer indexes

## Configuration Variables

### AWS Credentials (app.py lines 15-17)
```python
AWS_ACCESS_KEY_ID = "..."
AWS_SECRET_ACCESS_KEY = "..."
AWS_SESSION_TOKEN = "..."  # Required for STS
```

### Source URL (app.py line 20)
```python
SOURCE_URL = "https://signin.aws.amazon.com/federation?..."
```

### Known Resources (app.py lines 23-41)
```python
KNOWN_RESOURCES = [
    {
        "identifier": "resource-id",
        "service": "ec2",
        "resource_type": "ec2:subnet",
        "region": "us-east-1"
    },
    ...
]
```

## NVIDIA NIM Resources

### Documentation Links
- Reasoning Models: `https://docs.nvidia.com/nim/llm/guides/reasoning-mode.html`
- Retriever NIMs: `https://docs.api.nvidia.com/nim/retriever/overview`
- Deployment Guide: `https://docs.nvidia.com/nim/llm/deployment-guide/index.html`
- NIM Overview: `https://docs.api.nvidia.com/nim/overview`

### Search Queries
1. "NVIDIA NIM reasoning mode large language models"
2. "NVIDIA NIM reasoning model chain of thought prompt NIM for LLMs"
3. "NeMo Retriever Text Embedding NIM semantic search retrieval NIM API"
4. "Deploy NVIDIA NIM microservice Helm Kubernetes NIMPipeline NIMService"
5. "NVIDIA NIM text embedding NIM NV-EmbedQA-4 model"
6. "NVIDIA NIM inference microservice large language model Docker run nvcr.io/nim"

## Common Workflows

### Finding SageMaker Endpoints
1. Go to Resource Explorer tab
2. Select "SageMaker Endpoints" from dropdown
3. Choose region
4. Click "Search Resources"

### Querying by Tags
1. Go to Resource Search tab
2. Select "Resource Groups Tagging API"
3. Enter tag key and value
4. Click "Search Tags"

### Finding NIM Resources
1. Go to NVIDIA NIM Search tab
2. Select "NVIDIA NIM Resources" query
3. Choose region
4. Click "Search AWS Resources"

### Checking Service Details
1. Go to Service Details tab
2. Select service (e.g., EC2)
3. Choose region
4. Click "Get Service Details"

## Tips & Best Practices

1. **Start Broad**: Use `*` to see all resources, then narrow down
2. **Check Multiple Regions**: Resources may be in different regions
3. **Use Tags**: Tag-based queries are powerful for finding related resources
4. **Monitor Credentials**: Check sidebar regularly for expiration warnings
5. **Use Pre-defined Queries**: Faster than typing custom queries
6. **Resource Explorer**: Most comprehensive search option
7. **Tag Queries**: Best for finding resources by application/project

## Performance Considerations

- **Pagination**: Large results are paginated (50-100 items per page)
- **Caching**: AWS sessions are cached for performance
- **Region Selection**: Searching specific regions is faster than all regions
- **Query Complexity**: Simple queries are faster than complex ones

## Security Notes

- Credentials are currently hardcoded - consider environment variables for production
- STS tokens expire - implement refresh mechanism
- Follow least privilege for IAM permissions
- Review Resource Explorer indexes regularly

