# QuickBooks Online API Authentication & Authorization Reference

## OAuth 2.0 Authorization Flow

QuickBooks Online uses OAuth 2.0 to secure all API endpoints. The authorization flow is a standard Authorization Code Grant with Refresh Tokens.

### Step 1: Authorization Request
Redirect the user to the Intuit Authorization endpoint with the following query parameters:
*   `client_id`: Your app's Client ID.
*   `response_type`: Must be `code`.
*   `scope`: Space-separated list of scopes (e.g., `com.intuit.quickbooks.accounting`).
*   `redirect_uri`: Whitelisted callback URL.
*   `state`: Unique CSRF token.

```
https://appcenter.intuit.com/connect/oauth2?client_id=YOUR_CLIENT_ID&response_type=code&scope=com.intuit.quickbooks.accounting&redirect_uri=YOUR_REDIRECT_URI&state=YOUR_STATE
```

### Step 2: Token Exchange
Exchange the authorization code for access and refresh tokens by making a POST request:
*   **Endpoint:** `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer`
*   **Headers:**
    *   `Authorization`: `Basic <Base64(client_id:client_secret)>`
    *   `Content-Type`: `application/x-www-form-urlencoded`
*   **Body:**
    ```
    grant_type=authorization_code&code=AUTHORIZATION_CODE&redirect_uri=YOUR_REDIRECT_URI
    ```

### Step 3: Refreshing Tokens
Access tokens expire after **60 minutes**. Refresh tokens expire after **100 days**.
*   **Endpoint:** `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer`
*   **Body:**
    ```
    grant_type=refresh_token&refresh_token=YOUR_REFRESH_TOKEN
    ```

## Token Storage Best Practices
*   **Encryption:** Encrypt both `access_token` and `refresh_token` at rest using AES-256-GCM.
*   **Locking:** Use a distributed lock (e.g., Redis Redlock) during token refresh to prevent concurrent workers from refreshing the same token simultaneously and causing race conditions.
*   **Overwriting:** Always overwrite the stored refresh token with the newly returned value, as Intuit may rotate refresh tokens dynamically.
