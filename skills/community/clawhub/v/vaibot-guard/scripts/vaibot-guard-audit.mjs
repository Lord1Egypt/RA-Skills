#!/usr/bin/env node
/**
 * vaibot-guard-audit
 *
 * Recompute checkpoint roots and checkpoint hash chain from local files.
 *
 * Usage:
 *   VAIBOT_GUARD_LOG_DIR=... node scripts/vaibot-guard-audit.mjs --session_id <id>
 */

import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const WORKSPACE = process.env.VAIBOT_WORKSPACE || process.cwd();
const LOG_DIR = process.env.VAIBOT_GUARD_LOG_DIR || path.join(WORKSPACE, ".vaibot-guard");
// Reserved for future improvements; checkpoint hashing is sha256 for now.
const CHECKPOINT_HASH_ALG = (process.env.VAIBOT_CHECKPOINT_HASH_ALG || "").toLowerCase();

function die(msg, code = 2) {
  console.error(msg);
  process.exit(code);
}

function stableStringify(value) {
  if (value === null || value === undefined) return JSON.stringify(value);
  if (typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return "[" + value.map((v) => stableStringify(v)).join(",") + "]";
  const keys = Object.keys(value).sort();
  return "{" + keys.map((k) => JSON.stringify(k) + ":" + stableStringify(value[k])).join(",") + "}";
}

function sha256(s) {
  return createHash("sha256").update(s).digest("hex");
}

function hashCheckpoint(data) {
  // Intentionally ignore CHECKPOINT_HASH_ALG for now (future migration knob).
  return sha256(data);
}

function parentHash(left, right) {
  return sha256("node:" + left + ":" + right);
}

function nextLevel(nodes) {
  const out = [];
  for (let i = 0; i < nodes.length; i += 2) {
    const left = nodes[i];
    const right = nodes[i + 1] || nodes[i];
    out.push(parentHash(left, right));
  }
  return out;
}

function computeRootFromLeaves(leaves) {
  if (leaves.length === 0) return sha256("empty");
  let level = leaves.slice();
  while (level.length > 1) level = nextLevel(level);
  return level[0];
}

function readJsonl(filePath) {
  if (!fs.existsSync(filePath)) return [];
  return fs
    .readFileSync(filePath, "utf8")
    .split("\n")
    .filter(Boolean)
    .map((l) => JSON.parse(l));
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const k = a.slice(2);
      const v = argv[i + 1];
      out[k] = v;
      i++;
    } else out._.push(a);
  }
  return out;
}

const flags = parseArgs(process.argv.slice(2));
const sessionId = flags.session_id || flags.sessionId;
if (!sessionId) die("Missing --session_id");

const cpFile = path.join(LOG_DIR, `${sessionId}.checkpoints.jsonl`);
const leavesFile = path.join(LOG_DIR, `${sessionId}.leaves.jsonl`);

const cps = readJsonl(cpFile);
const leavesRows = readJsonl(leavesFile);
const leaves = leavesRows.map((r) => String(r.leaf));

if (cps.length === 0) die(`No checkpoints found at ${cpFile}`);
if (leaves.length === 0) die(`No leaves found at ${leavesFile}`);

let ok = true;
let prevHash = "";
for (const cp of cps) {
  const count = Number(cp.count);
  const root = computeRootFromLeaves(leaves.slice(0, count));
  const rootOk = root === cp.root;

  const { hash: _h, ...cpNoHash } = cp;
  const expectedHash = hashCheckpoint("checkpoint:" + stableStringify(cpNoHash));
  const hashOk = expectedHash === cp.hash;

  const chainOk = (cp.prevCheckpointHash || "") === prevHash;

  console.error(
    `checkpoint seq=${cp.seq} count=${count} rootOk=${rootOk} hashOk=${hashOk} chainOk=${chainOk}`
  );

  if (!rootOk || !hashOk || !chainOk) ok = false;
  prevHash = cp.hash;
}

if (!ok) process.exit(1);
console.error("audit: OK");
