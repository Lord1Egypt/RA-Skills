'use strict';
/**
 * lib/deps.js —— 依赖缺口的统一人话提示（元阁 0.24.0，方案 B）。
 *
 * 约定：按需触发、不常驻；每条提示回答四件事：
 *   需要什么 / 为什么 / 怎么办（一条可复制修复）/ 不影响使用。
 * 依赖矩阵：Node 18+ 必需；npm 与系统 tar 是回退通道（内置拉包 / 内置解包为主）；
 * 元信装前扫描需要 Python 3.8+，优先指向宿主自带 Python（--python / YOTTA_SKILLS_PYTHON）。
 */

const NEED = {
  node: { label: 'Node 18+', need: '>=18', why: '运行元阁 CLI 本体' },
  npm: { label: 'npm', need: '随 Node 安装', why: '拉包回退通道（内置拉包失败时的备用）' },
  python: { label: 'Python 3.8+', need: '>=3.8', why: '元信装前安全扫描' },
  tar: { label: 'tar', need: '可用即可', why: '解包回退通道（内置解包失败时的备用）' },
};

function fixFor(dep, platform) {
  const p = platform || process.platform;
  if (dep === 'node' || dep === 'npm') {
    if (p === 'win32') return 'winget install OpenJS.NodeJS.LTS';
    if (p === 'darwin') return 'brew install node';
    return 'sudo apt install nodejs npm（或到 https://nodejs.org/ 下载 LTS）';
  }
  if (dep === 'python') {
    if (p === 'win32') {
      return '优先用 --python <路径> 或 YOTTA_SKILLS_PYTHON 指向宿主自带 Python；否则 winget install Python.Python.3.12';
    }
    if (p === 'darwin') {
      return '优先用 --python <路径> 或 YOTTA_SKILLS_PYTHON 指向宿主自带 Python；否则 brew install python';
    }
    return '优先用 --python <路径> 或 YOTTA_SKILLS_PYTHON 指向宿主自带 Python；否则 sudo apt install python3';
  }
  if (dep === 'tar') {
    if (p === 'win32') return 'Windows 10+ 自带 tar（缺失时可 winget install bsdtar）';
    if (p === 'darwin') return 'macOS 自带 tar；或 brew install gnu-tar';
    return 'sudo apt install tar';
  }
  return '';
}

/**
 * 统一三行模板：
 *   需要 <依赖>（用途：<为什么>）—— 装好后重跑：<原命令>
 *   修复：<一条可复制命令>
 *   或者：继续用宿主自带技能，不影响正常使用。<补充>
 */
function describe(dep, options) {
  const meta = NEED[dep] || { label: dep, need: '', why: '' };
  const opts = options || {};
  const command = opts.command || 'yotta-skills <原命令>';
  const status = opts.missing
    ? '—— 未找到 ' + meta.label + '；装好后重跑：' + command
    : '—— 装好后重跑：' + command;
  const extra = opts.extra ? ' ' + opts.extra : '';
  return [
    '需要 ' + meta.label + '（用途：' + meta.why + '）' + status,
    '修复：' + (opts.fix || fixFor(dep)),
    '或者：继续用宿主自带技能，不影响正常使用。' + extra,
  ].join('\n');
}

function semverAtLeast(version, minimum) {
  const got = String(version || '').match(/(\d+)\.(\d+)(?:\.(\d+))?/);
  const need = String(minimum || '').match(/(\d+)\.(\d+)(?:\.(\d+))?/);
  if (!got || !need) return null;
  for (let i = 1; i <= 3; i += 1) {
    const a = Number(got[i] || 0);
    const b = Number(need[i] || 0);
    if (a > b) return true;
    if (a < b) return false;
  }
  return true;
}

/** Node 版本自检；version 可注入用于测试。 */
function nodeCheck(version) {
  const current = version || process.versions.node;
  return {
    name: 'node',
    found: true,
    version: current,
    ok: semverAtLeast(current, '18.0.0') === true,
    need: NEED.node.need,
    why: NEED.node.why,
  };
}

/** npm 缺失错误识别（spawn ENOENT / 命令不存在的中英文提示）。 */
function isNpmMissing(raw) {
  const text = String(raw || '');
  return /ENOENT|EINVAL|npm\.cmd'? ?(无法|不能被)|不是内部或外部命令|not recognized|系统找不到指定/i.test(text);
}

function versionLine(proc) {
  if (!proc) return null;
  const text = String((proc.stdout || '') + (proc.stderr || '')).trim();
  if (!text) return null;
  return text.split(/\r?\n/).map((s) => s.trim()).filter(Boolean)[0].slice(0, 80) || null;
}

/**
 * doctor 依赖自检块（只告警不失败）。
 * detected: { node:{version,ok}, npm:{found,version}, python:{found,version,path}, tar:{found,version} }
 */
function dependencyReport(detected) {
  const d = detected || {};
  const items = [];

  const node = d.node || {};
  const nodeVersion = node.version || process.versions.node;
  const nodeOk = node.ok !== undefined ? !!node.ok : semverAtLeast(nodeVersion, '18.0.0') === true;
  items.push({
    name: 'node',
    found: true,
    version: 'v' + String(nodeVersion),
    ok: nodeOk,
    need: NEED.node.need,
    why: NEED.node.why,
    optional: false,
    fix: nodeOk ? null : fixFor('node'),
  });

  const npm = d.npm || {};
  items.push({
    name: 'npm',
    found: !!npm.found,
    version: npm.version || null,
    ok: !!npm.found,
    need: NEED.npm.need,
    why: NEED.npm.why,
    optional: true,
    fix: npm.found ? null : fixFor('npm'),
  });

  const py = d.python || {};
  const pyVersionOk = py.found ? semverAtLeast(py.version || '', '3.8.0') : false;
  items.push({
    name: 'python',
    found: !!py.found,
    version: py.version || null,
    ok: pyVersionOk === true,
    need: NEED.python.need,
    why: NEED.python.why,
    optional: false,
    fix: pyVersionOk === true ? null : fixFor('python'),
  });

  const tar = d.tar || {};
  items.push({
    name: 'tar',
    found: !!tar.found,
    version: tar.version || null,
    ok: !!tar.found,
    need: NEED.tar.need,
    why: NEED.tar.why,
    optional: true,
    fix: tar.found ? null : fixFor('tar'),
  });

  return items;
}

module.exports = {
  NEED,
  fixFor,
  describe,
  nodeCheck,
  isNpmMissing,
  versionLine,
  dependencyReport,
  semverAtLeast,
};
