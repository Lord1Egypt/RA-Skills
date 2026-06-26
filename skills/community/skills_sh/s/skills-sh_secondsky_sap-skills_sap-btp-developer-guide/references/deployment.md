# SAP BTP Deployment Reference

## Overview

SAP BTP supports multiple deployment approaches depending on the runtime (Cloud Foundry, Kyma, or ABAP Environment) and application architecture.

## Cloud Foundry Deployment

### Multitarget Application (MTA)

**Recommended for**: Complex applications with multiple modules and services

#### Build and Deploy

```bash
# Install MTA Build Tool
npm install -g mbt

# Build MTA archive
mbt build

# Deploy to Cloud Foundry
cf deploy mta_archives/my-app_1.0.0.mtar
```

#### mta.yaml Structure

```yaml
_schema-version: "3.1"
ID: my-cap-app
version: 1.0.0

parameters:
  enable-parallel-deployments: true

modules:
  # Backend service
  - name: my-srv
    type: nodejs
    path: gen/srv
    parameters:
      buildpack: nodejs_buildpack
      memory: 256M
    requires:
      - name: my-hana
      - name: my-xsuaa
      - name: my-destination
    provides:
      - name: srv-api
        properties:
          srv-url: ${default-url}

  # UI application
  - name: my-app
    type: approuter.nodejs
    path: app/
    parameters:
      memory: 256M
    requires:
      - name: srv-api
        group: destinations
        properties:
          name: srv-api
          url: ~{srv-url}
          forwardAuthToken: true
      - name: my-xsuaa
      - name: my-html5-repo-runtime

  # Database deployer
  - name: my-db-deployer
    type: hdb
    path: gen/db
    parameters:
      buildpack: nodejs_buildpack
    requires:
      - name: my-hana

resources:
  - name: my-hana
    type: com.sap.xs.hdi-container
    parameters:
      service: hana
      service-plan: hdi-shared

  - name: my-xsuaa
    type: org.cloudfoundry.managed-service
    parameters:
      service: xsuaa
      service-plan: application
      path: ./xs-security.json

  - name: my-destination
    type: org.cloudfoundry.managed-service
    parameters:
      service: destination
      service-plan: lite

  - name: my-html5-repo-runtime
    type: org.cloudfoundry.managed-service
    parameters:
      service: html5-apps-repo
      service-plan: app-runtime
```

### Simple cf push

**For**: Simple applications without complex dependencies

```bash
# Deploy single application
cf push my-app -p ./dist -m 256M -b nodejs_buildpack
```

### manifest.yml

```yaml
applications:
  - name: my-app
    memory: 256M
    instances: 1
    buildpack: nodejs_buildpack
    path: ./dist
    routes:
      - route: my-app.cfapps.eu10.hana.ondemand.com
    services:
      - my-xsuaa
      - my-destination
    env:
      NODE_ENV: production
```

## Kyma Deployment

### Helm Charts

```bash
# Add Helm support to CAP
cds add helm

# Deploy to Kyma
helm upgrade --install my-app ./chart \
  --namespace my-namespace \
  --set image.repository=my-registry/my-app \
  --set image.tag=1.0.0
```

### Helm Chart Structure

```
chart/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── hpa.yaml
    └── servicebinding.yaml
```

### values.yaml

```yaml
replicaCount: 2

image:
  repository: my-registry/my-app
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilization: 80

serviceBindings:
  hana:
    serviceInstanceName: my-hana
  xsuaa:
    serviceInstanceName: my-xsuaa
```

### Terraform for Kyma

**Purpose**: Automate Kyma cluster provisioning via CI/CD pipelines for resource creation, deployment, testing, and teardown.

