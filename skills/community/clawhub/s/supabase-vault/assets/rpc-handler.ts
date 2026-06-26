/**
 * supabase-vault.ts — Gateway RPC handlers for Supabase Vault integration
 *
 * Install at: src/gateway/server-methods/supabase-vault.ts
 *
 * Register in src/gateway/server-methods.ts (or equivalent index):
 *   import { createSupabaseVaultHandlers } from "./supabase-vault.js";
 *   ...
 *   Object.assign(handlers, createSupabaseVaultHandlers());
 */

import { execFile } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { promisify } from "node:util";
import type { GatewayRequestHandlers } from "./types.js";
import { ErrorCodes, errorShape } from "../protocol/index.js";

const execFileAsync = promisify(execFile);

const SKILL_DIR    = path.join(os.homedir(), ".openclaw", "skills", "supabase-vault");
const KEYCHAIN_JS  = path.join(SKILL_DIR, "scripts", "keychain.js");
const MIGRATE_JS   = path.join(SKILL_DIR, "scripts", "migrate.js");
const SECRETS_FILE = path.join(os.homedir(), ".openclaw", "secrets.json");
const CONFIG_FILE  = path.join(os.homedir(), ".openclaw", "openclaw.json");

// ─── Supabase client helpers ──────────────────────────────────────────────────

function requireSupabase() {
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    return require(path.join(SKILL_DIR, "node_modules", "@supabase", "supabase-js"));
  } catch {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    return require("@supabase/supabase-js");
  }
}

function makeClient(url: string, serviceRoleKey: string) {
  const { createClient } = requireSupabase();
  return createClient(url, serviceRoleKey, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
}

// ─── Keychain interop (via child process to use CommonJS module) ───────────────

async function keychainDetect(): Promise<{ method: string; available: boolean }> {
  const { stdout } = await execFileAsync("node", [
    "-e",
    `const k=require(${JSON.stringify(KEYCHAIN_JS)});console.log(JSON.stringify(k.detect()));`,
  ]);
  return JSON.parse(stdout.trim());
}

async function keychainRetrieve(): Promise<{ url: string; serviceRoleKey: string }> {
  const { stdout } = await execFileAsync("node", [
    "-e",
    `const k=require(${JSON.stringify(KEYCHAIN_JS)});try{console.log(JSON.stringify(k.retrieve()));}catch(e){console.log(JSON.stringify({error:e.message}));}`,
  ]);
  const result = JSON.parse(stdout.trim());
  if (result.error) throw new Error(result.error);
  return result;
}

async function keychainStore(url: string, serviceRoleKey: string): Promise<void> {
  await execFileAsync("node", [
    "-e",
    `const k=require(${JSON.stringify(KEYCHAIN_JS)});k.store(${JSON.stringify(url)},${JSON.stringify(serviceRoleKey)});`,
  ]);
}

async function keychainClear(): Promise<void> {
  await execFileAsync("node", [
    "-e",
    `const k=require(${JSON.stringify(KEYCHAIN_JS)});k.clear();`,
  ]);
}

// ─── Config helpers ───────────────────────────────────────────────────────────

function readConfig(): Record<string, unknown> {
  return JSON.parse(fs.readFileSync(CONFIG_FILE, "utf-8"));
}

function writeConfig(config: Record<string, unknown>): void {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2) + "\n");
}

function addExecProvider(config: Record<string, unknown>): void {
  const secrets = (config.secrets as Record<string, unknown>) ?? {};
  const providers = (secrets.providers as Record<string, unknown>) ?? {};
  providers.supabase = {
    source: "exec",
    command: "node",
    args: [path.join(SKILL_DIR, "scripts", "fetch-secrets.js")],
    jsonOnly: true,
    trustedDirs: [SKILL_DIR],
    timeoutMs: 8000,
  };
  secrets.providers = providers;
  config.secrets = secrets;
}

function maskUrl(url: string): string {
  try {
    const u = new URL(url);
    const host = u.hostname; // e.g. abcxyz.supabase.co
    const parts = host.split(".");
    if (parts.length >= 3) {
      parts[0] = parts[0].slice(0, 4) + "****";
    }
    return `https://${parts.join(".")}`;
  } catch {
    return url.slice(0, 20) + "****";
  }
}

// ─── RPC Handlers ─────────────────────────────────────────────────────────────

