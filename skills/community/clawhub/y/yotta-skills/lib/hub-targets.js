'use strict';
/**
 * Hub 链接目标范围（0.29.5）—— `hub link --all` 与面板迁移向导 / 一键回滚的
 * 重链范围共用同一真源，避免 CLI 与面板两套范围漂移。
 *
 * 默认范围 = 通用目录（Universal .agents / 通用 AGENTS.md）+ 已核实宿主目录；
 * `includeDiscovered` 显式纳入自动发现目录；桥接目录永不纳入（发现层已过滤
 * 不接管名单与 YottaCode）。
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const agentDirsLib = require('./agent-dirs');
const hostsRegistryLib = require('./hosts-registry');

function normalizeTargetKey(dir) {
  const resolved = path.resolve(dir);
  let real = resolved;
  try {
    real = fs.realpathSync.native(resolved);
  } catch (_) { /* missing path: fall back to the resolved spelling */ }
  return process.platform === 'win32' ? real.toLowerCase() : real;
}

/** 通用技能目录（与旧 CLI universalSkillDirs 同源）。 */
function universalSkillDirs(options) {
  const opts = options || {};
  const home = opts.homeDir || os.homedir();
  const env = opts.env || process.env;
  const xdg = env.XDG_CONFIG_HOME || path.join(home, '.config');
  return [
    { dir: path.join(xdg, 'agents', 'skills'), agentId: 'universal', label: 'Universal .agents' },
    { dir: path.join(home, '.agents', 'skills'), agentId: 'agents', label: '通用 AGENTS.md' },
  ];
}

/**
 * 计算 --all 范围目标（只读；不创建目录、不链接）。
 * options: { discovery, registry, homeDir, env, includeDiscovered }
 */
function computeHubTargets(options) {
  const opts = options || {};
  const discovery = opts.discovery || { hosts: [] };
  const homeDir = opts.homeDir || os.homedir();
  const env = opts.env || process.env;
  const registry = opts.registry || hostsRegistryLib.readHostsRegistry({ homeDir, env });
  const excludedEntry = (input) => hostsRegistryLib.excludedEntryFor(registry, input);
  const targets = [];
  const seen = new Set();
  const add = (dir, agentId, label, meta) => {
    if (!dir) return;
    const resolved = path.resolve(dir);
    const key = normalizeTargetKey(resolved);
    if (seen.has(key)) return;
    seen.add(key);
    targets.push({
      dir: resolved,
      agentId: agentId || null,
      label: label || '指定目录',
      verified: Boolean(meta && meta.verified),
      bridgeOnly: Boolean(meta && meta.bridgeOnly),
      detection: (meta && meta.detection) || 'mapping',
      explicit: Boolean(meta && meta.explicit),
    });
  };

  for (const item of universalSkillDirs({ homeDir, env })) {
    if (agentDirsLib.isYottaCodeDir(item.dir)) continue;
    if (excludedEntry({ dir: item.dir, agentId: item.agentId })) continue;
    add(item.dir, item.agentId, item.label, { verified: true });
  }
  for (const host of discovery.hosts || []) {
    if (!host.exists) continue;
    if (host.bridgeOnly) continue;
    if (!opts.includeDiscovered && !host.verified) continue;
    add(host.dir, host.agentId, host.label, host);
  }
  return targets;
}

module.exports = {
  normalizeTargetKey,
  universalSkillDirs,
  computeHubTargets,
};
