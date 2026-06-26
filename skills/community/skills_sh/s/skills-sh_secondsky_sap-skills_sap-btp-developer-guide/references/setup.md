# SAP BTP Setup Reference

## Overview

Setting up SAP BTP landscape is an administrative task that involves configuring account structures, users, and infrastructure automation.

## Account Model

### Hierarchy

```
Global Account
├── Directory (optional)
│   ├── Subaccount (DEV)
│   ├── Subaccount (QA)
│   └── Subaccount (PROD)
└── Subaccount (Shared Services)
```

### Subaccount Configuration

Each subaccount can have:
- Cloud Foundry environment
- Kyma environment
- ABAP environment
- Service instances
- Role assignments

## User Types

### Platform Users

**Role**: Developers, administrators, operators

**Responsibilities**:
- Application deployment
- System administration
- Troubleshooting
- Operations

**Access**: Subaccounts, services, runtimes

### Business Users

**Role**: End users of applications

**Access**: Deployed applications, SaaS services

## Terraform Provider for SAP BTP

### Overview

**Purpose**: Automate provisioning, management, and configuration

**Benefits**:
- Infrastructure as code
- Reproducible deployments
- Version-controlled configuration
- CI/CD integration

### Installation

```hcl
# main.tf
terraform {
  required_providers {
    btp = {
      source  = "SAP/btp"
      version = "~> 1.0"
    }
  }
}

provider "btp" {
  globalaccount = var.globalaccount
}
```

### Common Resources

#### Subaccount

```hcl
resource "btp_subaccount" "dev" {
  name      = "development"
  subdomain = "dev-${var.org_id}"
  region    = "eu10"
  labels = {
    environment = "development"
  }
}
```

#### Entitlements

```hcl
resource "btp_subaccount_entitlement" "hana" {
  subaccount_id = btp_subaccount.dev.id
  service_name  = "hana-cloud"
  plan_name     = "hana"
  amount        = 1
}

resource "btp_subaccount_entitlement" "cf" {
  subaccount_id = btp_subaccount.dev.id
  service_name  = "APPLICATION_RUNTIME"
  plan_name     = "MEMORY"
}
```

#### Service Instances

```hcl
resource "btp_subaccount_service_instance" "xsuaa" {
  subaccount_id  = btp_subaccount.dev.id
  name           = "my-xsuaa"
  serviceplan_id = data.btp_subaccount_service_plan.xsuaa.id
  parameters = jsonencode({
    xsappname   = "my-app"
    tenant-mode = "dedicated"
  })
}
```

#### Role Collections

```hcl
resource "btp_subaccount_role_collection_assignment" "admin" {
  subaccount_id        = btp_subaccount.dev.id
  role_collection_name = "Subaccount Administrator"
  user_name           = "admin@example.com"
}
```

### Complete Example

```hcl
# variables.tf
variable "globalaccount" {
  description = "Global account subdomain"
  type        = string
}

variable "region" {
  description = "BTP region"
  type        = string
  default     = "eu10"
}

variable "admins" {
  description = "List of admin users"
  type        = list(string)
}

# main.tf
terraform {
  required_providers {
    btp = {
      source  = "SAP/btp"
      version = "~> 1.0"
    }
  }
}

provider "btp" {
  globalaccount = var.globalaccount
}

# Development subaccount
resource "btp_subaccount" "dev" {
  name      = "Development"
  subdomain = "dev-myorg"
  region    = var.region
}

# Enable Cloud Foundry
resource "btp_subaccount_entitlement" "cf" {
  subaccount_id = btp_subaccount.dev.id
  service_name  = "APPLICATION_RUNTIME"
  plan_name     = "MEMORY"
}

resource "btp_subaccount_environment_instance" "cf" {
  subaccount_id    = btp_subaccount.dev.id
  name             = "cf-dev"
  environment_type = "cloudfoundry"
  service_name     = "cloudfoundry"
  plan_name        = "standard"
  parameters = jsonencode({
    instance_name = "cf-dev"
  })
}

# HANA Cloud
resource "btp_subaccount_entitlement" "hana" {
  subaccount_id = btp_subaccount.dev.id
  service_name  = "hana-cloud"
  plan_name     = "hana"
  amount        = 1
}

# Admin role assignment
resource "btp_subaccount_role_collection_assignment" "admins" {
  for_each = toset(var.admins)

  subaccount_id        = btp_subaccount.dev.id
  role_collection_name = "Subaccount Administrator"
  user_name           = each.value
}

# outputs.tf
output "subaccount_id" {
  value = btp_subaccount.dev.id
}

output "cf_api_endpoint" {
  value = btp_subaccount_environment_instance.cf.labels["API Endpoint"]
}
```

