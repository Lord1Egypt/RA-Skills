# SAP BTP Development Tools Reference

## Development Environments

### SAP Business Application Studio

**Type**: Cloud-based IDE optimized for SAP development

**Foundation**: Code-OSS (VS Code base)

**Capabilities:**
- SAP Fiori application development
- CAP application development
- HANA database extensions
- Full-stack development
- Mobile development

**Dev Spaces:**

| Dev Space | Purpose |
|-----------|---------|
| Full Stack Cloud Application | CAP, Fiori, HANA |
| SAP Fiori | Fiori Elements, Freestyle |
| SAP HANA Native Application | HDI containers, calculation views |
| SAP Mobile Application | Mobile Development Kit |
| Basic | General development |

### ABAP Development Tools (ADT)

**Type**: Eclipse-based IDE for ABAP development

**Capabilities:**
- ABAP Cloud development
- RAP business objects
- CDS view modeling
- ABAP unit testing
- ATC integration

**Installation:**
1. Download Eclipse IDE
2. Install ADT from SAP update site
3. Connect to ABAP system

### SAP Build

**Type**: Low-code/no-code platform

**Components:**
- **SAP Build Apps**: Drag-and-drop application creation
- **SAP Build Process Automation**: Workflow and RPA
- **SAP Build Work Zone**: Business sites

## Administrative Tools

### SAP BTP Cockpit

**Purpose**: Web-based platform administration

**Capabilities:**
- Application management
- Resource configuration
- Security monitoring
- Cloud application operations
- Entitlement management

### Landscape Portal

**Purpose**: Partner and SaaS management (ABAP)

**Capabilities:**
- System management
- Tenant management
- Product lifecycle
- Deployment pipelines

## Command-Line Tools

### Cloud Foundry CLI

**Purpose**: Deploy and manage CF applications

**Installation:**
```bash
# macOS
brew install cloudfoundry/tap/cf-cli

# Windows
choco install cloudfoundry-cli

# Linux
wget -q -O - https://packages.cloudfoundry.org/debian/cli.cloudfoundry.org.key | sudo apt-key add -
echo "deb https://packages.cloudfoundry.org/debian stable main" | sudo tee /etc/apt/sources.list.d/cloudfoundry-cli.list
sudo apt update && sudo apt install cf-cli
```

**Common Commands:**
```bash
# Login
cf login -a https://api.cf.eu10.hana.ondemand.com

# Deploy
cf push my-app

# View apps
cf apps

# View services
cf services

# Scale
cf scale my-app -i 3

# Logs
cf logs my-app --recent
```

### CDS CLI

**Purpose**: CAP development commands

**Installation:**
```bash
# Install latest version (recommended for new projects)
npm install -g @sap/cds-dk@latest

# Or pin to specific version for reproducibility
npm install -g @sap/cds-dk@8.0.0
```

> **Version Strategy**: Use `@latest` for development to get newest features. For CI/CD pipelines and team consistency, pin to a specific version in your project's `package.json` devDependencies.

**Common Commands:**
```bash
cds init my-project        # Create project
cds add hana               # Add HANA support
cds add xsuaa              # Add authentication
cds watch                  # Run with live reload
cds build                  # Build for deployment
cds deploy                 # Deploy to HANA
cds compile                # Compile CDS models
```

### MTA Build Tool (mbt)

**Purpose**: Build multitarget applications

**Installation:**
```bash
npm install -g mbt
```

**Commands:**
```bash
mbt build                  # Build MTA archive
mbt build -t ./            # Build to current directory
```

### CF MTA Plugin

**Purpose**: Deploy MTA archives

**Installation:**
```bash
cf install-plugin multiapps
```

**Commands:**
```bash
cf deploy my-app.mtar      # Deploy MTA
cf mtas                    # List deployed MTAs
cf undeploy my-app         # Undeploy MTA
```

## Kubernetes Tools

### kubectl

**Purpose**: Kubernetes cluster management

**Commands:**
```bash
kubectl get pods           # List pods
kubectl logs my-pod        # View logs
kubectl describe pod       # Pod details
kubectl apply -f file.yaml # Apply configuration
```

### kubelogin

**Purpose**: OIDC authentication for kubectl

### Helm

**Purpose**: Kubernetes package manager

**Commands:**
```bash
helm install my-app ./chart      # Install chart
helm upgrade my-app ./chart      # Upgrade release
helm list                        # List releases
helm uninstall my-app            # Uninstall
```

### Paketo (Pack)

**Purpose**: Cloud Native Buildpacks for container images

**Commands:**
```bash
pack build my-image --builder paketobuildpacks/builder:base
```

### Docker Desktop

**Purpose**: Local container development

## Infrastructure Tools

### Terraform Provider for SAP BTP

**Purpose**: Infrastructure as code for SAP BTP

**Configuration:**
```hcl
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

resource "btp_subaccount" "my_subaccount" {
  name      = "my-subaccount"
  region    = "eu10"
  subdomain = "my-subdomain"
}
```

### Cloud Connector

**Purpose**: Secure on-premise connectivity

**Features:**
- Reverse proxy operation
- Access control
- High availability
- Audit logging

## Development Libraries

### SAP Cloud SDK

**Purpose**: Abstraction layer for enterprise development

**Languages**: Java, JavaScript/TypeScript

**Features:**
- Logging
- Multitenancy
- Connectivity
- OData/OpenAPI clients

**Installation (Node.js):**
```bash
npm install @sap-cloud-sdk/core
npm install @sap-cloud-sdk/odata-v2-generator
```

**Example:**
```javascript
const { BusinessPartner } = require('@sap/cloud-sdk-vdm-business-partner-service');

const partners = await BusinessPartner.requestBuilder()
  .getAll()
  .execute({ destinationName: 'S4HANA' });
```

## SAP Fiori Tools

### Capabilities

| Tool | Purpose |
|------|---------|
| Application Wizard | Generate Fiori apps |
| Service Modeler | Design OData services |
| Page Editor | Configure Fiori Elements pages |
| Guided Development | Step-by-step development |
| XML Editor | Edit Fiori Elements views |

### Installation (VS Code)

Search for "SAP Fiori tools" in VS Code extensions.

## Service-Specific Tools

Available through SAP Discovery Center for individual services.

## Source Documentation

- Tools Available: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/tools-available-for-sap-btp-multi-cloud-foundation-7f95cfa.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/tools-available-for-sap-btp-multi-cloud-foundation-7f95cfa.md)
- SAP Discovery Center: [https://discovery-center.cloud.sap/](https://discovery-center.cloud.sap/)
