# SAP BTP Security Reference

## Overview

Security must be integrated throughout the development lifecycle, from initial design through production operations. SAP BTP provides platform-level security with platform roles, segregation of duties, and audit logging with digital signatures.

## Security by Development Phase

### Explore Phase

| Guideline | Action |
|-----------|--------|
| Secure SDLC Framework | Implement OWASP-aligned development standards |
| Engagement & Training | Clarify stakeholder expectations, train teams |
| Risk Assessment | Identify high-level security risks |
| Threat Modeling | Evaluate industry-specific threats |
| Compliance Planning | Determine applicable regulations (GDPR, HIPAA) |

### Discover Phase

| Guideline | Action |
|-----------|--------|
| Map Data Flows | Document sensitive data movement using OWASP Threat Dragon |
| Establish Secure Architecture | Microservice isolation, least privilege, defense-in-depth |
| Validate Third-Party Services | Review security certifications |
| Security in Prototypes | Include input sanitization, mock authentication |
| Plan Data Protection | Anonymize user research data |
| Understand Boundary Conditions | Assess IAM and audit logging integration |

### Design Phase

| Guideline | Focus |
|-----------|-------|
| Secure User Interfaces | SAP Fiori authentication and validation |
| Access Control Models | RBAC/ABAC using OpenID Connect/OAuth |
| API Security | OAuth and TLS encryption |
| Secure Extensibility | Isolate and validate custom logic |
| Domain Model Validation | Review CDS models for data protection |

### Run and Scale Phase

| Guideline | Focus |
|-----------|-------|
| Continuous Threat Monitoring | SAP BTP observability tools |
| Security Patching | Regular updates to dependencies |
| Secure Auto-Scaling | Tenant isolation in multitenancy |
| Security Audits | Periodic compliance reviews |
| Data Protection | Privacy law compliance |

## Common Runtime Threats

| Threat | Description | CAP Mitigation |
|--------|-------------|----------------|
| SQL Injection | Malicious SQL in inputs | Parameterized queries |
| XSS | Script injection in UI | Input validation |
| CSRF | Unauthorized actions | Built-in CSRF protection |
| Authentication Bypass | Improper session handling | XSUAA integration |

## CAP Security Implementation

### Authentication Setup

```bash
# Add authentication
cds add xsuaa
```

### xs-security.json Configuration
```json
{
  "xsappname": "my-app",
  "tenant-mode": "dedicated",
  "scopes": [
    {
      "name": "$XSAPPNAME.Read",
      "description": "Read access"
    },
    {
      "name": "$XSAPPNAME.Write",
      "description": "Write access"
    },
    {
      "name": "$XSAPPNAME.Admin",
      "description": "Admin access"
    }
  ],
  "role-templates": [
    {
      "name": "Viewer",
      "scope-references": ["$XSAPPNAME.Read"]
    },
    {
      "name": "Editor",
      "scope-references": ["$XSAPPNAME.Read", "$XSAPPNAME.Write"]
    },
    {
      "name": "Administrator",
      "scope-references": ["$XSAPPNAME.Read", "$XSAPPNAME.Write", "$XSAPPNAME.Admin"]
    }
  ]
}
```

### CDS Authorization

```cds
// Role-based access control
service CatalogService @(requires: 'authenticated-user') {

  @(restrict: [
    { grant: 'READ', to: 'Viewer' },
    { grant: ['READ', 'WRITE'], to: 'Editor' },
    { grant: '*', to: 'Administrator' }
  ])
  entity Books as projection on bookshop.Books;

  // Instance-based authorization
  @(restrict: [
    { grant: 'READ', where: 'createdBy = $user' },
    { grant: '*', to: 'Administrator' }
  ])
  entity Orders as projection on bookshop.Orders;
}
```

### Input Validation
```cds
entity Books {
  key ID : UUID;
  title : String(100) @mandatory;
  price : Decimal(10,2) @assert.range: [0, 9999.99];
  isbn : String(13) @assert.format: '^[0-9]{13}$';
}
```

## ABAP Security

### Authorization Objects
```abap
AUTHORITY-CHECK OBJECT 'S_DEVELOP'
  ID 'DEVCLASS' FIELD iv_package
  ID 'OBJTYPE' FIELD 'CLAS'
  ID 'ACTVT' FIELD '02'.

IF sy-subrc <> 0.
  RAISE EXCEPTION TYPE cx_no_authorization.
ENDIF.
```

