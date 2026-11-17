'use strict';
/**
 * 元阁独立安装（install-self）与位置查看（where）—— 0.29.0 F1。
 *
 * 独立安装 = 把管理引擎完整运行件（bin / lib / assets / package.json / skills.json / scan-policy.json）
 * 装到用户级独立位置（默认 ~/.yottaskills/yotta-skills；YOTTA_SKILLS_HOME 可覆盖根），
 * 写 <root>/self.json 登记。与 Hub 真源、宿主技能池完全独立：不写宿主配置、
 * 不写 mcp.json、不建全局 shim。
 *
 * fail-closed：目标与 Hub 真源重叠 / 锁与数据桥接目录 / 非空陌生目录（--force 才覆盖
 * 同名运行件，无关文件保留）。
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const hubLib = require('./hub');
const agentDirsLib = require('./agent-dirs');

const SELF_REGISTRY_VERSION = 1;
const RUNTIME_PAYLOAD = ['bin', 'lib', 'assets', 'package.json', 'skills.json', 'scan-policy.json'];
const PACKAGE_NAME = '@yottameta/yotta-skills';

function nowIso() {
  return new Date().toISOString();
}

function resolveSelfRoot(opts) {
  const options = opts || {};
  const env = options.env || process.env;
  const explicit = options.selfRoot || env.YOTTA_SKILLS_HOME;
  if (explicit) return path.resolve(explicit);
  return path.join(options.homeDir || os.homedir(), '.yottaskills');
}

function selfRegistryPath(opts) {
  return path.join(resolveSelfRoot(opts), 'self.json');
}

function defaultSelfDir(opts) {
  return path.join(resolveSelfRoot(opts), 'yotta-skills');
}

function readSelfRegistry(opts) {
  try {
    const value = JSON.parse(fs.readFileSync(selfRegistryPath(opts), 'utf8'));
    if (value && typeof value === 'object' && Array.isArray(value.installs)) {
      return {
        version: SELF_REGISTRY_VERSION,
        installs: value.installs.filter((item) => item && typeof item.dir === 'string' && item.dir),
      };
    }
  } catch (_) { /* missing or corrupt registry falls back to empty */ }
  return { version: SELF_REGISTRY_VERSION, installs: [] };
}

function writeSelfRegistry(opts, registry) {
  const file = selfRegistryPath(opts);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = file + '.tmp-' + process.pid;
  fs.writeFileSync(tmp, JSON.stringify({
    version: SELF_REGISTRY_VERSION,
    installs: registry.installs,
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

function packageRoot() {
  return path.join(__dirname, '..');
}

function readPackageVersion(dir) {
  try {
    return JSON.parse(fs.readFileSync(path.join(dir, 'package.json'), 'utf8')).version || null;
  } catch (_) {
    return null;
  }
}

function hasContent(dir) {
  try {
    return fs.readdirSync(dir).length > 0;
  } catch (_) {
    return false;
  }
}

/** 目标是否已是元阁运行件目录（允许正常覆盖升级）。 */
function hasOwnMarker(dir) {
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(dir, 'package.json'), 'utf8'));
    if (pkg && pkg.name === PACKAGE_NAME) return true;
  } catch (_) { /* no readable package.json */ }
  return fs.existsSync(path.join(dir, 'bin', 'yotta-skills.js'));
}

function guardTarget(dir, opts) {
  const hubDir = hubLib.resolveHubDir(opts);
  if (samePath(dir, hubDir) || isInside(hubDir, dir) || isInside(dir, hubDir)) {
    return '目标与 Hub 真源重叠（' + hubDir + '）：独立安装与 Hub 必须分离';
  }
  if (agentDirsLib.isBridgeOnlyDir(dir, opts)) {
    return '目标是锁 / 数据桥接目录（XDG_STATE_HOME/skills 或 XDG_DATA_HOME/skills），不允许独立安装';
  }
  return null;
}

function copyEntry(from, to) {
  fs.rmSync(to, { recursive: true, force: true });
  if (fs.statSync(from).isDirectory()) {
    fs.mkdirSync(to, { recursive: true });
    fs.cpSync(from, to, { recursive: true });
  } else {
    fs.mkdirSync(path.dirname(to), { recursive: true });
    fs.copyFileSync(from, to);
  }
}

function installSelf(opts) {
  const options = opts || {};
  const src = packageRoot();
  const dir = path.resolve(options.dir || defaultSelfDir(options));
  const dryRun = Boolean(options.dryRun);
  const force = Boolean(options.force);
  const version = readPackageVersion(src);
  const registryFile = selfRegistryPath(options);

  const guard = guardTarget(dir, options);
  if (guard) return { ok: false, error: guard, exitCode: 2 };

  const exists = fs.existsSync(dir);
  const stranger = exists && hasContent(dir) && !hasOwnMarker(dir);
  if (stranger && !force) {
    return {
      ok: false,
      error: '目标是非空陌生目录：' + dir + '（默认拒绝覆盖）',
      hint: '确认目录用途后加 --force 覆盖同名运行件（无关文件保留）；或改用 --dir 指定空目录。',
      exitCode: 2,
    };
  }

  const payload = {
    action: 'install-self',
    dryRun,
    dir,
    version,
    files: RUNTIME_PAYLOAD.slice(),
    registry: registryFile,
    overwrite: exists,
    forced: Boolean(stranger && force),
    exitCode: 0,
  };
  if (dryRun) return { ok: true, ...payload };

  for (const name of RUNTIME_PAYLOAD) {
    copyEntry(path.join(src, name), path.join(dir, name));
  }

  const registry = readSelfRegistry(options);
  const entry = { dir, version, installedAt: nowIso(), source: src };
  const index = registry.installs.findIndex((item) => samePath(item.dir, dir));
  if (index >= 0) registry.installs[index] = entry;
  else registry.installs.push(entry);
  writeSelfRegistry(options, registry);

  return { ok: true, ...payload, installs: registry.installs };
}

function whereInfo(opts) {
  const options = opts || {};
  const running = safeRealpath(process.argv[1] || '');
  const registry = readSelfRegistry(options);
  const hubResolved = hubLib.resolveHub(options);
  return {
    action: 'where',
    running,
    version: readPackageVersion(packageRoot()),
    defaultDir: defaultSelfDir(options),
    hubDir: hubResolved.dir,
    hubSource: hubResolved.source,
    hubConfigured: hubResolved.configured,
    hubConfigFile: hubResolved.configFile,
    registry: selfRegistryPath(options),
    installs: registry.installs.map((item) => ({
      dir: item.dir,
      version: item.version || null,
      installedAt: item.installedAt || null,
      source: item.source || null,
      current: running ? isInside(item.dir, running) : false,
    })),
  };
}

module.exports = {
  SELF_REGISTRY_VERSION,
  RUNTIME_PAYLOAD,
  resolveSelfRoot,
  selfRegistryPath,
  defaultSelfDir,
  readSelfRegistry,
  writeSelfRegistry,
  installSelf,
  whereInfo,
};
