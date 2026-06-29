# SoundCloud OAuth 2.0 Authentication Guide

## Overview

SoundCloud uses OAuth 2.0 for authenticated API access. This guide covers the complete authentication flow for obtaining access tokens to perform user-specific actions like creating playlists, liking tracks, and accessing private data.

## Prerequisites

### 1. Create a SoundCloud Application
1. Go to https://soundcloud.com/you/apps
2. Click "Register a new application"
3. Fill in:
   - **App name:** Your application name
   - **Website:** Your app's website
   - **Redirect URI:** `http://localhost:8080/callback` (for development)
4. Save to get your **Client ID** and **Client Secret**

### 2. Required Credentials
```bash
# Environment variables to set
export SOUNDCLOUD_CLIENT_ID="your_client_id"
export SOUNDCLOUD_CLIENT_SECRET="your_client_secret"
```

## OAuth 2.0 Flow

### Authorization Code Flow (Recommended)

#### Step 1: Authorization Request
Direct user to SoundCloud's authorization endpoint:

```
GET https://soundcloud.com/connect
```

**Required Parameters:**
- `client_id` - Your application's client ID
- `redirect_uri` - Must match registered redirect URI
- `response_type` - `code`
- `scope` - `non-expiring` (for permanent access)
- `state` - Optional CSRF protection token

**Example URL:**
```
https://soundcloud.com/connect?
  client_id=YOUR_CLIENT_ID&
  redirect_uri=http://localhost:8080/callback&
  response_type=code&
  scope=non-expiring&
  state=random_string_123
```

#### Step 2: User Authorization
User will see SoundCloud's authorization screen asking to:
- Allow your app to access their account
- See the permissions requested (based on scope)

#### Step 3: Authorization Code
After user approves, SoundCloud redirects to your `redirect_uri` with:
```
http://localhost:8080/callback?code=AUTHORIZATION_CODE&state=random_string_123
```

#### Step 4: Exchange Code for Token
Exchange the authorization code for an access token:

```bash
curl -X POST "https://api.soundcloud.com/oauth2/token" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=http://localhost:8080/callback" \
  -d "code=AUTHORIZATION_CODE"
```

**Response:**
```json
{
  "access_token": "YOUR_ACCESS_TOKEN",
  "expires_in": 21599,
  "scope": "non-expiring",
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

#### Step 5: Use Access Token
Include token in API requests:
```bash
curl -X GET "https://api.soundcloud.com/me" \
  -H "Authorization: OAuth YOUR_ACCESS_TOKEN"
```

## Scopes

### Available Scopes

| Scope | Description | Permissions |
|-------|-------------|-------------|
| `*` (wildcard) | All permissions | Full access |
| `non-expiring` | Permanent access | All permissions, token doesn't expire |
| No scope | Default scope | Basic read access |

### Scope Recommendations

- **For most applications:** Use `non-expiring` scope
- **For read-only apps:** No scope needed (client_id only)
- **For specific permissions:** Use wildcard `*` (least privilege)

## Token Management

### Access Token Lifespan
- **With `non-expiring` scope:** Token never expires
- **Without scope:** Token expires in 6 hours
- **Default:** Token expires in 6 hours

### Refresh Tokens
Only provided when using `non-expiring` scope.

**Refresh expired token:**
```bash
curl -X POST "https://api.soundcloud.com/oauth2/token" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=YOUR_REFRESH_TOKEN"
```

### Token Storage Best Practices

#### Secure Storage
```bash
# DO NOT hardcode tokens in scripts
# DO NOT commit tokens to version control
# DO store in environment variables or secure vault

# Good practice: Use .env file (add to .gitignore)
echo "SOUNDCLOUD_ACCESS_TOKEN=your_token" >> .env
```

#### Environment Setup Script
```bash
#!/bin/bash
# setup_env.sh

read -sp "Enter SoundCloud Client ID: " client_id
echo
read -sp "Enter SoundCloud Client Secret: " client_secret
echo

# Save to .env file
cat > .env << EOF
SOUNDCLOUD_CLIENT_ID=$client_id
SOUNDCLOUD_CLIENT_SECRET=$client_secret
EOF

