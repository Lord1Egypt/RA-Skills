'use strict';

/**
 * YottaSkills Hub core (standard: yotta-skills-hub/v1).
 *
 * The hub is a local canonical skill store. Host directories receive links
 * (Windows junction / POSIX symlink) to the hub entries. This module is
 * deliberately filesystem-only and zero-dependency.
 */

const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const scanLib = require('./skills-scan');
const skillsCliLock = require('./skills-cli-lock');
const skillsConfigLib = require('./skills-config');

const STANDARD_ID = 'yotta-skills-hub/v1';
const STATE_VERSION = 1;
const STATE_FILE = '.yotta-hub.json';
const LINKS_FILE = '.yotta-links.json';
const AUDIT_FILE = '.yotta-hub-audit.jsonl';
const SKILL_FILE = 'SKILL.md';
const TRASH_RETENTION_DAYS = 7;

/**
 * Hub 家族范围 = 全家清单（skills.json，27）+ 特殊家族（5）。
 * 特殊家族不进一次性安装清单；仅参与 Hub 安装 / 更新 / 收敛 / 体检，
 * 版本跟随各自 npm latest（由安装管线在运行时解析）。
 */
const HUB_FAMILY_EXTRAS = [
  { slug: 'yotta-dev-mcp', name: '元开', pkg: '@yottameta/yotta-dev-mcp', version: 'latest' },
  { slug: 'yotta-partner', name: '元伴', pkg: '@yottameta/yotta-partner', version: 'latest' },
  { slug: 'yotta-present', name: '元呈', pkg: '@yottameta/yotta-present', version: 'latest' },
  { slug: 'yotta-skills', name: '元阁', pkg: '@yottameta/yotta-skills', version: 'latest', runtimePayload: ['bin'] },
  { slug: 'yotta-verify-mcp', name: '元信MCP', pkg: '@yottameta/yotta-verify-mcp', version: 'latest' },
];

const HASH_SKIP = new Set([
  '.git', 'node_modules', '__pycache__', '.pytest_cache', '.mypy_cache',
  '.yottaskills-staging', '.yottaskills-backup',
]);

function nowIso() {
  return new Date().toISOString();
}

/** 解析生效 Hub（含来源）：--hub > YOTTA_SKILLS_HUB > config.json > 默认。 */
function resolveHub(opts) {
  return skillsConfigLib.resolveHub(opts);
}

function resolveHubDir(opts) {
  return resolveHub(opts).dir;
}

function hubPaths(hubDir) {
  const root = path.resolve(hubDir);
  return {
    root,
    state: path.join(root, STATE_FILE),
    links: path.join(root, LINKS_FILE),
    audit: path.join(root, AUDIT_FILE),
  };
}

function readJson(file, fallback) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (_) {
    return fallback;
  }
}

function writeJsonAtomic(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = file + '.tmp-' + process.pid;
  fs.writeFileSync(tmp, JSON.stringify(value, null, 2) + '\n', 'utf8');
  fs.renameSync(tmp, file);
}

function readHubState(hubDir) {
  const fallback = {
    standard: STANDARD_ID,
    version: STATE_VERSION,
    updatedAt: null,
    skills: {},
  };
  const value = readJson(hubPaths(hubDir).state, fallback);
  if (!value || typeof value !== 'object') return fallback;
  if (!value.skills || typeof value.skills !== 'object') value.skills = {};
  value.standard = value.standard || STANDARD_ID;
  value.version = value.version || STATE_VERSION;
  return value;
}

function writeHubState(hubDir, state) {
  const next = {
    standard: STANDARD_ID,
    version: STATE_VERSION,
    updatedAt: nowIso(),
    skills: (state && state.skills) || {},
  };
  writeJsonAtomic(hubPaths(hubDir).state, next);
  return next;
}

function readLinkState(hubDir) {
  const fallback = {
    standard: STANDARD_ID,
    version: STATE_VERSION,
    updatedAt: null,
    links: [],
  };
  const value = readJson(hubPaths(hubDir).links, fallback);
  if (!value || typeof value !== 'object') return fallback;
  if (!Array.isArray(value.links)) value.links = [];
  value.standard = value.standard || STANDARD_ID;
  value.version = value.version || STATE_VERSION;
  return value;
}

function writeLinkState(hubDir, state) {
  const next = {
    standard: STANDARD_ID,
    version: STATE_VERSION,
    updatedAt: nowIso(),
    links: Array.isArray(state && state.links) ? state.links : [],
  };
  writeJsonAtomic(hubPaths(hubDir).links, next);
  return next;
}

function appendAudit(hubDir, entry) {
  const file = hubPaths(hubDir).audit;
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, JSON.stringify({ at: nowIso(), ...entry }) + '\n', 'utf8');
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

function pathKey(dir) {
  const real = safeRealpath(dir);
  return process.platform === 'win32' ? real.toLowerCase() : real;
}

function isInside(root, target) {
  const base = safeRealpath(root);
  const candidate = safeRealpath(target);
  const relative = path.relative(base, candidate);
  if (relative === '') return true;
  return !relative.startsWith('..') && !path.isAbsolute(relative);
}

function hashTree(dir) {
  const hash = crypto.createHash('sha256');
  const walk = (current, relative) => {
    const entries = fs.readdirSync(current, { withFileTypes: true })
      .sort((a, b) => a.name.localeCompare(b.name));
    for (const entry of entries) {
      if (HASH_SKIP.has(entry.name)) continue;
      if (entry.name.startsWith('.yottaskills-')) continue;
      if (/\.py[co]$/.test(entry.name)) continue;
      const full = path.join(current, entry.name);
      const rel = relative ? path.join(relative, entry.name) : entry.name;
      if (entry.isSymbolicLink()) {
        hash.update('L\0' + rel + '\0' + fs.readlinkSync(full) + '\0');
      } else if (entry.isDirectory()) {
        hash.update('D\0' + rel + '\0');
        walk(full, rel);
      } else if (entry.isFile()) {
        hash.update('F\0' + rel + '\0');
        hash.update(fs.readFileSync(full));
        hash.update('\0');
      }
    }
  };
  walk(path.resolve(dir), '');
  return hash.digest('hex');
}

/** 统计目录树中的普通文件数与总字节数（不跟随链接；跨卷复制校验用）。 */
function treeStats(dir) {
  let files = 0;
  let bytes = 0;
  const walk = (current) => {
    for (const name of fs.readdirSync(current)) {
      const full = path.join(current, name);
      const stat = fs.lstatSync(full);
      if (stat.isSymbolicLink()) continue;
      if (stat.isDirectory()) walk(full);
      else if (stat.isFile()) {
        files += 1;
        bytes += stat.size;
      }
    }
  };
  walk(path.resolve(dir));
  return { files, bytes };
}

/** 重建链接条目：目录优先用 junction（Windows）/ dir（POSIX），文件用 file。 */
function copyLinkEntry(src, dest) {
  const target = fs.readlinkSync(src);
  let kinds;
  if (process.platform === 'win32') {
    let isDir = null;
    try {
      isDir = fs.statSync(src).isDirectory();
    } catch (_) {
      isDir = null;
    }
    kinds = isDir === false ? ['file', 'junction'] : ['junction', 'file'];
  } else {
    let isDir = false;
    try {
      isDir = fs.statSync(src).isDirectory();
    } catch (_) {
      isDir = false;
    }
    kinds = [isDir ? 'dir' : 'file'];
  }
  let lastError = null;
  for (const kind of kinds) {
    try {
      fs.symlinkSync(target, dest, kind);
      return;
    } catch (error) {
      lastError = error;
    }
  }
  throw lastError || new Error('无法重建链接：' + src);
}

/** 逐条目复制目录树（保真：含链接、空目录与全部普通文件）。 */
function copyEntryFaithful(src, dest) {
  const stat = fs.lstatSync(src);
  if (stat.isSymbolicLink()) {
    copyLinkEntry(src, dest);
    return;
  }
  if (stat.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const name of fs.readdirSync(src)) {
      const child = path.join(src, name);
      const childStat = fs.lstatSync(child);
      if (childStat.isSymbolicLink()) copyLinkEntry(child, path.join(dest, name));
      else if (childStat.isDirectory()) copyEntryFaithful(child, path.join(dest, name));
      else if (childStat.isFile()) fs.copyFileSync(child, path.join(dest, name));
      else throw new Error('不支持的条目类型：' + child);
    }
    return;
  }
  if (stat.isFile()) {
    fs.copyFileSync(src, dest);
    return;
  }
  throw new Error('不支持的条目类型：' + src);
}