### RAP Authorization
```abap
define behavior for ZI_Travel alias Travel
authorization master ( instance )
{
  // Authorization check on entity level
}
```

### Behavior Implementation
```abap
METHOD get_instance_authorizations.
  DATA(lv_auth) = abap_false.

  " Check authorization for specific instance
  AUTHORITY-CHECK OBJECT 'ZTRAVEL'
    ID 'TRAVEL_ID' FIELD keys[ 1 ]-TravelID
    ID 'ACTVT' FIELD '02'.

  IF sy-subrc = 0.
    lv_auth = abap_true.
  ENDIF.

  result = VALUE #( FOR key IN keys
    ( %tky = key-%tky
      %update = COND #( WHEN lv_auth = abap_true THEN if_abap_behv=>auth-allowed
                        ELSE if_abap_behv=>auth-unauthorized ) ) ).
ENDMETHOD.
```

## Authentication Services

### SAP Authentication and Trust Management (XSUAA)

**Purpose**: Manage user authorizations

**Features:**
- OAuth 2.0 / OpenID Connect
- SAML 2.0 federation
- User attribute mapping
- Role collections

### Identity Authentication Service (IAS)

**Purpose**: Cloud-based identity management

**Features:**
- Single Sign-On (SSO)
- Multi-factor authentication
- Social login integration
- On-premise IdP integration

### Configuration
```yaml
# mta.yaml
resources:
  - name: my-xsuaa
    type: org.cloudfoundry.managed-service
    parameters:
      service: xsuaa
      service-plan: application
      config:
        xsappname: my-app
        tenant-mode: dedicated

  - name: my-ias
    type: org.cloudfoundry.managed-service
    parameters:
      service: identity
      service-plan: application
```

## Secrets Management

### SAP Credential Store (CAP)

**Use Cases:**
- API keys
- Database credentials
- Third-party service tokens

**Access via REST API:**
```javascript
const { CredentialStore } = require('@sap/credential-store');

const credStore = new CredentialStore();
const password = await credStore.readPassword('namespace', 'key');
```

### ABAP Communication Management

- Integrated credentials store
- Outbound communication configuration
- Certificate management

## Audit Logging

### CAP Audit Log Service
```javascript
const cds = require('@sap/cds');
const audit = cds.connect.to('audit-log');

// Log data access
await audit.log({
  type: 'DATA_READ',
  data_subject: { type: 'Customer', id: customerId },
  attributes: ['name', 'email']
});
```

### ABAP Audit Logging

**Security Audit Log:**
- Automatic for security-relevant events
- Configurable event classes

**Read Access Logging (RAL):**
- Sensitive data access monitoring
- Compliance reporting

## Data Privacy

### SAP Data Privacy Integration

**Capabilities:**
- Cross-application privacy features
- End-to-end compliance support
- Data subject access requests

### Personal Data Handling (CAP)
```cds
entity Customers {
  key ID : UUID;
  @PersonalData.FieldSemantics: 'DataSubjectID'
  customerID : String;
  @PersonalData.IsPotentiallyPersonal
  name : String;
  @PersonalData.IsPotentiallyPersonal
  email : String;
}
```

## Security Best Practices

### Environment Configuration
- Restrict network access
- Use private endpoints where possible
- Enable WAF protection

### Deployment Pipelines
- Code scanning in CI/CD
- Dependency vulnerability checks
- Container image scanning

### Secrets
- Never hardcode credentials
- Rotate secrets regularly
- Use managed services

### Network
- TLS 1.2+ for all connections
- Certificate pinning where appropriate
- IP allowlisting for sensitive services

## Compliance Resources

| Standard | SAP BTP Support |
|----------|-----------------|
| GDPR | Data Privacy Integration, audit logging |
| SOC 2 | SAP compliance certifications |
| ISO 27001 | Platform certifications |
| HIPAA | Healthcare-specific controls |

## Source Documentation

- Security Considerations: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/security-considerations-for-applications-a73f6ff.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/security-considerations-for-applications-a73f6ff.md)
- CAP Security Guide: [https://cap.cloud.sap/docs/guides/security/](https://cap.cloud.sap/docs/guides/security/)
- SAP BTP Security Recommendations: [https://help.sap.com/docs/btp/sap-btp-security-recommendations/sap-btp-security-recommendations](https://help.sap.com/docs/btp/sap-btp-security-recommendations/sap-btp-security-recommendations)
