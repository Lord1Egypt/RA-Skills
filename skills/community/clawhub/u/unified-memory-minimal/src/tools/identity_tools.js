/**
 * identity_tools.js — MCP Tools for Identity Memory
 * Part of Feature: Identity Memory Type (v2.7.0)
 *
 * Implements MCP tools:
 * - memory_identity_extract: Extract identity/preference/habit from text
 * - memory_identity_update: Update identity memories with importance=0.9
 * - memory_identity_get: Get a summary of user's identity profile
 *
 * Extraction rules:
 * - "我喜欢/讨厌..." → preference/dislike
 * - "我是..." → identity
 * - "我习惯..." → habit
 * - "我需要..." → requirement
 */

import { addMemory, getAllMemories, updateMemory, getMemory } from '../storage.js';

// ============ Extraction Rules ============

/** @type {{ pattern: RegExp, type: string, label: string, subType?: string }[]} */
const IDENTITY_PATTERNS = [
  // Identity: "我是...", "我叫...", "我的职业是..."
  { pattern: /(?:^|[，、\n])我(?:是|叫|名字|职业|身份|角色)([^\n，。.!！]{2,50})/m, type: 'identity', label: '身份描述' },
  // Preference positive: "我喜欢...", "我爱...", "我偏好..."
  { pattern: /(?:^|[，、\n])我(?:喜欢|爱|偏好|欣赏|想|想要|愿意)([^\n，。.!！]{2,60})/m, type: 'preference', label: '喜好', subType: 'like' },
  // Preference negative: "我讨厌...", "我不喜欢...", "我厌恶..."
  { pattern: /(?:^|[，、\n])我(?:讨厌|厌恶|不喜欢|反感|排斥|烦)([^\n，。.!！]{2,60})/m, type: 'preference', label: '厌恶', subType: 'dislike' },
  // Habit: "我习惯...", "我通常...", "我经常..."
  { pattern: /(?:^|[，、\n])我(?:习惯|通常|经常|往往|总是|一般)([^\n，。.!！]{2,60})/m, type: 'habit', label: '习惯' },
  // Requirement: "我需要...", "我必须...", "我想要..."
  { pattern: /(?:^|[，、\n])我(?:需要|必须|得|想要|希望|要求)([^\n，。.!！]{2,60})/m, type: 'requirement', label: '需求' },
  // Skill: "我会...", "我能...", "我擅长..."
  { pattern: /(?:^|[，、\n])我(?:会|能|擅长|懂得|可以)([^\n，。.!！]{2,60})/m, type: 'skill', label: '技能' },
  // Goal: "我的目标是...", "我想..."
  { pattern: /(?:^|[，、\n])(?:我的)?目标(?:是|)([^\n，。.!！]{2,60})/m, type: 'goal', label: '目标' },
];

/**
 * Extract identity-related statements from text
 * @param {string} text
 * @returns {{ type: string, label: string, content: string, subType?: string }[]}
 */
export function extractIdentityStatements(text) {
  const results = [];
  for (const { pattern, type, label, subType } of IDENTITY_PATTERNS) {
    const matches = text.matchAll(new RegExp(pattern, 'gm'));
    for (const match of matches) {
      const content = (match[1] || '').trim();
      if (content.length >= 2) {
        results.push({
          type,
          label,
          content,
          subType: subType || null,
          fullMatch: match[0].trim(),
        });
      }
    }
  }
  return results;
}

/**
 * Get importance score based on identity type
 * Identity type always gets 0.9+, others get 0.9
 * @param {string} type
 * @returns {number}
 */
function getIdentityImportance(type) {
  if (type === 'identity') return 0.95;
  return 0.9;
}

// ============ MCP Tools ============

/**
 * Tool: memory_identity_extract
 * Extract identity/preference/habit/requirement from text
 */
