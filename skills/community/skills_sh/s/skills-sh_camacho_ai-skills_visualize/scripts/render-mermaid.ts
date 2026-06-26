#!/usr/bin/env -S node --import tsx
// render-mermaid.ts — Render Mermaid diagram to PNG via @mermaid-js/mermaid-cli.
// Run from this skill: node --import tsx "${SKILL_DIR}/scripts/render-mermaid.ts" --input <file> --output <png> [--width N] [--height N]
// Or: "${SKILL_DIR}/scripts/render-mermaid.ts" --input <file> --output <png> (if chmod +x and tsx installed)

import { execFileSync } from "node:child_process";
import { readFileSync, unlinkSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const args = process.argv.slice(2);

if (args.includes("--help") || args.length === 0) {
  console.log(`Usage: node --import tsx "\${SKILL_DIR}/scripts/render-mermaid.ts" --input <file> --output <png> [options]

Renders a Mermaid diagram file to PNG using @mermaid-js/mermaid-cli (mmdc).

Options:
  --input <file>    Mermaid source file (or - for stdin)
  --output <path>   Output PNG path (required)
  --width <px>      Width in pixels (default: 2400)
  --height <px>     Height in pixels (default: 1800)
  --help            Show this help

Examples:
  node --import tsx "\${SKILL_DIR}/scripts/render-mermaid.ts" --input diagram.mmd --output diagram.png
  echo 'graph LR; A-->B' | node --import tsx "\${SKILL_DIR}/scripts/render-mermaid.ts" --input - --output out.png`);
  process.exit(0);
}

function getArg(name: string, fallback?: string): string {
  const idx = args.indexOf(name);
  if (idx === -1 || idx + 1 >= args.length) {
    if (fallback !== undefined) return fallback;
    process.stderr.write(`Error: ${name} is required.\n`);
    process.exit(1);
  }
  return args[idx + 1] as string;
}

const inputPath = getArg("--input");
const outputPath = getArg("--output");
const width = getArg("--width", "2400");
const height = getArg("--height", "1800");

let mermaidSource: string;
if (inputPath === "-") {
  mermaidSource = readFileSync(0, "utf-8");
} else {
  mermaidSource = readFileSync(inputPath, "utf-8");
}

// Write to temp file if reading from stdin
let inputFile = inputPath;
if (inputPath === "-") {
  inputFile = resolve(outputPath + ".tmp.mmd");
  writeFileSync(inputFile, mermaidSource, "utf-8");
}

try {
  execFileSync("npx", [
    "mmdc",
    "-i", inputFile,
    "-o", outputPath,
    "-w", width,
    "-H", height,
    "--quiet",
  ], {
    stdio: ["pipe", "pipe", "pipe"],
    timeout: 30_000,
  });
  console.log(outputPath);
} catch (err) {
  const error = err as { stderr?: Buffer };
  process.stderr.write(`Error rendering Mermaid: ${error.stderr?.toString() ?? "unknown error"}\n`);
  process.exit(1);
} finally {
  if (inputPath === "-") {
    try { unlinkSync(inputFile); } catch { /* ignore */ }
  }
}
