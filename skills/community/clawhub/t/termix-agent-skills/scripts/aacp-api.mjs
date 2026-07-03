#!/usr/bin/env node
//
// Termix Platform (dev-v2) authenticated API caller — the generic off-chain
// building block. Any Provider workflow that is a plain REST call (create/edit/
// publish listing, offers, campaign claim/submit-proof, register artifacts,
// reads) goes through here. On-chain steps use aacp-tx.mjs instead.
//
// Usage:
//   node aacp-api.mjs <METHOD> <path> [--body '<json>'] [--auth session|runtime|none]
//
// Examples:
//   node aacp-api.mjs GET  /api/v1/me
//   node aacp-api.mjs POST /api/v1/agents/<id>/services --body '{"title":"Audit"}'
//   node aacp-api.mjs POST /api/v1/campaigns/<id>/claim
//
// Auth (default: session):
//   session  → Bearer the wallet session from `a2a-runtime.mjs login` (.termix-a2a-session.env)
//   runtime  → Bearer the agent runtime token (.termix-a2a-runtime.env)
//   none     → no Authorization header (public endpoints)
//
// Env: AACP_BASE_URL (default https://platform-backend.prod.termix.live),
//      A2A_SESSION_TOKEN / A2A_RUNTIME_TOKEN (override the cached files).
//
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const DEFAULT_BASE = "https://platform-backend.prod.termix.live";
const args = process.argv.slice(2);

function arg(name) {
  const i = args.indexOf(`--${name}`);
  if (i < 0) return undefined;
  const v = args[i + 1];
  return v && !v.startsWith("--") ? v : true;
}

function baseUrl() {
  if (process.env.AACP_BASE_URL) return process.env.AACP_BASE_URL.replace(/\/$/, "");
  if (args.includes("--dev")) return "https://platform-backend.dev.termix.live";
  return DEFAULT_BASE;
}

function readCached(file, varName, envName) {
  if (process.env[envName]) return process.env[envName];
  const path = resolve(process.cwd(), file);
  if (!existsSync(path)) return null;
  const m = readFileSync(path, "utf8").match(new RegExp(`^${varName}=(.+)$`, "m"));
  return m ? m[1].trim() : null;
}

function authToken(mode) {
  if (mode === "none") return null;
  if (mode === "runtime") {
    const t = readCached(".termix-a2a-runtime.env", "A2A_RUNTIME_TOKEN", "A2A_RUNTIME_TOKEN");
    if (!t) throw new Error("No runtime token. Run `a2a-runtime.mjs token` (or autoreply) first.");
    return t;
  }
  const t = readCached(".termix-a2a-session.env", "A2A_SESSION_TOKEN", "A2A_SESSION_TOKEN");
  if (!t) throw new Error("Not logged in. Run `a2a-runtime.mjs login` first (or pass --auth none for public endpoints).");
  return t;
}

async function main() {
  if (args.includes("--help") || args.includes("-h") || args.length < 2) {
    process.stderr.write("Usage: node aacp-api.mjs <METHOD> <path> [--body '<json>'] [--auth session|runtime|none]\n");
    process.exit(args.length < 2 ? 2 : 0);
  }
  const method = args[0].toUpperCase();
  const path = args[1];
  const bodyRaw = arg("body");
  const authMode = (typeof arg("auth") === "string" && arg("auth")) || "session";

  const url = path.startsWith("http") ? path : `${baseUrl()}${path.startsWith("/") ? path : `/${path}`}`;
  const token = authToken(authMode);
  const headers = {};
  let body;
  if (typeof bodyRaw === "string") {
    JSON.parse(bodyRaw); // validate
    headers["content-type"] = "application/json";
    body = bodyRaw;
  }
  if (token) headers.authorization = `Bearer ${token}`;

  const res = await fetch(url, { method, headers, body });
  const text = await res.text();
  let json;
  try { json = text ? JSON.parse(text) : {}; } catch { json = { raw: text }; }
  if (!res.ok) {
    process.stderr.write(`${method} ${path} → HTTP ${res.status}\n`);
    console.log(JSON.stringify(json, null, 2));
    process.exit(1);
  }
  console.log(JSON.stringify(json, null, 2));
}

main().catch((err) => {
  process.stderr.write(`error: ${err.message}\n`);
  process.exit(1);
});
