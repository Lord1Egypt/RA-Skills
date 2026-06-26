# TBC Bank Authentication & OAuth2

## OAuth2 Authorization Code Flow

### Step 1: Authorization Request

```
GET https://test-api.tbcbank.ge/psd2/openbanking/oauth/authorize
  ?response_type=code
  &client_id={client_id}
  &redirect_uri={redirect_uri}
  &scope={scope}
  &state={random_state}
  &claims=userinfo={claims_object}
```

**Scopes:**
- `openid` - OpenID Connect
- `accounts` - Account information access
- `payments` - Payment initiation
- `profile` - User profile

### Step 2: Token Exchange

```http
POST https://test-api.tbcbank.ge/openbanking/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code={auth_code}
&redirect_uri={redirect_uri}
&client_id={client_id}
&client_secret={client_secret}
```

### Step 3: Token Response

```json
{
  "access_token": "eyJhbGciOiJS...",
  "token_type": "Bearer",
  "refresh_token": "...",
  "expires_in": 3600,
  "refresh_token_expires_in": 86400,
  "scope": "openid accounts",
  "issued_at": "1672531200000"
}
```

### Refresh Token

```http
POST https://test-api.tbcbank.ge/openbanking/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&refresh_token={refresh_token}
&client_id={client_id}
&client_secret={client_secret}
```

## OAuth Discovery

```
GET https://test-api.tbcbank.ge/.well-known/oauth-authorization-server
GET https://dev-openbanking.tbcbank.ge/openbanking/oauth/.well-known/oauth-authorization-server
```

Returns full OpenID Connect discovery document with all supported endpoints.

## User Info

```http
GET https://test-api.tbcbank.ge/userinfo
Authorization: Bearer {access_token}
```

## JWT / JWKS

```
GET https://test-api.tbcbank.ge/.well-known/jwks
```

## Code Examples

### Python (requests)
```python
import requests

# Step 1: Get token
token_resp = requests.post(
    "https://test-api.tbcbank.ge/openbanking/oauth/token",
    data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "accounts"
    }
)
token = token_resp.json()["access_token"]

# Step 2: Use token
headers = {
    "Authorization": f"Bearer {token}",
    "X-Request-ID": str(uuid.uuid4()),
    "PSU-IP-Address": "192.168.1.1"
}
```

### Node.js
```javascript
const axios = require('axios');

const getToken = async () => {
  const response = await axios.post(
    'https://test-api.tbcbank.ge/openbanking/oauth/token',
    new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: process.env.CLIENT_ID,
      client_secret: process.env.CLIENT_SECRET,
      scope: 'accounts'
    }),
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  );
  return response.data.access_token;
};
```

### Ruby
```ruby
require 'net/http'
require 'uri'

uri = URI.parse('https://test-api.tbcbank.ge/psd2/openbanking/oauth/authorize?claims=userinfo=[object Object]')
response = Net::HTTP.get_response(uri)
```

## Mutual TLS (mTLS)

For TPP certificate-based authentication, present client certificate alongside token:

```python
requests.get(url, cert=('/path/to/client.crt', '/path/to/client.key'))
```

## Request Signing

For signed requests, include:
```
Digest: SHA-256={base64(sha256(request_body))}
Signature: keyId="{cert_serial_number}",
           algorithm="rsa-sha256",
           headers="(request-target) host date digest x-request-id",
           signature="{base64_rsa_signature}"
```