/** 删除条目：链接只删链接本身，不触碰目标。 */
function removeEntryFaithful(entryPath) {
  const stat = fs.lstatSync(entryPath);
  if (stat.isSymbolicLink()) {
    removeDirLink(entryPath);
    return;
  }
  fs.rmSync(entryPath, { recursive: true, force: true });
}

/** 校验复制结果：链接比对目标，目录比对 treeHash + 文件数 + 字节数。 */
function verifyEntryCopy(src, dest) {
  const srcStat = fs.lstatSync(src);
  const destStat = fs.lstatSync(dest);
  if (srcStat.isSymbolicLink() !== destStat.isSymbolicLink()) {
    return { ok: false, reason: '条目类型不一致' };
  }
  if (srcStat.isSymbolicLink()) {
    if (fs.readlinkSync(src) !== fs.readlinkSync(dest)) {
      return { ok: false, reason: '链接目标不一致' };
    }
    return { ok: true };
  }
  if (hashTree(src) !== hashTree(dest)) {
    return { ok: false, reason: 'treeHash 不一致' };
  }
  const from = treeStats(src);
  const to = treeStats(dest);
  if (from.files !== to.files || from.bytes !== to.bytes) {
    return {
      ok: false,
      reason: '文件数 / 字节数不一致（源 ' + from.files + ' 个 / ' + from.bytes + ' 字节；副本 ' +
        to.files + ' 个 / ' + to.bytes + ' 字节）',
    };
  }
  return { ok: true };
}

/**
 * 跨卷安全移动：优先 rename；EXDEV（跨盘）时回退「复制 → 校验 → 删除源」。
 * 任一步失败都不静默丢数据：源完整则回滚副本；源已不完整则保留完整副本并报出路径。
 */
function moveEntryAcrossDevices(src, dest, options) {
  const opts = options || {};
  const renameEntry = typeof opts.renameEntry === 'function' ? opts.renameEntry : fs.renameSync;
  try {
    renameEntry(src, dest);
    return { method: 'rename' };
  } catch (error) {
    if (!error || error.code !== 'EXDEV') throw error;
  }
  copyEntryFaithful(src, dest);
  let check;
  try {
    check = verifyEntryCopy(src, dest);
  } catch (error) {
    check = { ok: false, reason: error.message };
  }
  if (!check.ok) {
    try { removeEntryFaithful(dest); } catch (_) { /* 保留现场供排查 */ }
    throw new Error('跨卷复制校验失败（' + check.reason + '）；源目录未动，副本已清理');
  }
  try {
    removeEntryFaithful(src);
  } catch (error) {
    let intact = false;
    try { intact = verifyEntryCopy(dest, src).ok; } catch (_) { intact = false; }
    if (intact) {
      try { removeEntryFaithful(dest); } catch (_) { /* 保留现场供排查 */ }
      throw new Error('跨卷复制完成但源删除失败：' + error.message + '；源目录完整，副本已回滚');
    }
    throw new Error('跨卷复制完成但源删除失败：' + error.message + '；完整副本保留在 ' + dest);
  }
  return { method: 'copy' };
}

function scanHubSkills(hubDir) {
  const root = path.resolve(hubDir);
  const result = [];
  let entries;
  try {
    entries = fs.readdirSync(root, { withFileTypes: true });
  } catch (_) {
    return result;
  }
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    if (entry.name.includes('.yottaskills-backup-') || entry.name.includes('.yottaskills-import-')) continue;
    if (!entry.isDirectory() && !entry.isSymbolicLink()) continue;
    const dir = path.join(root, entry.name);
    let stat;
    try {
      stat = fs.statSync(dir);
    } catch (_) {
      continue;
    }
    if (!stat.isDirectory()) continue;
    let text;
    try {
      text = fs.readFileSync(path.join(dir, SKILL_FILE), 'utf8');
    } catch (_) {
      continue;
    }
    const fm = scanLib.parseFrontmatter(text) || {};
    const slug = String(fm.name || entry.name).trim();
    result.push({
      slug,
      dir,
      dirName: entry.name,
      version: fm.version ? String(fm.version).trim() : '',
      description: fm.description ? String(fm.description).trim() : '',
      treeHash: hashTree(dir),
      slugMismatch: slug !== entry.name,
    });
  }
  return result.sort((a, b) => a.slug.localeCompare(b.slug));
}

/** 轻量技能计数（顶层目录 / 链接含 SKILL.md；不做哈希，用于提示与 doctor）。 */
function countHubSkills(dir) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (_) {
    return 0;
  }
  let count = 0;
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    if (!entry.isDirectory() && !entry.isSymbolicLink()) continue;
    try {
      if (fs.existsSync(path.join(dir, entry.name, SKILL_FILE))) count += 1;
    } catch (_) { /* skip unreadable entry */ }
  }
  return count;
}

/** 空 Hub 提示：优先指向「未迁移旧 Hub」（0.29.5 S1），否则回退到 install / adopt。 */
function emptyHubHint(opts, hubDir) {
  const fallback = '先运行 yotta-skills hub install 或 hub adopt --apply';
  try {
    const config = skillsConfigLib.readConfig({ homeDir: opts.homeDir, env: opts.env });
    if (config.lastSwitch && config.lastSwitch.from && !samePath(config.lastSwitch.from, hubDir)) {
      const count = countHubSkills(config.lastSwitch.from);
      if (count > 0) {
        return '旧 Hub ' + config.lastSwitch.from + ' 还有 ' + count + ' 个技能未迁移；迁移：yotta-skills hub config set --hub "' +
          path.resolve(hubDir) + '" --move（面板「一键迁移」同源）';
      }
    }
  } catch (_) { /* fall back */ }
  return fallback;
}

function manifestSlugs(manifest) {
  const set = new Set();
  const list = Array.isArray(manifest) ? manifest : (manifest && manifest.skills) || [];
  for (const item of list) {
    if (item && item.slug) set.add(item.slug);
  }
  return set;
}

/** 家族 slug 集合：接受清单数组 / Set / {skills} 结构，并始终并入特殊家族 5 个。 */
function familySlugSet(manifest) {
  const set = new Set();
  if (manifest instanceof Set) {
    for (const slug of manifest) set.add(String(slug));
  } else {
    const list = Array.isArray(manifest) ? manifest : (manifest && manifest.skills) || [];
    for (const item of list) {
      if (typeof item === 'string') set.add(item);
      else if (item && item.slug) set.add(item.slug);
    }
  }
  for (const item of HUB_FAMILY_EXTRAS) set.add(item.slug);
  return set;
}

function compareVersions(left, right) {
  return scanLib.compareSemver(left, right);
}

function readSkillMeta(dir) {
  try {
    const text = fs.readFileSync(path.join(dir, SKILL_FILE), 'utf8');
    const fm = scanLib.parseFrontmatter(text) || {};
    return {
      name: String(fm.name || '').trim(),
      version: fm.version ? String(fm.version).trim() : '',
    };
  } catch (_) {
    return null;
  }
}

function resolveTrashRoot(hubDir, opts) {
  const options = opts || {};
  const explicit = options.trashRoot || options.trashDir || process.env.YOTTA_SKILLS_TRASH;
  if (explicit) return path.resolve(explicit);
  return path.join(path.dirname(path.resolve(hubDir)), 'trash');
}

function trashRunStamp(now) {
  const d = now instanceof Date ? now : new Date();
  const pad = (value) => String(value).padStart(2, '0');
  return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()) + '-' +
    pad(d.getHours()) + pad(d.getMinutes()) + pad(d.getSeconds()) + '-' + process.pid;
}

