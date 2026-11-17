#!/usr/bin/env node
/**
 * yotta-dev-mcp 跨平台安装器（YottaSkills）
 *
 * 用法:
 *   npx -y --package @yottameta/yotta-dev-mcp yotta-dev-mcp-install --agent <name>   # 按智能体默认用户级目录安装（推荐）
 *   npx -y --package @yottameta/yotta-dev-mcp yotta-dev-mcp-install --dir <path>     # 装到指定目录（用户改了目录的智能体）
 *   npx -y --package @yottameta/yotta-dev-mcp yotta-dev-mcp-install -g               # 安装到全部已知智能体用户级目录
 *   npx -y --package @yottameta/yotta-dev-mcp yotta-dev-mcp-install                  # 安装到检测到的项目级目录
 *   npx -y --package @yottameta/yotta-dev-mcp yotta-dev-mcp-install --list           # 列出智能体 -> 默认目录
 *   npx -y --package @yottameta/yotta-dev-mcp yotta-dev-mcp-install --dry-run        # 只显示将写入的目标，不写文件
 *   npx -y --package @yottameta/yotta-dev-mcp yotta-dev-mcp-install --version        # 显示版本
 *   npx -y --package @yottameta/yotta-dev-mcp yotta-dev-mcp-install --help           # 显示帮助
 *
 * 退出码: 0 成功 / 1 安装失败 / 2 用法错误 / 4 目标错误
 */
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILL_NAME = 'yotta-dev-mcp';
const PKG_ROOT = path.join(__dirname, '..');

// 顶层开发文件 / 目录：只在安装包顶层跳过；技能包内嵌套同名载荷必须保留。
// 与 install.sh 同口径：开发件与运行时不相关目录一律不落目标。
const TOP_SKIP = [
  'package.json', 'package-lock.json', 'bin', 'lib', 'test',
  '.github', '.git', '.gitignore', '.npmignore', '.gitattributes',
  '.yotta', '.tmp', 'install.sh', 'node_modules',
];
const TOP_SKIP_SET = new Set(TOP_SKIP);
// 缓存 / 编译产物：任意层级跳过，安装时同样清理。
const CACHE_DIRS = new Set(['__pycache__', '.pytest_cache', '.mypy_cache']);

class UsageError extends Error {}
class TargetError extends Error {}
class InstallError extends Error {}

// 智能体 -> 用户级默认技能目录（dirs 按优先级排列；--agent 装到第一个）
// 依据官方文档：.agents/skills 并非通用目录，被 OpenCode / Cursor / Cline / Amp /
// Kimi / Gemini CLI / GitHub Copilot 等读取；Claude Code 与 Codex 默认不读 .agents。
const AGENT_DIRS = {
  claude:    { label: 'Claude Code',      dirs: ['.claude/skills'] },
  cursor:    { label: 'Cursor',           dirs: ['.cursor/skills', '.agents/skills'] },
  codex:     { label: 'Codex',            dirs: ['.codex/skills'] }, // 特判：$CODEX_HOME/skills
  gemini:    { label: 'Gemini CLI',       dirs: ['.gemini/skills', '.agents/skills'] },
  goose:     { label: 'Goose',            dirs: ['.config/goose/skills', '.agents/skills'] },
  amp:       { label: 'Amp',              dirs: ['.config/agents/skills', '.agents/skills'] },
  opencode:  { label: 'OpenCode',         dirs: ['.config/opencode/skills'] }, // 特判：$XDG_CONFIG_HOME
  windsurf:  { label: 'Windsurf',         dirs: ['.codeium/windsurf/skills'] },
  workbuddy: { label: 'WorkBuddy',        dirs: ['.workbuddy/skills'] },
  kiro:      { label: 'Kiro',             dirs: ['.kiro/skills'] },
  trae:      { label: 'Trae Code CLI',    dirs: ['.traecli/skills'] },
  'trae-cn': { label: 'Trae IDE（国内）',  dirs: ['.trae-cn/skills'] },
  qwen:      { label: 'Qwen Code',        dirs: ['.qwen/skills'] },
  comate:    { label: 'Comate 文心快码',   dirs: ['.comate/skills'] },
  codebuddy: { label: 'CodeBuddy Code',   dirs: ['.codebuddy/skills'] },
  kimi:      { label: 'Kimi Code CLI',    dirs: ['.kimi/skills'] },
  agents:    { label: '通用 AGENTS.md',    dirs: ['.agents/skills'] },
};

