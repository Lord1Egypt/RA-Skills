#!/usr/bin/env node

import { loadRuntimeConfig } from "./lib/config.mjs";
import { buildDoctorReport, formatDoctorMarkdown } from "./lib/doctor.mjs";
import { buildDoctorOutput } from "./lib/output.mjs";

function usage(exitCode = 2) {
  console.error(`web-search-pro doctor

Usage:
  doctor.mjs [--json]`);
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
const report = await buildDoctorReport({
  cwd,
  env,
  config: runtime.config,
  configMeta: runtime.meta,
  now: Date.now(),
});
const payload = buildDoctorOutput(report);

if (args.includes("--json")) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  console.log(formatDoctorMarkdown(payload));
}
