/**
 * lib/bootstrap.mjs
 * Thin bootstrap for wip-install.
 * If ldm is on PATH, delegates to ldm install.
 * If not, installs LDM OS from npm, then delegates.
 * This replaces the 700-line standalone install.js from the toolbox.
 * Zero external dependencies.
 */

import { execSync } from 'node:child_process';

/**
 * Check if ldm CLI is available on PATH.
 * @returns {boolean}
 */
export function isLdmAvailable() {
  try {
    execSync('ldm --version', { stdio: 'pipe', timeout: 5000 });
    return true;
  } catch {
    return false;
  }
}

/**
 * Install LDM OS from npm registry.
 * @returns {boolean} true if install succeeded
 */
export function bootstrapLdmOs() {
  try {
    execSync('npm install -g @wipcomputer/wip-ldm-os', { stdio: 'pipe', timeout: 120000 });
    execSync('ldm init --yes --none', { stdio: 'pipe', timeout: 30000 });
    return isLdmAvailable();
  } catch {
    return false;
  }
}

/**
 * Delegate to ldm install with the given arguments.
 * @param {string} target - what to install (org/repo, path, or empty for update-all)
 * @param {string[]} flags - CLI flags (--dry-run, --json, etc.)
 */
export function delegateToLdm(target, flags = []) {
  const cmd = target
    ? `ldm install ${target} ${flags.join(' ')}`
    : `ldm install ${flags.join(' ')}`;
  execSync(cmd.trim(), { stdio: 'inherit' });
}

/**
 * Full bootstrap + delegate flow.
 * Called by wip-install as the entry point.
 * @param {string[]} argv - process.argv.slice(2)
 */
export function run(argv) {
  const target = argv.find(a => !a.startsWith('--'));
  const flags = argv.filter(a => a.startsWith('--'));
  const jsonOutput = flags.includes('--json');

  if (isLdmAvailable()) {
    if (!jsonOutput) {
      console.log('');
      console.log('  LDM OS detected. Delegating to ldm install...');
      console.log('');
    }
    delegateToLdm(target, flags);
    return;
  }

  // LDM not on PATH, try bootstrap
  if (!jsonOutput) {
    console.log('');
    console.log('  LDM OS not found. Installing...');
    console.log('');
  }

  if (bootstrapLdmOs()) {
    if (!jsonOutput) {
      console.log('  LDM OS installed. Delegating to ldm install...');
      console.log('');
    }
    delegateToLdm(target, flags);
  } else {
    if (!jsonOutput) {
      console.log('  LDM OS could not be installed automatically.');
      console.log('  Install manually: npm install -g @wipcomputer/wip-ldm-os');
      console.log('');
    }
    process.exit(1);
  }
}
