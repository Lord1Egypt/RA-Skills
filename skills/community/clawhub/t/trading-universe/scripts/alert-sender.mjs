#!/usr/bin/env node
/**
 * alert-sender.mjs — reads alert queue and sends via OpenClaw message tool
 * Run as a frequent cron (every 30-60s) or as a small daemon
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, statSync, unlinkSync, openSync, closeSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";

const STATE_DIR = process.env.TRADE_DATA_DIR || join(homedir(), ".trading-universe");
mkdirSync(STATE_DIR, { recursive: true });
const QUEUE_FILE = join(STATE_DIR, "alert-queue.json");
const SENT_FILE = join(STATE_DIR, "alert-sent.json");
// Same lockfile watcher.mjs's sendAlert() uses — the two processes append to
// and drain QUEUE_FILE independently (watcher: persistent poller, this
// script: a frequent cron), so without a shared lock either side's
// read-modify-write can silently clobber the other's concurrent change.
const QUEUE_LOCK_FILE = join(STATE_DIR, "alert-queue.lock");
const LOCK_STALE_MS = 30000;

function log(msg) {
  console.log(`[${new Date().toISOString()}] ${msg}`);
}

function sleepSync(ms) {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}
function withQueueLock(fn) {
  const deadline = Date.now() + 20000;
  let acquired = false;
  for (;;) {
    try { closeSync(openSync(QUEUE_LOCK_FILE, "wx")); acquired = true; break; }
    catch (e) {
      if (e.code !== "EEXIST") throw e;
      try {
        if (Date.now() - statSync(QUEUE_LOCK_FILE).mtimeMs > LOCK_STALE_MS) { unlinkSync(QUEUE_LOCK_FILE); continue; }
      } catch {}
      if (Date.now() > deadline) throw new Error("alert-queue lock timed out");
      sleepSync(50 + Math.floor(Math.random() * 100));
    }
  }
  try { return fn(); } finally { if (acquired) try { unlinkSync(QUEUE_LOCK_FILE); } catch {} }
}

function sendTelegram(message) {
  try {
    execFileSync("openclaw", ["message", "send", "--channel", "telegram", "--message", message], { timeout: 15000, windowsHide: true, stdio: "ignore" });
    return true;
  } catch (e) {
    log(`Telegram send failed: ${e.message}`);
    return false;
  }
}

function main() {
  withQueueLock(() => {
    if (!existsSync(QUEUE_FILE)) {
      log("No queue file");
      return;
    }

    let queue = [];
    try { queue = JSON.parse(readFileSync(QUEUE_FILE, "utf8")); } catch { queue = []; }
    if (!queue.length) { log("Queue empty"); return; }

    let sent = [];
    if (existsSync(SENT_FILE)) {
      try { sent = JSON.parse(readFileSync(SENT_FILE, "utf8")); } catch {}
    }

    const newQueue = [];
    let sentCount = 0;

    for (const item of queue) {
      // Dedupe by a full-content hash — a truncated base64 prefix only covers
      // the first ~24 bytes, which for these fixed-template messages is often
      // just the emoji + label, so distinct alerts (same asset/pattern, a
      // different price level further into the string) could collide and get
      // silently dropped as "already sent".
      const hash = createHash("sha1").update(item.message).digest("hex");
      if (sent.includes(hash)) {
        // Already sent, drop
        continue;
      }

      log(`Sending alert: ${item.message.slice(0, 80)}...`);
      if (sendTelegram(item.message)) {
        sent.push(hash);
        sentCount++;
        if (sent.length > 200) sent = sent.slice(-200);
      } else {
        // Keep in queue for retry
        newQueue.push(item);
      }
    }

    writeFileSync(QUEUE_FILE, JSON.stringify(newQueue, null, 2));
    writeFileSync(SENT_FILE, JSON.stringify(sent, null, 2));

    log(`Done. Sent ${sentCount}, ${newQueue.length} remaining in queue.`);
  });
}

main();