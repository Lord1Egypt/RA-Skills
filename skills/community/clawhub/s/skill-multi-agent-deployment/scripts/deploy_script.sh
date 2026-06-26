#!/bin/bash
# Multi-Agent Deployment Script for OpenClaw
# One-click deployment to cloud platforms

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEFAULT_REGION="nyc3"
DEFAULT_SIZE="s-1vcpu-1gb"
DEFAULT_AGENTS="coordinator,research,builder,auditor,personal"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROJECT_NAME="openclaw-multi-agent-$TIMESTAMP"

# Platform-specific variables
PLATFORM=""
REGION=""
SIZE=""
AGENTS=""
DRY_RUN=false

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Platform detection
detect_platform() {
    if command_exists doctl; then
        echo "digitalocean"
    elif command_exists aws; then
        echo "aws"
    elif command_exists gcloud; then
        echo "gcp"
    elif command_exists az; then
        echo "azure"
    else
        echo "unknown"
    fi
}

# Generate deployment files
generate_deployment_files() {
    local platform="$1"
    local agents="$2"
    
    log_info "Generating deployment files for $platform..."
    
    mkdir -p ./deployments/$platform
    
    case $platform in
        digitalocean)
            # Generate DigitalOcean App Spec
            cat > ./deployments/digitalocean/app.yaml << EOF
name: $PROJECT_NAME
region: $REGION
services:
  - name: openclaw-gateway
    github:
      branch: main
      deploy_on_push: true
    dockerfile_path: Dockerfile.openclaw
    instance_size_slug: $SIZE
    envs:
      - key: OPENCLAW_AGENTS
        value: "$agents"
      - key: OPENCLAW_CONFIG
        type: secret
        value: openclaw-config
    health_check:
      http_path: /health
      initial_delay_seconds: 30
      period_seconds: 10
      timeout_seconds: 5
      success_threshold: 1
      failure_threshold: 3