export function createSupabaseVaultHandlers(): GatewayRequestHandlers {
  return {

    // ── Status ──────────────────────────────────────────────────────────────

    "supabase-vault.status": async ({ respond }) => {
      try {
        const det = await keychainDetect();
        let connected = false;
        let urlMasked = "";
        let keyCount = 0;

        try {
          const creds = await keychainRetrieve();
          urlMasked = maskUrl(creds.url);

          // Test connection by listing secrets
          const supabase = makeClient(creds.url, creds.serviceRoleKey);
          const { data, error } = await supabase.rpc("list_secret_names");
          if (!error) {
            connected = true;
            keyCount = Array.isArray(data) ? data.length : 0;
          }
        } catch { /* creds not set or connection failed */ }

        respond(true, {
          ok: true,
          connected,
          method: det.method,
          url: urlMasked,
          keyCount,
          skillDir: SKILL_DIR,
        });
      } catch (err) {
        respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, String(err)));
      }
    },

    // ── Connect ──────────────────────────────────────────────────────────────

    "supabase-vault.connect": async ({ params: p, respond }) => {
      try {
        const { url, serviceRoleKey } = p as { url?: string; serviceRoleKey?: string };
        if (!url?.trim() || !serviceRoleKey?.trim()) {
          respond(false, undefined, errorShape(ErrorCodes.INVALID_REQUEST, "url and serviceRoleKey required"));
          return;
        }

        // Test connection
        const supabase = makeClient(url.trim(), serviceRoleKey.trim());
        const { error } = await supabase.rpc("list_secret_names");
        if (error) {
          respond(false, undefined, errorShape(
            ErrorCodes.UNAVAILABLE,
            `Connection test failed: ${error.message}. Make sure you ran setup.sql in your Supabase project.`
          ));
          return;
        }

        // Store credentials
        await keychainStore(url.trim(), serviceRoleKey.trim());

        // Add exec provider to config
        const config = readConfig();
        addExecProvider(config);
        writeConfig(config);

        const det = await keychainDetect();
        respond(true, { ok: true, method: det.method, url: maskUrl(url.trim()) });
      } catch (err) {
        respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, String(err)));
      }
    },

    // ── Disconnect ───────────────────────────────────────────────────────────

    "supabase-vault.disconnect": async ({ respond }) => {
      try {
        await keychainClear();
        respond(true, { ok: true });
      } catch (err) {
        respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, String(err)));
      }
    },

    // ── List secrets ─────────────────────────────────────────────────────────

    "supabase-vault.list": async ({ respond }) => {
      try {
        const creds = await keychainRetrieve();
        const supabase = makeClient(creds.url, creds.serviceRoleKey);
        const { data, error } = await supabase.rpc("list_secret_names");
        if (error) throw new Error(error.message);
        const secrets = (data as Array<{ name: string; id: string }> || []).map(
          (row) => ({ name: row.name, id: row.id })
        );
        respond(true, { ok: true, secrets });
      } catch (err) {
        respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, String(err)));
      }
    },

    // ── Write secret ─────────────────────────────────────────────────────────

    "supabase-vault.write": async ({ params: p, respond }) => {
      try {
        const { name, value } = p as { name?: string; value?: string };
        if (!name?.trim() || !value?.trim()) {
          respond(false, undefined, errorShape(ErrorCodes.INVALID_REQUEST, "name and value required"));
          return;
        }
        const creds = await keychainRetrieve();
        const supabase = makeClient(creds.url, creds.serviceRoleKey);
        const { data, error } = await supabase.rpc("insert_secret", {
          name: name.trim(),
          secret: value.trim(),
        });
        if (error) throw new Error(error.message);
        respond(true, { ok: true, id: data, name: name.trim() });
      } catch (err) {
        respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, String(err)));
      }
    },

    // ── Delete secret ────────────────────────────────────────────────────────

    "supabase-vault.delete": async ({ params: p, respond }) => {
      try {
        const { name } = p as { name?: string };
        if (!name?.trim()) {
          respond(false, undefined, errorShape(ErrorCodes.INVALID_REQUEST, "name required"));
          return;
        }
        const creds = await keychainRetrieve();
        const supabase = makeClient(creds.url, creds.serviceRoleKey);
        const { error } = await supabase.rpc("delete_secret", { secret_name: name.trim() });
        if (error) throw new Error(error.message);
        respond(true, { ok: true, name: name.trim() });
      } catch (err) {
        respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, String(err)));
      }
    },

    // ── Migrate ──────────────────────────────────────────────────────────────

    "supabase-vault.migrate": async ({ respond }) => {
      try {
        const { stdout, stderr } = await execFileAsync(
          "node",
          [MIGRATE_JS, "--yes"],
          { timeout: 60_000 }
        );
        respond(true, { ok: true, output: stdout + stderr });
      } catch (err: unknown) {
        const e = err as { message?: string; stdout?: string; stderr?: string };
        respond(false, undefined, errorShape(
          ErrorCodes.UNAVAILABLE,
          e.message || "Migration failed"
        ));
      }
    },

    // ── Config snippet ───────────────────────────────────────────────────────

    "supabase-vault.config": async ({ respond }) => {
      respond(true, {
        ok: true,
        snippet: {
          secrets: {
            providers: {
              supabase: {
                source: "exec",
                command: "node",
                args: [path.join(SKILL_DIR, "scripts", "fetch-secrets.js")],
                jsonOnly: true,
                trustedDirs: [SKILL_DIR],
                timeoutMs: 8000,
              },
            },
          },
        },
      });
    },
  };
}
