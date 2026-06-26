/**
 * memory_qa - 记忆智能问答
 * 基于相关记忆回答用户问题
 */

import { getAllMemories } from '../storage.js';
import { hybridSearch } from '../fusion.js';
import { log } from '../config.js';

const MINIMAX_API_KEY = process.env.MINIMAX_API_KEY;
const MINIMAX_BASE_URL = process.env.MINIMAX_API_HOST || 'https://api.minimax.chat';
const LLM_MODEL = 'MiniMax-M2.7'; // user requested minimax-m2.7:cloud

// Simple in-memory LRU cache — server is long-running, so this persists
const llmCache = new Map();
const MAX_CACHE_SIZE = 50;

async function llmChat(prompt) {
  if (!MINIMAX_API_KEY) {
    log('ERROR', 'MINIMAX_API_KEY not set');
    return '抱歉，LLM API 未配置';
  }
  // Cache lookup — same prompt returns instantly
  if (llmCache.has(prompt)) {
    log('INFO', 'LLM cache hit');
    return llmCache.get(prompt);
  }
  try {
    const response = await fetch(`${MINIMAX_BASE_URL}/v1/text/chatcompletion_v2`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${MINIMAX_API_KEY}`
      },
      body: JSON.stringify({
        model: LLM_MODEL,
        messages: [{ role: 'user', content: prompt }],
        stream: false,
        max_tokens: 512
      }),
      signal: AbortSignal.timeout(15000)
    });
    if (!response.ok) throw new Error(`MiniMax ${response.status}`);
    const data = await response.json();
    const answer = data.choices?.[0]?.message?.content || '抱歉，生成答案失败';
    // Store in cache (LRU eviction)
    if (llmCache.size >= MAX_CACHE_SIZE) {
      const firstKey = llmCache.keys().next().value;
      llmCache.delete(firstKey);
    }
    llmCache.set(prompt, answer);
    return answer;
  } catch (err) {
    log('ERROR', `LLM call failed: ${err.message}`);
    return '抱歉，暂时无法连接 LLM 服务';
  }
}

export async function askQuestion({ question }) {
  if (!question) {
    return { content: [{ type: 'text', text: '请提供问题，例如: memory_qa ask --question "我的项目进展如何？"' }] };
  }
  
  log('INFO', `QA: ${question}`);
  
  // Build context first
  const results = await hybridSearch(question, 5, 'bm25');
  
  if (results.length === 0) {
    return {
      content: [{ type: 'text', text: '抱歉，我没有找到相关的记忆来回答您的问题。' }],
      isError: false
    };
  }
  
  // Build context and call LLM
  const context = results.map((r, i) => 
    `[${i + 1}] [${r.memory.category || 'memory'}] ${r.memory.text}`
  ).join('\n');
  
  const prompt = `基于以下记忆内容回答用户问题。如果记忆中没有相关信息，请直接说明你不清楚。

用户问题: ${question}

相关记忆：
${context}

请用简洁的语言回答，引用相关记忆的编号。`;
  
  // llmChat now handles its own cache — second call with same prompt returns instantly
  const answer = await llmChat(prompt);
  
  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        question,
        answer,
        sources: results.map(r => ({
          id: r.memory.id,
          text: r.memory.text.slice(0, 150),
          relevance: Math.round((r.bm25Score || 0.5) * 100) / 100
        }))
      }, null, 2)
    }]
  };
}
