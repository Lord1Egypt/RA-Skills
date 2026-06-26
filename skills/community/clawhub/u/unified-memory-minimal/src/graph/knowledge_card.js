/**
 * Knowledge Card - Summarize entities as shareable knowledge cards
 * 
 * Generates "knowledge cards" that summarize entities extracted from memories.
 * Each card: { entity, type, description, related_memories, last_updated }
 * 
 * @module graph/knowledge_card
 */

import { getAllMemories, getMemory } from '../storage.js';
import { existsSync, mkdirSync, writeFileSync } from 'fs';
import { join } from 'path';
import { config } from '../config.js';

/** @type {Map<string, string>} */
const ENTITY_COLORS = {
  person: '#667eea',
  project: '#10b981',
  tool: '#f59e0b',
  time: '#ef4444',
  action: '#8b5cf6',
};

/**
 * @typedef {Object} KnowledgeCard
 * @property {string} entity
 * @property {string} type
 * @property {string} description
 * @property {string[]} related_memories
 * @property {string} last_updated
 */

/**
 * @typedef {Object} CardExportOptions
 * @property {string} [output_dir]
 * @property {'markdown'|'json'|'feishu'|'text'} [format]
 */

/**
 * Format an ISO date string to a readable string.
 * @param {string} dateStr
 * @returns {string}
 */
function formatDate(dateStr) {
  if (!dateStr) return '未知时间';
  try {
    const d = new Date(dateStr);
    return d.toISOString().slice(0, 16).replace('T', ' ');
  } catch {
    return dateStr.slice(0, 10) || '未知时间';
  }
}

/**
 * Generate importance stars from a 0-1 score.
 * @param {number} importance
 * @returns {string}
 */
function importanceStars(importance) {
  const stars = Math.round((importance || 0.5) * 5);
  return '⭐'.repeat(Math.max(0, Math.min(5, stars)));
}

/**
 * Find all memories related to an entity (by text match).
 * @param {string} entityName
 * @param {Array<{id: string, text: string, tags?: string[]}>} memories
 * @returns {Array<{id: string, text: string, tags?: string[]}>}
 */
function findRelatedMemories(entityName, memories) {
  return memories.filter((m) => (m.text || '').includes(entityName));
}

/**
 * Generate a description for an entity based on its related memories.
 * @param {string} entityName
 * @param {Array<{id: string, text: string}>} relatedMemories
 * @returns {string}
 */
function generateDescription(entityName, relatedMemories) {
  if (relatedMemories.length === 0) {
    return `暂无关于「${entityName}」的记忆。`;
  }
  // Use the first memory text as the description base
  const firstText = relatedMemories[0].text || '';
  return firstText.slice(0, 200) + (firstText.length > 200 ? '...' : '');
}

/**
 * Build a knowledge card for a single entity.
 * @param {string} entity
 * @param {string} type
 * @param {Array<{id: string, text: string, tags?: string[]}>} [relatedMemories]
 * @returns {KnowledgeCard}
 */
export function buildCard(entity, type, relatedMemories = []) {
  if (!relatedMemories || relatedMemories.length === 0) {
    const allMems = getAllMemories();
    relatedMemories = findRelatedMemories(entity, allMems);
  }

  // Sort by most recent
  relatedMemories.sort((a, b) => (b.created_at || 0) - (a.created_at || 0));

  const description = generateDescription(entity, relatedMemories);
  const memoryIds = relatedMemories.map((m) => m.id);
  const lastUpdated = relatedMemories.length > 0
    ? formatDate(String(relatedMemories[0].created_at || ''))
    : new Date().toISOString().slice(0, 16).replace('T', ' ');

  return {
    entity,
    type,
    description,
    related_memories: memoryIds,
    last_updated: lastUpdated,
  };
}

/**
 * Build knowledge cards for all entities in the memory store.
 * @returns {KnowledgeCard[]}
 */
export function buildAllCards() {
  const memories = getAllMemories();
  const seen = new Map(); // entityName -> { type, memories }

  // Simple keyword-based entity extraction (same logic as graph.js)
  const ENTITY_KEYWORDS = {
    person: ['用户', '刘总', '我', '你', '他', '她'],
    project: ['项目', '龙宫', '官网', '重构', '开发'],
    tool: ['飞书', '微信', 'QQ', '钉钉', 'Slack'],
    time: ['今天', '明天', '下周', '月', '日'],
    action: ['喜欢', '使用', '决定', '创建', '完成'],
  };

  for (const mem of memories) {
    const text = mem.text || '';
    for (const [type, keywords] of Object.entries(ENTITY_KEYWORDS)) {
      for (const keyword of keywords) {
        if (text.includes(keyword)) {
          if (!seen.has(keyword)) {
            seen.set(keyword, { type, memories: [] });
          }
          seen.get(keyword).memories.push(mem);
        }
      }
    }
  }

  /** @type {KnowledgeCard[]} */
  const cards = [];
  for (const [entity, info] of seen.entries()) {
    // Deduplicate memories by id
    const uniqueMems = [];
    const ids = new Set();
    for (const m of info.memories) {
      if (!ids.has(m.id)) {
        ids.add(m.id);
        uniqueMems.push(m);
      }
    }
    cards.push(buildCard(entity, info.type, uniqueMems));
  }

  return cards;
}

