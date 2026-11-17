#!/usr/bin/env node
/**
 * yotta-dev-mcp launcher.
 *
 * Default: start the stdio MCP server.
 * Install flags: delegate to bin/install.js.
 */
'use strict';
const { spawn, spawnSync } = require('child_process');
const path = require('path');

const PKG_ROOT = path.join(__dirname, '..');
const SERVER = path.join(PKG_ROOT, 'scripts', 'yotta_dev_mcp.py');
const INSTALL_FLAGS = ['--agent', '--dir', '--list', '-l', '-g', '--global', '--dry-run', '--yes'];

function isInstallRequest(args) {
  return args.some(function (item) {
    if (INSTALL_FLAGS.indexOf(item) !== -1) return true;
    return item.indexOf('--agent=') === 0 || item.indexOf('--dir=') === 0;
  });
}

function findPython() {
  const candidates = [];
  if (process.env.YOTTA_MCP_PYTHON) candidates.push(process.env.YOTTA_MCP_PYTHON);
  candidates.push('python3', 'python', 'py');
  for (let i = 0; i < candidates.length; i++) {
    try {
      const result = spawnSync(candidates[i], ['--version'], { encoding: 'utf8', timeout: 5000 });
      if (result.status === 0) return candidates[i];
    } catch (error) {
      // Try the next candidate.
    }
  }
  return 'python';
}

function main() {
  const args = process.argv.slice(2);
  if (args.indexOf('--version') !== -1 || args.indexOf('-v') !== -1) {
    process.stdout.write(require(path.join(PKG_ROOT, 'package.json')).version + '\n');
    return;
  }
  if (isInstallRequest(args)) {
    require(path.join(__dirname, 'install.js'));
    return;
  }
  const python = findPython();
  const child = spawn(python, [SERVER].concat(args), { stdio: 'inherit' });
  child.on('exit', function (code) { process.exit(code || 0); });
  child.on('error', function (error) {
    process.stderr.write('yotta-dev-mcp: cannot start Python MCP server: ' + error.message + '\n');
    process.exit(1);
  });
}

main();
