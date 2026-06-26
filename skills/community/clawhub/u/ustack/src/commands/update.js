import { runImport } from './import.js';
import { runAnalyze } from './analyze.js';
import { runPublish } from './publish.js';
import { fileExists, readJson, getUpstreamDir } from '../lib/fs.js';
import path from 'node:path';

/**
 * ustack update <upstream-id>
 *
 * Combines: import (pull latest) → analyze → publish.
 * The canonical "check for updates and produce output" command.
 */
export async function runUpdate({ cwd, args = [] }) {
  const upstreamId = args[0];

  if (!upstreamId) {
    console.error('Usage: ustack update <upstream-id>');
    process.exitCode = 1;
    return;
  }

  const manifestPath = path.join(getUpstreamDir(cwd, upstreamId), 'manifest.json');

  if (!fileExists(manifestPath)) {
    console.error(`Upstream "${upstreamId}" not found. Run: ustack import <url> --name ${upstreamId}`);
    process.exitCode = 1;
    return;
  }

  const before = readJson(manifestPath);
  const previousSha = before.headSha;

  console.log(`=== ustack update: ${upstreamId} ===`);
  console.log('');

  // Step 1: Pull latest
  console.log('[1/3] Pulling upstream...');
  await runImport({ cwd, args: [before.repoUrl, '--name', upstreamId] });
  console.log('');

  // Check if anything changed
  const after = readJson(manifestPath);
  if (after.headSha === previousSha) {
    console.log('No changes upstream. Nothing to analyze or publish.');
    return;
  }

  // Step 2: Analyze
  console.log('[2/3] Analyzing changes...');
  await runAnalyze({ cwd, args: [upstreamId] });
  console.log('');

  // Step 3: Publish
  console.log('[3/3] Generating publish page...');
  await runPublish({ cwd, args: [upstreamId] });
  console.log('');

  console.log(`=== Update complete ===`);
  console.log(`From: ${previousSha.slice(0, 12)} → To: ${after.headSha.slice(0, 12)}`);
  console.log(`Run artifacts: .ustack/runs/${upstreamId}/`);
  console.log(`Site page: .ustack/site/updates/${upstreamId}/`);
}
