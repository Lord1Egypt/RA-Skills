/**
 * Trust score calculator (0–100).
 * Combines static findings, sandbox behavior, dependency checks, and repo metadata.
 */

const CRITICAL_PENALTY = 25;
const HIGH_PENALTY = 15;
const MEDIUM_PENALTY = 8;
const LOW_PENALTY = 3;

const POINTS_STATIC_CLEAN = 40;
const POINTS_SANDBOX_CLEAN = 30;
const POINTS_DEPS_CLEAN = 20;
const POINTS_REPO_LINKED = 10;

const LEVEL_SAFE = 'SAFE TO INSTALL';
const LEVEL_CAUTION = 'INSTALL WITH CAUTION';
const LEVEL_UNSAFE = 'NOT SAFE TO INSTALL';

/**
 * Calculates trust score and recommendation from scan results.
 * @param {Array<{ severity: string }>} staticFindings - Findings from Semgrep
 * @param {{ networkAttempted?: boolean, suspiciousSyscalls?: string[], sensitiveReads?: string[], exitCode?: number | null, error?: string, skipped?: boolean }} sandboxResult - Sandbox run result
 * @param {object} options - { hasDependencyVulns: boolean, hasRepoLink: boolean }
 * @returns {{ score: number, level: string, breakdown?: object }}
 */
function calculateTrustScore(staticFindings, sandboxResult, options = {}) {
  const hasDependencyVulns = options.hasDependencyVulns === true;
  const hasRepoLink = options.hasRepoLink === true;

  let score = 100;

  for (const f of staticFindings || []) {
    const sev = (f.severity || 'MEDIUM').toUpperCase();
    if (sev === 'CRITICAL') score -= CRITICAL_PENALTY;
    else if (sev === 'HIGH') score -= HIGH_PENALTY;
    else if (sev === 'MEDIUM') score -= MEDIUM_PENALTY;
    else if (sev === 'LOW') score -= LOW_PENALTY;
  }

  if (sandboxResult && !sandboxResult.skipped) {
    if (sandboxResult.networkAttempted) score -= 30;
    if ((sandboxResult.suspiciousSyscalls || []).length > 0) score -= 20;
    if ((sandboxResult.sensitiveReads || []).length > 0) score -= 15;
    if (sandboxResult.error) score -= 10;
  }

  if (hasDependencyVulns) score -= POINTS_DEPS_CLEAN;
  if (!hasRepoLink) score -= POINTS_REPO_LINKED;

  if (score < 0) score = 0;

  let level = LEVEL_UNSAFE;
  if (score >= 80) level = LEVEL_SAFE;
  else if (score >= 50) level = LEVEL_CAUTION;

  return {
    score: Math.round(score),
    level,
    breakdown: {
      staticFindings: (staticFindings || []).length,
      sandboxClean: sandboxResult && !sandboxResult.networkAttempted && (sandboxResult.suspiciousSyscalls || []).length === 0,
      depsClean: !hasDependencyVulns,
      repoLinked: hasRepoLink
    }
  };
}

module.exports = { calculateTrustScore, LEVEL_SAFE, LEVEL_CAUTION, LEVEL_UNSAFE };
