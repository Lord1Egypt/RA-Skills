---
name: tractusx-edc-v3
description: Interact with Tractus-X EDC (Eclipse Data Connector) control plane API v3 for managing assets, contract negotiations, policies, and data transfers.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - EDC_CONTROL_PLANE_URL
        - EDC_API_KEY
    primaryEnv: EDC_CONTROL_PLANE_URL
    emoji: "\U0001F680"
    homepage: https://eclipse-tractusx.github.io/tractusx-edc/
---

# Tractus-X EDC Connector Skill (v3 API)

Use this skill to interact with a Tractus-X EDC (Eclipse Data Connector) control plane using the v3 API.

## Configuration

Set these environment variables:

- `EDC_CONTROL_PLANE_URL` - Base URL of the EDC control plane (e.g., `http://localhost:9192`)
- `EDC_API_KEY` - API key for authentication (optional, depends on connector config)

## API Base URL

```
${EDC_CONTROL_PLANE_URL}/v3
```

## Core Operations

### 1. Assets Management (v3)

**Create Asset:**

```bash
curl -X POST "${EDC_CONTROL_PLANE_URL}/v3/assets" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}" \
  -d '{
    "properties": {
      "id": "asset-id",
      "name": "Asset Name",
      "contentType": "application/json",
      "description": "Data asset description"
    },
    "dataAddress": {
      "type": "HttpData",
      "baseUrl": "https://provider.example.com/data",
      "proxyBody": true,
      "proxyPath": true
    }
  }'
```

**Update Asset:**

```bash
curl -X PUT "${EDC_CONTROL_PLANE_URL}/v3/assets" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}" \
  -d '{
    "properties": {
      "id": "asset-id",
      "name": "Updated Asset Name"
    }
  }'
```

**List Assets:**

```bash
curl -X POST "${EDC_CONTROL_PLANE_URL}/v3/assets/request" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}" \
  -d '{
    "filterExpression": [],
    "range": {"from": 0, "to": 100}
  }'
```

**Get Asset:**

```bash
curl -X GET "${EDC_CONTROL_PLANE_URL}/v3/assets/{id}" \
  -H "X-Api-Key: ${EDC_API_KEY}"
```

**Delete Asset:**

```bash
curl -X DELETE "${EDC_CONTROL_PLANE_URL}/v3/assets/{id}" \
  -H "X-Api-Key: ${EDC_API_KEY}"
```

### 2. Policy Definitions (v3)

**List Policies:**

```bash
curl -X POST "${EDC_CONTROL_PLANE_URL}/v3/policydefinitions/request" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}" \
  -d '{"filterExpression": [], "range": {"from": 0, "to": 100}}'
```

### 3. Contract Definitions (v3)

**Create Contract Definition:**

```bash
curl -X POST "${EDC_CONTROL_PLANE_URL}/v3/contractdefinitions" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}" \
  -d '{
    "id": "contract-def-id",
    "accessPolicyId": "policy-id",
    "contractPolicyId": "policy-id",
    "assetsSelector": [{
      "operandLeft": "https://w3id.org/edc/v0.0.1/ns/id",
      "operator": "=",
      "operandRight": "asset-id"
    }]
  }'
```

**Update Contract Definition:**

```bash
curl -X PUT "${EDC_CONTROL_PLANE_URL}/v3/contractdefinitions" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}" \
  -d '{
    "id": "contract-def-id",
    "accessPolicyId": "policy-id",
    "contractPolicyId": "policy-id",
    "assetsSelector": [{
      "operandLeft": "https://w3id.org/edc/v0.0.1/ns/id",
      "operator": "=",
      "operandRight": "asset-id"
    }]
  }'
```

**List Contract Definitions:**

```bash
curl -X POST "${EDC_CONTROL_PLANE_URL}/v3/contractdefinitions/request" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}" \
  -d '{"filterExpression": [], "range": {"from": 0, "to": 100}}'
```

### 4. Contract Negotiations (v3)

**Initiate Negotiation:**

```bash
curl -X POST "${EDC_CONTROL_PLANE_URL}/v3/contractnegotiations" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}" \
  -d '{
    "connectorId": "provider-connector-id",
    "connectorAddress": "http://provider-connector:9194/protocol/dsp",
    "offer": {
      "assetId": "asset-id",
      "offerId": "offer-id:1",
      "policy": {
        "permissions": [{
          "target": "default",
          "action": {"type": "USE"},
          "constraints": []
        }]
      }
    }
  }'
```

**Query Negotiations:**

```bash
curl -X POST "${EDC_CONTROL_PLANE_URL}/v3/contractnegotiations/request" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}" \
  -d '{"filterExpression": [], "range": {"from": 0, "to": 100}}'
```

**Get Contract Agreement for Negotiation:**

