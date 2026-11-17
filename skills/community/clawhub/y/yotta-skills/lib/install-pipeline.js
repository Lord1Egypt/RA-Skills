'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');
const manifestLib = require('./manifest');
const gateLib = require('./verify-gate');
const lifecycleLib = require('./install-lifecycle');
const healthLib = require('./install-health');
const snapshotLib = require('./install-snapshot');
const hookAdapterLib = require('./hook-adapter');
const scanLib = require('./skills-scan');
const linkSafety = require('./link-safety');

function nowTag() {
  return new Date().toISOString().replace(/[:.]/g, '-');
}

function sleepSync(ms) {
  const array = new Int32Array(new SharedArrayBuffer(4));
  Atomics.wait(array, 0, 0, ms);
}

function renameWithRetry(from, to, options) {
  const rename = (options && options.rename) || fs.renameSync;
  const sleep = (options && options.sleep) || sleepSync;
  let lastError;
  for (let attempt = 0; attempt < 5; attempt++) {
    try {
      return rename(from, to);
    } catch (error) {
      lastError = error;
      if (!['EPERM', 'EACCES', 'EBUSY'].includes(error.code) || attempt === 4) throw error;
      sleep(100 * (attempt + 1));
    }
  }
  throw lastError;
}

function isSafeTarEntry(entry) {
  const value = String(entry || '').replace(/\\/g, '/');
  if (value !== 'package' && !value.startsWith('package/')) return false;
  if (value.startsWith('/') || /^[A-Za-z]:\//.test(value)) return false;
  return !value.split('/').includes('..');
}

function copyTree(src, dst, copyDir) {
  fs.rmSync(dst, { recursive: true, force: true });
  fs.mkdirSync(dst, { recursive: true });
  copyDir(src, dst);
}

function restoreBackup(target, backup, hadTarget) {
  if (backup && fs.existsSync(backup)) {
    if (fs.existsSync(target)) fs.rmSync(target, { recursive: true, force: true });
    renameWithRetry(backup, target);
    return true;
  }
  if (!hadTarget && fs.existsSync(target)) {
    fs.rmSync(target, { recursive: true, force: true });
    return true;
  }
  return false;
}

/** 暂存子目录超过 1 小时视为崩溃残留（并发安装的暂存目录总是新鲜的）。 */
const STAGING_STALE_MS = 60 * 60 * 1000;

/** 清理目标目录 `.yottaskills-staging` 中的陈旧暂存（best-effort，返回清理数）。 */
function pruneStaleStaging(stagingRoot, options) {
  const opts = options || {};
  const now = opts.now instanceof Date ? opts.now.getTime() : Date.now();
  let entries;
  try {
    entries = fs.readdirSync(stagingRoot, { withFileTypes: true });
  } catch (_) {
    return 0;
  }
  let pruned = 0;
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const full = path.join(stagingRoot, entry.name);
    let stat;
    try {
      stat = fs.statSync(full);
    } catch (_) {
      continue;
    }
    if (now - stat.mtimeMs > STAGING_STALE_MS) {
      try {
        fs.rmSync(full, { recursive: true, force: true });
        pruned += 1;
      } catch (_) { /* 保留供下次清理 */ }
    }
  }
  return pruned;
}

/** 0.29.1 U1「只升不降」跳过原因文案（equal / local-ahead / unknown）。 */
function versionSkipNote(relation, installed, target) {
  if (relation === 'equal') return '已是最新';
  if (relation === 'local-ahead') {
    return '本地领先 v' + installed + ' > 目标 v' + target + '，保留不降级（--force 可强制）';
  }
  return '无法比较版本（本地 v' + installed + ' / 目标 v' + target + '），保留（--force 可强制）';
}

