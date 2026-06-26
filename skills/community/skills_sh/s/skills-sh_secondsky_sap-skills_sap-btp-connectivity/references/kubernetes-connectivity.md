# Kubernetes Connectivity - Complete Reference

**Source**: [https://github.com/SAP-docs/btp-connectivity/blob/main/docs/1-connectivity-documentation/connectivity-proxy-for-kubernetes-e661713.md](https://github.com/SAP-docs/btp-connectivity/blob/main/docs/1-connectivity-documentation/connectivity-proxy-for-kubernetes-e661713.md)

---

## Overview

Kubernetes connectivity in SAP BTP involves two main components:

1. **Connectivity Proxy**: Enables on-premise system access from Kubernetes
2. **Transparent Proxy**: Exposes BTP destinations as Kubernetes Services

Both work together for comprehensive connectivity in Kubernetes and Kyma environments.

---

## Connectivity Proxy

### Purpose

Bridges Kubernetes workloads with on-premise systems via Cloud Connector.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│  ┌─────────────┐    ┌───────────────────┐                   │
│  │ Application │───►│ Connectivity Proxy │                   │
│  └─────────────┘    └─────────┬─────────┘                   │
└───────────────────────────────┼─────────────────────────────┘
                                │ Secure Tunnel
                    ┌───────────┴───────────┐
                    │  SAP Connectivity     │
                    │      Service          │
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    │   Cloud Connector     │
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    │  On-Premise Systems   │
                    └───────────────────────┘
```

### Installation via Helm

```bash
# Add SAP registry
helm repo add sap https://sapse.github.io/helm-charts

# Install Connectivity Proxy
helm install connectivity-proxy \
  oci://registry-1.docker.io/sapse/connectivity-proxy \
  --version <version> \
  --namespace <namespace> \
  -f values.yaml
```

### values.yaml Configuration

```yaml
# Connectivity Service credentials
config:
  integration:
    connectivityService:
      serviceCredentialsKey: connectivity-service-key

# Subaccount configuration
  subaccountId: <subaccount-id>
  subaccountSubdomain: <subdomain>

# High availability
replicaCount: 2

# Resource limits
resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

# Logging
config:
  servers:
    proxy:
      logging:
        level: INFO
```

### Create Connectivity Service Instance

```bash
# Cloud Foundry
cf create-service connectivity connectivity_proxy my-connectivity-service

# Create service key
cf create-service-key my-connectivity-service my-key

# Get credentials
cf service-key my-connectivity-service my-key
```

### Kubernetes Secret

Create secret from service key:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: connectivity-service-key
  namespace: <namespace>
type: Opaque
stringData:
  connectivity_key: |
    {
      "clientid": "...",
      "clientsecret": "...",
      "url": "...",
      "onpremise_proxy_host": "...",
      "onpremise_proxy_port": "..."
    }
```

### Using the Connectivity Proxy

Applications connect via HTTP with proxy configuration:

```javascript
const axios = require('axios');

// Get proxy settings from service binding
const proxy = {
  host: process.env.CONNECTIVITY_PROXY_HOST || 'connectivity-proxy.namespace',
  port: process.env.CONNECTIVITY_PROXY_PORT || 20003
};

// Make request to on-premise system
const response = await axios.get('http://virtual-host/api/resource', {
  proxy: {
    host: proxy.host,
    port: proxy.port,
    protocol: 'http'
  },
  headers: {
    'Proxy-Authorization': `Bearer ${accessToken}`,
    'SAP-Connectivity-SCC-Location_ID': 'optional-location-id'
  }
});
```

---

## Transparent Proxy

### Purpose

Provides unified access to BTP destinations as Kubernetes Services, handling authentication, principal propagation, and protocol translation automatically.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│  ┌─────────────┐    ┌───────────────────┐                   │
│  │ Application │───►│ Transparent Proxy  │                   │
│  └─────────────┘    └─────────┬─────────┘                   │
│                               │                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Destination Custom Resources               ││
│  │  my-destination.namespace → BTP Destination             ││
│  └─────────────────────────────────────────────────────────┘│
└───────────────────────────────┼─────────────────────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
     ┌────────┴────┐   ┌───────┴───────┐  ┌─────┴─────┐
     │  Internet   │   │ Connectivity  │  │   Cloud   │
     │  Services   │   │    Proxy      │  │ Connector │
     └─────────────┘   └───────────────┘  └───────────┘
```

### Installation via Helm

```bash
helm install transparent-proxy \
  oci://registry-1.docker.io/sapse/transparent-proxy \
  --version <version> \
  --namespace <namespace> \
  -f values.yaml
```

### values.yaml Configuration

```yaml
# Destination Service credentials
config:
  integration:
    destinationService:
      serviceCredentialsKey: destination-service-key

# Connectivity Proxy integration (for on-premise)
  connectivityProxy:
    enabled: true
    serviceName: connectivity-proxy

# Tenant mode
  tenantMode: shared  # or dedicated

# Logging
  logging:
    level: info

# Resources
replicaCount:
  http: 2
  tcp: 1

resources:
  http:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 256Mi
```

### Destination Custom Resource

Create a Custom Resource for each destination:

```yaml
apiVersion: destination.connectivity.api.sap/v1
kind: Destination
metadata:
  name: my-api-destination
  namespace: default
spec:
  destinationRef:
    name: my-btp-destination  # Name in BTP Destination Service
  destinationServiceInstanceName: my-dest-service  # Optional
```

### Accessing Destinations

After creating the Custom Resource, access the destination as a Kubernetes Service:

```javascript
const axios = require('axios');

// Access destination via Transparent Proxy
// URL format: http://<destination-name>.<namespace>
const response = await axios.get('http://my-api-destination.default/api/resource', {
  headers: {
    'Authorization': 'Bearer ' + userToken  // For user propagation
  }
});
```

### Supported Destination Types

| Type | Protocol | Notes |
|------|----------|-------|
| HTTP | HTTP/HTTPS | Internet and on-premise |
| LDAP | LDAP/LDAPS | Directory access |
| MAIL | SMTP/IMAP/POP3 | Email protocols |
| TCP | TCP (SOCKS5) | Generic TCP |

---

## Service Channels (On-Premise-to-Cloud)

### Purpose

Expose Kubernetes workloads to on-premise systems via Cloud Connector.

### ServiceMapping Resource

```yaml
apiVersion: servicemapping.connectivityproxy.sap.com/v1
kind: ServiceMapping
metadata:
  name: my-exposed-service
spec:
  # Protocol type
  type: TCP  # or RFC

  # Subaccount for routing
  subaccountId: <subaccount-id>

  # Virtual service name (exposed to on-premise)
  serviceId: my-k8s-service

  # Internal Kubernetes address
  internalAddress: my-service.namespace:8080

  # Optional: Location IDs for specific Cloud Connectors
  locationIds:
    - loc1
    - loc2
```

### Constraints

- `type` + `subaccountId` + `serviceId` must be unique
- ServiceMappings are cluster-scoped
- Requires Cloud Connector 2.15.0+ (2.14.2+ for RFC only)

---

## Kyma Environment

### Differences from Standalone Kubernetes

In Kyma, connectivity components are managed as Kyma modules:

1. **Module Installation**: Enable via Kyma dashboard
2. **Operator Management**: Kubernetes Operator handles lifecycle
3. **Feature Set**: May differ from standalone versions

### Enable Connectivity Module

```yaml
# Kyma module configuration
apiVersion: operator.kyma-project.io/v1alpha1
kind: ModuleTemplate
metadata:
  name: connectivity
spec:
  channel: regular
```

### Destination Custom Resource in Kyma

```yaml
apiVersion: destinations.connectivity.api.sap/v1alpha1
kind: Destination
metadata:
  name: my-destination
  namespace: default
spec:
  destinationRef:
    name: my-btp-destination
```

---

## Multi-Region Deployment

### Configuration

Deploy Connectivity Proxy across regions:

```yaml
# values.yaml for multi-region
config:
  multiRegion:
    enabled: true
    regions:
      - name: eu10
        connectivity:
          serviceCredentialsKey: eu10-connectivity-key
      - name: us10
        connectivity:
          serviceCredentialsKey: us10-connectivity-key
```

---

## Istio Service Mesh Integration

### Prerequisites

- Istio installed in cluster
- PeerAuthentication configured

### Configuration

```yaml
# values.yaml for Istio
config:
  istio:
    enabled: true

# Disable internal mTLS (Istio handles it)
config:
  servers:
    proxy:
      http:
        enableMTLS: false
```

### PeerAuthentication

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: connectivity-proxy
  namespace: <namespace>
spec:
  selector:
    matchLabels:
      app: connectivity-proxy
  mtls:
    mode: STRICT
```

---

## Lifecycle Management

### Upgrade

```bash
# Helm upgrade
helm upgrade connectivity-proxy \
  oci://registry-1.docker.io/sapse/connectivity-proxy \
  --version <new-version> \
  --namespace <namespace> \
  -f values.yaml
```

### Downgrade

```bash
# Same as upgrade with older version
helm upgrade connectivity-proxy \
  oci://registry-1.docker.io/sapse/connectivity-proxy \
  --version <older-version> \
  --namespace <namespace> \
  -f values.yaml
```

### Uninstall

```bash
helm uninstall connectivity-proxy --namespace <namespace>

# CRDs are preserved; delete manually if needed
kubectl delete crd servicemappings.servicemapping.connectivityproxy.sap.com
```

---

## Troubleshooting

### Log Retrieval

```bash
# Connectivity Proxy logs
kubectl logs statefulset/connectivity-proxy -n <namespace>

# Transparent Proxy logs
kubectl logs deployment/transparent-proxy -n <namespace>
```

### Change Log Level

```bash
kubectl exec <pod> -n <namespace> -it -- change-log-level DEBUG
```

### List Loggers

```bash
kubectl exec <pod> -n <namespace> -it -- list-loggers
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 405 | HTTPS instead of HTTP | Use `http://` with port 20003 |
| 407 | Missing proxy auth | Add `Proxy-Authorization: Bearer <token>` |
| 503 | Cloud Connector offline | Check CC connection and Location ID |

### Error Response Headers

- `x-error-message`: Error description
- `x-error-origin`: Component that failed
- `x-request-id`: Correlation ID

---

## Documentation Links

- Connectivity Proxy: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/connectivity-proxy-for-kubernetes](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/connectivity-proxy-for-kubernetes)
- Transparent Proxy: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/transparent-proxy-for-kubernetes](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/transparent-proxy-for-kubernetes)
- Kyma Connectivity: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/connectivity-in-kyma-environment](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/connectivity-in-kyma-environment)
- Helm Charts: [https://github.com/SAP/connectivity-proxy](https://github.com/SAP/connectivity-proxy)

---

**Last Updated**: 2025-11-22
