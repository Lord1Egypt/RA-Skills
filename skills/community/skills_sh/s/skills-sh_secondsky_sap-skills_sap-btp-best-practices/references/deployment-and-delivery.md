# SAP BTP Deployment and Delivery - Detailed Reference

**Source**: [https://github.com/SAP-docs/btp-best-practices-guide/tree/main/docs/deploy-and-deliver](https://github.com/SAP-docs/btp-best-practices-guide/tree/main/docs/deploy-and-deliver)

---

## Deployment Overview

After development, applications are deployed to TEST and PROD environments. The approach depends on organizational needs:

- **Simple applications**: Manual deployment acceptable
- **Enterprise settings**: Managed, automated delivery recommended

---

## Deployment Methods by Runtime

### Cloud Foundry Environment

**Key Recommendation**: Archive all components into one package as a Multitarget Application (MTA) archive including a deployment descriptor.

#### Java Applications

Deploy via:
- SAP BTP cockpit
- Cloud Foundry CLI
- Multiple runtime and JVM options available

#### HTML5 Applications

Deploy via:
- SAP Business Application Studio
- Cloud Foundry CLI
- SAP BTP cockpit

#### Node.js Applications

Deploy via:
- SAP Business Application Studio
- Cloud Foundry CLI

#### SAP HANA XSA Applications

Deploy via:
- SAP HANA Deployment Infrastructure (HDI) in Business Application Studio
- Cloud Foundry CLI

#### Custom Buildpacks

Cloud Foundry supports "Bring Your Own Buildpack" for custom runtime needs.

### Neo Environment

Similar deployment options to Cloud Foundry with:
- SAP BTP cockpit
- Neo console client

### Kyma Environment

**Core Requirement**: Package applications in Linux Docker images.

**Options**:
- Standard Dockerfile
- Cloud Native Buildpacks

**Production Setup**:
- Use automation tools like SAP Continuous Integration and Delivery
- Deploy with Helm charts
- Sample GitHub repositories available for Java, Node.js, HTML5

---

## Delivery Options

### Enterprise Delivery Approach

A managed, automated delivery approach is recommended because it:
- Is less error-prone
- Creates repeatable outcomes
- Enables governance
- Provides central control over production propagation

### Delivery Options Matrix

| Content Type | CI/CD | Cloud Transport Mgmt | CTS+ |
|--------------|-------|---------------------|------|
| Development Content (Java, HTML5, CAP) | Recommended | Recommended | - |
| SAP Cloud Integration Content | In development | Recommended | - |
| SAP HANA Cloud Artifacts | Recommended | Recommended | - |
| SAP Build Work Zone | - | Recommended | - |
| Other App-Specific Content | - | Recommended | Recommended |
| Kyma-Based Apps | Recommended | - | - |

---

## SAP Continuous Integration and Delivery

### Solution Options

| Aspect | SAP CI/CD Service | Project "Piper" |
|--------|-------------------|-----------------|
| Expertise Required | Low | Medium-to-High |
| Flexibility | Medium | High |
| Infrastructure | Ready-to-use | Requires Jenkins (or Cx Server) |
| Support | Direct SAP support | Open-source community |
| Best For | Typical SAP customers | Advanced customization |

### SAP CI/CD Service Features

- Pre-configured pipelines for SAP technologies
- Built-in code quality checks
- Automated testing integration
- Direct deployment to SAP BTP

### Project "Piper"

- Open-source CI/CD library
- Extensive customization options
- Jenkins-based pipelines
- GitHub: [https://github.com/SAP/jenkins-library](https://github.com/SAP/jenkins-library)

---

## Transport Management

### SAP Cloud Transport Management

Centralizes handling of development content archives across subaccounts and global accounts.

**Features**:
- MTA file transport
- Application-specific content transport
- Cross-global account transport
- Integration with change management tools

**Recommendation**: Use for all SAP BTP content regardless of format.

### CTS+ (Change and Transport System)

- Operates on-premise within ABAP systems
- Supports SAP BTP artifacts packaged as MTA archives
- Integration with SAP Solution Manager

**Direction**: SAP Cloud Transport Management is the future-proof choice.

### Combined CI/CD and Transport Approach

```
Developer Commit
       │
       ▼
┌──────────────────┐
│   CI Pipeline    │ (Build, Test, Deploy to Dev)
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────┐
│  SAP Cloud Transport Management  │
│                                  │
│  Dev ──► Test ──► Production     │
│  (Governance-defined pathways)   │
└──────────────────────────────────┘
         │
         ▼
   Optional Integration
   with SAP Cloud ALM or
   SAP Solution Manager
```

---

## Change Management Integration

### SAP Cloud ALM Integration

- Change and deployment management
- Centralized landscape definition
- Access control configuration
- Synchronized transports

### SAP Solution Manager Integration

- Minimum version: 7.2 SP10
- Hybrid scenario support (on-premise + cloud)
- Parallel operation with CTS+ and Cloud Transport Management

---

## Manual Delivery Methods

For simpler scenarios:

1. **Direct IDE Deployment**:
   - Deploy to multiple subaccounts via cockpit or CLI

2. **Solution Export Wizard** (Neo):
   - Model solutions as MTA files
   - Export for transport

3. **Git Repository Synchronization**:
   - For HTML5 applications
   - Manual deployment after sync

4. **SAP HANA XS Application Lifecycle Management**:
   - Transport routes between systems

---

## Multitarget Application (MTA) Archives

### Structure

```
my-app.mtar
├── mta.yaml (deployment descriptor)
├── app-module-1/
├── app-module-2/
├── db-module/
└── srv-module/
```

### mta.yaml Example

```yaml
_schema-version: "3.1"
ID: my-mta-app
version: 1.0.0

modules:
  - name: my-srv
    type: nodejs
    path: srv
    provides:
      - name: srv-api
        properties:
          url: ${default-url}
    requires:
      - name: my-db
      - name: my-auth

  - name: my-db-deployer
    type: hdb
    path: db
    requires:
      - name: my-db

resources:
  - name: my-db
    type: com.sap.xs.hdi-container
  - name: my-auth
    type: org.cloudfoundry.managed-service
    parameters:
      service: xsuaa
      service-plan: application
```

### Building MTAs

```bash
# Install MTA Build Tool
npm install -g mbt

# Build MTA archive
mbt build

# Result: mta_archives/my-app_1.0.0.mtar
```

---

## Kyma Deployment Details

### Docker Image Creation

**Standard Dockerfile**:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 8080
CMD ["npm", "start"]
```

**Cloud Native Buildpacks**:
```bash
# Using pack CLI
pack build my-app --builder paketobuildpacks/builder:base
```

### Helm Chart Structure

```
my-app/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── configmap.yaml
└── charts/
```

### Deployment Commands

```bash
# Deploy with Helm
helm upgrade --install my-app ./my-app \
  --namespace my-namespace \
  --set image.tag=1.0.0

# Or use kubectl directly
kubectl apply -f k8s/
```

---

## CI/CD Pipeline Example

### SAP CI/CD Service Configuration

```yaml
# .pipeline/config.yml
general:
  buildTool: 'mta'

stages:
  Build:
    mtaBuild: true

  Additional Unit Tests:
    npmExecuteScripts:
      - 'test'

  Acceptance:
    cloudFoundryDeploy:
      deployTool: 'mtaDeployPlugin'
      deployType: 'standard'

  Release:
    cloudFoundryDeploy:
      deployTool: 'mtaDeployPlugin'
      deployType: 'standard'
```

### Jenkins Pipeline (Project Piper)

```groovy
@Library('piper-lib-os') _

node {
    stage('Init') {
        checkout scm
        setupCommonPipelineEnvironment script: this
    }

    stage('Build') {
        mtaBuild script: this
    }

    stage('Deploy') {
        cloudFoundryDeploy script: this
    }
}
```

---

## Transport Landscape Configuration

### Defining Transport Routes

```
┌─────────────────────────────────────────────────────┐
│           SAP Cloud Transport Management            │
├─────────────────────────────────────────────────────┤
│                                                     │
│   Node: Development                                 │
│   ├── Import Queue                                  │
│   └── Forward to: Test                              │
│                                                     │
│   Node: Test                                        │
│   ├── Import Queue                                  │
│   └── Forward to: Production                        │
│                                                     │
│   Node: Production                                  │
│   └── Import Queue                                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Upload to Transport Management

```bash
# Using Cloud Transport Management API
curl -X POST "https://[ctms-url]/v2/files/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@my-app.mtar"

# Create transport request
curl -X POST "https://[ctms-url]/v2/nodes/[node-id]/transportRequests" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fileId": "[file-id]", "description": "Deploy version 1.0.0"}'
```

---

## Best Practices Summary

### Deployment

1. Use MTA archives for multi-component applications
2. Containerize applications for Kyma with proper Docker images
3. Implement proper health checks and probes
4. Use environment-specific configuration

### Delivery

1. Combine CI/CD with Cloud Transport Management
2. Automate testing at every stage
3. Implement proper approvals for production
4. Maintain audit trails for compliance

### Governance

1. Define clear transport routes
2. Implement approval workflows
3. Restrict who can deploy to production
4. Track all changes through transport requests

---

**Source Documentation**:
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/deploy-and-deliver-5972cdb.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/deploy-and-deliver-5972cdb.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/deploying-applications-866ab13.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/deploying-applications-866ab13.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/delivering-applications-b39bae3.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/deploy-and-deliver/delivering-applications-b39bae3.md)
