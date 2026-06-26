/**
 * Fallback Handler - 降级处理 v0.0.7
 * 
 * Provides degraded services when dependencies are unavailable:
 * - LanceDB unavailable → JSON file storage
 * - Ollama unavailable → Rule-based extraction
 * - Ontology unavailable → Pure vector search
 * 
 * Usage:
 *   node fallback_handler.js check     # 检查依赖状态
 *   node fallback_handler.js status    # 查看降级状态
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';
import http from 'http';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ========== Configuration ==========

const WORKSPACE = path.join(os.homedir(), '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const FALLBACK_FILE = path.join(MEMORY_DIR, 'memories.json');

// ========== Dependency Detection ==========

async function checkDependencies() {
  const deps = {
    lancedb: false,
    requests: false,
    ollama: false,
    ontology: false
  };
  
  // Check LanceDB
  try {
    // Would try to import lancedb
    deps.lancedb = false; // Not available in Node.js by default
  } catch {}
  
  // Check requests
  try {
    // Node.js has built-in http
    deps.requests = true;
  } catch {}
  
  // Check Ollama
  const OLLAMA_URL = process.env.OLLAMA_HOST || 'http://localhost:11434';
  try {
    const result = await new Promise((resolve) => {
      const req = http.get(`${OLLAMA_URL}/api/tags`, { timeout: 2000 }, (res) => {
        resolve(res.statusCode === 200);
      });
      req.on('error', () => resolve(false));
      req.on('timeout', () => resolve(false));
    });
    deps.ollama = result;
  } catch {}
  
  // Check Ontology (check if ontology skill exists)
  const ontologyPath = path.join(WORKSPACE, 'skills', 'ontology');
  try {
    await fs.access(ontologyPath);
    deps.ontology = true;
  } catch {}
  
  return deps;
}

// ========== JSON Storage (LanceDB Fallback) ==========

class JSONStorage {
  constructor() {
    this.file = FALLBACK_FILE;
  }
  
  async _ensureFile() {
    await fs.mkdir(path.dirname(this.file), { recursive: true });
    try {
      await fs.access(this.file);
    } catch {
      await fs.writeFile(this.file, '[]', 'utf-8');
    }
  }
  
  async load() {
    try {
      await this._ensureFile();
      const content = await fs.readFile(this.file, 'utf-8');
      return JSON.parse(content);
    } catch {
      return [];
    }
  }
  
  async save(memories) {
    await this._ensureFile();
    await fs.writeFile(this.file, JSON.stringify(memories, null, 2), 'utf-8');
  }
  
  async add(memory) {
    const memories = await this.load();
    memories.push(memory);
    await this.save(memories);
  }
  
  async delete(memoryId) {
    const memories = await this.load();
    const filtered = memories.filter(m => m.id !== memoryId);
    await this.save(filtered);
  }
  
  async search(query, limit = 10) {
    const memories = await this.load();
    const queryLower = query.toLowerCase();
    
    const results = [];
    for (const mem of memories) {
      const text = (mem.text || '').toLowerCase();
      if (text.includes(queryLower)) {
        results.push(mem);
      }
    }
    
    // Sort by importance
    results.sort((a, b) => (b.importance || 0.5) - (a.importance || 0.5));
    return results.slice(0, limit);
  }
}

// ========== Rule-based Extraction (Ollama Fallback) ==========

class RuleExtractor {
  constructor() {
    this.patterns = {
      preference: [
        /(?:我|用户)?(?:偏好|喜欢|想要)([^。！？\n]+)/,
        /(?:I\s+)?(?:prefer|like|want)\s+([^.!?\n]+)/i
      ],
      decision: [
        /(?:决定|确认|选择)([^。！？\n]+)/,
        /(?:decide|confirm|choose)\s+([^.!?\n]+)/i
      ],
      fact: [
        /(?:是|有|位于)([^。！？\n]{5,})/,
        /(?:is|has|located)\s+([^.!?\n]+)/i
      ],
      entity: [
        /(?:项目|公司|团队)[：:]\s*([^\n]+)/,
        /(?:project|company|team)[::]\s*([^\n]+)/i
      ]
    };
  }
  
  extract(text) {
    const memories = [];
    const textLower = text.toLowerCase();
    
    for (const [category, patterns] of Object.entries(this.patterns)) {
      for (const pattern of patterns) {
        const match = text.match(pattern);
        if (match) {
          memories.push({
            category,
            text: match[0],
            source: 'rule',
            importance: this._calculateImportance(category)
          });
          break;
        }
      }
    }
    
    // Check for decision keywords
    if (/(?:决定|选择|确认)/.test(text)) {
      if (!memories.some(m => m.category === 'decision')) {
        memories.push({
          category: 'decision',
          text: text.slice(0, 100),
          source: 'keyword',
          importance: 0.8
        });
      }
    }
    
    // Check for important keywords
    if (/(?:重要|关键|必须)/.test(text)) {
      memories.push({
        category: 'important',
        text: text.slice(0, 100),
        source: 'keyword',
        importance: 0.7
      });
    }
    
    return memories;
  }
  
  _calculateImportance(category) {
    const scores = {
      decision: 0.8,
      preference: 0.7,
      entity: 0.6,
      fact: 0.5,
      important: 0.7
    };
    return scores[category] || 0.5;
  }
}

// ========== Simple Vector Search (Ontology Fallback) ==========

class SimpleVectorSearch {
  constructor() {
    this.storage = new JSONStorage();
    this.extractor = new RuleExtractor();
  }
  
  async index(text, metadata = {}) {
    const memory = {
      id: `mem_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      text,
      metadata,
      importance: metadata.importance || 0.5,
      indexed_at: new Date().toISOString()
    };
    
    await this.storage.add(memory);
    return memory.id;
  }
  
  async search(query, limit = 5) {
    // Use rule extraction first
    const extracted = this.extractor.extract(query);
    
    // Search in storage
    const results = await this.storage.search(query, limit);
    
    return {
      results,
      extracted,
      method: extracted.length > 0 ? 'rule_based' : 'keyword'
    };
  }
}

// ========== Fallback Manager ==========

class FallbackManager {
  constructor() {
    this.deps = {};
    this.storage = new JSONStorage();
    this.vectorSearch = new SimpleVectorSearch();
    this.extractor = new RuleExtractor();
  }
  
  async checkDependencies() {
    this.deps = await checkDependencies();
    return this.deps;
  }
  
  getFallbackStatus() {
    return {
      lancedb: {
        available: this.deps.lancedb,
        fallback: 'JSONStorage',
        status: this.deps.lancedb ? '✅ 正常' : '⚠️ 降级 (JSON存储)'
      },
      ollama: {
        available: this.deps.ollama,
        fallback: 'RuleExtractor',
        status: this.deps.ollama ? '✅ 正常' : '⚠️ 降级 (规则提取)'
      },
      ontology: {
        available: this.deps.ontology,
        fallback: 'SimpleVectorSearch',
        status: this.deps.ontology ? '✅ 正常' : '⚠️ 降级 (简化搜索)'
      },
      requests: {
        available: this.deps.requests,
        fallback: 'Node.js http',
        status: '✅ 正常'
      }
    };
  }
  
  async store(text, metadata = {}) {
    // Always store to JSON fallback
    return this.vectorSearch.index(text, metadata);
  }
  
  async search(query, limit = 5) {
    // Use vector search or fallback
    return this.vectorSearch.search(query, limit);
  }
  
  async extract(conversation) {
    // Use rule extraction (always available)
    return this.extractor.extract(conversation);
  }
}

// ========== CLI ==========

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log(`
Fallback Handler - 降级处理 v0.0.7

Usage:
    node fallback_handler.js check     # 检查依赖状态
    node fallback_handler.js status    # 查看降级状态
    node fallback_handler.js store "内容" # 存储记忆
    node fallback_handler.js search "查询" # 搜索记忆
    node fallback_handler.js extract "对话" # 提取记忆
`);
    process.exit(1);
  }
  
  console.log('🚀 Fallback Handler v0.0.7...\n');
  
  const manager = new FallbackManager();
  await manager.checkDependencies();
  
  switch (command) {
    case 'check': {
      console.log('🔍 依赖检查:\n');
      const status = manager.getFallbackStatus();
      for (const [name, info] of Object.entries(status)) {
        console.log(`  ${name}: ${info.status}`);
      }
      break;
    }
    
    case 'status': {
      console.log('📋 降级状态:\n');
      const status = manager.getFallbackStatus();
      console.log(JSON.stringify(status, null, 2));
      break;
    }
    
    case 'store': {
      const content = args.slice(1).join(' ');
      if (!content) {
        console.log('❌ 请提供内容');
        process.exit(1);
      }
      
      const id = await manager.store(content, { source: 'cli' });
      console.log(`✅ 已存储: ${id}`);
      break;
    }
    
    case 'search': {
      const query = args.slice(1).join(' ') || args[1];
      if (!query) {
        console.log('❌ 请提供查询内容');
        process.exit(1);
      }
      
      const result = await manager.search(query);
      console.log(`📊 搜索结果 (${result.method}):\n`);
      for (const r of result.results.slice(0, 5)) {
        console.log(`  - ${r.text?.slice(0, 60)}... [I=${r.importance}]`);
      }
      break;
    }
    
    case 'extract': {
      const conversation = args.slice(1).join(' ');
      if (!conversation) {
        console.log('❌ 请提供对话内容');
        process.exit(1);
      }
      
      const memories = await manager.extract(conversation);
      console.log(`📝 提取到 ${memories.length} 条记忆:\n`);
      for (const m of memories) {
        console.log(`  [${m.category}] (I=${m.importance}) ${m.text?.slice(0, 60)}...`);
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

export {
  FallbackManager,
  JSONStorage,
  RuleExtractor,
  SimpleVectorSearch,
  checkDependencies
};

export default FallbackManager;