/**
 * Export a knowledge card as Markdown format.
 * @param {KnowledgeCard} card
 * @returns {string}
 */
export function toMarkdown(card) {
  const stars = importanceStars(0.7);
  const tags = card.related_memories.length > 0
    ? `相关记忆: ${card.related_memories.length} 条`
    : '无相关记忆';

  return `### 📚 知识卡片

**实体**: ${card.entity}
**类型**: ${card.type}
**更新时间**: ${card.last_updated}
**相关记忆**: ${tags}

---

${card.description}

---

> 生成时间: ${new Date().toISOString().slice(0, 16).replace('T', ' ')}`;
}

/**
 * Export a knowledge card as plain JSON.
 * @param {KnowledgeCard} card
 * @returns {string}
 */
export function toJson(card) {
  return JSON.stringify(card, null, 2);
}

/**
 * Export a knowledge card as a Feishu interactive card JSON.
 * @param {KnowledgeCard} card
 * @returns {object}
 */
export function toFeishu(card) {
  const description = card.description.length > 200
    ? card.description.slice(0, 200) + '...'
    : card.description;

  return {
    config: { wide_screen_mode: true },
    header: {
      title: { tag: 'plain_text', content: `📚 ${card.entity}` },
      template: 'blue',
    },
    elements: [
      {
        tag: 'div',
        text: { tag: 'lark_md', content: description },
      },
      {
        tag: 'div',
        fields: [
          { is_short: true, text: { tag: 'lark_md', content: `**类型:** ${card.type}` } },
          { is_short: true, text: { tag: 'lark_md', content: `**更新时间:** ${card.last_updated}` } },
        ],
      },
      {
        tag: 'div',
        text: {
          tag: 'lark_md',
          content: `**相关记忆:** ${card.related_memories.length} 条`,
        },
      },
    ],
  };
}

/**
 * Export a knowledge card as plain text.
 * @param {KnowledgeCard} card
 * @returns {string}
 */
export function toText(card) {
  const sep = '='.repeat(50);
  return `${sep}
【${card.entity}】(${card.type})
${sep}

${card.description}

${sep}
更新时间: ${card.last_updated}
相关记忆: ${card.related_memories.length} 条
${sep}`;
}

/**
 * Export a card to a specific format and save to disk.
 * @param {KnowledgeCard} card
 * @param {'markdown'|'json'|'feishu'|'text'} format
 * @param {string} [outputPath]
 * @returns {{ saved: string, preview: string }}
 */
export function exportCard(card, format = 'markdown', outputPath) {
  /** @type {string | object} */
  let content;

  switch (format) {
    case 'markdown':
      content = toMarkdown(card);
      break;
    case 'json':
      content = toJson(card);
      break;
    case 'feishu':
      content = toFeishu(card);
      break;
    case 'text':
      content = toText(card);
      break;
    default:
      content = toMarkdown(card);
  }

  if (!outputPath) {
    const cardsDir = join(config.memoryDir, 'cards');
    if (!existsSync(cardsDir)) {
      mkdirSync(cardsDir, { recursive: true });
    }
    const ext = format === 'feishu' ? 'json' : format;
    outputPath = join(cardsDir, `${card.entity.slice(0, 8)}_${Date.now()}.${ext}`);
  }

  if (format === 'feishu') {
    writeFileSync(outputPath, JSON.stringify(content, null, 2), 'utf8');
  } else {
    writeFileSync(outputPath, String(content), 'utf8');
  }

  const preview = typeof content === 'string'
    ? content.slice(0, 200) + '...'
    : '飞书卡片 JSON';

  return { saved: outputPath, preview };
}

/**
 * Batch export all knowledge cards.
 * @param {'markdown'|'json'|'feishu'|'text'} [format='markdown']
 * @param {string} [outputDir]
 * @returns {{ exported: number, output_dir: string }}
 */
export function batchExport(format = 'markdown', outputDir) {
  const cards = buildAllCards();

  const outPath = outputDir || join(config.memoryDir, 'cards', new Date().toISOString().slice(0, 10));
  if (!existsSync(outPath)) {
    mkdirSync(outPath, { recursive: true });
  }

  let exported = 0;
  for (const card of cards) {
    try {
      exportCard(card, format, join(outPath, `${card.entity.slice(0, 8)}.${format === 'feishu' ? 'json' : format}`));
      exported++;
    } catch {
      // Skip failures
    }
  }

  return { exported, output_dir: outPath };
}
