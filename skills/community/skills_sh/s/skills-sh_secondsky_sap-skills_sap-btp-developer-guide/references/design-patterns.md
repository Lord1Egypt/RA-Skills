# SAP BTP Design Patterns Reference

## Overview

Design patterns provide guidance for creating superior user experiences, implementing secure architectures, and building well-modularized applications on SAP BTP.

## User Experience Design

### Core Principle

Superior UX drives business value through:
- Improved productivity
- Better data quality
- Higher user adoption

### Common Challenges

| Challenge | Impact |
|-----------|--------|
| Information discovery | Users can't find data |
| Data fragmentation | Multiple systems to check |
| Excessive navigation | Wasted time |
| Poor error handling | User frustration |

### Design Thinking

**Approach**: Understand user needs through observation and feedback

**Process:**
1. Empathize - Understand users
2. Define - Clarify problems
3. Ideate - Generate solutions
4. Prototype - Build quickly
5. Test - Validate with users

**Motto**: "Fail fast, fail early"

## Development Use Case Patterns

### Process Automation

**Type**: Low-code/no-code

**Tool**: SAP Build Process Automation

**Best For**: Business experts creating workflows

### Web and Mobile Applications

**Tool**: SAP Build Apps, MDK

**Best For**: Cross-platform consumer applications

### Full-Stack Development

**Types:**
- Single-tenant applications
- Multitenant SaaS applications
- Tenant-specific extensions

**Reference Apps:**
- Poetry Slam Manager (SaaS)
- Catering Management (Extension)
- Incident Management (Full-stack)

## Technology Design

### Modularization Benefits

| Benefit | Description |
|---------|-------------|
| Maintainability | Easier to understand and modify |
| Testability | Independent unit testing |
| Scalability | Scale individual components |
| Reduced coupling | Changes don't cascade |
| Faster innovation | Independent development |

### Domain-Driven Design (DDD)

**When to Use**: Applications with 30+ use cases, complex domains

**Recommended Approach (SAP BTP/CAP):**
1. **SAP One Domain Model**: Leverage SAP's standardized business data model for consistency across SAP solutions
2. **CAP Domain Modeling**: Use CDS for human-readable, business-aligned domain models
3. **Community Practices**: Apply EventStorming, bounded-context discovery for complex scenarios

**Complexity Scoring Heuristic**:

> **Note**: This scoring is a pragmatic heuristic to help decide when deeper DDD practices (EventStorming, bounded-context discovery) may provide value. Always validate triggers against domain expert input, non-functional requirements (performance, scalability), and team constraints before applying.

| Criterion | Points | Consideration |
|-----------|--------|---------------|
| 30+ use cases | 2 | Scale indicator |
| Anticipated growth | 1 | Future complexity |
| Significant future changes | 2 | Maintainability needs |
| Novel domain | 2 | Unknown complexity |

**Score 7+ points**: Consider deeper DDD practices

**DDD Process** (8 steps from ddd-crew):
1. Align business goals
2. Discover domain
3. Decompose domain
4. Connect bounded contexts
5. Strategize models
6. Define domain events
7. Design bounded contexts
8. Evolve architecture

