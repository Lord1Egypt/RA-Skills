import fs from 'node:fs';
import path from 'node:path';
import { getCommitLog, getChangedFiles } from '../lib/git.js';
import { writeJson, writeText, fileExists, readJson, getUpstreamDir, getRunDir } from '../lib/fs.js';

/**
 * ustack analyze <upstream-id>
 *
 * Analyzes changes between previousSha and headSha.
 * Produces a structured analysis artifact at:
 *   .ustack/runs/<id>/<timestamp>/analysis.json
 *   .ustack/runs/<id>/<timestamp>/analysis.md
 */
export async function runAnalyze({ cwd, args = [] }) {
  const upstreamId = args[0];

  if (!upstreamId) {
    console.error('Usage: ustack analyze <upstream-id>');
    process.exitCode = 1;
    return;
  }

  const upstreamDir = getUpstreamDir(cwd, upstreamId);
  const manifestPath = path.join(upstreamDir, 'manifest.json');

  if (!fileExists(manifestPath)) {
    console.error(`Upstream "${upstreamId}" not found. Run: ustack import <url> --name ${upstreamId}`);
    process.exitCode = 1;
    return;
  }

  const manifest = readJson(manifestPath);
  const { repoDir, headSha, previousSha, repoUrl } = manifest;

  console.log(`Analyzing: ${upstreamId}`);
  console.log(`HEAD: ${headSha.slice(0, 12)}`);
  console.log(`Previous: ${previousSha ? previousSha.slice(0, 12) : 'none (first run)'}`);

  // Get commits in range
  const commits = getCommitLog(repoDir, previousSha, headSha);
  const changedFiles = getChangedFiles(repoDir, previousSha, headSha);

  console.log(`Commits: ${commits.length}`);
  console.log(`Changed files: ${changedFiles.length}`);

  // Classify changes by impact area
  const impact = classifyImpact(changedFiles, manifest.structure);

  // Classify portability of changed files
  const portabilityAnalysis = classifyPortability(changedFiles, manifest.keyFiles);

  // Read key file snippets for the analysis
  const keySnippets = {};
  const keyFilesToRead = ['README.md', 'CHANGELOG.md', 'ARCHITECTURE.md'].filter(
    f => changedFiles.some(c => c.path === f)
  );
  for (const kf of keyFilesToRead.slice(0, 3)) {
    const fullPath = path.join(repoDir, kf);
    if (fileExists(fullPath)) {
      keySnippets[kf] = fs.readFileSync(fullPath, 'utf8').split('\n').slice(0, 80).join('\n');
    }
  }

  // Build structured analysis
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const runDir = getRunDir(cwd, upstreamId, timestamp);

  const analysis = {
    upstreamId,
    repoUrl,
    analyzedAt: new Date().toISOString(),
    fromSha: previousSha,
    toSha: headSha,
    fromShaShort: previousSha ? previousSha.slice(0, 12) : null,
    toShaShort: headSha.slice(0, 12),
    commitCount: commits.length,
    changedFileCount: changedFiles.length,
    commits: commits.slice(0, 30),
    changedFiles,
    impact,
    portability: portabilityAnalysis,
    summary: buildSummary(commits, changedFiles, impact, manifest),
  };

  writeJson(path.join(runDir, 'analysis.json'), analysis);
  const mdReport = renderAnalysisMarkdown(analysis, keySnippets, manifest);
  writeText(path.join(runDir, 'analysis.md'), mdReport);

  // Update manifest with run reference
  manifest.lastAnalyzedAt = new Date().toISOString();
  manifest.lastRunDir = runDir;
  manifest.lastRunTimestamp = timestamp;
  writeJson(manifestPath, manifest);

  console.log(`\nAnalysis complete.`);
  console.log(`Run dir: .ustack/runs/${upstreamId}/${timestamp}/`);
  console.log(`\nImpact summary:`);
  for (const [area, level] of Object.entries(impact)) {
    if (level !== 'none') console.log(`  ${area}: ${level}`);
  }
  console.log(`\nPortability:`);
  console.log(`  portable: ${portabilityAnalysis.portable.length} files`);
  console.log(`  needs-adaptation: ${portabilityAnalysis.needsAdaptation.length} files`);
  console.log(`  host-specific: ${portabilityAnalysis.hostSpecific.length} files`);
  console.log(`\nNext: ustack publish ${upstreamId}`);
}

