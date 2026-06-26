#!/usr/bin/env node

import { readFileSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONFIG_PATH = join(__dirname, "..", "config.json");
const API_BASE = "https://api.heybossai.com/v1";
const WEB_BASE = "https://www.skillboss.co";

function loadConfig() {
  try { return JSON.parse(readFileSync(CONFIG_PATH, "utf8")); }
  catch { return {}; }
}

function saveConfig(config) {
  writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2) + "\n");
}

function getKey() {
  const envKey = (process.env.SKILLBOSS_API_KEY ?? "").trim();
  if (envKey) return envKey;

  const config = loadConfig();
  const key = config.apiKey;
  if (!key || key === "YOUR_API_KEY_HERE" || key.includes("...")) return null;
  return key;
}

function mask(key) {
  if (!key || key.length < 14) return key;
  return key.slice(0, 10) + "..." + key.slice(-4);
}

function usage() {
  console.error(`Usage: auth.mjs <command>

Commands:
  trial    Provision a free trial key ($0.25 credit)
  login    Sign in via browser (upgrade trial to permanent)
  status   Show current API key
  logout   Remove stored credentials`);
  process.exit(2);
}

const cmd = process.argv[2];
if (!cmd || cmd === "-h" || cmd === "--help") usage();

if (cmd === "trial") {
  const existing = getKey();
  if (existing) {
    console.error(`Already have key: ${mask(existing)}`);
    process.stdout.write(existing);
    process.exit(0);
  }

  const resp = await fetch(`${API_BASE}/temp-token/provision`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    console.error(`Provisioning failed (${resp.status}): ${text}`);
    process.exit(1);
  }

  const data = await resp.json();
  const config = loadConfig();
  config.apiKey = data.api_key;
  saveConfig(config);
  console.error(`Trial key provisioned ($${data.balance_usd} credit)`);
  console.error(`Upgrade anytime: node auth.mjs login`);
  process.stdout.write(data.api_key);

} else if (cmd === "login") {
  let key = getKey();

  if (!key) {
    const resp = await fetch(`${API_BASE}/temp-token/provision`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    if (!resp.ok) {
      console.error(`Provisioning failed (${resp.status})`);
      process.exit(1);
    }
    const data = await resp.json();
    const config = loadConfig();
    config.apiKey = data.api_key;
    saveConfig(config);
    key = data.api_key;
    console.error(`Trial key ready ($${data.balance_usd} credit)`);
  }

  const bindUrl = `${WEB_BASE}/login?temp=${encodeURIComponent(key)}`;
  console.error(`\nOpen this URL to sign in:\n  ${bindUrl}\n`);
  console.error(`Sign up or log in, then click "Bind & Transfer Credits".`);
  console.error(`Waiting for authentication...`);

  const start = Date.now();
  while (Date.now() - start < 5 * 60 * 1000) {
    await new Promise(r => setTimeout(r, 2000));
    try {
      const resp = await fetch(`${API_BASE}/temp-token/poll-bind`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ temp_api_key: key }),
      });
      if (!resp.ok) continue;
      const result = await resp.json();
      if (result.status === "bound" && result.permanent_api_key) {
        const config = loadConfig();
        config.apiKey = result.permanent_api_key;
        saveConfig(config);
        console.error(`\nAuthentication complete! Key saved to config.json`);
        process.exit(0);
      }
    } catch {}
  }

  console.error(`\nTimed out. Complete sign-in at: ${bindUrl}`);
  process.exit(1);

} else if (cmd === "status") {
  const key = getKey();
  if (!key) {
    console.error("Not logged in. Run: node auth.mjs trial");
    process.exit(1);
  }
  console.log(`Key: ${mask(key)}`);
  console.log(`Source: config.json`);

} else if (cmd === "logout") {
  const config = loadConfig();
  config.apiKey = "YOUR_API_KEY_HERE";
  saveConfig(config);
  console.error("Logged out. Key removed from config.json");

} else {
  console.error(`Unknown command: ${cmd}`);
  usage();
}
