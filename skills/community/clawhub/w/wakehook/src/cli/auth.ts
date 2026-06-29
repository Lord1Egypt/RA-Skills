#!/usr/bin/env bun
/**
 * One-time authorization: opens the consent flow, captures the redirect on a
 * temporary local listener, exchanges the code, and stores the refresh token.
 *
 *   bun run auth
 *
 * The adapter server should NOT be running on the redirect port while you do this.
 */
import { loadConfig } from "../config.ts";
import { Store } from "../db.ts";
import { buildAuthUrl, exchangeCode } from "../sources/google/oauth.ts";

const cfg = loadConfig();
if (!cfg.google.clientId || !cfg.google.clientSecret) {
  console.error("Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET (env or config.json) first.");
  process.exit(1);
}

const store = new Store(cfg.dbPath);
const redirect = new URL(cfg.google.redirectUri);
const state = crypto.randomUUID();
const authUrl = buildAuthUrl(cfg.google, state);

console.log("\nOpen this URL in your browser and approve access:\n");
console.log(authUrl + "\n");

const server = Bun.serve({
  port: Number(redirect.port || 80),
  hostname: redirect.hostname,
  async fetch(req) {
    const url = new URL(req.url);
    if (url.pathname !== redirect.pathname) return new Response("not found", { status: 404 });
    if (url.searchParams.get("state") !== state) return new Response("bad state", { status: 400 });
    const code = url.searchParams.get("code");
    if (!code) return new Response("missing code", { status: 400 });

    try {
      const tok = await exchangeCode(cfg.google, code);
      if (!tok.refresh_token) {
        return new Response(
          "No refresh_token returned. Revoke prior access and retry (prompt=consent), " +
            "and ensure the app is published to Production.",
          { status: 400 },
        );
      }
      store.upsertToken({
        user: "self", // placeholder; re-keyed to real healthUserId on first webhook
        access_token: tok.access_token,
        refresh_token: tok.refresh_token,
        expires_at: Date.now() + tok.expires_in * 1000,
      });
      console.log("✓ Authorized. Refresh token stored. You can close the browser tab.");
      setTimeout(() => server.stop(), 500);
      return new Response("Authorized — you can close this tab.", { status: 200 });
    } catch (err) {
      console.error("Token exchange failed:", err);
      return new Response("token exchange failed; see console", { status: 500 });
    }
  },
});

console.log(`Waiting for the redirect on ${cfg.google.redirectUri} …`);