const PROJECT_DIRS = [
  '.claude/skills',
  '.cursor/skills',
  '.codex/skills',
  '.config/goose/skills',
  '.config/agents/skills',
  '.opencode/skills',
  '.codeium/windsurf/skills',
  '.workbuddy/skills',
  '.kiro/skills',
  '.traecli/skills',
  '.gemini/skills',
  '.trae-cn/skills',
  '.qwen/skills',
  '.comate/skills',
  '.codebuddy/skills',
  '.kimi/skills',
  '.agents/skills',
];

// Codex 用户级目录特判：优先 $CODEX_HOME/skills，否则 ~/.codex/skills
function codexUserDir() {
  const base = process.env.CODEX_HOME || path.join(os.homedir(), '.codex');
  return path.join(base, 'skills');
}

// OpenCode 用户级目录特判：优先 $XDG_CONFIG_HOME/opencode/skills，否则 ~/.config/opencode/skills
function opencodeUserDir() {
  const base = process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config');
  return path.join(base, 'opencode', 'skills');
}

function resolveUserDir(rel) {
  if (rel === '.codex/skills') return codexUserDir();
  if (rel === '.config/opencode/skills') return opencodeUserDir();
  return path.join(os.homedir(), rel);
}

function displayDir(rel) {
  if (process.platform === 'win32') return '%USERPROFILE%\\' + rel.replace(/\//g, '\\');
  return '~/' + rel;
}

function skillVersion() {
  try {
    const data = JSON.parse(fs.readFileSync(path.join(PKG_ROOT, 'package.json'), 'utf8'));
    return data.version || null;
  } catch (_) {
    try {
      const version = fs.readFileSync(path.join(PKG_ROOT, 'VERSION'), 'utf8').trim();
      return version || null;
    } catch (_) {
      return null;
    }
  }
}

function usage() {
  console.log(SKILL_NAME + ' 安装器（YottaSkills）');
  console.log('');
  console.log('用法:');
  console.log('  node bin/install.js --agent <name>   按智能体默认用户级目录安装（推荐）');
  console.log('  node bin/install.js --dir <path>     装到指定目录（用户改了目录的智能体）');
  console.log('  node bin/install.js -g               安装到全部已知智能体用户级目录');
  console.log('  node bin/install.js                  安装到检测到的项目级目录');
  console.log('');
  console.log('参数:');
  console.log('  --agent <name>  智能体键名，见 --list');
  console.log('  --dir <path>    自定义技能目录');
  console.log('  -g, --global    安装到全部已知用户级目录');
  console.log('  --list, -l      列出支持的智能体目录');
  console.log('  --dry-run       只显示将写入的目标，不写文件');
  console.log('  --version, -v   显示版本');
  console.log('  --help, -h      显示帮助');
  console.log('  --yes, -y       兼容参数（-g 不再强制要求）');
  console.log('');
  console.log('退出码: 0 成功 / 1 安装失败 / 2 用法错误 / 4 目标错误');
}

function parseArgs(argv) {
  const opts = { help: false, version: false, list: false, global: false, dryRun: false, yes: false, dir: null, agent: null };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') opts.help = true;
    else if (arg === '--version' || arg === '-v') opts.version = true;
    else if (arg === '--list' || arg === '-l') opts.list = true;
    else if (arg === '--global' || arg === '-g') opts.global = true;
    else if (arg === '--dry-run') opts.dryRun = true;
    else if (arg === '--yes' || arg === '-y') opts.yes = true;
    else if (arg === '--dir') {
      const value = argv[++i];
      if (!value) throw new UsageError('--dir 需要一个非空路径');
      opts.dir = value;
    } else if (arg === '--agent') {
      const value = argv[++i];
      if (!value) throw new UsageError('--agent 需要一个非空名称');
      opts.agent = String(value).toLowerCase();
    } else {
      throw new UsageError('未知参数: ' + arg);
    }
  }
  if (!opts.help && !opts.version) {
    const selected = [opts.dir, opts.agent, opts.global].filter(Boolean).length;
    if (selected > 1) throw new UsageError('--dir / --agent / -g 只能选一个');
  }
  return opts;
}

