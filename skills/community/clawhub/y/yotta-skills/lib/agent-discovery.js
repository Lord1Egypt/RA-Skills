'use strict';

/**
 * Local agent / skill-directory discovery.
 *
 * The discovery path is intentionally filesystem-first: it does not read the
 * memory registry or any YottaMeta state. It combines:
 *   1. known host mappings + documented environment overrides;
 *   2. bounded scans of common config / app-data roots;
 *   3. a lightweight installed-app marker scan for hosts that have no
 *      conventional skills directory.
 */

const fs = require('fs');
const os = require('os');
const path = require('path');
const agentDirs = require('./agent-dirs');
const hostsRegistry = require('./hosts-registry');

const SKILL_FILE = 'SKILL.md';
const SKIP_DIRS = new Set([
  '.git', 'node_modules', '__pycache__', '.pytest_cache', '.mypy_cache',
  '.venv', 'venv', 'site-packages', 'dist', 'build', 'out', 'coverage',
  'logs', 'log', 'tmp', 'temp', 'cache', '.cache', '.npm', '.cargo',
  '.rustup', '.nuget', '.gradle', '.m2', '.ssh',
]);
const AGENT_HINT = /(agent|claude|cursor|codex|opencode|openclaw|qclaw|trae|qwen|kimi|comate|codebuddy|workbuddy|dsh|deepseek|mimo|yotta|bionic|cherry|teleagent|dumate|cc.?switch|lmstudio|box|hermes|mavis|pi\b)/i;
const INSTALLED_NOISE = /(uninstall|updater|update|virtualbox|oracle|redistributable|runtime|driver)/i;

function envObject(options) {
  return (options && options.env) || process.env;
}

function homeDir(options) {
  return (options && options.homeDir) || os.homedir();
}

function isDirectory(dir) {
  try {
    return fs.statSync(dir).isDirectory();
  } catch (_) {
    return false;
  }
}

function safeReaddir(dir) {
  try {
    return fs.readdirSync(dir, { withFileTypes: true });
  } catch (_) {
    return [];
  }
}

function countSkills(dir) {
  let count = 0;
  for (const entry of safeReaddir(dir)) {
    if (!entry.isDirectory() && !entry.isSymbolicLink()) continue;
    const child = path.join(dir, entry.name);
    if (!isDirectory(child)) continue;
    try {
      if (fs.statSync(path.join(child, SKILL_FILE)).isFile()) count++;
    } catch (_) { /* not a standard skill directory */ }
  }
  return count;
}

function normalizePath(dir) {
  const resolved = path.resolve(dir);
  try {
    return fs.realpathSync.native(resolved);
  } catch (_) {
    return resolved;
  }
}

function isNoisePath(dir, baseDir) {
  const resolved = path.resolve(dir);
  const base = baseDir ? path.resolve(baseDir) : null;
  const relative = base && isInsidePath(base, resolved) ? path.relative(base, resolved) : resolved;
  const parts = relative.split(/[\\/]+/).filter(Boolean).map((part) => part.toLowerCase());
  for (const part of parts) {
    if (part === 'temp' || part === 'tmp') return true;
    if (/\.bak$/.test(part)) return true;
    if (part === 'plugin-sources' || part === 'plugins' || part === 'node_modules') return true;
    if (part === '.yottacode') return true;
    if (part === 'candidate' || part.startsWith('candidate-') || part.includes('staging')) return true;
    if (part === 'memories' || part === 'connectors' || part === 'workspace') return true;
  }
  return false;
}

