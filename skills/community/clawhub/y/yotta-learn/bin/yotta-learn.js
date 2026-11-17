#!/usr/bin/env node
/**
 * yotta-learn 运行时入口（dispatcher）
 *
 * 用法:
 *   yotta-learn view [--port 8791] [--dir <KB>]   # 本地知识库管理台（图形界面）
 *   yotta-learn kb <子命令> …                      # 知识库操作（init/category/query/…）
 *   yotta-learn <学习命令> …                       # .learnings 闭环（log/list/review/…）
 *   yotta-learn install --agent <name>            # 安装技能（等价 yotta-learn-install）
 *   yotta-learn --version / --help
 *
 * 兼容: 无参数或首位为安装器旗标（--agent / --dir / -g / --list / --dry-run …）时
 *      按旧行为转发给 bin/install.js；其余命令转发给 Python 运行时
 *      （scripts/yotta_learn.py），解释器按 YOTTA_LEARN_PYTHON → py -3 → python → python3 探测。
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const BIN_DIR = __dirname;
const PKG_ROOT = path.join(BIN_DIR, '..');
const INSTALLER = path.join(BIN_DIR, 'install.js');
const RUNTIME = path.join(PKG_ROOT, 'scripts', 'yotta_learn.py');

// 旧版“直接旗标”安装用法（yotta-learn --agent …）保持原样转发安装器。
const INSTALL_FLAGS = new Set([
  '--agent', '--dir', '--global', '-g', '--list', '-l', '--dry-run', '--yes', '-y',
]);

function pkgVersion() {
  try {
    const raw = JSON.parse(fs.readFileSync(path.join(PKG_ROOT, 'package.json'), 'utf8'));
    return raw.version || 'unknown';
  } catch (err) {
    return 'unknown';
  }
}

function usage() {
  console.log('yotta-learn —— 元习（学习闭环 + 知识库）v' + pkgVersion());
  console.log('');
  console.log('运行时命令（需要 Python 3.8+）:');
  console.log('  yotta-learn view [--port <端口>] [--dir <KB>]   打开本地知识库管理台（图形界面，仅 127.0.0.1）');
  console.log('  yotta-learn kb <子命令> …                      知识库：init / category / add / list / show / query /');
  console.log('                                                review / index / backup / trash / stats / doctor');
  console.log('  yotta-learn <学习命令> …                       .learnings 闭环：init / log / list / review / update /');
  console.log('                                                resolve / promote / stats / extract');
  console.log('');
  console.log('安装（把技能装进智能体目录）:');
  console.log('  yotta-learn install --agent <name>            按智能体默认用户级目录安装');
  console.log('  yotta-learn install --dir <路径>              安装到指定目录');
  console.log('  yotta-learn install -g                        安装到全部已知智能体');
  console.log('  yotta-learn-install …                         等价安装器入口（无参数 = 检测到的项目级目录）');
  console.log('  旧用法兼容：yotta-learn --agent <name> / --dir <路径> / -g / --list / --dry-run');
  console.log('');
  console.log('其它:');
  console.log('  yotta-learn --version                         显示版本');
  console.log('  yotta-learn <命令> --help                     查看命令帮助（透传运行时）');
  console.log('  YOTTA_LEARN_PYTHON=<python 路径>              指定 Python 解释器（默认自动探测 py -3 / python / python3）');
  console.log('');
  console.log('技能目录直跑（与运行时命令等价）:');
  console.log('  python3 scripts/yotta_learn.py <命令> …');
  console.log('');
  console.log('快速上手:');
  console.log('  yotta-learn kb init && yotta-learn view');
}

function runInstaller(args) {
  const r = spawnSync(process.execPath, [INSTALLER].concat(args), { stdio: 'inherit' });
  if (r.error) {
    console.error('安装器启动失败: ' + r.error.message);
    process.exit(1);
  }
  process.exit(typeof r.status === 'number' ? r.status : 1);
}

function pythonCandidates() {
  const out = [];
  const fromEnv = String(process.env.YOTTA_LEARN_PYTHON || '').trim();
  if (fromEnv) out.push([fromEnv]);
  out.push(['py', '-3']);
  out.push(['python']);
  out.push(['python3']);
  return out;
}

/**
 * 候选解释器探测：先跑一次 `-c` 确认候选可用。
 * 隔离 HOME / 受限环境里 Windows `py` 启动器可能整体失效（如 exit 109），
 * 直接运行脚本会把启动器的退出码误当脚本结果；探测后可自动回退到下一个候选。
 */
function probePython(cmd) {
  const probe = spawnSync(cmd[0], cmd.slice(1).concat([
    '-c', 'import sys; sys.exit(0 if sys.version_info[0] >= 3 else 1)',
  ]), { encoding: 'utf8', timeout: 15000 });
  if (probe.error) {
    return { ok: false, reason: probe.error.code === 'ENOENT' ? '未找到' : probe.error.message };
  }
  if (probe.status !== 0) return { ok: false, reason: '退出码 ' + probe.status };
  return { ok: true };
}

function runRuntime(args) {
  const candidates = pythonCandidates();
  const failed = [];
  for (const cmd of candidates) {
    const probe = probePython(cmd);
    if (!probe.ok) {
      failed.push(cmd.join(' ') + '（' + probe.reason + '）');
      continue;
    }
    const r = spawnSync(cmd[0], cmd.slice(1).concat([RUNTIME]).concat(args), { stdio: 'inherit' });
    if (r.error) {
      console.error('运行时启动失败: ' + r.error.message);
      process.exit(1);
    }
    process.exit(typeof r.status === 'number' ? r.status : 1);
  }
  console.error('未找到可用的 Python 3（已尝试 ' + failed.join(' / ') + '）。');
  console.error('请安装 Python 3.8+，或设置 YOTTA_LEARN_PYTHON 指向 python 可执行文件。');
  process.exit(3);
}

function main() {
  const args = process.argv.slice(2);
  if (!args.length) return runInstaller(args); // 兼容：无参数 = 项目级安装（旧行为）
  const first = args[0];
  if (first === 'install') return runInstaller(args.slice(1));
  if (first === '--version' || first === '-v') {
    console.log('yotta-learn v' + pkgVersion());
    return;
  }
  if (first === '--help' || first === '-h') {
    usage();
    return;
  }
  if (INSTALL_FLAGS.has(first)) return runInstaller(args);
  return runRuntime(args);
}

main();
