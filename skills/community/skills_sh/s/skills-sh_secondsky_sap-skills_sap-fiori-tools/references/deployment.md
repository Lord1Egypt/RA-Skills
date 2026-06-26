# Deployment Reference

Comprehensive reference for deploying SAP Fiori applications to ABAP and Cloud Foundry.

## Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [ABAP Deployment](#abap-deployment)
3. [Cloud Foundry Deployment](#cloud-foundry-deployment)
4. [Fiori Launchpad Configuration](#fiori-launchpad-configuration)
5. [Undeployment](#undeployment)
6. [Troubleshooting](#troubleshooting)

---

## Deployment Overview

SAP Fiori tools supports deployment to two primary environments:

| Target | Repository | Runtime |
|--------|------------|---------|
| ABAP | SAPUI5 ABAP Repository | ABAP system provides hosting, routing, authentication |
| Cloud Foundry | HTML5 Repository | BTP provides hosting via HTML5 App Runtime |

### Deployment Workflow

1. Generate deployment configuration
2. Configure Fiori Launchpad (optional)
3. Execute deployment
4. Verify in target system

---

## ABAP Deployment

### Prerequisites

| Requirement | Details |
|-------------|---------|
| SAP_UI Component | Version 7.53 or higher |
| SAPUI5 ABAP Repository Service | `/sap/opu/odata/UI5/ABAP_REPOSITORY_SRV` enabled |
| Authorization | S_DEVELOP with required activities |
| Transport | Existing transport if package requires one |

### Authentication Methods

| Method | On-Premise | BTP ABAP |
|--------|------------|----------|
| Basic Authentication | Yes | No |
| OAuth 2.0 | No | Deprecated |
| Reentrance Ticket | No | Yes |

### Generate Configuration

**Command Palette**:
```
Fiori: Add Deployment Configuration
```

**CLI**:
```bash
npx fiori add deploy-config
```

### Configuration Prompts

| Field | Description | Required |
|-------|-------------|----------|
| Target | Select "ABAP" | Yes |
| Target System | Saved system or URL | Yes |
| Client | SAP client number (3 digits) | Yes |
| SAPUI5 ABAP Repository | Application name for deployment | Yes |
| Deployment Description | Optional descriptive text | No |
| Package | Valid ABAP package name | Yes |
| Transport Request | See options below | Yes |

### Transport Request Options

1. **Enter manually** - Provide transport request ID directly
2. **Choose from existing** - Select from system-provided list
3. **Create new** - Auto-generate during configuration
4. **Create during deployment** - Auto-generate on first deployment

### Generated Files

**ui5-deploy.yaml**:
```yaml
specVersion: "2.4"
metadata:
  name: project-name
type: application
builder:
  resources:
    excludes:
      - /test/**
      - /localService/**
deploy:
  target:
    url: https://system.url
    client: "100"
    scp: false
    params:
      sap-language: EN
  app:
    name: ZAPP_NAME
    package: ZPACKAGE
    description: Application description
    transport: DEVK900123
```

**package.json update**:
```json
{
  "scripts": {
    "deploy": "fiori deploy --config ui5-deploy.yaml"
  }
}
```

### Execute Deployment

```bash
npm run deploy
```

The command:
1. Builds the application
2. Creates ZIP of `dist` folder
3. Uploads to SAPUI5 ABAP Repository
4. Registers with transport (if applicable)

---

## Cloud Foundry Deployment

### Prerequisites

| Requirement | Installation |
|-------------|-------------|
| MTA Build Tool | `npm install -g mta` (version 1.0+) |
| GNU Make | Required on Windows (version 4.2.1) |
| Cloud Foundry CLI | Download from official site |
| MultiApps Plugin | `cf install-plugin -r CF-Community "multiapps"` |
| Backend Destination | Configured in BTP cockpit |

### Generate Configuration

**Command Palette**:
```
Fiori: Add Deployment Configuration
```

Select "Cloud Foundry" as target.

### Configuration Prompts

| Field | Description |
|-------|-------------|
| Destination Name | BTP destination for backend |
| Add Application Router | Yes for standalone deployment |
| Override HTML5 App Name | Custom name in repository |

### Generated Project Structure

```
project/
├── webapp/
│   └── manifest.json
├── mta.yaml                  # MTA descriptor
├── xs-app.json               # App router configuration
├── xs-security.json          # Security descriptor
├── package.json              # Updated with scripts
├── ui5.yaml
└── ui5-deploy.yaml
```

### MTA Descriptor (mta.yaml)

```yaml
_schema-version: "3.2"
ID: project-name
version: 0.0.1
modules:
  - name: project-name-destination-content
    type: com.sap.application.content
    requires:
      - name: project-name-destination-service
        parameters:
          content-target: true
      - name: project-name-repo-host
        parameters:
          service-key:
            name: project-name-repo-host-key
      - name: project-name-uaa
        parameters:
          service-key:
            name: project-name-uaa-key
    parameters:
      content:
        instance:
          destinations:
            - Name: project-name-repo-host
              ServiceInstanceName: project-name-html5-srv
              ServiceKeyName: project-name-repo-host-key
              sap.cloud.service: project-name
            - Authentication: OAuth2UserTokenExchange
              Name: project-name-uaa
              ServiceInstanceName: project-name-xsuaa
              ServiceKeyName: project-name-uaa-key
              sap.cloud.service: project-name
          existing_destinations_policy: update

  - name: project-name
    type: html5
    path: .
    build-parameters:
      build-result: dist
      builder: custom
      commands:
        - npm install
        - npm run build:cf

resources:
  - name: project-name-repo-host
    type: org.cloudfoundry.managed-service
    parameters:
      service: html5-apps-repo
      service-plan: app-host
  - name: project-name-destination-service
    type: org.cloudfoundry.managed-service
    parameters:
      service: destination
      service-plan: lite
  - name: project-name-uaa
    type: org.cloudfoundry.managed-service
    parameters:
      service: xsuaa
      service-plan: application
      config:
        xsappname: project-name
        tenant-mode: dedicated
```

### xs-app.json (App Router Configuration)

```json
{
  "welcomeFile": "/index.html",
  "authenticationMethod": "route",
  "routes": [
    {
      "source": "^/sap/opu/odata/(.*)$",
      "target": "/sap/opu/odata/$1",
      "destination": "backend-destination",
      "authenticationType": "xsuaa"
    },
    {
      "source": "^(.*)$",
      "target": "$1",
      "service": "html5-apps-repo-rt",
      "authenticationType": "xsuaa"
    }
  ]
}
```

### Build and Deploy

```bash
# Build MTA archive
npm run build

# Deploy to Cloud Foundry
npm run deploy
```

Or using CF CLI directly:

```bash
# Build
mbt build

# Deploy
cf deploy mta_archives/project-name_0.0.1.mtar
```

### SAP Business Application Studio Alternative

1. Create Basic Multitarget Application template
2. Add Approuter Configuration module
3. Configure destination-content module

---

## Fiori Launchpad Configuration

### Generate Configuration

**Command Palette**:
```
Fiori: Add Fiori Launchpad Configuration
```

**CLI**:
```bash
npx @sap-ux/create
```

### Configuration Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| Semantic Object | Unique identifier | `Product` |
| Action | Navigation action | `display`, `manage`, `create` |
| Title | Tile title | `Manage Products` |
| Subtitle | Tile subtitle (optional) | `Product Management` |

### Manifest Updates

```json
{
  "sap.app": {
    "crossNavigation": {
      "inbounds": {
        "intent1": {
          "semanticObject": "Product",
          "action": "display",
          "title": "{{appTitle}}",
          "subTitle": "{{appSubTitle}}",
          "signature": {
            "parameters": {},
            "additionalParameters": "allowed"
          }
        }
      }
    }
  }
}
```

---

## Undeployment

### ABAP Undeployment

Via Application Info page or CLI:

```bash
npx fiori undeploy --config ui5-deploy.yaml
```

### Cloud Foundry Undeployment

```bash
cf undeploy project-name --delete-services
```

---

## Troubleshooting

### Common ABAP Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Service activation error | SAP_UI component outdated | Verify SAP_UI 7.53+ |
| 400 status error | Backend processing error | Check `/IWFND/ERROR_LOG` |
| Virus scan failure | Scan profile misconfigured | Configure `/IWFND/VIRUS_SCAN` |
| Authorization error | Missing S_DEVELOP | Grant required authorizations |

### Debug Deployment

**macOS/Linux**:
```bash
DEBUG=ux-odata-client npm run deploy
```

**Windows**:
```bash
set DEBUG=ux-odata-client & npm run deploy
```

### CLI Help

```bash
npx fiori help                 # All commands
npx fiori deploy help          # Deploy command options
npx fiori add deploy-config help  # Configuration options
```

### Required OData Services

Ensure these services are enabled and accessible:

| Service | Path |
|---------|------|
| SAPUI5 Repository | `/sap/opu/odata/UI5/ABAP_REPOSITORY_SRV` |
| OData V2 Catalog | `/sap/opu/odata/IWFND/CATALOGSERVICE;v=2` |
| OData V4 Catalog (dev) | `/sap/opu/odata4/iwfnd/config/default/iwfnd/catalog/0001` |
| OData V4 Catalog (prod) | `/sap/opu/odata4/iwfnd/config/default/iwfnd/catalog/0002` |
| ATO Settings | `/sap/bc/adt/ato/settings` |

---

## Central Application Router

For exposing applications through central managed router:

1. Configure destination to HTML5 Repository
2. Set up managed application router service
3. Reference application in launchpad configuration

See `expose-application-to-central-application-router-85ad10d.md` for details.

---

## Documentation Source

**GitHub**: [https://github.com/SAP-docs/btp-fiori-tools/tree/main/docs/Deploying-an-Application](https://github.com/SAP-docs/btp-fiori-tools/tree/main/docs/Deploying-an-Application)

Key files:
- `deploying-an-application-1b7a3be.md`
- `deployment-configuration-1c85927.md`
- `generate-deployment-configuration-abap-c06b9cb.md`
- `generate-deployment-configuration-cloud-foundry-41e63bd.md`
- `sap-fiori-launchpad-configuration-bc3cb89.md`
- `deployment-of-application-607014e.md`
- `undeploy-an-application-70872c4.md`
- `security-8a147c6.md`
