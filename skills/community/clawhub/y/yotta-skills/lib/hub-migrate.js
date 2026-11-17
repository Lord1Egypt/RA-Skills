'use strict';
/**
 * Hub 迁移（0.29.2 U4；0.29.5 抽出共享内核）—— `hub config set --hub <new> --move`
 * 的两段式实现。
 *
 * 1) stageHubCopy({ from, to })：复制旧 Hub → 逐技能 treeHash 校验；失败
 *    fail-closed（清理暂存副本、旧 Hub 不动、配置不切换）。
 * 2) relinkAndRetireOldHub({ from, to, targets })：`hub link` 以新 Hub 为源、
 *    --force 重链各宿主 → 全部成功才把旧 Hub 移入回收站（7 天）；有失败则
 *    保留旧 Hub 供重试（此时新旧内容一致，链接混合指向两个 Hub 均可用）。
 *
 * 配置切换（config.json 写入）由调用方在两段之间执行；写入失败时调用
 * discardStagedCopy() 清理暂存副本。
 *
 * 0.29.5：runHubMigration() 把「复制 → 切配置 → 重链 → 旧 Hub 入回收站 → 记录
 * lastMigration」收成一个共享内核，CLI `hub config set --move` / `hub config
 * rollback` 与面板迁移向导 / 一键回滚共用，避免两套行为漂移。
 */
const fs = require('fs');
const path = require('path');
const hubLib = require('./hub');
const skillsConfigLib = require('./skills-config');

