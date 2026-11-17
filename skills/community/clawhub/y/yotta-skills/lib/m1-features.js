'use strict';

/**
 * M1 记忆裁决器：开源侧只做确定性特征快照与建议文件。
 *
 * 评分算法不在本文件，由私有 provider（capability m1.adjudicate）返回。
 * 快照只含技能元数据与聚合计数，不含需求原文、记忆正文、路径、用户名或主机名。
 */

const fs = require('fs');
const path = require('path');
const usageJournal = require('./usage-journal');

const SCHEMA = 1;
const REPORT_FILE = 'memory-adjudication.json';

function nowIso(options) {
  const value = options && options.now;
  return typeof value === 'string' && value ? value : new Date().toISOString();
}

function skillSignal(usage, slug) {
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
  };
}

function buildFeatureSnapshot(registry, usage, options) {
  const skills = Object.values((registry && registry.skills) || {})
    .filter((record) => record && record.slug)
    .map((record) => {
      const slug = String(record.slug);
      return {
        slug,
        version: String(record.version || ''),
        status: String(record.status || 'known'),
        description: String(record.description || ''),
        first_seen: String(record.first_seen || ''),
        last_seen: String(record.last_seen || ''),
        last_signal_at: String((usage && usage.skills && usage.skills[slug] && usage.skills[slug].last_signal_at) || ''),
        pinned: record.pinned === true,
        signals: skillSignal(usage, slug),
      };
    })
    .sort((left, right) => left.slug.localeCompare(right.slug));
  return {
    schema: SCHEMA,
    generated_at: nowIso(options),
    skills,
  };
}

function reportPath(options) {
  const opts = options || {};
  if (opts.file) return path.resolve(opts.file);
  const fromEnv = String(process.env.YOTTA_SKILLS_M1_REPORT_FILE || '').trim();
  if (fromEnv) return path.resolve(fromEnv);
  return path.join(path.dirname(usageJournal.usageFilePath(opts)), REPORT_FILE);
}

function buildMemoryCandidates(decisions, registry) {
  const records = (registry && registry.skills) || {};
  const candidates = [];
  for (const decision of Array.isArray(decisions) ? decisions : []) {
    if (!decision || decision.verdict !== 'promote') continue;
    const record = records[decision.slug] || {};
    const description = String(record.description || '').trim();
    const summary = description
      ? description.slice(0, 180)
      : '暂无描述';
    candidates.push({
      type: 'PREF',
      subject: '技能索引：' + decision.slug,
      statement: '本机长期保留技能 ' + decision.slug + '：' + summary
        + '；M1 评分：' + decision.score + '。',
      source: 'yotta-skills m1',
      weight: 0.8,
    });
  }
  return candidates;
}

function writeAdjudication(report, options) {
  const file = reportPath(options);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = file + '.tmp-' + process.pid + '-' + Date.now();
  fs.writeFileSync(tmp, JSON.stringify(report, null, 2) + '\n', 'utf8');
  try {
    fs.renameSync(tmp, file);
  } catch (_) {
    fs.rmSync(file, { force: true });
    fs.renameSync(tmp, file);
  }
  return file;
}

module.exports = {
  SCHEMA,
  REPORT_FILE,
  buildFeatureSnapshot,
  reportPath,
  buildMemoryCandidates,
  writeAdjudication,
};
