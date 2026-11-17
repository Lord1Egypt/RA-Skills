'use strict';
/**
 * 用户级自定义宿主注册表（0.29.0 F2）—— <root>/hosts.json。
 *
 * root = YOTTA_SKILLS_HOME 或 ~/.yottaskills（与 self.json 同根，独立于 Hub 目录）。
 * schema v1：{ version, hosts:[{ dir, label, agentId, scope:"verified", note,
 * addedAt, source:"manual", manualState? }] }
 *
 * 注册只影响发现 / 分发 / 收编范围：不创建目录、不改宿主配置；
 * 移除注册绝不删除目录。
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const hubLib = require('./hub');
const agentDirsLib = require('./agent-dirs');

const HOSTS_REGISTRY_VERSION = 1;
const LABEL_MAX_LENGTH = 48;
const MANUAL_STATES = ['available', 'orphan', 'ignored'];

function nowIso() {
  return new Date().toISOString();
}

function resolveSkillsRoot(opts) {
  const options = opts || {};
  const env = options.env || process.env;
  const explicit = options.skillsRoot || env.YOTTA_SKILLS_HOME;
  if (explicit) return path.resolve(explicit);
  return path.join(options.homeDir || os.homedir(), '.yottaskills');
}

function hostsRegistryPath(opts) {
  return path.join(resolveSkillsRoot(opts), 'hosts.json');
}

function readHostsRegistry(opts) {
  try {
    const value = JSON.parse(fs.readFileSync(hostsRegistryPath(opts), 'utf8'));
    if (value && typeof value === 'object' && Array.isArray(value.hosts)) {
      return {
        version: HOSTS_REGISTRY_VERSION,
        hosts: value.hosts.filter((item) => item && typeof item.dir === 'string' && item.dir),
        // 0.29.1 U2：不接管名单 + 目录覆盖（可选字段，向后兼容旧文件）。
        excluded: Array.isArray(value.excluded)
          ? value.excluded.filter((item) => item && typeof item.value === 'string' && item.value &&
              (item.kind === 'agent' || item.kind === 'dir'))
          : [],
        overrides: Array.isArray(value.overrides)
          ? value.overrides.filter((item) => item && typeof item.agentId === 'string' && item.agentId &&
              typeof item.dir === 'string' && item.dir)
          : [],
      };
    }
  } catch (_) { /* missing or corrupt registry falls back to empty */ }
  return { version: HOSTS_REGISTRY_VERSION, hosts: [], excluded: [], overrides: [] };
}

function writeHostsRegistry(opts, registry) {
  const file = hostsRegistryPath(opts);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = file + '.tmp-' + process.pid;
  fs.writeFileSync(tmp, JSON.stringify({
    version: HOSTS_REGISTRY_VERSION,
    hosts: registry.hosts,
    excluded: registry.excluded || [],
    overrides: registry.overrides || [],
  }, null, 2) + '\n', 'utf8');
  fs.renameSync(tmp, file);
  return file;
}

function safeRealpath(target) {
  try {
    return fs.realpathSync.native(target);
  } catch (_) {
    try {
      return fs.realpathSync(target);
    } catch (_) {
      return path.resolve(target);
    }
  }
}

function samePath(left, right) {
  const a = safeRealpath(left);
  const b = safeRealpath(right);
  if (process.platform === 'win32') return a.toLowerCase() === b.toLowerCase();
  return a === b;
}

