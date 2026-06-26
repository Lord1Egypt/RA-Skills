# CAP Development Reference

## Overview

SAP Cloud Application Programming Model (CAP) is SAP's recommended framework for building enterprise-grade applications on SAP BTP using Node.js or Java.

## Operational Profiles

CAP provides three operational profiles for different development stages:

### Development Profile

**Database**: SQLite (Node.js) / H2 (Java)

**Features:**
- Rapid prototyping with minimal setup
- Mocked variants of SAP BTP services (authentication, database, messaging, app gateway)
- No BTP subscription required
- Cost-effective testing

**Usage:**
```bash
cds watch  # Automatically uses development profile
```

### Hybrid Profile

**Database**: Cloud services (e.g., SAP HANA Cloud)

**Features:**
- Run application locally
- Bind to real cloud services for integration testing
- Use `cds bind` or local configuration files
- Test with production-like data

**Usage:**
```bash
cds bind --to hana:my-hana-instance
cds watch --profile hybrid
```

### Production Profile

**Database**: SAP HANA Cloud

**Features:**
- Deployed to SAP BTP (Cloud Foundry or Kyma)
- Platform-managed service bindings
- Production configuration for logging and security
- Database migrations via `cds deploy`

**Usage:**
```bash
cds build --production
cf deploy mta_archives/my-app.mtar
```

### Profile Summary

| Profile | Database | Use Case |
|---------|----------|----------|
| Development | SQLite/H2 | Local prototyping, mock services |
| Hybrid | Cloud services | Local app with cloud DB/services |
| Production | SAP HANA Cloud | Full cloud deployment |

## Supported Languages and Runtimes

| Language | Framework | Runtime Options |
|----------|-----------|-----------------|
| Node.js | Express.js | Cloud Foundry, Kyma |
| Java | Spring Boot | Cloud Foundry, Kyma |
| TypeScript | Node.js | Cloud Foundry, Kyma |

## Development Tools

| Tool | Purpose |
|------|---------|
| SAP Business Application Studio | Primary cloud IDE |
| Visual Studio Code | Local development with CDS extension |
| IntelliJ IDEA | Java CAP development |
| CDS CLI | Command-line development |

## Core CDS Commands

```bash
# Initialize new project
cds init my-project

# Add features
cds add hana          # SAP HANA Cloud support
cds add xsuaa         # Authentication
cds add mta           # MTA descriptor
cds add helm          # Helm charts for Kyma
cds add multitenancy  # Multitenant support
cds add approuter     # Application router

# Development
cds watch             # Run with live reload
cds build             # Build for deployment
cds deploy            # Deploy to HANA

# Service inspection
cds compile           # Compile CDS models
cds serve             # Start services
```

## Domain Modeling with CDS

### Entity Definition
```cds
namespace my.bookshop;

entity Books {
  key ID : UUID;
  title  : String(111);
  author : Association to Authors;
  stock  : Integer;
}

entity Authors {
  key ID : UUID;
  name   : String(111);
  books  : Association to many Books on books.author = $self;
}
```

### Service Definition
```cds
using my.bookshop from '../db/schema';

service CatalogService {
  @readonly entity Books as projection on bookshop.Books;
  entity Authors as projection on bookshop.Authors;

  action submitOrder(book: Books:ID, quantity: Integer);
}
```

## CAP Design Principles

### Domain-Driven Design
- Focus on core domain logic
- Align code structure with business concepts
- Collaboration between technical and domain experts

### Agnostic Design
CAP abstracts:
- Deployment approaches
- Authentication strategies
- Protocols (REST, OData, GraphQL)
- Asynchronous channels
- Database technologies

### Out-of-the-Box Integration
- SAP HANA Cloud for persistence
- Authorization management services
- Connectivity tools for external systems

## Platform Integration

### Database Support
| Database | Use Case |
|----------|----------|
| SQLite | Development (Node.js) |
| H2 | Development (Java) |
| PostgreSQL | Production alternative |
| SAP HANA Cloud | Production (recommended) |

### Service Bindings
```yaml
# mta.yaml service binding example
modules:
  - name: my-srv
    type: nodejs
    requires:
      - name: my-hana
      - name: my-xsuaa
      - name: my-destination

resources:
  - name: my-hana
    type: com.sap.xs.hdi-container
  - name: my-xsuaa
    type: org.cloudfoundry.managed-service
    parameters:
      service: xsuaa
      service-plan: application
```