EOF
            log_success "Generated DigitalOcean App Spec"
            ;;
            
        aws)
            # Generate AWS ECS Task Definition
            cat > ./deployments/aws/task-definition.json << EOF
{
  "family": "$PROJECT_NAME",
  "networkMode": "awsvpc",
  "executionRoleArn": "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
  "containerDefinitions": [
    {
      "name": "openclaw-gateway",
      "image": "openclaw/gateway:latest",
      "cpu": 256,
      "memory": 512,
      "essential": true,
      "environment": [
        {"name": "OPENCLAW_AGENTS", "value": "$agents"}
      ],
      "portMappings": [
        {"containerPort": 8080, "hostPort": 8080, "protocol": "tcp"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/$PROJECT_NAME",
          "awslogs-region": "$REGION",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
EOF
            log_success "Generated AWS ECS Task Definition"
            ;;
            
        gcp)
            # Generate GCP Cloud Run configuration
            cat > ./deployments/gcp/cloudrun.yaml << EOF
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: $PROJECT_NAME
  labels:
    app: openclaw-multi-agent
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "5"
    spec:
      containers:
      - image: openclaw/gateway:latest
        env:
        - name: OPENCLAW_AGENTS
          value: "$agents"
        ports:
        - containerPort: 8080
        resources:
          limits:
            cpu: 1000m
            memory: 512Mi
EOF
            log_success "Generated GCP Cloud Run configuration"
            ;;
            
        azure)
            # Generate Azure Container Instances configuration
            cat > ./deployments/azure/container-instance.yaml << EOF
apiVersion: 2018-10-01
location: $REGION
name: $PROJECT_NAME
properties:
  containers:
  - name: openclaw-gateway
    properties:
      image: openclaw/gateway:latest
      environmentVariables:
      - name: OPENCLAW_AGENTS
        value: "$agents"
      ports:
      - port: 8080
        protocol: TCP
      resources:
        requests:
          cpu: 1.0
          memoryInGB: 1.0
  ipAddress:
    type: Public
    ports:
    - protocol: tcp
      port: 8080
  osType: Linux
tags:
  project: openclaw-multi-agent
type: Microsoft.ContainerInstance/containerGroups
EOF
            log_success "Generated Azure Container Instances configuration"
            ;;
    esac
    
    # Generate Dockerfile
    cat > ./deployments/Dockerfile.openclaw << EOF
FROM node:22-alpine

# Install OpenClaw
RUN npm install -g openclaw

# Create workspace directory
RUN mkdir -p /data/.openclaw/workspace

# Copy agent configurations
COPY ./agents /data/.openclaw/agents
COPY ./shared_memory /data/.openclaw/shared_memory

# Copy OpenClaw configuration
COPY ./config.json /data/.openclaw/config.json

# Expose port
EXPOSE 8080

# Start OpenClaw gateway
CMD ["openclaw", "gateway", "start", "--port", "8080", "--host", "0.0.0.0"]
EOF
    
    log_success "Generated Dockerfile"
}

# Platform deployment functions
deploy_digitalocean() {
    log_info "Deploying to DigitalOcean..."
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Dry run - would deploy with:"
        echo "doctl apps create --spec ./deployments/digitalocean/app.yaml"
        return 0
    fi
    
    # Check if doctl is authenticated
    if ! doctl account get >/dev/null 2>&1; then
        log_error "DigitalOcean CLI not authenticated. Run: doctl auth init"
        return 1
    fi
    
    # Create config secret
    log_info "Creating OpenClaw config secret..."
    if [ -f "./config.json" ]; then
        doctl apps secrets set openclaw-config --value "$(cat ./config.json)" --app "$PROJECT_NAME" || true
    fi
    
    # Deploy app
    log_info "Creating DigitalOcean App..."
    doctl apps create --spec ./deployments/digitalocean/app.yaml
    
    log_success "DigitalOcean App created. Deployment may take a few minutes."
    log_info "Check status with: doctl apps list"
}

deploy_aws() {
    log_info "Deploying to AWS..."
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Dry run - would deploy with:"
        echo "aws ecs register-task-definition --cli-input-json file://./deployments/aws/task-definition.json"
        return 0
    fi
    
    # Register task definition
    log_info "Registering ECS task definition..."
    aws ecs register-task-definition --cli-input-json file://./deployments/aws/task-definition.json
    
    # Create ECS service (simplified - would need VPC, cluster, etc.)
    log_warning "Note: AWS deployment requires additional setup (VPC, ECS cluster, load balancer)"
    log_info "Task definition registered. Manual steps required for full deployment."
    
    log_success "AWS deployment prepared. Complete setup in AWS Console."
}

deploy_gcp() {
    log_info "Deploying to GCP..."
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Dry run - would deploy with:"
        echo "gcloud run deploy $PROJECT_NAME --source . --region $REGION --platform managed"
        return 0
    fi
    
    # Deploy to Cloud Run
    log_info "Deploying to Cloud Run..."
    gcloud run deploy "$PROJECT_NAME" \
        --source . \
        --region "$REGION" \
        --platform managed \
        --allow-unauthenticated \
        --memory 512Mi \
        --cpu 1
    
    log_success "GCP Cloud Run deployment complete"
    log_info "Get URL with: gcloud run services describe $PROJECT_NAME --region $REGION --format='value(status.url)'"
}

deploy_azure() {
    log_info "Deploying to Azure..."
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Dry run - would deploy with:"
        echo "az container create --resource-group openclaw --file ./deployments/azure/container-instance.yaml"
        return 0
    fi
    
    # Create resource group if needed
    log_info "Creating/updating resource group..."
    az group create --name openclaw --location "$REGION" || true
    
    # Deploy container instance
    log_info "Creating container instance..."
    az container create --resource-group openclaw --file ./deployments/azure/container-instance.yaml
    
    log_success "Azure Container Instance deployed"
    log_info "Get IP with: az container show --resource-group openclaw --name $PROJECT_NAME --query 'ipAddress.ip' -o tsv"
}

deploy_k8s() {
    log_info "Deploying to Kubernetes..."
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "Dry run - would deploy with:"
        echo "helm install openclaw ./deployments/k8s/helm/openclaw-multi-agent"
        return 0
    fi
    
    # Check if kubectl is available
    if ! command -v kubectl >/dev/null 2>&1; then
        log_error "kubectl not found. Please install kubectl first."
        return 1
    fi
    
    # Check cluster connectivity
    if ! kubectl cluster-info >/dev/null 2>&1; then
        log_error "Cannot connect to Kubernetes cluster"
        return 1
    fi
    
    # Generate Helm chart
    generate_k8s_deployment "$PROJECT_NAME" "$AGENTS"
    
    # Deploy using Helm
    log_info "Deploying OpenClaw multi-agent to Kubernetes..."
    helm upgrade --install openclaw ./deployments/k8s/helm/openclaw-multi-agent --namespace openclaw --create-namespace 2>/dev/null || {
        log_warning "Helm not found, using kubectl apply instead"
        kubectl apply -f ./deployments/k8s/helm/openclaw-multi-agent/templates/
    }
    
    log_success "Kubernetes deployment complete"
    log_info "Check status with: kubectl get pods -n openclaw"
}

generate_k8s_deployment() {
    local project_name="$1"
    local agents="$2"
    
    log_info "Generating Kubernetes deployment files..."
    
    mkdir -p ./deployments/k8s
    
    # Generate deployment YAML
    cat > ./deployments/k8s/deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: openclaw-gateway
  namespace: openclaw
spec:
  replicas: 2
  selector:
    matchLabels:
      app: openclaw
      component: gateway
  template:
    metadata:
      labels:
        app: openclaw
        component: gateway
    spec:
      containers:
      - name: gateway
        image: openclaw/gateway:latest
        ports:
        - containerPort: 8080
        env:
        - name: OPENCLAW_AGENTS
          value: "$agents"
        resources:
          limits:
            cpu: 1000m
            memory: 1Gi
          requests:
            cpu: 250m
            memory: 512Mi
---
apiVersion: v1
kind: Service
metadata:
  name: openclaw-gateway
  namespace: openclaw
spec:
  selector:
    app: openclaw
  ports:
  - port: 8080
    targetPort: 8080
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: openclaw-gateway-hpa
  namespace: openclaw
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: openclaw-gateway
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
EOF

    log_success "Generated Kubernetes deployment files"
}

# Main deployment function
deploy() {
    local platform="$1"
    
    log_info "Starting deployment to $platform..."
    log_info "Project: $PROJECT_NAME"
    log_info "Region: $REGION"
    log_info "Size: $SIZE"
    log_info "Agents: $AGENTS"
    
    # Generate deployment files
    generate_deployment_files "$platform" "$AGENTS"
    
    # Run platform-specific deployment
    case $platform in
        digitalocean) deploy_digitalocean ;;
        aws) deploy_aws ;;
        gcp) deploy_gcp ;;
        azure) deploy_azure ;;
        k8s|kubernetes) deploy_k8s ;;
        *) log_error "Unsupported platform: $platform" && exit 1 ;;
    esac
    
    # Generate deployment summary
    cat > ./deployments/deployment-summary.md << EOF
