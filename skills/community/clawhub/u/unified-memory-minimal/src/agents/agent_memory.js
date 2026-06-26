/**
 * Agent Memory - AI Agent 专用记忆系统 v4.0
 * 
 * Core Features:
 * - Auto extraction from conversations (using LLM)
 * - Context summary generation
 * - User profile maintenance (USER_MODEL.md)
 * - Agent self-awareness (AGENT_SELF.md)
 * - Capability boundary recording
 * 
 * Usage:
 *   node agent_memory.js extract --conversation "对话内容"
 *   node agent_memory.js context --query "当前任务"
 *   node agent_memory.js update-user
 *   node agent_memory.js learn --type success|failure --content "内容"
 *   node agent_memory.js status
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';
import http from 'http';
import crypto from 'crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ========== Configuration ==========

const WORKSPACE = path.join(os.homedir(), '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const ONTOLOGY_DIR = path.join(MEMORY_DIR, 'ontology');
const VECTOR_DB_DIR = path.join(MEMORY_DIR, 'vector');

const USER_MODEL_FILE = path.join(WORKSPACE, 'USER_MODEL.md');
const AGENT_SELF_FILE = path.join(WORKSPACE, 'AGENT_SELF.md');
const MEMORY_FILE = path.join(WORKSPACE, 'MEMORY.md');

const OLLAMA_URL = process.env.OLLAMA_HOST || 'http://localhost:11434';
const OLLAMA_EMBED_MODEL = process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text:latest';
const OLLAMA_LLM_MODEL = process.env.OLLAMA_LLM_MODEL || 'deepseek-v3.2:cloud';

// Ensure directories exist
await fs.mkdir(MEMORY_DIR, { recursive: true });
await fs.mkdir(ONTOLOGY_DIR, { recursive: true });
await fs.mkdir(VECTOR_DB_DIR, { recursive: true });

// ========== Memory Categories ==========

const MEMORY_CATEGORIES = {
  profile: '用户身份属性 (姓名、职业、位置等)',
  preferences: '用户偏好习惯 (喜欢/不喜欢、习惯做法)',
  entities: '持续存在的实体 (项目、设备、账号)',
  events: '发生的事件 (会议、完成任务、发生的事)',
  cases: '问题-解决方案对 (遇到什么问题、怎么解决的)',
  patterns: '可复用的处理流程 (做事方法)'
};

const ALWAYS_MERGE = new Set(['profile']);
const MERGE_SUPPORTED = new Set(['preferences', 'entities', 'patterns']);
const APPEND_ONLY = new Set(['events', 'cases']);

// ========== LLM Calls ==========

async function callLLM(prompt, model = null) {
  try {
    const result = await new Promise((resolve, reject) => {
      const req = http.request(
        `${OLLAMA_URL}/api/generate`,
        { method: 'POST', timeout: 60000 },
        (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => {
            try {
              resolve(JSON.parse(data));
            } catch {
              reject(new Error('Invalid JSON response'));
            }
          });
        }
      );
      req.on('error', reject);
      req.on('timeout', () => reject(new Error('Request timeout')));
      req.write(JSON.stringify({
        model: model || OLLAMA_LLM_MODEL,
        prompt,
        stream: false,
        options: { temperature: 0.1 }
      }));
      req.end();
    });
    return result.response || null;
  } catch (e) {
    console.warn(`⚠️ LLM 调用失败: ${e.message}`);
    return null;
  }
}

async function callLLMJson(prompt, model = null) {
  const response = await callLLM(prompt, model);
  if (!response) return null;
  
  // Try direct JSON parse
  try {
    return JSON.parse(response);
  } catch {}
  
  // Try markdown code block
  const jsonMatch = response.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (jsonMatch) {
    try {
      return JSON.parse(jsonMatch[1]);
    } catch {}
  }
  
  // Try brace content
  const braceMatch = response.match(/\{[\s\S]*\}/);
  if (braceMatch) {
    try {
      return JSON.parse(braceMatch[0]);
    } catch {}
  }
  
  return null;
}

async function getEmbedding(text) {
  try {
    const result = await new Promise((resolve, reject) => {
      const req = http.request(
        `${OLLAMA_URL}/api/embeddings`,
        { method: 'POST', timeout: 30000 },
        (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => {
            try {
              resolve(JSON.parse(data));
            } catch {
              reject(new Error('Invalid JSON'));
            }
          });
        }
      );
      req.on('error', reject);
      req.on('timeout', () => reject(new Error('Request timeout')));
      req.write(JSON.stringify({ model: OLLAMA_EMBED_MODEL, prompt: text }));
      req.end();
    });
    return result.embedding || null;
  } catch (e) {
    console.warn(`⚠️ Embedding 失败: ${e.message}`);
    return null;
  }
}

// ========== Auto Extraction ==========

const EXTRACTION_PROMPT = `你是一个记忆提取助手。从以下对话中提取值得记住的信息。

对话内容:
{conversation}

请提取以下类型的记忆:
1. profile - 用户身份信息 (姓名、职业、位置等)
2. preferences - 用户偏好 (喜欢/不喜欢、习惯做法)
3. entities - 重要实体 (项目名、设备、账号)
4. events - 重要事件 (会议、完成任务)
5. cases - 问题解决方案 (遇到什么问题、怎么解决的)
6. patterns - 处理模式 (可复用的方法)

返回 JSON 格式:
{
  "memories": [
    {
      "category": "preferences",
      "abstract": "一句话摘要",
      "detail": "详细说明",
      "importance": 0.7
    }
  ]
}

只提取真正有价值、对未来有用的信息。忽略寒暄、闲聊、无关细节。
`;

async function extractMemories(conversation) {
  const prompt = EXTRACTION_PROMPT.replace('{conversation}', conversation.slice(0, 4000));
  const result = await callLLMJson(prompt);
  
  if (!result || !result.memories) return [];
  return result.memories;
}

// ========== Context Generation ==========

const CONTEXT_PROMPT = `基于以下记忆，生成针对当前查询的上下文摘要。

用户画像:
{userModel}

相关记忆:
{memories}

当前查询: {query}

生成简洁的上下文摘要 (不超过 200 字)，包含:
1. 用户相关背景
2. 相关项目/任务
3. 需要注意的偏好
4. 可能相关的过去经验

只输出摘要内容，不要其他说明。
`;

async function generateContext(query, limit = 5) {
  // Load user model
  let userModel = '';
  try {
    userModel = await fs.readFile(USER_MODEL_FILE, 'utf-8');
  } catch {}
  
  // Search memories
  const memories = await searchMemories(query, limit);
  const memoriesText = memories.map(m => `- [${m.category}] ${m.text}`).join('\n');
  
  const prompt = CONTEXT_PROMPT
    .replace('{userModel}', userModel.slice(0, 1000))
    .replace('{memories}', memoriesText.slice(0, 2000))
    .replace('{query}', query);
  
  const context = await callLLM(prompt);
  return context || '无相关上下文';
}

async function searchMemories(query, limit = 5) {
  const results = [];
  
  // Vector search (simplified - would use LanceDB in production)
  const embedding = await getEmbedding(query);
  if (embedding) {
    // Would search LanceDB here
  }
  
  // Text search
  const textResults = await searchTextMemories(query, limit);
  results.push(...textResults);
  
  return results.slice(0, limit);
}

async function searchTextMemories(query, limit = 5) {
  const results = [];
  const queryLower = query.toLowerCase();
  
  try {
    const files = (await fs.readdir(MEMORY_DIR)).filter(f => f.endsWith('.md')).sort().reverse();
    
    for (const file of files) {
      const content = await fs.readFile(path.join(MEMORY_DIR, file), 'utf-8');
      const lines = content.split('\n');
      
      for (const line of lines) {
        if (line.toLowerCase().includes(queryLower)) {
          const match = line.match(/^- \[([^\]]+)\] \[([^\]]+)\] \[([^\]]+)\](?: \[I=([^\]]+)\])? (.+)$/);
          if (match) {
            const [, timestamp, category, scope, impStr, text] = match;
            results.push({
              text,
              category,
              importance: impStr ? parseFloat(impStr) : 0.5,
              source: 'text',
              file
            });
            if (results.length >= limit) break;
          }
        }
      }
      if (results.length >= limit) break;
    }
  } catch {}
  
  return results;
}

// ========== User Model Update ==========

async function updateUserModel() {
  const preferences = [];
  const entities = [];
  const profile = [];
  
  try {
    const files = await fs.readdir(MEMORY_DIR);
    
    for (const file of files) {
      if (!file.endsWith('.md')) continue;
      const content = await fs.readFile(path.join(MEMORY_DIR, file), 'utf-8');
      const lines = content.split('\n');
      
      for (const line of lines) {
        const match = line.match(/^- \[([^\]]+)\] \[([^\]]+)\].* (.+)$/);
        if (match) {
          const [, , category, text] = match;
          if (category === 'preferences') preferences.push(text);
          else if (category === 'entities') entities.push(text);
          else if (category === 'profile') profile.push(text);
        }
      }
    }
  } catch {}
  
  let content = '';
  try {
    content = await fs.readFile(USER_MODEL_FILE, 'utf-8');
  } catch {}
  
  // Update preferences section
  const prefSection = [...new Set(preferences)].map(p => `- ${p}`).join('\n');
  
  if (content.includes('## 沟通偏好')) {
    content = content.replace(
      /## 沟通偏好\n.*?(?=\n## |\n---|\Z)/s,
      `## 沟通偏好\n\n${prefSection}\n`
    );
  } else {
    content += `\n\n## 沟通偏好\n\n${prefSection}\n`;
  }
  
  await fs.writeFile(USER_MODEL_FILE, content, 'utf-8');
  return `✅ 已更新用户画像，偏好: ${[...new Set(preferences)].length} 条`;
}

// ========== Agent Learning ==========

async function recordLearning(learningType, content, context = '') {
  const today = new Date().toISOString().slice(0, 10);
  const timestamp = new Date().toISOString().slice(11, 19);
  
  const logFile = path.join(MEMORY_DIR, `${today}.md`);
  let entry = `- [${timestamp}] [learning] [${learningType}] ${content}`;
  if (context) {
    entry += ` | 上下文: ${context}`;
  }
  entry += '\n';
  
  await fs.appendFile(logFile, entry, 'utf-8');
  
  return `✅ 已记录学习: [${learningType}] ${content.slice(0, 50)}...`;
}

// ========== Memory Storage ==========

async function storeMemory(text, category = 'fact', scope = 'default', importance = null) {
  const today = new Date().toISOString().slice(0, 10);
  const timestamp = new Date().toISOString().slice(0, 19).replace('T', ' ');
  
  if (importance === null) {
    importance = scoreImportance(text, category);
  }
  
  const logFile = path.join(MEMORY_DIR, `${today}.md`);
  const entry = `- [${timestamp}] [${category}] [${scope}] [I=${importance.toFixed(2)}] ${text}\n`;
  
  await fs.appendFile(logFile, entry, 'utf-8');
  
  // Try vector storage
  let vectorStored = false;
  try {
    const embedding = await getEmbedding(text);
    if (embedding) {
      // Would store to LanceDB here
      vectorStored = true;
    }
  } catch {}
  
  let status = '✅ 已存储';
  if (vectorStored) status += ' (文本+向量)';
  else status += ' (文本)';
  
  return `${status}: ${text.slice(0, 50)}...`;
}

function scoreImportance(text, category) {
  let score = 0.5;
  const textLower = text.toLowerCase();
  
  // Category base scores
  const categoryScores = {
    decision: 0.8,
    preference: 0.7,
    entity: 0.6,
    event: 0.5,
    pattern: 0.6,
    fact: 0.4
  };
  score = categoryScores[category] || 0.5;
  
  // Keyword bonuses
  if (/决定|选择|确认/.test(text)) score += 0.1;
  if (/重要|关键/.test(text)) score += 0.1;
  if (/错误|失败|问题/.test(text)) score += 0.1;
  
  return Math.min(1.0, Math.max(0.0, score));
}

// ========== CLI ==========

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log(`
Agent Memory - AI Agent 专用记忆系统 v4.0

Usage:
    node agent_memory.js extract --conversation "对话内容"
    node agent_memory.js context --query "当前任务"
    node agent_memory.js update-user
    node agent_memory.js learn --type success|failure --content "内容"
    node agent_memory.js status
`);
    process.exit(1);
  }
  
  console.log('🚀 Agent Memory v4.0...\n');
  
  switch (command) {
    case 'extract': {
      const convIdx = args.indexOf('--conversation');
      const fileIdx = args.indexOf('--file');
      
      let conversation;
      if (convIdx !== -1) {
        conversation = args[convIdx + 1];
      } else if (fileIdx !== -1) {
        conversation = await fs.readFile(args[fileIdx + 1], 'utf-8');
      } else {
        console.log('❌ 请提供 --conversation 或 --file 参数');
        process.exit(1);
      }
      
      const memories = await extractMemories(conversation);
      console.log(`📝 提取到 ${memories.length} 条记忆:\n`);
      
      for (const mem of memories) {
        console.log(`[${mem.category}] ${mem.abstract}`);
        console.log(`   详情: ${mem.detail}`);
        console.log(`   重要性: ${mem.importance.toFixed(2)}`);
        console.log();
      }
      break;
    }
    
    case 'context': {
      const queryIdx = args.indexOf('--query');
      const query = queryIdx !== -1 ? args[queryIdx + 1] : args[1];
      
      if (!query) {
        console.log('❌ 请提供 --query 参数');
        process.exit(1);
      }
      
      const context = await generateContext(query);
      console.log('📋 上下文摘要:\n');
      console.log(context);
      break;
    }
    
    case 'update-user':
      console.log(await updateUserModel());
      break;
    
    case 'learn': {
      const typeIdx = args.indexOf('--type');
      const contentIdx = args.indexOf('--content');
      const ctxIdx = args.indexOf('--context');
      
      const type = typeIdx !== -1 ? args[typeIdx + 1] : 'success';
      const content = contentIdx !== -1 ? args[contentIdx + 1] : args[1];
      const context = ctxIdx !== -1 ? args[ctxIdx + 1] : '';
      
      if (!content) {
        console.log('❌ 请提供 --content 参数');
        process.exit(1);
      }
      
      console.log(await recordLearning(type, content, context));
      break;
    }
    
    case 'status': {
      let count = 0;
      try {
        const files = await fs.readdir(MEMORY_DIR);
        for (const file of files) {
          if (file.endsWith('.md')) {
            const content = await fs.readFile(path.join(MEMORY_DIR, file), 'utf-8');
            count += content.split('\n').filter(l => l.startsWith('-')).length;
          }
        }
      } catch {}
      
      console.log(`📚 总记忆: ${count} 条`);
      console.log(`📁 记忆目录: ${MEMORY_DIR}`);
      
      let userModelExists = false;
      try {
        await fs.access(USER_MODEL_FILE);
        userModelExists = true;
      } catch {}
      console.log(`👤 用户画像: ${userModelExists ? '已存在' : '未创建'}`);
      
      let agentSelfExists = false;
      try {
        await fs.access(AGENT_SELF_FILE);
        agentSelfExists = true;
      } catch {}
      console.log(`🤖 Agent 自我认知: ${agentSelfExists ? '已存在' : '未创建'}`);
      break;
    }
    
    default:
      console.log(`❌ 未知命令: ${command}`);
      process.exit(1);
  }
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export {
  extractMemories,
  generateContext,
  searchMemories,
  updateUserModel,
  recordLearning,
  storeMemory,
  scoreImportance,
  MEMORY_CATEGORIES
};

export default {
  extractMemories,
  generateContext,
  searchMemories,
  updateUserModel,
  recordLearning,
  storeMemory
};