function safeHostName(value) {
  const cleaned = String(value || '')
    .replace(/[\\/:*?"<>|\s]+/g, '-')
    .replace(/^-+|-+$/g, '');
  return cleaned || 'host';
}

/** 目录短哈希（回收站命名去重：不同目录同 basename 时不互相撞车）。 */
function shortPathHash(dir) {
  return crypto.createHash('sha1').update(path.resolve(dir)).digest('hex').slice(0, 8);
}

/** 清理回收站中超过保留期的条目（best-effort；返回清理数量）。 */
function pruneTrash(trashRoot, options) {
  const opts = options || {};
  const days = Number(opts.days) > 0 ? Number(opts.days) : TRASH_RETENTION_DAYS;
  const now = opts.now instanceof Date ? opts.now.getTime() : Date.now();
  let pruned = 0;
  let entries;
  try {
    entries = fs.readdirSync(trashRoot, { withFileTypes: true });
  } catch (_) {
    return 0;
  }
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const full = path.join(trashRoot, entry.name);
    let stat;
    try {
      stat = fs.statSync(full);
    } catch (_) {
      continue;
    }
    if (now - stat.mtimeMs > days * 24 * 60 * 60 * 1000) {
      try {
        fs.rmSync(full, { recursive: true, force: true });
        pruned += 1;
      } catch (_) { /* keep for next run */ }
    }
  }
  return pruned;
}

/** 历史备份 / 暂存残留的目录名标记（0.29.5 S3）。 */
const BACKUP_RESIDUE_MARKERS = [
  '.yottaskills-backup-',
  '.yottaskills-import-',
  '.yottaskills-rollback-',
  '.yottaskills-staging',
];

/**
 * 扫描宿主 / Hub 目录里的 `.yottaskills-backup-*` / `.yottaskills-import-*`
 * 历史残留（只读）。dirs = [{ dir, label }] 或字符串数组。
 */
function findBackupResidues(options) {
  const opts = options || {};
  const dirs = Array.isArray(opts.dirs) ? opts.dirs : [];
  const found = [];
  for (const item of dirs) {
    const dir = path.resolve(typeof item === 'string' ? item : item.dir);
    const label = typeof item === 'string' ? null : (item.label || null);
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch (_) {
      continue;
    }
    for (const entry of entries) {
      if (!BACKUP_RESIDUE_MARKERS.some((marker) => entry.name.includes(marker))) continue;
      found.push({
        dir,
        label,
        name: entry.name,
        path: path.join(dir, entry.name),
      });
    }
  }
  return found;
}

/**
 * 清理历史备份残留：移入回收站 `backup-cleanup-<stamp>/`（保留 7 天）。
 * options: { dirs, hubDir, trashRoot, residues, now, renameEntry }
 */
function cleanupBackupResidues(options) {
  const opts = options || {};
  const residues = Array.isArray(opts.residues) ? opts.residues : findBackupResidues(opts);
  const baseHub = opts.hubDir || (opts.dirs && opts.dirs.length
    ? (typeof opts.dirs[0] === 'string' ? opts.dirs[0] : opts.dirs[0].dir)
    : null);
  const trashRoot = opts.trashRoot || resolveTrashRoot(baseHub || process.cwd(), opts);
  const stamp = trashRunStamp(opts.now);
  const renameEntry = typeof opts.renameEntry === 'function' ? opts.renameEntry : fs.renameSync;
  const moved = [];
  const failed = [];
  for (const item of residues) {
    const dest = path.join(
      trashRoot,
      'backup-cleanup-' + stamp,
      safeHostName(path.basename(item.dir)) + '-' + shortPathHash(item.dir),
      item.name,
    );
    try {
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      const transfer = moveEntryAcrossDevices(item.path, dest, { renameEntry });
      moved.push({ from: item.path, to: dest, dir: item.dir, name: item.name, method: transfer.method });
    } catch (error) {
      failed.push({ path: item.path, error: error.message });
    }
  }
  return { ok: failed.length === 0, trashRoot, found: residues.length, moved, failed };
}

/**
 * 列出宿主目录中某个家族技能的副本：
 * - 精确同名（slug）的真目录 / 链接；
 * - `slug__*` 前缀命名、frontmatter name === slug 的重命名副本。
 */
function listFamilyCopies(targetDir, slug) {
  const copies = [];
  let entries;
  try {
    entries = fs.readdirSync(targetDir, { withFileTypes: true });
  } catch (_) {
    return copies;
  }
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    const isExact = entry.name === slug;
    const isRenamed = entry.name.startsWith(slug + '__');
    if (!isExact && !isRenamed) continue;
    const full = path.join(targetDir, entry.name);
    let stat;
    try {
      stat = fs.lstatSync(full);
    } catch (_) {
      continue;
    }
    if (stat.isSymbolicLink()) {
      copies.push({ name: entry.name, dir: full, kind: 'link', version: '' });
      continue;
    }
    if (!stat.isDirectory()) {
      if (isExact) copies.push({ name: entry.name, dir: full, kind: 'file', version: '' });
      continue;
    }
    const meta = readSkillMeta(full);
    if (isRenamed && (!meta || meta.name !== slug)) continue;
    copies.push({
      name: entry.name,
      dir: full,
      kind: 'directory',
      version: meta ? (meta.version || '') : '',
      metaName: meta ? meta.name : '',
    });
  }
  return copies;
}

function syncHubState(hubDir, options) {
  const opts = options || {};
  const previous = readHubState(hubDir);
  const family = familySlugSet(opts.manifest);
  const scanned = scanHubSkills(hubDir);
  const upstream = skillsCliLock.readLock({ homeDir: opts.homeDir, env: opts.env });
  const now = nowIso();
  const skills = {};
  const seen = new Set();

  for (const item of scanned) {
    seen.add(item.slug);
    const old = previous.skills[item.slug] || {};
    const origin = old.origin || (family.has(item.slug) ? 'yotta' : 'external');
    const upstreamEntry = upstream.available ? upstream.skills[item.slug] : null;
    skills[item.slug] = {
      slug: item.slug,
      origin,
      version: item.version || old.version || null,
      treeHash: item.treeHash,
      dir: item.dir,
      description: item.description || old.description || '',
      source: (upstreamEntry && upstreamEntry.source) || old.source || (origin === 'yotta' ? 'npm' : 'local'),
      sourceType: (upstreamEntry && upstreamEntry.sourceType) || old.sourceType || null,
      sourceUrl: (upstreamEntry && upstreamEntry.sourceUrl) || old.sourceUrl || null,
      upstreamSkillHash: (upstreamEntry && upstreamEntry.skillFolderHash) || old.upstreamSkillHash || null,
      upstreamInstalledAt: (upstreamEntry && upstreamEntry.installedAt) || old.upstreamInstalledAt || null,
      upstreamUpdatedAt: (upstreamEntry && upstreamEntry.updatedAt) || old.upstreamUpdatedAt || null,
      sourcePath: old.sourcePath || null,
      sourceAgent: old.sourceAgent || null,
      importedAt: old.importedAt || now,
      updatedAt: now,
      scanVerdict: old.scanVerdict || null,
      inPlace: Boolean(old.inPlace),
      status: 'present',
      slugMismatch: item.slugMismatch,
    };
  }
  for (const [slug, old] of Object.entries(previous.skills)) {
    if (seen.has(slug)) continue;
    skills[slug] = { ...old, status: 'missing', updatedAt: now };
  }

  const state = { skills, upstreamLock: { path: upstream.path, available: upstream.available, version: upstream.version } };
  writeHubState(hubDir, state);
  return { state: readHubState(hubDir), scanned };
}

function createDirLink(target, linkPath) {
  fs.mkdirSync(path.dirname(linkPath), { recursive: true });
  const type = process.platform === 'win32' ? 'junction' : 'dir';
  fs.symlinkSync(path.resolve(target), linkPath, type);
}

function removeDirLink(linkPath) {
  try {
    fs.unlinkSync(linkPath);
  } catch (error) {
    if (error && (error.code === 'EPERM' || error.code === 'EISDIR')) {
      fs.rmdirSync(linkPath);
      return;
    }
    throw error;
  }
}

