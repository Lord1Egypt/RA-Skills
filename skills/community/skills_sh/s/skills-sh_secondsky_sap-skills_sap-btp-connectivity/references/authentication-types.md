# Authentication Types - Complete Reference

**Source**: [https://github.com/SAP-docs/btp-connectivity/tree/main/docs/1-connectivity-documentation](https://github.com/SAP-docs/btp-connectivity/tree/main/docs/1-connectivity-documentation)

---

## Overview

SAP BTP Destination Service supports 17+ authentication types for HTTP destinations, covering various OAuth flows, certificate-based authentication, and principal propagation.

---

## Authentication Type Summary

| Type | Use Case | User Context |
|------|----------|--------------|
| `NoAuthentication` | Public APIs | No |
| `BasicAuthentication` | Simple credentials | Technical |
| `ClientCertificateAuthentication` | X.509 certificates | Technical |
| `OAuth2ClientCredentials` | Service-to-service | Technical |
| `OAuth2Password` | Legacy password flow | Technical |
| `OAuth2JWTBearer` | Token exchange | Business User |
| `OAuth2SAMLBearerAssertion` | Cloud-to-cloud propagation | Business User |
| `OAuth2UserTokenExchange` | User token exchange | Business User |
| `OAuth2TokenExchange` | Generic token exchange | Business User |
| `OAuth2TechnicalUserPropagation` | Technical user via OAuth | Technical |
| `OAuth2RefreshToken` | Refresh token flow | Depends |
| `OAuth2AuthorizationCode` | Interactive authorization | Business User |
| `SAMLAssertion` | SAML without OAuth | Business User |
| `PrincipalPropagation` | Cloud-to-on-premise SSO | Business User |
| `ServerCertificateAuthentication` | Server certificates | Technical |

---

## NoAuthentication

No authentication required for the target endpoint.

```json
{
  "Name": "public-api",
  "Type": "HTTP",
  "URL": "https://api.public.example.com",
  "ProxyType": "Internet",
  "Authentication": "NoAuthentication"
}
```

---

## BasicAuthentication

Username and password authentication.

```json
{
  "Name": "basic-auth-destination",
  "Type": "HTTP",
  "URL": "https://api.example.com",
  "ProxyType": "Internet",
  "Authentication": "BasicAuthentication",
  "User": "username",
  "Password": "password"
}
```

**Properties:**
| Property | Required | Description |
|----------|----------|-------------|
| `User` | Yes | Username |
| `Password` | Yes | Password |

---

## ClientCertificateAuthentication

X.509 client certificate authentication.

```json
{
  "Name": "cert-auth-destination",
  "Type": "HTTP",
  "URL": "https://api.example.com",
  "ProxyType": "Internet",
  "Authentication": "ClientCertificateAuthentication",
  "KeyStoreLocation": "cert.p12",
  "KeyStorePassword": "keystorepassword"
}
```

**Properties:**
| Property | Required | Description |
|----------|----------|-------------|
| `KeyStoreLocation` | Yes | Certificate location in Destination Service |
| `KeyStorePassword` | Yes | Keystore password |

---

## OAuth2ClientCredentials

OAuth 2.0 client credentials flow for service-to-service communication.

```json
{
  "Name": "oauth-cc-destination",
  "Type": "HTTP",
  "URL": "https://api.example.com",
  "ProxyType": "Internet",
  "Authentication": "OAuth2ClientCredentials",
  "clientId": "my-client-id",
  "clientSecret": "my-client-secret",
  "tokenServiceURL": "https://auth.example.com/oauth/token"
}
```

**Required Properties:**
| Property | Description |
|----------|-------------|
| `clientId` | OAuth client ID |
| `clientSecret` | OAuth client secret |
| `tokenServiceURL` | Token endpoint URL |

**Optional Properties:**
| Property | Description |
|----------|-------------|
| `tokenServiceURLType` | `Dedicated` (default) or `Common` (multi-tenant) |
| `scope` | OAuth scopes (space-separated) |
| `tokenServiceUser` | User for token service basic auth |
| `tokenServicePassword` | Password for token service basic auth |

**Token Caching**: Automatic caching with auto-renewal before expiration.

---

## OAuth2JWTBearer

Exchanges incoming user JWT for new access token.

```json
{
  "Name": "oauth-jwt-bearer",
  "Type": "HTTP",
  "URL": "https://api.example.com",
  "ProxyType": "Internet",
  "Authentication": "OAuth2JWTBearer",
  "clientId": "my-client-id",
  "clientSecret": "my-client-secret",
  "tokenServiceURL": "https://auth.example.com/oauth/token"
}
```

**Required Properties:**
| Property | Description |
|----------|-------------|
| `clientId` | OAuth client ID |
| `clientSecret` | OAuth client secret |
| `tokenServiceURL` | Token endpoint URL |

**Requires**: User JWT in request context (e.g., from XSUAA).

---

## OAuth2SAMLBearerAssertion

OAuth 2.0 SAML Bearer Assertion flow for user propagation between cloud systems.

```json
{
  "Name": "oauth-saml-bearer",
  "Type": "HTTP",
  "URL": "https://api.successfactors.com",
  "ProxyType": "Internet",
  "Authentication": "OAuth2SAMLBearerAssertion",
  "audience": "www.successfactors.com",
  "clientKey": "my-client-key",
  "tokenServiceURL": "https://api.successfactors.com/oauth/token",
  "KeyStoreLocation": "signing-cert.p12",
  "KeyStorePassword": "password"
}
```

**Required Properties:**
| Property | Description |
|----------|-------------|
| `audience` | SAML assertion audience |
| `clientKey` | Client identifier for authorization server |
| `tokenServiceURL` | Token endpoint URL |
| `KeyStoreLocation` | Certificate for SAML signing |
| `KeyStorePassword` | Keystore password |

**Optional Properties:**
| Property | Description |
|----------|-------------|
| `nameIdFormat` | SAML NameID format |
| `userIdSource` | JWT field for user ID extraction |
| `authnContextClassRef` | Authentication context class |
| `assertionIssuer` | SAML issuer |
| `assertionRecipient` | SAML recipient |
| `companyId` | Company identifier |

**User ID Resolution Order:**
1. `SystemUser` property (deprecated)
2. JWT field via `userIdSource` or `nameIdFormat`
3. Custom user attributes from IdP

---

## OAuth2Password

OAuth 2.0 Resource Owner Password flow.

```json
{
  "Name": "oauth-password",
  "Type": "HTTP",
  "URL": "https://api.example.com",
  "ProxyType": "Internet",
  "Authentication": "OAuth2Password",
  "User": "username",
  "Password": "password",
  "clientId": "my-client-id",
  "clientSecret": "my-client-secret",
  "tokenServiceURL": "https://auth.example.com/oauth/token"
}
```

**Deprecation Warning**: This flow is deprecated. Use `OAuth2ClientCredentials` or `OAuth2SAMLBearerAssertion` instead.

---

## OAuth2UserTokenExchange

Exchanges user token for new access token.

```json
{
  "Name": "oauth-ute",
  "Type": "HTTP",
  "URL": "https://api.example.com",
  "ProxyType": "Internet",
  "Authentication": "OAuth2UserTokenExchange",
  "clientId": "my-client-id",
  "clientSecret": "my-client-secret",
  "tokenServiceURL": "https://auth.example.com/oauth/token"
}
```

**Requires**: User token in request context.

---

## OAuth2TokenExchange

Generic OAuth 2.0 Token Exchange (RFC 8693).

```json
{
  "Name": "oauth-token-exchange",
  "Type": "HTTP",
  "URL": "https://api.example.com",
  "ProxyType": "Internet",
  "Authentication": "OAuth2TokenExchange",
  "clientId": "my-client-id",
  "clientSecret": "my-client-secret",
  "tokenServiceURL": "https://auth.example.com/oauth/token"
}
```

---

## OAuth2TechnicalUserPropagation

Propagates technical user identity via OAuth.

```json
{
  "Name": "oauth-tech-user",
  "Type": "HTTP",
  "URL": "https://api.example.com",
  "ProxyType": "Internet",
  "Authentication": "OAuth2TechnicalUserPropagation",
  "clientId": "my-client-id",
  "clientSecret": "my-client-secret",
  "tokenServiceURL": "https://auth.example.com/oauth/token"
}
```

---

## OAuth2RefreshToken

Uses refresh token to obtain access tokens.

```json
{
  "Name": "oauth-refresh",
  "Type": "HTTP",
  "URL": "https://api.example.com",
  "ProxyType": "Internet",
  "Authentication": "OAuth2RefreshToken",
  "clientId": "my-client-id",
  "clientSecret": "my-client-secret",
  "tokenServiceURL": "https://auth.example.com/oauth/token",
  "refreshToken": "stored-refresh-token"
}
```

---

## OAuth2AuthorizationCode

OAuth 2.0 Authorization Code flow for interactive authorization.

```json
{
  "Name": "oauth-auth-code",
  "Type": "HTTP",
  "URL": "https://api.example.com",
  "ProxyType": "Internet",
  "Authentication": "OAuth2AuthorizationCode",
  "clientId": "my-client-id",
  "clientSecret": "my-client-secret",
  "tokenServiceURL": "https://auth.example.com/oauth/token"
}
```

---

## SAMLAssertion

SAML assertion authentication without OAuth token exchange.

```json
{
  "Name": "saml-destination",
  "Type": "HTTP",
  "URL": "https://api.example.com",
  "ProxyType": "Internet",
  "Authentication": "SAMLAssertion",
  "audience": "target-audience"
}
```

---

## PrincipalPropagation

Cloud-to-on-premise user identity propagation via Cloud Connector.

```json
{
  "Name": "onprem-pp-destination",
  "Type": "HTTP",
  "URL": "http://virtual-host:443/api",
  "ProxyType": "OnPremise",
  "Authentication": "PrincipalPropagation"
}
```

**Requirements:**
1. Cloud Connector installed and configured
2. Subject pattern configured in Cloud Connector
3. Trust established between Cloud Connector and on-premise system
4. User JWT in request context

**How It Works:**
1. Application sends request with user JWT
2. Connectivity Service forwards to Cloud Connector
3. Cloud Connector generates X.509 certificate from user identity
4. Certificate used for on-premise system authentication

---

## Client Assertion

Alternative to client secret for OAuth flows using SAML or JWT assertions.

### SAML Client Assertion
```json
{
  "Authentication": "OAuth2ClientCredentials",
  "clientId": "my-client-id",
  "tokenServiceURL": "https://auth.example.com/oauth/token",
  "clientAssertion.type": "urn:ietf:params:oauth:client-assertion-type:saml2-bearer",
  "clientAssertion.destinationName": "saml-provider-destination"
}
```

### JWT Client Assertion
```json
{
  "Authentication": "OAuth2ClientCredentials",
  "clientId": "my-client-id",
  "tokenServiceURL": "https://auth.example.com/oauth/token",
  "clientAssertion.type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
  "clientAssertion.destinationName": "jwt-provider-destination"
}
```

---

## X.509 Certificate Authentication with OAuth

Combine OAuth flows with X.509 client certificate for token service.

```json
{
  "Authentication": "OAuth2ClientCredentials",
  "clientId": "my-client-id",
  "tokenServiceURL": "https://auth.example.com/oauth/token",
  "tokenService.KeyStoreLocation": "cert.p12",
  "tokenService.KeyStorePassword": "password"
}
```

---

## Decision Guide

### Service-to-Service (No User Context)
→ `OAuth2ClientCredentials`

### User Propagation (Cloud-to-Cloud)
→ `OAuth2SAMLBearerAssertion` or `OAuth2JWTBearer`

### User Propagation (Cloud-to-On-Premise)
→ `PrincipalPropagation`

### Simple Credentials
→ `BasicAuthentication`

### Certificate-Based
→ `ClientCertificateAuthentication`

### Public API
→ `NoAuthentication`

---

## Documentation Links

- Authentication Types Overview: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/http-destinations#authentication](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/http-destinations#authentication)
- OAuth2SAMLBearerAssertion: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/oauth-saml-bearer-assertion-authentication](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/oauth-saml-bearer-assertion-authentication)
- OAuth2ClientCredentials: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/oauth-client-credentials-authentication](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/oauth-client-credentials-authentication)
- Principal Propagation: [https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/principal-propagation](https://help.sap.com/docs/connectivity/sap-btp-connectivity-cf/principal-propagation)

---

**Last Updated**: 2025-11-22
