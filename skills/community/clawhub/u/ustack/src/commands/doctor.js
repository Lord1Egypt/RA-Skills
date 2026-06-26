import fs from 'node:fs';
import path from 'node:path';
import { fileExists, getUstackDir, readJson } from '../lib/fs.js';

/**
 * ustack doctor
 *
 * Checks workspace health: configured upstreams, last analysis dates, git availability.
 */
export async function runDoctor({ cwd, args = [] }) {
  console.log('uStack Doctor\n');

  // Check git
  try {
    const { execSync } = await import('node:child_process');
    const gitVersion = execSync('git --version', { encoding: 'utf8' }).trim();
    console.log(`✅ git: ${gitVersion}`);
  } catch {
    console.log('❌ git: not found — required for ustack import/update');
  }

  // Check .ustack dir
  const ustackDir = getUstackDir(cwd);
  if (!fileExists(ustackDir)) {
    console.log('\n⚪ No .ustack workspace found in current directory.');
    console.log('   Run: ustack import <github-url> --name <id>');
    return;
  }

  console.log(`✅ .ustack workspace: ${ustackDir}`);

  // List configured upstreams
  const upstreamsDir = path.join(ustackDir, 'upstreams');
  if (!fileExists(upstreamsDir)) {
    console.log('\n⚪ No upstreams configured yet.');
    console.log('   Run: ustack import https://github.com/garrytan/gstack --name gstack');
    return;
  }

  const upstreamIds = fs.readdirSync(upstreamsDir).filter(
    d => fileExists(path.join(upstreamsDir, d, 'manifest.json'))
  );

  if (!upstreamIds.length) {
    console.log('\n⚪ No upstreams configured yet.');
    return;
  }

  console.log(`\nConfigured upstreams (${upstreamIds.length}):\n`);

  for (const id of upstreamIds) {
    const manifest = readJson(path.join(upstreamsDir, id, 'manifest.json'));
    const head = manifest.headSha ? manifest.headSha.slice(0, 12) : 'unknown';
    const lastAnalyzed = manifest.lastAnalyzedAt
      ? manifest.lastAnalyzedAt.split('T')[0]
      : 'never';
    const lastUpdated = manifest.updatedAt
      ? manifest.updatedAt.split('T')[0]
      : 'unknown';

    const changed = manifest.headSha !== manifest.previousSha && manifest.previousSha
      ? ' ⚠️  (unanalyzed changes pending)'
      : '';

    console.log(`  ${id}`);
    console.log(`    source:        ${manifest.repoUrl}`);
    console.log(`    head:          ${head}`);
    console.log(`    last imported: ${lastUpdated}`);
    console.log(`    last analyzed: ${lastAnalyzed}${changed}`);
    console.log(`    skills:        ${manifest.structure?.skillCount ?? '?'}`);
    console.log(`    host conventions: ${manifest.structure?.hostConventions ?? 'unknown'}`);
    console.log('');
  }

  // List runs
  const runsDir = path.join(ustackDir, 'runs');
  if (fileExists(runsDir)) {
    console.log('Recent runs:');
    for (const id of upstreamIds) {
      const idRunsDir = path.join(runsDir, id);
      if (!fileExists(idRunsDir)) continue;
      const runs = fs.readdirSync(idRunsDir).sort().reverse().slice(0, 3);
      for (const run of runs) {
        const hasAnalysis = fileExists(path.join(idRunsDir, run, 'analysis.json'));
        const hasPublish = fileExists(path.join(idRunsDir, run, 'publish.md'));
        const status = [hasAnalysis ? '📊 analysis' : '', hasPublish ? '📄 publish' : '']
          .filter(Boolean).join(', ');
        console.log(`  ${id}/${run}  [${status || 'empty'}]`);
      }
    }
  }

  console.log('\nAll checks complete.');
}