**Key Resources:**
- **Terraform Provider for SAP BTP**: `SAP/btp` - Official SAP-maintained provider ([Terraform Registry](https://registry.terraform.io/providers/SAP/btp/latest/docs))
- **Kyma Terraform Module**: `github.com/kyma-project/terraform-module` - Open-source module maintained by the Kyma project (SAP-backed)

> **Note**: The Kyma Terraform module is an open-source project. Verify version compatibility and review the module documentation before production use.

#### Prerequisites

1. Terraform CLI on CI worker agents
2. Admin access (subaccount or global account level)
3. Dedicated Identity Authentication tenant
4. Technical user account

#### Variables File (.tfvars)

```hcl
# .tfvars - Store securely, use credential management
BTP_BOT_USER              = "technical-user@example.com"
BTP_BOT_PASSWORD          = "***"
BTP_GLOBAL_ACCOUNT        = "global-account-subdomain"
BTP_BACKEND_URL           = "https://cpcli.cf.sap.hana.ondemand.com"
BTP_CUSTOM_IAS_TENANT     = "custom-ias-tenant"
BTP_NEW_SUBACCOUNT_NAME   = "my-subaccount"
BTP_NEW_SUBACCOUNT_REGION = "eu10"
BTP_KYMA_PLAN             = "azure"
BTP_KYMA_REGION           = "westeurope"
```

#### main.tf Configuration

```hcl
# main.tf
terraform {
  required_providers {
    btp = {
      source = "SAP/btp"
    }
  }
}

provider "btp" {
  globalaccount = var.globalaccount
}

# Create Kyma environment using official module
module "kyma" {
  source = "git::https://github.com/kyma-project/terraform-module.git?ref=v0.3.1"

  subaccount_id = var.subaccount_id
  cluster_name  = var.BTP_NEW_SUBACCOUNT_NAME
  region        = var.BTP_KYMA_REGION

  administrators = [
    "admin@example.com"
  ]
}

# Outputs
output "kubeconfig" {
  value     = module.kyma.kubeconfig
  sensitive = true
}

output "cluster_id" {
  value = module.kyma.cluster_id
}

output "domain" {
  value = module.kyma.domain
}
```

#### Execution Commands

```bash
# Initialize Terraform
terraform init

# Apply configuration
terraform apply -var-file=.tfvars -auto-approve

# Retrieve outputs
terraform output -raw cluster_id

# Destroy resources when done
terraform destroy -var-file=.tfvars -auto-approve
```

**Security Recommendation**: Use credential management systems (e.g., HashiCorp Vault) for sensitive variables

## ABAP Deployment

### Software Components (gCTS)

**Manage Software Components App:**

1. Create software component
2. Clone to development system
3. Develop and release transport requests
4. Pull to test/production systems

```
Development Flow:
[Dev System] → Release TR → [Git Repository] → Pull → [Test System] → Pull → [Prod System]
```

### Partner Deployment

#### Multitenant SaaS

```
Partner Global Account:
├── Provider Subaccount
│   ├── ABAP System (Development)
│   ├── ABAP System (Test)
│   └── ABAP System (Production)
│       └── Tenant 1
│       └── Tenant 2
│       └── Tenant N
```

**Subscription Process:**
1. Customer subscribes via SaaS Provisioning
2. Tenant automatically created
3. Customer receives access URL

#### Add-on Product

```
Partner Global Account:
├── Development Subaccount
│   └── ABAP System (Dev)
├── Test Subaccount
│   └── ABAP System (Test)
└── Assembly Subaccount
    └── ABAP System (Assembly)

Customer Global Account:
└── Production Subaccount
    └── ABAP System + Add-on
```

**Delivery via Landscape Portal:**
1. Build add-on product
2. Register in SAP Store
3. Customer installs via Landscape Portal

### abapGit (Migration)

**Use Cases:**
- On-premise to cloud migration
- System decommissioning
- Cross-account transfers

**Not recommended for**: Standard production transports

## SAP Cloud Transport Management

### Configuration

```yaml
# Integration with CI/CD
transport:
  enabled: true
  landscape:
    - name: DEV
      type: Cloud Foundry
    - name: QA
      type: Cloud Foundry
      requires: DEV
    - name: PROD
      type: Cloud Foundry
      requires: QA
```

### Transport Routes

```
DEV → QA → PROD
     ↓
  [Manual Approval]
```

## Deployment Best Practices

### Blue-Green Deployment

```bash
# Deploy new version
cf push my-app-blue

# Test blue deployment
# ...

# Switch routes
cf map-route my-app-blue cfapps.eu10.hana.ondemand.com --hostname my-app
cf unmap-route my-app-green cfapps.eu10.hana.ondemand.com --hostname my-app
```

### Rolling Updates (Kyma)

```yaml
# deployment.yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

### Environment Variables

```yaml
# mta.yaml
modules:
  - name: my-srv
    properties:
      NODE_ENV: production
      LOG_LEVEL: info
      # Don't hardcode secrets!
```

### Resource Sizing

| Environment | Memory | Instances |
|-------------|--------|-----------|
| Development | 256M | 1 |
| QA | 512M | 2 |
| Production | 1G | 3+ |

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Memory exceeded | Insufficient allocation | Increase memory in mta.yaml |
| Service binding failed | Service not created | Create service first |
| Route conflict | Route already exists | Use unique hostname |
| Build failed | Missing dependencies | Check package.json |

## Useful Commands

### Cloud Foundry

```bash
# View logs
cf logs my-app --recent

# Scale application
cf scale my-app -i 3 -m 512M

# Restart application
cf restart my-app

# View environment
cf env my-app

# Bind service
cf bind-service my-app my-service
```

### Kyma/Kubernetes

```bash
# View pods
kubectl get pods -n my-namespace

# View logs
kubectl logs -f deployment/my-app -n my-namespace

# Scale deployment
kubectl scale deployment my-app --replicas=3 -n my-namespace

# Describe pod
kubectl describe pod my-app-xxx -n my-namespace
```

## Source Documentation

- Deploy (ABAP): [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/deploy-d7aec3c.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/deploy-d7aec3c.md)
- Terraforming Kyma: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/terraforming-kyma-runtimes-57c82ab.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/terraforming-kyma-runtimes-57c82ab.md)
- MTA Documentation: [https://help.sap.com/docs/btp/sap-business-technology-platform/multitarget-applications-in-cloud-foundry-environment](https://help.sap.com/docs/btp/sap-business-technology-platform/multitarget-applications-in-cloud-foundry-environment)
