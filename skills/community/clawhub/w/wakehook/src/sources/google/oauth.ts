/**
 * Google OAuth 2.0 token handling. The one-time `auth` CLI mints the refresh
 * token; at runtime we transparently refresh the access token as it nears expiry.
 *
 * NOTE: publish the OAuth app to "In Production" (still unverified, 100-user cap)
 * so the refresh token does not expire after 7 days (the "Testing" default).
 */
import type { GoogleHealthConfig } from "../../config.ts";
import type { Store, TokenRow } from "../../db.ts";

const TOKEN_URL = "https://oauth2.googleapis.com/token";
const AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth";
const SKEW_MS = 60_000; // refresh a minute early

interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  expires_in: number; // seconds
}

/** Build the consent URL for the one-time authorization (offline → refresh token). */
export function buildAuthUrl(cfg: GoogleHealthConfig, state: string): string {
  const p = new URLSearchParams({
    client_id: cfg.clientId,
    redirect_uri: cfg.redirectUri,
    response_type: "code",
    access_type: "offline",
    prompt: "consent",
    // NOTE: do NOT set include_granted_scopes — for the new Google Health API it
    // produces a malformed (HTTP 400) request when the account already holds
    // legacy googlehealth/fitness grants (mixed-scope token). Request only ours.
    scope: cfg.scopes.join(" "),
    state,
  });
  return `${AUTH_URL}?${p.toString()}`;
}

/** Exchange an authorization code for tokens (used by the auth CLI). */
export async function exchangeCode(
  cfg: GoogleHealthConfig,
  code: string,
): Promise<TokenResponse> {
  const res = await fetch(TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: cfg.clientId,
      client_secret: cfg.clientSecret,
      redirect_uri: cfg.redirectUri,
      grant_type: "authorization_code",
      code,
    }),
  });
  if (!res.ok) throw new Error(`token exchange failed: ${res.status} ${await res.text()}`);
  return (await res.json()) as TokenResponse;
}

async function refresh(cfg: GoogleHealthConfig, refreshToken: string): Promise<TokenResponse> {
  const res = await fetch(TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: cfg.clientId,
      client_secret: cfg.clientSecret,
      grant_type: "refresh_token",
      refresh_token: refreshToken,
    }),
  });
  if (!res.ok) throw new Error(`token refresh failed: ${res.status} ${await res.text()}`);
  return (await res.json()) as TokenResponse;
}

/** Return a currently-valid access token for `user`, refreshing if needed. */
export async function getValidAccessToken(
  cfg: GoogleHealthConfig,
  store: Store,
  user: string,
  now: () => number = Date.now,
): Promise<string> {
  // Single-user convenience: the auth CLI mints a token before the real
  // healthUserId is known (stored under a placeholder). Fall back to the sole
  // stored token and re-key it under the real user the first time we see it.
  let row = store.getToken(user) ?? store.getSoleToken();
  if (!row) throw new Error(`no stored token for user ${user}; run "bun run auth" first`);
  if (row.user !== user) {
    row = { ...row, user };
    store.upsertToken(row);
  }

  if (row.expires_at - SKEW_MS > now()) return row.access_token;

  const refreshed = await refresh(cfg, row.refresh_token);
  const updated: TokenRow = {
    user,
    access_token: refreshed.access_token,
    // Google may omit refresh_token on refresh; keep the existing one.
    refresh_token: refreshed.refresh_token ?? row.refresh_token,
    expires_at: now() + refreshed.expires_in * 1000,
  };
  store.upsertToken(updated);
  return updated.access_token;
}