function createInstaller(deps) {
  const homeDir = deps.homeDir || os.homedir();
  const runPhase = deps.runPhase || lifecycleLib.runPhase;
  const checkInstalledSkill = deps.checkInstalledSkill || healthLib.checkInstalledSkill;
  const captureSnapshot = deps.createSnapshot || snapshotLib.createSnapshot;
  const evaluateHook = deps.evaluateHook || hookAdapterLib.evaluateHook;
  const appendHookEvidence = deps.appendHookEvidence || hookAdapterLib.appendHookEvidence;

  function record(entry) {
    return deps.appendEvidence(entry, { homeDir });
  }

  function safeRecord(entry) {
    try {
      return record(entry);
    } catch (_) {
      return null;
    }
  }

  return function installOne(skill, dest, opts) {
    const target = path.join(dest, skill.slug);
    let resolvedTarget;
    try {
      resolvedTarget = linkSafety.resolveInstallTarget(target, skill.slug);
    } catch (error) {
      safeRecord({ event: 'install', skill: skill.slug, decision: 'block', error: error.message });
      return { skill, status: 'fail', version: null, note: error.message, exitCode: 4 };
    }
    const installTarget = resolvedTarget.target;
    const workDir = path.dirname(installTarget);
    const existingVersion = deps.readInstalledVersion(installTarget);
    // 0.29.1 U1「只升不降」：pin 模式目标即最终版本，入口即可判定；
    // range / latest 模式（目标非最终版本）在 npm pack 解析出精确版本后复判（见下方）。
    const relation = scanLib.versionRelation(existingVersion, skill.version);
    if (!opts.force && opts.pin !== false &&
        (relation === 'equal' || relation === 'local-ahead' || relation === 'unknown')) {
      return {
        skill,
        status: 'skip',
        version: existingVersion,
        note: versionSkipNote(relation, existingVersion, skill.version),
        exitCode: 0,
      };
    }
    if (opts.dryRun) {
      // 0.29.0 D1：只读预览 —— 不发网络请求、不写任何文件（含台账）。
      const latestUnresolved = skill.version === 'latest';
      const planned = existingVersion ? 'update' : 'install';
      return {
        skill,
        status: 'planned',
        planned,
        version: latestUnresolved ? 'latest' : skill.version,
        installedVersion: existingVersion,
        latestUnresolved,
        note: latestUnresolved
          ? 'latest（预览不解析）'
          : planned === 'update'
            ? '将更新 v' + existingVersion + ' -> v' + skill.version
            : '将安装 v' + skill.version,
        exitCode: 0,
      };
    }

    let tmp = null;
    let staged = null;
    let stagingRoot = null;
    let snapshot = null;
    let backup = null;
    const hadTarget = fs.existsSync(installTarget);
    let manifest = null;
    let extracted = null;
    let lifecycle = { setup: null, builtin_doctor: null, doctor: null, rollback: null };
    try {
      tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'yotta-skills-'));
      const packDir = path.join(tmp, 'pack');
      fs.mkdirSync(packDir, { recursive: true });
      const packed = deps.runNpmPack(skill, opts, packDir);
      if (packed.error) {
        safeRecord({ event: 'before_install', skill: skill.slug, decision: 'fail', error: packed.error });
        return { skill, status: 'fail', version: null, note: packed.error, exitCode: 1 };
      }

      // 0.29.1 U1：解析出精确版本后、任何解压 / 快照 / 写入之前复判（latest / range 路径）。
      const resolvedVersion = packed.resolved || (skill.version === 'latest' ? null : skill.version);
      if (!opts.force && existingVersion) {
        const resolvedRelation = resolvedVersion
          ? scanLib.versionRelation(existingVersion, resolvedVersion)
          : 'unknown';
        if (resolvedRelation === 'equal' || resolvedRelation === 'local-ahead' || resolvedRelation === 'unknown') {
          return {
            skill,
            status: 'skip',
            version: existingVersion,
            note: versionSkipNote(resolvedRelation, existingVersion, resolvedVersion || skill.version),
            exitCode: 0,
          };
        }
      }

      const extractDir = path.join(tmp, 'extract');
      fs.mkdirSync(extractDir, { recursive: true });
      extracted = deps.extractTarball(packed.tarball, extractDir);
      if (extracted.error) {
        safeRecord({ event: 'before_install', skill: skill.slug, decision: 'fail', error: extracted.error });
        return { skill, status: 'fail', version: packed.resolved, note: extracted.error, exitCode: 1 };
      }

      const resolvedSkill = { ...skill, version: packed.resolved || skill.version };
      const loaded = manifestLib.loadManifest({ pkgDir: extracted.pkgDir, skill: resolvedSkill });
      if (loaded.errors.length > 0) {
        const note = loaded.errors.join('; ');
        safeRecord({ event: 'manifest', skill: skill.slug, decision: 'block', errors: loaded.errors });
        return { skill, status: 'fail', version: packed.resolved, note, exitCode: 6 };
      }
      manifest = loaded.manifest;
      if (manifest.trust !== 'yottameta') {
        safeRecord({
          event: 'manifest',
          skill: skill.slug,
          decision: 'block',
          errors: ['trust 必须为 yottameta'],
        });
        return {
          skill,
          status: 'fail',
          version: packed.resolved,
          note: 'manifest trust 必须为 yottameta',
          exitCode: 6,
        };
      }

      let gate;
      let scan;
      if (opts.skipScan) {
        gate = { ok: true, engine: null, mode: 'explicit-unverified' };
        scan = { decision: 'unverified', verdict: null, counts: null, warn: true, mode: 'explicit-unverified' };
      } else {
        gate = deps.ensureGate({ skill, extracted, dest, opts });
        if (!gate.ok) {
          safeRecord({ event: 'before_install', skill: skill.slug, decision: 'block', error: gate.error });
          return { skill, status: 'fail', version: packed.resolved, note: gate.error, exitCode: 5 };
        }
        const scanResult = deps.scanTarget(gate.engine, extracted.pkgDir, {
          slug: skill.slug,
          version: packed.resolved,
          opts,
        });
        if (!scanResult.ok) {
          safeRecord({ event: 'before_install', skill: skill.slug, decision: 'block', error: scanResult.error });
          return { skill, status: 'fail', version: packed.resolved, note: scanResult.error, exitCode: 5 };
        }
        const verdict = gateLib.evaluateVerdict(scanResult.verdict);
        let hookEvaluation = { decision: 'allow', evidence: [], user_message: '无 hook 声明' };
        try {
          hookEvaluation = evaluateHook({
            host: opts.host || 'codex',
            event: 'before_install',
            manifest,
            capabilities: deps.hookCapabilities || hookAdapterLib.capabilitiesForHost(opts.host || 'codex'),
            context: opts.skipScan
              ? { wrapperRegistered: false, checks: {} }
              : {
                  wrapperRegistered: true,
                  checks: {
                    scan_skill: {
                      ok: !verdict.block,
                      evidence: { audit_log: 'install-log.jsonl' },
                    },
                  },
                },
          });
          for (const entry of hookEvaluation.evidence) {
            appendHookEvidence(entry, { homeDir });
          }
        } catch (error) {
          hookEvaluation = {
            decision: 'block',
            evidence: [],
            user_message: 'hook 适配器失败: ' + error.message,
          };
        }
        if (verdict.block || hookEvaluation.decision === 'block') {
          const hookReason = hookEvaluation.decision === 'block'
            ? 'before_install hook 阻断: ' + hookEvaluation.user_message
            : '元信 verdict: ' + scanResult.verdict;
          safeRecord({
            event: 'before_install',
            skill: skill.slug,
            decision: 'block',
            verdict: scanResult.verdict,
            counts: scanResult.counts,
            scan_policy: scanResult.policy || null,
            hook_decision: hookEvaluation.decision,
          });
          return {
            skill,
            status: 'fail',
            version: packed.resolved,
            note: hookReason,
            exitCode: 5,
          };
        }
        scan = {
          decision: verdict.decision,
          verdict: scanResult.verdict,
          counts: scanResult.counts,
          warn: verdict.warn,
          policy: scanResult.policy || null,
        };
      }

      fs.mkdirSync(workDir, { recursive: true });
      stagingRoot = path.join(workDir, '.yottaskills-staging');
      fs.mkdirSync(stagingRoot, { recursive: true });
      pruneStaleStaging(stagingRoot);
      staged = fs.mkdtempSync(path.join(stagingRoot, skill.slug + '-'));
      // Hub installs keep declared runtime payload (e.g. yotta-skills bin):
      // hosts linked to the Hub then inherit the runtime files (OpenCode contract).
      // 0.29.5 S4：`--dir` 托管目录更新保持既有运行时载荷（目标已带 bin/ 等 → 继续携带），
      // 防更新后引擎缺 bin；新装 / 普通技能目录仍只落本体（§6.3 口径不变）。
      let runtimePayload = [];
      if (Array.isArray(resolvedSkill.runtimePayload) && resolvedSkill.runtimePayload.length > 0) {
        if (opts.hubScope) {
          runtimePayload = resolvedSkill.runtimePayload;
        } else if (hadTarget) {
          const carriesPayload = resolvedSkill.runtimePayload
            .some((name) => fs.existsSync(path.join(installTarget, name)));
          if (carriesPayload) runtimePayload = resolvedSkill.runtimePayload;
        }
      }
      const copyWithRuntime = (src, dst) => deps.copyDir(src, dst, { keep: runtimePayload });
      copyTree(extracted.pkgDir, staged, copyWithRuntime);

      if (fs.existsSync(installTarget)) {
        const captured = captureSnapshot(installTarget, {
          homeDir,
          slug: skill.slug,
          version: existingVersion || 'unknown',
          copyDir: copyWithRuntime,
        });
        snapshot = captured.path;
        backup = path.join(workDir, '.yottaskills-backup-' + skill.slug + '-' + process.pid);
        renameWithRetry(installTarget, backup);
      }

      renameWithRetry(staged, installTarget);
      staged = null;

      function lifecycleSummary(result) {
        if (!result) return null;
        return {
          ok: !!result.ok,
          skipped: !!result.skipped,
          error: result.error || null,
          result: result.result || null,
        };
      }

      function rollbackAfterFailure(reason, phase) {
        let restoreError = null;
        let rollbackResult = { ok: false, skipped: true, error: null, result: null };
        try {
          restoreBackup(installTarget, backup, hadTarget);
          backup = null;
        } catch (error) {
          restoreError = error.message;
        }
        try {
          const rollbackPhase = runPhase(extracted.pkgDir, manifest, 'rollback', {
            skillDir: installTarget,
            packageDir: extracted.pkgDir,
            dest,
            snapshot,
          });
          if (!rollbackPhase.skipped) rollbackResult = rollbackPhase;
        } catch (error) {
          rollbackResult = { ok: false, skipped: false, error: error.message, result: null };
        }
        lifecycle.rollback = lifecycleSummary(rollbackResult);
        const rollbackError = restoreError || (rollbackResult.ok || rollbackResult.skipped ? null : rollbackResult.error);
        safeRecord({
          event: 'rollback',
          skill: skill.slug,
          package: skill.pkg,
          version: packed.resolved || skill.version,
          decision: rollbackError ? 'fail' : 'ok',
          phase,
          reason,
          restore_error: restoreError,
          rollback_error: rollbackResult.ok || rollbackResult.skipped ? null : rollbackResult.error,
          snapshot,
        });
        return {
          skill,
          status: 'fail',
          version: packed.resolved || skill.version,
          note: reason + (rollbackError ? '；回滚失败: ' + rollbackError : ''),
          exitCode: 1,
          snapshot,
          lifecycle,
          rollback_reason: reason,
        };
      }

      lifecycle.setup = runPhase(extracted.pkgDir, manifest, 'setup', {
        skillDir: installTarget,
        packageDir: extracted.pkgDir,
        dest,
        snapshot,
      });
      if (!lifecycle.setup.ok) {
        return rollbackAfterFailure('setup 失败: ' + lifecycle.setup.error, 'setup');
      }

      lifecycle.builtin_doctor = checkInstalledSkill({
        slug: skill.slug,
        target: installTarget,
        expectedVersion: packed.resolved || skill.version,
        expectedPackage: skill.pkg,
      });
      if (!lifecycle.builtin_doctor.ok) {
        return rollbackAfterFailure(
          '内置 doctor 失败: ' + lifecycle.builtin_doctor.errors.join('; '),
          'builtin-doctor',
        );
      }

      lifecycle.doctor = runPhase(extracted.pkgDir, manifest, 'doctor', {
        skillDir: installTarget,
        packageDir: extracted.pkgDir,
        dest,
        snapshot,
      });
      if (!lifecycle.doctor.ok) {
        return rollbackAfterFailure('doctor 失败: ' + lifecycle.doctor.error, 'doctor');
      }

      let evidence;
      try {
        evidence = record({
          event: 'before_install',
          skill: skill.slug,
          package: skill.pkg,
          version: packed.resolved || skill.version,
          gate_mode: gate.mode,
          bootstrap_scan: gate.mode === 'trusted-bootstrap' && skill.slug === 'yotta-verify' ? 'self' : null,
          verdict: scan.verdict,
          decision: scan.decision,
          scan_policy: scan.policy || null,
          fetch_channel: packed.channel || null,
          extract_channel: extracted.channel || null,
          npm_registry_fallback: Boolean(packed.registryFallback),
          snapshot,
        });
      } catch (error) {
        return rollbackAfterFailure('证据写入失败: ' + error.message, 'evidence');
      }

      safeRecord({
        event: 'after_install',
        skill: skill.slug,
        package: skill.pkg,
        version: packed.resolved || skill.version,
        decision: 'allow',
        fetch_channel: packed.channel || null,
        extract_channel: extracted.channel || null,
        snapshot,
        lifecycle: {
          setup: lifecycleSummary(lifecycle.setup),
          builtin_doctor: lifecycleSummary(lifecycle.builtin_doctor),
          doctor: lifecycleSummary(lifecycle.doctor),
        },
      });

      if (backup && fs.existsSync(backup)) {
        try {
          fs.rmSync(backup, { recursive: true, force: true });
        } catch (_) {
          // The new version is already active; a stale backup is safer than a failed install.
        }
        backup = null;
      }

      return {
        skill,
        status: 'ok',
        version: packed.resolved || skill.version,
        note: null,
        gate: { ...scan, mode: gate.mode },
        evidence,
        snapshot,
        lifecycle,
        exitCode: 0,
      };
    } catch (error) {
      restoreBackup(installTarget, backup, hadTarget);
      backup = null;
      safeRecord({ event: 'install', skill: skill.slug, decision: 'fail', error: error.message });
      return { skill, status: 'fail', version: null, note: error.message, exitCode: 1 };
    } finally {
      if (tmp) fs.rmSync(tmp, { recursive: true, force: true });
      if (staged) fs.rmSync(staged, { recursive: true, force: true });
      if (stagingRoot) {
        // 结束（含失败）强制清理：目录为空时删除；并发安装留下的新鲜暂存则保留。
        try { fs.rmdirSync(stagingRoot); } catch (_) { /* 非空 / 并发占用，保留 */ }
      }
    }
  };
}

module.exports = { createInstaller, renameWithRetry, isSafeTarEntry, pruneStaleStaging, STAGING_STALE_MS };