const IMPACT_CATEGORIES = {
  skills: {
    patterns: [/\/SKILL\.md$/, /\/SKILL\.md\.tmpl$/, /^[a-z-]+\/SKILL\./],
    description: 'Skill definitions changed',
  },
  install: {
    patterns: [/^setup/, /^bin\/dev-/, /CONTRIBUTING\.md$/, /README\.md$/],
    description: 'Install or setup flow changed',
  },
  browser: {
    patterns: [/^extension\//, /^browse\//, /^bin\/chrome/, /^bin\/gstack-open/, /^connect-chrome\//],
    description: 'Browser tooling changed',
  },
  workflow: {
    patterns: [/^review\//, /^ship\//, /^qa\//, /^plan-/, /^autoplan\//, /^retro\//],
    description: 'Core workflow skills changed',
  },
  safety: {
    patterns: [/^careful\//, /^freeze\//, /^guard\//, /^unfreeze\//],
    description: 'Safety/guardrail skills changed',
  },
  tooling: {
    patterns: [/^bin\/gstack-/, /^scripts\//, /^lib\//],
    description: 'Internal tooling changed',
  },
  docs: {
    patterns: [/^docs\//, /README\.md$/, /ARCHITECTURE\.md$/, /DESIGN\.md$/, /CHANGELOG\.md$/],
    description: 'Documentation changed',
  },
  config: {
    patterns: [/^package\.json$/, /^conductor\.json$/, /^\.github\//],
    description: 'Config or CI changed',
  },
};

function classifyImpact(changedFiles, structure) {
  const impact = {};

  for (const [area, { patterns }] of Object.entries(IMPACT_CATEGORIES)) {
    const matched = changedFiles.filter(({ path: p }) =>
      patterns.some(pattern => pattern.test(p))
    );
    impact[area] = matched.length === 0 ? 'none'
      : matched.length <= 2 ? 'low'
      : matched.length <= 6 ? 'medium'
      : 'high';
  }

  return impact;
}

const HOST_SPECIFIC_PATTERNS = [
  /CLAUDE\.md$/,
  /^\.claude\//,
  /^agents\/openai/,
  /^agents\/claude/,
  /hook.*claude/i,
];

const PORTABILITY_CONCERN_PATTERNS = [
  /SKILL\.md\.tmpl$/,    // template files need target-specific rendering
  /^bin\/gstack-/,        // binary tools — need rebuild for other hosts
  /^extension\//,         // Chrome extension — platform-specific
  /^lib\//,               // library code — may have host assumptions
];

function classifyPortability(changedFiles, keyFiles) {
  const portable = [];
  const needsAdaptation = [];
  const hostSpecific = [];

  for (const f of changedFiles) {
    const p = f.path;
    if (HOST_SPECIFIC_PATTERNS.some(pat => pat.test(p))) {
      hostSpecific.push(p);
    } else if (PORTABILITY_CONCERN_PATTERNS.some(pat => pat.test(p))) {
      needsAdaptation.push(p);
    } else {
      portable.push(p);
    }
  }

  return { portable, needsAdaptation, hostSpecific };
}

function buildSummary(commits, changedFiles, impact, manifest) {
  const highImpactAreas = Object.entries(impact)
    .filter(([, level]) => level === 'high')
    .map(([area]) => area);
  const mediumImpactAreas = Object.entries(impact)
    .filter(([, level]) => level === 'medium')
    .map(([area]) => area);

  const lines = [];

  if (commits.length === 0 && changedFiles.length === 0) {
    lines.push('No changes detected since last analysis.');
    return lines.join(' ');
  }

  lines.push(`${commits.length} commit(s), ${changedFiles.length} file(s) changed.`);

  if (highImpactAreas.length) {
    lines.push(`High-impact areas: ${highImpactAreas.join(', ')}.`);
  }
  if (mediumImpactAreas.length) {
    lines.push(`Medium-impact areas: ${mediumImpactAreas.join(', ')}.`);
  }

  // Notable commits
  if (commits.length > 0) {
    const notable = commits.slice(0, 3).map(c => c.subject).join('; ');
    lines.push(`Recent commits: ${notable}.`);
  }

  return lines.join(' ');
}

function renderAnalysisMarkdown(analysis, keySnippets, manifest) {
  const lines = [];

  lines.push(`# uStack Update Analysis — ${analysis.upstreamId}`);
  lines.push('');
  lines.push(`- upstream: [${analysis.repoUrl}](${analysis.repoUrl})`);
  lines.push(`- analyzed-at: ${analysis.analyzedAt}`);
  lines.push(`- from: \`${analysis.fromShaShort || 'initial'}\``);
  lines.push(`- to: \`${analysis.toShaShort}\``);
  lines.push(`- commits: ${analysis.commitCount}`);
  lines.push(`- files changed: ${analysis.changedFileCount}`);
  lines.push('');

  lines.push('## Summary');
  lines.push('');
  lines.push(analysis.summary || 'No changes detected.');
  lines.push('');

  lines.push('## Impact by Area');
  lines.push('');
  for (const [area, level] of Object.entries(analysis.impact)) {
    const icon = level === 'high' ? '🔴' : level === 'medium' ? '🟡' : level === 'low' ? '🟢' : '⚪';
    lines.push(`- ${icon} **${area}**: ${level}`);
  }
  lines.push('');

  lines.push('## Portability Assessment');
  lines.push('');
  lines.push(`- ✅ **Portable as-is**: ${analysis.portability.portable.length} files`);
  if (analysis.portability.portable.length > 0) {
    analysis.portability.portable.slice(0, 10).forEach(f => lines.push(`  - ${f}`));
  }
  lines.push(`- 🔧 **Needs adaptation**: ${analysis.portability.needsAdaptation.length} files`);
  if (analysis.portability.needsAdaptation.length > 0) {
    analysis.portability.needsAdaptation.slice(0, 10).forEach(f => lines.push(`  - ${f}`));
  }
  lines.push(`- 🔒 **Host-specific (Claude Code)**: ${analysis.portability.hostSpecific.length} files`);
  if (analysis.portability.hostSpecific.length > 0) {
    analysis.portability.hostSpecific.slice(0, 10).forEach(f => lines.push(`  - ${f}`));
  }
  lines.push('');

  if (analysis.commits.length > 0) {
    lines.push('## Commits');
    lines.push('');
    for (const c of analysis.commits.slice(0, 15)) {
      lines.push(`- \`${c.shortSha}\` ${c.subject} _(${c.date.split('T')[0]})_`);
    }
    lines.push('');
  }

  if (analysis.changedFiles.length > 0) {
    lines.push('## Changed Files');
    lines.push('');
    const byStatus = {};
    for (const f of analysis.changedFiles) {
      (byStatus[f.status] = byStatus[f.status] || []).push(f.path);
    }
    for (const [status, files] of Object.entries(byStatus)) {
      const label = status === 'A' ? 'Added' : status === 'M' ? 'Modified' : status === 'D' ? 'Deleted' : status;
      lines.push(`**${label}** (${files.length}):`);
      files.slice(0, 20).forEach(f => lines.push(`- ${f}`));
      if (files.length > 20) lines.push(`- ...and ${files.length - 20} more`);
      lines.push('');
    }
  }

  if (Object.keys(keySnippets).length > 0) {
    lines.push('## Key File Snapshots');
    lines.push('');
    for (const [filename, content] of Object.entries(keySnippets)) {
      lines.push(`### ${filename} (first 80 lines)`);
      lines.push('');
      lines.push('```markdown');
      lines.push(content.trim());
      lines.push('```');
      lines.push('');
    }
  }

  lines.push('## Next Steps');
  lines.push('');
  lines.push('1. Review portability assessment above.');
  lines.push('2. Run `ustack publish <id>` to generate a website-ready update page.');
  lines.push('3. Review and merge generated adapter output for supported targets.');
  lines.push('');
  lines.push('---');
  lines.push(`_Generated by uStack v0.1.0_`);

  return lines.join('\n') + '\n';
}
