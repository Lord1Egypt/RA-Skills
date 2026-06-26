#!/usr/bin/env node

import { loadRuntimeConfig } from "./lib/config.mjs";
import { buildHealthSnapshot } from "./lib/health-state.mjs";
import { buildHealthOutput } from "./lib/output.mjs";

function usage(exitCode = 2) {
  console.error(`web-search-pro health

Usage:
  health.mjs [--json]`);
  process.exit(exitCode);
}

function formatHealthMarkdown(report) {
  const lines = [];
  lines.push("# web-search-pro health");
  lines.push("");
  for (const [providerId, state] of Object.entries(report.providers)) {
    lines.push(
      `- ${providerId}: status=${state.status}, failures=${state.consecutiveFailures}, cooldownUntil=${
        state.cooldownUntil ?? "none"
      }`,
    );
  }
  return lines.join("\n");
}

const args = process.argv.slice(2);
if (args.some((arg) => arg === "-h" || arg === "--help")) {
  usage(0);
}
if (args.some((arg) => arg !== "--json")) {
  usage();
}

const cwd = process.cwd();
const env = process.env;
const { config } = loadRuntimeConfig({ cwd, env });
const snapshot = await buildHealthSnapshot({ cwd, config, now: Date.now() });
const payload = buildHealthOutput(snapshot);

if (args.includes("--json")) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  console.log(formatHealthMarkdown(payload));
}
