import { execSync, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

/**
 * Clone or pull an upstream repo into a target directory.
 * Returns the HEAD commit sha after the operation.
 */
export function syncUpstream({ repoUrl, targetDir }) {
  if (fs.existsSync(path.join(targetDir, '.git'))) {
    // Pull latest
    const result = spawnSync('git', ['pull', '--ff-only'], {
      cwd: targetDir,
      encoding: 'utf8',
    });
    if (result.status !== 0) {
      throw new Error(`git pull failed: ${result.stderr}`);
    }
  } else {
    // Clone
    fs.mkdirSync(targetDir, { recursive: true });
    const result = spawnSync('git', ['clone', '--depth', '50', repoUrl, targetDir], {
      encoding: 'utf8',
    });
    if (result.status !== 0) {
      throw new Error(`git clone failed: ${result.stderr}`);
    }
  }

  return getHead(targetDir);
}

/**
 * Get the current HEAD sha.
 */
export function getHead(repoDir) {
  return execSync('git rev-parse HEAD', { cwd: repoDir, encoding: 'utf8' }).trim();
}

/**
 * Get the short sha.
 */
export function getShortHead(repoDir) {
  return execSync('git rev-parse --short HEAD', { cwd: repoDir, encoding: 'utf8' }).trim();
}

/**
 * Get commit log between two shas.
 * Returns array of { sha, shortSha, date, subject }
 */
export function getCommitLog(repoDir, fromSha, toSha = 'HEAD') {
  const sep = '|||';
  const format = `%H${sep}%h${sep}%ci${sep}%s`;
  const range = fromSha ? `${fromSha}..${toSha}` : toSha;

  let raw;
  try {
    raw = execSync(`git log --format="${format}" ${range}`, {
      cwd: repoDir,
      encoding: 'utf8',
    }).trim();
  } catch {
    return [];
  }

  if (!raw) return [];

  return raw.split('\n').map((line) => {
    const [sha, shortSha, date, ...subjectParts] = line.split(sep);
    return { sha, shortSha, date: date.trim(), subject: subjectParts.join(sep) };
  });
}

/**
 * Get list of files changed between two shas.
 * Returns array of { status, path } where status is A/M/D/R etc.
 */
export function getChangedFiles(repoDir, fromSha, toSha = 'HEAD') {
  if (!fromSha) return [];

  let raw;
  try {
    raw = execSync(`git diff --name-status ${fromSha} ${toSha}`, {
      cwd: repoDir,
      encoding: 'utf8',
    }).trim();
  } catch {
    return [];
  }

  if (!raw) return [];

  return raw.split('\n').map((line) => {
    const parts = line.split('\t');
    return { status: parts[0], path: parts[1] || parts[2] || '' };
  });
}

/**
 * Get the content of a file at a specific sha.
 */
export function getFileAtRevision(repoDir, filePath, sha) {
  try {
    return execSync(`git show ${sha}:${filePath}`, {
      cwd: repoDir,
      encoding: 'utf8',
    });
  } catch {
    return null;
  }
}

/**
 * Get tags sorted by version/date (newest first).
 */
export function getTags(repoDir) {
  try {
    return execSync('git tag --sort=-version:refname', {
      cwd: repoDir,
      encoding: 'utf8',
    }).trim().split('\n').filter(Boolean);
  } catch {
    return [];
  }
}
