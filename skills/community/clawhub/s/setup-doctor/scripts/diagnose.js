#!/usr/bin/env node
/**
 * OpenClaw Environment Diagnostic Script (standalone, no shell execution)
 *
 * SECURITY NOTE: This script performs NO shell execution and NO network
 * requests. It uses only Node.js native APIs (fs, path, os, process) to
 * check local files and versions. No child_process is imported.
 *
 * For full diagnostics including gateway status and CLI version checks,
 * use the agent's built-in exec tool via the Setup Doctor skill instead.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

function findConfig() {
  const candidates = [
    path.join(os.homedir(), '.openclaw', 'openclaw.json'),
    path.join(os.homedir(), '.openclaw', 'openclaw.json5'),
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

const results = {
  timestamp: new Date().toISOString(),
  os: `${os.type()} ${os.release()} (${os.arch()})`,
  checks: []
};

// Node.js — native process API
const nodeVer = process.versions.node;
const nodeMajor = parseInt(nodeVer.split('.')[0], 10);
results.checks.push({
  name: 'Node.js',
  status: nodeMajor >= 20 ? 'pass' : 'fail',
  value: `v${nodeVer}`,
  fix: nodeMajor >= 20 ? null : 'Install Node.js 20+ from https://nodejs.org'
});

// npm — check if npm CLI exists (no file reading)
try {
  const npmCli = path.join(path.dirname(process.execPath), 'npm');
  if (process.platform === 'win32') {
    const npmCmd = npmCli + '.cmd';
    fs.accessSync(npmCmd, fs.constants.X_OK);
  } else {
    fs.accessSync(npmCli, fs.constants.X_OK);
  }
  results.checks.push({
    name: 'npm',
    status: 'pass',
    value: 'detected',
    fix: null
  });
} catch {
  results.checks.push({
    name: 'npm',
    status: 'warn',
    value: 'Not detected',
    fix: 'npm is bundled with Node.js — verify with: npm --version'
  });
}

// OpenClaw — check multiple possible install locations (no execution)
const npmPrefix = path.join(os.homedir(), 'AppData', 'Roaming', 'npm');
const openclawPaths = process.platform === 'win32'
  ? [
      path.join(npmPrefix, 'openclaw.cmd'),
      path.join(path.dirname(process.execPath), 'openclaw.cmd'),
    ]
  : [
      '/usr/local/bin/openclaw',
      path.join(os.homedir(), '.npm-global', 'bin', 'openclaw'),
    ];
const openclawPath = openclawPaths.find(p => fs.existsSync(p));
results.checks.push({
  name: 'OpenClaw',
  status: fs.existsSync(openclawPath) ? 'pass' : 'fail',
  value: fs.existsSync(openclawPath) ? `Found at ${openclawPath}` : 'Not found',
  fix: fs.existsSync(openclawPath) ? null : 'Run: npm install -g openclaw@latest'
});

// Gateway — check for PID file (no execution)
const gwPidFile = path.join(os.homedir(), '.openclaw', 'gateway.pid');
results.checks.push({
  name: 'Gateway',
  status: fs.existsSync(gwPidFile) ? 'pass' : 'warn',
  value: fs.existsSync(gwPidFile)
    ? `PID file found at ${gwPidFile}`
    : 'No PID file — gateway may be running via service manager. Use the agent to run: openclaw gateway status',
  fix: null
});

// Configuration — native fs API
const configPath = findConfig();
if (configPath) {
  try {
    fs.accessSync(configPath, fs.constants.R_OK);
    results.checks.push({
      name: 'Configuration',
      status: 'pass',
      value: `Found at ${configPath}`
    });
  } catch {
    results.checks.push({
      name: 'Configuration',
      status: 'fail',
      value: `Config file not accessible at ${configPath}`,
      fix: 'Fix JSON syntax in ~/.openclaw/openclaw.json'
    });
  }
} else {
  results.checks.push({
    name: 'Configuration',
    status: 'fail',
    value: 'No config file found',
    fix: 'Run: openclaw onboard'
  });
}

// Workspace — native fs API
const ws = path.join(os.homedir(), '.openclaw', 'workspace');
results.checks.push({
  name: 'Workspace',
  status: fs.existsSync(ws) ? 'pass' : 'warn',
  value: ws,
  fix: fs.existsSync(ws) ? null : 'Run: openclaw onboard'
});

// Summary
const passed = results.checks.filter(c => c.status === 'pass').length;
const failed = results.checks.filter(c => c.status === 'fail').length;
results.summary = { passed, failed, total: results.checks.length };

console.log(JSON.stringify(results, null, 2));
