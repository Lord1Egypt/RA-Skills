#!/usr/bin/env node
/**
 * migrate.js — Migrate local secrets.json → Supabase Vault
 *
 * Usage:
 *   node migrate.js           # interactive (prompts y/n)
 *   node migrate.js --yes     # non-interactive
 *   node migrate.js --dry-run # preview only, no changes
 */

"use strict";

const fs   = require("node:fs");
const os   = require("node:os");
const path = require("node:path");
const readline = require("node:readline");

const keychain = require(path.join(__dirname, "keychain.js"));

const SECRETS_FILE  = path.join(os.homedir(), ".openclaw", "secrets.json");
const CONFIG_FILE   = path.join(os.homedir(), ".openclaw", "openclaw.json");
const SKILL_DIR     = path.join(os.homedir(), ".openclaw", "skills", "supabase-vault");

const isDryRun = process.argv.includes("--dry-run");
const isYes    = process.argv.includes("--yes");

// ─── Helpers ──────────────────────────────────────────────────────────────────

function log(msg)   { process.stdout.write(msg + "\n"); }
function err(msg)   { process.stderr.write("✗ " + msg + "\n"); }
function ok(msg)    { log("✓ " + msg); }
function info(msg)  { log("  " + msg); }
function head(msg)  { log("\n" + msg); }

function readSecrets() {
  try {
    if (!fs.existsSync(SECRETS_FILE)) return {};
    return JSON.parse(fs.readFileSync(SECRETS_FILE, "utf8"));
  } catch {
    return {};
  }
}

function readConfig() {
  return JSON.parse(fs.readFileSync(CONFIG_FILE, "utf8"));
}

function writeConfig(config) {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2) + "\n");
}

function prompt(question) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question(question, (answer) => { rl.close(); resolve(answer.trim()); });
  });
}

// ─── SecretRef patching ───────────────────────────────────────────────────────

function isFileRef(value) {
  return (
    value &&
    typeof value === "object" &&
    value.source === "file" &&
    typeof value.id === "string"
  );
}

function toSupabaseRef(id) {
  // id is like "/OPENAI_API_KEY" — keep as-is
  return { source: "exec", provider: "supabase", id };
}

function patchRefsInObject(obj, migratedKeys) {
  if (!obj || typeof obj !== "object" || Array.isArray(obj)) return;
  for (const [k, v] of Object.entries(obj)) {
    if (isFileRef(v) && migratedKeys.has(v.id)) {
      obj[k] = toSupabaseRef(v.id);
    } else if (v && typeof v === "object") {
      patchRefsInObject(v, migratedKeys);
    }
  }
}

function addSupabaseProvider(config) {
  config.secrets = config.secrets || {};
  config.secrets.providers = config.secrets.providers || {};
  config.secrets.providers.supabase = {
    source: "exec",
    command: "node",
    args: [path.join(SKILL_DIR, "scripts", "fetch-secrets.js")],
    jsonOnly: true,
    trustedDirs: [SKILL_DIR],
    timeoutMs: 8000,
  };
  // Keep file provider as fallback
  if (!config.secrets.providers.default) {
    config.secrets.providers.default = {
      source: "file",
      path: SECRETS_FILE,
      mode: "json",
    };
  }
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  head("═══ Supabase Vault Migration ═══");

  // Check credentials
  let creds;
  try {
    creds = keychain.retrieve();
    ok(`Supabase credentials found (${keychain.detect().method})`);
  } catch (e) {
    err(`Supabase credentials not found: ${e.message}`);
    err("Connect Supabase first via the dashboard Integrations → Supabase Vault tab.");
    process.exit(1);
  }

  // Load local secrets
  const secrets = readSecrets();
  const keys = Object.keys(secrets);
  if (keys.length === 0) {
    log("\nNo keys found in ~/.openclaw/secrets.json — nothing to migrate.");
    process.exit(0);
  }

  head(`Found ${keys.length} key(s) to migrate:`);
  keys.forEach((k) => info(`• ${k}`));

  if (isDryRun) {
    head("Dry run — no changes made.");
    process.exit(0);
  }

  if (!isYes) {
    const answer = await prompt("\nMigrate all to Supabase Vault? [y/N] ");
    if (answer.toLowerCase() !== "y") {
      log("Aborted.");
      process.exit(0);
    }
  }

  // Load Supabase client
  let createClient;
  try {
    ({ createClient } = require(path.join(SKILL_DIR, "node_modules", "@supabase", "supabase-js")));
  } catch {
    try {
      ({ createClient } = require("@supabase/supabase-js"));
    } catch {
      err("@supabase/supabase-js not found. Run: npm install --prefix " + SKILL_DIR + " @supabase/supabase-js");
      process.exit(1);
    }
  }

  const supabase = createClient(creds.url, creds.serviceRoleKey, {
    auth: { persistSession: false, autoRefreshToken: false },
  });

  head("Migrating keys...");
  const migrated = [];
  const failed = [];

  for (const [key, value] of Object.entries(secrets)) {
    try {
      const { error } = await supabase.rpc("insert_secret", { name: key, secret: value });
      if (error) {
        // If already exists, try update
        if (error.message?.includes("unique") || error.code === "23505") {
          const uuid = await getSecretId(supabase, key);
          if (uuid) {
            const { error: updateErr } = await supabase.rpc("update_secret_by_name", {
              secret_name: key,
              new_secret: value,
            });
            if (updateErr) throw new Error(updateErr.message);
          }
        } else {
          throw new Error(error.message);
        }
      }
      ok(key);
      migrated.push(key);
    } catch (e) {
      err(`${key}: ${e.message}`);
      failed.push(key);
    }
  }

  // Patch openclaw.json
  head("Updating openclaw.json...");
  try {
    const config = readConfig();
    const migratedSet = new Set(migrated.map((k) => `/${k}`));
    patchRefsInObject(config, migratedSet);
    addSupabaseProvider(config);
    writeConfig(config);
    ok("openclaw.json updated — SecretRefs now point to Supabase provider");
  } catch (e) {
    err(`Failed to update openclaw.json: ${e.message}`);
  }

  head("═══ Migration Complete ═══");
  log(`  Migrated: ${migrated.length}  Failed: ${failed.length}`);
  if (failed.length > 0) {
    log(`  Failed keys: ${failed.join(", ")}`);
  }
  log("\n  Restart the OpenClaw gateway for changes to take effect.");
}

async function getSecretId(supabase, name) {
  try {
    const { data } = await supabase.rpc("list_secret_names");
    const found = (data || []).find((r) => (typeof r === "string" ? r : r.name) === name);
    return found?.id || null;
  } catch {
    return null;
  }
}

main().catch((e) => {
  err(String(e.message || e));
  process.exit(1);
});
