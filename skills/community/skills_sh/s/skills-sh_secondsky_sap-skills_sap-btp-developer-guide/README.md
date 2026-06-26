# SAP BTP Developer Guide Skill

Comprehensive skill for developing business applications on SAP Business Technology Platform using CAP (Node.js/Java) or ABAP Cloud.

## Capability Index

| Capability | Status |
|------------|--------|
| Commands | 1: `/btp-app-readiness-review` |
| Agents | 0 |
| Hooks | No |
| MCP | No |
| LSP | No |
| Source Freshness | `last_verified`: 2025-11-27; app readiness guidance requires project/tenant evidence for final verification. |
| Verification | `npm run validate`; deployment checks pending unless target evidence is provided. |

## Auto-Trigger Keywords

This skill triggers when discussing:

### Platform & Runtime
- SAP BTP, SAP Business Technology Platform
- Cloud Foundry, CF runtime, Cloud Foundry deployment
- Kyma, Kyma runtime, Kubernetes on SAP
- SAP BTP ABAP environment, ABAP Cloud
- BTP subaccount, global account, entitlements

### CAP Development
- CAP, Cloud Application Programming Model
- CDS, Core Data Services, cds init
- CAP Node.js, CAP Java, CAP TypeScript
- cds watch, cds build, cds deploy
- @sap/cds, @sap/cds-dk
- OData service, REST API on BTP

### ABAP Cloud Development
- RAP, ABAP RESTful Application Programming Model
- ABAP CDS views, ABAP behavior definition
- ABAP Development Tools, ADT Eclipse
- gCTS, abapGit, ABAP transport
- ABAP Cloud, ABAP environment
- ABAP unit test, ATC check

### UI Development
- SAP Fiori, SAP Fiori Elements
- SAPUI5, UI5 development
- Fiori Launchpad, FLP
- SAP Build Work Zone
- Fiori annotations, UI annotations

### Database
- SAP HANA Cloud, HDI container
- hdi-shared, HANA deployment
- CDS persistence, database artifacts
- HANA elastic scaling, NSE, ECN

### Security
- XSUAA, xs-security.json
- SAP Identity Authentication, IAS
- OAuth, OpenID Connect on BTP
- Role collections, authorization
- SAP Credential Store

### Connectivity
- SAP Connectivity Service, Cloud Connector
- SAP Destination Service, destinations
- Remote service, external service
- Principal propagation, user propagation
- SAP Cloud SDK

### Integration
- SAP Event Mesh, eventing
- SAP Integration Suite
- SAP API Business Hub
- S/4HANA integration, SuccessFactors integration
- Side-by-side extension

### Deployment
- MTA, multitarget application
- mta.yaml, mbt build
- cf deploy, cf push
- Helm chart, Kubernetes deployment
- Terraform SAP BTP

### CI/CD
- SAP Continuous Integration and Delivery
- CI/CD pipeline SAP
- Build automation SAP

### Observability
- SAP Cloud ALM, Cloud ALM
- SAP Cloud Logging
- OpenTelemetry SAP
- SAP Alert Notification
- Technical Monitoring Cockpit

### Development Tools
- SAP Business Application Studio, BAS
- SAP Build, low-code SAP
- CF CLI, Cloud Foundry CLI
- SAP Fiori tools

### Multitenancy
- Multitenant SAP, SaaS SAP BTP
- Tenant isolation, subscriber
- Key user extensibility

### Partner/ISV
- SAP ISV, independent software vendor
- Landscape Portal
- Add-on product, partner solution
- SAP PartnerEdge

### Operations
- System hibernation ABAP
- Elastic scaling ABAP
- ABAP compute units, ACU, HCU
- SAP BTP operations

### Common Scenarios
- "deploy to SAP BTP"
- "create CAP application"
- "build Fiori app"
- "connect to S/4HANA"
- "set up HANA Cloud"
- "configure authentication BTP"
- "multitenant application"
- "ABAP Cloud development"
- "SAP extension application"

## Skill Contents

### Main File
- `SKILL.md` - Core guidance for SAP BTP development

### Reference Files (Progressive Disclosure)
| File | Content |
|------|---------|
| `references/architecture.md` | Platform services, tools, architecture |
| `references/cap-development.md` | CAP development guide |
| `references/abap-cloud.md` | ABAP Cloud development guide |
| `references/connectivity.md` | Connectivity patterns and services |
| `references/security.md` | Security implementation |
| `references/observability.md` | Monitoring and logging |
| `references/cicd.md` | CI/CD pipelines |
| `references/deployment.md` | Deployment options |
| `references/tutorials.md` | Learning paths and missions |
| `references/partners.md` | ISV/Partner development |
| `references/operations.md` | Operations and scaling |
| `references/tools.md` | Development tools |
| `references/hana-cloud.md` | SAP HANA Cloud |
| `references/resilience.md` | Resilience patterns |
| `references/extensions.md` | SAP solution extensions |
| `references/mta.md` | Multitarget applications |
| `references/testing.md` | Testing strategies |
| `references/ux-design.md` | UX design and Fiori |
| `references/design-patterns.md` | Design patterns and DDD |
| `references/setup.md` | BTP setup and Terraform |
| `references/runtimes.md` | Runtime comparison (CF vs Kyma vs ABAP) |
| `references/whats-new.md` | Changelog and latest updates |

### Tracking

## Source Documentation

Based on: [https://github.com/SAP-docs/btp-developer-guide](https://github.com/SAP-docs/btp-developer-guide)

## Installation

Copy the `sap-btp-developer-guide` folder to your Claude Code skills directory:

```bash
# User-level installation
cp -r sap-btp-developer-guide ~/.claude/skills/

# Project-level installation
cp -r sap-btp-developer-guide .claude/skills/
```

## Usage

The skill automatically activates when you discuss SAP BTP development topics. Examples:

- "Create a CAP application with HANA database"
- "Deploy my app to Cloud Foundry"
- "Set up authentication with XSUAA"
- "Connect to S/4HANA from my CAP app"
- "Build a multitenant SaaS application"

## Version

- **Skill Version**: 1.1.0
- **Last Updated**: 2025-11-27
- **Last Verified**: 2025-11-27
- **SAP BTP Developer Guide Source**: [https://github.com/SAP-docs/btp-developer-guide](https://github.com/SAP-docs/btp-developer-guide)

## License

GPL-3.0
