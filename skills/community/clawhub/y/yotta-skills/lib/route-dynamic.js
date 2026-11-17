'use strict';

/**
 * 元阁 O1 动态路由：provider 响应白名单校验与应用。
 *
 * provider 输出一律当数据：未知 slug 丢弃、非法字段忽略、展示文本限长去控制字符。
 * 静态 playbook 是锚点：provider 只允许在已装白名单内增补 / 重排，不能删除静态技能。
 */

const CONFIDENCE = new Set(['high', 'medium', 'low']);
const MAX_SKILLS = 8;
const MAX_ADDED = 3;
const MAX_REASONS = 20;
const MAX_ALTERNATIVES = 3;
const MAX_ROLE = 160;
const MAX_REASON = 240;
const MAX_SUMMARY = 320;

function sanitizeText(value, maxLen) {
  return String(value || '')
    .replace(/[\u0000-\u001f\u007f]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, maxLen);
}

function sanitizeList(value, maxItems, maxLen) {
  if (!Array.isArray(value)) return [];
  const out = [];
  const seen = new Set();
  for (const item of value) {
    const text = sanitizeText(item, maxLen);
    if (!text || seen.has(text)) continue;
    seen.add(text);
    out.push(text);
    if (out.length >= maxItems) break;
  }
  return out;
}

function dynamicBlock(status, providerId, note) {
  return {
    status: status || 'not_installed',
    provider_id: providerId || '',
    applied: false,
    confidence: '',
    added: [],
    dropped: [],
    summary: '',
    reasons: [],
    alternatives: [],
    note: note || '',
  };
}

function installedSet(registry) {
  return new Set(Object.values((registry && registry.skills) || {})
    .filter((record) => record && record.slug && record.status !== 'gone')
    .map((record) => String(record.slug)));
}

function normalizeRequestedSkills(data, installed) {
  const requested = Array.isArray(data && data.skills) ? data.skills : [];
  const seen = new Set();
  const ordered = [];
  const dropped = [];
  for (const raw of requested) {
    const slug = raw && typeof raw === 'object' ? String(raw.slug || '') : '';
    if (!slug) continue;
    if (seen.has(slug) || !installed.has(slug)) {
      dropped.push(slug);
      continue;
    }
    seen.add(slug);
    const score = Number(raw.score);
    ordered.push({
      slug,
      role: sanitizeText(raw.role, MAX_ROLE),
      reason: sanitizeText(raw.reason, MAX_REASON),
      score: Number.isFinite(score) ? Math.max(0, Math.min(100, Math.round(score))) : null,
    });
    if (ordered.length >= MAX_SKILLS) break;
  }
  return { ordered, dropped };
}

function normalizeAlternatives(value, installed, selected) {
  if (!Array.isArray(value)) return [];
  const out = [];
  const seen = new Set();
  for (const raw of value) {
    const slug = raw && typeof raw === 'object' ? String(raw.slug || '') : '';
    if (!slug || seen.has(slug) || !installed.has(slug) || selected.has(slug)) continue;
    seen.add(slug);
    const score = Number(raw.score);
    out.push({
      slug,
      score: Number.isFinite(score) ? Math.max(0, Math.min(100, Math.round(score))) : null,
      reason: sanitizeText(raw.reason, MAX_REASON),
    });
    if (out.length >= MAX_ALTERNATIVES) break;
  }
  return out;
}

/**
 * 把 provider 的 data 应用到静态结果。
 * 返回 dynamic 块；若 provider 未给出任何有效技能，则不修改 result。
 */
function applyDynamicData(result, data, registry, options) {
  const opts = options || {};
  const block = dynamicBlock('active', opts.providerId || '', '');
  const installed = installedSet(registry);
  const staticBySlug = new Map((result.skills || []).map((skill) => [skill.slug, skill]));
  const { ordered, dropped } = normalizeRequestedSkills(data, installed);
  block.dropped = dropped;
  if (!ordered.length) {
    block.note = '提供方未返回白名单内技能';
    return block;
  }

  const next = [];
  for (const item of ordered) {
    const existing = staticBySlug.get(item.slug);
    if (existing) {
      next.push(Object.assign({}, existing, {
        role: item.role || existing.role,
        dynamic_reason: item.reason || '',
        dynamic_score: item.score,
      }));
      continue;
    }
    const record = (registry.skills && registry.skills[item.slug]) || {};
    next.push({
      slug: item.slug,
      order: 0,
      role: item.role || '由动态路由补充',
      installed: true,
      version: record.version || '',
      sources: record.sources || [],
      variants: Array.isArray(record.variants) ? record.variants : [],
      conflicts: Array.isArray(record.conflicts) ? record.conflicts : [],
      dynamic_reason: item.reason || '',
      dynamic_score: item.score,
    });
  }
  for (const skill of result.skills || []) {
    if (!next.some((item) => item.slug === skill.slug)) next.push(skill);
  }
  next.forEach((skill, index) => { skill.order = index + 1; });

  const added = next.filter((skill) => !staticBySlug.has(skill.slug)).map((skill) => skill.slug);
  if (added.length > MAX_ADDED) {
    const allowed = new Set(added.slice(0, MAX_ADDED));
    for (const skill of next.slice()) {
      if (!staticBySlug.has(skill.slug) && !allowed.has(skill.slug)) {
        block.dropped.push(skill.slug);
      }
    }
    for (let i = next.length - 1; i >= 0; i--) {
      if (!staticBySlug.has(next[i].slug) && !allowed.has(next[i].slug)) next.splice(i, 1);
    }
    next.forEach((skill, index) => { skill.order = index + 1; });
  }

  const selected = new Set(next.map((skill) => skill.slug));
  block.applied = true;
  block.confidence = CONFIDENCE.has(data && data.confidence) ? data.confidence : (result.confidence || '');
  block.summary = sanitizeText(data && data.summary, MAX_SUMMARY);
  block.reasons = sanitizeList(data && data.reasons, MAX_REASONS, MAX_REASON);
  block.alternatives = normalizeAlternatives(data && data.alternatives, installed, selected);
  block.added = next.filter((skill) => !staticBySlug.has(skill.slug)).map((skill) => skill.slug);
  result.skills = next;
  return block;
}

module.exports = {
  CONFIDENCE,
  MAX_SKILLS,
  MAX_ADDED,
  MAX_REASONS,
  MAX_ALTERNATIVES,
  sanitizeText,
  sanitizeList,
  dynamicBlock,
  installedSet,
  applyDynamicData,
};
