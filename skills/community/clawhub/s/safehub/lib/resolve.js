/**
 * Resolves a scan target (skill name, path, or GitHub URL) to a local directory path.
 * For ClawHub skill names we do not have an API; we treat as "not found" and suggest path/URL.
 */

const path = require('path');
const fs = require('fs').promises;
const os = require('os');
const { execSync } = require('child_process');

const GITHUB_URL_REGEX = /^https?:\/\/(?:www\.)?github\.com\/([^/]+)\/([^/]+?)(?:\.git)?(?:\/.*)?$/i;

/**
 * Resolves target to an absolute path to a directory containing skill code.
 * @param {string} target - Skill name, local path, or GitHub URL
 * @returns {Promise<{ path: string, name: string, version?: string }>}
 */
async function resolveTarget(target) {
  const trimmed = (target || '').trim();
  if (!trimmed) {
    throw new Error('Scan target is required (skill name, path, or GitHub URL).');
  }

  if (GITHUB_URL_REGEX.test(trimmed)) {
    return resolveGitHubUrl(trimmed);
  }

  const asPath = path.resolve(trimmed);
  try {
    const stat = await fs.stat(asPath);
    if (!stat.isDirectory()) {
      throw new Error(`Target is not a directory: ${trimmed}`);
    }
    const name = path.basename(asPath);
    let version;
    try {
      const pkgPath = path.join(asPath, 'package.json');
      const pkg = JSON.parse(await fs.readFile(pkgPath, 'utf8'));
      version = pkg.version;
    } catch {
      try {
        const skillPath = path.join(asPath, 'skill.json');
        const skill = JSON.parse(await fs.readFile(skillPath, 'utf8'));
        version = skill.version;
      } catch {
        version = undefined;
      }
    }
    return { path: asPath, name, version };
  } catch (err) {
    if (err.code === 'ENOENT') {
      throw new Error(
        `Target not found: "${trimmed}". Use a local path or a GitHub URL (e.g. https://github.com/user/repo).`
      );
    }
    throw err;
  }
}

/**
 * Clones a GitHub repo to a temp dir and returns its path.
 */
async function resolveGitHubUrl(url) {
  const match = url.match(GITHUB_URL_REGEX);
  if (!match) {
    throw new Error('Invalid GitHub URL.');
  }

  const [, owner, repo] = match;
  const repoName = repo.replace(/\.git$/i, '');
  const cloneDir = path.join(os.tmpdir(), `safehub-scan-${repoName}-${Date.now()}`);

  try {
    execSync(`git clone --depth 1 "${url}" "${cloneDir}"`, {
      stdio: 'pipe',
      timeout: 60000
    });
  } catch (err) {
    throw new Error(`Failed to clone repository: ${err.message}`);
  }

  let version;
  try {
    const pkgPath = path.join(cloneDir, 'package.json');
    const pkg = JSON.parse(await fs.readFile(pkgPath, 'utf8'));
    version = pkg.version;
  } catch {
    try {
      const skillPath = path.join(cloneDir, 'skill.json');
      const skill = JSON.parse(await fs.readFile(skillPath, 'utf8'));
      version = skill.version;
    } catch {
      version = undefined;
    }
  }

  return {
    path: cloneDir,
    name: repoName,
    version,
    _tempClone: true
  };
}

module.exports = { resolveTarget, GITHUB_URL_REGEX };
