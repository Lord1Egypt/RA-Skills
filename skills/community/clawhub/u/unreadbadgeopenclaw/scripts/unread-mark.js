#!/usr/bin/env node
/**
 * unread-mark.js v1.0 — mark an OpenClaw session as "unread" in the Control UI sidebar.
 *
 * Sets agentStatus = { statusNote, attention, ttlMinutes } via one
 * `openclaw gateway call sessions.patch` RPC:
 *   --event done  → flag icon  + "[New reply] HH:mm"
 *   --event warn  → alert icon + "[Failed] HH:mm"
 *
 * The icon rides the attention channel and is ALWAYS visible in the sidebar,
 * even when "Show message preview" is disabled (pure-text notes are not).
 *
 * The gateway clears the mark natively when the operator:
 *   1. opens the session (read)
 *   2. sends a new message to it
 *   3. TTL expires (default 120 min — the gateway cap; extend with
 *      unread-mark-keepalive.js)
 *
 * Usage:
 *   node unread-mark.js --key <sessionKey> --event done|warn
 *        [--ttl 120] [--note "text"] [--icon alert|flag|hand|key|lock|hourglass]
 *
 * State file: $OPENCLAW_STATE_DIR/unread-marks.json (default ~/.openclaw)
 *   { "<sessionKey>": { "note": "...", "attention": "flag", "created": 169... } }
 *
 * Implementation notes:
 * - execFileSync with an args array: arguments never pass through a shell, so
 *   JSON/quoting survives (PowerShell 5.1 Start-Process splits on spaces and
 *   eats inner quotes — never route this through one).
 * - The CLI exits 0 even when the gateway rejects the call — validate the
 *   response body for "ok":false.
 * - Any failure exits 0 silently: a notification helper must never break the
 *   pipeline it reports for.
 */

const { execFileSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const STATE_DIR = process.env.OPENCLAW_STATE_DIR || path.join(os.homedir(), ".openclaw");
const STATE_FILE = path.join(STATE_DIR, "unread-marks.json");
const ICONS = ["alert", "flag", "hand", "key", "lock", "hourglass"];

function resolveCliEntry() {
  if (process.env.OPENCLAW_MJS && fs.existsSync(process.env.OPENCLAW_MJS)) {
    return process.env.OPENCLAW_MJS;
  }
  try { return require.resolve("openclaw/openclaw.mjs"); } catch {}
  const roots = [
    process.env.NPM_CONFIG_PREFIX,
    "C:\\npm-global",
    path.join(process.env.APPDATA || "", "npm"), // Windows default npm global
    path.join(os.homedir(), ".npm-global"),
    "/usr/local/lib/node_modules",
    "/usr/lib/node_modules",
    "/opt/homebrew/lib/node_modules",
  ];
  for (const root of roots) {
    if (!root) continue;
    const p = path.join(root, "node_modules", "openclaw", "openclaw.mjs");
    try { if (fs.existsSync(p)) return p; } catch {}
  }
  // Last resort: ask npm for its global root (shell only needed on Windows
  // where `npm` is npm.cmd; no user-controlled args are involved).
  try {
    const out = execFileSync("npm", ["root", "-g"], {
      timeout: 10000, encoding: "utf8", windowsHide: true,
      shell: process.platform === "win32",
    });
    const p = path.join(String(out).trim(), "openclaw", "openclaw.mjs");
    if (fs.existsSync(p)) return p;
  } catch {}
  return null;
}

function hhmm() {
  const d = new Date();
  return String(d.getHours()).padStart(2, "0") + ":" + String(d.getMinutes()).padStart(2, "0");
}

function main() {
  const args = process.argv.slice(2);
  const get = (name) => {
    const i = args.indexOf(name);
    return i >= 0 && i + 1 < args.length ? args[i + 1] : null;
  };
  const key = get("--key");
  const event = (get("--event") || "").toLowerCase();
  const iconArg = (get("--icon") || "").toLowerCase();
  const noteOverride = get("--note");
  const ttlRaw = Number(get("--ttl") || 120);
  const ttl = Number.isInteger(ttlRaw) && ttlRaw > 0 && ttlRaw <= 120 ? ttlRaw : 120;

  const attention = iconArg || (event === "warn" ? "alert" : event === "done" ? "flag" : null);
  const note = noteOverride || (event === "warn" ? `[Failed] ${hhmm()}` : `[New reply] ${hhmm()}`);

  if (!key || !attention || !ICONS.includes(attention)) {
    console.error(
      "usage: node unread-mark.js --key <sessionKey> --event done|warn " +
      "[--ttl 120] [--note \"text\"] [--icon alert|flag|hand|key|lock|hourglass]"
    );
    process.exit(2);
  }

  const cli = resolveCliEntry();
  if (!cli) {
    console.error("[unread-mark] openclaw.mjs not found (set OPENCLAW_MJS), skip");
    process.exit(0);
  }

  const callPatch = (params, tag) => {
    const out = execFileSync(
      process.execPath,
      [cli, "gateway", "call", "sessions.patch", "--params", JSON.stringify(params), "--timeout", "20000"],
      { timeout: 25000, windowsHide: true, encoding: "utf8" }
    );
    // CLI exit code is always 0; gateway rejection only shows in the response body.
    const m = /"ok"\s*:\s*(true|false)/.exec(out || "");
    if (m && m[1] === "false") {
      throw new Error(`gateway rejected ${tag}: ${String(out).slice(0, 200)}`);
    }
    console.log(`[unread-mark] ${tag} ${key}`);
  };

  try {
    // Single-patch overwrite: replacing the whole agentStatus also replaces any
    // previous icon (e.g. warn's alert is cleanly replaced by done's flag).
    callPatch({ key, statusNote: note, attention, ttlMinutes: ttl }, `OK(${attention})`);
  } catch (err) {
    console.error(`[unread-mark] FAIL ${String((err && err.message) || err).slice(0, 200)}`);
    process.exit(0); // silent-fail: never break the notifying pipeline
  }

  // Record for the keep-alive script (best effort).
  try {
    let state = {};
    try { state = JSON.parse(fs.readFileSync(STATE_FILE, "utf8")); } catch {}
    state[key] = { note, attention, created: Date.now() };
    fs.mkdirSync(STATE_DIR, { recursive: true });
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), "utf8");
  } catch {}
}

main();
