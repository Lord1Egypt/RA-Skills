# Advanced Configuration - Complete Reference

**Source**: [https://github.com/SAP-docs/btp-connectivity/tree/main/docs/1-connectivity-documentation](https://github.com/SAP-docs/btp-connectivity/tree/main/docs/1-connectivity-documentation)

---

## Destination Deployment Methods

### MTA Descriptor

Deploy destinations via Multi-Target Application (MTA) descriptors.

**mta.yaml Structure:**
```yaml
_schema-version: "3.2"
ID: my-mta-app
version: 1.0.0

modules:
  - name: my-app
    type: nodejs
    requires:
      - name: dest-service

resources:
  - name: dest-service
    type: org.cloudfoundry.managed-service
    parameters:
      service: destination
      service-plan: lite
      config:
        init_data:
          subaccount:
            existing_destinations_policy: update
            destinations:
              - Name: my-destination
                Type: HTTP
                URL: https://api.example.com
                Authentication: NoAuthentication
```

**Existing Destinations Policy:**
| Policy | Behavior |
|--------|----------|
| `fail` | Error if destination exists (default) |
| `ignore` | Skip existing destinations |
| `update` | Overwrite existing destinations |

### Config.JSON for Service Instance

```json
{
  "HTML5Runtime_enabled": true,
  "init_data": {
    "subaccount": {
      "existing_destinations_policy": "update",
      "existing_certificates_policy": "update",
      "destinations": [
        {
          "Name": "my-destination",
          "Type": "HTTP",
          "URL": "https://api.example.com",
          "Authentication": "OAuth2ClientCredentials",
          "clientId": "...",
          "clientSecret": "...",
          "tokenServiceURL": "..."
        }
      ],
      "certificates": [
        {
          "Name": "my-cert",
          "Content": "base64-encoded-certificate"
        }
      ]
    },
    "instance": {
      "existing_destinations_policy": "update",
      "destinations": []
    }
  }
}
```

---

## Destination Chaining

### Predefined Chains

| Chain Name | Purpose |
|------------|---------|
| `com.sap.iasGeneratedOAuth2SamlBearerAssertion` | IAS SAML to OAuth2 token |
| `com.sap.sequentialUserPropagation` | User token transformation |

### IAS-Generated SAML Bearer Chain

**Provider Destination (SAML Token):**
```json
{
  "Name": "ias-saml-provider",
  "Type": "HTTP",
  "URL": "https://ias-tenant.accounts.ondemand.com",
  "Authentication": "OAuth2TokenExchange",
  "tokenServiceURL": "https://ias-tenant.accounts.ondemand.com/oauth2/token"
}
```

**Consumer Destination (Bearer Token):**
```json
{
  "Name": "target-api",
  "Type": "HTTP",
  "URL": "https://api.example.com",
  "Authentication": "OAuth2SAMLBearerAssertion",
  "x_chain_name": "com.sap.iasGeneratedOAuth2SamlBearerAssertion",
  "x_chain_var_saml_provider": "ias-saml-provider"
}
```

### Dynamic Lookup (Destination Gateway)

Single custom resource for multiple destinations:

```yaml
apiVersion: destination.connectivity.api.sap/v1
kind: Destination
metadata:
  name: dynamic-destination
spec:
  destinationRef:
    name: "*"
```

**Request Headers:**
| Header | Description |
|--------|-------------|
| `X-Destination-Name` | Target destination name |
| `X-Fragment-Name` | Optional fragment name |
| `X-Fragment-Optional` | Allow missing fragment |
| `X-Destination-Level` | provider_subaccount, provider_instance |
| `X-Chain-Name` | Destination chain name |
| `X-Chain-Var-*` | Chain variable values |

---

## Cloud Connector Advanced

### System Mappings REST API

**Create Mapping:**
```bash
POST /api/v1/configuration/subaccounts/{region}/{subaccount}/systemMappings

{
  "virtualHost": "virtual-erp",
  "virtualPort": 443,
  "localHost": "erp.internal.corp",
  "localPort": 443,
  "protocol": "HTTPS",
  "backendType": "ABAP",
  "authenticationMode": "NONE",
  "description": "ERP System"
}
```

**Supported Protocols:**
- HTTP, HTTPS
- RFC, RFCS
- LDAP, LDAPS
- TCP, TCPS

**Backend Types:**
- ABAP (HTTP, RFC, TCP)
- SAP_GATEWAY (HTTP, RFC, TCP)
- SAP_HANA (HTTP, TCP)
- OTHER_SAP (HTTP, TCP)
- NON_SAP (HTTP, TCP, LDAP)
- SAP_JAVA (HTTP)

### Domain Mappings for Cookies

When on-premise servers set cookies with internal domains:

1. Navigate to **Cloud To On-Premises > Cookie Domains**
2. Add mapping:
   - Virtual Domain: cloud-facing domain
   - Internal Domain: on-premise domain
3. Cloud Connector rewrites `Set-Cookie` domain attributes

### Kerberos Configuration

For Kerberos-enabled backends (non-ABAP):

1. Navigate to **Configuration > On Premise > Kerberos**
2. Configure:
   - Realm name
   - KEYTAB file (with rc4-hmac key)
   - Service user credentials
   - KDC addresses (host:port, default port 88)

**Note:** Not supported for ABAP backends (use certificate-based).

### Named Cloud Connector Users

For audit trail and multi-user access:

1. Enable LDAP user administration
2. Configure user groups with appropriate roles
3. Map LDAP groups to Cloud Connector roles

### Certificate Rule-Based Mapping

For principal propagation to ABAP systems:

1. Enable `login/certificate_mapping_rulebased` parameter in RZ10
2. Import sample certificate in transaction CERTRULE
3. Create mapping rules for certificate attributes to users

---

## Cache Configuration

### Transparent Proxy Caching

| Cache Type | Content | TTL |
|------------|---------|-----|
| Destination Service Token | OAuth access tokens | Token lifetime |
| Destination Cache | Destination configs | 2 minutes |
| Destination Tokens | OAuth/SAML tokens | Token lifetime |

### Resilience Behavior

When services unavailable:
- Proxy continues using cached data
- Updates cache when services restore
- Expired tokens trigger re-authentication

---

## System Requirements

### Disk Space

| Component | Minimum |
|-----------|---------|
| Installation files | 50 MB |
| Installed Cloud Connector | 70 MB |
| **Total** | **120 MB** |

### Runtime Space

| Component | Recommendation |
|-----------|----------------|
| Log files | 1-20 GB |
| Trace files | Variable (GB at trace level "All") |
| Audit logs | Based on retention policy |

### Log Files Location

| File | Path | Content |
|------|------|---------|
| Core traces | `<scc_dir>/log/scc_core.trc` | General traces |
| Tunnel traffic | `<scc_dir>/log/tunnel_traffic_*.trc` | Communication payload |
| SNC traffic | `<scc_dir>/log/snc_traffic_*.trc` | ABAP Cloud SNC |
| Audit logs | `<scc_dir>/log/audit/<subaccount>/` | Security events |

---

## Service Channels

### Port Overview

View all configured service channels:
1. Navigate to **Connector > Service Channels Overview**
2. Filter by status: All, Enabled, Disabled, Failed
3. View details: Status, Type, Subaccount, Tenant Host

### Service Channel Types

| Type | Protocol | Use Case |
|------|----------|----------|
| ABAP Cloud System | RFC | Invoke ABAP Cloud function modules |
| Kubernetes Cluster | TCP/RFC | Expose K8s workloads |

### Kubernetes Service Mapping

```yaml
apiVersion: servicemapping.connectivityproxy.sap.com/v1
kind: ServiceMapping
metadata:
  name: my-service
spec:
  type: TCP
  subaccountId: <subaccount-id>
  serviceId: my-virtual-host
  internalAddress: my-service.namespace:8080
  locationIds:
    - loc1
```

---

## Destination Service Notifications

Subscribe to alerts via SAP Alert Notification Service:

1. Create Alert Notification service instance
2. Configure event subscriptions
3. Receive notifications for:
   - Certificate expiration
   - Configuration changes
   - Service health events

---

## Zero Trust Identity Service (ZTIS)

### Workload Attestation Method

1. Create Zero Trust service credentials for each Transparent Proxy component
2. Configure x509 attestation for Destination service
3. Set Helm values for SPIRE agent socket path

### SVID Store Method

1. Configure credentials for Kubernetes Secret-based identity
2. Set Helm values for secret name and namespace
3. ZTIS stores identity documents in specified secrets

---

## Documentation Links

- MTA Destinations: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/create-destinations-using-mta-descriptor](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/create-destinations-using-mta-descriptor)
- Config.JSON: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/use-config-json](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/use-config-json)
- Destination Chaining: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/destination-chaining](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/destination-chaining)
- System Mappings API: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/system-mappings](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/system-mappings)
- ZTIS Integration: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/integration-with-zero-trust-identity-service](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/integration-with-zero-trust-identity-service)

---

**Last Updated**: 2025-11-22