function printList() {
  console.log('智能体 -> 默认技能目录（--agent <name> 装到第一个，用户级）:');
  for (const [key, value] of Object.entries(AGENT_DIRS)) {
    const resolved = value.dirs.map(displayDir);
    console.log('  ' + key.padEnd(10) + value.label.padEnd(18) + resolved.join('、'));
  }
  console.log('\n说明：Windows 用 %USERPROFILE%，Linux/macOS 用 ~；仅收录有官方默认目录的智能体。');
  console.log('改了目录的请用 --dir <路径>，不要依赖默认位置；若设置了 CODEX_HOME / XDG_CONFIG_HOME，安装自动以该变量为准。');
}

function assertSafeTarget(target) {
  const rel = path.relative(PKG_ROOT, target);
  if (rel === '' || (!rel.startsWith('..') && !path.isAbsolute(rel))) {
    throw new UsageError('目标目录不能在技能源目录内（防止自装自毁）');
  }
  if (isDirectLink(target) && !isManagedHubTarget(target)) {
    throw new TargetError('目标目录是符号链接或 junction，拒绝跟随: ' + target);
  }
}

function isDirectLink(target) {
  let stat = null;
  try { stat = fs.lstatSync(target); } catch (_) { return false; }
  if (stat.isSymbolicLink()) return true;
  try {
    const real = fs.realpathSync(target);
    const parentReal = fs.realpathSync(path.dirname(target));
    const norm = (value) => process.platform === 'win32'
      ? path.resolve(value).toLowerCase()
      : path.resolve(value);
    return norm(real) !== norm(path.join(parentReal, path.basename(target)));
  } catch (_) {
    return false;
  }
}

function isManagedHubTarget(target) {
  if (!isDirectLink(target)) return false;
  try {
    const real = fs.realpathSync(target);
    if (path.basename(real) !== SKILL_NAME) return false;
    const parent = path.dirname(real);
    return fs.existsSync(path.join(parent, '.yotta-hub.json'))
      || fs.existsSync(path.join(parent, '.yotta-links.json'));
  } catch (_) {
    return false;
  }
}

function removeLink(target) {
  try {
    fs.unlinkSync(target);
  } catch (_) {
    fs.rmdirSync(target);
  }
}

function safeRemove(target) {
  let stat = null;
  try { stat = fs.lstatSync(target); } catch (_) { return; }
  if (isDirectLink(target)) {
    removeLink(target);
    return;
  }
  if (stat.isDirectory()) {
    for (const name of fs.readdirSync(target)) {
      safeRemove(path.join(target, name));
    }
    fs.rmdirSync(target);
  } else {
    fs.unlinkSync(target);
  }
}

function shouldSkipCache(name, isFile) {
  if (CACHE_DIRS.has(name)) return true;
  if (isFile && (name.endsWith('.pyc') || name.endsWith('.pyo'))) return true;
  return false;
}

function copyDir(src, dst, topLevel) {
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    // 只跳过安装包顶层开发文件；template/ 等嵌套同名载荷必须保留。
    if (topLevel && TOP_SKIP_SET.has(entry.name)) continue;
    if (shouldSkipCache(entry.name, entry.isFile())) continue;
    const s = path.join(src, entry.name);
    const d = path.join(dst, entry.name);
    if (entry.isDirectory()) {
      if (isDirectLink(d)) {
        throw new TargetError('目标目录包含符号链接或 junction，拒绝写入: ' + d);
      }
      fs.mkdirSync(d, { recursive: true });
      if (isDirectLink(d)) {
        throw new TargetError('目标目录包含符号链接或 junction，拒绝写入: ' + d);
      }
      copyDir(s, d, false);
    } else if (entry.isFile()) {
      if (isDirectLink(d)) {
        throw new TargetError('目标文件是符号链接，拒绝写入: ' + d);
      }
      fs.copyFileSync(s, d);
    }
  }
}

