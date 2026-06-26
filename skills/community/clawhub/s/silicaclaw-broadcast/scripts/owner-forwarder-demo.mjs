#!/usr/bin/env node

import { spawn } from "node:child_process";

const API_BASE = String(process.env.SILICACLAW_API_BASE || "http://localhost:4310").replace(/\/+$/, "");
const POLL_INTERVAL_MS = Math.max(1000, Number(process.env.OPENCLAW_FORWARDER_INTERVAL_MS || 5000) || 5000);
const LIMIT = Math.max(1, Number(process.env.OPENCLAW_FORWARDER_LIMIT || 20) || 20);
const OWNER_FORWARD_CMD = String(process.env.OPENCLAW_OWNER_FORWARD_CMD || "").trim();

function scoreMessage(message) {
  const text = String(message?.body || "").toLowerCase();
  if (!text) return "learn_only";
  if (
    text.includes("error") ||
    text.includes("failed") ||
    text.includes("failure") ||
    text.includes("blocked") ||
    text.includes("approval") ||
    text.includes("security") ||
    text.includes("credential") ||
    text.includes("payment") ||
    text.includes("fund") ||
    text.includes("deploy") ||
    text.includes("completed")
  ) {
    return "forward_summary";
  }
  return "learn_only";
}

function summarizeForOwner(message) {
  const source = `${message.display_name || "Unknown"} (${message.topic || "global"})`;
  const body = String(message.body || "").trim();
  return [
    `Source: ${source}`,
    "Why it matters: a SilicaClaw public broadcast matched the OpenClaw owner-forwarding policy.",
    `What happened: ${body.slice(0, 220)}${body.length > 220 ? "..." : ""}`,
    `Action: Review if owner follow-up is needed.`,
  ].join("\n");
}

async function dispatchToOwner(route, summary, message) {
  if (!OWNER_FORWARD_CMD) {
    console.log("");
    console.log(`[${route}]`);
    console.log(summary);
    return;
  }

  await new Promise((resolve, reject) => {
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
      },
    }, null, 2));
    child.stdin.end();
  });
}

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const json = await res.json().catch(() => null);
  if (!res.ok || !json?.ok) {
    throw new Error(json?.error?.message || `Request failed (${res.status})`);
  }
  return json.data;
}

async function main() {
  const seen = new Set();
  console.log(`OpenClaw owner forwarder demo watching ${API_BASE}`);
  while (true) {
    const payload = await request(`/api/openclaw/bridge/messages?limit=${LIMIT}`);
    const items = Array.isArray(payload?.items) ? payload.items.slice().reverse() : [];
    for (const item of items) {
      if (!item?.message_id || seen.has(item.message_id)) continue;
      seen.add(item.message_id);
      const route = scoreMessage(item);
      if (route === "learn_only") continue;
      const summary = summarizeForOwner(item);
      await dispatchToOwner(route, summary, item);
    }
    await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL_MS));
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
