/**
 * XO Protocol — Quick Start Example
 *
 * Demonstrates the OAuth 2.0 Authorization Code Flow:
 * 1. Generate an authorization URL
 * 2. Exchange the auth code for tokens
 * 3. Call the Dating Intelligence API (scores, tiers, verification — no PII)
 *
 * Prerequisites:
 *   - An XO Protocol API key
 *   - OAuth client credentials (client_id + client_secret)
 *   - Node.js 18+
 *
 * Usage:
 *   node quickstart.js
 */

const API_BASE = "https://protocol.xoxo.space";
const API_KEY = "your-api-key";
const CLIENT_ID = "your_client_id";
const CLIENT_SECRET = "your_client_secret";
const REDIRECT_URI = "https://yourapp.com/callback";

// Step 1: Generate the authorization URL
// Redirect the user to this URL in a browser
function getAuthorizationUrl(state) {
  const params = new URLSearchParams({
    client_id: CLIENT_ID,
    redirect_uri: REDIRECT_URI,
    scope: "identity,connections,reputation",
    state: state,
    response_type: "code",
  });
  return `https://xoxo.space/en/oauth/authorize?${params}`;
}

// Step 2: Exchange the authorization code for tokens
async function exchangeCodeForToken(code) {
  const res = await fetch(`${API_BASE}/protocol/v1/auth/token`, {
    method: "POST",
    headers: {
      "X-API-Key": API_KEY,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      grant_type: "authorization_code",
      code,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      redirect_uri: REDIRECT_URI,
    }),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(`Token exchange failed: ${error.detail || error.title}`);
  }

  return res.json();
}

// Step 3: Call the API
async function getIdentity(accessToken) {
  const res = await fetch(`${API_BASE}/protocol/v1/identity/verify`, {
    headers: {
      "X-API-Key": API_KEY,
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(`API call failed: ${error.detail || error.title}`);
  }

  return res.json();
}

async function getConnections(accessToken, limit = 10) {
  const res = await fetch(
    `${API_BASE}/protocol/v1/connections/search?limit=${limit}`,
    {
      headers: {
        "X-API-Key": API_KEY,
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (!res.ok) {
    const error = await res.json();
    throw new Error(`API call failed: ${error.detail || error.title}`);
  }

  return res.json();
}

async function getReputation(accessToken, token = "me") {
  const res = await fetch(
    `${API_BASE}/protocol/v1/reputation/${token}`,
    {
      headers: {
        "X-API-Key": API_KEY,
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (!res.ok) {
    const error = await res.json();
    throw new Error(`API call failed: ${error.detail || error.title}`);
  }

  return res.json();
}

// --- Demo ---
async function main() {
  // Generate auth URL (redirect user here in your app)
  const state = Math.random().toString(36).substring(2);
  const authUrl = getAuthorizationUrl(state);
  console.log("1. Redirect user to:\n", authUrl);
  console.log();

  // After user authorizes, you'll receive a code at your redirect_uri
  // For this demo, replace with the actual code you received:
  const code = "PASTE_YOUR_AUTH_CODE_HERE";

  if (code === "PASTE_YOUR_AUTH_CODE_HERE") {
    console.log("2. After authorization, paste the code from the redirect URL");
    console.log("   and run this script again.");
    return;
  }

  // Exchange code for token
  console.log("2. Exchanging code for token...");
  const tokenResponse = await exchangeCodeForToken(code);
  console.log("   Token type:", tokenResponse.token_type);
  console.log("   Expires in:", tokenResponse.expires_in, "seconds");
  console.log("   Scope:", tokenResponse.scope);
  console.log();

  const { access_token } = tokenResponse;

  // Get identity
  console.log("3. Fetching identity...");
  const identity = await getIdentity(access_token);
  console.log("   Verified:", identity.verified);
  console.log("   Trust score:", identity.trust_score);
  console.log("   Has SBT:", identity.has_minted_sbt);
  console.log();

  // Get connections
  console.log("4. Searching connections...");
  const connections = await getConnections(access_token, 5);
  console.log("   Found:", connections.total, "connections");
  for (const c of connections.connections) {
    console.log(
      `   - ${c.tmp_id} (compatibility: ${c.compatibility_score}, verified: ${c.verified})`
    );
  }
  console.log();

  // Get reputation
  console.log("5. Fetching reputation...");
  const reputation = await getReputation(access_token);
  console.log("   Tier:", reputation.tier);
  console.log("   Score:", reputation.reputation_score);
}

main().catch(console.error);