function classifyTarget(target, hubDir) {
  let stat;
  try {
    stat = fs.lstatSync(target);
  } catch (_) {
    return { kind: 'missing' };
  }
  if (stat.isSymbolicLink()) {
    let real = null;
    let targetExists = false;
    try {
      real = fs.realpathSync.native ? fs.realpathSync.native(target) : fs.realpathSync(target);
      targetExists = true;
    } catch (_) {
      try {
        real = fs.realpathSync(target);
        targetExists = true;
      } catch (_) { /* broken link: fall back to the recorded link value */ }
    }
    if (!real) {
      // A broken junction / symlink no longer resolves. Read the link value so
      // an unlink can still tell whether it points into the hub (fail-closed
      // cleanup path) without treating it as an arbitrary directory.
      let linkValue = null;
      try { linkValue = fs.readlinkSync(target); } catch (_) { linkValue = null; }
      real = linkValue ? path.resolve(path.dirname(path.resolve(target)), linkValue) : path.resolve(target);
    }
    return {
      kind: 'link',
      target: real,
      inHub: isInside(hubDir, real),
      targetExists,
    };
  }
  if (stat.isDirectory()) return { kind: 'directory' };
  return { kind: 'file' };
}

/**
 * 0.30.0 UX-02 / OPT-01：以文件系统为真源扫描目标目录内的链接。
 * - hubSlugs：指向当前 Hub 的链接（可安全清理）
 * - otherLinks：指向其它位置的链接（fail-closed，不动；供错位警告）
 */
function scanDirForHubLinks(targetDir, hubDir) {
  const hubSlugs = [];
  const otherLinks = [];
  let entries = [];
  try {
    entries = fs.readdirSync(targetDir, { withFileTypes: true });
  } catch (_) {
    return { hubSlugs, otherLinks, scanned: 0, readable: false };
  }
  for (const entry of entries) {
    const target = path.join(targetDir, entry.name);
    const current = classifyTarget(target, hubDir);
    if (current.kind !== 'link') continue;
    if (current.inHub) hubSlugs.push(entry.name);
    else otherLinks.push({ slug: entry.name, target: current.target, root: foreignHubRoot(current.target) });
  }
  return { hubSlugs, otherLinks, scanned: entries.length, readable: true };
}

/**
 * 解析链接目标所属的「其它 Hub」根目录：宿主链接通常指向 <hub>/<slug>，
 * 因此先看目标本身、再看父目录是否含元阁 Hub 台账标记；都不是则返回 null。
 */
function foreignHubRoot(target) {
  if (!target) return null;
  const resolved = path.resolve(target);
  for (const dir of [resolved, path.dirname(resolved)]) {
    try {
      if (fs.existsSync(path.join(dir, STATE_FILE))) return dir;
      if (fs.existsSync(path.join(dir, LINKS_FILE))) return dir;
      if (fs.existsSync(path.join(dir, AUDIT_FILE))) return dir;
    } catch (_) { /* 单个候选失败继续 */ }
  }
  return null;
}

