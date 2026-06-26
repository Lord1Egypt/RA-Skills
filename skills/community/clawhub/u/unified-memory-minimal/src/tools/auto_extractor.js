/**
 * Auto Extractor - 自动记忆提取器
 * 
 * Features:
 * - 从对话中自动提取重要信息
 * - 使用 LLM 识别记忆候选
 * - 自动分类和评分
 * - 敏感信息脱敏
 * 
 * Usage:
 *   node auto_extractor.js extract --conversation "对话内容"
 *   node auto_extractor.js extract --file conversation.txt
 *   node auto_extractor.js batch --dir ./conversations/
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
const VECTOR_DB_DIR = path.join(WORKSPACE, 'memory', 'vector');

const OLLAMA_URL = process.env.OLLAMA_HOST || 'http://localhost:11434';
const OLLAMA_LLM_MODEL = process.env.OLLAMA_LLM_MODEL || 'deepseek-v3.2:cloud';
const OLLAMA_EMBED_MODEL = process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text:latest';

// ========== Sensitive Patterns ==========

const SENSITIVE_PATTERNS = {
  password: [
    /password["\s:=]+["']?([^"\s,}]+)/gi,
    /passwd["\s:=]+["']?([^"\s,}]+)/gi,
    /pwd["\s:=]+["']?([^"\s,}]+)/gi
  ],
  api_key: [
    /api[_-]?key["\s:=]+["']?([^"\s,}]+)/gi,
    /apikey["\s:=]+["']?([^"\s,}]+)/gi
  ],
  secret: [
    /secret["\s:=]+["']?([^"\s,}]+)/gi,
    /private[_-]?key["\s:=]+["']?([^"\s,}]+)/gi,
    /token["\s:=]+["']?([^"\s,}]+)/gi
  ],
  credential: [
    /credential["\s:=]+["']?([^"\s,}]+)/gi,
    /auth["\s:=]+["']?([^"\s,}]+)/gi
  ]
};

// ========== Memory Categories ==========

const MEMORY_CATEGORIES = {
  preference: ['偏好', '喜欢', '不喜欢', '想要', 'prefer', 'like', 'want'],
  fact: ['是', '有', '位于', 'is', 'has', 'located', '成立于'],
  decision: ['决定', '选择', '确认', 'decide', 'choose', 'confirm'],
  entity: ['项目', '公司', '团队', 'project', 'company', 'team'],
  task: ['任务', '待办', '需要', 'task', 'todo', 'need'],
  event: ['会议', '时间', '日期', 'meeting', 'time', 'date']
};

// ========== Sensitive Filter ==========

class SensitiveFilter {
  constructor() {
    this.patterns = SENSITIVE_PATTERNS;
    this.redactedCount = 0;
  }
  
  sanitize(text) {
    const redactions = [];
    
    for (const [category, patterns] of Object.entries(this.patterns)) {
      for (const pattern of patterns) {
        let match;
        while ((match = pattern.exec(text)) !== null) {
          const original = match[0];
          const sensitiveValue = match[1] || '';
          
          if (sensitiveValue && sensitiveValue.length > 2) {
            // Keep first 2 and last 1 characters
            const masked = sensitiveValue.slice(0, 2) + '***REDACTED***' + sensitiveValue.slice(-1);
            const redacted = original.replace(sensitiveValue, masked);
            text = text.replace(original, redacted);
            
            redactions.push({
              category,
              original_length: sensitiveValue.length,
              position: match.index
            });
            this.redactedCount++;
          }
        }
      }
    }
    
    return { text, redactions };
  }
  
  checkSensitive(text) {
    for (const patterns of Object.values(this.patterns)) {
      for (const pattern of patterns) {
        if (pattern.test(text)) return true;
      }
    }
    return false;
  }
}

// ========== Auto Extractor ==========

class AutoExtractor {
  constructor() {
    this.sensitiveFilter = new SensitiveFilter();
    this.extractionCount = 0;
  }
  
  async extractFromConversation(conversation, useLLM = true) {
    const memories = [];
    
    // 1. Rule extraction (fast)
    const ruleMemories = this._extractByRules(conversation);
    memories.push(...ruleMemories);
    
    // 2. LLM extraction (deep) - would call Ollama here
    if (useLLM) {
      try {
        const llmMemories = await this._extractByLLM(conversation);
        memories.push(...llmMemories);
      } catch (e) {
        console.warn(`LLM extraction failed: ${e.message}`);
      }
    }
    
    // 3. Deduplicate and score
    const deduplicated = this._deduplicate(memories);
    const scored = this._scoreMemories(deduplicated, conversation);
    
    this.extractionCount += scored.length;
    return scored;
  }
  
  _extractByRules(conversation) {
    const memories = [];
    const lines = conversation.split('\n');
    
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      
      // Check for category keywords
      for (const [category, keywords] of Object.entries(MEMORY_CATEGORIES)) {
        for (const keyword of keywords) {
          if (trimmed.includes(keyword)) {
            // Sanitize sensitive info
            const { text } = this.sensitiveFilter.sanitize(trimmed);
            
            memories.push({
              category,
              text,
              source: 'rule',
              matched_keyword: keyword,
              importance: this._calculateImportance(text, category)
            });
            break;
          }
        }
      }
      
      // Check for decisions (contains "决定" or "选择")
      if (/决定|选择|确认/.test(trimmed)) {
        const { text } = this.sensitiveFilter.sanitize(trimmed);
        memories.push({
          category: 'decision',
          text,
          source: 'rule',
          matched_keyword: '决定',
          importance: 0.8
        });
      }
      
      // Check for entities (contains project/company names)
      const entityMatch = trimmed.match(/(?:项目|产品|系统)[：:]\s*([^\n，,。]+)/);
      if (entityMatch) {
        const { text } = this.sensitiveFilter.sanitize(entityMatch[0]);
        memories.push({
          category: 'entity',
          text: entityMatch[0],
          source: 'rule',
          matched_keyword: 'entity',
          importance: 0.6
        });
      }
    }
    
    return memories;
  }
  
  async _extractByLLM(conversation) {
    // Would call Ollama LLM for extraction
    // For now, return empty array (rule extraction handles most cases)
    return [];
  }
  
  _deduplicate(memories) {
    const seen = new Map();
    
    for (const mem of memories) {
      const key = mem.text.slice(0, 50).toLowerCase();
      if (!seen.has(key)) {
        seen.set(key, mem);
      } else {
        // Keep higher importance
        const existing = seen.get(key);
        if (mem.importance > existing.importance) {
          seen.set(key, mem);
        }
      }
    }
    
    return Array.from(seen.values());
  }
  
  _scoreMemories(memories, conversation) {
    return memories.map(mem => ({
      ...mem,
      importance: mem.importance * this._calculateRecencyScore(conversation),
      extracted_at: new Date().toISOString()
    }));
  }
  
  _calculateImportance(text, category) {
    let score = 0.5;
    
    // Category base scores
    const categoryScores = {
      decision: 0.9,
      preference: 0.7,
      entity: 0.6,
      fact: 0.5,
      task: 0.6,
      event: 0.4
    };
    score = categoryScores[category] || 0.5;
    
    // Length bonus (detailed content is usually more important)
    if (text.length > 20) score += 0.1;
    if (text.length > 100) score += 0.1;
    
    // Keyword bonus
    if (/重要|关键|必须|一定要/.test(text)) score += 0.2;
    if (/记得|不要忘记|别忘了/.test(text)) score += 0.15;
    
    return Math.min(1.0, Math.max(0.0, score));
  }
  
  _calculateRecencyScore(conversation) {
    // Check if conversation mentions recent time
    if (/今天|刚才|刚刚|现在/.test(conversation)) {
      return 1.2;
    }
    if (/昨天|前天/.test(conversation)) {
      return 1.0;
    }
    if (/上周|上周/.test(conversation)) {
      return 0.8;
    }
    return 1.0;
  }
  
  async storeExtractedMemories(memories) {
    const results = [];
    
    for (const mem of memories) {
      if (mem.importance < 0.3) continue; // Skip low importance
      
      const today = new Date().toISOString().slice(0, 10);
      const timestamp = new Date().toISOString().slice(11, 19);
      const logFile = path.join(MEMORY_DIR, `${today}.md`);
      
      const entry = `- [${timestamp}] [${mem.category}] [extracted] [I=${mem.importance.toFixed(2)}] ${mem.text}\n`;
      
      try {
        await fs.appendFile(logFile, entry, 'utf-8');
        results.push({ success: true, memory: mem });
      } catch (e) {
        results.push({ success: false, error: e.message });
      }
    }
    
    return results;
  }
}

// ========== CLI ==========

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log(`
Auto Extractor - 自动记忆提取器

Usage:
    node auto_extractor.js extract --conversation "对话内容"
    node auto_extractor.js extract --file conversation.txt
    node auto_extractor.js batch --dir ./conversations/
    node auto_extractor.js test --text "我决定了做这个项目"
`);
    process.exit(1);
  }
  
  console.log('🚀 Auto Extractor...\n');
  
  const extractor = new AutoExtractor();
  
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
      
      const memories = await extractor.extractFromConversation(conversation);
      
      console.log(`📝 提取到 ${memories.length} 条记忆:\n`);
      
      for (const mem of memories) {
        console.log(`[${mem.category}] (I=${mem.importance.toFixed(2)})`);
        console.log(`   ${mem.text.slice(0, 80)}${mem.text.length > 80 ? '...' : ''}`);
        console.log();
      }
      
      // Ask to store
      if (memories.length > 0 && args.includes('--store')) {
        const results = await extractor.storeExtractedMemories(memories);
        const stored = results.filter(r => r.success).length;
        console.log(`✅ 已存储 ${stored}/${memories.length} 条记忆`);
      }
      break;
    }
    
    case 'batch': {
      const dirIdx = args.indexOf('--dir');
      if (dirIdx === -1) {
        console.log('❌ 请提供 --dir 参数');
        process.exit(1);
      }
      
      const dir = args[dirIdx + 1];
      const files = (await fs.readdir(dir)).filter(f => f.endsWith('.txt'));
      
      console.log(`📁 处理 ${files.length} 个文件...\n`);
      
      let totalMemories = 0;
      for (const file of files) {
        const conversation = await fs.readFile(path.join(dir, file), 'utf-8');
        const memories = await extractor.extractFromConversation(conversation);
        console.log(`  ${file}: ${memories.length} 条记忆`);
        totalMemories += memories.length;
        
        if (args.includes('--store')) {
          await extractor.storeExtractedMemories(memories);
        }
      }
      
      console.log(`\n✅ 共提取 ${totalMemories} 条记忆`);
      break;
    }
    
    case 'test': {
      const textIdx = args.indexOf('--text');
      const text = textIdx !== -1 ? args[textIdx + 1] : '';
      
      if (!text) {
        console.log('❌ 请提供 --text 参数');
        process.exit(1);
      }
      
      const { text: sanitized, redactions } = extractor.sensitiveFilter.sanitize(text);
      
      console.log('🧪 敏感信息检测:\n');
      console.log(`原始: ${text}`);
      console.log(`脱敏: ${sanitized}`);
      console.log(`检测到: ${redactions.length} 处`);
      
      for (const r of redactions) {
        console.log(`  - ${r.category}: ${r.original_length} 字符`);
      }
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

export { AutoExtractor, SensitiveFilter };

export default AutoExtractor;
