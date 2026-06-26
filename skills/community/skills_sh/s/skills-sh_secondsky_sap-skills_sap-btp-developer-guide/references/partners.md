# SAP BTP Partner Development Reference

## Overview

SAP BTP provides deployment options for partners (ISVs) to build and deliver ABAP and CAP-based applications as products or SaaS offerings.

## Deployment Models

### Multitenant SaaS

**Definition**: Cloud service operated in partner's global account

**Characteristics:**
- Partner owns infrastructure
- Customers subscribe to service
- Partner manages operations, monitoring
- Customers get key-user extensibility

**Advantages:**
- Single codebase for all customers
- Centralized operations
- Easy updates (deploy once)
- Lower per-customer costs at scale

### Add-on Product

**Definition**: Product installed in customer's ABAP environment

**Characteristics:**
- Customer owns infrastructure
- Customer manages lifecycle
- Customer has full data control
- Developer extensibility available

**Requirements:**
- SAP PartnerEdge Build contract
- Distribution via SAP Store
- Registered ABAP namespace

## ABAP Partner Development

### Landscape Portal

**Purpose**: Central management for partner solutions

**Capabilities:**

| Feature | Description |
|---------|-------------|
| System Management | Create, configure ABAP systems |
| Tenant Management | SaaS tenant operations |
| Product Lifecycle | Build, register, publish products |
| Deployment Pipelines | CI/CD for ABAP |
| Monitoring | System and application health |

### Software Components

**Requirement**: At least one software component per solution

**Rules:**
- Registered ABAP namespace mandatory
- Y*/Z* objects only within single global account
- Multiple global accounts require add-on products

### Transport Mechanisms

| Tool | Use Case |
|------|----------|
| gCTS | BTP system-to-system transports (recommended) |
| abapGit | On-premise migration, backup, cross-account |
| Landscape Portal Products | Multi-account delivery |

### Namespace Requirements

**Mandatory**: All objects in a Product require registered namespace

**Process:**
1. Request namespace from SAP
2. Register in development system
3. Use namespace prefix for all objects

## CAP Partner Development

### Poetry Slam Manager

**Type**: Reference application for multitenant CAP SaaS

