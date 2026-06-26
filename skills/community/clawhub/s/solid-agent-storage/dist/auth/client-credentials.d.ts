/**
 * Gets an authenticated fetch function using CSS client credentials.
 *
 * CSS v7 flow:
 * 1. POST /.oidc/token with Basic auth (id:secret) and grant_type=client_credentials
 * 2. Receive a Bearer access_token (JWT, 600s expiry)
 * 3. Use Authorization: Bearer <token> on subsequent requests
 */
export declare function getAuthenticatedFetch(serverUrl: string, id: string, secret: string): Promise<typeof fetch>;
