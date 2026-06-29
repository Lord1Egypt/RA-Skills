#!/usr/bin/env node
/**
 * RedReplier Mean Marketer — thin loop client.
 *
 * ALL logic lives in the RedReplier backend (criteria, escalation, the roast copy).
 * This script only: reads/sets config, calls the poll endpoint each tick, and relays
 * the server-generated message + opportunity link. It contains NO insults and NO
 * decision-making of its own — by design.
 *
 * Zero dependencies. Reuses your existing RedReplier API key.
 * MIT Licensed.
 */
const fs = require("fs");
const path = require("path");
const os = require("os");

const API_BASE = "https://ai.redreplier.com/ai-app";
const CONFIG_DIR = path.join(os.homedir(), ".config", "redreplier");
const CONFIG_FILE = path.join(CONFIG_DIR, "config.json");
const LOCAL_CONFIG = path.join(process.cwd(), ".redreplier", "config.json");

// ── API key (shared with the base redreplier skill) ─────────────────────────

function getApiKey() {
  if (process.env.REDREPLIER_API_KEY) return process.env.REDREPLIER_API_KEY;
  for (const f of [LOCAL_CONFIG, CONFIG_FILE]) {
    if (fs.existsSync(f)) {
      try {
        return JSON.parse(fs.readFileSync(f, "utf8")).apiKey;
      } catch {}
    }
  }
  return null;
}

function saveApiKey(key) {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  fs.writeFileSync(CONFIG_FILE, JSON.stringify({ apiKey: key }, null, 2));
}

// ── HTTP ─────────────────────────────────────────────────────────────────────

async function request(method, endpoint, body = null) {
  const apiKey = getApiKey();
  if (!apiKey) {
    error(
      "No API key found. Run: ./scripts/mean-marketer.js setup --key redreplier_xxxxx",
    );
    error("Get your API key at: https://redreplier.com/api-tokens");
    process.exit(1);
  }
  const headers = {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  };
  const options = { method, headers };
  if (body) options.body = JSON.stringify(body);

  const res = await fetch(`${API_BASE}${endpoint}`, options);
  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : { ok: true };
  } catch {
    data = { raw: text };
  }
  if (!res.ok) {
    error(`API error (${res.status}): ${JSON.stringify(data)}`);
    process.exit(1);
  }
  return data;
}

function output(data) {
  console.log(JSON.stringify(data, null, 2));
}
function error(msg) {
  console.error(`\x1b[31mError:\x1b[0m ${msg}`);
}
function info(msg) {
  console.error(`\x1b[36mInfo:\x1b[0m ${msg}`);
}

function parseArgs(args) {
  const parsed = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const key = args[i].slice(2);
      const next = args[i + 1];
      if (!next || next.startsWith("--")) parsed[key] = true;
      else {
        parsed[key] = next;
        i++;
      }
    }
  }
  return parsed;
}

// ── Commands (each maps 1:1 to a backend endpoint) ───────────────────────────

const COMMANDS = {
  setup: async (args) => {
    const parsed = parseArgs(args);
    const key = parsed.key || parsed["api-key"];
    if (!key) {
      error("Usage: ./scripts/mean-marketer.js setup --key redreplier_xxxxx");
      process.exit(1);
    }
    saveApiKey(key);
    info("API key saved (shared with the redreplier skill).");
    output({ status: "configured" });
  },

  // GET/PUT the criteria the backend uses. The user controls everything here.
  config: async (args) => {
    const parsed = parseArgs(args);
    const body = {};
    if (parsed["min-score"] !== undefined)
      body.minScore = parseInt(parsed["min-score"], 10);
    if (parsed.enabled !== undefined)
      body.enabled = parsed.enabled === true || parsed.enabled === "true";
    if (parsed.profanity !== undefined)
      body.profanity = parsed.profanity === true || parsed.profanity === "true";
    if (parsed.website !== undefined) body.websiteId = parsed.website;

    if (Object.keys(body).length === 0) {
      output(await request("GET", "/api/v1/mean-marketer/config"));
      return;
    }
    output(await request("PUT", "/api/v1/mean-marketer/config", body));
  },

  // The heartbeat. One call = one loop tick. Returns the full JSON.
  poll: async () => {
    output(await request("POST", "/api/v1/mean-marketer/poll"));
  },

  // Cron/loop entrypoint. Polls once and prints ONLY the user-facing text — the
  // roast plus the opportunity link — or nothing at all when there's nothing to say.
  // Empty stdout = "stay quiet this tick", which is exactly what a no-agent cron wants.
  // IMPORTANT: a poll mutates server state (hands the lead over, advances the clock),
  // so always let this deliver its output — never poll just to peek.
  notify: async () => {
    const data = await request("POST", "/api/v1/mean-marketer/poll");

    // Stay silent when the server says there's nothing worth pinging about.
    if (!data || data.enabled === false) return;
    if (!data.message) return;
    if (data.noNewOpportunity && !data.beMean) return;

    const lines = [String(data.message)];
    const opp = data.opportunity;
    if (opp) {
      lines.push("");
      lines.push("Opportunity:");
      if (opp.title) lines.push(`- Title: ${opp.title}`);
      if (opp.url) lines.push(`- Link: ${opp.url}`);
      if (opp.source) {
        lines.push(
          `- Source: ${opp.source}${opp.subreddit ? ` (r/${opp.subreddit})` : ""}`,
        );
      }
      if (opp.relevanceScore != null)
        lines.push(`- Score: ${opp.relevanceScore}/100`);
      if (opp.relevanceReason) lines.push(`- Why: ${opp.relevanceReason}`);
      lines.push(`- ID: ${opp.id}  (reply "approve" or "reject" to triage)`);
    }
    console.log(lines.join("\n").trim());
  },

  // Clear the outstanding-lead memory + strike count.
  reset: async () => {
    output(await request("POST", "/api/v1/mean-marketer/reset"));
  },

  // Close the loop when the user replies approve/reject (reuses the core API).
  triage: async (args) => {
    const parsed = parseArgs(args);
    if (!parsed.id || !parsed.status) {
      error(
        "Usage: ./scripts/mean-marketer.js triage --id <mention_id> --status APPROVED|REJECTED|NEW",
      );
      process.exit(1);
    }
    output(
      await request("PATCH", `/api/v1/mentions/${parsed.id}/status`, {
        status: parsed.status,
      }),
    );
  },

  help: async () => {
    output({
      name: "RedReplier Mean Marketer (thin client)",
      commands: Object.keys(COMMANDS).filter((c) => c !== "help"),
      docs: "https://redreplier.com",
    });
  },
};

async function main() {
  const command = process.argv[2] || "help";
  const args = process.argv.slice(3);
  if (!COMMANDS[command]) {
    error(`Unknown command: ${command}`);
    error(`Available: ${Object.keys(COMMANDS).join(", ")}`);
    process.exit(1);
  }
  try {
    await COMMANDS[command](args);
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}

main();