function linkSkills(options) {
  const opts = options || {};
  const hubDir = path.resolve(opts.hubDir);
  const targetDir = path.resolve(opts.targetDir);
  const dryRun = Boolean(opts.dryRun);
  const force = Boolean(opts.force);
  const slugs = Array.isArray(opts.slugs) && opts.slugs.length > 0
    ? opts.slugs
    : scanHubSkills(hubDir).map((item) => item.slug);
  const hubBySlug = new Map(scanHubSkills(hubDir).map((item) => [item.slug, item]));
  const family = familySlugSet(opts.familySlugs || opts.manifest);
  const familyFallback = !opts.familySlugs && !opts.manifest;
  const links = readLinkState(hubDir).links.slice();
  const results = [];
  const trashRoot = resolveTrashRoot(hubDir, opts);
  const makeLink = typeof opts.createLink === 'function' ? opts.createLink : createDirLink;
  const renameEntry = typeof opts.renameEntry === 'function' ? opts.renameEntry : fs.renameSync;
  const stamp = trashRunStamp(opts.now);
  const hostName = safeHostName(opts.label || path.basename(targetDir)) + '-' + shortPathHash(targetDir);
  let prunedTrash = 0;
  if (!dryRun) {
    try {
      prunedTrash = pruneTrash(trashRoot, { days: opts.trashRetentionDays });
    } catch (_) { prunedTrash = 0; }
  }

  for (const slug of slugs) {
    const skill = hubBySlug.get(slug);
    if (!skill) {
      results.push({ slug, status: 'missing', note: 'hub 中没有该技能' });
      continue;
    }
    const target = path.join(targetDir, slug);
    const current = classifyTarget(target, hubDir);
    const isFamily = family.has(slug) || (familyFallback && slug.startsWith('yotta-'));

    // ── 家族技能：链接时唯一性收敛（产品口径） ──────────────────────────
    if (isFamily) {
      const copies = listFamilyCopies(targetDir, slug);
      const exactCopy = copies.find((copy) => copy.name === slug) || null;
      const renamedCopies = copies.filter((copy) => copy.name !== slug);
      const exactHealthy = current.kind === 'link' && current.inHub &&
        current.targetExists !== false && samePath(current.target, skill.dir);
      const moves = [];
      const skipped = [];
      let block = null;
      let replaceExactLink = false;

      const evaluate = (copy, isExact) => {
        if (!copy) return;
        const cls = classifyTarget(copy.dir, hubDir);
        if (cls.kind === 'link') {
          const pointsAtHub = cls.inHub && cls.targetExists !== false && samePath(cls.target, skill.dir);
          if (pointsAtHub && isExact) return; // 已是目标链接，保留
          if (cls.inHub) {
            moves.push({ name: copy.name, dir: copy.dir, version: copy.version || '' });
            return;
          }
          if (isExact) {
            if (force) {
              replaceExactLink = true;
            } else {
              block = { status: 'conflict', note: '目标已存在指向 Hub 之外的链接（默认跳过；确认后可加 --force 替换）' };
            }
          } else {
            skipped.push(copy.name + '（外部链接，保留）');
          }
          return;
        }
        if (cls.kind === 'directory') {
          const meta = readSkillMeta(copy.dir);
          if (!meta || meta.name !== slug) {
            if (isExact) block = { status: 'conflict', note: '目标已存在真目录（frontmatter name 与技能不符，拒绝收敛）' };
            else skipped.push(copy.name + '（name 不符，保留）');
            return;
          }
          const version = meta.version || '';
          if (!skill.version) {
            block = { status: 'skipped', note: 'Hub 副本版本无法解析；跳过收敛（fail-safe）' };
            return;
          }
          if (!version) {
            block = { status: 'skipped', note: copy.name + ' 版本无法解析；跳过收敛（fail-safe）' };
            return;
          }
          if (compareVersions(version, skill.version) > 0) {
            block = {
              status: 'skipped',
              note: copy.name + ' v' + version + ' 高于 Hub v' + skill.version + '；先运行 yotta-skills hub update 再链接',
            };
            return;
          }
          moves.push({ name: copy.name, dir: copy.dir, version });
          return;
        }
        if (cls.kind === 'file') {
          if (isExact) block = { status: 'conflict', note: '目标已存在普通文件（拒绝覆盖）' };
        }
      };
      evaluate(exactCopy, true);
      for (const copy of renamedCopies) evaluate(copy, false);

      if (block) {
        if (exactHealthy) {
          results.push({ slug, status: 'linked', target, note: '已链接到 hub；仍有未收敛副本：' + block.note });
        } else {
          results.push({ slug, status: block.status, target, note: block.note });
        }
        continue;
      }
      if (moves.length === 0 && exactHealthy) {
        results.push({
          slug,
          status: 'linked',
          target,
          note: '已链接到 hub' + (skipped.length ? '（保留：' + skipped.join('、') + '）' : ''),
        });
        continue;
      }
      if (moves.length > 0 && dryRun) {
        results.push({
          slug,
          status: 'would-converge',
          target,
          note: '将收敛 ' + moves.length + ' 份旧副本（移入回收站，保留 ' + TRASH_RETENTION_DAYS + ' 天）' +
            (replaceExactLink ? '并替换指向 Hub 之外的链接' : '') + '后建立链接：' +
            moves.map((item) => item.name).join('、'),
          moves: moves.map((item) => ({ from: item.dir, name: item.name, version: item.version || null })),
          trashDir: trashRoot,
        });
        continue;
      }
      if (moves.length === 0 && dryRun) {
        results.push(replaceExactLink
          ? { slug, status: 'would-replace', target, note: '将替换指向 Hub 之外的链接并建立链接' }
          : { slug, status: 'would-link', target, note: '将建立链接' });
        continue;
      }
      if (moves.length === 0) {
        try {
          if (replaceExactLink) removeDirLink(target);
          makeLink(skill.dir, target);
          const index = links.findIndex((item) => item.slug === slug && samePath(item.dir || '', targetDir));
          const record = {
            slug,
            agent: opts.agentId || null,
            label: opts.label || null,
            dir: targetDir,
            target,
            hubDir: skill.dir,
            linkedAt: nowIso(),
            backup: null,
          };
          if (index >= 0) links[index] = record;
          else links.push(record);
          results.push({
            slug,
            status: 'linked',
            target,
            note: (replaceExactLink
              ? '已替换指向 Hub 之外的链接并建立链接（仅移除链接本身，目标目录未动）'
              : '已建立链接') + (skipped.length ? '（保留：' + skipped.join('、') + '）' : ''),
          });
          appendAudit(hubDir, {
            event: 'link',
            slug,
            target,
            hubDir: skill.dir,
            backup: null,
            ...(replaceExactLink ? { replacedExternalLink: true } : {}),
          });
        } catch (error) {
          results.push({
            slug,
            status: 'error',
            target,
            note: (replaceExactLink ? '替换失败：' : '') + error.message +
              '（未静默降级为复制；请检查目录权限或改用 --dir 指定可写目录）',
          });
        }
        continue;
      }
      const moved = [];
      try {
        for (const item of moves) {
          const dest = path.join(trashRoot, stamp, hostName, item.name);
          fs.mkdirSync(path.dirname(dest), { recursive: true });
          const transfer = moveEntryAcrossDevices(item.dir, dest, { renameEntry });
          moved.push({
            from: item.dir,
            to: dest,
            name: item.name,
            version: item.version || null,
            method: transfer.method,
          });
        }
        if (!exactHealthy) {
          if (replaceExactLink) removeDirLink(target);
          makeLink(skill.dir, target);
        }
        const index = links.findIndex((item) => item.slug === slug && samePath(item.dir || '', targetDir));
        const record = {
          slug,
          agent: opts.agentId || null,
          label: opts.label || null,
          dir: targetDir,
          target,
          hubDir: skill.dir,
          linkedAt: nowIso(),
          backup: null,
          converged: moved.map((item) => item.to),
        };
        if (index >= 0) links[index] = record;
        else links.push(record);
        const copiedCount = moved.filter((item) => item.method === 'copy').length;
        results.push({
          slug,
          status: 'linked',
          target,
          note: '已收敛 ' + moved.length + ' 份旧副本（回收站保留 ' + TRASH_RETENTION_DAYS + ' 天）并建立链接' +
            (replaceExactLink ? '（已替换指向 Hub 之外的链接；仅移除链接本身）' : '') +
            (copiedCount ? '（其中 ' + copiedCount + ' 份跨卷复制，校验通过）' : '') +
            (skipped.length ? '；保留：' + skipped.join('、') : ''),
          moved,
          trashDir: trashRoot,
        });
        appendAudit(hubDir, {
          event: 'converge',
          slug,
          target,
          hubDir: skill.dir,
          hubVersion: skill.version,
          moved,
          trashDir: trashRoot,
          ...(replaceExactLink ? { replacedExternalLink: true } : {}),
        });
      } catch (error) {
        let restored = true;
        for (const item of moved.slice().reverse()) {
          try {
            fs.mkdirSync(path.dirname(item.from), { recursive: true });
            moveEntryAcrossDevices(item.to, item.from, { renameEntry });
          } catch (_) { restored = false; }
        }
        results.push({
          slug,
          status: 'error',
          target,
          restored,
          note: '收敛失败：' + error.message +
            (restored ? '（已恢复原目录）' : '（恢复失败，请查看回收站：' + trashRoot + '）'),
          trashDir: trashRoot,
        });
      }
      continue;
    }

    // ── 非家族技能：保持原行为（同名冲突默认跳过，不自动删） ────────────
    let backup = null;
    let backupMethod = null;
    if (current.kind === 'link' && current.inHub && current.targetExists !== false && samePath(current.target, skill.dir)) {
      results.push({ slug, status: 'linked', target, note: '已链接到 hub' });
      continue;
    }
    if (current.kind !== 'missing') {
      if (!force) {
        results.push({
          slug,
          status: 'conflict',
          target,
          note: current.kind === 'directory'
            ? '目标已存在真目录（默认跳过；确认后可加 --force 备份并替换）'
            : current.kind === 'link'
              ? '目标已存在其他链接（默认跳过；确认后可加 --force 替换）'
              : '目标已存在普通文件（拒绝覆盖）',
        });
        continue;
      }
      if (current.kind === 'directory') {
        if (dryRun) {
          results.push({
            slug,
            status: 'would-backup',
            target,
            note: '将把真目录旧副本移入回收站（保留 ' + TRASH_RETENTION_DAYS + ' 天）后建立链接',
          });
          continue;
        }
        // 0.29.5 S3：旧副本不再原地留 <name>.yottaskills-backup-*（宿主会当技能扫），
        // 统一移入回收站（7 天可恢复）；跨卷走复制 + 校验 + 删源。
        const dest = path.join(trashRoot, stamp, hostName, slug);
        fs.mkdirSync(path.dirname(dest), { recursive: true });
        const transfer = moveEntryAcrossDevices(target, dest, { renameEntry });
        backup = dest;
        backupMethod = transfer.method;
      } else if (current.kind === 'link') {
        if (dryRun) {
          results.push({ slug, status: 'would-replace', target, note: '将替换已有链接' });
          continue;
        }
        removeDirLink(target);
      } else {
        results.push({ slug, status: 'conflict', target, note: '目标已存在普通文件（拒绝覆盖）' });
        continue;
      }
    }
    if (dryRun) {
      results.push({ slug, status: 'would-link', target, note: '将建立链接' });
      continue;
    }
    let linked = false;
    try {
      makeLink(skill.dir, target);
      linked = true;
      const index = links.findIndex((item) => item.slug === slug && samePath(item.dir || '', targetDir));
      const record = {
        slug,
        agent: opts.agentId || null,
        label: opts.label || null,
        dir: targetDir,
        target,
        hubDir: skill.dir,
        linkedAt: nowIso(),
        backup,
        backupMethod,
      };
      if (index >= 0) links[index] = record;
      else links.push(record);
      results.push({
        slug,
        status: 'linked',
        target,
        note: backup
          ? '真目录旧副本已移入回收站（保留 ' + TRASH_RETENTION_DAYS + ' 天）并建立链接'
          : '已建立链接',
        backup,
        backupMethod,
        trashDir: backup ? trashRoot : null,
      });
      try {
        appendAudit(hubDir, { event: 'link', slug, target, hubDir: skill.dir, backup, backupMethod });
      } catch (_) { /* 审计失败不把已完成的链接判失败 */ }
    } catch (error) {
      // 替换失败时把旧副本从回收站移回原位，避免宿主目录留下空位。
      let restored = false;
      if (backup && !linked) {
        try {
          moveEntryAcrossDevices(backup, target, { renameEntry });
          restored = true;
        } catch (_) { /* 保留回收站副本供人工恢复 */ }
      }
      results.push({
        slug,
        status: 'error',
        target,
        backup: restored ? null : backup,
        note: error.message +
          (backup ? (restored ? '（旧副本已恢复原位）' : '（旧副本保留在回收站：' + backup + '）') : '') +
          '（未静默降级为复制；请检查目录权限或改用 --dir 指定可写目录）',
      });
    }
  }
  if (!dryRun) {
    writeLinkState(hubDir, { links });
    try {
      syncHubState(hubDir, { manifest: opts.manifest, homeDir: opts.homeDir, env: opts.env });
    } catch (_) { /* link state is already durable; state refresh is best-effort */ }
  }
  return { hubDir, targetDir, dryRun, results, trashRoot, prunedTrash };
}

