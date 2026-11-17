'use strict';
/**
 * 残留目录清理核心（0.29.0 F3）：CLI 与面板共用。
 *
 * 只处理 state=orphan 的宿主目录 —— 全量 unlink（只删指向 Hub 的链接，含死链）
 * → 目录移入回收站（保留 7 天，跨卷走复制 + 校验 + 删源）→ 清注册 / 链接台账
 * → 写审计。非 Hub 链接 / 非链接内容保留并报告。
 *
 * fail-closed：Hub 真源 / 子目录、锁与数据桥接目录、非残留状态（可用 / 仅标记 /
 * 未创建 / 已忽略）一律拒绝；需要人工确认时先 hub hosts mark --state orphan。
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const hubLib = require('./hub');
const agentDirsLib = require('./agent-dirs');
const agentDiscoveryLib = require('./agent-discovery');
const hostsRegistryLib = require('./hosts-registry');

function purgeStamp(now) {
  const d = now instanceof Date ? now : new Date();
  const pad = (value) => String(value).padStart(2, '0');
  return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()) + '-' +
    pad(d.getHours()) + pad(d.getMinutes()) + pad(d.getSeconds()) + '-' + process.pid;
}

function safeOrphanName(value) {
  const cleaned = String(value || '')
    .replace(/[\\/:*?"<>|\s]+/g, '-')
    .replace(/^-+|-+$/g, '');
  return cleaned || 'host';
}

function pathKey(dir) {
  let real = path.resolve(dir);
  try {
    real = fs.realpathSync.native(real);
  } catch (_) {
    try { real = fs.realpathSync(real); } catch (_) { /* keep resolved */ }
  }
  return process.platform === 'win32' ? real.toLowerCase() : real;
}

function isInside(root, target) {
  const relative = path.relative(path.resolve(root), path.resolve(target));
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

/** 只读预检 + 清理计划（不写任何文件）。 */
function planHostPurge(options) {
  const opts = options || {};
  const hubDir = path.resolve(opts.hubDir);
  const target = path.resolve(opts.dir);
  const homeDir = opts.homeDir || os.homedir();
  const env = opts.env || process.env;

  if (!fs.existsSync(target)) {
    return { ok: false, code: 400, error: '目录不存在: ' + target };
  }
  if (isInside(hubDir, target)) {
    return { ok: false, code: 400, error: '该目录不允许残留清理（Hub 真源 / 子目录）: ' + target };
  }
  if (agentDirsLib.isBridgeOnlyDir(target, { homeDir, env })) {
    return { ok: false, code: 400, error: '锁 / 数据桥接目录不参与残留清理: ' + target };
  }

  const discovery = opts.discovery || agentDiscoveryLib.discoverHosts({ homeDir, env });
  const host = discovery.hosts.find((item) => pathKey(item.dir) === pathKey(target));
  const state = host ? host.state : null;
  if (state !== 'orphan') {
    return {
      ok: false,
      code: 400,
      state,
      error: '目标不是「残留（实体未确认）」状态' + (state ? '（当前: ' + state + '）' : '（不在发现列表）'),
    };
  }

  const linkSlugs = [];
  let keptLinks = 0;
  let keptEntries = 0;
  let entries = [];
  try { entries = fs.readdirSync(target, { withFileTypes: true }); } catch (_) { entries = []; }
  for (const entry of entries) {
    const full = path.join(target, entry.name);
    const cls = hubLib.classifyTarget(full, hubDir);
    if (cls.kind === 'link') {
      if (cls.inHub) linkSlugs.push(entry.name);
      else keptLinks++;
    } else if (cls.kind !== 'missing') {
      keptEntries++;
    }
  }
  const trashRoot = hubLib.resolveTrashRoot(hubDir, opts);
  const label = host && host.label ? host.label : path.basename(target);
  const trashPath = path.join(trashRoot, purgeStamp(opts.now), 'orphan-' + safeOrphanName(label));
  return {
    ok: true,
    hubDir,
    target,
    state,
    label,
    linkSlugs,
    keptLinks,
    keptEntries,
    trashRoot,
    trashPath,
  };
}

/** 执行清理：unlink → trash → 清注册 / 台账 → 审计。 */
function applyHostPurge(options) {
  const opts = options || {};
  const plan = planHostPurge(opts);
  if (!plan.ok) return plan;

  const unlinkResult = hubLib.unlinkSkills({
    hubDir: plan.hubDir,
    targetDir: plan.target,
    slugs: plan.linkSlugs,
    dryRun: false,
  });
  const unlinkedCount = (unlinkResult.results || [])
    .filter((item) => item.status === 'unlinked').length;

  fs.mkdirSync(path.dirname(plan.trashPath), { recursive: true });
  hubLib.moveEntryAcrossDevices(plan.target, plan.trashPath);
  try {
    hubLib.pruneTrash(plan.trashRoot, { days: hubLib.TRASH_RETENTION_DAYS });
  } catch (_) { /* best-effort */ }

  const registryOpts = { homeDir: opts.homeDir, env: opts.env, hub: opts.hub };
  const registry = hostsRegistryLib.readHostsRegistry(registryOpts);
  if (registry.hosts.some((item) => pathKey(item.dir) === pathKey(plan.target))) {
    hostsRegistryLib.removeHost(registryOpts, { dir: plan.target });
  }

  try {
    hubLib.appendAudit(plan.hubDir, {
      event: 'hosts.purge',
      dir: plan.target,
      label: plan.label,
      state: plan.state,
      trashedTo: plan.trashPath,
      unlinked: unlinkedCount,
      keptLinks: plan.keptLinks,
      keptEntries: plan.keptEntries,
    });
  } catch (_) { /* 审计失败不阻断 */ }

  return {
    ok: true,
    dir: plan.target,
    state: plan.state,
    unlinkCount: unlinkedCount,
    keptLinks: plan.keptLinks,
    keptEntries: plan.keptEntries,
    trashedTo: plan.trashPath,
  };
}

module.exports = {
  planHostPurge,
  applyHostPurge,
  purgeStamp,
  safeOrphanName,
};
