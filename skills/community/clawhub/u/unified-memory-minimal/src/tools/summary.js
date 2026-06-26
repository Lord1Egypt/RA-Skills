/**
 * Memory Summary - 记忆摘要生成
 * 
 * 功能:
 * - 多粒度摘要 (short/medium/long)
 * - 批量生成记忆摘要
 * - 知识块摘要
 * 
 * Ported from memory_summary.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const SUMMARY_DIR = join(MEMORY_DIR, 'summaries');
const SUMMARY_CACHE_FILE = join(MEMORY_DIR, 'summary_cache.json');

const OLLAMA_HOST = process.env.OLLAMA_HOST || 'http://localhost:11434';
const OLLAMA_LLM_MODEL = process.env.OLLAMA_LLM_MODEL || 'deepseek-v3.2:cloud';

const SUMMARY_PROMPTS = {
  short: '用一句话概括以下内容的要点（不超过50字）：\n\n{text}',
  medium: '用一段话概括以下内容的要点（150字以内）：\n\n{text}',
  long: '详细概括以下内容，包括主要观点和关键信息（300字以内）：\n\n{text}'
};

// ============================================================
// MemorySummarizer
// ============================================================

export class MemorySummarizer {
  constructor() {
    this.cache = this._loadCache();
    mkdirSync(SUMMARY_DIR, { recursive: true });
  }

  _loadCache() {
    if (existsSync(SUMMARY_CACHE_FILE)) {
      try { return JSON.parse(readFileSync(SUMMARY_CACHE_FILE, 'utf-8')); } catch { /* ignore */ }
    }
    return { summaries: {} };
  }

  _saveCache() {
    writeFileSync(SUMMARY_CACHE_FILE, JSON.stringify(this.cache, null, 2), 'utf-8');
  }

  /**
   * Get summary from Ollama LLM
   * @param {string} text
   * @param {string} style
   */
  async _getSummaryFromOllama(text, style = 'medium') {
    if (text.length < 100) return text.slice(0, 100);

    const prompt = SUMMARY_PROMPTS[style] || SUMMARY_PROMPTS.medium;
    const fullPrompt = prompt.replace('{text}', text.slice(0, 1000));

    try {
      const response = await fetch(`${OLLAMA_HOST}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: OLLAMA_LLM_MODEL,
          prompt: fullPrompt,
          stream: false,
          options: { temperature: 0.3 }
        }),
        signal: AbortSignal.timeout(30000)
      });

      if (response.ok) {
        const data = await response.json();
        const summary = (data.response || '').trim();
        return summary.slice(0, 500) || null;
      }
    } catch { /* ignore */ }
    return null;
  }

  /**
   * Extract key sentences (rule-based)
   * @param {string} text
   * @param {number} maxSentences
   */
  _extractKeySentences(text, maxSentences = 3) {
    const sentences = text.replace(/\n/g, '。').split('。').filter(s => s.trim().length > 10);
    if (!sentences.length) return text.slice(0, 100);

    const keywords = new Set(['决定', '选择', '偏好', '重要', '关键', '核心', '主要', '需要', '应该']);
    const scored = [];

    for (let i = 0; i < sentences.length; i++) {
      let score = 0;
      const sent = sentences[i];
      for (const kw of keywords) {
        if (sent.includes(kw)) score += 2;
      }
      if (i < 3) score += 1; // Position bonus
      scored.push({ score, sent });
    }

    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, maxSentences).map(s => s.sent).join('。') + '。';
  }

  /**
   * Generate summary for a text
   * @param {string} text
   * @param {string} style
   * @param {boolean} useLLM
   */
  async generateSummary(text, style = 'medium', useLLM = true) {
    const cacheKey = `${text.slice(0, 50)}_${style}`;
    if (this.cache.summaries && this.cache.summaries[cacheKey]) {
      return this.cache.summaries[cacheKey];
    }

    let summary = '';

    if (useLLM) {
      try {
        summary = await this._getSummaryFromOllama(text, style) || '';
      } catch { /* ignore */ }
    }

    if (!summary) {
      // Fallback: rule-based
      if (style === 'short') summary = this._extractKeySentences(text, 1).slice(0, 50);
      else if (style === 'long') summary = this._extractKeySentences(text, 5).slice(0, 300);
      else summary = this._extractKeySentences(text, 3).slice(0, 150);
    }

    if (!this.cache.summaries) this.cache.summaries = {};
    this.cache.summaries[cacheKey] = summary;
    this._saveCache();

    return summary;
  }

  /**
   * Summarize a memory by ID
   * @param {string} memoryId
   * @param {string} style
   */
  async summarizeMemory(memoryId, style = 'medium') {
    let text = '';

    // Try loading from storage
    try {
      const { getMemory } = require('../storage.js');
      const mem = getMemory(memoryId);
      if (mem) text = mem.text || '';
    } catch {
      // Try loading from file
      const memoryFile = join(MEMORY_DIR, 'memories.json');
      if (existsSync(memoryFile)) {
        try {
          const data = JSON.parse(readFileSync(memoryFile, 'utf-8'));
          const mems = Array.isArray(data) ? data : (data.memories || []);
          const mem = mems.find(m => m.id === memoryId);
          if (mem) text = mem.text || '';
        } catch { /* ignore */ }
      }
    }

    if (!text) return null;

    const summary = await this.generateSummary(text, style);

    // Save to file
    const summaryFile = join(SUMMARY_DIR, `${memoryId}.json`);
    writeFileSync(summaryFile, JSON.stringify({
      memory_id: memoryId,
      style,
      summary,
      original_length: text.length,
      summary_length: summary.length,
      generated_at: new Date().toISOString()
    }, null, 2), 'utf-8');

    return summary;
  }

  /**
   * Batch summarize memories
   * @param {number} limit
   * @param {string} style
   */
  async batchSummarize(limit = 10, style = 'medium') {
    /** @type {Array} */
    let memories = [];

    try {
      const { getAllMemories } = require('../storage.js');
      memories = getAllMemories().slice(0, limit);
    } catch {
      const memoryFile = join(MEMORY_DIR, 'memories.json');
      if (existsSync(memoryFile)) {
        try {
          const data = JSON.parse(readFileSync(memoryFile, 'utf-8'));
          memories = (Array.isArray(data) ? data : (data.memories || [])).slice(0, limit);
        } catch { /* ignore */ }
      }
    }

    const results = [];
    for (const mem of memories) {
      const summary = await this.generateSummary(mem.text || '', style);
      results.push({
        memory_id: mem.id,
        summary,
        text_preview: ((mem.text || '').slice(0, 50)) + (((mem.text || '').length > 50) ? '...' : '')
      });
    }

    return {
      total: memories.length,
      generated: results.length,
      results
    };
  }
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string} command
 * @param {object} args
 * @returns {Promise<object>}
 */
export async function cmdSummary(command, args) {
  const summarizer = new MemorySummarizer();

  switch (command) {
    case 'generate': {
      if (!args.id) return { error: '请提供 --id' };
      const summary = await summarizer.summarizeMemory(args.id, args.style || 'medium');
      if (summary === null) return { error: '记忆不存在' };
      if (args.json) return { type: 'json', data: { memory_id: args.id, style: args.style || 'medium', summary } };
      return { type: 'text', text: `📝 摘要 (${args.style || 'medium'}):\n${summary}` };
    }

    case 'batch': {
      const result = await summarizer.batchSummarize(parseInt(args.limit) || 10, args.style || 'medium');
      if (args.json) return { type: 'json', data: result };
      const lines = [`📦 批量摘要 (limit=${args.limit || 10}, style=${args.style || 'medium'})`, '', `总数: ${result.total}`, `生成: ${result.generated}`];
      result.results.slice(0, 5).forEach(r => lines.push(`\n${r.memory_id.slice(0, 8)}...\n${r.summary.slice(0, 60)}...`));
      return { type: 'text', text: lines.join('\n') };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { MemorySummarizer, cmdSummary };
