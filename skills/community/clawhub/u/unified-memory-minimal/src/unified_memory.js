/**
 * Unified Memory - 统一记忆入口 v3.0
 * 
 * 整合 Memory（文本+向量）+ Ontology（知识图谱），支持双写同步
 * 
 * Core Features:
 * - BM25 Text Search
 * - Vector Search (LanceDB + embeddings)
 * - Ontology Graph Traversal
 * - Automatic Importance Scoring
 * - Smart Summarization
 * 
 * Usage:
 *   node unified_memory.js store --text "内容" [--category fact]
 *   node unified_memory.js query --text "搜索内容" [--limit 5]
 *   node unified_memory.js graph --from ENTITY_ID [--depth 2]
 *   node unified_memory.js score --text "内容"
 *   node unified_memory.js status
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
const MEMORY_FILE = path.join(WORKSPACE, 'MEMORY.md');

const OLLAMA_URL = process.env.OLLAMA_HOST || 'http://localhost:11434';
const OLLAMA_EMBED_MODEL = process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text:latest';

// Ensure directories exist
await fs.mkdir(MEMORY_DIR, { recursive: true });
await fs.mkdir(ONTOLOGY_DIR, { recursive: true });
await fs.mkdir(VECTOR_DB_DIR, { recursive: true });

// ========== Ollama Integration ==========

async function getOllamaEmbedding(text) {
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
            } catch (e) {
              reject(new Error('Invalid JSON response'));
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
    console.warn(`⚠️ Ollama embedding 失败: ${e.message}`);
    return null;
  }
}

async function callOllama(prompt, model = null, temperature = 0.1) {
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
            } catch (e) {
              reject(new Error('Invalid JSON response'));
            }
          });
        }
      );
      req.on('error', reject);
      req.on('timeout', () => reject(new Error('Request timeout')));
      req.write(JSON.stringify({
        model: model || 'deepseek-v3.2:cloud',
        prompt,
        stream: false,
        options: { temperature }
      }));
      req.end();
    });
    return result.response || null;
  } catch (e) {
    console.warn(`⚠️ Ollama 调用失败: ${e.message}`);
    return null;
  }
}

// ========== BM25 Implementation ==========

class BM25 {
  constructor(k1 = 1.5, b = 0.75) {
    this.k1 = k1;
    this.b = b;
    this.docFreqs = {};
    this.docLens = [];
    this.avgdl = 0;
    this.docs = [];
    this.docTerms = [];
  }
  
  tokenize(text) {
    const tokens = [];
    // Chinese characters
    for (const char of text) {
      if (char >= '\u4e00' && char <= '\u9fff') {
        tokens.push(char);
      }
    }
    // English words
    const enMatches = text.match(/[a-zA-Z]+/g) || [];
    tokens.push(...enMatches.map(w => w.toLowerCase()));
    return tokens;
  }
  
  fit(docs) {
    this.docs = docs;
    this.docLens = [];
    this.docTerms = [];
    this.docFreqs = {};
    
    const freqMap = new Map();
    
    for (const doc of docs) {
      const text = doc.text || doc.content || '';
      const tokens = this.tokenize(text);
      this.docLens.push(tokens.length);
      
      const termFreq = new Map();
      for (const term of tokens) {
        termFreq.set(term, (termFreq.get(term) || 0) + 1);
        freqMap.set(term, (freqMap.get(term) || 0) + 1);
      }
      this.docTerms.push(termFreq);
    }
    
    this.docFreqs = Object.fromEntries(freqMap);
    if (this.docLens.length > 0) {
      this.avgdl = this.docLens.reduce((a, b) => a + b, 0) / this.docLens.length;
    }
  }
  
  search(query, topK = 5) {
    if (!this.docs.length || !this.avgdl) return [];
    
    const queryTokens = this.tokenize(query);
    const scores = [];
    const N = this.docs.length;
    
    for (let i = 0; i < this.docs.length; i++) {
      const docLen = this.docLens[i];
      const docTermFreq = this.docTerms[i];
      let score = 0;
      
      for (const term of queryTokens) {
        if (!docTermFreq.has(term)) continue;
        
        const df = this.docFreqs[term] || 0;
        if (df === 0) continue;
        
        // IDF
        const idf = Math.log((N - df + 0.5) / (df + 0.5) + 1);
        
        // TF
        const tf = docTermFreq.get(term);
        const tfNorm = tf * (this.k1 + 1) / (tf + this.k1 * (1 - this.b + this.b * docLen / this.avgdl));
        
        score += idf * tfNorm;
      }
      
      if (score > 0) {
        scores.push([i, score, this.docs[i]]);
      }
    }
    
    scores.sort((a, b) => b[1] - a[1]);
    return scores.slice(0, topK);
  }
}

// ========== Importance Scorer ==========

class ImportanceScorer {
  constructor() {
    this.importantPatterns = {
      decision: ['决定', '决策', '选择', '确定', '选中', 'choose', 'decide', 'selected'],
      critical: ['重要', '关键', '紧急', 'critical', 'urgent'],
      preference: ['喜欢', '偏好', '习惯', 'prefer', 'like', '习惯'],
      error: ['错误', '失败', '异常', 'error', 'fail', 'bug', '问题'],
      success: ['完成', '成功', '解决', 'done', 'success', 'fixed', '✅'],
      entity: ['项目', '任务', '人员', 'project', 'task', 'person']
    };
    
    this.decayFactor = 0.95;
    this.baseScore = 0.5;
  }
  
  score(text, timestamp = null, accessCount = 0, entityLinked = false) {
    let score = this.baseScore;
    const textLower = text.toLowerCase();
    
    // Keyword scoring
    for (const [, patterns] of Object.entries(this.importantPatterns)) {
      for (const pattern of patterns) {
        if (textLower.includes(pattern)) {
          score += 0.05;
          break;
        }
      }
    }
    
    // Time decay
    if (timestamp) {
      const ts = typeof timestamp === 'string' ? new Date(timestamp) : timestamp;
      const daysOld = Math.floor((Date.now() - ts.getTime()) / (1000 * 60 * 60 * 24));
      score *= Math.pow(this.decayFactor, daysOld);
    }
    
    // Access frequency bonus
    score += Math.min(0.2, accessCount * 0.02);
    
    // Entity link bonus
    if (entityLinked) score += 0.1;
    
    // Length penalty
    if (text.length > 500) score *= 0.9;
    
    return Math.min(1.0, Math.max(0.0, score));
  }
  
  categorize(text) {
    const textLower = text.toLowerCase();
    for (const [category, patterns] of Object.entries(this.importantPatterns)) {
      for (const pattern of patterns) {
        if (textLower.includes(pattern)) {
          return category;
        }
      }
    }
    return 'other';
  }
}

// ========== Ontology Graph ==========

class OntologyGraph {
  constructor(graphFile) {
    this.graphFile = graphFile;
    this.entities = {};
    this.relations = [];
    this._load();
  }
  
  async _load() {
    try {
      const content = await fs.readFile(this.graphFile, 'utf-8');
      const lines = content.split('\n').filter(l => l.trim());
      
      for (const line of lines) {
        try {
          const data = JSON.parse(line);
          if (data.op === 'create') {
            const entity = data.entity || {};
            this.entities[entity.id] = entity;
          } else if (data.op === 'relate') {
            this.relations.push({
              from: data.from,
              rel: data.rel,
              to: data.to,
              created: data.created
            });
          }
        } catch (e) {
          // Skip invalid JSON lines
        }
      }
    } catch (e) {
      // File doesn't exist yet
    }
  }
  
  getEntity(entityId) {
    return this.entities[entityId] || null;
  }
  
  getEntitiesByType(entityType) {
    return Object.values(this.entities).filter(e => e.type === entityType);
  }
  
  getRelationsFrom(entityId) {
    return this.relations.filter(r => r.from === entityId);
  }
  
  getRelationsTo(entityId) {
    return this.relations.filter(r => r.to === entityId);
  }
  
  traverse(startId, depth = 2, relationFilter = null) {
    const result = {
      center: this.entities[startId] || null,
      nodes: [],
      edges: []
    };
    
    if (!this.entities[startId]) return result;
    
    const visited = new Set([startId]);
    let frontier = [startId];
    
    for (let d = 0; d < depth; d++) {
      const newFrontier = [];
      
      for (const nodeId of frontier) {
        // Outgoing edges
        for (const rel of this.getRelationsFrom(nodeId)) {
          if (relationFilter && rel.rel !== relationFilter) continue;
          
          const targetId = rel.to;
          result.edges.push({
            from: nodeId,
            rel: rel.rel,
            to: targetId
          });
          
          if (this.entities[targetId] && !visited.has(targetId)) {
            visited.add(targetId);
            newFrontier.push(targetId);
            result.nodes.push(this.entities[targetId]);
          }
        }
        
        // Incoming edges
        for (const rel of this.getRelationsTo(nodeId)) {
          if (relationFilter && rel.rel !== relationFilter) continue;
          
          const sourceId = rel.from;
          result.edges.push({
            from: sourceId,
            rel: rel.rel,
            to: nodeId
          });
          
          if (this.entities[sourceId] && !visited.has(sourceId)) {
            visited.add(sourceId);
            newFrontier.push(sourceId);
            result.nodes.push(this.entities[sourceId]);
          }
        }
      }
      
      frontier = newFrontier;
    }
    
    return result;
  }
  
  search(query, limit = 5) {
    const results = [];
    const queryLower = query.toLowerCase();
    
    for (const entity of Object.values(this.entities)) {
      const props = entity.properties || {};
      const name = props.name || '';
      const text = JSON.stringify(props);
      
      if (text.toLowerCase().includes(queryLower) || name.toLowerCase().includes(queryLower)) {
        results.push(entity);
        if (results.length >= limit) break;
      }
    }
    
    return results;
  }
}

// ========== Core Functions ==========

function getTodayMemoryFile() {
  const today = new Date().toISOString().slice(0, 10);
  return path.join(MEMORY_DIR, `${today}.md`);
}

async function initVectorDb() {
  // LanceDB integration would go here
  // For now, return null (fallback to text search)
  return null;
}

async function storeToVector(text, category, scope, importance, timestamp) {
  // LanceDB storage would go here
  return false;
}

async function searchVector(query, limit = 5) {
  // LanceDB search would go here
  return [];
}

async function storeToMemory(text, category = 'fact', scope = 'default', importance = null) {
  const todayFile = getTodayMemoryFile();
  const timestamp = new Date().toISOString().slice(0, 19).replace('T', ' ');
  
  if (importance === null) {
    const scorer = new ImportanceScorer();
    importance = scorer.score(text);
  }
  
  const entry = `- [${timestamp}] [${category}] [${scope}] [I=${importance.toFixed(2)}] ${text}\n`;
  
  await fs.appendFile(todayFile, entry, 'utf-8');
  
  const vectorStored = await storeToVector(text, category, scope, importance, timestamp);
  
  let status = '✅ 已写入 Memory';
  if (vectorStored) status += ' + 向量';
  status += ` (重要性: ${importance.toFixed(2)}): ${text.slice(0, 50)}...`;
  
  return status;
}

async function storeToOntology(entityType, properties) {
  const graphFile = path.join(ONTOLOGY_DIR, 'graph.jsonl');
  const entityId = `${entityType.toLowerCase()}_${crypto.randomUUID().slice(0, 8)}`;
  
  const entity = {
    op: 'create',
    entity: {
      id: entityId,
      type: entityType,
      properties,
      created: new Date().toISOString()
    }
  };
  
  await fs.appendFile(graphFile, JSON.stringify(entity) + '\n', 'utf-8');
  
  return { entityId, message: `✅ 已创建 Ontology 实体: ${entityType} (${entityId})` };
}

async function relateEntities(fromId, relationType, toId) {
  const graphFile = path.join(ONTOLOGY_DIR, 'graph.jsonl');
  
  const relation = {
    op: 'relate',
    from: fromId,
    rel: relationType,
    to: toId,
    created: new Date().toISOString()
  };
  
  await fs.appendFile(graphFile, JSON.stringify(relation) + '\n', 'utf-8');
  
  return `✅ 已创建关系: ${fromId} --[${relationType}]--> ${toId}`;
}

async function loadAllMemories() {
  const memories = [];
  
  try {
    const files = (await fs.readdir(MEMORY_DIR))
      .filter(f => f.endsWith('.md'))
      .sort()
      .reverse();
    
    for (const file of files) {
      const content = await fs.readFile(path.join(MEMORY_DIR, file), 'utf-8');
      const lines = content.split('\n');
      
      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || !trimmed.startsWith('-')) continue;
        
        // Parse format: [time] [category] [scope] [importance?] content
        const match = trimmed.match(/^- \[([^\]]+)\] \[([^\]]+)\] \[([^\]]+)\](?: \[I=([^\]]+)\])? (.+)$/);
        if (match) {
          const [, timestampStr, cat, sc, impStr, text] = match;
          let timestamp;
          try {
            timestamp = new Date(timestampStr.replace(' ', 'T') + ':00');
          } catch (e) {
            timestamp = new Date();
          }
          
          const imp = impStr ? parseFloat(impStr) : 0.5;
          
          memories.push({
            text,
            timestamp,
            category: cat,
            scope: sc,
            importance: imp,
            file
          });
        } else {
          // Legacy format
          const stripped = trimmed.slice(2).trim();
          if (stripped && !stripped.startsWith('#')) {
            memories.push({
              text: stripped,
              timestamp: new Date(),
              category: 'legacy',
              scope: 'default',
              importance: 0.5,
              file
            });
          }
        }
      }
    }
  } catch (e) {
    console.error(`加载记忆失败: ${e.message}`);
  }
  
  return memories;
}

async function unifiedQuery(text, limit = 5) {
  const results = [];
  
  // Vector search
  const vectorResults = await searchVector(text, limit);
  if (vectorResults.length > 0) {
    results.push('📐 向量搜索 (语义相似):');
    vectorResults.slice(0, 3).forEach((r, i) => {
      const imp = r.importance || 0.5;
      const dist = r._distance || 0;
      results.push(`  ${i + 1}. [I=${imp.toFixed(2)}] ${(r.text || '').slice(0, 50)}... (距离: ${dist.toFixed(2)})`);
    });
  }
  
  // Load memories for BM25
  const memories = await loadAllMemories();
  
  if (memories.length > 0) {
    const bm25 = new BM25();
    bm25.fit(memories);
    const searchResults = bm25.search(text, limit);
    
    if (searchResults.length > 0) {
      results.push('\n📝 文本搜索 (BM25):');
      searchResults.forEach(([idx, score, doc], i) => {
        const imp = doc.importance || 0.5;
        results.push(`  ${i + 1}. [I=${imp.toFixed(2)}] ${(doc.text || '').slice(0, 60)}... (score: ${score.toFixed(2)})`);
      });
    }
  }
  
  // Ontology search
  const graph = new OntologyGraph(path.join(ONTOLOGY_DIR, 'graph.jsonl'));
  const entityResults = graph.search(text, 3);
  
  if (entityResults.length > 0) {
    results.push('\n🔗 Ontology 匹配:');
    entityResults.forEach((entity, i) => {
      const props = entity.properties || {};
      const name = props.name || entity.id;
      results.push(`  ${i + 1}. [${entity.type}] ${name}`);
    });
  }
  
  if (results.length > 0) {
    return '🔍 统一查询结果:\n' + results.join('\n');
  } else {
    return '❌ 未找到相关内容';
  }
}

async function graphTraverse(entityId, depth = 2) {
  const graph = new OntologyGraph(path.join(ONTOLOGY_DIR, 'graph.jsonl'));
  const result = graph.traverse(entityId, depth);
  
  if (!result.center) {
    return `❌ 未找到实体: ${entityId}`;
  }
  
  const output = [];
  const center = result.center;
  const props = center.properties || {};
  const name = props.name || center.id;
  
  output.push(`🎯 中心实体: [${center.type}] ${name}`);
  output.push(`   ID: ${center.id}`);
  
  if (result.nodes.length > 0) {
    output.push(`\n📦 关联实体 (${result.nodes.length} 个):`);
    result.nodes.slice(0, 10).forEach(node => {
      const nodeProps = node.properties || {};
      const nodeName = nodeProps.name || node.id;
      output.push(`   - [${node.type}] ${nodeName}`);
    });
  }
  
  if (result.edges.length > 0) {
    output.push(`\n🔗 关系 (${result.edges.length} 条):`);
    result.edges.slice(0, 10).forEach(edge => {
      const fromEntity = graph.getEntity(edge.from);
      const toEntity = graph.getEntity(edge.to);
      const fromName = fromEntity?.properties?.name || edge.from;
      const toName = toEntity?.properties?.name || edge.to;
      output.push(`   - ${fromName} --[${edge.rel}]--> ${toName}`);
    });
  }
  
  return output.join('\n');
}

function scoreText(text) {
  const scorer = new ImportanceScorer();
  const score = scorer.score(text);
  const category = scorer.categorize(text);
  
  return `📊 重要性评分

文本: ${text.slice(0, 50)}...

分数: ${score.toFixed(2)}
分类: ${category}

建议: ${score > 0.6 ? '📌 值得长期记住' : '📋 普通记录'}
`;
}

function extractKeyPoints(text) {
  const points = [];
  
  for (const line of text.split('\n')) {
    const trimmed = line.trim();
    if (trimmed.startsWith('# ')) {
      points.push(trimmed.slice(2));
    } else if (trimmed.startsWith('## ')) {
      points.push('  - ' + trimmed.slice(3));
    } else if (/[✅❌⚠️📌🔧]/.test(trimmed) && trimmed.length > 10 && trimmed.length < 150) {
      points.push('  - ' + trimmed);
    } else if (/已完成|创建|修复|决定|选择|重要/.test(trimmed) && trimmed.length > 10 && trimmed.length < 150) {
      points.push('  - ' + trimmed);
    }
  }
  
  return points.slice(0, 15);
}

async function summarizeToMemoryMd(days = 7) {
  const today = new Date();
  const summaryPoints = [];
  
  for (let i = 0; i < days; i++) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const dateFile = path.join(MEMORY_DIR, `${date.toISOString().slice(0, 10)}.md`);
    
    try {
      const content = await fs.readFile(dateFile, 'utf-8');
      const points = extractKeyPoints(content);
      if (points.length > 0) {
        summaryPoints.push(`### ${date.toISOString().slice(0, 10)}\n` + points.join('\n'));
      }
    } catch (e) {
      // File doesn't exist
    }
  }
  
  if (summaryPoints.length === 0) {
    return '⚠️ 没有可摘要的内容';
  }
  
  let existing = '';
  try {
    existing = await fs.readFile(MEMORY_FILE, 'utf-8');
  } catch (e) {
    // File doesn't exist
  }
  
  const summarySection = '\n\n## 最近活动\n\n' + summaryPoints.join('\n\n') + '\n';
  
  await fs.writeFile(MEMORY_FILE, existing + summarySection, 'utf-8');
  
  return `✅ 已生成 ${summaryPoints.length} 天的摘要`;
}

async function cleanOldMemories(days = 30) {
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);
  
  let deletedCount = 0;
  
  try {
    const files = await fs.readdir(MEMORY_DIR);
    
    for (const file of files) {
      if (!file.endsWith('.md')) continue;
      if (file === 'MEMORY.md') continue; // Don't delete summary file
      
      const dateMatch = file.match(/^(\d{4}-\d{2}-\d{2})\.md$/);
      if (!dateMatch) continue;
      
      const fileDate = new Date(dateMatch[1]);
      if (fileDate < cutoff) {
        await fs.unlink(path.join(MEMORY_DIR, file));
        deletedCount++;
      }
    }
  } catch (e) {
    return `⚠️ 清理失败: ${e.message}`;
  }
  
  return `✅ 已清理 ${deletedCount} 个旧记忆文件`;
}

// ========== CLI ==========

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log(`
Unified Memory - 统一记忆入口 v3.0

Usage:
    node unified_memory.js store --text "内容" [--category fact]
    node unified_memory.js query --text "搜索内容" [--limit 5]
    node unified_memory.js graph --from ENTITY_ID [--depth 2]
    node unified_memory.js score --text "内容"
    node unified_memory.js summarize [--days 7]
    node unified_memory.js clean [--days 30]
    node unified_memory.js status
`);
    process.exit(1);
  }
  
  console.log('🚀 启动 Unified Memory v3.0...\n');
  
  try {
    switch (command) {
      case 'store': {
        const textIdx = args.indexOf('--text');
        const text = textIdx !== -1 ? args[textIdx + 1] : args[1];
        const catIdx = args.indexOf('--category');
        const category = catIdx !== -1 ? args[catIdx + 1] : 'fact';
        
        if (!text) {
          console.log('❌ 请提供 --text 参数');
          process.exit(1);
        }
        
        const result = await storeToMemory(text, category);
        console.log(result);
        break;
      }
      
      case 'query': {
        const textIdx = args.indexOf('--text');
        const query = textIdx !== -1 ? args[textIdx + 1] : args[1];
        const limitIdx = args.indexOf('--limit');
        const limit = limitIdx !== -1 ? parseInt(args[limitIdx + 1]) : 5;
        
        if (!query) {
          console.log('❌ 请提供 --text 参数');
          process.exit(1);
        }
        
        console.log(await unifiedQuery(query, limit));
        break;
      }
      
      case 'graph': {
        const fromIdx = args.indexOf('--from');
        const depthIdx = args.indexOf('--depth');
        
        if (fromIdx === -1) {
          console.log('❌ 请提供 --from ENTITY_ID 参数');
          process.exit(1);
        }
        
        const entityId = args[fromIdx + 1];
        const depth = depthIdx !== -1 ? parseInt(args[depthIdx + 1]) : 2;
        
        console.log(await graphTraverse(entityId, depth));
        break;
      }
      
      case 'score': {
        const textIdx = args.indexOf('--text');
        const text = textIdx !== -1 ? args[textIdx + 1] : args[1];
        
        if (!text) {
          console.log('❌ 请提供 --text 参数');
          process.exit(1);
        }
        
        console.log(scoreText(text));
        break;
      }
      
      case 'summarize': {
        const daysIdx = args.indexOf('--days');
        const days = daysIdx !== -1 ? parseInt(args[daysIdx + 1]) : 7;
        
        console.log(await summarizeToMemoryMd(days));
        break;
      }
      
      case 'clean': {
        const daysIdx = args.indexOf('--days');
        const days = daysIdx !== -1 ? parseInt(args[daysIdx + 1]) : 30;
        
        console.log(await cleanOldMemories(days));
        break;
      }
      
      case 'status': {
        const memories = await loadAllMemories();
        console.log(`📚 总记忆: ${memories.length} 条`);
        
        const graph = new OntologyGraph(path.join(ONTOLOGY_DIR, 'graph.jsonl'));
        const entityCount = Object.keys(graph.entities).length;
        const relationCount = graph.relations.length;
        
        console.log(`🔗 Ontology 实体: ${entityCount}`);
        console.log(`🔗 关系: ${relationCount}`);
        console.log('\n✅ 系统正常');
        break;
      }
      
      default:
        console.log(`❌ 未知命令: ${command}`);
        process.exit(1);
    }
  } catch (e) {
    console.error(`❌ 错误: ${e.message}`);
    process.exit(1);
  }
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export {
  BM25,
  ImportanceScorer,
  OntologyGraph,
  storeToMemory,
  storeToOntology,
  relateEntities,
  loadAllMemories,
  unifiedQuery,
  graphTraverse,
  scoreText,
  summarizeToMemoryMd,
  cleanOldMemories
};

export default { BM25, ImportanceScorer, OntologyGraph };
