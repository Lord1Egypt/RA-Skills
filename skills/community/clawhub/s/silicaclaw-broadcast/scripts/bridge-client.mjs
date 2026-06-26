#!/usr/bin/env node

const API_BASE = String(process.env.SILICACLAW_API_BASE || "http://localhost:4310").replace(/\/+$/, "");
const argv = process.argv.slice(2);
const cmd = String(argv[0] || "status").trim().toLowerCase();

function parseFlag(name, fallback = "") {
  const prefix = `--${name}=`;
  for (const item of argv.slice(1)) {
    if (item.startsWith(prefix)) return item.slice(prefix.length);
  }
  return fallback;
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
  if (cmd === "status") {
    console.log(JSON.stringify(await request("/api/openclaw/bridge"), null, 2));
    return;
  }
  if (cmd === "profile") {
    console.log(JSON.stringify(await request("/api/openclaw/bridge/profile"), null, 2));
    return;
  }
  if (cmd === "messages") {
    const limit = Number(parseFlag("limit", "10")) || 10;
    console.log(JSON.stringify(await request(`/api/openclaw/bridge/messages?limit=${limit}`), null, 2));
    return;
  }
  if (cmd === "send") {
    const body = parseFlag("body", "");
    if (!body.trim()) {
      throw new Error("Missing --body=... for send");
    }
    console.log(JSON.stringify(await request("/api/openclaw/bridge/message", {
      method: "POST",
      body: JSON.stringify({ body }),
    }), null, 2));
    return;
  }

  throw new Error(`Unknown command: ${cmd}`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
