#!/usr/bin/env node
/**
 * unread-mark-keepalive.js v1.1 — renew session unread marks; 7-day hard fallback.
 *
 * Why: the gateway clamps agentStatus ttlMinutes to 1–120. Marks created by
 * unread-mark.js are recorded in $OPENCLAW_STATE_DIR/unread-marks.json; this
 * script periodically re-patches them so unread work stays visible until the
 * operator actually reads it (or 7 days pass).
 *
 * Run cadence: every 90 minutes (< TTL 120) via an OpenClaw automation, cron,
 * or Windows Task Scheduler.
 *
 * Per recorded mark:
 *   - older than 7 days            → force-clear, drop record
 *   - session gone from list       → drop record
 *   - agentStatus already gone     → mark was cleared (read/TTL) → drop record, NEVER resurrect
 *   - lastReadAt > created         → operator read it → drop record
 *   - otherwise                    → renew (statusNote + attention + ttl 120)
 *
 * v1.1 (2026-09-09): fixed "cleared mark comes back" — the gateway owns the
 *   mark, so a missing agentStatus now always wins over the read-time heuristic.
 *   Previously `lastReadAt > created` was checked first; when the operator read
 *   the session at (or just before) the mark creation time the mark was judged
 *   "unread" and a cleared badge was renewed ~90 min later.
 *
 * Everything goes through the gateway API (sessions.list / sessions.patch) —
 * no local database access, no agent-specific paths.
 *
 * Usage: node unread-mark-keepalive.js [--limit 300] [--dry-run]
 * Silent-fail policy: never throws, always exit 0.
 */

const { execFileSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const STATE_DIR = process.env.OPENCLAW_STATE_DIR || path.join(os.homedir(), ".openclaw");
const STATE_FILE = path.join(STATE_DIR, "unread-marks.json");
const TTL_MAX_MS = 7 * 24 * 60 * 60 * 1000; // 7-day fallback
const RENEW_TTL_MIN = 120; // gateway cap
const ICONS = ["alert", "flag", "hand", "key", "lock", "hourglass"];

function resolveCliEntry() {
  if (process.env.OPENCLAW_MJS && fs.existsSync(process.env.OPENCLAW_MJS)) {
    return process.env.OPENCLAW_MJS;
  }
  try { return require.resolve("openclaw/openclaw.mjs"); } catch {}
  const roots = [
    process.env.NPM_CONFIG_PREFIX,
    "C:\\npm-global",
    path.join(process.env.APPDATA || "", "npm"),
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
  return null;
}

function gwCall(method, params) {
  const cli = resolveCliEntry();
  if (!cli) return null;
  try {
    return execFileSync(
      process.execPath,
      [cli, "gateway", "call", method, "--params", JSON.stringify(params), "--timeout", "20000"],
      { timeout: 25000, windowsHide: true, encoding: "utf8" }
    );
  } catch {
    return null;
  }
}

function gwPatch(params) {
  const out = gwCall("sessions.patch", params);
  if (out == null) return { ok: false, reason: "rpc-failed" };
  const m = /"ok"\s*:\s*(true|false)/.exec(out || "");
  if (m && m[1] === "false") return { ok: false, reason: String(out).slice(0, 120) };
  return { ok: true };
}

function fetchSessions(limit) {
  const out = gwCall("sessions.list", { limit });
  if (!out) return null;
  const start = out.indexOf("{");
  if (start < 0) return null;
  try {
    const resp = JSON.parse(out.slice(start));
    const map = new Map();
    for (const s of resp.sessions || []) if (s && s.key) map.set(s.key, s);
    return map;
  } catch {
    return null;
  }
}

function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const limitIdx = args.indexOf("--limit");
  const limit = limitIdx >= 0 && Number(args[limitIdx + 1]) > 0 ? Number(args[limitIdx + 1]) : 300;

  let state = {};
  try { state = JSON.parse(fs.readFileSync(STATE_FILE, "utf8")); } catch { state = {}; }
  const keys = Object.keys(state);
  if (keys.length === 0) {
    console.log("[keepalive] no marks recorded");
    process.exit(0);
  }

  const sessions = fetchSessions(limit);
  if (!sessions) {
    // Conservative: if we cannot see the session list, do not renew and do not
    // drop anything — retry on the next cycle.
    console.log("[keepalive] sessions.list unavailable, skip this cycle");
    process.exit(0);
  }

  const now = Date.now();
  const patch = (params) => {
    if (dryRun) { console.log(`[keepalive] (dry-run) patch ${JSON.stringify(params)}`); return { ok: true }; }
    return gwPatch(params);
  };

  for (const key of keys) {
    const entry = state[key] || {};
    const created = Number(entry.created) || now;

    if (now - created >= TTL_MAX_MS) {
      patch({ key, attention: null });
      delete state[key];
      console.log(`[keepalive] EXPIRED-7d cleared ${key}`);
      continue;
    }

    const row = sessions.get(key);
    if (!row) {
      delete state[key];
      console.log(`[keepalive] drop ${key} (not in session list)`);
      continue;
    }
    // ★ v1.1 fix: the gateway owns the mark — if agentStatus is gone it was
    //   already cleared (read by the operator, or TTL-expired). Never
    //   resurrect it. This check must come BEFORE the read-time heuristic.
    if (!row.agentStatus) {
      delete state[key];
      console.log(`[keepalive] mark-cleared(read/ttl), drop ${key}`);
      continue;
    }
    const lastReadAt = Number(row.lastReadAt) || 0;
    if (lastReadAt > created) {
      delete state[key];
      console.log(`[keepalive] read-by-operator, drop ${key}`);
      continue;
    }

    let ok;
    if (entry.attention && ICONS.includes(entry.attention)) {
      // Renew with the original icon semantics (alert/flag ride the icon channel).
      ok = patch({ key, statusNote: entry.note, attention: entry.attention, ttlMinutes: RENEW_TTL_MIN }).ok;
    } else {
      patch({ key, attention: null }); // clear any inherited icon first
      ok = patch({ key, statusNote: entry.note, ttlMinutes: RENEW_TTL_MIN }).ok;
    }
    if (!ok) {
      delete state[key];
      console.log(`[keepalive] renew failed, drop ${key}`);
    } else {
      console.log(`[keepalive] renew OK ${key}`);
    }
  }

  if (!dryRun) {
    try { fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), "utf8"); } catch {}
  }
  process.exit(0);
}

main();
