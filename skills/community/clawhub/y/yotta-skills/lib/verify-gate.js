'use strict';
const fs = require('fs');
const path = require('path');
const trusted = require('./trusted-verifier');

const SAFE = 'SAFE TO INSTALL';
const CAUTION = 'INSTALL WITH CAUTION';
const REVIEW = 'REVIEW REQUIRED';
const BLOCK = 'DO NOT INSTALL';

/** 用户显式指定的引擎（人工可信，不做身份判定）。 */
function explicitCandidates(opts) {
  const candidates = [];
  if (opts && opts.verify) candidates.push(path.resolve(opts.verify));
  if (process.env.YOTTA_SKILLS_VERIFY) candidates.push(path.resolve(process.env.YOTTA_SKILLS_VERIFY));
  return candidates;
}

/**
 * 定位元信扫描引擎（v0.19.13 收紧）。
 *
 * 旧实现会读本地注册表里 slug=yotta-verify 的 source_dirs，而注册表身份来自被扫描技能
 * 自己 SKILL.md frontmatter 的 name —— 伪造目录即可劫持校验器（执行任意代码 + 伪造
 * SAFE 结论）。现只认两类来源：
 *   ① 用户显式指定：--verify / YOTTA_SKILLS_VERIFY；
 *   ② 安装管线写入的受信记录：包身份（slug / package / trust / 版本）+ 路径 realpath
 *      + 引擎 SHA-256 与记录一致。
 * 其余一律返回 null（fail-closed），由上层走自举安装。
 */
function findVerifier(context) {
  const ctx = context || {};
  for (const candidate of explicitCandidates(ctx.opts || {})) {
    try {
      if (fs.statSync(candidate).isFile()) return candidate;
    } catch (_) {
      // Try the next candidate.
    }
  }
  const record = ctx.trustedVerifier;
  if (record && record.path) {
    const check = trusted.verifyEngine(record.path, { record });
    if (check.ok) return check.path;
  }
  return null;
}

function parseScanOutput(stdout) {
  try {
    const value = JSON.parse(String(stdout || ''));
    if (!value || typeof value.verdict !== 'string') {
      return { ok: false, verdict: null, counts: null, findings: null, error: '扫描输出缺少 verdict' };
    }
    return {
      ok: true,
      verdict: value.verdict,
      counts: value.counts || {},
      findings: Array.isArray(value.findings) ? value.findings : null,
      error: null,
    };
  } catch (error) {
    return { ok: false, verdict: null, counts: null, findings: null, error: error.message };
  }
}

function evaluateVerdict(verdict) {
  if (verdict === SAFE) return { decision: 'allow', block: false, warn: false };
  if (verdict === CAUTION || verdict === REVIEW) return { decision: 'warn', block: false, warn: true };
  return { decision: 'block', block: true, warn: true };
}

function runScanOnce(engine, target, options) {
  return options.spawnSync(options.python, ['-B', engine, 'scan', target, '--json'], {
    encoding: 'utf8',
    timeout: 60000,
    maxBuffer: 32 * 1024 * 1024,
  });
}

function stderrBrief(result) {
  const text = String((result && result.stderr) || '').trim();
  if (!text) return '';
  return text.split(/\r?\n/).filter(Boolean).slice(-2).join(' | ').slice(0, 300);
}

/**
 * 元信扫描是只读幂等操作：解析失败（空输出 / 截断 / 进程异常）时重试一次，
 * 避免偶发的子进程抖动把安装判死；两次都失败才按阻断处理。
 */
function runVerifier(engine, target, options) {
  const opts = options || {};
  const retries = opts.retries === undefined ? 1 : Math.max(0, Number(opts.retries) || 0);
  let result = null;
  let parsed = null;
  for (let attempt = 0; attempt <= retries; attempt += 1) {
    result = runScanOnce(engine, target, opts);
    if (!result || result.error || result.status === null) {
      parsed = null;
      continue;
    }
    parsed = parseScanOutput(result.stdout);
    if (parsed.ok) break;
  }
  if (result && result.error) {
    return { ok: false, verdict: null, counts: null, findings: null, error: result.error.message, exitCode: null };
  }
  if (!result || result.status === null) {
    return {
      ok: false,
      verdict: null,
      counts: null,
      findings: null,
      error: '元信 scan 执行失败（超时或无法启动）',
      exitCode: null,
    };
  }
  if (!parsed || !parsed.ok) {
    const brief = stderrBrief(result);
    return {
      ok: false,
      verdict: null,
      counts: null,
      findings: null,
      error: '元信 scan 输出无法解析（exit ' + result.status + '）' + (brief ? ': ' + brief : ''),
      exitCode: result.status,
    };
  }
  return {
    ok: true,
    verdict: parsed.verdict,
    counts: parsed.counts,
    findings: parsed.findings,
    error: null,
    exitCode: result.status,
  };
}

module.exports = {
  SAFE,
  CAUTION,
  REVIEW,
  BLOCK,
  explicitCandidates,
  findVerifier,
  parseScanOutput,
  evaluateVerdict,
  runVerifier,
};
