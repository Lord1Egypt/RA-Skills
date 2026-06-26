import path from 'node:path';
import { writeText, fileExists, readJson, readText, getUpstreamDir, listRunDirs, getRunDir } from '../lib/fs.js';

/**
 * ustack publish <upstream-id>
 *
 * Generates a website-ready markdown page from the latest analysis.
 * Output: .ustack/runs/<id>/<timestamp>/publish.md
 *
 * Format designed to drop directly into AGI.security blog/update feed.
 */
export async function runPublish({ cwd, args = [] }) {
  const upstreamId = args[0];

  if (!upstreamId) {
    console.error('Usage: ustack publish <upstream-id>');
    process.exitCode = 1;
    return;
  }

  const upstreamDir = getUpstreamDir(cwd, upstreamId);
  const manifestPath = path.join(upstreamDir, 'manifest.json');

  if (!fileExists(manifestPath)) {
    console.error(`Upstream "${upstreamId}" not found. Run: ustack import then ustack analyze.`);
    process.exitCode = 1;
    return;
  }

  const manifest = readJson(manifestPath);

  if (!manifest.lastRunTimestamp) {
    console.error(`No analysis found for "${upstreamId}". Run: ustack analyze ${upstreamId}`);
    process.exitCode = 1;
    return;
  }

  // Find latest run
  const runs = listRunDirs(cwd, upstreamId);
  if (!runs.length) {
    console.error(`No run directories found. Run: ustack analyze ${upstreamId}`);
    process.exitCode = 1;
    return;
  }

  const latestRun = runs[0];
  const runDir = path.join(cwd, '.ustack', 'runs', upstreamId, latestRun);
  const analysisPath = path.join(runDir, 'analysis.json');

  if (!fileExists(analysisPath)) {
    console.error(`Analysis artifact missing at ${analysisPath}`);
    process.exitCode = 1;
    return;
  }

  const analysis = readJson(analysisPath);

  console.log(`Publishing update page for: ${upstreamId}`);
  console.log(`From analysis: ${latestRun}`);

  const page = renderPublishPage(analysis, manifest);
  const outputPath = path.join(runDir, 'publish.md');
  writeText(outputPath, page);

  // Also write to site/updates dir for direct blog integration
  const siteDir = path.join(cwd, '.ustack', 'site', 'updates', upstreamId);
  const slugDate = analysis.analyzedAt.split('T')[0];
  const sitePagePath = path.join(siteDir, `${slugDate}-${analysis.toShaShort}.md`);
  writeText(sitePagePath, page);

  console.log(`\nPublish page generated:`);
  console.log(`  Run: ${outputPath.replace(cwd + '/', '')}`);
  console.log(`  Site: ${sitePagePath.replace(cwd + '/', '')}`);
  console.log(`\nReady to drop into AGI.security blog/updates feed.`);
}

