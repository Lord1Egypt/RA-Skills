/**
 * Formats a SafeHub scan result as terminal output.
 * Uses ✅ / ⚠️ / ❌ and the structure from the spec.
 */

const path = require('path');

const LEVEL_SAFE = 'SAFE TO INSTALL';
const LEVEL_CAUTION = 'INSTALL WITH CAUTION';
const LEVEL_UNSAFE = 'NOT SAFE TO INSTALL';

/**
 * Formats a single finding for static or sandbox section.
 * @param {{ message: string, severity: string, path?: string, line?: number }} f
 * @param {string} basePath - Base path to relativize file paths
 */
function formatFinding(f, basePath) {
  const file = f.path ? path.relative(basePath || '.', f.path) : 'unknown';
  const line = f.line != null ? ` line ${f.line}` : '';
  const icon = f.severity === 'CRITICAL' || f.severity === 'HIGH' ? '❌' : '⚠️';
  return `${icon}  ${f.message}${file !== 'unknown' ? ` in ${file}${line}` : ''}`;
}

/**
 * Builds the full report string for a scan result.
 * @param {object} report - Cached report: { target, name, version, staticFindings, sandboxResult, trustScore, level, recommendation }
 * @returns {string}
 */
function formatReport(report) {
  const name = report.name || report.target || 'unknown';
  const version = report.version ? ` v${report.version}` : '';
  const staticFindings = report.staticFindings || [];
  const sandboxResult = report.sandboxResult || {};
  const score = report.trustScore ?? report.score ?? 0;
  const level = report.level || report.trustLevel || LEVEL_UNSAFE;
  const basePath = report.scanPath || '';

  const lines = [
    `Scanning ${name}${version}...`,
    '─────────────────────────────',
    'STATIC ANALYSIS:'
  ];

  const networkFindings = staticFindings.filter((f) =>
    (f.ruleId || '').toLowerCase().includes('network')
  );
  const fsFindings = staticFindings.filter((f) =>
    (f.ruleId || '').toLowerCase().includes('filesystem')
  );
  const execFindings = staticFindings.filter((f) =>
    (f.ruleId || '').toLowerCase().includes('execution') || (f.ruleId || '').toLowerCase().includes('eval')
  );
  const envFindings = staticFindings.filter((f) =>
    (f.ruleId || '').toLowerCase().includes('env')
  );
  const obfuscationFindings = staticFindings.filter((f) =>
    (f.ruleId || '').toLowerCase().includes('obfuscation')
  );

  if (networkFindings.length === 0) {
    lines.push('✅ No outbound network calls detected');
  } else {
    networkFindings.forEach((f) => lines.push(formatFinding(f, basePath)));
  }

  if (fsFindings.length === 0) {
    lines.push('✅ No filesystem writes outside /tmp');
  } else {
    fsFindings.forEach((f) => lines.push(formatFinding(f, basePath)));
  }

  envFindings.forEach((f) => lines.push(formatFinding(f, basePath)));
  obfuscationFindings.forEach((f) => lines.push(formatFinding(f, basePath)));
  execFindings.forEach((f) => lines.push(formatFinding(f, basePath)));

  const otherFindings = staticFindings.filter(
    (f) =>
      !networkFindings.includes(f) &&
      !fsFindings.includes(f) &&
      !envFindings.includes(f) &&
      !obfuscationFindings.includes(f) &&
      !execFindings.includes(f)
  );
  otherFindings.forEach((f) => lines.push(formatFinding(f, basePath)));

  lines.push('', 'SANDBOX BEHAVIOR:');
  if (sandboxResult.skipped) {
    lines.push('⚠️  Sandbox skipped (no Docker or --no-sandbox)');
  } else {
    if (!sandboxResult.networkAttempted) {
      lines.push('✅ No network connections attempted');
    } else {
      lines.push('❌ Network connection attempted');
    }
    if ((sandboxResult.suspiciousSyscalls || []).length === 0) {
      lines.push('✅ No suspicious syscalls');
    } else {
      sandboxResult.suspiciousSyscalls.forEach((s) => lines.push(`❌ ${s}`));
    }
    if ((sandboxResult.sensitiveReads || []).length > 0) {
      sandboxResult.sensitiveReads.forEach((s) => lines.push(`⚠️  Attempted to read ${s}`));
    }
    if (sandboxResult.error) {
      lines.push(`⚠️  Sandbox error: ${sandboxResult.error}`);
    }
  }

  const scoreIcon = score >= 80 ? '✅' : score >= 50 ? '⚠️' : '❌';
  lines.push(
    '',
    `TRUST SCORE: ${score}/100 ${scoreIcon} ${level}`,
    '─────────────────────────────'
  );

  const issueCount = staticFindings.length + (sandboxResult.sensitiveReads || []).length;
  let recommendation;
  if (score >= 80) {
    recommendation = 'RECOMMENDATION: This skill appears safe to install.';
  } else if (score >= 50) {
    recommendation = 'RECOMMENDATION: Install with caution. Review the issues above.';
  } else {
    recommendation = 'RECOMMENDATION: Do not install this skill.';
  }
  lines.push(recommendation);
  if (issueCount > 0) {
    lines.push(`${issueCount} issue(s) found. See full report above.`);
  }

  return lines.join('\n');
}

module.exports = { formatReport, formatFinding };
