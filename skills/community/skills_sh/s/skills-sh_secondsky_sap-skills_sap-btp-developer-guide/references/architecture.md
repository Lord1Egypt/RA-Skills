# SAP BTP Architecture Reference

## Platform Overview

SAP BTP provides a three-tier architecture:
- **Presentation Layer**: SAP Fiori/SAPUI5 frontends
- **Logic Layer**: CAP (Node.js/Java) or ABAP Cloud
- **Persistence Layer**: SAP HANA Cloud

**Data Protocols:**
- OData (transactional data)
- InA (analytical data)

## Core Services Catalog

### Persistence & Data

| Service | Purpose | Details |
|---------|---------|---------|
| SAP HANA Cloud | Database-as-a-Service | Relational, document, geospatial, vector data |
| HANA Data Lake Files | Object storage | Large-scale data storage |
| SAP Datasphere | Cross-application analytics | Data federation and warehousing |

**HANA Cloud Optimization Features:**

| Feature | Description | Free/Trial | Paid |
|---------|-------------|------------|------|
| **Native Storage Extension (NSE)** | Store infrequently accessed data on disk | No | Yes |
| **Elastic Compute Nodes (ECN)** | On-demand scaling for peak workloads | No | Yes |
| **Table Partitioning** | Enhanced query performance | Limited | Yes |
| **Native Multi-Tenancy** | Up to 1,000 isolated tenants per instance | No | Yes |
| **Free Tier** | 16GB memory at no cost | Yes (16GB) | N/A |

> **Note**: Feature availability varies by plan. See [SAP HANA Cloud Capacity Units](https://help.sap.com/docs/hana-cloud/sap-hana-cloud-administration-guide/capacity-units) for detailed tier comparison.

### Integration Services

| Service | Purpose | Supported Scenarios |
|---------|---------|---------------------|
| SAP Event Mesh | Event distribution | Cross-application eventing |
| SAP Integration Suite | API Management, Cloud Integration | B2B, A2A, API publishing |
| SAP Master Data Integration | Central data hub | SAP One Domain Model |
| Cloud Integration Automation | Guided workflows | Automated integration setup |

### Identity & Security

| Service | CAP | ABAP |
|---------|-----|------|
| SAP Authentication and Trust Management | Yes | Yes |
| Identity Authentication | Yes (SSO, on-prem) | Yes (SSO, on-prem) |
| SAP Credential Store | Yes (secrets via REST) | Communication Management |
| SAP Audit Log Service | Yes | Security audit logging |
| Identity Provisioning | Yes | Yes (business user provisioning) |

### Workflow & Automation

| Service | Purpose |
|---------|---------|
| SAP Task Center | Unified inbox across applications |
| SAP Build Process Automation | Workflow, RPA, decision management |
| SAP Job Scheduling Service | REST APIs, recurring schedules (CAP) |
| Application Jobs | Integrated scheduling (ABAP) |

### Observability

| Service | Purpose |
|---------|---------|
| SAP Cloud ALM | Central monitoring (RUM, health, integration) |
| SAP Cloud Logging | Logs, metrics, traces (OpenSearch-based) |
| SAP Alert Notification | Event subscriptions, multi-channel delivery |
| Technical Monitoring Cockpit | ABAP on-stack analysis |

### Extensibility Services

| Service | Purpose |
|---------|---------|
| SAP S/4HANA Cloud Extensibility | Side-by-side extensions |
| SAP SuccessFactors Extensibility | HR solution extensions |
| SAP Build Work Zone | Business sites, central entry point |

## Client Libraries

### CAP (Non-ABAP)
- **SAP Cloud SDK**: OData/OpenAPI clients, Destination, Connectivity services
- **Languages**: Java (Spring Boot), JavaScript, TypeScript (Node.js)
- **Guaranteed Node.js/Java version compatibility**

### ABAP
- **Service Consumption Model**: Generates local APIs for OData, SOAP, RFC
- **Communication Management**: System integration with credentials
- **Native RAP event support**

## User Interface Options

### Web Development
| Approach | Description | Use When |
|----------|-------------|----------|
| SAP Fiori Elements | Predefined templates (List Report, Object Page) | Standard business apps |
| Flexible Programming Model | Fiori Elements + custom extensions | Selective customization |
| Freestyle SAPUI5 | Full UI control | Highly custom interfaces |

### Mobile Development
| SDK | Platform |
|-----|----------|
| SAP Mobile Development Kit | Cross-platform |
| SAP BTP SDK for Android | Android native |
| SAP BTP SDK for iOS | iOS native |

Features: Offline sync, push notifications, mobile security

## Central Access Points

| Application Type | Entry Point |
|-----------------|-------------|
| CAP Applications | SAP Build Work Zone, HTML5 Repository |
| ABAP Applications | SAP Fiori Launchpad for BTP ABAP Environment |

## Analytics Capabilities

### CAP
- SAP Analytics Cloud (embedded dashboards)
- SAP Datasphere (cross-application analytics)

### ABAP
- SAP Analytics Cloud on InA-enabled CDS models
- Dragonfly-based multidimensional reporting
- SAP Datasphere via ABAP SQL Service

## System Landscape Management

### Unified Customer Landscape
- Auto-discovery of associated systems
- Manual system registration
- Support for S/4HANA, Ariba, SuccessFactors, third-party

### ABAP-Specific
- Landscape Portal for system hibernation
- Pre-upgrade nomination for quarterly releases

## Low-Code/No-Code Options

**SAP Build Suite:**
- SAP Build Apps (enterprise applications)
- SAP Build Process Automation (workflow, RPA)
- SAP Build Work Zone (business sites)
- Prebuilt connectors for SAP and third-party

## Infrastructure Automation

| Tool | Purpose |
|------|---------|
| Terraform Provider for SAP BTP | Resource provisioning automation |
| SAP Automation Pilot | Operational task automation, database lifecycle |

## Key Design Principles

1. **API-First**: Follow SAP Business Accelerator Hub guidelines
2. **Compliance**: Accessibility, theming for all UI components
3. **Observability**: Central unified operations experience
4. **Consistency**: Unified solution experience across customer base
5. **Enterprise Standards**: Prefer SAP BTP services over custom solutions

## Source Documentation

- Understanding Available Technology: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/understanding-available-technology-c1f21a4.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/understanding-available-technology-c1f21a4.md)
- Tools Available: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/tools-available-for-sap-btp-multi-cloud-foundation-7f95cfa.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/tools-available-for-sap-btp-multi-cloud-foundation-7f95cfa.md)
