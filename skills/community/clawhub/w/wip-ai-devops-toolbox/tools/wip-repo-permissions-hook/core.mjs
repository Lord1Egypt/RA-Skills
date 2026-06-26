/**
 * wip-repo-permissions-hook/core.mjs
 * Pure logic for repo visibility permissions.
 * Blocks repos from going public without a -private counterpart.
 * Zero dependencies. Uses gh CLI for GitHub API calls.
 */

import { execFileSync } from 'node:child_process';

/**
 * Check if a repo has a -private counterpart on GitHub.
 * @param {string} org - GitHub org (e.g. "wipcomputer")
 * @param {string} repoName - Repo name (e.g. "memory-crystal")
 * @returns {{ allowed: boolean, reason: string }}
 */
export function checkPrivateCounterpart(org, repoName) {
  // If the repo itself IS the private repo, allow
  if (repoName.endsWith('-private')) {
    return { allowed: true, reason: `${repoName} is already a private repo.` };
  }

  // Check if it's a fork (forks of external projects are exempt)
  const forkStatus = isThirdPartyFork(org, repoName);
  if (forkStatus.isFork) {
    return { allowed: true, reason: `${repoName} is a fork of ${forkStatus.parent}. Forks are exempt.` };
  }

  // Check if -private counterpart exists
  const privateName = `${repoName}-private`;
  try {
    execFileSync('gh', ['api', `repos/${org}/${privateName}`, '--jq', '.name'], {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: 10000,
    });
    return { allowed: true, reason: `${privateName} exists. ${repoName} can be public.` };
  } catch {
    return {
      allowed: false,
      reason: `BLOCKED: ${org}/${repoName} cannot be made public. No -private counterpart found (expected ${org}/${privateName}). Create the -private repo first, move all ai/ content there, then make this repo public.`,
    };
  }
}

/**
 * Check if a repo is a fork of an external project.
 * @param {string} org
 * @param {string} repoName
 * @returns {{ isFork: boolean, parent: string }}
 */
export function isThirdPartyFork(org, repoName) {
  try {
    const json = execFileSync('gh', ['api', `repos/${org}/${repoName}`, '--jq', '{fork: .fork, parent: .parent.full_name}'], {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: 10000,
    });
    const data = JSON.parse(json);
    if (data.fork && data.parent && !data.parent.startsWith(`${org}/`)) {
      return { isFork: true, parent: data.parent };
    }
    return { isFork: false, parent: '' };
  } catch {
    return { isFork: false, parent: '' };
  }
}

/**
 * Audit all public repos in an org for missing -private counterparts.
 * @param {string} org
 * @returns {{ violations: Array<{name: string, reason: string}>, ok: Array<{name: string, reason: string}> }}
 */
export function auditOrg(org) {
  // Get all public repos
  let repos;
  try {
    const json = execFileSync('gh', [
      'repo', 'list', org,
      '--visibility', 'public',
      '--json', 'name',
      '--limit', '200',
    ], { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'], timeout: 30000 });
    repos = JSON.parse(json);
  } catch (e) {
    throw new Error(`Failed to list repos for ${org}: ${e.message}`);
  }

  const violations = [];
  const ok = [];

  for (const repo of repos) {
    const result = checkPrivateCounterpart(org, repo.name);
    if (result.allowed) {
      ok.push({ name: repo.name, reason: result.reason });
    } else {
      violations.push({ name: repo.name, reason: result.reason });
    }
  }

  return { violations, ok };
}

/**
 * Extract repo org/name from a gh command string.
 * Looks for patterns like: gh repo edit wipcomputer/repo-name --visibility public
 * @param {string} command
 * @returns {{ org: string, repo: string, isVisibilityChange: boolean } | null}
 */
export function parseVisibilityCommand(command) {
  // Match: gh repo edit <org/repo> ... --visibility public
  const editMatch = command.match(/gh\s+repo\s+edit\s+([^\s]+)/);
  if (!editMatch) return null;

  const visibilityMatch = command.match(/--visibility\s+(public|private|internal)/);
  if (!visibilityMatch || visibilityMatch[1] !== 'public') return null;

  const slug = editMatch[1];
  const parts = slug.split('/');
  if (parts.length !== 2) return null;

  return { org: parts[0], repo: parts[1], isVisibilityChange: true };
}
