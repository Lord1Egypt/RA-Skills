#!/usr/bin/env node

import { clearCache, getCacheStats } from "./lib/cache.mjs";
import { loadRuntimeConfig } from "./lib/config.mjs";
import { buildCacheOutput } from "./lib/output.mjs";

function usage(exitCode = 2) {
  console.error(`web-search-pro cache

Usage:
  cache.mjs stats [--json]
  cache.mjs clear [--json]`);
  process.exit(exitCode);
}

function formatCacheMarkdown(report) {
  const lines = [];
  lines.push("# web-search-pro cache");
  lines.push("");
  lines.push(`- Action: ${report.action}`);
  lines.push(`- Enabled: ${report.enabled ? "yes" : "no"}`);
  lines.push(`- Directory: ${report.dir}`);
  if (report.entries !== undefined) {
    lines.push(`- Entries: ${report.entries}`);
  }
  if (report.bytes !== undefined) {
    lines.push(`- Bytes: ${report.bytes}`);
  }
  if (report.removedEntries !== undefined) {
    lines.push(`- Removed entries: ${report.removedEntries}`);
  }
  return lines.join("\n");
}

const args = process.argv.slice(2);
const command = args[0];
const json = args.includes("--json");

if (!command || args.includes("-h") || args.includes("--help")) {
  usage(command ? 0 : 2);
}
if (!["stats", "clear"].includes(command) || args.some((arg, index) => index > 0 && arg !== "--json")) {
  usage();
}

const cwd = process.cwd();
const env = process.env;
const { config } = loadRuntimeConfig({ cwd, env });
const report =
  command === "clear"
    ? {
        action: "clear",
        enabled: config.cache.enabled,
        ...(await clearCache({ cwd, config })),
      }
    : {
        action: "stats",
        ...(await getCacheStats({ cwd, config, now: Date.now() })),
      };
const payload = buildCacheOutput(report);

if (json) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  console.log(formatCacheMarkdown(payload));
}
