/**
 * wip-repos core ... repo manifest reconciler
 *
 * The manifest is the source of truth. The filesystem adapts to it.
 * Like prettier for folder structure.
 */

import { readFileSync, writeFileSync, existsSync, readdirSync, statSync, mkdirSync, renameSync } from 'node:fs';
import { join, dirname, relative, resolve } from 'node:path';

/**
 * Load and parse a repos-manifest.json file.
 * Supports both v1 (flat key-value) and v2 (rich objects) formats.
 */
export function loadManifest(manifestPath) {
  if (!existsSync(manifestPath)) {
    throw new Error(`Manifest not found: ${manifestPath}`);
  }
  const raw = JSON.parse(readFileSync(manifestPath, 'utf8'));

  // Detect format
  const meta = {};
  const repos = {};

  for (const [key, value] of Object.entries(raw)) {
    if (key.startsWith('_')) {
      meta[key] = value;
      continue;
    }
    if (typeof value === 'string') {
      // v1 flat format: path -> remote
      repos[key] = { remote: value };
    } else if (typeof value === 'object' && value !== null) {
      // v2 rich format
      repos[key] = value;
    }
  }

  return { meta, repos, format: meta._format || 'v1', path: manifestPath };
}

/**
 * Save manifest back to disk.
 */
export function saveManifest(manifestPath, meta, repos) {
  const out = {};
  for (const [key, value] of Object.entries(meta)) {
    out[key] = value;
  }
  for (const [key, value] of Object.entries(repos)) {
    // v1: just write the remote string
    if (Object.keys(value).length === 1 && value.remote) {
      out[key] = value.remote;
    } else {
      out[key] = value;
    }
  }
  writeFileSync(manifestPath, JSON.stringify(out, null, 2) + '\n', 'utf8');
}

/**
 * Walk a directory tree and find all git repos (directories containing .git/).
 * Returns array of relative paths from the root.
 */
export function walkRepos(rootDir, prefix = '') {
  const results = [];
  if (!existsSync(rootDir)) return results;

  const entries = readdirSync(rootDir, { withFileTypes: true });
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    if (entry.name === '.git' || entry.name === 'node_modules') continue;
    if (entry.name === '.DS_Store') continue;

    const fullPath = join(rootDir, entry.name);
    const relPath = prefix ? `${prefix}/${entry.name}` : entry.name;

    // If this directory has a .git, it's a repo
    if (existsSync(join(fullPath, '.git'))) {
      results.push(relPath);
    } else {
      // Recurse into non-repo directories (organizational folders)
      results.push(...walkRepos(fullPath, relPath));
    }
  }
  return results;
}

/**
 * Check: diff the filesystem against the manifest.
 * Returns { inManifestOnly, onDiskOnly, matched }
 */
export function check(manifestPath, reposRoot) {
  const manifest = loadManifest(manifestPath);
  const manifestPaths = new Set(Object.keys(manifest.repos));
  const diskPaths = new Set(walkRepos(reposRoot));

  const inManifestOnly = [];
  const onDiskOnly = [];
  const matched = [];

  for (const p of manifestPaths) {
    if (diskPaths.has(p)) {
      matched.push(p);
    } else {
      inManifestOnly.push(p);
    }
  }

  for (const p of diskPaths) {
    if (!manifestPaths.has(p)) {
      onDiskOnly.push(p);
    }
  }

  return {
    inManifestOnly: inManifestOnly.sort(),
    onDiskOnly: onDiskOnly.sort(),
    matched: matched.sort(),
    total: {
      manifest: manifestPaths.size,
      disk: diskPaths.size,
      matched: matched.length,
    },
  };
}

/**
 * Sync: move local folders to match the manifest.
 * Returns array of { from, to } moves that were performed.
 *
 * Only handles repos that exist on disk but at the wrong path.
 * Matches by remote URL (git remote -v) against manifest remotes.
 */
