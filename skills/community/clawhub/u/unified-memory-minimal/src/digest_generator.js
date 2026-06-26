/**
 * Digest Generator v1.0
 * Generates daily and weekly memory digests
 */

import { getAllMemories } from './storage.js';
import { getLogger } from './logger.js';

const log = getLogger('digest_generator');

/**
 * Group memories by topic/category with summary
 * @param {object[]} memories
 * @param {number} maxPerGroup
 */
function groupByTopic(memories, maxPerGroup = 10) {
  /** @type {Record<string, object[]>} */
  const groups = {};

  for (const mem of memories) {
    const key = mem.category || 'general';
    if (!groups[key]) groups[key] = [];
    if (groups[key].length < maxPerGroup) {
      groups[key].push(mem);
    }
  }

  return groups;
}

/**
 * Score memory recency within a time window
 * @param {object} mem
 * @param {number} windowMs - time window in ms
 */
function recencyScore(mem, windowMs) {
  const age = Date.now() - new Date(mem.created_at || mem.updated_at || 0).getTime();
  if (age > windowMs) return 0;
  return 1 - age / windowMs;
}

/**
 * Score memory by importance
 * @param {object} mem
 */
function importanceScore(mem) {
  return mem.importance || 0.5;
}

/**
 * Combined score for ranking
 * @param {object} mem
 * @param {number} windowMs
 */
function combinedScore(mem, windowMs) {
  return importanceScore(mem) * 0.6 + recencyScore(mem, windowMs) * 0.4;
}

/**
 * Generate a daily digest (past 24 hours)
 * @param {object} [options]
 * @param {number} [options.topK]
 * @param {string} [options.scope]
 */
export function generateDailyDigest({ topK = 10, scope = 'agent' } = {}) {
  const allMemories = getAllMemories();
  const now = Date.now();
  const windowMs = 24 * 60 * 60 * 1000; // 24 hours

  const recent = allMemories.filter(m => {
    const age = now - new Date(m.created_at || m.updated_at || 0).getTime();
    return age <= windowMs;
  });

  // Score and sort
  const scored = recent.map(m => ({
    memory: m,
    score: combinedScore(m, windowMs),
    recency: recencyScore(m, windowMs),
  }));

  scored.sort((a, b) => b.score - a.score);
  const top = scored.slice(0, topK);

  const categoryGroups = {};
  for (const item of top) {
    const cat = item.memory.category || 'general';
    if (!categoryGroups[cat]) categoryGroups[cat] = [];
    categoryGroups[cat].push(item.memory);
  }

  const sections = [];
  for (const [cat, mems] of Object.entries(categoryGroups)) {
    const texts = mems.map(m => `- ${(m.text || '').substring(0, 100)}`).join('\n');
    sections.push(`### ${cat.charAt(0).toUpperCase() + cat.slice(1)} (${mems.length})\n${texts}`);
  }

  const digest = {
    type: 'daily',
    generatedAt: new Date().toISOString(),
    period: { start: new Date(now - windowMs).toISOString(), end: new Date(now).toISOString() },
    memoryCount: recent.length,
    topK: top.length,
    topMemories: top.map(t => ({
      id: t.memory.id,
      text: t.memory.text,
      category: t.memory.category,
      importance: t.memory.importance,
      score: Math.round(t.score * 1000) / 1000,
    })),
    sections: sections.join('\n\n'),
    summary: `You have ${recent.length} memories from the past 24h. Top ${top.length} by combined importance+recency score.`,
  };

  log.info(`[DigestGenerator] daily: ${recent.length} recent, ${top.length} in digest`);

  return digest;
}

/**
 * Generate a weekly digest (past 7 days)
 * @param {object} [options]
 * @param {number} [options.topK]
 * @param {string} [options.scope]
 */
export function generateWeeklyDigest({ topK = 20, scope = 'agent' } = {}) {
  const allMemories = getAllMemories();
  const now = Date.now();
  const windowMs = 7 * 24 * 60 * 60 * 1000; // 7 days

  const recent = allMemories.filter(m => {
    const age = now - new Date(m.created_at || m.updated_at || 0).getTime();
    return age <= windowMs;
  });

  // Score and sort
  const scored = recent.map(m => ({
    memory: m,
    score: combinedScore(m, windowMs),
    recency: recencyScore(m, windowMs),
  }));

  scored.sort((a, b) => b.score - a.score);
  const top = scored.slice(0, topK);

  // Group by topic/category for weekly view
  const byTopic = groupByTopic(recent, 15);

  const topicSections = [];
  for (const [topic, mems] of Object.entries(byTopic)) {
    const top3 = mems.slice(0, 3);
    const snippets = top3.map(m => `- ${(m.text || '').substring(0, 100)}`).join('\n');
    topicSections.push(`### ${topic.charAt(0).toUpperCase() + topic.slice(1)} (${mems.length} total)\n${snippets}`);
  }

  // Day-by-day distribution
  const dayGroups = {};
  for (const m of recent) {
    const day = new Date(m.created_at || m.updated_at || now).toISOString().slice(0, 10);
    if (!dayGroups[day]) dayGroups[day] = 0;
    dayGroups[day]++;
  }

  const dayBars = Object.entries(dayGroups)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([day, count]) => `  ${day}: ${'█'.repeat(Math.min(count, 20))} ${count}`)
    .join('\n');

  const digest = {
    type: 'weekly',
    generatedAt: new Date().toISOString(),
    period: { start: new Date(now - windowMs).toISOString(), end: new Date(now).toISOString() },
    memoryCount: recent.length,
    topK: top.length,
    topMemories: top.map(t => ({
      id: t.memory.id,
      text: t.memory.text,
      category: t.memory.category,
      importance: t.memory.importance,
      score: Math.round(t.score * 1000) / 1000,
    })),
    topicSections: topicSections.join('\n\n'),
    dailyDistribution: dayBars,
    summary: `You have ${recent.length} memories from the past 7 days across ${Object.keys(byTopic).length} topics.`,
  };

  log.info(`[DigestGenerator] weekly: ${recent.length} recent, ${top.length} in digest`);

  return digest;
}

/**
 * Format digest as readable text
 * @param {object} digest
 * @returns {string}
 */
export function formatDigestText(digest) {
  if (digest.type === 'daily') {
    const lines = [
      `📅 **Daily Digest** — ${new Date(digest.generatedAt).toLocaleDateString()}`,
      `Memory activity (24h): ${digest.memoryCount} new/modified`,
      '',
      digest.summary,
      '',
      '--- Top Memories ---',
    ];
    for (const m of digest.topMemories) {
      const snippet = (m.text || '').substring(0, 100).replace(/\n/g, ' ');
      lines.push(`[${m.category}] imp:${m.importance.toFixed(2)} ${snippet}…`);
    }
    return lines.join('\n');
  }

  if (digest.type === 'weekly') {
    const lines = [
      `📆 **Weekly Digest** — week of ${digest.period.start.slice(0, 10)}`,
      `Memory activity (7d): ${digest.memoryCount} memories`,
      '',
      digest.summary,
      '',
      '--- Daily Activity ---',
      digest.dailyDistribution,
      '',
      '--- Top Memories by Topic ---',
      digest.topicSections,
    ];
    return lines.join('\n');
  }

  return JSON.stringify(digest, null, 2);
}