```bash
curl -X GET "${EDC_CONTROL_PLANE_URL}/v3/contractnegotiations/{id}/agreement" \
  -H "X-Api-Key: ${EDC_API_KEY}"
```

### 5. Contract Agreements (v3)

**Get Contract Agreement:**

```bash
curl -X GET "${EDC_CONTROL_PLANE_URL}/v3/contractagreements/{id}" \
  -H "X-Api-Key: ${EDC_API_KEY}"
```

**Get Retired Agreements:**

```bash
curl -X POST "${EDC_CONTROL_PLANE_URL}/v3/contractagreements/retirements/request" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}"
```

### 6. Transfer Processes (v3)

**Initiate Transfer:**

```bash
curl -X POST "${EDC_CONTROL_PLANE_URL}/v3/transferprocesses" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}" \
  -d '{
    "protocol": "dsp",
    "connectorId": "provider-connector-id",
    "connectorAddress": "http://provider-connector:9194/protocol/dsp",
    "contractId": "contract-agreement-id",
    "assetId": "asset-id",
    "managedResources": true,
    "dataDestination": {
      "type": "HttpProxy",
      "baseUrl": "http://consumer-backend:8080/data"
    }
  }'
```

**Suspend Transfer:**

```bash
curl -X POST "${EDC_CONTROL_PLANE_URL}/v3/transferprocesses/{id}/suspend" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}" \
  -d '{"reason": "Suspension reason"}'
```

### 7. EDR (Endpoint Data Reference) Management (v3)

**Initiate EDR Negotiation:**

```bash
curl -X POST "${EDC_CONTROL_PLANE_URL}/v3/edrs" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: ${EDC_API_KEY}" \
  -d '{
    "connectorId": "provider-connector-id",
    "connectorAddress": "http://provider-connector:9194/protocol/dsp",
    "offer": {
      "assetId": "asset-id",
      "offerId": "offer-id:1",
      "policy": {
        "permissions": [{
          "target": "default",
          "action": {"type": "USE"},
          "constraints": []
        }]
      }
    }
  }'
```

**Get EDR Data Address:**

```bash
curl -X GET "${EDC_CONTROL_PLANE_URL}/v3/edrs/{transferProcessId}/dataaddress" \
  -H "X-Api-Key: ${EDC_API_KEY}"
```

### 8. Business Partner Groups (v3)

**Resolve All Groups:**

```bash
curl -X GET "${EDC_CONTROL_PLANE_URL}/v3/business-partner-groups/groups" \
  -H "X-Api-Key: ${EDC_API_KEY}"
```

**Resolve Groups for BPN:**

```bash
curl -X GET "${EDC_CONTROL_PLANE_URL}/v3/business-partner-groups/{bpn}" \
  -H "X-Api-Key: ${EDC_API_KEY}"
```

**Delete BPN Entry:**

```bash
curl -X DELETE "${EDC_CONTROL_PLANE_URL}/v3/business-partner-groups/{bpn}" \
  -H "X-Api-Key: ${EDC_API_KEY}"
```

### 9. Health Checks

**Health Check:**

```bash
curl -X GET "${EDC_CONTROL_PLANE_URL}/check/health"
```

**Startup Check:**

```bash
curl -X GET "${EDC_CONTROL_PLANE_URL}/check/startup"
```

## Workflow: Complete Data Exchange

1. **Provider Side:**
   - Create Asset with data address
   - Create Policy definition
   - Create Contract definition linking asset to policy

2. **Consumer Side:**
   - Initiate Contract Negotiation
   - Query negotiations to track state
   - Get Contract Agreement from negotiation
   - Initiate Transfer Process
   - Suspend/resume transfer as needed
   - Get EDR data address for actual data access

## Common States

### Contract Negotiation States (from negotiation object)

- `REQUESTING` - Initial request sent
- `OFFERED` - Offer received
- `ACCEPTED` - Offer accepted
- `AGREED` - Agreement reached
- `VERIFIED` - Agreement verified
- `TERMINATED` - Negotiation ended

### Transfer Process States

- `INITIAL` - Transfer initiated
- `PROVISIONING` - Resources being provisioned
- `PROVISIONED` - Resources ready
- `REQUESTING` - Request sent to provider
- `STARTED` - Transfer started
- `SUSPENDED` - Transfer paused
- `COMPLETED` - Transfer finished
- `TERMINATED` - Transfer ended
- `ERROR` - Transfer failed

## Error Handling

Errors return with status codes:

- `400` - Request malformed
- `404` - Resource not found
- `409` - Conflict (e.g., asset already exists)
- `500` - Internal server error

Response format:

```json
[{ "message": "Error description", "path": "field/path", "invalidValue": "bad-value" }]
```

## OpenAPI Reference

Full API specification: https://eclipse-tractusx.github.io/api-hub/tractusx-edc/0.12.0/control-plane/control-plane.yaml
