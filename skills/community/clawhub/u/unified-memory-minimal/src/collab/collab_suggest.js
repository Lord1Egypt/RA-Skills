/**
 * Collaboration Suggestion System
 * 
 * Analyzes memory content to suggest when/how agents should collaborate.
 * Uses keyword patterns to detect information worth synchronizing.
 * 
 * @module collab/collab_suggest
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { config } from '../config.js';

/**
 * @typedef {Object} SyncPattern
 * @property {string} id
 * @property {string[]} keywords
 * @property {string} category
 * @property {string} target
 * @property {'high'|'medium'|'low'} priority
 */

/**
 * @typedef {Object} CollabSuggestion
 * @property {string} pattern_id
 * @property {string} category
 * @property {string} target
 * @property {'high'|'medium'|'low'} priority
 * @property {string} matched_keyword
 * @property {string} text_snippet
 */

/**
 * @typedef {Object} AnalysisResult
 * @property {string} text
 * @property {string} source_agent
 * @property {string} timestamp
 * @property {string[]} matched_keywords
 * @property {CollabSuggestion[]} suggestions
 * @property {boolean} should_sync
 */

/** @type {SyncPattern[]} */
const DEFAULT_PATTERNS = [
  {
    id: 'user_preference',
    keywords: ['偏好', '喜欢', '习惯', 'prefer', 'like'],
    category: 'preference',
    target: 'all',
    priority: 'high',
  },
  {
    id: 'user_info',
    keywords: ['刘总', '老板', '用户', 'user', '张三'],
    category: 'user',
    target: 'all',
    priority: 'high',
  },
  {
    id: 'task',
    keywords: ['任务', '待办', 'todo', 'task', '需要'],
    category: 'task',
    target: 'all',
    priority: 'medium',
  },
  {
    id: 'project',
    keywords: ['项目', '工程', 'project', 'repo'],
    category: 'project',
    target: 'all',
    priority: 'medium',
  },
  {
    id: 'decision',
    keywords: ['决定', '确定', '选择', 'decide', 'confirm'],
    category: 'decision',
    target: 'all',
    priority: 'high',
  },
];

/**
 * Ensure the suggest directory and files exist.
 */
function ensureDirs() {
  const suggestDir = join(config.memoryDir, 'suggest');
  if (!existsSync(suggestDir)) {
    mkdirSync(suggestDir, { recursive: true });
  }

  const patternsFile = join(suggestDir, 'patterns.json');
  if (!existsSync(patternsFile)) {
    writeFileSync(patternsFile, JSON.stringify({ patterns: DEFAULT_PATTERNS }, null, 2), 'utf8');
  }

  const suggestionsFile = join(suggestDir, 'suggestions.jsonl');
  if (!existsSync(suggestionsFile)) {
    writeFileSync(suggestionsFile, '', 'utf8');
  }

  const learnedFile = join(suggestDir, 'learned.jsonl');
  if (!existsSync(learnedFile)) {
    writeFileSync(learnedFile, '', 'utf8');
  }
}

/**
 * Get the path to a suggest data file.
 * @param {string} name
 * @returns {string}
 */
function suggestPath(name) {
  return join(config.memoryDir, 'suggest', name);
}

/**
 * Load all sync patterns.
 * @returns {SyncPattern[]}
 */
export function loadPatterns() {
  ensureDirs();
  try {
    const data = JSON.parse(readFileSync(suggestPath('patterns.json'), 'utf8'));
    return data.patterns || DEFAULT_PATTERNS;
  } catch {
    return DEFAULT_PATTERNS;
  }
}

/**
 * Save patterns to disk.
 * @param {SyncPattern[]} patterns
 */
function savePatterns(patterns) {
  ensureDirs();
  writeFileSync(suggestPath('patterns.json'), JSON.stringify({ patterns }, null, 2), 'utf8');
}

/**
 * Analyze text and generate collaboration suggestions.
 * @param {string} text
 * @param {string} [sourceAgent='main']
 * @returns {AnalysisResult}
 */
export function analyzeText(text, sourceAgent = 'main') {
  ensureDirs();
  const patterns = loadPatterns();
  const textLower = text.toLowerCase();

  /** @type {CollabSuggestion[]} */
  const suggestions = [];
  /** @type {string[]} */
  const matchedKeywords = [];

  for (const pattern of patterns) {
    for (const keyword of pattern.keywords) {
      if (textLower.includes(keyword.toLowerCase())) {
        matchedKeywords.push(keyword);
        suggestions.push({
          pattern_id: pattern.id,
          category: pattern.category,
          target: pattern.target,
          priority: pattern.priority,
          matched_keyword: keyword,
          text_snippet: text.slice(0, 100),
        });
        break; // Only match each pattern once
      }
    }
  }

  /** @type {AnalysisResult} */
  const result = {
    text: text.slice(0, 200),
    source_agent: sourceAgent,
    timestamp: new Date().toISOString(),
    matched_keywords: [...new Set(matchedKeywords)],
    suggestions,
    should_sync: suggestions.length > 0,
  };

  // Persist suggestions
  if (suggestions.length > 0) {
    const line = JSON.stringify(result);
    writeFileSync(suggestPath('suggestions.jsonl'), line + '\n', { flag: 'a', encoding: 'utf8' });
  }

  return result;
}

/**
 * Get stored collaboration suggestions.
 * @param {string} [agent]
 * @param {number} [limit=10]
 * @returns {AnalysisResult[]}
 */
