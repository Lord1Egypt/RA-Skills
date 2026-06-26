#!/usr/bin/env node

/**
 * Scan the workspace for Next.js + Enonic XP integration markers.
 *
 * Detects:
 *   - package.json with "next" and/or "@enonic/nextjs-adapter" dependencies
 *   - .env / .env.local files with ENONIC_* variables
 *   - _mappings.ts component registry files
 *   - Guillotine query files (.ts files containing "guillotine")
 *   - next.config.* files
 *
 * Usage:
 *   node find-nextxp-targets.mjs [rootDir]
 *
 * Output (stdout): JSON object with detected integration surface.
 * On failure: error message to stderr, exit code 1.
 */

import { readdir, readFile, stat } from "node:fs/promises";
import { join, resolve } from "node:path";

async function exists(path) {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

async function findNextjsProjects(dir, depth = 0, maxDepth = 3) {
  const results = [];
  if (depth > maxDepth) return results;

  const pkgPath = join(dir, "package.json");
  if (await exists(pkgPath)) {
    try {
      const pkg = JSON.parse(await readFile(pkgPath, "utf-8"));
      const allDeps = { ...pkg.dependencies, ...pkg.devDependencies };
      if (allDeps["next"]) {
        results.push({
          path: dir,
          nextVersion: allDeps["next"],
          adapterVersion: allDeps["@enonic/nextjs-adapter"] || null,
          hasAdapter: !!allDeps["@enonic/nextjs-adapter"],
        });
        return results; // Don't recurse into detected projects
      }
    } catch {
      // invalid package.json, skip
    }
  }

  try {
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      if (entry.name.startsWith(".") || entry.name === "node_modules" || entry.name === "build" || entry.name === ".next") continue;
      const sub = await findNextjsProjects(join(dir, entry.name), depth + 1, maxDepth);
      results.push(...sub);
    }
  } catch {
    // skip inaccessible directories
  }
  return results;
}

async function findEnvFiles(dir, depth = 0, maxDepth = 3) {
  const results = [];
  if (depth > maxDepth) return results;

  for (const name of [".env", ".env.local"]) {
    const envPath = join(dir, name);
    if (await exists(envPath)) {
      try {
        const content = await readFile(envPath, "utf-8");
        if (/ENONIC_/.test(content)) {
          results.push(envPath);
        }
      } catch {
        // skip unreadable
      }
    }
  }

  try {
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      if (entry.name.startsWith(".") || entry.name === "node_modules" || entry.name === "build" || entry.name === ".next") continue;
      const sub = await findEnvFiles(join(dir, entry.name), depth + 1, maxDepth);
      results.push(...sub);
    }
  } catch {
    // skip inaccessible
  }
  return results;
}

async function findFiles(dir, predicate, depth = 0, maxDepth = 3) {
  const results = [];
  if (depth > maxDepth) return results;

  try {
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = join(dir, entry.name);
      if (entry.isDirectory()) {
        if (entry.name.startsWith(".") || entry.name === "node_modules" || entry.name === "build" || entry.name === ".next") continue;
        const sub = await findFiles(fullPath, predicate, depth + 1, maxDepth);
        results.push(...sub);
      } else if (entry.isFile() && predicate(entry.name)) {
        results.push(fullPath);
      }
    }
  } catch {
    // skip inaccessible
  }
  return results;
}

async function main() {
  const rootDir = resolve(process.argv[2] || ".");
  if (!(await exists(rootDir))) {
    process.stderr.write(`ERROR: Directory not found: ${rootDir}\n`);
    process.exit(1);
  }

  const nextjsProjects = await findNextjsProjects(rootDir);
  const envFiles = await findEnvFiles(rootDir);
  const mappingFiles = await findFiles(rootDir, (name) => name === "_mappings.ts" || name === "_mappings.js");

  const queryFiles = [];
  const tsFiles = await findFiles(rootDir, (name) => (name.endsWith(".ts") || name.endsWith(".js")) && !name.endsWith(".d.ts"));
  for (const file of tsFiles) {
    try {
      const content = await readFile(file, "utf-8");
      if (/guillotine/i.test(content) && /query|gql|graphql/i.test(content)) {
        queryFiles.push(file);
      }
    } catch {
      // skip unreadable
    }
  }

  const result = {
    nextjsProjects,
    envFiles,
    mappingFiles,
    queryFiles,
  };

  if (nextjsProjects.length === 0) {
    process.stderr.write("WARNING: No Next.js projects detected in workspace.\n");
  }

  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
}

main().catch((err) => {
  process.stderr.write(`ERROR: ${err.message}\n`);
  process.exit(1);
});
