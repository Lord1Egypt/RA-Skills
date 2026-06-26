#!/usr/bin/env node

import { buildBootstrapReport } from "./lib/bootstrap.mjs";
import { loadRuntimeConfig } from "./lib/config.mjs";
import { buildBootstrapOutput, formatBootstrapMarkdown } from "./lib/output.mjs";

function usage(exitCode = 2) {
  console.error(`web-search-pro bootstrap

Usage:
  bootstrap.mjs [--json]`);
  process.exit(exitCode);
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
const runtime = loadRuntimeConfig({ cwd, env });
const report = await buildBootstrapReport({
  cwd,
  env,
  config: runtime.config,
  configMeta: runtime.meta,
  now: Date.now(),
});
const payload = buildBootstrapOutput(report);

if (args.includes("--json")) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  console.log(formatBootstrapMarkdown(payload));
}
