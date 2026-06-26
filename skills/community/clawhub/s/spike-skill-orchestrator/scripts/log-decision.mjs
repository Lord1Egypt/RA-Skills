#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const LOG_PATH = "/Users/spikescp/.openclaw/workspace/openclaw-evolution/data/skill-orchestrator-log.jsonl";

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) continue;
    const key = arg.slice(2);
    const value = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : "";
    out[key] = value;
  }
  return out;
}

const args = parseArgs(process.argv.slice(2));

const row = {
  ts: new Date().toISOString(),
  task: args.task || "",
  proposed: args.proposed ? args.proposed.split(",").map((s) => s.trim()).filter(Boolean) : [],
  accepted: args.accepted ? args.accepted.split(",").map((s) => s.trim()).filter(Boolean) : [],
  mode: args.mode || "unknown",
};

fs.mkdirSync(path.dirname(LOG_PATH), { recursive: true });
fs.appendFileSync(LOG_PATH, `${JSON.stringify(row)}\n`, "utf-8");
console.log(`logged -> ${LOG_PATH}`);
