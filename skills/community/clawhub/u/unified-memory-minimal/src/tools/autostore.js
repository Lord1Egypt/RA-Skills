/**
 * autostore.js - 自动存储记忆
 * Ported from Python memory_autostore.py
 * 
 * 对话后自动提取重要信息存入记忆系统
 */

import { addMemory } from '../storage.js';
import { config, log } from '../config.js';

// 敏感词过滤
const SENSITIVE_WORDS = [
  'password', '密码', 'token', '密钥', 'secret', 'api_key',
  '信用卡', '银行卡', '身份证', '手机号', '验证码', 'secret',
  'sk-', 'ak-', 'Bearer'
];

// v2.7.0 Identity 记忆类型提取模式（优先级最高，importance 默认 0.9）
// 使用 [\s\S] 或非贪婪匹配来捕获句中 "我..." 表述
const IDENTITY_PATTERNS = [
  // Identity: "我是...", "我叫...", "我的职业是..."
  { pattern: /(?:^|[，、\n])我(?:是|叫|名字|职业|身份|角色)([^\n，。.!！]{2,50})/m, type: 'identity', label: 'identity' },
  // Preference positive: "我喜欢...", "我爱...", "我偏好..."
  { pattern: /(?:^|[，、\n])我(?:喜欢|爱|偏好|欣赏|想|想要|愿意)([^\n，。.!！]{2,60})/m, type: 'preference', label: 'identity' },
  // Preference negative: "我讨厌...", "我不喜欢..."
  { pattern: /(?:^|[，、\n])我(?:讨厌|厌恶|不喜欢|反感|排斥|烦)([^\n，。.!！]{2,60})/m, type: 'preference', label: 'identity' },
  // Habit: "我习惯...", "我通常...", "我经常..."
  { pattern: /(?:^|[，、\n])我(?:习惯|通常|经常|往往|总是|一般)([^\n，。.!！]{2,60})/m, type: 'habit', label: 'identity' },
  // Requirement: "我需要...", "我必须..."
  { pattern: /(?:^|[，、\n])我(?:需要|必须|得|想要|希望|要求)([^\n，。.!！]{2,60})/m, type: 'requirement', label: 'identity' },
];

// 重要信息提取模式（原有）
const IMPORTANT_PATTERNS = [
  { pattern: /(?:喜欢|偏好|爱|习惯用|用.{0,5}进行)/, category: 'preference' },
  { pattern: /项目.*?(?:名称|类型|进度|状态|负责人)/, category: 'project' },
  { pattern: /(?:决定|确定|选择|采用|使用)/, category: 'decision' },
  { pattern: /(?:会议|生日|截止|安排|计划|预约)/, category: 'event' },
  { pattern: /(?:学到|学会|掌握|了解|发现)/, category: 'learning' },
  { pattern: /(?:技能|能力|可以|能|会)/, category: 'skill' },
];

/**
 * 检查是否包含敏感信息
 */
export function isSensitive(text) {
  const lower = text.toLowerCase();
  for (const word of SENSITIVE_WORDS) {
    if (lower.includes(word.toLowerCase())) {
      return true;
    }
  }
  return false;
}

/**
 * v2.7.0: 提取身份类信息（优先级最高）
 * 匹配 "我..." 句式，标记为 identity/preference/habit/requirement
 * @param {string} text
 * @returns {{ text: string, category: string, source: string, isIdentity: boolean }[]}
 */
export function extractIdentityInfo(text) {
  const results = [];
  for (const { pattern, type } of IDENTITY_PATTERNS) {
    const matches = text.matchAll(new RegExp(pattern, 'gm'));
    for (const match of matches) {
      const content = (match[1] || '').trim();
      if (content.length >= 2) {
        results.push({
          text: content,
          category: type, // identity, preference, habit, requirement
          source: 'identity-extract',
          isIdentity: true,
        });
      }
    }
  }
  return results;
}

/**
 * 提取重要信息（规则方式）
 */