# OpenClaw Multi-Agent Deployment Summary

## Deployment Details
- **Platform**: $platform
- **Project Name**: $PROJECT_NAME
- **Region**: $REGION
- **Instance Size**: $SIZE
- **Agents**: $AGENTS
- **Deployment Time**: $(date)

## Generated Files
- Platform configuration: ./deployments/$platform/
- Dockerfile: ./deployments/Dockerfile.openclaw
- Agent directory: ./agents/
- Shared memory: ./shared_memory/

## Next Steps
1. Wait for deployment to complete (check platform console)
2. Configure DNS/domain if needed
3. Set up monitoring and alerts
4. Test agent coordination
5. Scale as needed based on usage

## Troubleshooting
- Check logs in platform console
- Verify agent directories are accessible
- Test shared memory synchronization
- Monitor resource usage
EOF
    
    log_success "Deployment process complete!"
    log_info "See ./deployments/deployment-summary.md for details"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --platform)
            PLATFORM="$2"
            shift 2
            ;;
        --region)
            REGION="$2"
            shift 2
            ;;
        --size)
            SIZE="$2"
            shift 2
            ;;
        --agents)
            AGENTS="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            echo "OpenClaw Multi-Agent Deployment Script"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --platform <digitalocean|aws|gcp|azure|k8s>  Cloud platform (default: auto-detect)"
            echo "  --region <region>                        Cloud region (default: $DEFAULT_REGION)"
            echo "  --size <size>                            Instance size (default: $DEFAULT_SIZE)"
            echo "  --agents <list>                          Comma-separated agent list (default: $DEFAULT_AGENTS)"
            echo "  --dry-run                                Generate files without deploying"
            echo "  --help                                   Show this help"
            echo ""
            echo "Examples:"
            echo "  $0 --platform digitalocean --region nyc3"
            echo "  $0 --platform aws --region us-east-1 --dry-run"
            echo "  $0 --agents coordinator,research,builder --size s-2vcpu-2gb"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Set defaults if not provided
: ${PLATFORM:=$(detect_platform)}
: ${REGION:=$DEFAULT_REGION}
: ${SIZE:=$DEFAULT_SIZE}
: ${AGENTS:=$DEFAULT_AGENTS}

# Validate platform
if [ "$PLATFORM" = "unknown" ]; then
    log_error "No cloud platform detected and none specified"
    log_info "Please install one of: doctl (DigitalOcean), aws-cli (AWS), gcloud (GCP), az (Azure), kubectl (Kubernetes)"
    log_info "Or specify platform with --platform"
    exit 1
fi

# Check for required files
if [ ! -d "./agents" ]; then
    log_warning "Agents directory not found. Run agent_setup.py first."
    log_info "Creating minimal agent structure..."
    python3 scripts/agent_setup.py --agents "$AGENTS" --output ./agents
fi

if [ ! -f "./config.json" ]; then
    log_warning "config.json not found. Generating routing configuration..."
    python3 scripts/routing_config.py --input ./agents --output ./config.json
fi

if [ ! -d "./shared_memory" ]; then
    log_warning "Shared memory directory not found. Initializing..."
    python3 scripts/memory_sync.py --init --path ./shared_memory
fi

# Start deployment
log_info "Preparing deployment..."
deploy "$PLATFORM"

exit 0