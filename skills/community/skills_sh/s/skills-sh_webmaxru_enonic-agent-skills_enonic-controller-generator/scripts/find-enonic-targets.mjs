#!/usr/bin/env node

/**
 * find-enonic-targets.mjs
 *
 * Scans the workspace for Enonic XP project markers and reports the locations
 * of existing page, part, layout, and processor directories.
 *
 * Usage:
 *   node scripts/find-enonic-targets.mjs <workspace-root>
 *
 * Exit codes:
 *   0 — Enonic XP project detected; results printed to stdout as JSON.
 *   1 — No Enonic XP project markers found; message printed to stderr.
 */

import { existsSync, readdirSync, statSync } from 'fs';
import { join, resolve } from 'path';

const workspaceRoot = process.argv[2];

if (!workspaceRoot) {
  process.stderr.write('ERROR: Provide a workspace root path as the first argument.\n');
  process.exit(1);
}

const resolvedRoot = resolve(workspaceRoot);

// Markers that indicate an Enonic XP project
const MARKERS = ['build.gradle', 'gradle.properties'];
const SITE_BASE = join('src', 'main', 'resources', 'site');
const COMPONENT_DIRS = ['pages', 'parts', 'layouts', 'processors'];

function findGradleRoots(dir, depth = 0) {
  const results = [];
  if (depth > 4) return results;
  try {
    const hasMarker = MARKERS.some(m => existsSync(join(dir, m)));
    if (hasMarker) {
      results.push(dir);
    }
    for (const entry of readdirSync(dir)) {
      if (entry.startsWith('.') || entry === 'node_modules' || entry === 'build') continue;
      const full = join(dir, entry);
      if (statSync(full).isDirectory()) {
        results.push(...findGradleRoots(full, depth + 1));
      }
    }
  } catch {
    // permission or read errors — skip
  }
  return results;
}

function listComponents(siteDir, type) {
  const dir = join(siteDir, type);
  if (!existsSync(dir)) return [];
  try {
    return readdirSync(dir).filter(e => statSync(join(dir, e)).isDirectory());
  } catch {
    return [];
  }
}

const gradleRoots = findGradleRoots(resolvedRoot);

if (gradleRoots.length === 0) {
  process.stderr.write('NO_PROJECT: No Enonic XP project markers (build.gradle) found under ' + resolvedRoot + '\n');
  process.exit(1);
}

const report = gradleRoots.map(root => {
  const siteDir = join(root, SITE_BASE);
  const hasSite = existsSync(siteDir);
  const components = {};
  if (hasSite) {
    for (const type of COMPONENT_DIRS) {
      components[type] = listComponents(siteDir, type);
    }
  }
  return {
    projectRoot: root,
    siteDirExists: hasSite,
    sitePath: siteDir,
    components
  };
});

process.stdout.write(JSON.stringify(report, null, 2) + '\n');
process.exit(0);
