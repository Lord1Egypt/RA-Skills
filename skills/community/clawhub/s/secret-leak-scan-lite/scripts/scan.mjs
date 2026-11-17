#!/usr/bin/env node
// secret-leak-scan-lite: static pattern scan for leaked credentials in a
// project directory. Raw values are never returned, logged, or written:
// every finding carries only the credential type, file, line, and a masked
// fingerprint (first 4 chars + length + first 8 hex of sha256).
//
// Lite edition: directory input only, core pattern set.
// The full version adds .asar scanning, more credential types, the triage
// workflow, git-history cleanup, and a CI gate recipe.
//
// Usage: node scan.mjs <directory>
// Stdout: JSON report only. Exit codes: 0 = no findings, 1 = findings, 2 = error.

import { createHash } from "node:crypto";
import { promises as fs } from "node:fs";
import path from "node:path";

const NOTICE =
  "secret-leak-scan-lite: static secret scanner. Use it only on files you own or are authorized to analyze. Findings are masked; rotate anything it flags.";

const usage = `Usage:
  node scan.mjs <directory>

Prints a JSON report to stdout. Exit codes:
  0  no findings
  1  findings present
  2  usage or read error`;

// ---------- masked matching ----------

const MAX_FILE_BYTES = 5 * 1024 * 1024;
const MAX_FINDINGS_PER_FILE = 20;

const PATTERNS = [
  ["aws-access-key-id", /\bAKIA[0-9A-Z]{16}\b/g],
  ["github-personal-access-token", /\bghp_[A-Za-z0-9]{36}\b/g],
  ["slack-token", /\bxox[baprs]-[A-Za-z0-9-]{10,}\b/g],
  ["private-key-block", /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/g],
];

const sha256hex = (text) =>
  createHash("sha256").update(text, "utf8").digest("hex");

const fingerprint = (raw) =>
  `${raw.slice(0, 4)}… (len=${raw.length}, sha256:${sha256hex(raw).slice(0, 8)})`;

const looksBinary = (buf) => buf.subarray(0, 8192).includes(0);

const lineOf = (text, index) => {
  let line = 1;
  for (let i = 0; i < index; i++) if (text.charCodeAt(i) === 10) line++;
  return line;
};

// ---------- input layer ----------
// Paths returned by listFiles() are always relative, forward-slash separated,
// and safe to pass back to readBuffer(). Symlinks are never followed.

class DirInput {
  constructor(root) {
    this.kind = "directory";
    this.root = root;
    this.notes = [];
  }

  async listFiles() {
    const out = [];
    const walk = async (rel) => {
      let entries;
      try {
        entries = await fs.readdir(path.join(this.root, rel), {
          withFileTypes: true,
        });
      } catch {
        this.notes.push(`skipped ${rel || "."}: unreadable directory`);
        return;
      }
      for (const entry of entries) {
        const relPath = rel ? `${rel}/${entry.name}` : entry.name;
        if (entry.isDirectory()) await walk(relPath);
        else if (entry.isFile()) {
          try {
            const st = await fs.stat(path.join(this.root, relPath));
            out.push({ path: relPath, size: st.size });
          } catch {
            this.notes.push(`skipped ${relPath}: unreadable`);
          }
        }
      }
    };
    await walk("");
    return out;
  }

  async readBuffer(relPath) {
    return fs.readFile(path.join(this.root, relPath));
  }
}

async function openInput(rootPath) {
  const st = await fs.stat(rootPath);
  if (st.isDirectory()) return new DirInput(rootPath);
  throw new Error(`Input must be a directory: ${rootPath}`);
}

// ---------- scan ----------

/** Scan every file in input; returns masked findings + notes + counts. */
async function scanInput(input) {
  const findings = [];
  const notes = [];
  let filesScanned = 0;
  let filesSkipped = 0;
  for (const file of await input.listFiles()) {
    if (file.size != null && file.size > MAX_FILE_BYTES) {
      filesSkipped++;
      notes.push(`skipped ${file.path}: larger than 5 MB`);
      continue;
    }
    let buf;
    try {
      buf = await input.readBuffer(file.path);
    } catch {
      filesSkipped++;
      notes.push(`skipped ${file.path}: unreadable`);
      continue;
    }
    if (buf.length > MAX_FILE_BYTES) {
      filesSkipped++;
      notes.push(`skipped ${file.path}: larger than 5 MB`);
      continue;
    }
    if (looksBinary(buf)) continue;
    filesScanned++;
    const text = buf.toString("utf8");
    let count = 0;
    for (const [type, pattern] of PATTERNS) {
      pattern.lastIndex = 0;
      let m;
      while ((m = pattern.exec(text)) !== null) {
        if (count < MAX_FINDINGS_PER_FILE) {
          findings.push({
            type,
            file: file.path,
            line: lineOf(text, m.index),
            fingerprint: fingerprint(m[0]),
          });
        }
        count++;
      }
    }
    if (count > MAX_FINDINGS_PER_FILE)
      notes.push(
        `${file.path}: ${count - MAX_FINDINGS_PER_FILE} further match(es) suppressed (per-file cap ${MAX_FINDINGS_PER_FILE})`,
      );
  }
  findings.sort(
    (a, b) =>
      a.file.localeCompare(b.file) ||
      a.line - b.line ||
      a.type.localeCompare(b.type),
  );
  notes.push(...(input.notes ?? []));
  return { findings, notes, filesScanned, filesSkipped };
}

// ---------- CLI ----------

const main = async () => {
  console.error(NOTICE);
  const argv = process.argv.slice(2).filter((a) => a !== "--");
  if (argv.includes("--help") || argv.includes("-h")) {
    console.error(usage);
    process.exit(0);
  }
  if (argv.length !== 1 || argv[0].startsWith("-")) {
    console.error(usage);
    process.exit(2);
  }

  const input = await openInput(argv[0]);
  const { findings, notes, filesScanned, filesSkipped } =
    await scanInput(input);

  const byType = {};
  for (const f of findings) byType[f.type] = (byType[f.type] ?? 0) + 1;

  const report = {
    tool: "secret-leak-scan-lite",
    version: "1.0.0",
    generatedAt: new Date().toISOString(),
    input: { path: path.resolve(argv[0]), kind: input.kind },
    summary: {
      filesScanned,
      filesSkipped,
      findings: findings.length,
      byType,
    },
    findings,
    notes,
  };
  process.stdout.write(JSON.stringify(report, null, 2) + "\n");
  process.exit(findings.length > 0 ? 1 : 0);
};

main().catch((err) => {
  console.error(`error: ${err.message}`);
  process.exit(2);
});