export function planSync(manifestPath, reposRoot) {
  const manifest = loadManifest(manifestPath);
  const diskPaths = walkRepos(reposRoot);
  const moves = [];

  // Build a map of remote -> manifest path
  const remoteToManifest = new Map();
  for (const [mPath, info] of Object.entries(manifest.repos)) {
    if (info.remote) {
      remoteToManifest.set(info.remote, mPath);
    }
  }

  // For each repo on disk, check if its remote matches a manifest entry at a different path
  for (const diskPath of diskPaths) {
    const fullPath = join(reposRoot, diskPath);
    const gitConfig = join(fullPath, '.git', 'config');
    if (!existsSync(gitConfig)) continue;

    const configText = readFileSync(gitConfig, 'utf8');
    // Extract remote URL
    const match = configText.match(/url\s*=\s*.*[:/]([^/]+\/[^/\s.]+?)(?:\.git)?\s*$/m);
    if (!match) continue;

    const remote = match[1];
    const expectedPath = remoteToManifest.get(remote);

    if (expectedPath && expectedPath !== diskPath) {
      moves.push({
        from: diskPath,
        to: expectedPath,
        remote,
        fromFull: fullPath,
        toFull: join(reposRoot, expectedPath),
      });
    }
  }

  return moves;
}

/**
 * Execute sync moves. Creates parent directories as needed.
 */
export function executeSync(moves, reposRoot) {
  const results = [];
  for (const move of moves) {
    const parentDir = dirname(move.toFull);
    if (!existsSync(parentDir)) {
      mkdirSync(parentDir, { recursive: true });
    }
    if (existsSync(move.toFull)) {
      results.push({ ...move, status: 'skipped', reason: 'target exists' });
      continue;
    }
    try {
      renameSync(move.fromFull, move.toFull);
      results.push({ ...move, status: 'moved' });
    } catch (err) {
      results.push({ ...move, status: 'error', reason: err.message });
    }
  }
  return results;
}

/**
 * Add a repo to the manifest.
 */
export function addRepo(manifestPath, repoPath, remote, opts = {}) {
  const manifest = loadManifest(manifestPath);

  if (manifest.repos[repoPath]) {
    throw new Error(`Already in manifest: ${repoPath}`);
  }

  const entry = { remote };
  if (opts.description) entry.description = opts.description;
  if (opts.category) entry.category = opts.category;
  if (opts.public) entry.public = opts.public;
  if (opts.privatized !== undefined) entry.privatized = opts.privatized;

  manifest.repos[repoPath] = entry;
  saveManifest(manifestPath, manifest.meta, manifest.repos);

  return entry;
}

/**
 * Move a repo in the manifest from one path to another.
 */
export function moveRepo(manifestPath, fromPath, toPath) {
  const manifest = loadManifest(manifestPath);

  if (!manifest.repos[fromPath]) {
    throw new Error(`Not in manifest: ${fromPath}`);
  }
  if (manifest.repos[toPath]) {
    throw new Error(`Target already exists in manifest: ${toPath}`);
  }

  manifest.repos[toPath] = manifest.repos[fromPath];
  delete manifest.repos[fromPath];
  saveManifest(manifestPath, manifest.meta, manifest.repos);

  return manifest.repos[toPath];
}

/**
 * Generate a markdown directory tree from the manifest.
 */
export function generateReadmeTree(manifestPath) {
  const manifest = loadManifest(manifestPath);
  const paths = Object.keys(manifest.repos).sort();

  // Build tree structure
  const tree = {};
  for (const p of paths) {
    const parts = p.split('/');
    let node = tree;
    for (const part of parts) {
      if (!node[part]) node[part] = {};
      node = node[part];
    }
  }

  // Render tree
  const lines = ['repos/'];
  function render(node, prefix, isLast) {
    const entries = Object.keys(node).sort((a, b) => {
      // underscore-prefixed folders sort to top
      const aUnder = a.startsWith('_');
      const bUnder = b.startsWith('_');
      if (aUnder && !bUnder) return 1;
      if (!aUnder && bUnder) return -1;
      return a.localeCompare(b);
    });

    for (let i = 0; i < entries.length; i++) {
      const name = entries[i];
      const last = i === entries.length - 1;
      const connector = last ? '└── ' : '├── ';
      const childPrefix = last ? '    ' : '│   ';
      const children = Object.keys(node[name]);

      if (children.length > 0) {
        lines.push(`${prefix}${connector}${name}/`);
        render(node[name], prefix + childPrefix, last);
      } else {
        lines.push(`${prefix}${connector}${name}`);
      }
    }
  }

  render(tree, '', false);
  return lines.join('\n');
}

// ── Compliance checking (Wave 3.3) ──────────────────────────────────