## Microservices Architecture

CAP supports microservice development with:
- Separate lifecycles per service
- Independent runtimes
- Event-based communication

**Considerations:**
- Microservices introduce complexity
- Potential performance trade-offs
- Start monolithic, extract when needed

## API Consumption

### Supported Protocols
- OData V2/V4
- REST
- OpenAPI

### SAP Cloud SDK Integration

**Generate typed client** (recommended approach):
```bash
# Generate OData client from service specification
npx @sap-cloud-sdk/generator --input ./API_BUSINESS_PARTNER.edmx --outputDir ./generated
```

**Use generated client**:
```javascript
// Import from generated client (path depends on generator output)
const { businessPartnerApi } = require('./generated/business-partner-service');

// Fetch business partners from S/4HANA
const businessPartners = await businessPartnerApi
  .requestBuilder()
  .getAll()
  .execute({ destinationName: 'S4HANA' });
```

> **Note**: The `@sap/cloud-sdk-vdm-*` packages are deprecated. Use `@sap-cloud-sdk/generator` to generate typed clients from OData service specifications. See [SAP Cloud SDK documentation](https://sap.github.io/cloud-sdk/docs/js/features/odata/generate-client) for details.

## Multitenancy

### Enable Multitenancy
```bash
cds add multitenancy
```

### Key Features
- Tenant isolation
- Per-tenant database schemas
- Subscription lifecycle hooks
- Resource sharing across tenants

### SaaS Entry Points

| Approach | Description | Consumer Requirements |
|----------|-------------|----------------------|
| Central | SAP Build Work Zone managed | Own Work Zone instance |
| Local | Standalone app router | None |

## Extensibility

### In-App Extensions
```cds
// Extend existing service
extend service CatalogService with {
  entity CustomEntity {
    key ID : UUID;
    customField : String;
  }
}
```

### Custom Handlers
```javascript
// srv/cat-service.js
module.exports = (srv) => {
  srv.before('CREATE', 'Books', async (req) => {
    // Validation logic
    if (!req.data.title) {
      req.error(400, 'Title is required');
    }
  });

  srv.on('submitOrder', async (req) => {
    // Custom action implementation
    const { book, quantity } = req.data;
    // Process order...
  });
};
```

## Security Implementation

### Authentication
```cds
// Require authentication
service CatalogService @(requires: 'authenticated-user') {
  entity Books as projection on bookshop.Books;
}
```

### Authorization
```cds
// Role-based access
service AdminService @(requires: 'admin') {
  entity Books as projection on bookshop.Books;

  @(restrict: [{ grant: 'READ', to: 'viewer' }])
  entity Reports { ... }
}
```

### Built-in Security Features
- Parameterized queries (SQL injection prevention)
- CSRF protection for UI applications
- CDS constraints for input validation

## Testing

### Unit Testing with Jest
```javascript
const cds = require('@sap/cds');

describe('CatalogService', () => {
  let srv;

  beforeAll(async () => {
    srv = await cds.connect.to('CatalogService');
  });

  it('should return books', async () => {
    const books = await srv.read('Books');
    expect(books).toBeDefined();
  });
});
```

### Integration Testing
```bash
# Run tests
npm test

# With coverage
npm test -- --coverage
```

## Deployment Commands

### Cloud Foundry
```bash
# Build MTA
mbt build

# Deploy
cf deploy mta_archives/my-project_1.0.0.mtar

# Or with cf push for simple apps
cf push
```

### Kyma
```bash
# Add Helm support
cds add helm

# Deploy with Helm
helm upgrade --install my-app ./chart
```

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `HANA deployment fails` | Wrong HDI container | Verify `requires` in mta.yaml |
| `Authentication errors` | XSUAA not bound | Run `cf bind-service` |
| `Database connection refused` | Wrong profile | Set `NODE_ENV=production` |
| `Model compilation errors` | CDS syntax | Run `cds compile --to json` for details |

## Source Documentation

- CAP Documentation: [https://cap.cloud.sap/docs/](https://cap.cloud.sap/docs/)
- SAP BTP CF/Kyma with CAP: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/sap-btp-cloud-foundry-and-sap-btp-kyma-runtimes-with-cap-0f9cfe9.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/sap-btp-cloud-foundry-and-sap-btp-kyma-runtimes-with-cap-0f9cfe9.md)
- Development Guide: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/develop-7e30686.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/develop-7e30686.md)