echo "Environment variables saved to .env"
```

## Simplified Authentication Scripts

### 1. Complete OAuth Flow Script

```bash
#!/bin/bash
# auth_soundcloud.sh

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check for required variables
if [ -z "$SOUNDCLOUD_CLIENT_ID" ] || [ -z "$SOUNDCLOUD_CLIENT_SECRET" ]; then
    echo "Error: Missing client ID or secret"
    echo "Please create .env file with:"
    echo "SOUNDCLOUD_CLIENT_ID=your_id"
    echo "SOUNDCLOUD_CLIENT_SECRET=your_secret"
    exit 1
fi

# Generate state for CSRF protection
STATE=$(openssl rand -hex 16)
REDIRECT_URI="http://localhost:8080/callback"

# Step 1: Generate authorization URL
AUTH_URL="https://soundcloud.com/connect?client_id=${SOUNDCLOUD_CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=non-expiring&state=${STATE}"

echo "========================================="
echo "SoundCloud OAuth Authentication"
echo "========================================="
echo ""
echo "1. Open this URL in your browser:"
echo "$AUTH_URL"
echo ""
echo "2. Authorize the application"
echo "3. You will be redirected to localhost:8080"
echo "4. Copy the 'code' parameter from the URL"
echo ""
echo "========================================="

# Start temporary HTTP server to catch redirect
echo "Starting temporary server on port 8080..."
echo "Press Ctrl+C after you get the authorization code"
echo ""

# Simple Python server to catch redirect
python3 -m http.server 8080 --directory /tmp 2>/dev/null &
SERVER_PID=$!

# Wait for user to get code
read -p "Paste the authorization code here: " AUTH_CODE

# Kill the server
kill $SERVER_PID 2>/dev/null

# Step 2: Exchange code for token
echo ""
echo "Exchanging code for access token..."