const DEFAULT_LICENSE_GUARD = {
  copyright: 'WIP Computer, Inc.',
  license: 'MIT+AGPL',
  spdx: 'MIT AND AGPL-3.0-or-later',
};

/**
 * Check compliance of all repos in the manifest.
 * Returns array of { repoPath, fullPath, issues[], hasPackageJson }
 */
export function checkCompliance(manifestPath, reposRoot) {
  const manifest = loadManifest(manifestPath);
  const results = [];

  for (const [repoPath, info] of Object.entries(manifest.repos)) {
    const fullPath = join(reposRoot, repoPath);
    if (!existsSync(fullPath)) continue;
    if (!existsSync(join(fullPath, 'package.json'))) continue;

    // Skip _to-privatize, _sort, _sunsetted, _trash
    if (repoPath.includes('_to-privatize') || repoPath.includes('_sort') ||
        repoPath.includes('_sunsetted') || repoPath.includes('_trash')) continue;

    const issues = [];

    if (!existsSync(join(fullPath, '.license-guard.json'))) {
      issues.push('missing .license-guard.json');
    }
    if (!existsSync(join(fullPath, 'LICENSE'))) {
      issues.push('missing LICENSE');
    } else {
      const lic = readFileSync(join(fullPath, 'LICENSE'), 'utf8');
      if (!lic.includes('WIP Computer')) issues.push('LICENSE missing copyright');
      if (!lic.includes('AGPL') && !lic.includes('GNU Affero')) issues.push('LICENSE missing AGPL');
    }
    if (!existsSync(join(fullPath, 'CLA.md'))) {
      issues.push('missing CLA.md');
    }
    if (existsSync(join(fullPath, 'ai')) && !existsSync(join(fullPath, '.npmignore'))) {
      issues.push('missing .npmignore (has ai/ directory)');
    } else if (existsSync(join(fullPath, 'ai')) && existsSync(join(fullPath, '.npmignore'))) {
      const npmignore = readFileSync(join(fullPath, '.npmignore'), 'utf8');
      if (!npmignore.includes('ai/')) issues.push('.npmignore does not exclude ai/');
    }

    results.push({ repoPath, fullPath, issues, clean: issues.length === 0 });
  }

  return results;
}

/**
 * Fix compliance issues for a single repo.
 * Creates missing files with WIP Computer defaults.
 * Returns array of files created.
 */
export function fixCompliance(fullPath) {
  const created = [];

  // .license-guard.json
  if (!existsSync(join(fullPath, '.license-guard.json'))) {
    writeFileSync(
      join(fullPath, '.license-guard.json'),
      JSON.stringify(DEFAULT_LICENSE_GUARD, null, 2) + '\n',
    );
    created.push('.license-guard.json');
  }

  // CLA.md
  if (!existsSync(join(fullPath, 'CLA.md'))) {
    writeFileSync(join(fullPath, 'CLA.md'), [
      '# Contributor License Agreement',
      '',
      'By submitting a pull request to this repository, you agree that:',
      '',
      '1. Your contribution is original work or you have the right to submit it.',
      '2. You grant WIP Computer, Inc. a perpetual, worldwide, non-exclusive,',
      '   royalty-free license to use, modify, and distribute your contribution',
      '   under the terms of this project\'s license.',
      '3. You understand your contribution will be publicly available.',
      '',
      'This CLA is required for all contributions. By opening a PR, you accept these terms.',
      '',
    ].join('\n'));
    created.push('CLA.md');
  }

  // .npmignore (if ai/ exists)
  if (existsSync(join(fullPath, 'ai'))) {
    const npmignorePath = join(fullPath, '.npmignore');
    if (!existsSync(npmignorePath)) {
      writeFileSync(npmignorePath, 'ai/\n.claude/\n.worktrees/\n.DS_Store\nCLAUDE.md\n');
      created.push('.npmignore');
    } else {
      const content = readFileSync(npmignorePath, 'utf8');
      if (!content.includes('ai/')) {
        writeFileSync(npmignorePath, content.trimEnd() + '\nai/\n');
        created.push('.npmignore (updated)');
      }
    }
  }

  return created;
}

/**
 * Find repos on disk that are NOT in the manifest.
 * This is the watchdog function for the daily audit.
 */
export function findUnmanifested(manifestPath, reposRoot) {
  const result = check(manifestPath, reposRoot);
  return result.onDiskOnly;
}
