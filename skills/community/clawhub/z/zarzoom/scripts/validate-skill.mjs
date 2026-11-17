#!/usr/bin/env node
/**
 * openclaw-skill/scripts/validate-skill.mjs
 *
 * Validates SKILL.md against the ClawHub frontmatter spec before
 * submission. Lint-style — fails fast with a clear message; doesn't
 * try to be comprehensive (ClawHub's server runs the canonical check
 * at publish time).
 *
 * Run via:
 *   node openclaw-skill/scripts/validate-skill.mjs
 *
 * Exits 0 on success, 1 on validation failure.
 *
 * Reference: docs.openclaw.ai/tools/skills + openclaw/clawhub/docs/skill-format.md
 */

import { readFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_PATH = resolve(__dirname, "..", "SKILL.md");

const errors = [];
const warn = (msg) => console.warn("[warn]", msg);
const fail = (msg) => errors.push(msg);

let raw;
try {
  raw = readFileSync(SKILL_PATH, "utf8");
} catch (err) {
  console.error(`[fatal] Could not read ${SKILL_PATH}:`, err.message);
  process.exit(1);
}

// Extract YAML frontmatter (between the first two `---` lines).
const fmMatch = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
if (!fmMatch) {
  fail("SKILL.md is missing YAML frontmatter (must start with `---` ... `---`).");
} else {
  const fm = fmMatch[1];
  const body = fmMatch[2];

  // Parse with a minimal hand-rolled YAML reader — we only support
  // single-line key: value pairs + simple lists, which is all the
  // ClawHub spec accepts anyway ("frontmatter keys must be single-line").
  const fields = {};
  let inList = null;
  for (const line of fm.split(/\r?\n/)) {
    const stripped = line.replace(/^\s+/, "");
    if (stripped === "" || stripped.startsWith("#")) continue;

    const listItem = line.match(/^\s+-\s+(.*)$/);
    if (listItem && inList) {
      fields[inList].push(listItem[1].trim());
      continue;
    }
    inList = null;

    const kv = line.match(/^([a-zA-Z_][\w.-]*)\s*:\s*(.*)$/);
    if (!kv) continue;
    const [, key, value] = kv;
    if (value === "") {
      fields[key] = [];
      inList = key;
    } else {
      fields[key] = value.trim().replace(/^["']|["']$/g, "");
    }
  }

  // Required fields per ClawHub skill-format spec.
  if (!fields.name) fail("frontmatter is missing required field `name`.");
  else if (!/^[a-z][a-z0-9-]*$/.test(fields.name)) {
    fail(`frontmatter \`name\` must be lowercase + hyphens (got "${fields.name}").`);
  }

  if (!fields.description) fail("frontmatter is missing required field `description`.");
  else if (fields.description.length < 20) {
    warn(`frontmatter \`description\` is very short (${fields.description.length} chars); aim for ≥ 50 for vector-search ranking.`);
  } else if (fields.description.length > 500) {
    warn(`frontmatter \`description\` is long (${fields.description.length} chars); ClawHub may truncate.`);
  }

  // Optional but strongly recommended.
  if (!fields.version) warn("frontmatter has no `version` (semver recommended).");
  else if (!/^\d+\.\d+\.\d+(-[\w.]+)?$/.test(fields.version)) {
    fail(`frontmatter \`version\` should be semver (got "${fields.version}").`);
  }

  if (!fields.homepage) warn("frontmatter has no `homepage` URL.");
  else if (!/^https?:\/\//.test(fields.homepage)) {
    fail(`frontmatter \`homepage\` must be an http(s) URL (got "${fields.homepage}").`);
  }

  if (!fields.primaryEnv && !fields.requires?.length) {
    warn("frontmatter declares no `primaryEnv` or `requires.env` — is this skill really credential-free?");
  }

  // Body sanity checks.
  if (body.trim().length < 200) {
    fail("SKILL.md body is suspiciously short (<200 chars). The body is what guides the model — it should be substantial.");
  }
}

// Print + exit.
if (errors.length === 0) {
  console.log("[ok] SKILL.md frontmatter validates.");
  process.exit(0);
} else {
  console.error("[fail] SKILL.md validation failed:");
  for (const e of errors) console.error("  -", e);
  process.exit(1);
}