function nowStamp() {
  return new Date().toISOString().replace(/[:.]/g, '-');
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

function listEntries(dir) {
  try {
    return fs.readdirSync(dir);
  } catch (_) {
    return [];
  }
}

/** 空 Hub 台账残留：目标目录里只有元阁自己写过的空台账 / 审计文件。 */
const HUB_RESIDUE_FILES = new Set(['.yotta-hub.json', '.yotta-hub-audit.jsonl']);

/** 只读检查目标目录状态（迁移 fail-closed 判定 + 面板「清理残留并迁移」入口）。 */
function inspectTargetDir(dir) {
  const resolved = path.resolve(dir);
  const exists = fs.existsSync(resolved);
  const entries = exists ? listEntries(resolved) : [];
  const residueOnly = entries.length > 0 && entries.every((name) => HUB_RESIDUE_FILES.has(name));
  return {
    dir: resolved,
    exists,
    entries,
    empty: entries.length === 0,
    residueOnly,
    residueFiles: residueOnly ? entries : [],
  };
}

/** 把「空 Hub 台账残留」移入回收站（保留 7 天），返回 { ok, moved, trashDir }。 */
function clearTargetResidue(dir, options) {
  const opts = options || {};
  const resolved = path.resolve(dir);
  const state = inspectTargetDir(resolved);
  if (!state.residueOnly) return { ok: false, error: '目标目录不是空 Hub 台账残留：' + resolved };
  const trashRoot = hubLib.resolveTrashRoot(opts.hubDir || resolved, opts);
  const dest = path.join(trashRoot, 'hub-residue-' + nowStamp());
  const moved = [];
  try {
    fs.mkdirSync(dest, { recursive: true });
    for (const name of state.residueFiles) {
      const from = path.join(resolved, name);
      const to = path.join(dest, name);
      hubLib.moveEntryAcrossDevices(from, to);
      moved.push({ from, to });
    }
  } catch (error) {
    return { ok: false, error: '清理残留失败：' + error.message, moved, trashDir: dest };
  }
  return { ok: true, moved, trashDir: dest };
}

/** 清理暂存副本（仅在 stage 阶段失败或配置写入失败时调用）。 */
function discardStagedCopy(options) {
  const opts = options || {};
  const to = path.resolve(opts.to);
  try {
    if (opts.existed) {
      for (const name of listEntries(to)) fs.rmSync(path.join(to, name), { recursive: true, force: true });
    } else {
      fs.rmSync(to, { recursive: true, force: true });
    }
  } catch (_) { /* 保留现场供排查 */ }
}

/** 复制 + 校验（不切配置）。返回 { ok, error?, from, to, existed, verifiedSkills }。 */
function stageHubCopy(options) {
  const opts = options || {};
  const from = path.resolve(opts.from);
  const to = path.resolve(opts.to);
  if (samePath(from, to)) return { ok: false, error: '新旧 Hub 路径相同：' + from };
  if (isInside(from, to) || isInside(to, from)) return { ok: false, error: '新旧 Hub 不能互相嵌套：' + from + ' / ' + to };
  let stat = null;
  try {
    stat = fs.statSync(from);
  } catch (_) { /* handled below */ }
  if (!stat || !stat.isDirectory()) return { ok: false, error: '旧 Hub 不存在或不是目录：' + from };
  const existed = fs.existsSync(to);
  if (existed && listEntries(to).length > 0) {
    return { ok: false, error: '新 Hub 目录非空（fail-closed，不合并）：' + to };
  }

  try {
    fs.mkdirSync(to, { recursive: true });
    fs.cpSync(from, to, { recursive: true });
  } catch (error) {
    discardStagedCopy({ to, existed });
    return { ok: false, error: '复制失败：' + error.message };
  }

  const mismatches = [];
  for (const name of listEntries(from)) {
    if (!fs.existsSync(path.join(to, name))) mismatches.push('entry:' + name);
  }
  const skills = hubLib.scanHubSkills(from);
  for (const skill of skills) {
    let sourceStat = null;
    try {
      sourceStat = fs.lstatSync(skill.dir);
    } catch (_) {
      continue;
    }
    // in-place / 外部链接条目：随链接原样复制，不做内容校验。
    if (sourceStat.isSymbolicLink() || !isInside(from, skill.dir)) continue;
    const copied = path.join(to, path.relative(from, skill.dir));
    let copiedStat = null;
    try {
      copiedStat = fs.lstatSync(copied);
    } catch (_) { /* mismatch below */ }
    if (!copiedStat || !copiedStat.isDirectory()) {
      mismatches.push(skill.slug);
      continue;
    }
    try {
      if (hubLib.hashTree(skill.dir) !== hubLib.hashTree(copied)) mismatches.push(skill.slug);
    } catch (_) {
      mismatches.push(skill.slug);
    }
  }
  if (mismatches.length > 0) {
    discardStagedCopy({ to, existed });
    return {
      ok: false,
      error: '迁移校验失败（未切换配置；已清理暂存副本）：' + mismatches.slice(0, 8).join(', ') +
        (mismatches.length > 8 ? ' 等 ' + mismatches.length + ' 项' : ''),
    };
  }
  return { ok: true, from, to, existed, verifiedSkills: skills.length };
}

/** 重链（新 Hub 为源）+ 旧 Hub 入回收站（仅当重链无失败）。 */
function relinkAndRetireOldHub(options) {
  const opts = options || {};
  const from = path.resolve(opts.from);
  const to = path.resolve(opts.to);
  const targets = Array.isArray(opts.targets) ? opts.targets : [];
  const relink = [];
  let incomplete = 0;
  for (const target of targets) {
    if (!target || !target.dir) continue;
    if (samePath(target.dir, from) || samePath(target.dir, to)) continue;
    const result = hubLib.linkSkills({
      hubDir: to,
      targetDir: target.dir,
      agentId: target.agentId,
      label: target.label,
      force: true,
      manifest: opts.manifest,
      homeDir: opts.homeDir,
      env: opts.env,
    });
    const notLinked = result.results.filter((item) => item.status !== 'linked' && item.status !== 'missing');
    incomplete += notLinked.length;
    relink.push({
      dir: target.dir,
      label: target.label,
      linked: result.results.filter((item) => item.status === 'linked').length,
      incomplete: notLinked.map((item) => item.slug + ': ' + item.note),
    });
  }

  let trashedTo = null;
  let trashError = null;
  if (incomplete === 0) {
    try {
      const trashRoot = hubLib.resolveTrashRoot(from, { env: opts.env });
      const dest = path.join(trashRoot, 'hub-migrate-' + nowStamp(), path.basename(from));
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      hubLib.moveEntryAcrossDevices(from, dest);
      trashedTo = dest;
    } catch (error) {
      trashError = error.message;
    }
  }
  return { ok: incomplete === 0, from, to, relink, incomplete, trashedTo, trashError };
}

function classifyStageError(error) {
  const text = String(error || '');
  if (/非空/.test(text)) return 'target-non-empty';
  if (/嵌套/.test(text)) return 'target-nested';
  if (/相同/.test(text)) return 'target-same';
  return 'stage-failed';
}

/**
 * 共享迁移内核：stage → 切配置 → 重链 → 旧 Hub 入回收站 → 记录 lastMigration。
 *
 * options:
 * - from / to（必填）；targets（宿主目录数组；不传则不重链）
 * - configOpts（默认 { homeDir, env }）；manifest / homeDir / env
 * - via（'cli' | 'view'）；kind（'migrate' | 'rollback'）
 * - cleanResidue（true = 目标为空 Hub 台账残留时先移入回收站再迁移）
 *
 * 返回 { ok, phase, report?, error?, code?, stage?, finish? }；部分失败
 * （重链未全部完成）时旧 Hub 保留、report 记录 incomplete，绝不报成功。
 */
function runHubMigration(options) {
  const opts = options || {};
  const from = path.resolve(opts.from);
  const to = path.resolve(opts.to);
  const via = opts.via || 'cli';
  const kind = opts.kind === 'rollback' ? 'rollback' : 'migrate';
  const configOpts = opts.configOpts || { homeDir: opts.homeDir, env: opts.env };

  const oldHasContent = fs.existsSync(from) && listEntries(from).length > 0;
  if (!oldHasContent) {
    const setResult = skillsConfigLib.setHub(configOpts, { hub: to });
    if (!setResult.ok) return { ok: false, phase: 'config', error: setResult.error, code: 'config-failed' };
    return {
      ok: true,
      phase: 'done',
      switchedOnly: true,
      report: {
        moved: false,
        kind,
        from,
        to,
        at: new Date().toISOString(),
        reason: '旧 Hub 不存在或为空（' + from + '），仅切换指针',
        verifiedSkills: 0,
        relinkDirs: 0,
        incomplete: 0,
        trashedTo: null,
        trashError: null,
        oldHubKept: null,
        via,
      },
    };
  }

  let residue = null;
  const targetState = inspectTargetDir(to);
  if (targetState.residueOnly) {
    if (!opts.cleanResidue) {
      return {
        ok: false,
        phase: 'preflight',
        code: 'target-residue',
        error: '新 Hub 目录含空 Hub 台账残留（' + targetState.residueFiles.join('、') + '）：' + to +
          '。可勾选「清理残留并迁移」后重试。',
        target: targetState,
      };
    }
    residue = clearTargetResidue(to, { hubDir: from, env: opts.env });
    if (!residue.ok) return { ok: false, phase: 'preflight', code: 'residue-clean-failed', error: residue.error };
  }

  const staged = stageHubCopy({ from, to });
  if (!staged.ok) {
    return { ok: false, phase: 'stage', code: classifyStageError(staged.error), error: staged.error };
  }
  const setResult = skillsConfigLib.setHub(configOpts, { hub: to });
  if (!setResult.ok) {
    discardStagedCopy({ to, existed: staged.existed });
    return { ok: false, phase: 'config', code: 'config-failed', error: setResult.error };
  }
  const finish = relinkAndRetireOldHub({
    from,
    to,
    targets: opts.targets,
    manifest: opts.manifest,
    homeDir: opts.homeDir,
    env: opts.env,
  });
  const report = {
    moved: true,
    kind,
    from,
    to,
    at: new Date().toISOString(),
    verifiedSkills: staged.verifiedSkills,
    relinkDirs: finish.relink.length,
    relink: finish.relink,
    incomplete: finish.incomplete,
    trashedTo: finish.trashedTo,
    trashError: finish.trashError,
    oldHubKept: (finish.incomplete > 0 || finish.trashError) ? from : null,
    via,
  };
  skillsConfigLib.recordLastMigration(configOpts, report);
  return {
    ok: finish.ok,
    phase: finish.ok ? 'done' : 'relink',
    report,
    finish,
    residue,
  };
}

/** 回收站保留剩余天数（向上取整，最小 0；at 缺失按 0 天算）。 */
function trashDaysLeft(at, options) {
  const opts = options || {};
  const days = Number(opts.days) > 0 ? Number(opts.days) : hubLib.TRASH_RETENTION_DAYS;
  const started = Date.parse(at || '');
  if (!Number.isFinite(started)) return 0;
  const elapsedDays = Math.floor(Math.max(0, Date.now() - started) / (24 * 60 * 60 * 1000));
  return Math.max(0, days - elapsedDays);
}

/**
 * 回滚预览（只读）：当前 Hub → 上次迁移的原位置，反向迁移同内核。
 * 语义 = 位置回退（用当前内容，不丢迁移后改动），不是恢复旧快照。
 */
function previewRollback(options) {
  const opts = options || {};
  const configOpts = opts.configOpts || { homeDir: opts.homeDir, env: opts.env };
  const config = skillsConfigLib.readConfig(configOpts);
  const last = config.lastMigration;
  if (!last) {
    return { ok: false, code: 'no-migration', error: '没有可回滚的迁移记录（config.json 无 lastMigration）' };
  }
  const current = opts.currentDir
    ? { dir: path.resolve(opts.currentDir), source: opts.currentSource || 'flag' }
    : skillsConfigLib.resolveHub(configOpts);
  const target = inspectTargetDir(last.from);
  const blocked = [];
  if (!fs.existsSync(current.dir)) blocked.push('当前 Hub 不存在：' + current.dir);
  if (target.exists && !target.empty && !target.residueOnly) {
    blocked.push('回滚目标非空（fail-closed，不合并）：' + target.dir);
  }
  return {
    ok: blocked.length === 0,
    code: blocked.length ? 'rollback-blocked' : null,
    blocked,
    current: current.dir,
    target: target.dir,
    targetState: target,
    lastMigration: last,
    daysLeft: trashDaysLeft(last.at, opts),
    command: 'yotta-skills hub config rollback --yes',
  };
}

module.exports = {
  discardStagedCopy,
  stageHubCopy,
  relinkAndRetireOldHub,
  inspectTargetDir,
  clearTargetResidue,
  runHubMigration,
  previewRollback,
  trashDaysLeft,
  HUB_RESIDUE_FILES,
};
