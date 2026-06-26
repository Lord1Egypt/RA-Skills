# SAP BTP Connectivity Reference

## Overview

SAP BTP provides comprehensive connectivity infrastructure for secure communication between cloud applications and various system types including on-premise systems, private clouds, and public cloud services.

## Core Components

### SAP Connectivity Service

**Purpose**: Secure connections to on-premise and private cloud systems

**Features:**
- Cloud Connector integration
- Connectivity Proxy support
- Multiple protocol support

### Cloud Connector

**Purpose**: Secure link between cloud and on-premise systems

**Characteristics:**
- Operates as reverse proxy in secured networks
- Controlled resource access
- No inbound firewall rules required
- High availability configuration supported

**Installation:**
- Windows or Linux
- Portable version available
- Master-shadow configuration for HA

### Connectivity Proxy

**Purpose**: Cloud-side counterpart to Cloud Connector

**Supported Environments:**
- Cloud Foundry
- Kyma
- Native Kubernetes
- ABAP Environment

### SAP Destination Service

**Purpose**: Routing and authentication management

**Capabilities:**
- Store connection properties
- Manage OAuth token flows
- Custom parameter handling
- Design-time configuration

**Destination Types:**
| Type | Use Case |
|------|----------|
| HTTP | REST/OData APIs |
| RFC | SAP function calls |
| LDAP | Directory services |
| Mail | Email servers |

### SAP Transparent Proxy

**Purpose**: Simplify Kubernetes connectivity

**Features:**
- Exposes target systems on local network
- Automates authentication
- Automatic destination retrieval
- Native Kubernetes integration

## Connectivity Patterns

### Cloud-to-Cloud

**Use Cases:**
- Kubernetes to databases
- Application to SAP services
- OData endpoint consumption
- Third-party API integration

**Implementation:**
```yaml
# destination configuration
- name: S4HANA_CLOUD
  type: HTTP
  url: https://my-s4.cloud.sap
  authentication: OAuth2SAMLBearerAssertion
  tokenServiceURL: https://my-s4.cloud.sap/sap/bc/sec/oauth2/token
```

### Cloud-to-On-Premise

**Supported Systems:**
- ABAP systems (RFC, OData)
- Databases
- Mail servers
- FTP servers
- LDAP directories

**User Propagation:**
- Principal propagation supported
- SSO via SAML/OAuth
- Technical user fallback

**Configuration Steps:**
1. Install Cloud Connector
2. Connect to BTP subaccount
3. Map virtual hosts to internal systems
4. Configure destinations in BTP Cockpit

### On-Premise-to-Cloud

**Use Cases:**
- RFC callbacks from cloud
- Kubernetes cluster service access
- Event notifications

## Destination Configuration

### HTTP Destination (CAP)
```javascript
// package.json
{
  "cds": {
    "requires": {
      "API_BUSINESS_PARTNER": {
        "kind": "odata-v2",
        "model": "srv/external/API_BUSINESS_PARTNER",
        "credentials": {
          "destination": "S4HANA",
          "path": "/sap/opu/odata/sap/API_BUSINESS_PARTNER"
        }
      }
    }
  }
}
```

### Destination in BTP Cockpit

| Property | Value | Description |
|----------|-------|-------------|
| Name | S4HANA | Destination identifier |
| Type | HTTP | Protocol type |
| URL | [https://...](https://...) | Target system URL |
| Proxy Type | Internet/OnPremise | Connection type |
| Authentication | OAuth2SAMLBearerAssertion | Auth method |

### Authentication Types

| Type | Use Case |
|------|----------|
| NoAuthentication | Public APIs |
| BasicAuthentication | Technical users |
| OAuth2ClientCredentials | Server-to-server |
| OAuth2SAMLBearerAssertion | User propagation |
| OAuth2UserTokenExchange | Token exchange |
| PrincipalPropagation | SSO on-premise |
| ClientCertificateAuthentication | mTLS |

## Cloud Connector Configuration

### System Mapping

```
Cloud Configuration:
  Virtual Host: s4hana.cloud
  Virtual Port: 443

On-Premise Configuration:
  Internal Host: s4hana.internal.corp
  Internal Port: 44300
  Protocol: HTTPS
```

### Access Control

- Define allowed resources
- Path-based filtering
- HTTP method restrictions

### High Availability

1. Install secondary Cloud Connector
2. Configure as shadow instance
3. Automatic failover

## CAP Integration

### Remote Service Configuration
```cds
// srv/external/API_BUSINESS_PARTNER.cds
using { API_BUSINESS_PARTNER as external } from './API_BUSINESS_PARTNER';

service RemoteService {
  entity BusinessPartners as projection on external.A_BusinessPartner {
    BusinessPartner,
    BusinessPartnerFullName,
    BusinessPartnerType
  };
}
```

### Service Implementation
```javascript
const cds = require('@sap/cds');

module.exports = cds.service.impl(async function() {
  const bupa = await cds.connect.to('API_BUSINESS_PARTNER');

  this.on('READ', 'BusinessPartners', async (req) => {
    return bupa.run(req.query);
  });
});
```

## ABAP Integration

### Communication Arrangement

1. Create Communication System
2. Define Communication Arrangement
3. Configure Authentication
4. Test Connection

### Service Consumption Model

```abap
" Generated proxy class usage
DATA(lo_client) = NEW /sap/bc/bupa/a_businesspartner( ).

TRY.
    DATA(lt_partners) = lo_client->get_business_partners(
      iv_top = 100
    ).
  CATCH cx_remote_call_error INTO DATA(lx_error).
    " Handle error
ENDTRY.
```

### RFC Destination (SM59 equivalent)
- Configure in Communication Systems app
- Support for trusted RFC
- User propagation options

## Kyma Connectivity

### Transparent Proxy Deployment
```yaml
apiVersion: gateway.kyma-project.io/v1beta1
kind: APIRule
metadata:
  name: my-api
spec:
  gateway: kyma-gateway.kyma-system.svc.cluster.local
  host: my-api
  rules:
    - path: /.*
      methods: ["GET", "POST"]
      accessStrategies:
        - handler: jwt
```

### Destination Binding
```yaml
apiVersion: services.cloud.sap.com/v1
kind: ServiceBinding
metadata:
  name: destination-binding
spec:
  serviceInstanceName: destination-instance
  secretName: destination-secret
```

## Best Practices

1. **Use Transparent Proxy** for Kubernetes connectivity
2. **Design-time configuration** via Destination Service
3. **Connectivity Service** for hybrid cloud-to-on-premise
4. **Principal propagation** when user context needed
5. **Technical users** for batch/background processing
6. **High availability** Cloud Connector for production

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection timeout | Firewall blocking | Check Cloud Connector logs |
| Authentication failed | Token expired | Refresh OAuth configuration |
| Destination not found | Wrong name | Verify destination exists in subaccount |
| Certificate error | Untrusted CA | Import certificate in Cloud Connector |

## Source Documentation

- Connecting to Remote Systems: [https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/connecting-to-remote-systems-d61a5fc.md](https://github.com/SAP-docs/btp-developer-guide/blob/main/docs/connecting-to-remote-systems-d61a5fc.md)
- SAP Connectivity Service: [https://help.sap.com/docs/connectivity](https://help.sap.com/docs/connectivity)
- Cloud Connector: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/cloud-connector](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/cloud-connector)
