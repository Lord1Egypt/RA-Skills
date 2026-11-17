'use strict';
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const VERDICT_SAFE = 'SAFE TO INSTALL';
const VERDICT_CAUTION = 'INSTALL WITH CAUTION';
const VERDICT_REVIEW = 'REVIEW REQUIRED';
const VERDICT_BLOCK = 'DO NOT INSTALL';

const VERDICT_BY_SEVERITY = {
  critical: VERDICT_BLOCK,
  high: VERDICT_CAUTION,
  medium: VERDICT_REVIEW,
  low: VERDICT_SAFE,
  info: VERDICT_SAFE,
};
const SEVERITY_ORDER = ['critical', 'high', 'medium', 'low', 'info'];
const VERIFY_SCANNER = 'yotta-verify';

// 与 tools/build_opencode_bundle.py（handoff 构建器）逐字节同口径：
// 例外表绑定 prune 后的技能树 treeHash，技能升版或内容变化后旧例外自动失效（fail-closed）。
const REMOVE_NAMES = new Set([
  '.git', '.github', '.gitignore', '.npmignore', 'test', 'bin',
  'package.json', 'package-lock.json', 'install.sh', 'server.json',
  '__pycache__', '.pytest_cache', '.mypy_cache',
]);
const KEEP_EXTRA = {
  'yotta-memory': ['bin'],
  'yotta-skills': ['bin', 'lib', 'skills.json', 'scan-policy.json'],
};
const PRUNE_DIRS = new Set(['__pycache__', '.pytest_cache', '.mypy_cache']);
const HASH_SKIP_FILES = new Set(['.yotta-managed.json']);

function normalizeRel(value) {
  return String(value == null ? '' : value).replace(/\\/g, '/').replace(/^\.\//, '');
}

function loadPolicy(policyPath) {
  try {
    const raw = fs.readFileSync(policyPath, 'utf8');
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object' || !parsed.skills) return null;
    return parsed;
  } catch (_) {
    return null;
  }
}

function keepExtraFor(slug) {
  return new Set(KEEP_EXTRA[slug] || []);
}

function collectRows(dir, relBase, keepExtra, depth, rows) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (_) {
    return;
  }
  for (const entry of entries) {
    if (entry.isSymbolicLink()) continue;
    const rel = relBase ? relBase + '/' + entry.name : entry.name;
    if (entry.isDirectory()) {
      if (PRUNE_DIRS.has(entry.name)) continue;
      if (depth === 0 && REMOVE_NAMES.has(entry.name) && !keepExtra.has(entry.name)) continue;
      collectRows(path.join(dir, entry.name), rel, keepExtra, depth + 1, rows);
      continue;
    }
    if (!entry.isFile()) continue;
    if (depth === 0 && REMOVE_NAMES.has(entry.name) && !keepExtra.has(entry.name)) continue;
    if (entry.name.endsWith('.pyc') || entry.name.endsWith('.pyo')) continue;
    if (HASH_SKIP_FILES.has(rel)) continue;
    let data;
    try {
      data = fs.readFileSync(path.join(dir, entry.name));
    } catch (_) {
      continue;
    }
    rows.push({ rel, hash: crypto.createHash('sha256').update(data).digest('hex') });
  }
}

function computeTreeHash(pkgDir, slug) {
  const rows = [];
  collectRows(pkgDir, '', keepExtraFor(slug), 0, rows);
  rows.sort((a, b) => Buffer.compare(Buffer.from(a.rel, 'utf8'), Buffer.from(b.rel, 'utf8')));
  const manifest = rows.map((row) => Buffer.concat([
    Buffer.from(row.rel, 'utf8'),
    Buffer.from('\0', 'ascii'),
    Buffer.from(row.hash, 'ascii'),
    Buffer.from('\n', 'ascii'),
  ]));
  const digest = crypto.createHash('sha256').update(Buffer.concat(manifest)).digest('hex');
  return 'sha256:' + digest;
}

function summarize(findings) {
  const counts = { critical: 0, high: 0, medium: 0, low: 0, info: 0 };
  for (const finding of findings) {
    const severity = finding && finding.severity;
    if (Object.prototype.hasOwnProperty.call(counts, severity)) counts[severity] += 1;
  }
  let verdict = VERDICT_SAFE;
  for (const severity of SEVERITY_ORDER) {
    if (counts[severity]) {
      verdict = VERDICT_BY_SEVERITY[severity];
      break;
    }
  }
  return { counts, verdict };
}

function exceptionMatches(exception, finding) {
  if (!exception || exception.action !== 'allow') return false;
  const scanners = Array.isArray(exception.scanners) ? exception.scanners : [];
  if (scanners.length > 0 && !scanners.includes(VERIFY_SCANNER)) return false;
  if (String(exception.rule || '') !== String(finding.rule_id || '')) return false;
  return normalizeRel(exception.path) === normalizeRel(finding.file);
}

/**
 * 用随包分发的 scanPolicy 例外表复核元信扫描结果。
 *
 * 绑定校验（缺一即不生效，fail-closed）：skill 条目存在 + version 一致 + treeHash 一致。
 * 只有 action=allow 且 scanners 含 yotta-verify 的例外才会豁免对应 (rule, path) 发现。
 */
function applyScanPolicy(scan, context) {
  const ctx = context || {};
  const base = {
    applied: false,
    reason: null,
    excluded: 0,
    excludedFindings: [],
    version: null,
    treeHash: null,
  };
  const result = { ...scan, policy: base };
  if (!scan || !scan.ok) {
    result.policy.reason = 'scan-failed';
    return result;
  }
  const policy = ctx.policy;
  const slug = ctx.slug;
  const version = ctx.version;
  const pkgDir = ctx.pkgDir;
  if (!policy || !slug || !pkgDir) {
    result.policy.reason = 'policy-unavailable';
    return result;
  }
  const entry = policy.skills[slug];
  if (!entry) {
    result.policy.reason = 'no-entry';
    return result;
  }
  if (!Array.isArray(scan.findings)) {
    result.policy.reason = 'findings-unavailable';
    return result;
  }
  if (entry.version !== version) {
    result.policy.reason = 'version-mismatch';
    return result;
  }
  const treeHash = computeTreeHash(pkgDir, slug);
  result.policy.version = entry.version;
  result.policy.treeHash = treeHash;
  if (entry.treeHash !== treeHash) {
    result.policy.reason = 'treehash-mismatch';
    return result;
  }
  const exceptions = Array.isArray(entry.exceptions) ? entry.exceptions : [];
  const kept = [];
  for (const finding of scan.findings) {
    const hit = exceptions.find((exception) => exceptionMatches(exception, finding));
    if (hit) {
      result.policy.excludedFindings.push({
        rule: finding.rule_id,
        path: normalizeRel(finding.file),
        severity: finding.severity,
        reason: hit.reason || null,
      });
      continue;
    }
    kept.push(finding);
  }
  const summary = summarize(kept);
  result.policy.applied = true;
  result.policy.reason = 'applied';
  result.policy.excluded = result.policy.excludedFindings.length;
  result.verdict = summary.verdict;
  result.counts = summary.counts;
  result.findings = kept;
  return result;
}

module.exports = {
  VERDICT_SAFE,
  VERDICT_CAUTION,
  VERDICT_REVIEW,
  VERDICT_BLOCK,
  REMOVE_NAMES,
  KEEP_EXTRA,
  normalizeRel,
  loadPolicy,
  computeTreeHash,
  summarize,
  exceptionMatches,
  applyScanPolicy,
};