// 清理旧版安装残留（fail-closed 白名单）：
// 仅在目标目录已存在且含 SKILL.md 时触发；只删顶层开发项 + 任意层级缓存；
// 不整目录删除、不跟随符号链接。
function cleanResidue(target) {
  const removed = [];
  const workTarget = isManagedHubTarget(target) ? fs.realpathSync(target) : target;
  let stat = null;
  try { stat = fs.lstatSync(workTarget); } catch (_) { return removed; }
  if (!stat.isDirectory()) return removed;
  if (isDirectLink(workTarget)) return removed;
  if (!fs.existsSync(path.join(workTarget, 'SKILL.md'))) return removed;
  for (const name of TOP_SKIP) {
    const p = path.join(workTarget, name);
    let entry = null;
    try { entry = fs.lstatSync(p); } catch (_) { continue; }
    if (entry.isSymbolicLink() || isDirectLink(p)) continue;
    safeRemove(p);
    removed.push(name);
  }
  const walk = (dir) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, entry.name);
      if (entry.isSymbolicLink() || isDirectLink(p)) continue;
      if (entry.isDirectory()) {
        if (CACHE_DIRS.has(entry.name)) {
          safeRemove(p);
          removed.push(path.relative(target, p));
        } else {
          walk(p);
        }
      } else if (entry.isFile() && (entry.name.endsWith('.pyc') || entry.name.endsWith('.pyo'))) {
        fs.unlinkSync(p);
        removed.push(path.relative(target, p));
      }
    }
  };
  walk(workTarget);
  return removed;
}

function installTo(dest, opts) {
  if (!dest || typeof dest !== 'string') throw new UsageError('目标目录不能为空');
  const target = path.resolve(dest, SKILL_NAME);
  assertSafeTarget(target);
  if (opts.dryRun) {
    console.log('[dry-run] 将安装到 -> ' + target);
    return target;
  }
  try {
    for (const rel of cleanResidue(target)) console.log('已清理残留: ' + rel);
    fs.mkdirSync(target, { recursive: true });
    if (isDirectLink(target) && !isManagedHubTarget(target)) {
      throw new TargetError('目标目录在安装期间变成了链接，拒绝写入: ' + target);
    }
    copyDir(PKG_ROOT, target, true);
    if (!fs.existsSync(path.join(target, 'SKILL.md'))) {
      throw new InstallError('安装结果缺少 SKILL.md');
    }
  } catch (err) {
    if (err instanceof UsageError || err instanceof TargetError || err instanceof InstallError) throw err;
    throw new InstallError('安装到 ' + target + ' 失败: ' + err.message);
  }
  console.log('installed -> ' + target);
  return target;
}

function run() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) { usage(); return; }
  if (opts.version) {
    const version = skillVersion();
    if (!version) {
      console.error(SKILL_NAME + ' 版本未知（未找到 package.json）');
      process.exitCode = 1;
      return;
    }
    console.log(SKILL_NAME + ' v' + version);
    return;
  }
  if (opts.list) { printList(); return; }

  if (opts.dir) { installTo(opts.dir, opts); return; }

  if (opts.agent) {
    const info = AGENT_DIRS[opts.agent];
    if (!info) {
      throw new UsageError('未收录智能体: ' + opts.agent + '。可用: ' + Object.keys(AGENT_DIRS).join(', ') + '；自定义目录请用 --dir <路径>。');
    }
    installTo(resolveUserDir(info.dirs[0]), opts);
    console.log('完成。');
    return;
  }

  if (opts.global) {
    const seen = new Set();
    for (const value of Object.values(AGENT_DIRS)) {
      for (const rel of value.dirs) {
        if (seen.has(rel)) continue;
        seen.add(rel);
        installTo(resolveUserDir(rel), opts);
      }
    }
    if (!opts.dryRun) console.log('完成。');
    return;
  }

  const dirs = PROJECT_DIRS.filter((d) => fs.existsSync(d));
  if (!dirs.length) {
    throw new TargetError('未检测到项目级智能体目录。可用 --agent <name> 装到用户级，或用 --dir <路径> 指定目录。');
  }
  for (const dir of dirs) installTo(dir, opts);
  if (!opts.dryRun) console.log('完成。');
}

function main() {
  try {
    run();
  } catch (err) {
    if (err instanceof UsageError) {
      console.error('用法错误: ' + err.message);
      usage();
      process.exitCode = 2;
    } else if (err instanceof TargetError) {
      console.error('目标错误: ' + err.message);
      process.exitCode = 4;
    } else if (err instanceof InstallError) {
      console.error('安装失败: ' + err.message);
      console.error('修复建议: 检查目录权限与磁盘空间后重试，或用 --dir 换一个目录。');
      process.exitCode = 1;
    } else {
      console.error('未知错误: ' + (err && err.message ? err.message : String(err)));
      process.exitCode = 1;
    }
  }
}

main();
