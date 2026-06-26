#!/usr/bin/env node
/**
 * scripts/audit.mjs
 *
 * Static audit for a Next.js project that follows the
 * nextjs-cache-architecture skill. Runs the checks from the
 * post-implementation checklist that can be verified without executing
 * the app.
 *
 * Usage:
 *   node scripts/audit.mjs <project-root>
 *   node scripts/audit.mjs .
 *
 * Exit codes:
 *   0 — all checks passed
 *   1 — at least one check failed
 *   2 — bad invocation / project not found
 *
 * Zero runtime dependencies. Node 18+.
 */

import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const SCRIPT_NAME = path.basename(__filename);

const projectRoot = path.resolve(process.argv[2] ?? ".");

try {
  await fs.access(projectRoot);
} catch {
  console.error(`${SCRIPT_NAME}: project root not found: ${projectRoot}`);
  process.exit(2);
}

// Files we expect to exist by convention.
const TAGS_FILE = "lib/cache/tags.ts";
const REVALIDATE_FILE = "lib/cache/revalidate.ts";

// Directories we scan for source files.
const SCAN_DIRS = ["app", "src/app", "lib", "src/lib", "components", "src/components"];
const SOURCE_EXTS = new Set([".ts", ".tsx", ".mts", ".cts"]);

// Ignore directories that should not be scanned.
const IGNORE_DIRS = new Set([
  "node_modules", ".next", ".turbo", "dist", "build", "out", ".git", "coverage",
]);

/** Walk `dir` recursively, yielding absolute paths to source files. */
async function* walk(dir) {
  let entries;
  try {
    entries = await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const entry of entries) {
    if (entry.name.startsWith(".") && entry.name !== ".") continue;
    if (IGNORE_DIRS.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      yield* walk(full);
    } else if (SOURCE_EXTS.has(path.extname(entry.name))) {
      yield full;
    }
  }
}

const findings = [];
function fail(check, detail) {
  findings.push({ ok: false, check, detail });
}
function pass(check) {
  findings.push({ ok: true, check });
}

// Check 1 — next.config.* declares cacheComponents: true.
async function checkNextConfig() {
  const candidates = ["next.config.ts", "next.config.mjs", "next.config.js"];
  for (const name of candidates) {
    const file = path.join(projectRoot, name);
    try {
      const text = await fs.readFile(file, "utf8");
      if (/cacheComponents\s*:\s*true/.test(text)) {
        pass(`${name} declares cacheComponents: true`);
        return;
      }
      fail(`${name}`, "found but does not set cacheComponents: true");
      return;
    } catch {
      // try next candidate
    }
  }
  fail("next.config.{ts,mjs,js}", "no Next.js config file found");
}

// Check 2 — tag registry and revalidation utility files exist.
async function checkSkeletonFiles() {
  for (const rel of [TAGS_FILE, REVALIDATE_FILE]) {
    const file = path.join(projectRoot, rel);
    try {
      await fs.access(file);
      pass(`${rel} exists`);
    } catch {
      fail(rel, "expected file is missing");
    }
  }
}

// Check 3 — `updateTag(` only appears inside lib/cache/revalidate.ts.
async function checkUpdateTagCentralization() {
  const offenders = [];
  for await (const file of (async function* () {
    for (const dir of SCAN_DIRS) {
      yield* walk(path.join(projectRoot, dir));
    }
  })()) {
    if (file.endsWith(REVALIDATE_FILE.replace(/\//g, path.sep))) continue;
    const text = await fs.readFile(file, "utf8");
    if (/\bupdateTag\s*\(/.test(text)) {
      offenders.push(path.relative(projectRoot, file));
    }
  }
  if (offenders.length === 0) {
    pass("updateTag() centralized in lib/cache/revalidate.ts");
  } else {
    fail(
      "updateTag() centralization",
      `raw updateTag() calls found outside lib/cache/revalidate.ts:\n    ${offenders.join("\n    ")}`,
    );
  }
}

// Check 4 — no deprecated single-arg revalidateTag(...) calls.
async function checkRevalidateTagSecondArg() {
  const offenders = [];
  for await (const file of (async function* () {
    for (const dir of SCAN_DIRS) {
      yield* walk(path.join(projectRoot, dir));
    }
  })()) {
    const text = await fs.readFile(file, "utf8");
    // Match revalidateTag("...") or revalidateTag('...') with no comma after the literal.
    const re = /\brevalidateTag\(\s*(['"])[^'"]+\1\s*\)/g;
    if (re.test(text)) {
      offenders.push(path.relative(projectRoot, file));
    }
  }
  if (offenders.length === 0) {
    pass("revalidateTag() always called with a second argument");
  } else {
    fail(
      "revalidateTag() second-arg form",
      `deprecated single-arg revalidateTag() calls found:\n    ${offenders.join("\n    ")}`,
    );
  }
}

// Check 5 — files declaring "use cache" do not also call cookies()/headers()/auth().
//   Heuristic: a file that contains `"use cache"` AND also imports/calls
//   any of the dynamic APIs is suspicious. False positives are possible
//   when the dynamic API is used outside the cached function in the same
//   file — review manually.
async function checkDynamicApisInsideCache() {
  const suspicious = [];
  for await (const file of (async function* () {
    for (const dir of SCAN_DIRS) {
      yield* walk(path.join(projectRoot, dir));
    }
  })()) {
    const text = await fs.readFile(file, "utf8");
    if (!/["']use cache(?::\s*private)?["']/.test(text)) continue;
    if (/["']use cache:\s*private["']/.test(text)) continue; // private allows dynamic APIs
    if (/\b(cookies|headers|auth)\s*\(/.test(text)) {
      suspicious.push(path.relative(projectRoot, file));
    }
  }
  if (suspicious.length === 0) {
    pass("no dynamic-API calls in files declaring \"use cache\"");
  } else {
    fail(
      "dynamic APIs near \"use cache\"",
      `files declaring "use cache" that also call cookies()/headers()/auth() (review manually — false positives possible):\n    ${suspicious.join("\n    ")}`,
    );
  }
}

// Run all checks.
await checkNextConfig();
await checkSkeletonFiles();
await checkUpdateTagCentralization();
await checkRevalidateTagSecondArg();
await checkDynamicApisInsideCache();

// Report.
const passed = findings.filter((f) => f.ok).length;
const failed = findings.length - passed;

console.log(`\nnextjs-cache-architecture audit — ${path.relative(process.cwd(), projectRoot) || "."}\n`);
for (const f of findings) {
  const mark = f.ok ? "PASS" : "FAIL";
  console.log(`  [${mark}] ${f.check}`);
  if (!f.ok && f.detail) console.log(`         ${f.detail}`);
}
console.log(`\n${passed} passed, ${failed} failed.\n`);

process.exit(failed === 0 ? 0 : 1);
