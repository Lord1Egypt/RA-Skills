'use strict';

/**
 * 元阁 O1 动态路由：开源侧确定性特征快照。
 *
 * 边界：
 * - 只读注册表元数据与本地使用记录的聚合计数；不读 SKILL.md 全文。
 * - 不评分、不排序；评分在私有 provider 中完成。
 * - 不写文件、不联网、不调用模型。
 */

const crypto = require('crypto');

const MAX_TOKENS = 64;
const MAX_INSTALLED = 500;
const MAX_PLAYBOOK_MATCHES = 5;
const MAX_DESCRIPTION = 500;

const EN_STOPWORDS = new Set([
  'a', 'an', 'the', 'and', 'or', 'of', 'to', 'in', 'on', 'for', 'with', 'from',
  'this', 'that', 'is', 'are', 'was', 'were', 'be', 'been', 'your', 'you', 'our',
  'we', 'it', 'at', 'by', 'as', 'not', 'no', 'so', 'do', 'does',
]);

function normalizeText(text) {
  return String(text || '').toLowerCase().replace(/\s+/g, ' ').trim();
}

function normalizedKeyword(text) {
  return normalizeText(text).replace(/\s+/g, '');
}

function englishTokens(text) {
  const out = [];
  const seen = new Set();
  for (const match of normalizeText(text).match(/[a-z][a-z0-9]{2,}/g) || []) {
    if (EN_STOPWORDS.has(match) || seen.has(match)) continue;
    seen.add(match);
    out.push(match);
    if (out.length >= MAX_TOKENS) break;
  }
  return out;
}

function cjkBigrams(text) {
  const out = [];
  const seen = new Set();
  for (const match of String(text || '').match(/[\u4e00-\u9fff]+/g) || []) {
    for (let i = 0; i < match.length - 1; i++) {
      const bigram = match.slice(i, i + 2);
      if (seen.has(bigram)) continue;
      seen.add(bigram);
      out.push(bigram);
      if (out.length >= MAX_TOKENS) return out;
    }
  }
  return out;
}

function requestHash(request) {
  return crypto.createHash('sha256').update(normalizeText(request), 'utf8').digest('hex');
}

function playbookMatches(request, playbooks) {
  const text = normalizedKeyword(request);
  const matches = [];
  for (const playbook of Array.isArray(playbooks) ? playbooks : []) {
    const matched = [];
    let score = 0;
    for (const keyword of Array.isArray(playbook.keywords) ? playbook.keywords : []) {
      const normalized = normalizedKeyword(keyword);
      if (!normalized || !text.includes(normalized)) continue;
      matched.push(String(keyword));
      score += normalized.length >= 3 ? 2 : 1;
    }
    if (score > 0) {
      matches.push({
        id: String(playbook.id || ''),
        score,
        matched_keywords: matched,
      });
    }
  }
  return matches
    .sort((left, right) => right.score - left.score || left.id.localeCompare(right.id))
    .slice(0, MAX_PLAYBOOK_MATCHES);
}

function trustOf(record) {
  const slug = String(record && record.slug || '');
  const sources = Array.isArray(record && record.sources) ? record.sources.join(' ').toLowerCase() : '';
  if (slug.startsWith('yotta-') || sources.includes('yottameta')) return 'yottameta';
  return 'third-party';
}

function skillUsage(usage, slug) {
  const source = usage && usage.skills && usage.skills[slug] ? usage.skills[slug] : {};
  const pairs = source.pairs && typeof source.pairs === 'object' && !Array.isArray(source.pairs)
    ? source.pairs
    : {};
  return {
    used: Number(source.used) || 0,
    named: Number(source.named) || 0,
    accepted: Number(source.accepted) || 0,
    route_hits: Number(source.route_hits) || 0,
    distinct_pairs: Object.keys(pairs).length,
    last_signal_at: String(source.last_signal_at || ''),
  };
}

function buildRouteFeatures(options) {
  const opts = options || {};
  const request = String(opts.request || '');
  const registry = opts.registry || { skills: {} };
  const staticResult = opts.staticResult || {};
  const usage = opts.usage || {};
  const playbooks = Array.isArray(opts.playbooks) ? opts.playbooks : [];
  const usageEnabled = usage.enabled === true;

  const installedSkills = Object.values(registry.skills || {})
    .filter((record) => record && record.slug && record.status !== 'gone')
    .slice(0, MAX_INSTALLED)
    .map((record) => ({
      slug: String(record.slug),
      version: String(record.version || ''),
      description: String(record.description || '').slice(0, MAX_DESCRIPTION),
      status: String(record.status || 'known'),
      sources: Array.isArray(record.sources) ? record.sources.slice(0, 8).map(String) : [],
      first_seen: String(record.first_seen || ''),
      last_seen: String(record.last_seen || ''),
      trust: trustOf(record),
    }));

  const usageSkills = {};
  if (usageEnabled) {
    for (const slug of Object.keys(usage.skills || {}).sort()) {
      usageSkills[slug] = skillUsage(usage, slug);
    }
  }

  return {
    schema: 2,
    request,
    request_features: {
      request_hash: requestHash(request),
      english_tokens: englishTokens(request),
      cjk_bigrams: cjkBigrams(request),
      playbook_matches: playbookMatches(request, playbooks),
    },
    static_result: {
      playbook: String(staticResult.playbook && staticResult.playbook.id || staticResult.playbook || ''),
      confidence: String(staticResult.confidence || ''),
      skills: Array.isArray(staticResult.skills)
        ? staticResult.skills.map((skill) => String(skill && skill.slug || skill || '')).filter(Boolean)
        : [],
    },
    installed_skills: installedSkills,
    usage: {
      enabled: usageEnabled,
      skills: usageSkills,
      last_route: usage.last_route && typeof usage.last_route === 'object'
        ? {
          at: String(usage.last_route.at || ''),
          playbook: String(usage.last_route.playbook || ''),
          confidence: String(usage.last_route.confidence || ''),
          skills: Array.isArray(usage.last_route.skills) ? usage.last_route.skills.map(String).slice(0, 12) : [],
        }
        : null,
    },
    playbooks: playbooks.map((playbook) => ({
      id: String(playbook.id || ''),
      name: String(playbook.name || ''),
      intent: String(playbook.intent || ''),
      keywords: Array.isArray(playbook.keywords) ? playbook.keywords.slice(0, 32).map(String) : [],
      skills: Array.isArray(playbook.skills)
        ? playbook.skills.map((skill) => String(skill && skill.slug || skill || '')).filter(Boolean)
        : [],
    })),
  };
}

module.exports = {
  MAX_TOKENS,
  MAX_INSTALLED,
  MAX_PLAYBOOK_MATCHES,
  normalizeText,
  englishTokens,
  cjkBigrams,
  requestHash,
  playbookMatches,
  trustOf,
  skillUsage,
  buildRouteFeatures,
};
