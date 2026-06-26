# Destination Service REST API - Complete Reference

**Source**: [https://github.com/SAP-docs/btp-connectivity/blob/main/docs/1-connectivity-documentation/destination-service-rest-api-23ccafb.md](https://github.com/SAP-docs/btp-connectivity/blob/main/docs/1-connectivity-documentation/destination-service-rest-api-23ccafb.md)

**API Specification**: [https://api.sap.com/api/SAP_CP_CF_Connectivity_Destination](https://api.sap.com/api/SAP_CP_CF_Connectivity_Destination)

---

## Overview

The Destination Service REST API enables programmatic management of destinations, certificates, and destination fragments on SAP BTP.

---

## Authentication

### Get OAuth Access Token

```bash
# Extract credentials from service key
clientId="<from-service-key>"
clientSecret="<from-service-key>"
tokenUrl="<from-service-key>/oauth/token"
destinationUri="<from-service-key>"

# Request access token
curl -X POST "${tokenUrl}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  --data-urlencode "client_id=${clientId}" \
  --data-urlencode "client_secret=${clientSecret}"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 43199,
  "scope": "uaa.resource"
}
```

### Using mTLS (Recommended)

For enhanced security, use X.509 certificates instead of client secrets:

```bash
curl -X POST "${tokenUrl}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --cert client-cert.pem \
  --key client-key.pem \
  -d "grant_type=client_credentials" \
  --data-urlencode "client_id=${clientId}"
```

---

## Base URL

```
{destinationUri}/destination-configuration/v1
```

The `destinationUri` is obtained from the service key (field: `uri`).

---

## Endpoints

### Subaccount Destinations

#### List All Destinations

```bash
GET /subaccountDestinations

curl -X GET "${destinationUri}/destination-configuration/v1/subaccountDestinations" \
  -H "Authorization: Bearer ${access_token}"
```

**Response:**
```json
[
  {
    "Name": "my-destination",
    "Type": "HTTP",
    "URL": "https://api.example.com",
    "Authentication": "OAuth2ClientCredentials",
    "ProxyType": "Internet"
  }
]
```

#### Get Specific Destination

```bash
GET /subaccountDestinations/{destinationName}

curl -X GET "${destinationUri}/destination-configuration/v1/subaccountDestinations/my-destination" \
  -H "Authorization: Bearer ${access_token}"
```

#### Create Destination

```bash
POST /subaccountDestinations

curl -X POST "${destinationUri}/destination-configuration/v1/subaccountDestinations" \
  -H "Authorization: Bearer ${access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "new-destination",
    "Type": "HTTP",
    "URL": "https://api.example.com",
    "Authentication": "BasicAuthentication",
    "ProxyType": "Internet",
    "User": "username",
    "Password": "password"
  }'
```

#### Update Destination

```bash
PUT /subaccountDestinations/{destinationName}

curl -X PUT "${destinationUri}/destination-configuration/v1/subaccountDestinations/my-destination" \
  -H "Authorization: Bearer ${access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "my-destination",
    "Type": "HTTP",
    "URL": "https://api.updated.example.com",
    "Authentication": "BasicAuthentication",
    "ProxyType": "Internet",
    "User": "newuser",
    "Password": "newpassword"
  }'
```

#### Delete Destination

```bash
DELETE /subaccountDestinations/{destinationName}

curl -X DELETE "${destinationUri}/destination-configuration/v1/subaccountDestinations/my-destination" \
  -H "Authorization: Bearer ${access_token}"
```

---

### Service Instance Destinations

#### List Instance Destinations

```bash
GET /instanceDestinations

curl -X GET "${destinationUri}/destination-configuration/v1/instanceDestinations" \
  -H "Authorization: Bearer ${access_token}"
```

#### CRUD Operations

Same as subaccount destinations but using `/instanceDestinations` path.

---

### Find Destination (with Authentication)

The most commonly used endpoint - retrieves destination configuration with authentication tokens.

```bash
GET /destinations/{destinationName}

curl -X GET "${destinationUri}/destination-configuration/v1/destinations/my-destination" \
  -H "Authorization: Bearer ${access_token}"
```

**Response Structure:**
```json
{
  "owner": {
    "SubaccountId": "abc123",
    "InstanceId": null
  },
  "destinationConfiguration": {
    "Name": "my-destination",
    "Type": "HTTP",
    "URL": "https://api.example.com",
    "Authentication": "OAuth2ClientCredentials",
    "ProxyType": "Internet",
    "clientId": "...",
    "tokenServiceURL": "..."
  },
  "authTokens": [
    {
      "type": "Bearer",
      "value": "eyJhbGciOiJSUzI1NiIs...",
      "http_header": {
        "key": "Authorization",
        "value": "Bearer eyJhbGciOiJSUzI1NiIs..."
      },
      "expires_in": "43199",
      "scope": "read write"
    }
  ],
  "certificates": []
}
```

#### With User Token (Principal Propagation)

For destinations requiring user context:

```bash
curl -X GET "${destinationUri}/destination-configuration/v1/destinations/my-destination" \
  -H "Authorization: Bearer ${access_token}" \
  -H "X-user-token: ${user_jwt}"
```

#### With Destination Fragment

```bash
curl -X GET "${destinationUri}/destination-configuration/v1/destinations/my-destination" \
  -H "Authorization: Bearer ${access_token}" \
  -H "X-Fragment-Name: my-fragment"
```

---

### Certificates

#### List Certificates

```bash
GET /subaccountCertificates

curl -X GET "${destinationUri}/destination-configuration/v1/subaccountCertificates" \
  -H "Authorization: Bearer ${access_token}"
```

#### Upload Certificate

```bash
POST /subaccountCertificates

curl -X POST "${destinationUri}/destination-configuration/v1/subaccountCertificates" \
  -H "Authorization: Bearer ${access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "my-certificate",
    "Type": "CERTIFICATE",
    "Content": "base64-encoded-certificate"
  }'
```

#### Delete Certificate

```bash
DELETE /subaccountCertificates/{certificateName}

curl -X DELETE "${destinationUri}/destination-configuration/v1/subaccountCertificates/my-certificate" \
  -H "Authorization: Bearer ${access_token}"
```

---

### Destination Fragments

#### List Fragments

```bash
GET /subaccountDestinationFragments

curl -X GET "${destinationUri}/destination-configuration/v1/subaccountDestinationFragments" \
  -H "Authorization: Bearer ${access_token}"
```

#### Create Fragment

```bash
POST /subaccountDestinationFragments

curl -X POST "${destinationUri}/destination-configuration/v1/subaccountDestinationFragments" \
  -H "Authorization: Bearer ${access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "my-fragment",
    "FragmentProperties": [
      {
        "Name": "URL.headers.X-Tenant-Id",
        "Value": "tenant-123"
      }
    ]
  }'
```

#### Delete Fragment

```bash
DELETE /subaccountDestinationFragments/{fragmentName}

curl -X DELETE "${destinationUri}/destination-configuration/v1/subaccountDestinationFragments/my-fragment" \
  -H "Authorization: Bearer ${access_token}"
```

---

## Subscription-Level Destinations (Multitenancy)

For SaaS applications with tenant-specific destinations.

### Create Subscription Destination

1. Get subscriber token using provider credentials
2. Call API with subscriber context

```bash
# Get subscriber token
curl -X POST "${subscriberTokenUrl}/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  --data-urlencode "client_id=${providerClientId}" \
  --data-urlencode "client_secret=${providerClientSecret}"

# Create subscription destination
curl -X POST "${destinationUri}/destination-configuration/v1/subscriptionDestinations" \
  -H "Authorization: Bearer ${subscriber_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "tenant-destination",
    "Type": "HTTP",
    "URL": "https://tenant-api.example.com",
    "Authentication": "BasicAuthentication",
    "User": "tenant-user",
    "Password": "tenant-password"
  }'
```

---

## Pagination

For large numbers of destinations, use pagination:

```bash
GET /subaccountDestinations?$top=100&$skip=0

curl -X GET "${destinationUri}/destination-configuration/v1/subaccountDestinations?\$top=100&\$skip=0" \
  -H "Authorization: Bearer ${access_token}"
```

**Parameters:**
- `$top`: Maximum number of results (default: 100)
- `$skip`: Number of results to skip

---

## Error Handling

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | Deleted |
| 400 | Bad Request (invalid payload) |
| 401 | Unauthorized (invalid/expired token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 409 | Conflict (destination already exists) |
| 500 | Internal Server Error |

### Error Response Format

```json
{
  "ErrorMessage": "Destination with name 'my-destination' already exists."
}
```

---

## Best Practices

### Caching

- Cache access tokens for their validity period
- Cache destination configurations (3-5 minutes recommended)
- Use stale cache if refresh fails

### Retry Logic

```javascript
const retryDelays = [2000, 4000, 8000, 16000]; // ms

async function callWithRetry(fn) {
  for (let i = 0; i < retryDelays.length; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === retryDelays.length - 1) throw error;
      await sleep(retryDelays[i]);
    }
  }
}
```

### Timeouts

- Connect timeout: 2-5 seconds
- Read timeout: ~30 seconds

---

## SDK Usage

### SAP Cloud SDK (Node.js)

```javascript
const { getDestination } = require('@sap-cloud-sdk/connectivity');

// Get destination with authentication
const destination = await getDestination({
  destinationName: 'my-destination',
  jwt: userJwt  // For user propagation
});

console.log(destination.url);
console.log(destination.authTokens);
```

### SAP Cloud SDK (Java)

```java
import com.sap.cloud.sdk.cloudplatform.connectivity.DestinationAccessor;

// Get destination
Destination destination = DestinationAccessor
    .getDestination("my-destination");

String url = destination.get(DestinationProperty.URI)
    .orElseThrow();
```

---

## Documentation Links

- API Specification: [https://api.sap.com/api/SAP_CP_CF_Connectivity_Destination](https://api.sap.com/api/SAP_CP_CF_Connectivity_Destination)
- Calling the API: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/calling-destination-service-rest-api](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/calling-destination-service-rest-api)
- Multitenancy: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/multitenancy-in-destination-service](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/multitenancy-in-destination-service)

---

**Last Updated**: 2025-11-22
