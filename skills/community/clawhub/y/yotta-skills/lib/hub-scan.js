'use strict';

/**
 * Shared "yotta-verify" engine discovery + scan runner for Hub adoption.
 *
 * The CLI and the local Hub panel (yotta-skills view) both import this module
 * so an adopt action always runs the same gate: locate a trusted verifier,
 * run it against the candidate directory, then evaluate the verdict.
 */

const path = require('path');
const { spawnSync } = require('child_process');
const depsLib = require('./deps');
const gateLib = require('./verify-gate');
const trustedVerifierLib = require('./trusted-verifier');
const scanPolicyLib = require('./scan-policy');
const hubLib = require('./hub');

const POLICY_PATH = path.join(__dirname, '..', 'scan-policy.json');

function currentCommand() {
  const args = process.argv.slice(2).map((a) => (/\s/.test(a) ? '"' + a + '"' : a));
  return 'yotta-skills ' + args.join(' ');
}

function findVerifyEngine(dest, opts) {
  // Do not use the registry for verifier identity: only the trusted record
  // written by the install pipeline (path + digest) counts.
  return gateLib.findVerifier({ dest, opts, trustedVerifier: trustedVerifierLib.loadRecord() });
}

function findPython(opts) {
  const options = opts || {};
  const cands = [];
  if (options.python) cands.push(options.python);
  if (process.env.YOTTA_SKILLS_PYTHON) cands.push(process.env.YOTTA_SKILLS_PYTHON);
  cands.push('python3', 'python');
  if (process.platform === 'win32') cands.push('py');
  for (const c of cands) {
    try {
      const r = spawnSync(c, ['--version'], { encoding: 'utf8', timeout: 10000 });
      if (r.status === 0) return c;
    } catch (_) { /* next candidate */ }
  }
  return null;
}

function runScan(engine, skillDir, opts) {
  const python = findPython(opts || {});
  if (!python) {
    return {
      ok: false,
      error: depsLib.describe('python', { command: currentCommand(), missing: true }),
    };
  }
  return gateLib.runVerifier(engine, skillDir, { python, spawnSync });
}

/**
 * 复用安装管线的 scanPolicy 复核（0.29.2）：版本 + treeHash 绑定，fail-closed。
 * 未命中例外表 / 绑定不匹配时返回原始 scan（不豁免任何发现）。
 */
function reviewScanWithPolicy(scan, context) {
  const ctx = context || {};
  const policy = scanPolicyLib.loadPolicy(ctx.policyPath || POLICY_PATH);
  return scanPolicyLib.applyScanPolicy(scan, {
    slug: ctx.slug,
    version: ctx.version,
    pkgDir: ctx.pkgDir,
    policy,
  });
}

/** Hub adopt scan engine: Hub itself first, then every discovered host dir. */
function scanEngineForHub(hubDir, discovery, opts) {
  const direct = findVerifyEngine(hubDir, opts);
  if (direct) return direct;
  const hosts = (discovery && discovery.hosts) || [];
  for (const host of hosts) {
    if (!host.exists) continue;
    const engine = findVerifyEngine(host.dir, opts);
    if (engine) return engine;
  }
  return null;
}

/**
 * Scan one candidate directory for Hub adoption.
 * Returns { ok, verdict, counts, block } or { ok:false, error }.
 */
function hubScanSkill(hubDir, discovery, opts, skillDir, context) {
  const options = opts || {};
  if (options.skipScan) {
    return { ok: true, verdict: 'explicit-unverified', counts: null, block: false };
  }
  const engine = scanEngineForHub(hubDir, discovery, options);
  if (!engine) {
    return {
      ok: false,
      error: '未找到元信扫描引擎（可先安装 yotta-verify，或用 --allow-unverified 显式降级）',
    };
  }
  const scan = runScan(engine, skillDir, options);
  if (!scan.ok) return scan;
  const ctx = context || {};
  const meta = hubLib.readSkillMeta(skillDir);
  const reviewed = reviewScanWithPolicy(scan, {
    slug: ctx.slug || (meta && (meta.slug || meta.name)) || null,
    version: ctx.version || (meta && meta.version) || null,
    pkgDir: skillDir,
    policyPath: options.policyPath,
  });
  const verdict = gateLib.evaluateVerdict(reviewed.verdict);
  return {
    ok: true,
    verdict: reviewed.verdict,
    counts: reviewed.counts,
    block: verdict.block,
    policy: reviewed.policy || null,
    findings: reviewed.findings || null,
  };
}

module.exports = {
  currentCommand,
  findVerifyEngine,
  findPython,
  runScan,
  reviewScanWithPolicy,
  scanEngineForHub,
  hubScanSkill,
};
