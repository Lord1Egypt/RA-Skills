#!/usr/bin/env node
'use strict';

const path = require('path');
const fs = require('fs');
const os = require('os');
const { execSync } = require('child_process');

const projectPath = process.argv[2];

if (!projectPath) {
  console.log(JSON.stringify({
    action: 'init',
    status: 'error',
    error: 'missing_project_path',
    usage: 'node init.js <project-path>'
  }));
  process.exit(1);
}

// ─────────────────────────────────────────────
// Git environment check & auto-install
// ─────────────────────────────────────────────

function findGit() {
  try {
    const v = execSync('git --version', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
    const m = v.trim().match(/git version\s+([\d.]+)/);
    return { found: true, version: m ? m[1] : 'unknown' };
  } catch {
    return { found: false, version: null };
  }
}

function tryInstall() {
  const platform = os.platform();
  const installers = [];

  if (platform === 'linux') {
    // Debian/Ubuntu
    if (fs.existsSync('/usr/bin/apt-get')) {
      installers.push({
        cmd: 'apt-get update -qq && apt-get install -y -qq git',
        name: 'apt-get'
      });
    }
    // Alpine
    if (fs.existsSync('/sbin/apk')) {
      installers.push({
        cmd: 'apk add --no-cache git',
        name: 'apk'
      });
    }
    // RHEL/CentOS/Fedora
    if (fs.existsSync('/usr/bin/yum')) {
      installers.push({
        cmd: 'yum install -y git',
        name: 'yum'
      });
    }
    if (fs.existsSync('/usr/bin/dnf')) {
      installers.push({
        cmd: 'dnf install -y git',
        name: 'dnf'
      });
    }
    // Arch
    if (fs.existsSync('/usr/bin/pacman')) {
      installers.push({
        cmd: 'pacman -S --noconfirm git',
        name: 'pacman'
      });
    }
    // Termux (Android)
    if (process.env.PREFIX === '/data/data/com.termux/files/usr' || fs.existsSync('/data/data/com.termux')) {
      installers.push({
        cmd: 'pkg install -y git',
        name: 'pkg'
      });
    }
  } else if (platform === 'darwin') {
    if (fs.existsSync('/usr/local/bin/brew') || fs.existsSync('/opt/homebrew/bin/brew')) {
      installers.push({
        cmd: 'brew install git',
        name: 'brew'
      });
    }
  }

  // Fallback: nix, if present
  if (fs.existsSync('/nix')) {
    installers.push({
      cmd: 'nix-env -iA nixpkgs.git',
      name: 'nix'
    });
  }

  const detail = {
    platform,
    arch: os.arch(),
    tried: installers.map(i => i.name),
    manual_install: getManualInstallHint(platform)
  };

  for (const installer of installers) {
    try {
      execSync(installer.cmd, {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe'],
        timeout: 120000,
        env: { ...process.env, DEBIAN_FRONTEND: 'noninteractive' }
      });
      // Verify
      const git = findGit();
      if (git.found) {
        return { success: true, method: installer.name, version: git.version };
      }
    } catch (err) {
      // Try next installer
    }
  }

  return { success: false, detail };
}

function getManualInstallHint(platform) {
  const hints = {
    linux: 'Install git: apt-get install git / apk add git / yum install git',
    darwin: 'Install git: brew install git, or install Xcode Command Line Tools: xcode-select --install',
    win32: 'Install git from https://git-scm.com/download/win',
  };
  return hints[platform] || `Install git for ${platform}: https://git-scm.com/downloads`;
}

// ─────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────

let gitInfo = findGit();

if (!gitInfo.found) {
  const installResult = tryInstall();

  if (installResult.success) {
    gitInfo = { found: true, version: installResult.version };
  } else {
    // Auto-install failed — report structured error for LLM
    const d = installResult.detail;
    console.log(JSON.stringify({
      action: 'init',
      status: 'error',
      error: 'git_not_found',
      project: path.resolve(projectPath),
      detail: {
        platform: d.platform,
        arch: d.arch,
        package_managers_found: d.tried,
        auto_install: 'all_failed',
        manual_install_hint: d.manual_install,
        llm_hint: 'Install git before running this skill. Try: sudo apt-get install git, or brew install git, or pkg install git (Termux). If in a container, ensure the base image includes git.'
      }
    }));
    process.exit(1);
  }
}

// Git is available — proceed with init
const { initProject } = require('../lib/git');
const absPath = path.resolve(projectPath);

try {
  const result = initProject(absPath);

  if (!result.success) {
    console.log(JSON.stringify({
      action: 'init',
      status: 'error',
      error: result.message,
      project: absPath,
      gitVersion: gitInfo.version
    }));
    process.exit(1);
  }

  console.log(JSON.stringify({
    action: 'init',
    status: 'success',
    initialized: result.initialized,
    project: absPath,
    storagePath: result.barePath,
    gitVersion: gitInfo.version,
    message: result.initialized ? 'Tracking initialized' : 'Already tracked'
  }));

} catch (err) {
  console.log(JSON.stringify({
    action: 'init',
    status: 'error',
    error: err.message,
    project: absPath,
    gitVersion: gitInfo.version
  }));
  process.exit(1);
}