export function getSuggestions(agent, limit = 10) {
  ensureDirs();
  const suggestionsFile = suggestPath('suggestions.jsonl');

  /** @type {AnalysisResult[]} */
  const results = [];

  if (!existsSync(suggestionsFile)) return results;

  try {
    const lines = readFileSync(suggestionsFile, 'utf8').split('\n').filter(Boolean);
    for (const line of lines) {
      try {
        const entry = /** @type {AnalysisResult} */ (JSON.parse(line));
        if (agent === undefined || entry.source_agent === agent) {
          results.push(entry);
        }
      } catch {
        // Skip malformed lines
      }
    }
  } catch {
    // File not found or unreadable
  }

  // Sort by timestamp descending
  results.sort((a, b) => (b.timestamp > a.timestamp ? 1 : -1));
  return results.slice(0, limit);
}

/**
 * Learn (add or update) a sync pattern.
 * @param {string} patternId
 * @param {string[]} keywords
 * @param {string} category
 * @param {string} target
 * @param {'high'|'medium'|'low'} [priority='medium']
 * @returns {{ learned: boolean, pattern_id: string }}
 */
export function learnPattern(patternId, keywords, category, target, priority = 'medium') {
  ensureDirs();
  const patterns = loadPatterns();

  const existing = patterns.find((p) => p.id === patternId);
  if (existing) {
    // Merge keywords
    const merged = [...new Set([...existing.keywords, ...keywords])];
    existing.keywords = merged;
    existing.category = category;
    existing.target = target;
    existing.priority = priority;
  } else {
    patterns.push({ id: patternId, keywords, category, target, priority });
  }

  savePatterns(patterns);

  // Log the learning event
  const logEntry = {
    timestamp: new Date().toISOString(),
    action: 'learn_pattern',
    pattern_id: patternId,
    keywords,
  };
  writeFileSync(suggestPath('learned.jsonl'), JSON.stringify(logEntry) + '\n', { flag: 'a', encoding: 'utf8' });

  return { learned: true, pattern_id: patternId };
}

/**
 * Get statistics about stored suggestions.
 * @returns {{
 *   total_suggestions: number,
 *   by_category: Record<string, number>,
 *   by_priority: Record<string, number>,
 *   patterns_count: number,
 *   learned_count: number
 * }}
 */
export function getStats() {
  ensureDirs();

  /** @type {Record<string, number>} */
  const byCategory = {};
  /** @type {Record<string, number>} */
  const byPriority = { high: 0, medium: 0, low: 0 };
  let total = 0;
  let learnedCount = 0;

  const suggestionsFile = suggestPath('suggestions.jsonl');
  if (existsSync(suggestionsFile)) {
    try {
      const lines = readFileSync(suggestionsFile, 'utf8').split('\n').filter(Boolean);
      for (const line of lines) {
        try {
          const entry = /** @type {AnalysisResult} */ (JSON.parse(line));
          total++;
          for (const s of entry.suggestions || []) {
            byCategory[s.category] = (byCategory[s.category] || 0) + 1;
            byPriority[s.priority] = (byPriority[s.priority] || 0) + 1;
          }
        } catch {
          // Skip
        }
      }
    } catch {
      // Skip
    }
  }

  const learnedFile = suggestPath('learned.jsonl');
  if (existsSync(learnedFile)) {
    try {
      learnedCount = readFileSync(learnedFile, 'utf8').split('\n').filter(Boolean).length;
    } catch {
      // Skip
    }
  }

  return {
    total_suggestions: total,
    by_category: byCategory,
    by_priority: byPriority,
    patterns_count: loadPatterns().length,
    learned_count: learnedCount,
  };
}

/**
 * Find collaboration overlap between two agents based on shared tags/categories.
 * @param {string[]} tags1
 * @param {string[]} tags2
 * @returns {{ overlap: string[], score: number }}
 */
export function findOverlap(tags1, tags2) {
  const set2 = new Set(tags2.map((t) => t.toLowerCase()));
  const overlap = tags1.filter((t) => set2.has(t.toLowerCase()));
  const score = tags1.length > 0 ? overlap.length / tags1.length : 0;
  return { overlap, score };
}

/**
 * Suggest collaboration opportunities based on stored patterns and categories.
 * @param {string} [agentId]
 * @returns {Array<{ agent: string, category: string, reason: string, score: number }>}
 */
export function suggestCollaborations(agentId) {
  const patterns = loadPatterns();
  const suggestions = getSuggestions(agentId, 50);

  /** @type {Array<{ agent: string, category: string, reason: string, score: number }>} */
  const collabs = [];

  // Group suggestions by category to find overlap
  /** @type {Record<string, AnalysisResult[]>} */
  const byCategory = {};
  for (const s of suggestions) {
    for (const sug of s.suggestions) {
      if (!byCategory[sug.category]) byCategory[sug.category] = [];
      byCategory[sug.category].push(s);
    }
  }

  // Build collab suggestions for each category with multiple hits
  for (const [category, entries] of Object.entries(byCategory)) {
    if (entries.length >= 2) {
      const agents = [...new Set(entries.map((e) => e.source_agent))];
      if (agents.length >= 2) {
        collabs.push({
          agent: agents.join(', '),
          category,
          reason: `发现 ${entries.length} 条相关记录，关键词: ${entries.map((e) => e.matched_keywords).flat().join(', ')}`,
          score: entries.length / suggestions.length,
        });
      }
    }
  }

  // Sort by score descending
  collabs.sort((a, b) => b.score - a.score);
  return collabs;
}