function unlinkSkills(options) {
  const opts = options || {};
  const hubDir = path.resolve(opts.hubDir);
  const targetDir = path.resolve(opts.targetDir);
  const dryRun = Boolean(opts.dryRun);
  const linkState = readLinkState(hubDir);
  let slugs = null;
  let discovery = null;
  if (Array.isArray(opts.slugs) && opts.slugs.length > 0) {
    slugs = opts.slugs;
  } else {
    // 0.30.0 UX-02 / OPT-01：无 slug 时以文件系统为真源扫描目标目录
    // （台账仅作辅助），保证「指向当前 Hub 的链接」即使台账缺失也能被清理；
    // 同时记录指向其它位置的链接数，供调用方输出错位警告。
    const ledgerSlugs = linkState.links
      .filter((item) => samePath(item.dir || '', targetDir))
      .map((item) => item.slug);
    const scan = scanDirForHubLinks(targetDir, hubDir);
    slugs = [...new Set(ledgerSlugs.concat(scan.hubSlugs))];
    discovery = {
      source: 'filesystem+ledger',
      fromLedger: ledgerSlugs.length,
      fromFilesystem: scan.hubSlugs.length,
      scannedEntries: scan.scanned,
      dirReadable: scan.readable,
      otherLinks: scan.otherLinks.length,
      otherTargets: [...new Set(scan.otherLinks.map((item) => item.root || item.target))].slice(0, 5),
    };
  }
  const unique = [...new Set(slugs)];
  const links = linkState.links.slice();
  const results = [];

  for (const slug of unique) {
    const target = path.join(targetDir, slug);
    const current = classifyTarget(target, hubDir);
    if (current.kind === 'missing') {
      results.push({ slug, status: 'missing', target, note: '目标不存在' });
      continue;
    }
    if (current.kind !== 'link') {
      results.push({ slug, status: 'refused', target, note: '目标不是链接；fail-closed，拒绝删除' });
      continue;
    }
    if (!current.inHub) {
      results.push({ slug, status: 'refused', target, note: '链接目标不在 hub 内；fail-closed，拒绝删除' });
      continue;
    }
    if (dryRun) {
      results.push({ slug, status: 'would-unlink', target, note: '将删除链接（不动 hub 真源）' });
      continue;
    }
    try {
      removeDirLink(target);
      for (let i = links.length - 1; i >= 0; i--) {
        if (links[i].slug === slug && samePath(links[i].dir || '', targetDir)) links.splice(i, 1);
      }
      results.push({ slug, status: 'unlinked', target, note: '已删除链接（hub 真源保留）' });
      appendAudit(hubDir, { event: 'unlink', slug, target });
    } catch (error) {
      results.push({ slug, status: 'error', target, note: error.message });
    }
  }
  if (!dryRun) writeLinkState(hubDir, { links });
  return { hubDir, targetDir, dryRun, results, discovery };
}

/**
 * 删除 Hub 技能：全宿主清理指向 Hub 的链接（含死链）→ Hub 目录移入回收站 →
 * 定向清 Hub 台账与链接台账 → 写审计。
 *
 * 五阶段 fail-closed：
 *   1. preflight（只读分类，dry-run 到此为止）
 *   2. unlink（只删指向 Hub 的链接；报错即中止，不进入 3）
 *   3. trash（目录移入回收站保留 7 天；跨卷走复制 + 校验 + 删源）
 *   4. ledger（定向删 Hub 台账条目 + 过滤链接台账；不调 syncHubState，防记回 missing）
 *   5. 汇总（含版本闸门报告）
 *
 * options:
 * - hubDir / slug（必填）
 * - targets: [{ dir, label, agentId }]（调用方解析范围；核心不做范围判断）
 * - dryRun / trashRoot / trashRetentionDays / now
 * - renameEntry / unlink（测试注入点）
 */
function removeSkills(options) {
  const opts = options || {};
  const hubDir = path.resolve(opts.hubDir);
  const slug = String(opts.slug || '').trim().toLowerCase();
  const dryRun = Boolean(opts.dryRun);
  const unlinkFn = typeof opts.unlink === 'function' ? opts.unlink : unlinkSkills;
  const targets = (Array.isArray(opts.targets) ? opts.targets : [])
    .filter((item) => item && item.dir)
    .map((item) => ({
      dir: path.resolve(item.dir),
      label: item.label || '指定目录',
      agentId: item.agentId || null,
    }));
  const trashRoot = resolveTrashRoot(hubDir, opts);
  const skillDir = path.join(hubDir, slug);
  const compact = (plan) => ({
    dir: plan.dir,
    label: plan.label,
    status: plan.status,
    action: plan.action,
    note: plan.note,
    ...(plan.version ? { version: plan.version } : {}),
    ...(plan.versionGate ? { versionGate: true } : {}),
    ...(plan.drift ? { drift: true } : {}),
    ...(plan.broken ? { broken: true } : {}),
  });

  let hubPathKind = 'missing';
  let hubEntry = null;
  try {
    const stat = fs.lstatSync(skillDir);
    hubPathKind = stat.isSymbolicLink() ? 'link' : stat.isDirectory() ? 'directory' : 'file';
  } catch (_) {
    hubPathKind = 'missing';
  }
  if (hubPathKind === 'file') {
    return {
      hubDir,
      slug,
      dryRun,
      verdict: 'failed',
      ok: false,
      exitCode: 1,
      hubPresent: false,
      hubPathKind,
      hubVersion: null,
      targets: [],
      unlinkable: 0,
      kept: [],
      failed: [{ dir: skillDir, note: 'Hub 内同名路径是普通文件；fail-closed，拒绝删除' }],
      trashedTo: null,
    };
  }
  if (hubPathKind !== 'missing') {
    hubEntry = scanHubSkills(hubDir).find((item) => samePath(item.dir, skillDir)) || null;
  }
  const hubVersion = hubEntry && hubEntry.version ? hubEntry.version : '';

  // ── 1. preflight（只读） ────────────────────────────────────────────────
  const plans = targets.map((target) => {
    const targetPath = path.join(target.dir, slug);
    const current = classifyTarget(targetPath, hubDir);
    if (current.kind === 'missing') {
      return {
        dir: target.dir,
        label: target.label,
        target: targetPath,
        action: 'none',
        status: 'missing',
        note: '目标不存在',
      };
    }
    if (current.kind === 'link') {
      if (!current.inHub) {
        return {
          dir: target.dir,
          label: target.label,
          target: targetPath,
          action: 'keep',
          status: 'refused',
          note: '链接指向 Hub 之外；fail-closed 保留',
        };
      }
      const drift = !samePath(current.target, skillDir);
      const broken = current.targetExists === false;
      return {
        dir: target.dir,
        label: target.label,
        target: targetPath,
        action: 'unlink',
        status: 'link',
        drift,
        broken,
        note: broken
          ? '死链（Hub 目标缺失），将清理'
          : drift
            ? '链接指向 Hub 内其它技能，将一并清理'
            : '指向本技能的链接，将清理',
      };
    }
    if (current.kind === 'directory') {
      const meta = readSkillMeta(targetPath);
      const version = meta && meta.version ? meta.version : '';
      const higher = Boolean(version && hubVersion && compareVersions(version, hubVersion) > 0);
      return {
        dir: target.dir,
        label: target.label,
        target: targetPath,
        action: 'keep',
        status: 'kept-directory',
        version: version || null,
        versionGate: higher,
        note: higher
          ? '宿主真副本 v' + version + ' 高于 Hub v' + hubVersion + '；保留（先确认该副本）'
          : '宿主真副本，保留（只删链接）',
      };
    }
    return {
      dir: target.dir,
      label: target.label,
      target: targetPath,
      action: 'keep',
      status: 'kept-file',
      note: '普通文件，保留',
    };
  });

  const stateSnapshot = readHubState(hubDir);
  const hasStateEntry = Boolean(stateSnapshot.skills && stateSnapshot.skills[slug]);
  const hubPresent = hubPathKind === 'directory' || hubPathKind === 'link';
  const unlinkable = plans.filter((plan) => plan.action === 'unlink').length;
  const kept = plans.filter((plan) => plan.action === 'keep');
  const base = {
    hubDir,
    slug,
    dryRun,
    hubPresent,
    hubPathKind,
    hubVersion: hubVersion || null,
    targets: plans.map(compact),
    unlinkable,
    kept: kept.map(compact),
  };
  if (dryRun) {
    return { ...base, verdict: 'dry-run', ok: true, exitCode: 0, trashedTo: null };
  }

  // ── 2. unlink（含死链；报错即中止，不删 Hub） ───────────────────────────
  const unlinked = [];
  const failed = [];
  for (const plan of plans) {
    if (plan.action !== 'unlink') continue;
    const result = unlinkFn({ hubDir, targetDir: plan.dir, slugs: [slug], dryRun: false });
    const item = (result.results || [])[0] || { status: 'error', note: '未知结果' };
    plan.status = item.status;
    plan.note = item.note || plan.note;
    if (item.status === 'error') failed.push({ dir: plan.dir, note: item.note });
    else unlinked.push({ dir: plan.dir, status: item.status, note: item.note });
  }
  if (failed.length > 0) {
    if (fs.existsSync(hubDir)) {
      try {
        appendAudit(hubDir, {
          event: 'remove',
          slug,
          verdict: 'failed',
          reason: 'unlink-error',
          targets: plans.map(compact),
          removedLinks: unlinked.length,
        });
      } catch (_) { /* audit best-effort */ }
    }
    return { ...base, verdict: 'failed', ok: false, exitCode: 1, unlinked, failed, trashedTo: null };
  }

  // ── 3. trash（Hub 目录入回收站；失败即中止） ────────────────────────────
  let trashedTo = null;
  let method = null;
  if (hubPresent) {
    trashedTo = path.join(trashRoot, trashRunStamp(opts.now), 'hub-remove', slug);
    try {
      fs.mkdirSync(path.dirname(trashedTo), { recursive: true });
      const transfer = moveEntryAcrossDevices(skillDir, trashedTo, { renameEntry: opts.renameEntry });
      method = transfer.method;
    } catch (error) {
      if (fs.existsSync(hubDir)) {
        try {
          appendAudit(hubDir, {
            event: 'remove',
            slug,
            verdict: 'failed',
            reason: 'trash-error',
            targets: plans.map(compact),
            removedLinks: unlinked.length,
            trashedTo,
          });
        } catch (_) { /* audit best-effort */ }
      }
      return {
        ...base,
        verdict: 'failed',
        ok: false,
        exitCode: 1,
        unlinked,
        failed: [{ dir: skillDir, note: error.message }],
        trashedTo,
      };
    }
  }

  // ── 4. ledger（定向清台账；不调 syncHubState） ──────────────────────────
  const state = readHubState(hubDir);
  if (state.skills && state.skills[slug]) {
    delete state.skills[slug];
    writeHubState(hubDir, state);
  }
  const linkState = readLinkState(hubDir);
  const remainingLinks = linkState.links.filter((item) => item.slug !== slug);
  if (remainingLinks.length !== linkState.links.length) {
    writeLinkState(hubDir, { links: remainingLinks });
  }
  let prunedTrash = 0;
  try { prunedTrash = pruneTrash(trashRoot, { days: opts.trashRetentionDays }); } catch (_) { prunedTrash = 0; }

  // ── 5. 汇总 + 审计 ─────────────────────────────────────────────────────
  const verdict = hubPresent ? 'removed' : (unlinked.length > 0 || hasStateEntry ? 'cleanup-only' : 'not-found');
  const exitCode = verdict === 'not-found' ? 4 : 0;
  if (fs.existsSync(hubDir)) {
    try {
      appendAudit(hubDir, {
        event: 'remove',
        slug,
        verdict,
        targets: plans.map(compact),
        removedLinks: unlinked.length,
        kept: kept.length,
        trashedTo,
        method,
      });
    } catch (_) { /* audit best-effort */ }
  }
  return {
    ...base,
    verdict,
    ok: exitCode === 0,
    exitCode,
    unlinked,
    kept: kept.map(compact),
    trashedTo,
    method,
    prunedTrash,
  };
}

