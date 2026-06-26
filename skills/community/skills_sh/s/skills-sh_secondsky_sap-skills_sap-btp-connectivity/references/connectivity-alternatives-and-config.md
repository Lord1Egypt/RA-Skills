# Connectivity Alternatives and Configuration Reference

Alternative connectivity approaches, user roles, target system configuration, and getting started guide.

**Source**: [https://github.com/SAP-docs/btp-connectivity/tree/main/docs/1-connectivity-documentation](https://github.com/SAP-docs/btp-connectivity/tree/main/docs/1-connectivity-documentation)

---

## Getting Started

### Core Components Overview

| Component | Purpose |
|-----------|---------|
| **Destination Service** | Stores connection config, automates OAuth2 tokens |
| **Connectivity Service** | Secure tunnel access via Cloud Connector |
| **Cloud Connector** | Secure link between cloud and on-premise |
| **Connectivity Proxy** | Kubernetes access to on-premise systems |
| **Transparent Proxy** | Automated destination retrieval for Kubernetes |

### Quick Start Path

1. **Store Configuration**: Use Destination Service for credentials, certificates, URLs
2. **Choose Architecture**:
   - Cloud Foundry → Cloud Connector + Connectivity Service
   - Kubernetes → Connectivity Proxy or Transparent Proxy
3. **Enhance**: Deploy Transparent Proxy for automated destination handling

---

## Connectivity Alternatives

### Reverse Proxy vs Cloud Connector

Organizations may choose between Cloud Connector and a reverse proxy/ADC for on-premise connectivity.

#### Reverse Proxy Approach

**Configuration**:
```
ProxyType: Internet
```

**Advantages**:
- Reuses existing reverse proxy/ADC infrastructure
- Cloud-agnostic (works with any cloud)
- Centralized entry point to corporate network

**Disadvantages**:
- Services exposed to Internet (DoS vulnerability)
- IP filtering allows only one BTP outbound address
- Cannot restrict to customer-specific apps
- RFC requires WebSocket (S/4HANA 1909+ only)
- No straightforward principal propagation
- Requires intensive IT involvement

#### Cloud Connector Approach

**Configuration**:
```
ProxyType: OnPremise
```

**Advantages**:
- TLS tunnel with reverse invocation
- No DMZ/firewall changes needed
- Prevents Internet-based attacks
- Simplified setup
- Granular access controls
- Supports HTTP, RFC, LDAP, TCP
- Principal propagation built-in

#### Decision Matrix

| Requirement | Reverse Proxy | Cloud Connector |
|-------------|---------------|-----------------|
| Reuse existing infra | ✅ | ❌ |
| RFC to old ABAP | ❌ | ✅ |
| Principal propagation | ❌ | ✅ |
| Minimal IT involvement | ❌ | ✅ |
| DoS protection | ❌ | ✅ |
| Quick implementation | ❌ | ✅ |

---

## User Roles

### Cloud Connector Roles

| Role | Permissions |
|------|-------------|
| **Administrator** | Full configuration, subaccount management |
| **Subaccount Administrator** | Connect Cloud Connector to subaccounts |
| **Cloud Connector Auditor** | Read-only access (included in Subaccount Viewer) |
| **Display** | View configurations |
| **Support** | Monitoring and logs |

### BTP Role Collections

| Role Collection | Includes |
|-----------------|----------|
| **Subaccount Administrator** | Cloud Connector Administrator |
| **Cloud Connector Administrator** | Dedicated CC role |
| **Connectivity and Destination Administrator** | CC Admin + Destination Admin |
| **Subaccount Viewer** | Cloud Connector Auditor |

### Permission Requirements

**View Connected Cloud Connectors**:
- Requires `readSCCTunnels` permission
- Cloud Connector Administrator role satisfies this

**Configure Access Control**:
- Requires Administrator role in Cloud Connector UI
- Not configurable via BTP Cockpit

---

## Target System Configuration (RFC)

### Connection Types

#### 1. Direct Connection

**Use When**: Single application server target

**Proxy Type**: `OnPremise` (Load Balancing: unchecked)

| Property | Description | Example |
|----------|-------------|---------|
| `jco.client.ashost` | Application server host | `sap-erp.virtual` |
| `jco.client.sysnr` | 2-digit system number | `00` |
| `jco.client.client` | 3-digit client number | `100` |

**Cloud Connector**: Virtual port must be `sapgw<##>` (e.g., `sapgw00`)

#### 2. Load Balancing Connection

**Use When**: Multiple app servers with message server

**Proxy Type**: `OnPremise` (Load Balancing: checked)

| Property | Description | Example |
|----------|-------------|---------|
| `jco.client.mshost` | Message server host | `sap-ms.virtual` |
| `jco.client.group` | Logon group (default: PUBLIC) | `SPACE` |
| `jco.client.r3name` | 3-char system ID | `ERP` |
| `jco.client.msserv` | Message server port (alt to r3name) | `3601` |
| `jco.client.client` | 3-digit client number | `100` |

**Cloud Connector**: Virtual port must be `sapms<###>` (e.g., `sapmsERP`)

#### 3. WebSocket Connection (Internet)

**Use When**: Direct Internet access to ABAP (S/4HANA 1909+)

**Proxy Type**: `Internet`

| Property | Description | Example |
|----------|-------------|---------|
| `jco.client.wshost` | WebSocket RFC server | `s4hana.example.com` |
| `jco.client.wsport` | WebSocket port | `443` |
| `jco.client.client` | Client (optional) | `100` |
| `jco.destination.ws_ping_period` | Keep-alive (0 or 10-86400s) | `60` |
| `jco.destination.ws_pong_timeout` | Pong timeout (0 or 10-3600s) | `30` |
| `jco.client.tls_trust_all` | Trust all certs (0=no, 1=yes) | `0` |

**Trust Store Options**:
- Dedicated trust store with location/password
- Default client trust store
- Trust all (demo only)

**Supported Targets**:
- SAP S/4HANA Cloud
- BTP ABAP Environment
- On-premise ABAP 1909+

---

## User Logon Properties (RFC)

### Core Properties

| Property | Description | Max Length | Case |
|----------|-------------|------------|------|
| `jco.client.user` | Username | 12 chars | Insensitive |
| `jco.client.alias_user` | Alias (alt to user) | 40 chars | Sensitive |
| `jco.client.passwd` | Password | 8-40 chars | Depends on NW version |
| `jco.client.lang` | Logon language | 2 chars | ISO code |

### Password Behavior

| NetWeaver Version | Max Length | Case Sensitive |
|-------------------|------------|----------------|
| < 7.0 | 8 chars | No |
| >= 7.0 | 40 chars | Yes |

### Authentication Types

**`jco.destination.auth_type`**:

| Value | Description |
|-------|-------------|
| `CONFIGURED_USER` | Direct credentials (default) |
| `PrincipalPropagation` | Business user SSO via tokens |
| `TechnicalUserPropagation` | Technical user token forwarding |

### Certificate-Based Login

| Property | Description |
|----------|-------------|
| `jco.client.tls_client_certificate_logon` | Enable cert login (1=yes) |
| Key Store Location | Path to keystore file |
| Key Store Password | Keystore password |

When certificate login enabled, username/password fields hidden.

### Technical User Propagation

| Property | Description |
|----------|-------------|
| `jco.client.tech_user_id` | OAuth client ID |
| `jco.client.tech_user_secret` | OAuth client secret |
| `jco.client.tech_user_service_url` | Token service URL |

---

## SAP SuccessFactors Integration

### OAuth Client Setup

**Prerequisites**:
1. Download X.509 certificate from BTP Cockpit
   - Navigate to Connectivity > Destinations
   - Click "Download Trust"

**Configuration Steps**:

1. **Access OAuth Management**:
   - SuccessFactors Admin Center
   - Search "OAuth"
   - Select "Manage OAuth2 Client Applications"

2. **Register Application**:
   ```
   Application Name: <descriptive-name>
   Application URL: https://api.cf.<region>.ondemand.com/<subaccount-GUID>
   X.509 Certificate: <paste downloaded certificate>
   ```

3. **Get API Key**:
   - Find client by name
   - Click "View" in Actions
   - Copy the API Key

**Use in Destination**:
```json
{
  "Name": "successfactors-dest",
  "Type": "HTTP",
  "URL": "https://<sf-instance>.successfactors.com",
  "Authentication": "OAuth2SAMLBearerAssertion",
  "ProxyType": "Internet",
  "audience": "www.successfactors.com",
  "apiKey": "<API-Key-from-SF>",
  "companyId": "<company-id>",
  "clientKey": "<client-key-from-sf-oauth>",
  "tokenServiceUrl": "https://<sf-api>.successfactors.com/oauth/token",
  "tokenServiceUser": "<token-service-user>",
  "tokenServicePassword": "<token-service-password>"
}
```

---

## Common Properties (Cloud Connector API)

### Instance Properties

| Property | Description | Values |
|----------|-------------|--------|
| `ha` | High availability role | `master`, `shadow` |
| `description` | Instance description | String |
| `version` | Software version (v2.14+) | String |

### API Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get properties | GET | `/api/v1/configuration/connector` |
| Get version | GET | `/api/v1/connector/version` |
| Update description | PUT | `/api/v1/configuration/connector` |

### Role Requirements

| Operation | Required Roles |
|-----------|---------------|
| Read properties | Admin, Subaccount Admin, Display, Support |
| Update description | Administrator only |

---

## Prerequisites

### Cloud Foundry Environment

- SAP BTP subaccount with Cloud Foundry enabled
- Destination Service instance
- Connectivity Service instance (for on-premise)
- Cloud Connector (for on-premise systems)

### Kubernetes/Kyma Environment

- Kubernetes cluster with BTP integration
- Connectivity Proxy (for on-premise)
- Transparent Proxy (for simplified access)
- Destination Service instance

### Cloud Connector

- Supported OS (Windows, Linux, macOS)
- Java 8+ runtime
- Network access to BTP region hosts
- Network access to target backend systems

### On-Premise Systems

- SAP NetWeaver 4.6C+ (for RFC)
- SAP NetWeaver 7.0+ (for principal propagation)
- S/4HANA 1909+ (for WebSocket RFC)

---

## Connectivity Support

### Getting Help

**SAP Support Portal**:
- Component: `BC-CP-CON` (Connectivity)
- Component: `BC-CP-CF-SEC-DST` (Destination Service)
- Component: `BC-CP-TOOLS-SCC` (Cloud Connector)

**SAP Community**:
- Tag: `SAP BTP Connectivity`
- Tag: `Cloud Connector`

### Log Collection

**Cloud Connector**:
```bash
# Windows
%PROGRAMDATA%\SAP\scc\logs\

# Linux
/opt/sap/scc/logs/
```

**Kubernetes**:
```bash
kubectl logs deployment/connectivity-proxy -n <namespace>
kubectl logs deployment/transparent-proxy -n <namespace>
```

---

**Last Updated**: 2025-11-22
**Source Files**:
- connectivity-via-reverse-proxy-dde01af.md
- user-roles-b922fc8.md
- target-system-configuration-ab6eac9.md
- user-logon-properties-8b1e1c3.md
- create-an-oauth-client-in-sap-successfactors-69130a7.md
- common-properties-8aed644.md
- getting-started-daca64d.md
- prerequisites-e23f776.md
- connectivity-support-e5580c5.md
