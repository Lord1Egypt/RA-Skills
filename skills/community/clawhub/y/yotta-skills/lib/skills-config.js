'use strict';
/**
 * 用户级配置（0.29.2 U4；0.29.5 扩展 lastMigration / lastSwitch）—— <root>/config.json。
 *
 * root = YOTTA_SKILLS_HOME 或 ~/.yottaskills（与 hosts.json / self.json 同根，
 * 独立于 Hub 目录本身）。schema v1（向后兼容增量）：
 *   { version, hub: "<path>" | null, lastMigration?: {...}, lastSwitch?: {...} }
 *
 * - lastMigration：最近一次成功切换位置的真实迁移（含回滚；from→to + 校验技能数 +
 *   重链目录数 + 回收站路径），供 `hub config get` / 面板「最近一次迁移 + 一键回滚」。
 * - lastSwitch：仅切换指针（未迁移）时记录的原位置，供面板提示
 *   「旧 Hub 还有 N 个技能未迁移」。
 *
 * Hub 解析优先级：--hub flag > YOTTA_SKILLS_HUB env > config.hub > 默认 <root>/hub。
 * set 为 fail-closed 校验：不能是文件、不能与配置根 / 独立安装目录重叠、
 * 不能是锁 / 数据桥接目录；路径不存在时允许（首次使用时创建）。
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const agentDirsLib = require('./agent-dirs');

const CONFIG_VERSION = 1;

function resolveSkillsRoot(opts) {
  const options = opts || {};
  const env = options.env || process.env;
  const explicit = options.skillsRoot || env.YOTTA_SKILLS_HOME;
  if (explicit) return path.resolve(explicit);
  return path.join(options.homeDir || os.homedir(), '.yottaskills');
}

function configPath(opts) {
  return path.join(resolveSkillsRoot(opts), 'config.json');
}

function defaultHubDir(opts) {
  return path.join(resolveSkillsRoot(opts), 'hub');
}

function readConfig(opts) {
  try {
    const value = JSON.parse(fs.readFileSync(configPath(opts), 'utf8'));
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      return {
        version: CONFIG_VERSION,
        hub: typeof value.hub === 'string' && value.hub.trim() ? value.hub : null,
        lastMigration: sanitizeMigration(value.lastMigration),
        lastSwitch: sanitizeSwitch(value.lastSwitch),
      };
    }
  } catch (_) { /* missing or corrupt config falls back to empty */ }
  return { version: CONFIG_VERSION, hub: null, lastMigration: null, lastSwitch: null };
}

function cleanString(value) {
  return typeof value === 'string' && value.trim() ? value : null;
}

function cleanCount(value) {
  const num = Number(value);
  return Number.isFinite(num) && num >= 0 ? num : 0;
}

/** 规范化 lastMigration（非法条目按缺失处理，绝不抛错）。 */
function sanitizeMigration(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return null;
  const from = cleanString(value.from);
  const to = cleanString(value.to);
  if (!from || !to) return null;
  return {
    kind: value.kind === 'rollback' ? 'rollback' : 'migrate',
    from,
    to,
    at: cleanString(value.at),
    verifiedSkills: cleanCount(value.verifiedSkills),
    relinkDirs: cleanCount(value.relinkDirs),
    incomplete: cleanCount(value.incomplete),
    trashedTo: cleanString(value.trashedTo),
    trashError: cleanString(value.trashError),
    oldHubKept: cleanString(value.oldHubKept),
    via: cleanString(value.via),
  };
}

/** 规范化 lastSwitch（仅切换指针的记录）。 */
function sanitizeSwitch(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return null;
  const from = cleanString(value.from);
  const to = cleanString(value.to);
  if (!from || !to) return null;
  return {
    from,
    to,
    at: cleanString(value.at),
    skills: cleanCount(value.skills),
    via: cleanString(value.via),
  };
}

function writeConfig(opts, config) {
  const file = configPath(opts);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = file + '.tmp-' + process.pid;
  const payload = {
    version: CONFIG_VERSION,
    hub: config && config.hub ? config.hub : null,
  };
  const migration = sanitizeMigration(config && config.lastMigration);
  const switched = sanitizeSwitch(config && config.lastSwitch);
  if (migration) payload.lastMigration = migration;
  if (switched) payload.lastSwitch = switched;
  fs.writeFileSync(tmp, JSON.stringify(payload, null, 2) + '\n', 'utf8');
  fs.renameSync(tmp, file);
  return file;
}

