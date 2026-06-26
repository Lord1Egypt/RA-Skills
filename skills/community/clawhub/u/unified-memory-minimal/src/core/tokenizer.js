/**
 * tokenizer.js - 智能分块系统
 * 借鉴 QMD 的断点检测算法，实现自然语义分块
 * Ported from Python smart_chunk.py
 */

import { regexMatch } from '../utils/text.js';

// 断点类型和分数
const BREAK_TYPES = {
  h1: 100,
  h2: 90,
  h3: 80,
  h4: 70,
  h5: 60,
  h6: 50,
  codeblock: 80,
  hr: 60,
  blank: 20,
  list: 5,
  numlist: 5,
  newline: 1
};

/**
 * 找出所有代码块区域（这些区域内的内容不应被切断）
 */
function findCodeFences(text) {
  const regions = [];
  const fencePattern = /```/g;
  let match;
  
  while ((match = fencePattern.exec(text)) !== null) {
    if (regions.length % 2 === 0) {
      regions.push({ start: match.index, end: null });
    } else {
      regions[regions.length - 1].end = match.index + 3;
    }
  }
  
  // 未闭合的代码块
  if (regions.length % 2 !== 0) {
    regions[regions.length - 1].end = text.length;
  }
  
  return regions;
}

/**
 * 判断位置是否在代码块内
 */
function isInCodeFence(pos, fences) {
  for (const fence of fences) {
    if (pos >= fence.start && pos < fence.end) {
      return true;
    }
  }
  return false;
}

/**
 * 查找所有断点
 */
function findBreakpoints(text, maxTokens = 900) {
  const breakpoints = [];
  const fences = findCodeFences(text);
  
  // 标题断点
  const h1Pattern = /^# .+$/gm;
  const h2Pattern = /^## .+$/gm;
  const h3Pattern = /^### .+$/gm;
  const h4Pattern = /^#### .+$/gm;
  const h5Pattern = /^##### .+$/gm;
  const h6Pattern = /^###### .+$/gm;
  
  let m;
  while ((m = h1Pattern.exec(text)) !== null) {
    breakpoints.push({ pos: m.index, score: BREAK_TYPES.h1, type: 'h1' });
  }
  while ((m = h2Pattern.exec(text)) !== null) {
    breakpoints.push({ pos: m.index, score: BREAK_TYPES.h2, type: 'h2' });
  }
  while ((m = h3Pattern.exec(text)) !== null) {
    breakpoints.push({ pos: m.index, score: BREAK_TYPES.h3, type: 'h3' });
  }
  while ((m = h4Pattern.exec(text)) !== null) {
    breakpoints.push({ pos: m.index, score: BREAK_TYPES.h4, type: 'h4' });
  }
  while ((m = h5Pattern.exec(text)) !== null) {
    breakpoints.push({ pos: m.index, score: BREAK_TYPES.h5, type: 'h5' });
  }
  while ((m = h6Pattern.exec(text)) !== null) {
    breakpoints.push({ pos: m.index, score: BREAK_TYPES.h6, type: 'h6' });
  }
  
  // 代码块
  while ((m = /\n```/g.exec(text)) !== null) {
    if (!isInCodeFence(m.index, fences)) {
      breakpoints.push({ pos: m.index, score: BREAK_TYPES.codeblock, type: 'codeblock' });
    }
  }
  
  // 水平线
  while ((m = /\n(?:---|\*\*\*|___)\s*\n/g.exec(text)) !== null) {
    breakpoints.push({ pos: m.index, score: BREAK_TYPES.hr, type: 'hr' });
  }
  
  // 空行
  while ((m = /\n\n+/g.exec(text)) !== null) {
    breakpoints.push({ pos: m.index + 1, score: BREAK_TYPES.blank, type: 'blank' });
  }
  
  // 排序
  breakpoints.sort((a, b) => a.pos - b.pos);
  
  return breakpoints;
}

/**
 * 估算token数（简单按中英文混合估算）
 */
function estimateTokens(text) {
  const chinese = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const english = (text.match(/[a-zA-Z]+/g) || []).join('').length;
  const other = text.length - chinese - english;
  return Math.ceil(chinese * 1.5 + english * 0.25 + other * 0.5);
}

/**
 * 智能分块
 */
export function smartChunk(text, maxTokens = 900) {
  if (!text || text.trim().length === 0) {
    return [];
  }
  
  const breakpoints = findBreakpoints(text, maxTokens);
  const chunks = [];
  
  let chunkStart = 0;
  let currentTokens = 0;
  let currentChunk = '';
  
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    currentChunk += char;
    
    // 估算token
    if (/[\u4e00-\u9fff]/.test(char)) {
      currentTokens += 1.5;
    } else if (/[a-zA-Z]/.test(char)) {
      currentTokens += 0.25;
    } else {
      currentTokens += 0.5;
    }
    
    // 检查是否该分块
    if (currentTokens >= maxTokens) {
      // 找最近的断点
      const candidates = breakpoints.filter(bp => bp.pos > chunkStart && bp.pos < i);
      
      if (candidates.length > 0) {
        // 在最佳断点处切断
        const bestBp = candidates.reduce((best, c) => c.score > best.score ? c : best);
        const cutPos = bestBp.pos;
        chunks.push(text.slice(chunkStart, cutPos).trim());
        i = cutPos - 1;
      } else {
        // 硬切断
        chunks.push(currentChunk.trim());
      }
      
      currentTokens = 0;
      currentChunk = '';
      chunkStart = i + 1;
    }
  }
  
  // 剩余内容
  if (currentChunk.trim().length > 0) {
    chunks.push(currentChunk.trim());
  }
  
  return chunks.filter(c => c.length > 0);
}

/**
 * 简单分词（中英文）
 */
export function tokenize(text) {
  const tokens = [];
  
  // 英文单词
  const english = text.match(/[a-zA-Z]+/g) || [];
  tokens.push(...english.map(t => t.toLowerCase()));
  
  // 中文单字
  const chinese = text.match(/[\u4e00-\u9fff]/g) || [];
  tokens.push(...chinese);
  
  // 数字
  const numbers = text.match(/\d+/g) || [];
  tokens.push(...numbers);
  
  return tokens;
}