**Resources:**
- SAP One Domain Model: [https://api.sap.com/sap-one-domain-model](https://api.sap.com/sap-one-domain-model)
- CAP Domain Modeling: [https://cap.cloud.sap/docs/guides/domain-modeling](https://cap.cloud.sap/docs/guides/domain-modeling)
- DDD Starter Modeling: [https://github.com/ddd-crew/ddd-starter-modelling-process](https://github.com/ddd-crew/ddd-starter-modelling-process)

## CAP Design Principles

### Domain-Driven Development

- Collaborate with domain experts
- Use CDS for human-readable models
- Focus on business concepts

### Out-of-the-Box Best Practices

CAP provides automatic:
- OData service generation
- CRUD operations
- Authorization checks
- Audit logging

### Platform Agnostic Design

CAP abstracts:
- Deployment targets (CF, Kyma)
- Authentication methods
- Protocols (REST, OData, GraphQL)
- Database technologies
- Messaging systems

## ABAP Design Principles

### Model-Driven Architecture

**Benefits:**
- Common architecture reduces boilerplate
- Patterns transfer across implementations
- Built-in mock frameworks
- Consistent code quality

### Use Case Patterns

**Customer Applications:**
- Decoupled lifecycles
- Independent workload management
- Hub scenarios

**Partner Solutions:**
- Multitenant SaaS
- Add-on products

**Other:**
- Mobile applications
- Business automation
- Code quality analysis

## Security Design

### Five Guidelines

| Guideline | Focus |
|-----------|-------|
| Secure User Interfaces | SAP Fiori authentication, validation |
| Access Control Models | RBAC/ABAC with OAuth/OpenID Connect |
| API Security | OAuth 2.0, TLS encryption |
| Secure Extensibility | Isolate and validate custom logic |
| Domain Model Validation | Review CDS models for data protection |

### Secure SDLC

**Explore Phase:**
- Implement OWASP standards
- Train development teams
- Conduct risk assessments
- Plan compliance requirements

**Discover Phase:**
- Map data flows
- Establish secure architecture
- Validate third-party services
- Incorporate security in prototypes

**Design Phase:**
- Apply least privilege
- Implement defense in depth
- Validate inputs at boundaries

## Microservices Patterns

### When to Use

**Benefits:**
- Independent scaling
- Technology flexibility
- Team autonomy

**Considerations:**
- Increased complexity
- Network latency
- Distributed transactions

### CAP Approach

Start monolithic, extract services when:
- Different scaling needs
- Different team ownership
- Independent deployment required

### Communication Patterns

| Pattern | Use Case |
|---------|----------|
| Synchronous (REST/OData) | Real-time queries |
| Asynchronous (Events) | Decoupled processes |
| Event Sourcing | Audit requirements |

## Database Design

### CAP with CDS

```cds
// Domain model
entity Orders {
  key ID : UUID;
  customer : Association to Customers;
  items : Composition of many OrderItems on items.order = $self;
  status : Status;
}

entity OrderItems {
  key ID : UUID;
  order : Association to Orders;
  product : Association to Products;
  quantity : Integer;
}
```

### ABAP with CDS

```abap
define root view entity ZI_Order
  as select from zorder
  composition [0..*] of ZI_OrderItem as _Items
{
  key order_uuid as OrderUUID,
      customer_id as CustomerID,
      _Items
}
```

## API Design

### API-First Approach

1. Design API before implementation
2. Use OpenAPI/OData specifications
3. Follow SAP API Style Guide
4. Publish to API Business Hub

### Versioning Strategy

```
/api/v1/orders    # Version 1
/api/v2/orders    # Version 2 (breaking changes)
```

## Testing Patterns

### Test Pyramid

```
        /\
       /  \      E2E Tests (few)
      /----\
     /      \    Integration Tests (some)
    /--------\
   /          \  Unit Tests (many)
  /------------\
```

### CAP Testing

```javascript
const cds = require('@sap/cds');

describe('OrderService', () => {
  let srv;

  beforeAll(async () => {
    srv = await cds.connect.to('OrderService');
  });

  it('creates order', async () => {
    const order = await srv.create('Orders', {
      customerID: '123'
    });
    expect(order.ID).toBeDefined();
  });
});
```

### ABAP Testing

```abap
CLASS ltcl_order DEFINITION FOR TESTING.
  METHODS test_create_order FOR TESTING.
ENDCLASS.

CLASS ltcl_order IMPLEMENTATION.
  METHOD test_create_order.
    " Test implementation
    cl_abap_unit_assert=>assert_not_initial( lv_order_id ).
  ENDMETHOD.
ENDCLASS.
```

## Source Documentation

- Design (CAP): [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/design-6bb7339.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/design-6bb7339.md)
- Design (ABAP): [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/design-314ae3e.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/design-314ae3e.md)
- Technology Design: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/technology-design-a5b8129.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/technology-design-a5b8129.md)
- UX Design: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/user-experience-design-323bd93.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/user-experience-design-323bd93.md)