**GitHub**: [https://github.com/SAP-samples/partner-reference-application/](https://github.com/SAP-samples/partner-reference-application/)

**Demonstrates:**
- Full-stack cloud applications using SAP Cloud Application Programming Model (CAP)
- Multitenant architecture aligned with SAP BTP Developer's Guide
- ERP-agnostic design (compatible with S/4HANA Cloud, Business One, Business ByDesign)
- Subscription lifecycle management
- Cost optimization patterns

**Tutorial Structure:**
1. Core application development (business models, logic)
2. Enhancement to multitenant (multi-customer) solutions
3. ERP backend integration
4. Feature expansion
5. Application extension

**Bill of Materials**: Complete service list at [https://github.com/SAP-samples/partner-reference-application/blob/main/Tutorials/01-BillOfMaterials.md](https://github.com/SAP-samples/partner-reference-application/blob/main/Tutorials/01-BillOfMaterials.md)

### Partner Reference Application Extension

**Type**: Customer-specific extension example

**GitHub**: [https://github.com/SAP-samples/partner-reference-application-extension](https://github.com/SAP-samples/partner-reference-application-extension)

**Demonstrates:**
- Enhanced catering management capabilities
- Seamless base application integration
- Granular tenant-specific configurations
- Consistent UX across extended and core features
- Secure multitenant architecture with data isolation

## ABAP Sample Application

### Music Festival Manager

**Type**: Reference application for multitenant ABAP SaaS

**GitHub**: [https://github.com/SAP-samples/abap-platform-partner-reference-application](https://github.com/SAP-samples/abap-platform-partner-reference-application)

**Demonstrates:**
- Full-stack ABAP Cloud development using RAP
- Scalable, multitenant architecture
- SAP BTP Developer's Guide best practices
- ERP-agnostic design (side-by-side extensions)
- Compatibility with any SAP solution including S/4HANA Cloud ERP

**Tutorial Structure:**
1. **Core Application Development**: Business models, logic, UI, authentication, role-based authorization
2. **Deployment & Provisioning**: Building and deploying to consumers
3. **SAP S/4HANA Cloud Integration**: Connecting with enterprise systems
4. **Feature Enhancement**: Expanding application capabilities

**Key Features:**
- Uses ABAP RESTful Application Programming Model (RAP)
- Leverages SAP BTP services for enterprise-class standards
- Enables focus on business logic and domain functionality

## Cost Estimation

### Total Cost of Ownership Calculator

**Location**: SAP Partner Portal

**Inputs:**
- Expected tenant count
- Resource requirements
- Support level
- Region

**Outputs:**
- Monthly operational costs
- Per-tenant estimates
- Scaling projections

## Development Workflow

### SaaS Development Flow

```
1. Setup
   ├── Create global account
   ├── Configure Landscape Portal
   └── Setup development system

2. Develop
   ├── Build software components
   ├── Implement business logic
   ├── Create Fiori apps
   └── Configure multitenancy

3. Test
   ├── Unit testing (ABAP Unit)
   ├── Integration testing
   ├── Tenant isolation testing
   └── Performance testing

4. Deploy
   ├── Build product
   ├── Register in Landscape Portal
   └── Publish to SAP Store (optional)

5. Operate
   ├── Monitor via SAP Cloud ALM
   ├── Manage subscriptions
   └── Handle support requests
```

### Add-on Development Flow

```
1. Develop
   ├── Create software components
   ├── Use registered namespace
   └── Follow ABAP Cloud guidelines

2. Build
   ├── Assemble product via Landscape Portal
   ├── Run quality checks
   └── Create release

3. Distribute
   ├── Register in SAP Store
   ├── Define pricing
   └── Enable discovery

4. Support
   ├── Customer installation support
   ├── Update delivery
   └── Issue resolution
```

## Key User Extensibility (SaaS)

**Available to customers:**
- UI adaptations
- Custom fields
- Custom logic (BAdIs)
- Business configuration

**Not available:**
- Database schema changes
- Core code modifications
- Direct system access

## Tenant Management

### Subscription Lifecycle

```
Customer Subscription Request
         ↓
Tenant Provisioning (automatic)
         ↓
Tenant Configuration
         ↓
User Access Setup
         ↓
Operational Phase
         ↓
[Optional] Tenant Offboarding
```

### Isolation Guarantees

| Aspect | Isolation Level |
|--------|-----------------|
| Data | Complete (separate schemas) |
| Configuration | Per-tenant |
| Customizations | Per-tenant |
| Resources | Shared compute, isolated data |

## Best Practices

### Architecture

1. **Design for multitenancy** from the start
2. **Implement proper tenant isolation**
3. **Use SAP-recommended patterns**
4. **Plan for scale** (up to 1000 tenants per HANA instance)

### Development

1. **Follow ABAP Cloud guidelines**
2. **Use ATC for quality checks**
3. **Implement comprehensive testing**
4. **Document APIs and extensions**

### Operations

1. **Monitor with SAP Cloud ALM**
2. **Automate deployments**
3. **Plan upgrade windows**
4. **Establish support processes**

### Pricing

1. **Calculate TCO accurately**
2. **Consider scaling costs**
3. **Plan for support overhead**
4. **Offer flexible pricing tiers**

## Resources

| Resource | Location |
|----------|----------|
| Partner Portal | partner.sap.com |
| Discovery Center | discovery-center.cloud.sap |
| PartnerEdge Build | SAP PartnerEdge program |
| Reference Applications | github.com/SAP-samples |

## Source Documentation

- ISV ABAP Guide: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/build-and-run-abap-applications-for-partners-who-are-independent-software-vendors-210db8e.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/build-and-run-abap-applications-for-partners-who-are-independent-software-vendors-210db8e.md)
- ISV SaaS Guide: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/build-and-run-multitenant-saas-applications-for-partners-who-are-independent-software-ven-9b5e06f.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/build-and-run-multitenant-saas-applications-for-partners-who-are-independent-software-ven-9b5e06f.md)
