import fs from 'node:fs';
import path from 'node:path';
import { syncUpstream, getTags } from '../lib/git.js';
import { writeJson, writeText, fileExists, getUpstreamDir, ensureDir } from '../lib/fs.js';

/**
 * ustack import <github-url> [--name <id>]
 *
 * Clones (or pulls) the upstream repo and records baseline metadata.
 * Creates:
 *   .ustack/upstreams/<id>/
 *     manifest.json       — upstream metadata + current revision
 *     snapshot/           — shallow copy of key files for fast inspection
 */
export async function runImport({ cwd, args = [] }) {
  let repoUrl = null;
  let upstreamId = null;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--name' && args[i + 1]) {
      upstreamId = args[i + 1];
      i++;
    } else if (!repoUrl && !args[i].startsWith('--')) {
      repoUrl = args[i];
    }
  }

  if (!repoUrl) {
    console.error('Usage: ustack import <github-url> [--name <id>]');
    console.error('Example: ustack import https://github.com/garrytan/gstack --name gstack');
    process.exitCode = 1;
    return;
  }

  if (!upstreamId) {
    upstreamId = repoUrl.split('/').pop().replace(/\.git$/, '');
  }

  const upstreamDir = getUpstreamDir(cwd, upstreamId);
  const repoDir = path.join(upstreamDir, 'repo');

  console.log(`Importing upstream: ${upstreamId}`);
  console.log(`Source: ${repoUrl}`);

  console.log('Cloning/pulling upstream...');
  let headSha;
  try {
    headSha = syncUpstream({ repoUrl, targetDir: repoDir });
  } catch (err) {
    console.error(`Failed to sync upstream: ${err.message}`);
    process.exitCode = 1;
    return;
  }

  console.log(`HEAD: ${headSha}`);

  const keyFiles = detectKeyFiles(repoDir);
  const tags = getTags(repoDir);
  const latestTag = tags[0] || null;
  const structure = detectStructure(repoDir, keyFiles);

  // Load existing manifest to preserve previousSha
  const manifestPath = path.join(upstreamDir, 'manifest.json');
  let previousSha = null;
  if (fileExists(manifestPath)) {
    try {
      const existing = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
      previousSha = existing.headSha || null;
    } catch { /* ignore */ }
  }

  const manifest = {
    id: upstreamId,
    repoUrl,
    repoDir,
    importedAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    headSha,
    previousSha,
    latestTag,
    keyFiles,
    structure,
  };

  writeJson(manifestPath, manifest);

  // Save README snapshot
  const readmePath = path.join(repoDir, 'README.md');
  if (fileExists(readmePath)) {
    ensureDir(path.join(upstreamDir, 'snapshot'));
    const readmeHead = fs.readFileSync(readmePath, 'utf8').split('\n').slice(0, 60).join('\n');
    writeText(path.join(upstreamDir, 'snapshot', 'README-head.md'), readmeHead);
  }

  console.log(`\nImport complete.`);
  console.log(`Manifest: .ustack/upstreams/${upstreamId}/manifest.json`);
  console.log(`\nKey files:`);
  for (const [category, files] of Object.entries(keyFiles)) {
    if (files.length) console.log(`  ${category}: ${files.slice(0, 8).join(', ')}`);
  }
  console.log(`\nStructure:`);
  for (const [key, val] of Object.entries(structure)) {
    console.log(`  ${key}: ${val}`);
  }
  if (previousSha && previousSha !== headSha) {
    console.log(`\nChanges detected since last import:`);
    console.log(`  from: ${previousSha.slice(0, 12)}`);
    console.log(`  to:   ${headSha.slice(0, 12)}`);
    console.log(`  Run: ustack analyze ${upstreamId}`);
  } else if (!previousSha) {
    console.log(`\nFirst import. Run: ustack analyze ${upstreamId}`);
  } else {
    console.log(`\nNo changes since last import (${headSha.slice(0, 12)}).`);
  }
}

function detectKeyFiles(repoDir) {
  const check = (f) => fileExists(path.join(repoDir, f));

  const controlDocs = [];
  const config = [];
  const skills = [];
  const tooling = [];

  for (const f of ['README.md', 'ARCHITECTURE.md', 'AGENTS.md', 'CLAUDE.md', 'DESIGN.md', 'ETHOS.md', 'CONTRIBUTING.md', 'TODOS.md', 'CHANGELOG.md']) {
    if (check(f)) controlDocs.push(f);
  }

  for (const f of ['package.json', 'conductor.json', '.env.example', 'bun.lock', 'package-lock.json', 'VERSION']) {
    if (check(f)) config.push(f);
  }

  try {
    const entries = fs.readdirSync(repoDir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      if (fileExists(path.join(repoDir, entry.name, 'SKILL.md'))) {
        skills.push(entry.name + '/');
      }
      if (['bin', 'scripts', 'lib'].includes(entry.name)) {
        tooling.push(entry.name + '/');
      }
    }
  } catch { /* ignore */ }

  return { controlDocs, config, skills, tooling };
}

function detectStructure(repoDir, keyFiles) {
  const skillCount = keyFiles.skills.length;
  const hasClaude = keyFiles.controlDocs.includes('CLAUDE.md');
  const hasArchitecture = keyFiles.controlDocs.includes('ARCHITECTURE.md');
  const hasBun = keyFiles.config.includes('bun.lock');
  const hasConductor = keyFiles.config.includes('conductor.json');

  const hostConventions = [];
  if (hasClaude) hostConventions.push('claude-code');
  if (fileExists(path.join(repoDir, 'codex'))) hostConventions.push('codex');
  try {
    const agentFiles = fs.readdirSync(path.join(repoDir, 'agents'));
    if (agentFiles.some(f => f.includes('openai') || f.includes('codex'))) {
      if (!hostConventions.includes('codex')) hostConventions.push('codex');
    }
  } catch { /* no agents dir */ }

  const category = skillCount > 10 ? 'workflow-skill-framework'
    : skillCount > 0 ? 'skill-library'
    : 'agent-workspace';

  return {
    skillCount,
    skillFormat: skillCount > 0 ? 'SKILL.md' : 'none',
    hostConventions: hostConventions.join(', ') || 'unknown',
    hasArchitecture,
    hasBun,
    hasConductor,
    category,
  };
}