function isInside(root, target) {
  const relative = path.relative(path.resolve(root), path.resolve(target));
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

/** YottaCode 目标判定：.yottacode 路径或 YOTTACODE_HOME 子树（0.29.1 U2）。 */
function isYottaCodeTarget(dir, opts) {
  if (agentDirsLib.isYottaCodeDir(dir)) return true;
  const env = (opts && opts.env) || process.env;
  const ycHome = env.YOTTACODE_HOME ? path.resolve(env.YOTTACODE_HOME) : null;
  return Boolean(ycHome && dir && isInside(ycHome, dir));
}

/** fail-closed 校验：返回中文错误或 null。 */
function validateHostDir(dir, opts) {
  const target = path.resolve(dir);
  let stat;
  try {
    stat = fs.statSync(target);
  } catch (_) {
    return '目录不存在：' + target;
  }
  if (!stat.isDirectory()) return '不是目录：' + target;
  const hubDir = hubLib.resolveHubDir(opts);
  if (samePath(target, hubDir) || isInside(hubDir, target)) {
    return '指向 Hub 自身或子目录，不允许注册：' + target;
  }
  if (agentDirsLib.isBridgeOnlyDir(target, opts)) {
    return '锁 / 数据桥接目录不允许注册：' + target;
  }
  if (isYottaCodeTarget(target, opts)) {
    return 'YottaCode 自带三层技能管理（skill-inventory / skill / user-skills），不纳入元阁接管：' + target;
  }
  return null;
}

function validateLabel(label) {
  const value = String(label || '').trim();
  if (!value) return 'label 不能为空';
  if (/[\u0000-\u001f\u007f]/.test(value)) return 'label 含控制字符';
  if (value.length > LABEL_MAX_LENGTH) return 'label 过长（最多 ' + LABEL_MAX_LENGTH + ' 字符）';
  return null;
}

/** 注册自定义宿主目录（fail-closed；不创建目录、不改宿主配置）。 */
function addHost(opts, input) {
  const options = opts || {};
  const dir = input && input.dir ? path.resolve(input.dir) : null;
  if (!dir) return { ok: false, error: '缺少目录：hub hosts add <dir>' };
  const guard = validateHostDir(dir, options);
  if (guard) return { ok: false, error: guard };
  const label = String((input && input.label) || path.basename(dir)).trim();
  const labelError = validateLabel(label);
  if (labelError) return { ok: false, error: labelError };
  const agentId = input && input.agentId ? String(input.agentId).trim().toLowerCase() : null;

  const registry = readHostsRegistry(options);
  const existing = registry.hosts.find((item) => samePath(item.dir, dir));
  if (existing) {
    return { ok: false, error: '该目录已注册：' + dir, existing };
  }
  const entry = {
    dir,
    label,
    agentId,
    scope: 'verified',
    note: (input && input.note) || null,
    addedAt: nowIso(),
    source: 'manual',
  };
  registry.hosts.push(entry);
  writeHostsRegistry(options, registry);
  return { ok: true, entry, registry };
}

/** 移除注册（只移除登记，绝不删除目录）。 */
function removeHost(opts, target) {
  const options = opts || {};
  const registry = readHostsRegistry(options);
  const index = registry.hosts.findIndex((item) =>
    (target && target.dir && samePath(item.dir, target.dir)) ||
    (target && target.id && String(item.agentId || '').toLowerCase() === String(target.id).toLowerCase()));
  if (index < 0) return { ok: false, error: '未找到注册项' };
  const removed = registry.hosts.splice(index, 1)[0];
  writeHostsRegistry(options, registry);
  return { ok: true, removed, registry };
}

/** 手动标记宿主状态（可用 / 残留 / 忽略）；条目不存在时先注册。 */
function markHost(opts, input) {
  const options = opts || {};
  const state = input && input.state ? String(input.state).toLowerCase() : null;
  if (!MANUAL_STATES.includes(state)) {
    return { ok: false, error: '未知手动状态：' + state + '（可用 available / 残留 orphan / 隐藏标记 ignored）' };
  }
  const dir = input && input.dir ? path.resolve(input.dir) : null;
  if (!dir) return { ok: false, error: '缺少目录' };
  if (isYottaCodeTarget(dir, options)) {
    return { ok: false, error: 'YottaCode 自带三层技能管理，不纳入元阁接管，不能标记：' + dir };
  }
  const registry = readHostsRegistry(options);
  let entry = registry.hosts.find((item) => samePath(item.dir, dir));
  if (!entry) {
    const added = addHost(options, { dir, label: input.label });
    if (!added.ok) return added;
    const refreshed = readHostsRegistry(options);
    entry = refreshed.hosts.find((item) => samePath(item.dir, dir));
    entry.manualState = state;
    writeHostsRegistry(options, refreshed);
    return { ok: true, entry, registry: refreshed };
  }
  entry.manualState = state;
  writeHostsRegistry(options, registry);
  return { ok: true, entry, registry };
}

/** 一步改名：只改显示名 label，不动目录 / 手动状态 / 覆盖（0.30.0 UX-08）。 */
function renameHost(opts, input) {
  const options = opts || {};
  const label = String((input && input.label) || '').trim();
  const labelError = validateLabel(label);
  if (labelError) return { ok: false, error: labelError };
  const dir = input && input.dir ? path.resolve(input.dir) : null;
  const id = input && input.id ? String(input.id).trim().toLowerCase() : null;
  if (!dir && !id) return { ok: false, error: '缺少目标：hub hosts rename <目录> --label <名称> 或 --id <agentId>' };
  const registry = readHostsRegistry(options);
  const entry = registry.hosts.find((item) =>
    (dir && samePath(item.dir, dir)) ||
    (id && String(item.agentId || '').toLowerCase() === id));
  if (!entry) {
    return {
      ok: false,
      error: '未找到注册项' + (dir ? '：' + dir : '：' + id),
      hint: '本命令只改自定义注册表（hub hosts list）里的显示名；未注册目录先 hub hosts add <目录> --label <名称>，内置映射改名用 hub hosts set <agentId> --label <名称>。',
    };
  }
  const previous = entry.label;
  entry.label = label;
  entry.updatedAt = nowIso();
  writeHostsRegistry(options, registry);
  return { ok: true, entry, previous, registry };
}

/** 0.29.1 U2：不接管名单匹配（agentId 或目录）；返回命中条目或 null。 */
function excludedEntryFor(registry, input) {
  const agentId = input && input.agentId ? String(input.agentId).toLowerCase() : null;
  const dir = input && input.dir ? path.resolve(input.dir) : null;
  for (const item of (registry && registry.excluded) || []) {
    if (!item) continue;
    if (item.kind === 'agent' && agentId && String(item.value).toLowerCase() === agentId) return item;
    if (item.kind === 'dir' && dir && samePath(item.value, dir)) return item;
  }
  return null;
}

/** 目标归类：已收录 agentId -> agent；否则按目录。 */
function classifyExcludeTarget(target) {
  const value = String(target || '').trim();
  const agentId = value.toLowerCase();
  if (agentDirsLib.AGENT_DIRS[agentId]) return { kind: 'agent', value: agentId };
  return { kind: 'dir', value: path.resolve(value) };
}

/**
 * 加入「不接管」名单（0.29.1 U2）：发现 / 显示 / 链接三层全部跳过，
 * `--include-discovered` 也不纳入；幂等。
 */
function excludeHost(opts, input) {
  const options = opts || {};
  const target = input && input.target ? String(input.target).trim() : '';
  if (!target) return { ok: false, error: '缺少目标：hub hosts exclude <agentId|目录>' };
  const { kind, value } = classifyExcludeTarget(target);
  if (kind === 'dir') {
    if (isYottaCodeTarget(value, options)) {
      return { ok: false, error: 'YottaCode 自带三层技能管理，不纳入元阁接管，无需加入不接管名单：' + value };
    }
    if (agentDirsLib.isBridgeOnlyDir(value, options)) {
      return { ok: false, error: '锁 / 数据桥接目录本就不参与链接，无需加入不接管名单：' + value };
    }
  }
  const registry = readHostsRegistry(options);
  const existing = excludedEntryFor(registry, { agentId: kind === 'agent' ? value : null, dir: kind === 'dir' ? value : null });
  if (existing) return { ok: true, entry: existing, registry, already: true };
  const label = input && input.label
    ? String(input.label).trim()
    : kind === 'agent'
      ? ((agentDirsLib.AGENT_DIRS[value] || {}).label || value)
      : path.basename(value);
  const entry = { kind, value, label, addedAt: nowIso() };
  registry.excluded = (registry.excluded || []).concat([entry]);
  writeHostsRegistry(options, registry);
  return { ok: true, entry, registry };
}

/** 移出「不接管」名单（恢复接管）。 */
function includeHost(opts, input) {
  const options = opts || {};
  const target = input && input.target ? String(input.target).trim() : '';
  if (!target) return { ok: false, error: '缺少目标：hub hosts include <agentId|目录>' };
  const { kind, value } = classifyExcludeTarget(target);
  const registry = readHostsRegistry(options);
  const index = (registry.excluded || []).findIndex((item) => item.kind === kind &&
    (kind === 'agent' ? String(item.value).toLowerCase() === value : samePath(item.value, value)));
  if (index < 0) return { ok: false, error: '未在不接管名单：' + target };
  const removed = registry.excluded.splice(index, 1)[0];
  writeHostsRegistry(options, registry);
  return { ok: true, removed, registry };
}

/**
 * 目录覆盖（0.29.1 U2）：用户级覆盖已收录 agentId 的内置映射目录；
 * 被覆盖的旧目录不再进入默认发现 / 链接。
 */
function setHostOverride(opts, input) {
  const options = opts || {};
  const agentId = input && input.agentId ? String(input.agentId).trim().toLowerCase() : '';
  if (!agentId) return { ok: false, error: '缺少 agentId：hub hosts set <agentId> --dir <目录>（恢复默认用 --clear）' };
  const info = agentDirsLib.AGENT_DIRS[agentId];
  if (!info) return { ok: false, error: '未收录智能体: ' + agentId };
  if (info.neverLink) return { ok: false, error: 'YottaCode 不纳入元阁接管，不能设置目录覆盖。' };
  const dir = input && input.dir ? path.resolve(input.dir) : null;
  if (!dir) return { ok: false, error: '缺少目录：hub hosts set <agentId> --dir <目录>（恢复默认用 --clear）' };
  const guard = validateHostDir(dir, options);
  if (guard) return { ok: false, error: guard };
  const label = input && input.label ? String(input.label).trim() : info.label;
  const labelError = validateLabel(label);
  if (labelError) return { ok: false, error: labelError };
  const registry = readHostsRegistry(options);
  const entry = {
    agentId,
    dir,
    label,
    previousDirs: (info.dirs || []).map((rel) => agentDirsLib.resolveUserDir(rel, options)),
    addedAt: nowIso(),
  };
  const index = (registry.overrides || []).findIndex((item) => String(item.agentId).toLowerCase() === agentId);
  if (index >= 0) registry.overrides[index] = entry;
  else registry.overrides = (registry.overrides || []).concat([entry]);
  writeHostsRegistry(options, registry);
  return { ok: true, entry, registry };
}

/** 清除目录覆盖（恢复内置映射）。 */
function clearHostOverride(opts, input) {
  const options = opts || {};
  const agentId = input && input.agentId ? String(input.agentId).trim().toLowerCase() : '';
  if (!agentId) return { ok: false, error: '缺少 agentId：hub hosts set <agentId> --clear' };
  const registry = readHostsRegistry(options);
  const index = (registry.overrides || []).findIndex((item) => String(item.agentId).toLowerCase() === agentId);
  if (index < 0) return { ok: false, error: '未找到目录覆盖：' + agentId };
  const removed = registry.overrides.splice(index, 1)[0];
  writeHostsRegistry(options, registry);
  return { ok: true, removed, registry };
}

module.exports = {
  HOSTS_REGISTRY_VERSION,
  MANUAL_STATES,
  LABEL_MAX_LENGTH,
  resolveSkillsRoot,
  hostsRegistryPath,
  readHostsRegistry,
  writeHostsRegistry,
  validateHostDir,
  validateLabel,
  addHost,
  removeHost,
  markHost,
  renameHost,
  excludedEntryFor,
  excludeHost,
  includeHost,
  setHostOverride,
  clearHostOverride,
};
