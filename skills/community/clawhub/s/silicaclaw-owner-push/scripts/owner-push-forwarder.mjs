#!/usr/bin/env node

import { closeSync, existsSync, mkdirSync, openSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, resolve } from "node:path";
import { spawn } from "node:child_process";

const API_BASE = String(process.env.SILICACLAW_API_BASE || "http://localhost:4310").replace(/\/+$/, "");
const POLL_INTERVAL_MS = Math.max(1000, Number(process.env.OPENCLAW_FORWARDER_INTERVAL_MS || 5000) || 5000);
const LIMIT = Math.max(1, Number(process.env.OPENCLAW_FORWARDER_LIMIT || 30) || 30);
const OWNER_FORWARD_CMD = String(process.env.OPENCLAW_OWNER_FORWARD_CMD || "").trim();
const STATE_PATH = resolve(
  String(process.env.OPENCLAW_OWNER_FORWARD_STATE_PATH || resolve(homedir(), ".openclaw", "workspace", "state", "silicaclaw-owner-push.json"))
);
const LOCK_PATH = `${STATE_PATH}.lock`;
const LATEST_ONLY = String(process.env.OPENCLAW_FORWARD_LATEST_ONLY || "true").trim().toLowerCase() !== "false";
const ONCE = process.argv.includes("--once");
const VERBOSE = process.argv.includes("--verbose");
let lockFd = null;

function parseListEnv(name) {
  return String(process.env[name] || "")
    .split(",")
    .map((item) => item.trim().toLowerCase())
    .filter(Boolean);
}

const TOPIC_FILTERS = parseListEnv("OPENCLAW_FORWARD_TOPICS");
const INCLUDE_TERMS = parseListEnv("OPENCLAW_FORWARD_INCLUDE");
const EXCLUDE_TERMS = parseListEnv("OPENCLAW_FORWARD_EXCLUDE");
const DEFAULT_SIGNAL_TERMS = [
  "approval",
  "approve",
  "blocked",
  "error",
  "failed",
  "failure",
  "complete",
  "completed",
  "deploy",
  "security",
  "credential",
  "fund",
  "payment",
  "risk",
  "urgent",
];

function request(path, options = {}) {
  return fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  }).then(async (res) => {
    const json = await res.json().catch(() => null);
    if (!res.ok || !json?.ok) {
      throw new Error(json?.error?.message || `Request failed (${res.status})`);
    }
    return json.data;
  });
}

function loadState() {
  if (!existsSync(STATE_PATH)) {
    return {
      seen_ids: [],
      pushed_at: {},
      last_pushed_created_at: 0,
      last_pushed_message_id: "",
    };
  }
  try {
    const parsed = JSON.parse(readFileSync(STATE_PATH, "utf8"));
    return {
      seen_ids: Array.isArray(parsed?.seen_ids) ? parsed.seen_ids : [],
      pushed_at: parsed?.pushed_at && typeof parsed.pushed_at === "object" ? parsed.pushed_at : {},
      last_pushed_created_at: Number(parsed?.last_pushed_created_at || 0) || 0,
      last_pushed_message_id: String(parsed?.last_pushed_message_id || ""),
    };
  } catch {
    return {
      seen_ids: [],
      pushed_at: {},
      last_pushed_created_at: 0,
      last_pushed_message_id: "",
    };
  }
}

function saveState(state) {
  mkdirSync(dirname(STATE_PATH), { recursive: true });
  writeFileSync(STATE_PATH, JSON.stringify(state, null, 2), "utf8");
}

