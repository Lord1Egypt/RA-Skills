# SAP BTP Account Models - Detailed Reference

**Source**: [https://github.com/SAP-docs/btp-best-practices-guide/tree/main/docs/set-up-and-plan](https://github.com/SAP-docs/btp-best-practices-guide/tree/main/docs/set-up-and-plan)

---

## Account Hierarchy Deep Dive

### Global Accounts

Global accounts are region and runtime-independent entities representing contracts with SAP:
- Administrators manage subaccounts, members, entitlements, and quotas
- Typically one global account per commercial model
- Separate billing per global account
- Multiple global accounts may be needed for legal or commercial separation

**Commercial Contract Options**:
- **Consumption-Based**: BTPEA, CPEA, Pay-As-You-Go (cannot mix flavors)
- **Subscription-Based**: Fixed-cost for 1-3 year periods

### Directories

Directories group subaccounts for organized management and can nest up to 5 levels deep.

**Directory Use Cases**:
1. **Administrative Organization**: By subsidiary, department, or line of business
2. **Billing and Accounting**: Align with financial structure
3. **Geographical Grouping**: Regulatory compliance and performance optimization
4. **Business Scenario Alignment**: Group by project or initiative
5. **Resource Control**: Usage limitations and quota management
6. **Technical Organization**: Based on infrastructure constraints

### Subaccounts

Subaccounts are individual operational units where applications run and services are consumed:
- Deployed in exactly one region
- Can enable multiple runtime environments
- Support dedicated identity provider configuration
- Independent quota and user management

### Labels

Labels are user-defined tags for organizing directories, subaccounts, instances, and subscriptions:
- Landscape designations: Dev, Test, Prod
- Departments: HR, IT, Finance, Sales
- Cost center codes
- Custom tags: "Flagged for deletion", "Important"

**Best Practice**: Use directories as primary structure, labels for virtual grouping and reporting.

---

## Account Model Templates

### Template 1: Directories Per Functional Area

```
Global Account
├── Directory: HR
│   ├── Subaccount: hr-development
│   │   └── Identity Provider: Corporate IdP
│   ├── Subaccount: hr-test
│   │   └── Identity Provider: Corporate IdP
│   └── Subaccount: hr-production
│       └── Identity Provider: Corporate IdP (hardened)
├── Directory: Sales
│   ├── Subaccount: sales-development
│   ├── Subaccount: sales-test
│   └── Subaccount: sales-production
└── Directory: IT Services
    ├── Subaccount: shared-services-dev
    ├── Subaccount: shared-services-test
    └── Subaccount: shared-services-prod
```

**Benefits**:
- Clear functional separation
- Independent entitlement management per directory
- Easy cost allocation by department

### Template 2: Directories Per Location

```
Global Account
├── Directory: Europe
│   ├── Labels: Region=EU, Compliance=GDPR
│   ├── Subaccount: eu-development (Frankfurt)
│   ├── Subaccount: eu-test (Frankfurt)
│   └── Subaccount: eu-production (Frankfurt)
├── Directory: North America
│   ├── Labels: Region=NA
│   ├── Subaccount: na-development (Virginia)
│   ├── Subaccount: na-test (Virginia)
│   └── Subaccount: na-production (Virginia)
└── Directory: APAC
    ├── Labels: Region=APAC
    ├── Subaccount: apac-development (Singapore)
    ├── Subaccount: apac-test (Singapore)
    └── Subaccount: apac-production (Singapore)
```

**Benefits**:
- Regulatory compliance (data residency)
- Performance optimization (proximity to users)
- Regional legal requirements

### Template 3: Directories Per Subsidiary

```
Global Account
├── Directory: ACME Corp
│   ├── Labels: CostCenter=CC001, Owner=John
│   └── Subaccounts: acme-dev, acme-test, acme-prod
├── Directory: ACME Manufacturing
│   ├── Labels: CostCenter=CC002, Owner=Jane
│   └── Subaccounts: acme-mfg-dev, acme-mfg-test, acme-mfg-prod
└── Directory: ACME Services
    ├── Labels: CostCenter=CC003, Owner=Bob
    └── Subaccounts: acme-svc-dev, acme-svc-test, acme-svc-prod
```

**Benefits**:
- Clear subsidiary boundaries
- Cost allocation to legal entities
- Independent ownership and management

---

## Simple Subaccount Model (Without Directories)

For initial implementations or smaller organizations:

```
Global Account
├── Subaccount: Development
│   ├── Labels: Stage=Dev, CostCenter=IT
│   └── Identity Provider: Corporate IdP
├── Subaccount: Test
│   ├── Labels: Stage=Test, CostCenter=IT
│   └── Identity Provider: Corporate IdP
└── Subaccount: Production
    ├── Labels: Stage=Prod, CostCenter=IT
    └── Identity Provider: Corporate IdP (hardened)
```

**When to Use**:
- Less than 3 projects
- Single team
- Initial BTP adoption

**Upgrade Path**: Transition to directory model when exceeding 3 subaccounts.

---

## Specialized Subaccount Patterns

### Separate API Management Subaccounts

```
Global Account
├── Directory: Central IT Tools
│   ├── Subaccount: api-management-dev
│   ├── Subaccount: api-management-test
│   └── Subaccount: api-management-prod
├── Directory: Shared Data
│   ├── Subaccount: hana-dev-test (shared HANA Cloud)
│   └── Subaccount: hana-production
└── Directory: Projects
    ├── Subaccount: project-a-dev
    ├── Subaccount: project-a-test
    ├── Subaccount: project-a-prod
    └── ... (consume APIs via destinations)
```

**Benefits**:
- Centralized API governance
- Shared database costs
- Rapid scaling with API-based connections

### Large Project Separation

```
Global Account
├── Subaccount: development (standard)
├── Subaccount: test (standard)
├── Subaccount: production (standard)
└── Subaccount: project-x-all-stages
    └── (Completely separated support and operations model)
```

**Use When**:
- Project requires isolated operations
- Different SLA requirements
- Separate support processes

---

## Cloud Foundry Staging Details

### Subaccount-Org Relationship

When Cloud Foundry is enabled, the system automatically creates a corresponding CF org with a 1:1 relationship:

```
Subaccount: hr-development
    └── CF Org: acme-hr-development (auto-created)
        ├── Space: recruiting
        ├── Space: payroll
        └── Space: benefits
```

### Configuration Capabilities Comparison

| Feature | Subaccount Level | Space Level |
|---------|------------------|-------------|
| Business user groups | Yes | No |
| Cloud Connector tunnels | Yes | No |
| Roles and trust settings | Yes | No |
| Quota assignment | Yes (mandatory) | Yes (optional) |

### Data Segregation

Data access is controlled at subaccount level, not application or space level:
- Services consume messages from ALL applications within a subaccount
- Use separate subaccounts to restrict cross-application visibility
- Spaces are for organization when dedicated user management isn't required

---

## Kyma Staging Details

### Subaccount-Cluster Relationship

Each subaccount provisions exactly one Kubernetes cluster:

```
Subaccount: platform-dev-test
    └── Kyma Cluster (auto-provisioned)
        ├── Namespace: hr-dev
        ├── Namespace: hr-test
        ├── Namespace: sales-dev
        └── Namespace: sales-test

Subaccount: platform-production
    └── Kyma Cluster
        ├── Namespace: hr
        └── Namespace: sales
```

### Subaccounts vs Namespaces Decision Framework

**Use Separate Subaccounts When**:
- Data access isolation required
- Different network connectivity needs
- Dedicated user management necessary
- Separate billing/cost tracking required
- Ingress traffic isolation needed

**Use Namespaces When**:
- Structuring within cluster sufficient
- Trust exists between teams
- Cost efficiency priority
- Development/testing environments

### Configuration Comparison

| Function | Subaccount | Namespace |
|----------|-----------|-----------|
| User group configuration | Yes | Yes |
| Cloud Connector tunnel | Yes | No |
| Roles/trust setup | Yes | Yes |
| Resource quotas | Yes (mandatory) | Limited |
| Cost monitoring | Yes | No |

---

## Account Model Setup Checklist

### Prerequisites

- [ ] Review SAP Cloud Identity Services onboarding guide
- [ ] Assess organizational needs for account model selection
- [ ] Test hierarchy with pilot project managers
- [ ] Familiarize teams with administration tools

### Ownership Structure

| Level | Owner |
|-------|-------|
| Global Account | Platform Engineering Team/CoE |
| Directories | Designated owners with role collections |
| Subaccounts | Designated owners with role collections |
| Spaces/Namespaces | Development units |

### Directory Template Requirements

When creating new directories, document:
- Name (following naming guidelines)
- Minimum two owners
- Description of developer audience and applications
- Cost center allocation
- Enrollment procedures

### Rules to Define

1. Directory creation criteria
2. Naming conventions (see naming guide)
3. Labels and values for reporting
4. Quota limitations per directory/subaccount
5. Entitlement distribution rules

---

## Naming Convention Details

### Character Restrictions

- Use lowercase letters and hyphens
- Avoid spaces and underscores (except subaccounts)
- Maximum 63 characters for URL-related entities:
  - Subdomains
  - CF orgs and spaces
  - Kyma clusters and namespaces

### Company Identification

| Entity | Include Company Name? |
|--------|----------------------|
| Subaccount name | No |
| Subdomain | Yes |
| CF Org | Yes |
| Directory | Depends on use case |

### Cloud Foundry Naming Example

| Entity | Dev | Test | Prod |
|--------|-----|------|------|
| Subaccount | HR Development | HR Test | HR Production |
| Subdomain | `acme-hr-dev` | `acme-hr-test` | `acme-hr-prod` |
| CF Org | `acme-hr-dev` | `acme-hr-test` | `acme-hr-prod` |
| Space | `recruiting` | `recruiting` | `recruiting` |

### Kyma Naming Example

| Entity | Dev/Test | Prod |
|--------|----------|------|
| Subaccount | Platform Dev Test | Platform Production |
| Subdomain | `acme-platform-devtest` | `acme-platform-prod` |
| Cluster | `acme-platform-devtest` | `acme-platform-prod` |
| Namespace | `hr-dev`, `hr-test` | `hr` |

---

## SaaS Application Considerations

A SaaS application can only be used once within a subaccount. This necessitates:
- Separate subaccounts per functional area using same SaaS
- Or using CF spaces with HTML5 repository for central Fiori Launchpad

---

**Source Documentation**:
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/setting-up-your-account-model-2db81f4.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/setting-up-your-account-model-2db81f4.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/account-model-with-directories-and-subaccounts-b5a6b58.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/account-model-with-directories-and-subaccounts-b5a6b58.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/account-model-with-subaccounts-049d331.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/account-model-with-subaccounts-049d331.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/naming-conventions-for-sap-btp-accounts-5302ea4.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/naming-conventions-for-sap-btp-accounts-5302ea4.md)
