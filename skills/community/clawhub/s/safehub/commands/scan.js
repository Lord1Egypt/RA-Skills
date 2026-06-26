/**
 * SafeHub scan command.
 * Resolves target (path or GitHub URL), runs Semgrep, optional Docker sandbox,
 * calculates trust score, and returns a report (formatted and cached).
 */

const path = require('path');
const { resolveTarget } = require('../lib/resolve');
const { runStaticScan } = require('../scanner/static');
const { runSandbox } = require('../scanner/sandbox');
const { calculateTrustScore } = require('../scanner/scorer');
const { formatReport } = require('./formatReport');
const { saveReport } = require('./report');

const RULES_DIR = path.join(__dirname, '..', 'rules');

/**
 * Runs the full scan pipeline and returns the report object plus formatted text.
 * @param {string} target - Skill name, local path, or GitHub URL
 * @param {object} options - { skipSandbox: boolean }
 * @returns {Promise<{ report: object, formatted: string }>}
 */
async function runScan(target, options = {}) {
  const resolved = await resolveTarget(target);
  const { path: scanPath, name, version, _tempClone } = resolved;

  let staticFindings = [];
  let sandboxResult = { networkAttempted: false, suspiciousSyscalls: [], sensitiveReads: [] };

  try {
    const staticResult = await runStaticScan(scanPath, RULES_DIR);
    staticFindings = staticResult.findings || [];
  } catch (err) {
    throw new Error(`Static scan failed: ${err.message}`);
  }

  try {
    sandboxResult = await runSandbox(scanPath, {
      skipSandbox: options.skipSandbox,
      timeoutMs: parseInt(process.env.SAFEHUB_SANDBOX_TIMEOUT_MS || '30000', 10)
    });
  } catch (err) {
    sandboxResult = {
      networkAttempted: false,
      suspiciousSyscalls: [],
      sensitiveReads: [],
      error: err.message,
      skipped: true
    };
  }

  const hasRepoLink = !!_tempClone || !!target.match(/^https?:\/\//);
  const { score, level } = calculateTrustScore(staticFindings, sandboxResult, {
    hasDependencyVulns: false,
    hasRepoLink
  });

  const report = {
    target,
    name,
    version,
    scanPath,
    staticFindings,
    sandboxResult,
    trustScore: score,
    level,
    scannedAt: new Date().toISOString()
  };

  const formatted = formatReport(report);

  try {
    await saveReport(name, report);
  } catch (_) {
    // Non-fatal if we can't cache
  }

  return {
    report,
    formatted,
    trustScore: score,
    level
  };
}

module.exports = { runScan };