function linkStatus(hubDir) {
  const state = readLinkState(hubDir);
  return state.links.map((item) => {
    const current = classifyTarget(item.target, hubDir);
    return {
      ...item,
      status: current.kind === 'link'
        ? (!current.inHub ? 'drift' : (current.targetExists === false ? 'broken' : 'ok'))
        : current.kind === 'missing' ? 'broken' : 'drift',
      actual: current,
    };
  });
}

function status(options) {
  const opts = options || {};
  const hubDir = path.resolve(opts.hubDir);
  const synced = syncHubState(hubDir, { manifest: opts.manifest, homeDir: opts.homeDir, env: opts.env });
  const links = linkStatus(hubDir);
  const skills = Object.values(synced.state.skills)
    .sort((a, b) => a.slug.localeCompare(b.slug))
    .map((skill) => ({
      ...skill,
      links: links.filter((link) => link.slug === skill.slug),
    }));
  return {
    standard: STANDARD_ID,
    hubDir,
    skills,
    links,
    summary: {
      skills: skills.filter((skill) => skill.status === 'present').length,
      external: skills.filter((skill) => skill.origin === 'external').length,
      links: links.length,
      brokenLinks: links.filter((link) => link.status !== 'ok').length,
    },
  };
}

/**
 * doctor 只读检查：宿主目录中的家族技能副本是否唯一 / 版本是否落后。
 * 只报告不修改；真正的收敛发生在 hub link 执行时。
 */
function singleSourceChecks(opts, add) {
  const hubDir = path.resolve(opts.hubDir);
  if (!fs.existsSync(hubDir)) return;
  const family = familySlugSet(opts.manifest);
  let discovery = opts.discovery;
  if (!discovery) {
    try {
      discovery = require('./agent-discovery').discoverHosts({ homeDir: opts.homeDir, env: opts.env });
    } catch (_) {
      return;
    }
  }
  const hubSkills = new Map(scanHubSkills(hubDir).map((item) => [item.slug, item]));
  for (const host of discovery.hosts || []) {
    if (!host || !host.exists) continue;
    const groups = new Map();
    let entries;
    try {
      entries = fs.readdirSync(host.dir, { withFileTypes: true });
    } catch (_) {
      continue;
    }
    for (const entry of entries) {
      if (entry.name.startsWith('.')) continue;
      if (!entry.name.startsWith('yotta-')) continue; // 家族 slug 统一前缀，避免读外部技能
      if (!entry.isDirectory() && !entry.isSymbolicLink()) continue;
      const dir = path.join(host.dir, entry.name);
      const meta = readSkillMeta(dir);
      if (!meta || !meta.name || !family.has(meta.name)) continue;
      if (!groups.has(meta.name)) groups.set(meta.name, []);
      groups.get(meta.name).push({
        name: entry.name,
        dir,
        version: meta.version || '',
        kind: entry.isSymbolicLink() ? 'link' : 'directory',
      });
    }
    for (const [slug, copies] of groups) {
      if (copies.length > 1) {
        add('single_source:' + (host.agentId || host.label) + ':' + slug, false, 'warning',
          host.label + ' 中 ' + slug + ' 存在 ' + copies.length + ' 份副本（按 name 引用有歧义）：' +
            copies.map((copy) => copy.name).join('、'),
          '运行 yotta-skills hub link --agent ' + (host.agentId || '<id>') + ' 收敛（旧副本移入回收站，保留 ' + TRASH_RETENTION_DAYS + ' 天）');
      }
      const hubSkill = hubSkills.get(slug);
      if (!hubSkill || !hubSkill.version) continue;
      const single = copies.length === 1 ? copies[0] : null;
      if (!single || single.kind !== 'directory' || !single.version) continue;
      const diff = compareVersions(single.version, hubSkill.version);
      if (diff > 0) {
        add('single_source_version:' + (host.agentId || host.label) + ':' + slug, false, 'warning',
          host.label + ' 的 ' + slug + ' v' + single.version + ' 高于 Hub v' + hubSkill.version,
          '先运行 yotta-skills hub update（或该技能自身更新）再链接');
      } else if (diff < 0) {
        add('single_source_version:' + (host.agentId || host.label) + ':' + slug, true, 'info',
          host.label + ' 的 ' + slug + ' v' + single.version + ' 低于 Hub v' + hubSkill.version + '（链接时自动收敛）');
      }
    }
  }
}