function isInsidePath(root, target) {
  const relative = path.relative(path.resolve(root), path.resolve(target));
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

function addRoot(list, seen, dir, meta) {
  if (!dir) return;
  const resolved = path.resolve(dir);
  const key = normalizePath(resolved).toLowerCase();
  if (seen.has(key)) {
    const existing = seen.get(key);
    if (meta && meta.known && existing) existing.known = true;
    if (meta && meta.agentId && !existing.agentId) existing.agentId = meta.agentId;
    if (meta && meta.label && existing.label === '自动发现目录') existing.label = meta.label;
    if (meta && meta.verified) existing.verified = true;
    if (meta && meta.bridgeOnly) existing.bridgeOnly = true;
    // 用户注册优先：覆盖分类与手动标记（0.29.0 F2/F3）。
    if (meta && meta.registry) {
      existing.registry = true;
      existing.verified = true;
      existing.detection = 'user-registry';
      if (meta.label) existing.label = meta.label;
      if (meta.agentId) existing.agentId = meta.agentId;
      if (meta.manualState) existing.manualState = meta.manualState;
    }
    return;
  }
  const record = {
    dir: resolved,
    agentId: (meta && meta.agentId) || null,
    label: (meta && meta.label) || '自动发现目录',
    known: Boolean(meta && meta.known),
    env: Boolean(meta && meta.env),
    verified: Boolean(meta && meta.verified),
    bridgeOnly: Boolean(meta && meta.bridgeOnly),
    detection: (meta && meta.detection) || 'mapping',
    exists: isDirectory(resolved),
    registry: Boolean(meta && meta.registry),
    manualState: (meta && meta.manualState) || null,
  };
  record.skillCount = record.exists ? countSkills(resolved) : 0;
  record.status = record.exists ? 'skills-dir' : 'missing';
  seen.set(key, record);
  list.push(record);
}

/**
 * Bounded recursive scan for directories named "skills".
 * Only branches that look agent-related are followed after the first level.
 */
function scanForSkillDirs(root, options) {
  const maxDepth = (options && options.maxDepth) || 3;
  const maxVisits = (options && options.maxVisits) || 6000;
  const found = [];
  const queue = [{ dir: path.resolve(root), depth: 0 }];
  let visits = 0;

  while (queue.length > 0 && visits < maxVisits) {
    const current = queue.shift();
    if (!isDirectory(current.dir)) continue;
    visits++;
    const entries = safeReaddir(current.dir);
    for (const entry of entries) {
      if (SKIP_DIRS.has(entry.name)) continue;
      const full = path.join(current.dir, entry.name);
      if (/^skills$/i.test(entry.name)) {
        if (isDirectory(full) && !isNoisePath(full, options && options.baseDir)) found.push({ dir: full, parent: current.dir });
        continue;
      }
      if (current.depth >= maxDepth) continue;
      if (!entry.isDirectory() && !entry.isSymbolicLink()) continue;
      if (!isDirectory(full)) continue;
      const branchLooksRelevant = current.depth === 0
        || AGENT_HINT.test(entry.name)
        || AGENT_HINT.test(path.basename(current.dir));
      if (branchLooksRelevant) queue.push({ dir: full, depth: current.depth + 1 });
    }
  }
  return found;
}

function commonRoots(options) {
  const env = envObject(options);
  const home = homeDir(options);
  const roots = [];
  const add = (dir, depth) => {
    if (!dir) return;
    roots.push({ dir: path.resolve(dir), maxDepth: depth });
  };

  add(home, 2);
  add(env.APPDATA, 3);
  add(env.LOCALAPPDATA, 3);
  add(env.LOCALAPPDATA && path.join(env.LOCALAPPDATA, 'Programs'), 3);
  add(env.ProgramFiles, 2);
  add(env['ProgramFiles(x86)'], 2);
  add(env.XDG_CONFIG_HOME, 3);
  // XDG_STATE_HOME / XDG_DATA_HOME are lock / data bridges, not skill roots:
  // never scan them for link targets (see agent-dirs envRoots bridgeOnly).
  add(env.DSH_HOME, 3);
  add(env.DSH_AGENTS_HOME, 3);
  add(env.OPENCLAW_STATE_DIR, 2);
  add(env.CLAUDE_CONFIG_DIR, 2);
  add(env.CODEX_HOME, 2);
  // YOTTACODE_HOME 不扫描（YottaCode 自带三层技能管理，0.29.1 U2）。

  // A portable agent install often lives beside the current workspace. The
  // scanner only follows agent-looking branches, so this stays bounded.
  if (!options || (options.includeCwd !== false && String(env.YOTTA_SKILLS_DISCOVERY_NO_CWD || '') !== '1')) {
    let current = path.resolve(process.cwd());
    for (let depth = 0; depth < 3; depth++) {
      add(current, 2);
      const parent = path.dirname(current);
      if (parent === current) break;
      current = parent;
    }
  }
  return roots;
}

function collectMarkerNames(root, depth, output, maxEntries) {
  if (!root || depth < 0 || output.size >= maxEntries) return;
  for (const entry of safeReaddir(root)) {
    if (SKIP_DIRS.has(entry.name)) continue;
    if (/\.lnk$/i.test(entry.name)) {
      output.add(entry.name.replace(/\.lnk$/i, '').trim());
      continue;
    }
    if (entry.isDirectory() && depth > 0) {
      collectMarkerNames(path.join(root, entry.name), depth - 1, output, maxEntries);
    }
  }
}

function installedMarkers(options) {
  const env = envObject(options);
  const names = new Set();
  const roots = [
    env.APPDATA && path.join(env.APPDATA, 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
    env.ProgramData && path.join(env.ProgramData, 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
    env.APPDATA,
    env.LOCALAPPDATA,
    env.LOCALAPPDATA && path.join(env.LOCALAPPDATA, 'Programs'),
    env.ProgramFiles,
    env['ProgramFiles(x86)'],
  ];
  for (const root of roots) collectMarkerNames(root, 2, names, 800);
  // 标记过滤：已收录宿主的 label 双向匹配 + 启发式关键词；排除卸载器 / 运行时噪音。
  return [...names].filter((name) =>
    (knownLabelMatches(name) || AGENT_HINT.test(name)) && !INSTALLED_NOISE.test(name));
}

function normalizeLabel(value) {
  return String(value || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
}

/** 标记名与已收录宿主 label 的双向词边界包含（"Trae" ↔ "Trae Code CLI"）。 */
function knownLabelMatches(name) {
  const normalized = normalizeLabel(name);
  if (!normalized) return false;
  for (const info of Object.values(agentDirs.AGENT_DIRS)) {
    const label = normalizeLabel(info.label);
    if (!label) continue;
    if (normalized === label) return true;
    if (normalized.startsWith(label + ' ') || normalized.endsWith(' ' + label) || normalized.includes(' ' + label + ' ')) return true;
    if (label.startsWith(normalized + ' ') || label.endsWith(' ' + normalized) || label.includes(' ' + normalized + ' ')) return true;
  }
  return false;
}

/**
 * 应用标记与宿主匹配：label / agentId 与标记名按词边界双向包含。
 * 例："Claude" 匹配 "Claude Code"；"Trae" 匹配 "Trae Code CLI"；
 * 避免 "Pi" 误配 "Pilot" 这类裸子串。
 */
function markerMatchesHost(markerName, host) {
  const marker = normalizeLabel(markerName);
  if (!marker) return false;
  const candidates = [host && host.label, host && host.agentId].filter(Boolean).map(normalizeLabel);
  for (const candidate of candidates) {
    if (!candidate) continue;
    if (marker === candidate) return true;
    if (marker.startsWith(candidate + ' ') || marker.endsWith(' ' + candidate) || marker.includes(' ' + candidate + ' ')) return true;
    if (candidate.startsWith(marker + ' ') || candidate.endsWith(' ' + marker) || candidate.includes(' ' + marker + ' ')) return true;
  }
  return false;
}

/** F3 状态判定：目录 × 实体证据（应用标记 / 用户注册 / 手动标记）。 */
function judgeHostState(host) {
  if (host.manualState) return host.manualState; // 手动覆盖（available / orphan / ignored）
  const entity = Boolean(host.markerEvidence || (host.evidence && host.evidence.registry));
  if (host.exists && entity) return 'available';
  if (host.exists) return 'orphan';
  if (entity) return 'marker-only';
  return 'missing';
}

/**
 * 0.29.1 U2：installed 配对优先级 ——
 * user-registry / 目录覆盖 / 已核实映射 > env > 未核实映射 > 自动发现。
 */
function hostPairingPriority(host) {
  if (host.detection === 'user-registry' || host.registry) return 0;
  if (host.detection === 'override') return 1;
  if (host.verified && host.detection === 'mapping') return 1;
  if (host.detection === 'env') return 2;
  if (host.detection === 'mapping') return 3;
  return 4;
}

/** 同级按技能数降序 + 路径稳定排序（消除 last-write-wins）。 */
function compareHostCandidates(a, b) {
  const priority = hostPairingPriority(a) - hostPairingPriority(b);
  if (priority) return priority;
  const count = (b.skillCount || 0) - (a.skillCount || 0);
  if (count) return count;
  return String(a.dir).localeCompare(String(b.dir));
}

/**
 * Discover hosts and their skill directories.
 *
 * Returns:
 *   hosts    - all candidate skill roots (existing and missing known mappings)
 *   installed - entity evidence (app markers + user registry), including hosts
 *               without a skills dir; plain directory existence is NOT an
 *               installed marker (0.29.0 F3)
 *   errors   - non-fatal discovery errors
 */
function discoverHosts(options) {
  const roots = [];
  const seen = new Map();
  const errors = [];

  // 0.29.1 U2：用户级「不接管」名单 + 目录覆盖（hosts.json；旧文件向后兼容）。
  let registry = { hosts: [], excluded: [], overrides: [] };
  try {
    registry = hostsRegistry.readHostsRegistry(options);
  } catch (_) { /* registry 读取失败不影响发现 */ }
  const overridesByAgent = new Map(
    (registry.overrides || []).map((item) => [String(item.agentId).toLowerCase(), item]),
  );
  const previousDirKeys = new Set();
  for (const item of registry.overrides || []) {
    for (const prev of item.previousDirs || []) previousDirKeys.add(normalizePath(prev).toLowerCase());
  }
  // YottaCode 不接管：.yottacode 路径 + YOTTACODE_HOME 整棵子树（含任意自定义目录名）。
  const yottacodeHome = envObject(options).YOTTACODE_HOME
    ? path.resolve(envObject(options).YOTTACODE_HOME)
    : null;
  const isYottaCodePath = (dir) => {
    if (!dir) return false;
    if (agentDirs.isYottaCodeDir(dir)) return true;
    if (!yottacodeHome) return false;
    const resolved = path.resolve(dir);
    const relative = path.relative(yottacodeHome, resolved);
    return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
  };
  const isExcluded = (meta) => Boolean(hostsRegistry.excludedEntryFor(registry, meta || {}));
  const skipDir = (dir, agentId) => isYottaCodePath(dir) || isExcluded({ dir, agentId });

  for (const root of agentDirs.knownRoots(options)) {
    const override = root.agentId ? overridesByAgent.get(String(root.agentId).toLowerCase()) : null;
    if (override) {
      if (skipDir(override.dir, root.agentId)) continue;
      addRoot(roots, seen, override.dir, {
        ...root,
        label: override.label || root.label,
        verified: true,
        detection: 'override',
      });
      continue;
    }
    if (skipDir(root.dir, root.agentId)) continue;
    addRoot(roots, seen, root.dir, { ...root, detection: 'mapping' });
  }
  for (const root of agentDirs.envRoots(options)) {
    if (skipDir(root.dir, root.agentId)) continue;
    addRoot(roots, seen, root.dir, { ...root, detection: root.env ? 'env' : 'workspace' });
  }
  // 合并顺序：内置映射 → 环境变量 → 用户注册表（F2）→ 自动发现；
  // 同 realpath 用户注册优先（分类 = 已核实，detection = user-registry）。
  for (const item of registry.hosts || []) {
    if (skipDir(item.dir, item.agentId)) continue;
    addRoot(roots, seen, item.dir, {
      detection: 'user-registry',
      label: item.label || '自定义宿主',
      agentId: item.agentId || null,
      verified: true,
      known: false,
      registry: true,
      manualState: item.manualState || null,
    });
  }
  for (const root of commonRoots(options)) {
    for (const found of scanForSkillDirs(root.dir, {
      maxDepth: root.maxDepth,
      baseDir: options.homeDir || os.homedir(),
    })) {
      if (skipDir(found.dir, null)) continue;
      // 被目录覆盖替换掉的旧映射目录不再进入默认发现 / 链接。
      if (previousDirKeys.has(normalizePath(found.dir).toLowerCase())) continue;
      addRoot(roots, seen, found.dir, {
        detection: 'discovered',
        label: '自动发现：' + path.basename(found.parent),
      });
    }
  }

  // F3：目录证据与实体证据分开记录，判定生命周期状态。
  const markers = installedMarkers(options);
  for (const host of roots) {
    const markerEvidence = markers.some((name) => markerMatchesHost(name, host));
    host.markerEvidence = markerEvidence;
    host.dirEvidence = host.exists;
    host.evidence = {
      dir: host.exists,
      marker: markerEvidence,
      registry: Boolean(host.registry),
      manual: Boolean(host.manualState),
    };
    host.stateSource = host.manualState ? 'manual' : 'auto';
    host.state = judgeHostState(host);
  }

  const installed = [];
  const installedSeen = new Set();
  const addInstalled = (name, source) => {
    const label = String(name || '').trim();
    if (!label) return;
    const key = label.toLowerCase();
    if (installedSeen.has(key)) return;
    installedSeen.add(key);
    installed.push({ label, source, hasSkillsDir: false });
  };
  // 0.29.1 U2：不接管（excluded）/ neverLink（YottaCode）宿主的应用标记同样跳过显示。
  const isMarkerSuppressed = (name) => {
    for (const [agentId, info] of Object.entries(agentDirs.AGENT_DIRS)) {
      if (!info.neverLink) continue;
      if (markerMatchesHost(name, { agentId, label: info.label })) return true;
    }
    return (registry.excluded || []).some((item) => {
      if (item.kind !== 'agent') return false;
      const info = agentDirs.AGENT_DIRS[String(item.value).toLowerCase()] || {};
      return markerMatchesHost(name, { agentId: item.value, label: info.label || item.value });
    });
  };
  for (const name of markers) {
    if (isMarkerSuppressed(name)) continue;
    if (knownLabelMatches(name) || AGENT_HINT.test(name)) addInstalled(name, '应用标记');
  }
  for (const host of roots) {
    if (host.detection === 'user-registry') addInstalled(host.label, '用户注册');
  }
  // 0.29.1 U2：配对确定性优选（先收集全部候选，再按优先级选定），消除 last-write-wins。
  const pairCandidates = new Map();
  for (const host of roots) {
    if (!host.exists) continue;
    if (!host.markerEvidence && host.detection !== 'user-registry') continue;
    for (const item of installed) {
      if (!markerMatchesHost(item.label, host)) continue;
      if (!pairCandidates.has(item)) pairCandidates.set(item, []);
      pairCandidates.get(item).push(host);
    }
  }
  for (const [item, hosts] of pairCandidates) {
    hosts.sort(compareHostCandidates);
    const host = hosts[0];
    item.hasSkillsDir = true;
    item.skillDir = host.dir;
    item.skillCount = host.skillCount;
    item.agentId = host.agentId;
  }

  return {
    generatedAt: new Date().toISOString(),
    hosts: roots,
    installed,
    errors,
  };
}

/**
 * 0.29.1 U2：未配对且无技能目录的已安装标记（CLI / 面板共用单一真源）。
 * 已配对（hasSkillsDir）或 label 与已显示宿主重复的标记不再出现在「无技能目录」区。
 */
function unpairedMarkers(discovery) {
  const shown = new Set();
  for (const host of (discovery && discovery.hosts) || []) {
    if (host.exists || host.state === 'marker-only') shown.add(String(host.label).toLowerCase());
  }
  return ((discovery && discovery.installed) || []).filter((item) =>
    !item.hasSkillsDir && !shown.has(String(item.label).toLowerCase()));
}

module.exports = {
  AGENT_HINT,
  discoverHosts,
  scanForSkillDirs,
  countSkills,
  markerMatchesHost,
  judgeHostState,
  unpairedMarkers,
};
