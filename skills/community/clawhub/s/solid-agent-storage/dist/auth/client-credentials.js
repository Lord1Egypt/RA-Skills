/**
 * Gets an authenticated fetch function using CSS client credentials.
 *
 * CSS v7 flow:
 * 1. POST /.oidc/token with Basic auth (id:secret) and grant_type=client_credentials
 * 2. Receive a Bearer access_token (JWT, 600s expiry)
 * 3. Use Authorization: Bearer <token> on subsequent requests
 */
export async function getAuthenticatedFetch(serverUrl, id, secret) {
    const tokenUrl = `${serverUrl}/.oidc/token`;
    const authString = Buffer.from(`${id}:${secret}`).toString('base64');
    let token = null;
    let tokenExpiry = 0;
    async function refreshToken() {
        const res = await fetch(tokenUrl, {
            method: 'POST',
            headers: {
                authorization: `Basic ${authString}`,
                'content-type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                grant_type: 'client_credentials',
                scope: 'webid',
            }),
        });
        if (!res.ok) {
            throw new Error(`Failed to get access token: ${res.status} ${await res.text()}`);
        }
        const json = await res.json();
        token = json.access_token;
        // Refresh 30s before expiry
        tokenExpiry = Date.now() + (json.expires_in - 30) * 1000;
        return token;
    }
    async function getToken() {
        if (!token || Date.now() >= tokenExpiry) {
            return refreshToken();
        }
        return token;
    }
    return async (input, init) => {
        const accessToken = await getToken();
        const headers = new Headers(init?.headers);
        headers.set('authorization', `Bearer ${accessToken}`);
        return fetch(input, {
            ...init,
            headers,
        });
    };
}
//# sourceMappingURL=client-credentials.js.map