function isPidRunning(pid) {
  if (!pid || !Number.isFinite(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

function releaseLock() {
  if (lockFd !== null) {
    try {
      closeSync(lockFd);
    } catch {
      // ignore
    }
    try {
      rmSync(LOCK_PATH, { force: true });
    } catch {
      // ignore
    }
    lockFd = null;
  }
}

function acquireLock() {
  mkdirSync(dirname(LOCK_PATH), { recursive: true });
  try {
    lockFd = openSync(LOCK_PATH, "wx");
    writeFileSync(lockFd, JSON.stringify({
      pid: process.pid,
      started_at: new Date().toISOString(),
      state_path: STATE_PATH,
    }, null, 2), "utf8");
    process.on("exit", releaseLock);
    process.on("SIGINT", () => {
      releaseLock();
      process.exit(130);
    });
    process.on("SIGTERM", () => {
      releaseLock();
      process.exit(143);
    });
    return;
  } catch {
    // fall through
  }

  try {
    const existing = JSON.parse(readFileSync(LOCK_PATH, "utf8"));
    const existingPid = Number(existing?.pid || 0) || 0;
    if (isPidRunning(existingPid)) {
      throw new Error(`owner push forwarder already running (pid=${existingPid})`);
    }
  } catch (error) {
    if (error instanceof Error && error.message.includes("already running")) {
      throw error;
    }
  }

  rmSync(LOCK_PATH, { force: true });
  lockFd = openSync(LOCK_PATH, "wx");
  writeFileSync(lockFd, JSON.stringify({
    pid: process.pid,
    started_at: new Date().toISOString(),
    state_path: STATE_PATH,
  }, null, 2), "utf8");
  process.on("exit", releaseLock);
  process.on("SIGINT", () => {
    releaseLock();
    process.exit(130);
  });
  process.on("SIGTERM", () => {
    releaseLock();
    process.exit(143);
  });
}

function trimState(state) {
  const recentIds = Array.isArray(state.seen_ids) ? state.seen_ids.slice(-500) : [];
  const pushedEntries = Object.entries(state.pushed_at || {}).slice(-500);
  state.seen_ids = recentIds;
  state.pushed_at = Object.fromEntries(pushedEntries);
}

function messageCreatedAt(item) {
  const createdAt = Number(item?.created_at || 0);
  return Number.isFinite(createdAt) && createdAt > 0 ? createdAt : 0;
}

function isNewerThanCursor(item, state) {
  const createdAt = messageCreatedAt(item);
  const lastCreatedAt = Number(state.last_pushed_created_at || 0) || 0;
  const messageId = String(item?.message_id || "").trim();
  const lastMessageId = String(state.last_pushed_message_id || "").trim();
  if (createdAt > lastCreatedAt) return true;
  if (createdAt < lastCreatedAt) return false;
  if (!createdAt) return !state.seen_ids.includes(messageId);
  return Boolean(messageId) && messageId !== lastMessageId && !state.seen_ids.includes(messageId);
}

function shouldWatchTopic(message) {
  if (!TOPIC_FILTERS.length) return true;
  return TOPIC_FILTERS.includes(String(message?.topic || "global").toLowerCase());
}

function scoreRoute(message) {
  const text = [
    String(message?.topic || ""),
    String(message?.display_name || ""),
    String(message?.body || ""),
  ].join(" ").toLowerCase();

  if (!text.trim()) return "ignore";
  if (EXCLUDE_TERMS.some((term) => text.includes(term))) return "ignore";

  if (INCLUDE_TERMS.length && INCLUDE_TERMS.some((term) => text.includes(term))) {
    return "push_summary";
  }

  if (DEFAULT_SIGNAL_TERMS.some((term) => text.includes(term))) {
    return "push_summary";
  }

  return "ignore";
}

function summarizeForOwner(message) {
  const source = `${message.display_name || "Unknown"} · ${message.topic || "global"}`;
  const body = String(message.body || "").trim();
  const priority = scoreRoute(message) === "push_summary"
    ? "Owner-relevant SilicaClaw broadcast"
    : "Routine";
  return [
    `Source: ${source}`,
    `Priority: ${priority}`,
    `What happened: ${body.slice(0, 240)}${body.length > 240 ? "..." : ""}`,
    "Action: Review whether owner follow-up or approval is needed.",
  ].join("\n");
}

function dispatchToOwner(route, summary, message) {
  if (!OWNER_FORWARD_CMD) {
    console.log("");
    console.log(`[${route}] ${message.message_id || "-"}`);
    console.log(summary);
    return Promise.resolve();
  }

  return new Promise((resolve, reject) => {
    const child = spawn(OWNER_FORWARD_CMD, {
      shell: true,
      stdio: ["pipe", "inherit", "inherit"],
      env: process.env,
    });
    child.on("error", reject);
    child.on("exit", (code) => {
      if (code === 0) {
        resolve();
        return;
      }
      reject(new Error(`owner dispatch failed (exit=${code ?? "unknown"})`));
    });
    child.stdin.write(JSON.stringify({
      route,
      summary,
      message: {
        message_id: message.message_id || "",
        display_name: message.display_name || "",
        topic: message.topic || "global",
        body: message.body || "",
        created_at: message.created_at || Date.now(),
      },
    }, null, 2));
    child.stdin.end();
  });
}

async function pollOnce(state) {
  const payload = await request(`/api/openclaw/bridge/messages?limit=${LIMIT}`);
  const items = Array.isArray(payload?.items) ? payload.items.slice().reverse() : [];
  const candidates = [];

  for (const item of items) {
    const messageId = String(item?.message_id || "").trim();
    if (!messageId) continue;
    if (!isNewerThanCursor(item, state)) {
      if (!state.seen_ids.includes(messageId)) {
        state.seen_ids.push(messageId);
      }
      continue;
    }

    if (!shouldWatchTopic(item)) {
      state.seen_ids.push(messageId);
      if (VERBOSE) console.log(`skip topic: ${messageId}`);
      continue;
    }

    const route = scoreRoute(item);
    if (route === "ignore") {
      state.seen_ids.push(messageId);
      if (VERBOSE) console.log(`ignore low-signal: ${messageId}`);
      continue;
    }

    candidates.push({ item, messageId, route, createdAt: messageCreatedAt(item) });
  }

  const selected = LATEST_ONLY
    ? candidates.sort((left, right) => {
        if (left.createdAt !== right.createdAt) return right.createdAt - left.createdAt;
        return left.messageId.localeCompare(right.messageId);
      })[0] || null
    : null;

  const toPush = LATEST_ONLY ? (selected ? [selected] : []) : candidates;

  for (const candidate of toPush) {
    const summary = summarizeForOwner(candidate.item);
    await dispatchToOwner(candidate.route, summary, candidate.item);
    state.pushed_at[candidate.messageId] = new Date().toISOString();
    state.last_pushed_created_at = candidate.createdAt || Date.now();
    state.last_pushed_message_id = candidate.messageId;
    if (VERBOSE) console.log(`pushed to owner: ${candidate.messageId}`);
  }

  if (LATEST_ONLY && selected) {
    for (const candidate of candidates) {
      state.seen_ids.push(candidate.messageId);
    }
  } else {
    for (const candidate of candidates) {
      state.seen_ids.push(candidate.messageId);
    }
  }

  trimState(state);
  saveState(state);
}

async function main() {
  acquireLock();
  const state = loadState();
  if (VERBOSE) {
    console.log(`SilicaClaw owner push watching ${API_BASE}`);
    console.log(`State file: ${STATE_PATH}`);
    console.log(`Lock file: ${LOCK_PATH}`);
    console.log(`Latest-only mode: ${LATEST_ONLY ? "on" : "off"}`);
  }

  do {
    await pollOnce(state);
    if (ONCE) break;
    await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL_MS));
  } while (true);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