export function memoryIdentityExtractTool({ text }) {
  try {
    if (!text || !text.trim()) {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({ count: 0, extractions: [], summary: 'No text provided' }, null, 2),
        }],
      };
    }

    const extractions = extractIdentityStatements(text);

    // Deduplicate by content
    const seen = new Set();
    const unique = extractions.filter(e => {
      const key = `${e.type}:${e.content}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });

    // Group by type for summary
    const byType = {};
    for (const e of unique) {
      if (!byType[e.type]) byType[e.type] = [];
      byType[e.type].push(e.content);
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          count: unique.length,
          extractions: unique.map(e => ({
            type: e.type,
            label: e.label,
            content: e.content,
            subType: e.subType,
            suggested_importance: getIdentityImportance(e.type),
          })),
          by_type: Object.fromEntries(
            Object.entries(byType).map(([k, v]) => [k, { count: v.length, samples: v.slice(0, 3) }])
          ),
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Identity extract error: ${err.message}` }], isError: true };
  }
}

/**
 * Tool: memory_identity_update
 * Store extracted identity statements as high-priority memories
 * Always uses importance=0.9+
 */
export function memoryIdentityUpdateTool({ extractions }) {
  try {
    if (!extractions || !Array.isArray(extractions) || extractions.length === 0) {
      return {
        content: [{ type: 'text', text: JSON.stringify({ stored: 0, error: 'No extractions provided' }, null, 2) }],
        isError: true,
      };
    }

    const stored = [];
    const errors = [];

    for (const ex of extractions) {
      try {
        const content = ex.content || ex.text || '';
        const type = ex.type || 'identity';
        if (!content || content.length < 2) continue;

        const importance = ex.importance || getIdentityImportance(type);

        const mem = addMemory({
          text: content,
          category: type, // identity, preference, habit, requirement, skill, goal
          importance,
          tags: ['identity', ex.label || type, ...(ex.subType ? [ex.subType] : [])],
        });
        stored.push({ id: mem.id, type, content: content.slice(0, 50) });
      } catch (err) {
        errors.push({ extraction: ex, error: err.message });
      }
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          success: true,
          stored: stored.length,
          memories: stored,
          errors: errors.length > 0 ? errors : undefined,
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Identity update error: ${err.message}` }], isError: true };
  }
}

/**
 * Tool: memory_identity_get
 * Get a summary of the user's identity profile from stored identity memories
 */
export async function memoryIdentityGetTool({ type } = {}) {
  try {
    const allMemories = await getAllMemories();

    // Identity-related categories
    const identityCategories = ['identity', 'preference', 'habit', 'requirement', 'skill', 'goal'];

    let identityMemories;
    if (type) {
      identityMemories = allMemories.filter(m => m.category === type);
    } else {
      identityMemories = allMemories.filter(m => identityCategories.includes(m.category));
    }

    // Sort by importance desc, then by updated_at desc
    identityMemories.sort((a, b) => {
      if (b.importance !== a.importance) return b.importance - a.importance;
      return (b.updated_at || 0) - (a.updated_at || 0);
    });

    // Group by category
    const byCategory = {};
    for (const m of identityMemories) {
      if (!byCategory[m.category]) byCategory[m.category] = [];
      byCategory[m.category].push({
        id: m.id,
        text: m.text,
        importance: m.importance,
        tags: m.tags || [],
        updated_at: new Date(m.updated_at || m.created_at).toISOString(),
      });
    }

    // Build a readable summary
    const summaryParts = [];
    const categoryLabels = {
      identity: '👤 身份',
      preference: '❤️ 偏好/喜好',
      habit: '🔄 习惯',
      requirement: '📌 需求',
      skill: '💡 技能',
      goal: '🎯 目标',
    };

    for (const [cat, memories] of Object.entries(byCategory)) {
      const label = categoryLabels[cat] || cat;
      summaryParts.push(`\n## ${label} (${memories.length}条)`);
      for (const m of memories.slice(0, 10)) {
        summaryParts.push(`- ${m.text} [重要性:${Math.round(m.importance * 100)}%, ID:${m.id.slice(0, 12)}]`);
      }
    }

    const summary = summaryParts.length > 0
      ? summaryParts.join('\n')
      : '暂无身份信息记录。';

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          total: identityMemories.length,
          by_category: Object.fromEntries(
            Object.entries(byCategory).map(([k, v]) => [k, v.length])
          ),
          summary,
          memories: Object.fromEntries(
            Object.entries(byCategory).map(([k, v]) => [k, v.slice(0, 20)])
          ),
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Identity get error: ${err.message}` }], isError: true };
  }
}

export default {
  memoryIdentityExtractTool,
  memoryIdentityUpdateTool,
  memoryIdentityGetTool,
};