export function extractImportantInfo(text) {
  const results = [];

  // v2.7.0: 先提取身份类信息（优先级最高）
  const identityResults = extractIdentityInfo(text);
  results.push(...identityResults);

  // 原有模式匹配（跳过 identity 相关避免重复）
  const lines = text.split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.length < 5) continue;

    // 跳过敏感信息
    if (isSensitive(trimmed)) continue;

    // 模式匹配
    for (const { pattern, category } of IMPORTANT_PATTERNS) {
      if (pattern.test(trimmed)) {
        // 提取核心内容
        let content = trimmed;
        const colonIdx = trimmed.indexOf('：');
        if (colonIdx !== -1) {
          content = trimmed.slice(colonIdx + 1).trim();
        } else {
          const colonIdx2 = trimmed.indexOf(':');
          if (colonIdx2 !== -1) {
            content = trimmed.slice(colonIdx2 + 1).trim();
          }
        }

        if (content.length > 3) {
          // 避免与 identity 结果重复
          const isDuplicate = results.some(r => r.text.includes(content) || content.includes(r.text));
          if (!isDuplicate) {
            results.push({
              text: content,
              category,
              source: 'auto-extract',
              isIdentity: false,
            });
          }
        }
        break;
      }
    }
  }

  return results;
}

/**
 * 使用 LLM 提取（可选）
 */
export async function extractWithLLM(text) {
  try {
    const prompt = `从以下对话中提取重要信息，输出JSON数组格式（只输出JSON，不要其他内容）：
[
  {"text": "核心内容", "category": "preference|project|decision|event|learning|skill"}
]

对话内容：
${text.slice(0, 1000)}

输出JSON数组：`;

    const response = await fetch(`${config.ollamaUrl}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: config.llmModel,
        prompt,
        stream: false
      })
    });
    
    if (!response.ok) return [];
    
    const data = await response.json();
    const result = data.response || '';
    
    // Try to parse JSON
    const jsonMatch = result.match(/\[.*\]/s);
    if (jsonMatch) {
      try {
        return JSON.parse(jsonMatch[0]);
      } catch {
        return [];
      }
    }
  } catch (err) {
    log('WARN', `LLM extraction failed: ${err.message}`);
  }
  
  return [];
}

/**
 * 自动存储
 */
export async function autoStore(conversation, { useLLM = true, minLength = 5 } = {}) {
  const results = {
    extracted: [],
    stored: 0,
    skipped: 0
  };
  
  // 1. 规则提取
  const extracted = extractImportantInfo(conversation);
  results.extracted.push(...extracted);
  
  // 2. LLM 提取（可选）
  if (useLLM) {
    try {
      const llmExtracted = await extractWithLLM(conversation);
      for (const item of llmExtracted) {
        const exists = results.extracted.some(e => 
          e.text.includes(item.text) || item.text.includes(e.text)
        );
        if (!exists && item.text && item.category) {
          results.extracted.push({
            ...item,
            source: 'llm-extract'
          });
        }
      }
    } catch (err) {
      log('WARN', `LLM extraction skipped: ${err.message}`);
    }
  }
  
  // 3. 存储
  for (const item of results.extracted) {
    const text = item.text;
    
    if (!text || text.length < minLength) {
      results.skipped++;
      continue;
    }
    
    if (isSensitive(text)) {
      results.skipped++;
      continue;
    }
    
    try {
      // v2.7.0: Identity 类信息 importance 默认 0.9，其他 0.6
      const importance = item.isIdentity ? 0.9 : 0.6;
      addMemory({
        text,
        category: item.category || 'general',
        importance,
        tags: [item.source || 'auto', ...(item.isIdentity ? ['identity-auto'] : [])],
      });
      results.stored++;
      log('INFO', `Auto-stored: ${text.slice(0, 40)}... [${item.category}] importance=${importance}`);
    } catch (err) {
      log('ERROR', `Auto-store failed: ${err.message}`);
      results.skipped++;
    }
  }
  
  return results;
}

/**
 * CLI entry
 */
export async function cmdAutoStore(args) {
  const { conversation, file, noLLM } = args;
  
  let text = conversation || '';
  
  if (file) {
    try {
      const { readFileSync } = await import('fs');
      text = readFileSync(file, 'utf-8');
    } catch (err) {
      console.error(`❌ 读取文件失败: ${err.message}`);
      return;
    }
  }
  
  if (!text) {
    console.log('Usage: memory autostore --conversation "对话" 或 --file path.txt');
    return;
  }
  
  console.log(`📝 处理对话 (${text.length} 字符)...`);
  
  const results = await autoStore(text, { useLLM: !noLLM });
  
  console.log(`\n📊 结果:`);
  console.log(`   提取: ${results.extracted.length} 条`);
  console.log(`   存储: ${results.stored} 条`);
  console.log(`   跳过: ${results.skipped} 条`);
}
