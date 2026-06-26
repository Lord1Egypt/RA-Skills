# SAP BTP Security and Authentication - Detailed Reference

**Source**: [https://github.com/SAP-docs/btp-best-practices-guide/tree/main/docs/set-up-and-plan](https://github.com/SAP-docs/btp-best-practices-guide/tree/main/docs/set-up-and-plan)

---

## Security Fundamentals

Applications on SAP BTP are exposed to the Internet and must fulfill the highest security requirements to prevent unauthorized access.

### Network Security

The SAP BTP landscape runs in an isolated network protected by:
- Firewalls
- DMZ (Demilitarized Zone)
- Communication proxies for all inbound/outbound traffic
- Transport Layer Security (TLS) encryption for all user connections

---

## User Types

### Platform Users

Developers, administrators, and operators who:
- Deploy applications
- Administer accounts and environments
- Troubleshoot platform issues

**Permissions managed through**: Membership assignments at global account, directory, subaccount, and environment levels.

### Business Users

End users of deployed applications and SaaS services who require:
- Authentication configuration
- Authorization controls
- Role assignments

---

## Identity Provider Architecture

### Recommended Setup

**Always use SAP Cloud Identity Services - Identity Authentication for SAP BTP.**

```
┌─────────────────┐      ┌──────────────────────┐      ┌─────────────┐
│ Corporate IdP   │ ──── │ Identity             │ ──── │ SAP BTP     │
│ (ADFS, Okta,   │      │ Authentication       │      │             │
│  Azure AD)      │      │ (Proxy Mode)         │      │             │
└─────────────────┘      └──────────────────────┘      └─────────────┘
```

**Benefits of Proxy Mode**:
- Single integration point for multiple corporate IdPs
- Centralized security policies
- Required for certain user types and applications
- Consistent authentication experience

### Default Identity Providers

| Provider | Purpose |
|----------|---------|
| **SAP ID Service** | Preconfigured for starter scenarios and testing |
| **SAP Universal ID** | Manages official SAP community users |

### Trust Configuration Levels

| User Type | Configuration Level |
|-----------|---------------------|
| Platform Users | Global account level (applies across directories, subaccounts, environments) |
| Business Users | Individual subaccount level |

**Critical**: Maintain backup administrators in default provider OR alternative custom provider for recovery scenarios.

---

## SAP Cloud Identity Services Onboarding

### Why Onboard?

The default identity provider doesn't support:
- Custom security policies
- Multifactor authentication
- SCIM APIs for user provisioning

### Tenant Options

Organizations receive both productive and test tenants:

**Option 1**: Test tenant for dev/test, productive for all
**Option 2**: Test tenant for dev/test only, productive for production

### Onboarding Procedure

**Step 1: Administrator Setup**
- Add multiple administrators (coverage across time zones)
- Ensure backup during absences

**Step 2: Security Hardening**
- Implement MFA for administrator accounts
- "Administrators have critical access to the system. Set a higher security standard."

**Step 3: Monitoring Configuration**
- Establish system notifications
- Configure security alerts

**Step 4: Corporate Integration**
- Configure Identity Authentication as proxy
- Connect to corporate identity provider(s)

---

## Authorization Methods

### Comparison Table

| Aspect | Provisioning | Federation |
|--------|-------------|------------|
| **Mechanism** | Synchronizes users/groups between systems | Maps authorizations to user attributes in tokens |
| **Tools** | Identity Provisioning, Cloud Identity Access Governance | btp CLI, SAP BTP cockpit |
| **Advantages** | Centrally defined roles, approval workflows, automated offboarding | Simpler implementation, real-time authorization |
| **Disadvantages** | Users wait for provisioning jobs | Doesn't scale, manual role grouping, orphaned data |
| **Restrictions** | Partial for platform users (subaccount level only) | ABAP environment doesn't support |

### Recommendations

- **Production with many users**: Use provisioning or federation
- **Feasible scenarios**: Prefer provisioning
- **Simple setups**: Federation acceptable
- **Testing only**: Manual assignment okay

---

## Identity Lifecycle Management

### Central Identity Management

The persistency layer of SAP Cloud Identity Services is the **Identity Directory**.

**Process**:
1. Corporate identity system → Identity Provisioning → SAP Cloud Identity Services
2. Identity Directory stores user data
3. Identity Provisioning synchronizes to SAP BTP applications

### Global User ID

Use universally unique identifiers rather than changeable attributes:

**Avoid**: Email addresses (can change)
**Use**: Generated UUID or corporate employee ID

### Authentication Requirements

| Environment | Requirements |
|-------------|--------------|
| ABAP | Unique email address required |
| Kyma | Unique email address required |
| Cloud Foundry | Email + IdP information |

### Implementation Options

1. **Manual**: Create users via BTP cockpit, CLI, or APIs
2. **Automatic**: Create after successful IdP authentication
3. **Centralized**: Manage through SAP Cloud Identity Services

---

## Platform User Access Rights

### Team-Based Access Distribution

| Team | Development | Test | Production |
|------|-------------|------|------------|
| Cloud Development Team | Full access | No access | No access |
| Platform Engineering Team | No access | Full access | Full access |

### Environment-Specific Roles

#### Cloud Foundry

| Role | Capability | Recommended For |
|------|------------|-----------------|
| Space Developer | Deploy apps, access service credentials, sensitive data | Dev team (dev only), Platform Engineering (test/prod) |
| Org Manager | Manage org settings | Platform Engineering |
| Space Manager | Manage space settings | Platform Engineering |

**Security Note**: Space Developer provides broad access; restrict in production.

#### ABAP Environment

Requires both:
- CF roles: Org Manager, Space Manager, Space Developer
- ABAP business roles: SAP_BR_ADMINISTRATOR, SAP_BR_DEVELOPER

#### Kyma

Uses Kubernetes RBAC:
- Start with simple role concept separating developers and operators
- Refine as needed
- See Kyma RBAC reference for details

#### Neo

- Administrators assign predefined platform roles
- Custom roles can be configured

### Sensitive Production Access

For scenarios where even Platform Engineering cannot access data:

1. **Automate tasks** requiring developer access
2. **Integrate into CI/CD pipelines** using technical users
3. **Temporary role assignment** for firefighter situations
4. **Special user accounts** with controlled credential distribution
5. **Maintain audit trails** of all access usage

---

## Destination Authentication Methods

### Complete Method Reference

| Method | Description | CF | Neo | Internet | On-Premise |
|--------|-------------|----|----|----------|------------|
| **NoAuthentication** | No authentication required | Yes | Yes | Yes | Yes |
| **BasicAuthentication** | Username/password (testing only) | Yes | Yes | Yes | Yes |
| **ClientCertificateAuthentication** | Mutual TLS with technical user | Yes | Yes | Yes | No |
| **PrincipalPropagation** | Forward user identity via Cloud Connector | Yes | Yes | No | Yes |
| **OAuth2SAMLBearerAssertion** | SAML to OAuth for third-party | Yes | Yes | Yes | Yes |
| **OAuth2ClientCredentials** | Client credentials grant (cached) | Yes | Yes | Yes | Yes |
| **OAuth2UserTokenExchange** | Token exchange in same tenant | Yes | No | Yes | Yes |
| **OAuth2Password** | Password grant (testing only) | Yes | No | Yes | Yes |
| **OAuth2JWTBearer** | JWT bearer for user context | Yes | No | Yes | Yes |
| **SAMLAssertion** | Generated SAML assertion | Yes | No | Yes | Yes |
| **AppToAppSSO** | Application-to-application SSO | No | Yes | Yes | No |

### Recommendations

**For SAP Systems**: `PrincipalPropagation`
**For Third-Party**: `OAuth2SAMLBearerAssertion`
**For Token Exchange**: `OAuth2JWTBearer` (preferred over OAuth2UserTokenExchange)

**Avoid in Production**: `BasicAuthentication`, `OAuth2Password`

---

## Identity Propagation

### Cloud Foundry Environment

**Decision Tree**:
1. SAP system on-premise? → Use `PrincipalPropagation`
2. Third-party system? → Use `OAuth2SAMLBearerAssertion`
3. Same tenant token exchange? → Use `OAuth2JWTBearer`

### Neo Environment

Follow similar principles:
- `PrincipalPropagation` for SAP systems
- `OAuth2SAMLBearerAssertion` for third-party

---

## Kyma RBAC Details

### Recommended Setup Goals

1. Separate operators from development teams
2. Isolate day-to-day accounts from administrative accounts
3. Use dedicated namespaces per service, project, or team
4. Leverage `common-resource-viewer` ClusterRole for read access

### Kubernetes Impersonation Strategy

Rather than granting powerful roles directly, use Kubernetes User Impersonation:
- Subjects (users, groups, service accounts) assume temporary identities
- "Virtual users" (vUsers) needn't exist in the system
- Provides just-in-time privilege escalation

### Role Configurations

**Operators (All Environments)**:
- Default: View-only access
- Administrative tasks: Impersonate `cluster-admin` virtual user

**Developers (Dev/Test Clusters)**:
- Full namespace access via `admin` ClusterRole binding

**Developers (Production Clusters)**:
- Read-only namespace access via `cluster-viewer` ClusterRole
- Administrative tasks: Impersonate application-specific virtual users

### Sample Manifest: Operator Impersonation

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-admin-impersonator
rules:
- apiGroups: [""]
  resources: ["users"]
  verbs: ["impersonate"]
  resourceNames: ["cluster-admin"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: operators-can-impersonate-admin
subjects:
- kind: Group
  name: operators
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-admin-impersonator
  apiGroup: rbac.authorization.k8s.io
```

---

## Connectivity and Remote Systems

### Destination Benefits

Using destinations provides:
- Separation of application code from configuration
- Easier updates without code changes
- Secure credential and certificate storage
- Runtime resolution of connection details

### Destination Creation Levels

| Level | Use Case |
|-------|----------|
| Subaccount | Organization-wide availability |
| Service Instance | Specific scenario use |

**Security**: Limit access authorizations to minimum necessary.

### Cloud Connector

Lightweight on-premise agent establishing secure tunnel:

**Capabilities**:
- No inbound firewall ports required
- Fine-grained access control per exposed system
- RFC and HTTP protocol support
- Principal propagation for user identity forwarding
- Configuration via SAP BTP cockpit

**Note**: Each subaccount requires separate Cloud Connector integration setup.

---

## mTLS Certificate Extraction

### Steps to Extract X.509 Certificates

1. **Locate Service Key**: Navigate to service instance in BTP cockpit
2. **Find Attributes**: Look for `certificate` and `key` attributes (verify `credential-type: x509`)
3. **Extract Values**: Copy to separate text files (avoid `\n` characters)
4. **Save as PEM**:
   - `my-private-key.pem`
   - `my-certificate.pem`
5. **Combine**: Create `my-keypair.pem` with private key first, then certificate

### PEM File Structure

```
-----BEGIN RSA PRIVATE KEY-----
[Base64 encoded private key]
-----END RSA PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
[Base64 encoded certificate]
-----END CERTIFICATE-----
```

**Note**: Converting to `.cer`, `.jks`, `.p12` requires third-party tools.

---

## Data Protection and Privacy

### Key Principles

- Compliance should be integrated early in development, not as an afterthought
- Simply using SAP BTP doesn't make applications compliant
- SAP provides security features; you must implement them properly
- Consult legal experts for specific requirements

**Important Disclaimer**: "SAP does not provide legal advice in any form." Compliance requires case-by-case decisions based on your specific system landscape and applicable laws.

### Important Considerations

- Compliance involves multiple systems and products
- User deletion requests may require coordinated removal across platforms
- Tailor decisions to your system environment and legal framework
- SAP Discovery Center provides EU Access service information

### SAP's Role vs Your Responsibility

| SAP Provides | You Must |
|--------------|----------|
| Security features | Implement them properly |
| Data protection-relevant functions | Configure for your requirements |
| Identity lifecycle management | Coordinate across all integrated systems |
| Documentation and guidance | Consult legal experts for your jurisdiction |

---

**Source Documentation**:
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/security-concepts-951d36c.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/security-concepts-951d36c.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/setting-up-authentication-1dbce9c.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/setting-up-authentication-1dbce9c.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/setting-up-authorization-cb9f0ac.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/setting-up-authorization-cb9f0ac.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/setting-up-identity-lifecycle-2c30208.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/setting-up-identity-lifecycle-2c30208.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/role-based-access-control-rbac-in-kyma-bb31080.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/role-based-access-control-rbac-in-kyma-bb31080.md)
- [https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/destination-authentication-methods-765423d.md](https://github.com/SAP-docs/btp-best-practices-guide/blob/main/docs/set-up-and-plan/destination-authentication-methods-765423d.md)
