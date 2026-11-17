#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { existsSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

function usage() {
  console.error("Usage: node scripts/run-w3c-validator.mjs <input.html> <output.json> [source-url]");
}

const [inputPath, outputPath, sourceUrl] = process.argv.slice(2);
if (!inputPath || !outputPath) {
  usage();
  process.exit(64);
}

const absoluteInput = resolve(inputPath);
if (!existsSync(absoluteInput)) {
  console.error(`Input file not found: ${absoluteInput}`);
  process.exit(66);
}

const result = spawnSync("vnu", ["--format", "json", absoluteInput], { encoding: "utf8" });
if (result.error) {
  console.error("Unable to start vnu. Install vnu-jar and ensure Java is available.");
  console.error(result.error.message);
  process.exit(69);
}

const stdoutReport = result.stdout.trim();
const stderrReport = result.stderr.trim();
let rawReport = stdoutReport || stderrReport;

// Try to parse the entire rawReport as JSON first.
let parsed;
try {
  parsed = JSON.parse(rawReport);
} catch (err) {
  // If that fails, try to find a JSON object in the output.
  // Look for a line that starts with '{' and ends with '}'
  const lines = rawReport.split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('{') && trimmed.endsWith('}')) {
      try {
        parsed = JSON.parse(trimmed);
        break;
      } catch (e) {
        // Not valid JSON, continue
      }
    }
  }
  if (!parsed) {
    console.error("Nu checker did not return JSON.");
    console.error(`Raw report (${rawReport.length} chars): ${rawReport}`);
    if (result.stderr) console.error(`stderr: ${result.stderr.trim()}`);
    process.exit(70);
  }
}

// This report validates the raw HTTP response markup only. It does not see
// DOM mutations produced by JavaScript, authenticated routes, or other
// post-load states — those require the browser-based tools (axe, Pa11y,
// QualWeb) run against each relevant state.
const report = {
  scope: "source-html",
  scopeNote: "Validates the raw HTTP response body, not the JavaScript-rendered DOM.",
  sourceUrl: sourceUrl ?? null,
  messages: parsed.messages ?? [],
};

writeFileSync(resolve(outputPath), JSON.stringify(report));

// vnu exits non-zero when it finds markup errors, same as it would for a
// technical fault. This script's job is only to produce the report (as
// axe/Pa11y/QualWeb do above in a11y-audit.sh), not to gate on findings, so
// always exit 0 once the report has been written successfully.
process.exit(0);
