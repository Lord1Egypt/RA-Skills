# HTTP Destinations - Complete Reference

**Source**: [https://github.com/SAP-docs/btp-connectivity/blob/main/docs/1-connectivity-documentation/http-destinations-42a0e6b.md](https://github.com/SAP-docs/btp-connectivity/blob/main/docs/1-connectivity-documentation/http-destinations-42a0e6b.md)

---

## Overview

HTTP destinations define connection parameters for HTTP/HTTPS endpoints, supporting internet, on-premise, and PrivateLink connections.

---

## Required Properties

| Property | Description | Values |
|----------|-------------|--------|
| `Name` | Unique destination identifier | String (max 200 chars) |
| `Type` | Destination type | `HTTP` |
| `URL` | Target endpoint URL | Valid HTTP(S) URL |
| `ProxyType` | Connection routing | `Internet`, `OnPremise`, `PrivateLink` |
| `Authentication` | Authentication method | See Authentication Types |

---

## Proxy Types

### Internet
Direct connection to internet-accessible endpoints.
- Default proxy type
- No additional components required

### OnPremise
Connection via Cloud Connector to on-premise systems.
- Requires Cloud Connector installation
- Optional `CloudConnectorLocationId` for multiple connectors
- Also applies to VPC environments

### PrivateLink
Connection via SAP Private Link Service.
- Available for selected SAP BTP services
- Requires Private Link setup with IaaS provider

---

## Authentication Types

### No Authentication
```
Authentication: NoAuthentication
```

### Basic Authentication
```
Authentication: BasicAuthentication
User: <username>
Password: <password>
```

### Client Certificate Authentication
```
Authentication: ClientCertificateAuthentication
KeyStoreLocation: <certificate-location>
KeyStorePassword: <password>
```

### OAuth2ClientCredentials
```
Authentication: OAuth2ClientCredentials
clientId: <client-id>
clientSecret: <client-secret>
tokenServiceURL: https://auth.example.com/oauth/token
tokenServiceURLType: Dedicated | Common
```

**Optional Properties:**
- `scope`: OAuth scopes
- `tokenServiceUser` / `tokenServicePassword`: For token service basic auth
- `URL.headers.<name>`: Custom headers for target
- `URL.queries.<name>`: Custom query parameters
- `tokenService.body.<name>`: Custom token request body

### OAuth2JWTBearer
```
Authentication: OAuth2JWTBearer
clientId: <client-id>
clientSecret: <client-secret>
tokenServiceURL: https://auth.example.com/oauth/token
```

Exchanges incoming user JWT for new access token.

### OAuth2SAMLBearerAssertion
```
Authentication: OAuth2SAMLBearerAssertion
audience: <saml-audience>
clientKey: <client-key>
tokenServiceURL: https://auth.example.com/oauth2/token
KeyStoreLocation: <certificate-for-signing>
```

**Required for user propagation (cloud-to-cloud).**

**Additional Properties:**
- `nameIdFormat`: SAML NameID format
- `userIdSource`: JWT field for user ID
- `authnContextClassRef`: Authentication context class
- `assertionIssuer`: SAML assertion issuer
- `companyId`: Company identifier
- `assertionRecipient`: SAML recipient

### OAuth2Password
```
Authentication: OAuth2Password
User: <username>
Password: <password>
clientId: <client-id>
clientSecret: <client-secret>
tokenServiceURL: https://auth.example.com/oauth/token
```

**Deprecated**: Use OAuth2ClientCredentials or OAuth2SAMLBearerAssertion instead.

### OAuth2AuthorizationCode
```
Authentication: OAuth2AuthorizationCode
clientId: <client-id>
clientSecret: <client-secret>
tokenServiceURL: https://auth.example.com/oauth/token
```

For interactive user authorization flows.

### OAuth2UserTokenExchange
```
Authentication: OAuth2UserTokenExchange
clientId: <client-id>
clientSecret: <client-secret>
tokenServiceURL: https://auth.example.com/oauth/token
```

Exchanges user token for access token.

### OAuth2RefreshToken
```
Authentication: OAuth2RefreshToken
clientId: <client-id>
clientSecret: <client-secret>
tokenServiceURL: https://auth.example.com/oauth/token
refreshToken: <refresh-token>
```

Uses refresh token to obtain access tokens.

### SAMLAssertion
```
Authentication: SAMLAssertion
audience: <saml-audience>
```

For SAML assertion authentication without OAuth.

### PrincipalPropagation
```
Authentication: PrincipalPropagation
ProxyType: OnPremise
```

**Required for user propagation (cloud-to-on-premise).**
- Requires Cloud Connector configuration
- Generates X.509 certificate from user identity

---

## Optional Properties

### Connection Settings
| Property | Description | Default |
|----------|-------------|---------|
| `URL.connectionTimeoutInSeconds` | Connection timeout | 0 (system default) |
| `URL.socketReadTimeoutInSeconds` | Read timeout | 0 (system default) |

Valid ranges:
- Connection timeout: 0-60 seconds
- Socket read timeout: 0-600 seconds

### Custom Headers and Parameters
```
URL.headers.<header-name>: <value>
URL.queries.<param-name>: <value>
tokenService.headers.<header-name>: <value>
tokenService.queries.<param-name>: <value>
tokenService.body.<param-name>: <value>
```

### TLS Configuration
```
TrustStoreLocation: <truststore-location>
TrustAll: true | false
```

**Warning**: `TrustAll: true` disables certificate validation. Use only for testing.

### Cloud Connector
```
CloudConnectorLocationId: <location-id>
```

Required when multiple Cloud Connectors connect to the same subaccount.

---

## Token Service URL Types

| Type | Behavior |
|------|----------|
| `Dedicated` | Use URL as-is (default) |
| `Common` | Replace `{tenant}` placeholder with subaccount subdomain |

Example with `Common`:
```
tokenServiceURL: https://{tenant}.auth.example.com/oauth/token
```

---

## Example: Complete OAuth2ClientCredentials Destination

```json
{
  "Name": "my-api-destination",
  "Type": "HTTP",
  "URL": "https://api.example.com/v1",
  "ProxyType": "Internet",
  "Authentication": "OAuth2ClientCredentials",
  "clientId": "my-client-id",
  "clientSecret": "my-client-secret",
  "tokenServiceURL": "https://auth.example.com/oauth/token",
  "tokenServiceURLType": "Dedicated",
  "scope": "read write",
  "URL.headers.X-Custom-Header": "custom-value",
  "URL.connectionTimeoutInSeconds": "30",
  "URL.socketReadTimeoutInSeconds": "60"
}
```

---

## Example: On-Premise with Principal Propagation

```json
{
  "Name": "onprem-sap-system",
  "Type": "HTTP",
  "URL": "http://virtual-host:443/sap/opu/odata/sap/API_BUSINESS_PARTNER",
  "ProxyType": "OnPremise",
  "Authentication": "PrincipalPropagation",
  "CloudConnectorLocationId": "loc1"
}
```

---

## Documentation Links

- HTTP Destinations: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/http-destinations](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/http-destinations)
- Authentication Types: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/http-destinations#authentication](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/http-destinations#authentication)
- Destination Service API: [https://api.sap.com/api/SAP_CP_CF_Connectivity_Destination](https://api.sap.com/api/SAP_CP_CF_Connectivity_Destination)

---

**Last Updated**: 2025-11-22
