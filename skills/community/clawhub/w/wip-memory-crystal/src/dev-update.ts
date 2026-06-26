// memory-crystal/dev-update.ts — Auto-generate dev updates for changed repos.
// Called before compaction (Lēsa) or at session end when context is high (CC).
// Scans all repos for recent git activity, writes dated updates to wip-dev-updates.

import { execSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join, basename } from 'node:path';
import { resolveStatePath, stateWritePath } from './ldm.js';

const HOME = process.env.HOME || '';

function resolveWorkspace(): string {
  const configPath = join(HOME, '.ldm', 'config.json');
  if (existsSync(configPath)) {
    try {
      const config = JSON.parse(readFileSync(configPath, 'utf-8'));
      if (config.workspace) return config.workspace;
    } catch {}
  }
  return join(HOME, 'wipcomputerinc');
}

const TEAM_DIR = join(resolveWorkspace(), 'team');
const CC_REPOS = join(TEAM_DIR, 'cc-mini', 'repos');
const LESA_REPOS = join(TEAM_DIR, 'Lēsa', 'repos');
const DEV_UPDATES_DIR = join(CC_REPOS, 'wip-dev-updates'); // Legacy, kept for fallback
const LAST_RUN_PATH = resolveStatePath('dev-update-last-run.json');

interface LastRun {
  timestamp: string;
  author: string;
  reposUpdated: number;
}

function loadLastRun(): LastRun | null {
  try {
    if (existsSync(LAST_RUN_PATH)) {
      return JSON.parse(readFileSync(LAST_RUN_PATH, 'utf-8'));
    }
  } catch {}
  return null;
}

function saveLastRun(run: LastRun): void {
  const writePath = stateWritePath('dev-update-last-run.json');
  writeFileSync(writePath, JSON.stringify(run, null, 2));
}

function git(repoPath: string, cmd: string): string {
  try {
    return execSync(`git -C "${repoPath}" ${cmd}`, {
      encoding: 'utf-8',
      timeout: 10000,
      stdio: ['pipe', 'pipe', 'pipe'],
    }).trim();
  } catch {
    return '';
  }
}

function scanRepo(repoPath: string, since: string): string | null {
  if (!existsSync(join(repoPath, '.git'))) return null;

  const name = basename(repoPath);
  if (name === '_third-party-repos' || name === 'wip-dev-updates') return null;

  const recentCommits = git(repoPath, `log --oneline --since="${since}"`);
  const uncommitted = git(repoPath, 'status --porcelain');

  if (!recentCommits && !uncommitted) return null;

  const lines: string[] = [];
  lines.push(`# ${name}`);
  lines.push('');

  if (recentCommits) {
    lines.push('## Recent Commits');
    lines.push('');
    lines.push('```');
    lines.push(...recentCommits.split('\n').slice(0, 10));
    lines.push('```');
    lines.push('');
  }

  if (uncommitted) {
    lines.push('## Uncommitted Changes');
    lines.push('');
    lines.push('```');
    lines.push(...uncommitted.split('\n').slice(0, 20));
    lines.push('```');
    lines.push('');
  }

  if (recentCommits) {
    const diffStat = git(repoPath, `diff --stat "HEAD@{${since}}" HEAD`);
    if (diffStat) {
      lines.push('## Files Changed');
      lines.push('');
      lines.push('```');
      lines.push(...diffStat.split('\n').slice(-15));
      lines.push('```');
      lines.push('');
    }
  }

  const branch = git(repoPath, 'branch --show-current') || 'unknown';
  lines.push(`**Branch:** ${branch}`);
  lines.push('');

  return lines.join('\n');
}

export function runDevUpdate(author: 'cc' | 'lesa'): { reposUpdated: number; files: string[] } {
  // Throttle: don't run more than once per hour
  const lastRun = loadLastRun();
  if (lastRun) {
    const elapsed = Date.now() - new Date(lastRun.timestamp).getTime();
    if (elapsed < 60 * 60 * 1000) {
      return { reposUpdated: 0, files: [] };
    }
  }

  // Determine "since" window: since last run, or 6 hours
  let since = '6 hours ago';
  if (lastRun?.timestamp) {
    const lastDate = new Date(lastRun.timestamp);
    const hoursAgo = Math.ceil((Date.now() - lastDate.getTime()) / (1000 * 60 * 60));
    since = `${Math.max(hoursAgo, 1)} hours ago`;
  }

  const now = new Date();
  const ts = [
    String(now.getMonth() + 1).padStart(2, '0'),
    String(now.getDate()).padStart(2, '0'),
    String(now.getFullYear()),
  ].join('-') + '--' + [
    String(now.getHours()).padStart(2, '0'),
    String(now.getMinutes()).padStart(2, '0'),
    String(now.getSeconds()).padStart(2, '0'),
  ].join('-');

  const files: string[] = [];

  // Scan all repo directories
  const repoDirs = [CC_REPOS, LESA_REPOS];
  for (const parentDir of repoDirs) {
    if (!existsSync(parentDir)) continue;
    let entries: string[];
    try {
      entries = execSync(`ls "${parentDir}"`, { encoding: 'utf-8' }).trim().split('\n');
    } catch { continue; }

    for (const entry of entries) {
      const repoPath = join(parentDir, entry);
      const content = scanRepo(repoPath, since);
      if (!content) continue;

      const repoName = basename(repoPath);
      // Write to repo's own ai/ folder (decentralized)
      const outDir = join(repoPath, 'ai');
      const outFile = join(outDir, `${now.toISOString().slice(0, 10)}--${now.toISOString().slice(11, 19).replace(/:/g, '-')}--${author}--dev-update-${repoName}.md`);

      mkdirSync(outDir, { recursive: true });

      const header = `*Auto-generated dev update by ${author} at ${now.toISOString().slice(0, 16).replace('T', ' ')}*\n\n`;
      writeFileSync(outFile, content.replace(/^# .+\n/, `$&\n${header}`));
      files.push(`${repoName}/ai/${basename(outFile)}`);
    }
  }

  // Dev updates now in each repo's ai/ folder. Skip centralized commit.
  if (false && files.length > 0 && existsSync(join(DEV_UPDATES_DIR, '.git'))) {
    try {
      execSync(
        `cd "${DEV_UPDATES_DIR}" && git add -A && git commit -m "${author} auto-dev-update ${ts}: ${files.length} repo(s)" --no-verify && git push --quiet`,
        { encoding: 'utf-8', timeout: 30000, stdio: 'pipe' }
      );
    } catch {
      // best-effort
    }
  }

  saveLastRun({
    timestamp: now.toISOString(),
    author,
    reposUpdated: files.length,
  });

  return { reposUpdated: files.length, files };
}