### Terraform Commands

```bash
# Initialize
terraform init

# Plan changes
terraform plan -var-file="dev.tfvars"

# Apply changes
terraform apply -var-file="dev.tfvars"

# Destroy resources
terraform destroy -var-file="dev.tfvars"
```

## Manual Setup Steps

### 1. Global Account Configuration

1. Access SAP BTP Cockpit
2. Navigate to Global Account
3. Configure directories (optional)
4. Set up entitlements

### 2. Subaccount Creation

1. Click "Create Subaccount"
2. Specify name and subdomain
3. Select region
4. Configure labels
5. Enable environments

### 3. Entitlement Assignment

1. Navigate to Entitlements
2. Configure Service Assignments
3. Set quotas per service
4. Assign to subaccounts

### 4. User Management

1. Navigate to Security > Users
2. Add users by email
3. Assign role collections
4. Configure IdP trust (optional)

## ABAP System Landscape Setup

### Recommended Landscapes

Start with only needed systems. Additional systems can be provisioned later.

**3-System Landscape (DEV, QAS, PRD)**
- Recommended for most projects
- Suitable when development is occasional or release cycles are less frequent
- Enables testing outside development
- Verifies application behavior before production

**5-System Landscape (DEV, COR, TST, QAS, PRD)**
- Appropriate for larger teams with continuous development
- Enables parallel correction handling
- Supports uninterrupted development work

### Sizing Specifications

**Production Capacity:**
- 1 ACU can serve up to **1,000 active business users per day**

**Recommended Minimum Starting Configuration:**

| Resource | Size | Memory |
|----------|------|--------|
| ABAP Compute Units (ACU) | 1 | 16 GB |
| HANA Compute Units (HCU) | 2 | 32 GB total |

**Scaling Options:**
- Manual scaling via SAP BTP Cockpit
- Automatic runtime scaling (Release 2402+) requires consumption-based contract

**Cost Optimization:**
- Use system hibernation for DEV, COR, TST systems during inactive periods
- Reduces costs significantly when systems not in use

## Best Practices

### Account Structure

| Environment | Purpose | Entitlements |
|-------------|---------|--------------|
| Development | Development work | Full entitlements |
| QA/Test | Testing | Production-like |
| Production | Live workloads | Production quotas |
| Sandbox | Experimentation | Minimal |

### Security

1. **Least privilege** - Minimal necessary permissions
2. **Separation of duties** - Different roles for different tasks
3. **Audit logging** - Enable for compliance
4. **IdP integration** - Use corporate identity

### Automation

1. **Use Terraform** for reproducibility
2. **Version control** configurations
3. **CI/CD integration** for changes
4. **Document** manual steps

## Source Documentation

- Setup: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/set-up-3b774f8.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/set-up-3b774f8.md)
- SAP BTP Administrator's Guide: [https://help.sap.com/docs/btp/sap-business-technology-platform/administration-and-operations](https://help.sap.com/docs/btp/sap-business-technology-platform/administration-and-operations)
- Terraform Provider: [https://registry.terraform.io/providers/SAP/btp/latest](https://registry.terraform.io/providers/SAP/btp/latest)
