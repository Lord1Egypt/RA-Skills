#!/usr/bin/env node
/**
 * yotta-verify-mcp —— 元信 MCP server 启动器（YottaSkills）
 *
 * 用法（二选一）：
 *   作为 MCP server（默认，stdio JSON-RPC）：
 *     npx -y @yottameta/yotta-verify-mcp
 *     或在 MCP 客户端配置 command=npx args=["-y","@yottameta/yotta-verify-mcp"]
 *   作为技能安装器（委托给 install.js）：
 *     npx -y @yottameta/yotta-verify-mcp --agent <name>
 *     npx -y @yottameta/yotta-verify-mcp --dir <path>
 *     npx -y @yottameta/yotta-verify-mcp -g
 *     npx -y @yottameta/yotta-verify-mcp --list
 *
 * 说明：本启动器负责定位可用的 Python（3.8+）并拉起 stdio MCP server；
 * 检测到安装参数时委托给 install.js，保持与其它 YottaSkills 技能一致的一键安装体验。
 */
'use strict';
const { spawn, spawnSync } = require('child_process');
const path = require('path');

const PKG_ROOT = path.join(__dirname, '..');
const SERVER = path.join(PKG_ROOT, 'scripts', 'yotta_verify_mcp.py');

// 安装器识别参数（含前导短横线前缀，覆盖 --agent=X 等价写法）
const INSTALL_FLAG_TOKENS = ['--agent', '--dir', '--list', '-l', '-g', '--global'];

function isInstallRequest(args) {
  return args.some(function (a) {
    if (INSTALL_FLAG_TOKENS.indexOf(a) !== -1) return true;
    return a.indexOf('--agent=') === 0 || a.indexOf('--dir=') === 0;
  });
}

function findPython() {
  const candidates = [];
  if (process.env.YOTTA_MCP_PYTHON) candidates.push(process.env.YOTTA_MCP_PYTHON);
  candidates.push('python3', 'python', 'py');
  for (let i = 0; i < candidates.length; i++) {
    try {
      const r = spawnSync(candidates[i], ['--version'], { encoding: 'utf8', timeout: 5000 });
      if (r.status === 0) return candidates[i];
    } catch (e) { /* 尝试下一个 */ }
  }
  return 'python';
}

function main() {
  const args = process.argv.slice(2);

  if (args.indexOf('--version') !== -1 || args.indexOf('-v') !== -1) {
    const pkg = require(path.join(PKG_ROOT, 'package.json'));
    process.stdout.write(pkg.version + '\n');
    return;
  }

  if (isInstallRequest(args)) {
    // 委托给安装器（install.js 读取自身 process.argv，检测到安装参数即执行）
    require(path.join(__dirname, 'install.js'));
    return;
  }

  const py = findPython();
  const child = spawn(py, [SERVER].concat(args), { stdio: 'inherit' });
  child.on('exit', function (code, signal) { process.exit(code || 0); });
  child.on('error', function (err) {
    process.stderr.write('yotta-verify-mcp: 无法启动 Python MCP server: ' + err.message + '\n');
    process.exit(1);
  });
}

main();