/** 解析生效 Hub：返回 { dir, source, configured, configFile, defaultDir }。 */
function resolveHub(opts) {
  const options = opts || {};
  const env = options.env || process.env;
  const config = readConfig(options);
  const base = {
    configured: config.hub,
    configFile: configPath(options),
    defaultDir: defaultHubDir(options),
  };
  if (options.hub) return { dir: path.resolve(options.hub), source: 'flag', ...base };
  if (env.YOTTA_SKILLS_HUB) return { dir: path.resolve(env.YOTTA_SKILLS_HUB), source: 'env', ...base };
  if (config.hub) return { dir: path.resolve(config.hub), source: 'config', ...base };
  return { dir: base.defaultDir, source: 'default', ...base };
}

function sourceLabel(source) {
  if (source === 'flag') return '--hub 参数';
  if (source === 'env') return 'YOTTA_SKILLS_HUB 环境变量';
  if (source === 'config') return 'config.json 配置';
  return '默认位置';
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

/** fail-closed 校验 Hub 路径；返回 { ok:true, dir } 或 { ok:false, error }。 */
function validateHubPath(input, opts) {
  const options = opts || {};
  const raw = String(input == null ? '' : input).trim();
  if (!raw) return { ok: false, error: '缺少路径：hub config set --hub <path>' };
  const dir = path.resolve(raw);
  let stat = null;
  try {
    stat = fs.statSync(dir);
  } catch (_) { /* 不存在允许：首次使用时创建 */ }
  if (stat && !stat.isDirectory()) return { ok: false, error: '不是目录：' + dir };
  const root = resolveSkillsRoot(options);
  if (isInside(dir, root)) {
    return {
      ok: false,
      error: 'Hub 不能与配置根相同或包含配置根（' + root + '）：config.json / hosts.json / self.json 需保持独立',
    };
  }
  const selfDir = path.join(root, 'yotta-skills');
  if (samePath(dir, selfDir) || isInside(selfDir, dir) || isInside(dir, selfDir)) {
    return { ok: false, error: 'Hub 不能与独立安装目录重叠（' + selfDir + '）' };
  }
  if (agentDirsLib.isBridgeOnlyDir(dir, options)) {
    return { ok: false, error: '锁 / 数据桥接目录不能作为 Hub：' + dir };
  }
  return { ok: true, dir };
}

/** 写入持久 Hub 覆盖；返回 { ok, hub, configFile, previous }。 */
function setHub(opts, input) {
  const options = opts || {};
  const guard = validateHubPath(input && input.hub, options);
  if (!guard.ok) return guard;
  const config = readConfig(options);
  const previous = config.hub;
  config.hub = guard.dir;
  const file = writeConfig(options, config);
  return { ok: true, hub: guard.dir, configFile: file, previous };
}

/** 清除持久 Hub 覆盖（恢复 flag > env > 默认）。 */
function clearHub(opts) {
  const options = opts || {};
  const config = readConfig(options);
  if (!config.hub) return { ok: false, error: '没有可清除的 Hub 配置覆盖（当前来源不是 config.json）' };
  const removed = config.hub;
  config.hub = null;
  const file = writeConfig(options, config);
  return { ok: true, removed, configFile: file };
}

/**
 * 记录最近一次迁移（真实移动；kind=migrate / rollback）。
 * 迁移完成即清除 lastSwitch（原位置内容已处理，不再提示）。
 */
function recordLastMigration(opts, migration) {
  const options = opts || {};
  const config = readConfig(options);
  config.lastMigration = sanitizeMigration(migration);
  config.lastSwitch = null;
  const file = writeConfig(options, config);
  return { ok: true, lastMigration: readConfig(options).lastMigration, configFile: file };
}

/** 记录「仅切换位置」（未迁移）：原位置留给面板提示「未迁移」。 */
function recordLastSwitch(opts, info) {
  const options = opts || {};
  const config = readConfig(options);
  config.lastSwitch = sanitizeSwitch(info);
  const file = writeConfig(options, config);
  return { ok: true, lastSwitch: readConfig(options).lastSwitch, configFile: file };
}

/** 清除「未迁移」提示（原位置已空 / 已迁移 / 用户处理）。 */
function clearLastSwitch(opts) {
  const options = opts || {};
  const config = readConfig(options);
  if (!config.lastSwitch) return { ok: false, cleared: null };
  const cleared = config.lastSwitch;
  config.lastSwitch = null;
  const file = writeConfig(options, config);
  return { ok: true, cleared, configFile: file };
}

module.exports = {
  CONFIG_VERSION,
  resolveSkillsRoot,
  configPath,
  defaultHubDir,
  readConfig,
  writeConfig,
  resolveHub,
  sourceLabel,
  validateHubPath,
  setHub,
  clearHub,
  recordLastMigration,
  recordLastSwitch,
  clearLastSwitch,
};
