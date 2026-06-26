/**
 * SafeHub update command.
 * Pulls the latest Semgrep scanner rules from the SafeHub GitHub repo.
 */

const path = require('path');
const fs = require('fs').promises;
const https = require('https');

const RULES_REPO = process.env.SAFEHUB_RULES_REPO || 'safehub/safehub';
const GITHUB_API_BASE = 'https://api.github.com';
const RULES_DIR = path.join(__dirname, '..', 'rules');

/**
 * Fetches JSON from a URL using Node built-in https.
 * @param {string} url - Full URL
 * @returns {Promise<object>}
 */
function fetchJson(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers: { 'User-Agent': 'SafeHub/1.0' } }, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode === 404) {
          reject(new Error('Repo or rules path not found (404). Set SAFEHUB_RULES_REPO to your fork.'));
          return;
        }
        if (res.statusCode !== 200) {
          reject(new Error(`GitHub API returned ${res.statusCode}`));
          return;
        }
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error('Invalid JSON from GitHub'));
        }
      });
    });
    req.on('error', reject);
    req.setTimeout(15000, () => { req.destroy(); reject(new Error('Request timeout')); });
  });
}

/**
 * Fetches raw file content from GitHub.
 * @param {string} owner - Repo owner
 * @param {string} repo - Repo name
 * @param {string} filePath - Path in repo (e.g. rules/network.yml)
 * @param {string} branch - Branch (e.g. main)
 */
function fetchRawFile(owner, repo, filePath, branch) {
  const b = branch || 'main';
  const url = `https://raw.githubusercontent.com/${owner}/${repo}/${b}/${filePath}`;
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers: { 'User-Agent': 'SafeHub/1.0' } }, (res) => {
      if (res.statusCode === 302 || res.statusCode === 301) {
        const redirect = res.headers.location;
        return https.get(redirect, (r2) => {
          let d = '';
          r2.on('data', (c) => { d += c; });
          r2.on('end', () => resolve(d));
        }).on('error', reject);
      }
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
    req.setTimeout(10000, () => { req.destroy(); reject(new Error('Request timeout')); });
  });
}

/**
 * Pulls latest rules from GitHub and writes them to ./rules.
 * Uses SAFEHUB_RULES_REPO (default safehub/safehub) or branch via SAFEHUB_RULES_BRANCH (default main).
 * @returns {Promise<{ updated: boolean, message?: string, files?: string[] }>}
 */
async function updateRules() {
  const branch = process.env.SAFEHUB_RULES_BRANCH || 'main';
  const [owner, repo] = RULES_REPO.split('/').filter(Boolean);
  if (!owner || !repo) {
    return { updated: false, message: 'Invalid SAFEHUB_RULES_REPO (use owner/repo).' };
  }

  try {
    const contentsUrl = `${GITHUB_API_BASE}/repos/${owner}/${repo}/contents/rules`;
    const list = await fetchJson(contentsUrl);
    if (!Array.isArray(list)) {
      return { updated: false, message: 'No rules directory in repo.' };
    }

    const yamlFiles = list.filter((f) => f.name && f.name.endsWith('.yml'));
    const files = [];

    for (const file of yamlFiles) {
      const raw = await fetchRawFile(owner, repo, `rules/${file.name}`, branch);
      const outPath = path.join(RULES_DIR, file.name);
      await fs.mkdir(RULES_DIR, { recursive: true });
      await fs.writeFile(outPath, raw, 'utf8');
      files.push(file.name);
    }

    return { updated: true, files };
  } catch (err) {
    if (err.message && err.message.includes('timeout')) {
      return { updated: false, message: 'Update failed: timeout. Check network and SAFEHUB_RULES_REPO.' };
    }
    if (err.message && err.message.includes('Invalid JSON')) {
      return { updated: false, message: 'Update failed: invalid response from GitHub.' };
    }
    if (err.message && (err.message.includes('404') || err.message.includes('not found'))) {
      return { updated: false, message: err.message };
    }
    throw new Error(`Rules update failed: ${err.message}`);
  }
}

module.exports = { updateRules };
