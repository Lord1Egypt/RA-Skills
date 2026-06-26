/**
 * Static analysis using Semgrep.
 * Runs Semgrep CLI with rules from ./rules against skill source code.
 * Returns normalized findings for the report and scorer.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs').promises;

const SEMGREP_TIMEOUT_MS = 120000;

/**
 * Runs Semgrep scan and returns parsed findings.
 * @param {string} sourcePath - Absolute path to skill directory to scan
 * @param {string} rulesDir - Absolute path to directory containing .yml rules
 * @returns {Promise<{findings: Array<{ruleId: string, message: string, severity: string, path: string, line: number}>}>}
 */
async function runStaticScan(sourcePath, rulesDir) {
  const normalizedPath = path.resolve(sourcePath);
  const normalizedRules = path.resolve(rulesDir);

  try {
    await fs.access(normalizedPath);
    await fs.access(normalizedRules);
  } catch (err) {
    throw new Error(`Static scan: path not accessible (${err.message})`);
  }

  return new Promise((resolve, reject) => {
    const args = [
      'scan',
      '--config', normalizedRules,
      '--json',
      '--no-git-ignore',
      '--quiet',
      normalizedPath
    ];

    const proc = spawn('semgrep', args, {
      timeout: SEMGREP_TIMEOUT_MS,
      shell: false
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (chunk) => { stdout += chunk; });
    proc.stderr.on('data', (chunk) => { stderr += chunk; });

    proc.on('error', (err) => {
      if (err.code === 'ENOENT') {
        reject(new Error('Semgrep not found. Install it: npm install -g semgrep or brew install semgrep'));
      } else {
        reject(err);
      }
    });

    proc.on('close', (code) => {
      try {
        const parsed = JSON.parse(stdout || '{}');
        const results = parsed.results || [];
        const findings = results.map((r) => ({
          ruleId: r.check_id || r.rule_id || 'unknown',
          message: r.extra?.message || r.message || 'Finding',
          severity: (r.extra?.severity || r.severity || 'MEDIUM').toUpperCase(),
          path: r.path || r.file_path || '',
          line: r.start?.line ?? r.line ?? 0
        }));
        resolve({ findings });
      } catch (parseErr) {
        if (stderr.includes('Invalid rule')) {
          reject(new Error(`Semgrep rule error: ${stderr.trim()}`));
        } else if (code !== 0 && code !== 1) {
          reject(new Error(`Semgrep failed: ${stderr.trim() || stdout.trim() || 'unknown'}`));
        } else {
          resolve({ findings: [] });
        }
      }
    });
  });
}

module.exports = { runStaticScan };
