#!/usr/bin/env node

/**
 * Scan the workspace for Enonic XP project markers.
 *
 * Detects Enonic XP projects by looking for:
 *   - build.gradle with "com.enonic.xp" plugin references
 *   - gradle.properties with xpVersion or appName
 *   - src/main/resources/site/ directory structure
 *
 * Usage:
 *   node find-enonic-targets.mjs [rootDir]
 *
 * Output (stdout): JSON array of detected project roots.
 * On failure: error message to stderr, exit code 1.
 */

import { readdir, readFile, stat } from "node:fs/promises";
import { join, resolve } from "node:path";

const MARKERS = [
  { file: "build.gradle", pattern: /com\.enonic\.xp/ },
  { file: "gradle.properties", pattern: /xpVersion|appName/ },
];

const SITE_DIR = join("src", "main", "resources", "site");

async function exists(path) {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

async function isEnonicProject(dir) {
  for (const marker of MARKERS) {
    const filePath = join(dir, marker.file);
    if (await exists(filePath)) {
      const content = await readFile(filePath, "utf-8");
      if (marker.pattern.test(content)) return true;
    }
  }
  if (await exists(join(dir, SITE_DIR))) return true;
  return false;
}

async function scanDir(dir, depth = 0, maxDepth = 3) {
  const results = [];
  if (depth > maxDepth) return results;
  if (await isEnonicProject(dir)) {
    results.push(dir);
    return results;
  }
  try {
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      if (entry.name.startsWith(".") || entry.name === "node_modules" || entry.name === "build") continue;
      const sub = await scanDir(join(dir, entry.name), depth + 1, maxDepth);
      results.push(...sub);
    }
  } catch {
    // skip inaccessible directories
  }
  return results;
}

async function main() {
  const rootDir = resolve(process.argv[2] || ".");
  if (!(await exists(rootDir))) {
    process.stderr.write(`ERROR: Directory not found: ${rootDir}\n`);
    process.exit(1);
  }
  const projects = await scanDir(rootDir);
  if (projects.length === 0) {
    process.stderr.write("WARNING: No Enonic XP projects detected in workspace.\n");
  }
  process.stdout.write(JSON.stringify(projects, null, 2) + "\n");
}

main().catch((err) => {
  process.stderr.write(`ERROR: ${err.message}\n`);
  process.exit(1);
});