function renderPublishPage(analysis, manifest) {
  const date = analysis.analyzedAt.split('T')[0];
  const upstreamName = upstreamDisplayName(analysis.upstreamId);
  const hasChanges = analysis.commitCount > 0 || analysis.changedFileCount > 0;

  const highAreas = Object.entries(analysis.impact).filter(([, v]) => v === 'high').map(([k]) => k);
  const mediumAreas = Object.entries(analysis.impact).filter(([, v]) => v === 'medium').map(([k]) => k);
  const activeAreas = [...highAreas, ...mediumAreas];

  const lines = [];

  // Frontmatter
  lines.push('---');
  lines.push(`title: "${upstreamName} Update — ${date}"`);
  lines.push(`date: ${date}`);
  lines.push(`upstream: ${analysis.repoUrl}`);
  lines.push(`from_sha: ${analysis.fromShaShort || 'initial'}`);
  lines.push(`to_sha: ${analysis.toShaShort}`);
  lines.push(`commits: ${analysis.commitCount}`);
  lines.push(`files_changed: ${analysis.changedFileCount}`);
  lines.push(`impact_areas: ${activeAreas.join(', ') || 'none'}`);
  lines.push(`portable: ${analysis.portability.portable.length}`);
  lines.push(`needs_adaptation: ${analysis.portability.needsAdaptation.length}`);
  lines.push(`host_specific: ${analysis.portability.hostSpecific.length}`);
  lines.push('---');
  lines.push('');

  // Header
  lines.push(`# ${upstreamName} Update — ${date}`);
  lines.push('');

  if (!hasChanges) {
    lines.push('No changes detected since last analysis.');
    return lines.join('\n') + '\n';
  }

  // Lead
  lines.push(`**${analysis.commitCount} commit(s)** · **${analysis.changedFileCount} file(s) changed** · from \`${analysis.fromShaShort || 'initial'}\` → \`${analysis.toShaShort}\``);
  lines.push('');

  // Summary
  lines.push('## What Changed');
  lines.push('');
  lines.push(analysis.summary);
  lines.push('');

  // Notable commits
  if (analysis.commits.length > 0) {
    lines.push('### Notable Commits');
    lines.push('');
    for (const c of analysis.commits.slice(0, 8)) {
      lines.push(`- \`${c.shortSha}\` — ${c.subject}`);
    }
    if (analysis.commits.length > 8) {
      lines.push(`- _...and ${analysis.commits.length - 8} more_`);
    }
    lines.push('');
  }

  // Impact
  lines.push('## Impact by Area');
  lines.push('');
  const impactTable = Object.entries(analysis.impact)
    .filter(([, v]) => v !== 'none')
    .map(([area, level]) => {
      const icon = level === 'high' ? '🔴' : level === 'medium' ? '🟡' : '🟢';
      const desc = IMPACT_DESCRIPTIONS[area] || area;
      return `| ${icon} ${area} | ${level} | ${desc} |`;
    });

  if (impactTable.length) {
    lines.push('| Area | Impact | What it means |');
    lines.push('|------|--------|----------------|');
    lines.push(...impactTable);
  } else {
    lines.push('No significant impact areas detected.');
  }
  lines.push('');

  // Portability
  lines.push('## Portability for Other Agents');
  lines.push('');
  lines.push('These changes have been classified for portability to non-Claude Code runtimes:');
  lines.push('');

  lines.push(`**✅ Portable as-is** (${analysis.portability.portable.length} files)`);
  if (analysis.portability.portable.length > 0) {
    lines.push('');
    analysis.portability.portable.slice(0, 12).forEach(f => lines.push(`- \`${f}\``));
    if (analysis.portability.portable.length > 12) lines.push(`- _...and ${analysis.portability.portable.length - 12} more_`);
  }
  lines.push('');

  if (analysis.portability.needsAdaptation.length > 0) {
    lines.push(`**🔧 Needs adaptation** (${analysis.portability.needsAdaptation.length} files)`);
    lines.push('');
    lines.push('These files use conventions that need to be translated for other runtimes:');
    analysis.portability.needsAdaptation.slice(0, 10).forEach(f => lines.push(`- \`${f}\``));
    lines.push('');
  }

  if (analysis.portability.hostSpecific.length > 0) {
    lines.push(`**🔒 Claude Code–specific** (${analysis.portability.hostSpecific.length} files)`);
    lines.push('');
    lines.push('These files use Claude Code–specific conventions. uStack emits advisory notes for other runtimes.');
    analysis.portability.hostSpecific.slice(0, 10).forEach(f => lines.push(`- \`${f}\``));
    lines.push('');
  }

  // How to use
  lines.push('## Using This Update');
  lines.push('');
  lines.push('If you track this upstream via uStack, run:');
  lines.push('');
  lines.push('```bash');
  lines.push(`ustack update ${analysis.upstreamId}`);
  lines.push('```');
  lines.push('');
  lines.push('This will pull the latest changes, re-analyze, and regenerate adapted output for your configured target runtimes.');
  lines.push('');

  // Trust note
  lines.push('## Trust Note');
  lines.push('');
  lines.push('This analysis is generated mechanically from git metadata. It classifies files by pattern, not by semantic understanding.');
  lines.push('Review the portability classification carefully before applying adapted output to production workflows.');
  lines.push('');

  // Footer
  lines.push('---');
  lines.push(`_Analyzed by [uStack](https://agi.security) · ${date} · [${analysis.repoUrl}](${analysis.repoUrl})_`);

  return lines.join('\n') + '\n';
}

const IMPACT_DESCRIPTIONS = {
  skills: 'One or more slash-command skills were updated',
  install: 'Setup, install, or onboarding flow changed',
  browser: 'Browser automation tooling changed',
  workflow: 'Core planning/review/ship workflow skills changed',
  safety: 'Safety guardrail behaviors changed',
  tooling: 'Internal binaries or scripts changed',
  docs: 'Documentation or README updated',
  config: 'Package config or CI configuration changed',
};

function upstreamDisplayName(id) {
  const names = {
    gstack: 'Gstack',
  };
  return names[id] || id.charAt(0).toUpperCase() + id.slice(1);
}