/** 0.29.5 S3：历史备份 / 暂存残留只读检查（宿主扫描目录 + Hub 自身）。 */
function backupResidueChecks(opts, add) {
  const hubDir = path.resolve(opts.hubDir);
  const dirs = [];
  if (fs.existsSync(hubDir)) dirs.push({ dir: hubDir, label: 'Hub' });
  let discovery = opts.discovery;
  if (!discovery) {
    try {
      discovery = require('./agent-discovery').discoverHosts({ homeDir: opts.homeDir, env: opts.env });
    } catch (_) {
      discovery = { hosts: [] };
    }
  }
  for (const host of discovery.hosts || []) {
    if (!host || !host.exists || !host.dir) continue;
    dirs.push({ dir: host.dir, label: host.label || host.agentId || host.dir });
  }
  const residues = findBackupResidues({ dirs });
  if (residues.length === 0) return;
  const byDir = new Map();
  for (const item of residues) {
    if (!byDir.has(item.dir)) byDir.set(item.dir, []);
    byDir.get(item.dir).push(item.name);
  }
  for (const [dir, names] of byDir) {
    add('backup_residue:' + dir, false, 'warning',
      '发现 ' + names.length + ' 个历史备份 / 暂存残留（宿主会把备份当技能扫描）: ' + names.slice(0, 5).join('、') +
        (names.length > 5 ? ' 等 ' + names.length + ' 项' : ''),
      '清理：yotta-skills hub cleanup-backups --yes（移入回收站，保留 ' + TRASH_RETENTION_DAYS + ' 天）');
  }
}

function doctor(options) {
  const opts = options || {};
  const hubDir = path.resolve(opts.hubDir);
  const checks = [];
  const add = (id, ok, severity, message, hint) => {
    checks.push({ id, ok: Boolean(ok), severity, message, hint: hint || null });
  };

  add('hub_dir', fs.existsSync(hubDir), 'error',
    fs.existsSync(hubDir) ? 'Hub 目录存在' : 'Hub 目录不存在',
    fs.existsSync(hubDir) ? null : emptyHubHint(opts, hubDir));
  if (fs.existsSync(hubDir)) {
    try {
      fs.accessSync(hubDir, fs.constants.W_OK);
      add('hub_writable', true, 'error', 'Hub 目录可写');
    } catch (_) {
      add('hub_writable', false, 'error', 'Hub 目录不可写', '检查目录权限后重试');
    }
  }

  const synced = syncHubState(hubDir, {
    manifest: opts.manifest,
    homeDir: opts.homeDir,
    env: opts.env,
  });
  const stateSkills = Object.values(synced.state.skills || {});
  if (fs.existsSync(hubDir) && stateSkills.length === 0) {
    add('hub_nonempty', false, 'error', 'Hub 目录存在但没有任何技能',
      emptyHubHint(opts, hubDir));
  }
  for (const skill of stateSkills) {
    add('skill_present:' + skill.slug, skill.status === 'present', 'error',
      skill.status === 'present' ? skill.slug + ' 目标存在' : skill.slug + ' 目标缺失',
      skill.status === 'present' ? null : '重新收编 / 重装该技能，或删除对应链接');
    if (skill.slugMismatch) {
      add('slug_match:' + skill.slug, false, 'warning',
        skill.slug + ' 的 frontmatter name 与目录名不一致',
        '把目录名改为 frontmatter name，或修正 SKILL.md');
    }
  }

  const links = linkStatus(hubDir);
  for (const link of links) {
    add('link:' + link.slug + ':' + link.dir, link.status === 'ok', link.status === 'ok' ? 'info' : 'error',
      link.status === 'ok' ? '链接正常: ' + link.slug : '链接异常（' + link.status + '）: ' + link.slug,
      link.status === 'ok' ? null : '运行 hub link --all 重建，或 hub unlink 清理断链');
  }

  const scopeDirs = Array.isArray(opts.linkScopeDirs) ? opts.linkScopeDirs : null;
  if (scopeDirs && scopeDirs.length > 0) {
    const scope = new Set(scopeDirs.map((dir) => pathKey(dir)));
    const outside = new Map();
    for (const link of links) {
      if (!link.dir) continue;
      if (scope.has(pathKey(link.dir))) continue;
      if (!outside.has(link.dir)) outside.set(link.dir, []);
      outside.get(link.dir).push(link.slug);
    }
    for (const [dir, slugs] of outside) {
      add('link_scope:' + dir, false, 'warning',
        '链接位于默认范围之外: ' + dir + '（' + slugs.length + ' 条）',
        '默认范围 = 已核实宿主；如需保留请用 hub link --dir 或 --include-discovered 显式重建，否则用 hub unlink --dir "' + dir + '" 清理');
    }
  }

  // 0.30.0 UX-03：宿主链接目标 vs 当前 Hub 一致性（配置错位提前发现）。
  if (scopeDirs && scopeDirs.length > 0) {
    const foreign = new Map();
    for (const dir of scopeDirs) {
      let entries = [];
      try {
        entries = fs.readdirSync(dir, { withFileTypes: true });
      } catch (_) {
        continue;
      }
      for (const entry of entries) {
        const target = path.join(dir, entry.name);
        const current = classifyTarget(target, hubDir);
        if (current.kind !== 'link' || current.inHub) continue;
        const root = foreignHubRoot(current.target);
        if (!root) continue;
        if (!foreign.has(root)) {
          foreign.set(root, { count: 0, dirs: new Set(), slugs: new Set() });
        }
        const rec = foreign.get(root);
        rec.count += 1;
        rec.dirs.add(dir);
        rec.slugs.add(entry.name);
      }
    }
    for (const [target, rec] of foreign) {
      add('hub_mismatch:' + pathKey(target), false, 'warning',
        '发现 ' + rec.count + ' 条链接指向其它 Hub: ' + target + '（当前 Hub: ' + hubDir + '）',
        '核对位置来源: yotta-skills hub config get；恢复配置 = hub config set --hub "' + target +
        '"，或重链到当前 Hub = hub link --all --force。');
    }
  }

  try {
    singleSourceChecks(opts, add);
  } catch (_) { /* 只读检查失败不影响 doctor 主流程 */ }
  try {
    backupResidueChecks(opts, add);
  } catch (_) { /* 只读检查失败不影响 doctor 主流程 */ }

  // F3（0.29.0）：宿主状态细分只读检查 —— 残留 / 仅标记给 info 提示，不 fail。
  if (opts.discovery) {
    for (const host of opts.discovery.hosts || []) {
      if (!host || !host.dir) continue;
      if (host.state === 'orphan') {
        add('host_state:' + pathKey(host.dir), true, 'info',
          '宿主目录疑似残留（实体未确认）: ' + host.label + ' — ' + host.dir,
          '确认宿主已卸载后可清理：yotta-skills hub hosts remove "' + host.dir + '" --purge（默认预览，--yes 执行）');
      } else if (host.state === 'marker-only') {
        add('host_state:' + pathKey(host.dir), true, 'info',
          '已装实体但技能目录未创建: ' + host.label,
          '需要分发时运行 yotta-skills hub link --agent ' + (host.agentId || '<id>'));
      }
    }
  }

  const errors = checks.filter((check) => !check.ok && check.severity === 'error');
  const warnings = checks.filter((check) => !check.ok && check.severity === 'warning');
  return {
    ok: errors.length === 0,
    hubDir,
    checks,
    summary: {
      errors: errors.length,
      warnings: warnings.length,
      info: checks.filter((check) => check.severity === 'info').length,
    },
  };
}

module.exports = {
  STANDARD_ID,
  STATE_FILE,
  LINKS_FILE,
  AUDIT_FILE,
  TRASH_RETENTION_DAYS,
  HUB_FAMILY_EXTRAS,
  resolveHub,
  resolveHubDir,
  hubPaths,
  readHubState,
  writeHubState,
  readLinkState,
  writeLinkState,
  appendAudit,
  hashTree,
  moveEntryAcrossDevices,
  scanHubSkills,
  countHubSkills,
  syncHubState,
  familySlugSet,
  compareVersions,
  readSkillMeta,
  resolveTrashRoot,
  pruneTrash,
  BACKUP_RESIDUE_MARKERS,
  findBackupResidues,
  cleanupBackupResidues,
  trashRunStamp,
  safeHostName,
  listFamilyCopies,
  createDirLink,
  removeDirLink,
  classifyTarget,
  scanDirForHubLinks,
  linkSkills,
  unlinkSkills,
  removeSkills,
  linkStatus,
  status,
  doctor,
};
