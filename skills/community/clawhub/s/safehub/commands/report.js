/**
 * SafeHub report command.
 * Shows the last scan report for a skill without rescanning.
 * Uses cached report from ~/.safehub/reports/<skill-name>.json
 */

const path = require('path');
const fs = require('fs').promises;
const os = require('os');
const { formatReport } = require('./formatReport');

const SAFEHUB_DATA_DIR = process.env.SAFEHUB_DATA_DIR || path.join(os.homedir(), '.safehub');
const REPORTS_DIR = path.join(SAFEHUB_DATA_DIR, 'reports');

/**
 * Returns the path where we store the cached report for a given skill name.
 * @param {string} skillName - Normalized skill name (e.g. repo name or folder name)
 */
function getReportPath(skillName) {
  const safeName = (skillName || '').replace(/[^a-zA-Z0-9-_]/g, '_');
  return path.join(REPORTS_DIR, `${safeName}.json`);
}

/**
 * Loads and returns the last scan report for a skill, or null if none.
 * @param {string} skillName - Skill name used when scanning
 * @returns {Promise<object | null>} Cached report object or null
 */
async function loadReport(skillName) {
  try {
    const filePath = getReportPath(skillName);
    const data = await fs.readFile(filePath, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    if (err.code === 'ENOENT') return null;
    throw err;
  }
}

/**
 * Saves a scan result as the last report for a skill (used by scan command).
 * @param {string} skillName - Skill name to key the report
 * @param {object} report - Full report object to cache
 */
async function saveReport(skillName, report) {
  try {
    await fs.mkdir(REPORTS_DIR, { recursive: true });
    const filePath = getReportPath(skillName);
    await fs.writeFile(filePath, JSON.stringify(report, null, 0), 'utf8');
  } catch (err) {
    throw new Error(`Failed to cache report: ${err.message}`);
  }
}

/**
 * Shows the last scan report for a skill without rescanning.
 * @param {string} skillName - Skill name
 * @returns {Promise<string | null>} Formatted report text, or null if no cached report
 */
async function showReport(skillName) {
  const report = await loadReport(skillName);
  if (!report) return null;
  return formatReport(report);
}

module.exports = { showReport, loadReport, saveReport, getReportPath };