RESPONSE=$(curl -s -X POST "https://api.soundcloud.com/oauth2/token" \
  -d "client_id=${SOUNDCLOUD_CLIENT_ID}" \
  -d "client_secret=${SOUNDCLOUD_CLIENT_SECRET}" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=${REDIRECT_URI}" \
  -d "code=${AUTH_CODE}")

# Parse response
if echo "$RESPONSE" | jq -e '.access_token' >/dev/null 2>&1; then
    ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
    REFRESH_TOKEN=$(echo "$RESPONSE" | jq -r '.refresh_token // empty')
    
    echo "========================================="
    echo "Authentication Successful!"
    echo "========================================="
    echo ""
    echo "Access Token: ${ACCESS_TOKEN:0:20}..."
    if [ -n "$REFRESH_TOKEN" ]; then
        echo "Refresh Token: ${REFRESH_TOKEN:0:20}..."
    fi
    echo ""
    echo "Add to your environment:"
    echo "export SOUNDCLOUD_ACCESS_TOKEN=\"$ACCESS_TOKEN\""
    
    # Save to .env file
    echo "SOUNDCLOUD_ACCESS_TOKEN=$ACCESS_TOKEN" >> .env
    if [ -n "$REFRESH_TOKEN" ]; then
        echo "SOUNDCLOUD_REFRESH_TOKEN=$REFRESH_TOKEN" >> .env
    fi
    
    echo ""
    echo "Tokens saved to .env file"
else
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.error_description // .error // "Unknown error"')
    echo "Error: $ERROR_MSG"
    exit 1
fi
```

### 2. Token Validation Script

```bash
#!/bin/bash
# validate_token.sh

set -e

if [ -z "$SOUNDCLOUD_ACCESS_TOKEN" ]; then
    echo "Error: SOUNDCLOUD_ACCESS_TOKEN not set"
    exit 1
fi

echo "Validating access token..."

RESPONSE=$(curl -s -X GET "https://api.soundcloud.com/me" \
  -H "Authorization: OAuth ${SOUNDCLOUD_ACCESS_TOKEN}")

if echo "$RESPONSE" | jq -e '.id' >/dev/null 2>&1; then
    USERNAME=$(echo "$RESPONSE" | jq -r '.username')
    USER_ID=$(echo "$RESPONSE" | jq -r '.id')
    
    echo "✓ Token is valid"
    echo "  User: $USERNAME (ID: $USER_ID)"
    echo "  Permissions: Full access"
else
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.error // "Invalid token"')
    echo "✗ Token validation failed: $ERROR_MSG"
    exit 1
fi
```

## Common Authentication Issues

### 1. "Invalid client identifier"
- Client ID is incorrect or not registered
- Check at https://soundcloud.com/you/apps

### 2. "Invalid redirect URI"
- Redirect URI doesn't match registered URI
- Ensure exact match including protocol (http/https)

### 3. "Invalid authorization code"
- Code has expired (codes expire quickly)
- Code was already used
- Generate new authorization code

### 4. "Invalid scope"
- Requested scope not approved for your app
- Use `non-expiring` or no scope

### 5. Rate Limiting
- Too many authentication attempts
- Wait before retrying

## Security Considerations

### 1. Client Secret Protection
- Never expose client secret in client-side code
- Store server-side only
- Use environment variables or secure vault

### 2. Token Security
- Access tokens are equivalent to passwords
- Transmit over HTTPS only
- Store encrypted at rest
- Rotate tokens periodically

### 3. Redirect URI Validation
- Use exact redirect URIs
- Avoid open redirects
- Validate state parameter

### 4. CSRF Protection
- Always use `state` parameter
- Validate state on callback
- Generate cryptographically random state

## Testing Authentication

### Local Development Setup

#### 1. Create Test Application
```bash
# Register test app at soundcloud.com/you/apps
# Use redirect: http://localhost:8080/callback
```

#### 2. Set Up Environment
```bash
# Create .env file
cat > .env << EOF
SOUNDCLOUD_CLIENT_ID=test_client_id
SOUNDCLOUD_CLIENT_SECRET=test_client_secret
EOF

# Source environment
source .env
```

#### 3. Run Authentication
```bash
# Make script executable
chmod +x auth_soundcloud.sh

# Run authentication
./auth_soundcloud.sh
```

#### 4. Test API Access
```bash
# Test with user info
curl -X GET "https://api.soundcloud.com/me" \
  -H "Authorization: OAuth ${SOUNDCLOUD_ACCESS_TOKEN}"

# Test with playlist creation
curl -X POST "https://api.soundcloud.com/playlists" \
  -H "Authorization: OAuth ${SOUNDCLOUD_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"playlist": {"title": "Test Playlist", "sharing": "public"}}'
```

## Production Deployment

### 1. Update Redirect URI
- Change from `localhost` to your production domain
- Update in SoundCloud app settings
- Update in your application code

### 2. Secure Storage
- Use AWS Secrets Manager, HashiCorp Vault, or similar
- Never commit secrets to version control
- Use different secrets for different environments

### 3. Monitoring
- Log authentication attempts
- Monitor token usage
- Set up alerts for failed authentications

### 4. Token Rotation
- Implement token refresh logic
- Handle token expiration gracefully
- Provide re-authentication flow

## Troubleshooting

### Debugging Tips

#### 1. Enable Verbose Output
```bash
curl -v -X POST "https://api.soundcloud.com/oauth2/token" \
  -d "client_id=..." \
  -d "client_secret=..." \
  -d "grant_type=authorization_code" \
  -d "code=..."
```

#### 2. Check Response Headers
```bash
curl -I -X GET "https://api.soundcloud.com/me" \
  -H "Authorization: OAuth ..."
```

#### 3. Validate JSON Responses
```bash
# Pipe through jq for pretty printing
curl ... | jq .
```

#### 4. Test with Different Scopes
- Try without scope first
- Then try with `non-expiring`
- Compare permissions

### Common Solutions

#### "Token doesn't work for certain endpoints"
- Check if endpoint requires specific permissions
- Verify token has required scope
- Some endpoints require Pro/Enterprise access

#### "Authentication works locally but not in production"
- Check redirect URI matches exactly
- Verify environment variables are set
- Check firewall/network restrictions

#### "Getting 403 Forbidden"
- Token may have expired
- User may have revoked permissions
- App may be in development mode

## Additional Resources

- [Official OAuth Documentation](https://developers.soundcloud.com/docs/api/authentication)
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [SoundCloud API Forum](https://community.soundcloud.com/c/developers)
- [API Status](https://status.soundcloud.com/)