/**
 * keychain.js — Platform-aware bootstrap credential storage
 *
 * Priority order:
 *   1. macOS Keychain    (security CLI)
 *   2. Linux Secret Svc  (secret-tool CLI)
 *   3. AES-256-GCM file  (crypto-local.js fallback — works everywhere)
 *
 * All methods store under:
 *   service = "openclaw-supabase-vault"
 *   account = "credentials"
 *
 * Stored payload is always JSON: { url, serviceRoleKey }
 */

"use strict";

const { execSync, execFileSync } = require("node:child_process");
const fs   = require("node:fs");
const os   = require("node:os");
const path = require("node:path");

const { encrypt, decrypt } = require("./crypto-local.js");

const SERVICE  = "openclaw-supabase-vault";
const ACCOUNT  = "credentials";
const ENC_FILE = path.join(os.homedir(), ".openclaw", "supabase-vault-config.enc");

// ─── Platform detection ───────────────────────────────────────────────────────

function which(cmd) {
  try {
    execSync(`which ${cmd}`, { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

function isMacOS() {
  return process.platform === "darwin";
}

function hasSecretTool() {
  return process.platform === "linux" && which("secret-tool");
}

/**
 * Detect the best available keychain method.
 * @returns {{ method: string, available: boolean }}
 */
function detect() {
  if (isMacOS() && which("security")) {
    return { method: "macos", available: true };
  }
  if (hasSecretTool()) {
    return { method: "linux-secret-service", available: true };
  }
  // AES-256-GCM file fallback always available
  return { method: "aes-gcm", available: true };
}

// ─── macOS Keychain ───────────────────────────────────────────────────────────

function macosStore(payload) {
  const json = JSON.stringify(payload);
  // Delete existing entry if present (ignore errors)
  try {
    execFileSync("security", [
      "delete-generic-password",
      "-s", SERVICE,
      "-a", ACCOUNT,
    ], { stdio: "ignore" });
  } catch { /* not present, that's fine */ }

  execFileSync("security", [
    "add-generic-password",
    "-s", SERVICE,
    "-a", ACCOUNT,
    "-w", json,
    "-U",
  ], { stdio: "pipe" });
}

function macosRetrieve() {
  const raw = execFileSync("security", [
    "find-generic-password",
    "-s", SERVICE,
    "-a", ACCOUNT,
    "-w",
  ], { encoding: "utf8" }).trim();
  return JSON.parse(raw);
}

function macosClear() {
  try {
    execFileSync("security", [
      "delete-generic-password",
      "-s", SERVICE,
      "-a", ACCOUNT,
    ], { stdio: "ignore" });
  } catch { /* already gone */ }
}

// ─── Linux Secret Service (secret-tool) ──────────────────────────────────────

function secretToolStore(payload) {
  const json = JSON.stringify(payload);
  const child = require("node:child_process").spawn(
    "secret-tool",
    ["store", "--label", "OpenClaw Supabase Vault", "service", SERVICE, "account", ACCOUNT],
    { stdio: ["pipe", "ignore", "ignore"] }
  );
  child.stdin.write(json);
  child.stdin.end();
  // Wait synchronously via a simple poll
  const start = Date.now();
  while (child.exitCode === null && Date.now() - start < 5000) {
    require("node:timers").setImmediate(() => {});
  }
}

function secretToolRetrieve() {
  const raw = execFileSync("secret-tool", [
    "lookup",
    "service", SERVICE,
    "account", ACCOUNT,
  ], { encoding: "utf8" }).trim();
  return JSON.parse(raw);
}

function secretToolClear() {
  try {
    execFileSync("secret-tool", [
      "clear",
      "service", SERVICE,
      "account", ACCOUNT,
    ], { stdio: "ignore" });
  } catch { /* already gone */ }
}

// ─── AES-256-GCM file fallback ────────────────────────────────────────────────

function aesStore(payload) {
  const json = JSON.stringify(payload);
  const blob = encrypt(json);
  fs.mkdirSync(path.dirname(ENC_FILE), { recursive: true });
  fs.writeFileSync(ENC_FILE, blob, { mode: 0o600 });
}

function aesRetrieve() {
  if (!fs.existsSync(ENC_FILE)) {
    throw new Error("No Supabase credentials found. Run the setup in the dashboard first.");
  }
  const blob = fs.readFileSync(ENC_FILE);
  const json = decrypt(blob);
  return JSON.parse(json);
}

function aesClear() {
  try { fs.unlinkSync(ENC_FILE); } catch { /* already gone */ }
}

// ─── Public API ───────────────────────────────────────────────────────────────

/**
 * Store Supabase bootstrap credentials.
 * @param {string} url           Supabase project URL
 * @param {string} serviceRoleKey  Supabase service_role key
 */
function store(url, serviceRoleKey) {
  const payload = { url, serviceRoleKey };
  const { method } = detect();

  if (method === "macos") {
    macosStore(payload);
  } else if (method === "linux-secret-service") {
    secretToolStore(payload);
  } else {
    aesStore(payload);
  }
}

/**
 * Retrieve stored credentials.
 * @returns {{ url: string, serviceRoleKey: string }}
 */
function retrieve() {
  const { method } = detect();

  if (method === "macos") {
    return macosRetrieve();
  } else if (method === "linux-secret-service") {
    return secretToolRetrieve();
  } else {
    return aesRetrieve();
  }
}

/**
 * Clear stored credentials.
 */
function clear() {
  // Try all methods in case the method changed since storage
  try { macosClear(); } catch { /* not macOS or not present */ }
  try { secretToolClear(); } catch { /* not Linux or not present */ }
  aesClear();
}

module.exports = { detect, store, retrieve, clear };
