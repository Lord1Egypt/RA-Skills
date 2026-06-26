# Multitarget Applications (MTA) Reference

## Overview

Multitarget Applications enable packaging multiple interconnected cloud components into a single deployable bundle, addressing the complexity of modern cloud applications.

## Key Characteristics

- Single archive with all modules and dependencies
- Deployable across multiple SAP BTP subaccounts
- Automated deployment in proper dependency order
- Integrated deployment descriptor (mta.yaml)

## When to Use MTAs

| Scenario | Recommendation |
|----------|----------------|
| Business app with multiple components | Use MTA |
| Dependencies on external resources (DB, messaging) | Use MTA |
| Need standardized configuration | Use MTA |
| Simple single-module app | Consider cf push |

## Creation Options

| Tool | Description |
|------|-------------|
| SAP Business Application Studio | Native MTA support |
| SAP Web IDE Full-Stack | Automatic descriptor maintenance |
| mbt (Command Line) | Java-based builder |
| CI/CD Pipelines | Automated archive generation |

## MTA Structure

```
my-app/
├── mta.yaml              # Deployment descriptor
├── package.json          # Node.js dependencies
├── xs-security.json      # Security configuration
├── app/                  # UI module
│   ├── webapp/
│   └── package.json
├── srv/                  # Service module
│   ├── src/
│   └── package.json
└── db/                   # Database module
    ├── src/
    └── package.json
```

## mta.yaml Anatomy

### Schema and Identification

```yaml
_schema-version: "3.1"
ID: my-cap-app
version: 1.0.0
description: My CAP Application
```

### Parameters

```yaml
parameters:
  enable-parallel-deployments: true
  deploy_mode: html5-repo
```

### Modules

```yaml
modules:
  - name: my-srv
    type: nodejs
    path: gen/srv
    parameters:
      buildpack: nodejs_buildpack
      memory: 256M
      disk-quota: 512M
    build-parameters:
      builder: npm
    requires:
      - name: my-hana
      - name: my-xsuaa
    provides:
      - name: srv-api
        properties:
          srv-url: ${default-url}
```

### Resources

```yaml
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
```

## Module Types

| Type | Description |
|------|-------------|
| nodejs | Node.js application |
| java | Java application |
| hdb | HANA database content |
| html5 | Static HTML5 content |
| approuter.nodejs | Application Router |
| com.sap.application.content | Generic content |

## Resource Types

| Type | Description |
|------|-------------|
| com.sap.xs.hdi-container | HDI container |
| org.cloudfoundry.managed-service | Managed service instance |
| org.cloudfoundry.existing-service | Existing service reference |
| org.cloudfoundry.user-provided-service | User-provided service |

## Complete Example

```yaml
_schema-version: "3.1"
ID: incident-management
version: 1.0.0

parameters:
  enable-parallel-deployments: true

build-parameters:
  before-all:
    - builder: custom
      commands:
        - npm ci
        - npx cds build --production

modules:
  # Service module
  - name: incident-srv
    type: nodejs
    path: gen/srv
    parameters:
      buildpack: nodejs_buildpack
      memory: 256M
    requires:
      - name: incident-db
      - name: incident-auth
      - name: incident-destination
    provides:
      - name: srv-api
        properties:
          srv-url: ${default-url}

  # Database deployer
  - name: incident-db-deployer
    type: hdb
    path: gen/db
    parameters:
      buildpack: nodejs_buildpack
    requires:
      - name: incident-db

  # UI Application
  - name: incident-app
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
      - name: incident-auth
      - name: incident-html5-repo-runtime

  # UI content deployer
  - name: incident-ui-deployer
    type: com.sap.application.content
    path: .
    requires:
      - name: incident-html5-repo-host
        parameters:
          content-target: true
    build-parameters:
      build-result: resources
      requires:
        - artifacts:
            - nsincidents.zip
          name: nsincidents
          target-path: resources/

  - name: nsincidents
    type: html5
    path: app/incidents
    build-parameters:
      build-result: dist
      builder: custom
      commands:
        - npm ci
        - npm run build:cf

resources:
  - name: incident-db
    type: com.sap.xs.hdi-container
    parameters:
      service: hana
      service-plan: hdi-shared

  - name: incident-auth
    type: org.cloudfoundry.managed-service
    parameters:
      service: xsuaa
      service-plan: application
      path: ./xs-security.json
      config:
        xsappname: incident-${org}-${space}
        tenant-mode: dedicated

  - name: incident-destination
    type: org.cloudfoundry.managed-service
    parameters:
      service: destination
      service-plan: lite

  - name: incident-html5-repo-runtime
    type: org.cloudfoundry.managed-service
    parameters:
      service: html5-apps-repo
      service-plan: app-runtime

  - name: incident-html5-repo-host
    type: org.cloudfoundry.managed-service
    parameters:
      service: html5-apps-repo
      service-plan: app-host
```

## Build Commands

```bash
# Install MTA Build Tool
npm install -g mbt

# Build MTA archive
mbt build

# Build with specific platform
mbt build -p cf

# Build to specific directory
mbt build -t ./dist
```

## Deploy Commands

```bash
# Install MTA plugin
cf install-plugin multiapps

# Deploy
cf deploy mta_archives/my-app_1.0.0.mtar

# Deploy with options
cf deploy my-app.mtar --version-rule ALL

# Blue-green deployment
cf bg-deploy my-app.mtar

# List deployed MTAs
cf mtas

# Undeploy
cf undeploy my-app --delete-services
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Service binding fails | Service not ready | Add dependency order |
| Memory exceeded | Insufficient allocation | Increase in mta.yaml |
| Build fails | Missing dependencies | Run npm ci first |
| Deploy timeout | Large application | Increase timeout |

## Best Practices

1. **Use build-parameters** for complex builds
2. **Enable parallel deployments** for faster deploys
3. **Externalize configuration** via variables
4. **Version your MTAs** semantically
5. **Test locally** before deploying

## Source Documentation

- Using MTAs: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/using-multitarget-applications-to-manage-dependencies-41184aa.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/using-multitarget-applications-to-manage-dependencies-41184aa.md)
- MTA Documentation: [https://help.sap.com/docs/btp/sap-business-technology-platform/multitarget-applications-in-cloud-foundry-environment](https://help.sap.com/docs/btp/sap-business-technology-platform/multitarget-applications-in-cloud-foundry-environment)
