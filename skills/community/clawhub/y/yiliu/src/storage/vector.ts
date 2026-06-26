/**
 * 向量存储模块
 * 使用 @llm-tools/embedjs 实现向量存储和语义搜索
 * 支持本地和云端嵌入模型
 */

import fs from 'fs';
import path from 'path';
import { Note } from '../types/index.js';

// 嵌入模型配置
export interface EmbedderConfig {
  provider: 'openai' | 'huggingface' | 'local';
  model?: string;
  apiKey?: string;
  baseUrl?: string;
}

const VECTOR_FILE = 'vectors.json';
const EMBEDDING_DIM = 1536; // text-embedding-3-small 默认维度

interface VectorRecord {
  id: string;        // note id
  embedding: number[];
  content: string;   // for fallback search
  timestamp: number;
}

interface VectorIndex {
  records: VectorRecord[];
  version: number;
  config: EmbedderConfig;
}

let index: VectorIndex = { records: [], version: 1, config: { provider: 'openai' } };
let dataPath = path.join(process.cwd(), 'data');

/**
 * 初始化向量存储
 */
export function initVectorStore(basePath?: string): void {
  if (basePath) {
    dataPath = basePath;
  }

  const vectorPath = path.join(dataPath, VECTOR_FILE);
  
  if (fs.existsSync(vectorPath)) {
    try {
      const data = fs.readFileSync(vectorPath, 'utf-8');
      index = JSON.parse(data);
      console.log(`[yiliu] Loaded ${index.records.length} vector records`);
    } catch (e) {
      console.error('[yiliu] Failed to load vector index:', e);
      index = { records: [], version: 1, config: { provider: 'openai' } };
    }
  }
}

/**
 * 保存向量索引到磁盘
 */
export function saveIndex(): void {
  const vectorPath = path.join(dataPath, VECTOR_FILE);
  
  if (!fs.existsSync(dataPath)) {
    fs.mkdirSync(dataPath, { recursive: true });
  }
  
  fs.writeFileSync(vectorPath, JSON.stringify(index), 'utf-8');
}

/**
 * 添加向量记录
 */
export function addVector(id: string, embedding: number[], content: string): void {
  // 移除旧记录（如果存在）
  index.records = index.records.filter(r => r.id !== id);
  
  // 添加新记录
  index.records.push({
    id,
    embedding,
    content,
    timestamp: Date.now(),
  });
  
  saveIndex();
}

/**
 * 批量添加向量
 */
export function addVectors(items: Array<{ id: string; embedding: number[]; content: string }>): void {
  const idSet = new Set(items.map(i => i.id));
  
  // 移除已存在的记录
  index.records = index.records.filter(r => !idSet.has(r.id));
  
  // 添加新记录
  for (const item of items) {
    index.records.push({
      id: item.id,
      embedding: item.embedding,
      content: item.content,
      timestamp: Date.now(),
    });
  }
  
  saveIndex();
}

/**
 * 删除向量记录
 */
export function removeVector(id: string): void {
  index.records = index.records.filter(r => r.id !== id);
  saveIndex();
}

/**
 * 计算 cosine 相似度
 */
function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) return 0;
  
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  
  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  
  if (normA === 0 || normB === 0) return 0;
  
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

/**
 * 语义搜索：返回最相似的笔记
 */
export function semanticSearch(
  queryEmbedding: number[],
  topK: number = 10,
  threshold: number = 0.5
): Array<{ id: string; score: number; content: string }> {
  const results: Array<{ id: string; score: number; content: string }> = [];
  
  for (const record of index.records) {
    const score = cosineSimilarity(queryEmbedding, record.embedding);
    
    if (score >= threshold) {
      results.push({
        id: record.id,
        score,
        content: record.content,
      });
    }
  }
  
  // 按相似度排序
  results.sort((a, b) => b.score - a.score);
  
  return results.slice(0, topK);
}

/**
 * 混合搜索：结合语义搜索和关键词匹配
 */
export function hybridSearch(
  queryEmbedding: number[] | null,
  keywords: string[],
  topK: number = 10
): Array<{ id: string; score: number; content: string }> {
  const scoreMap = new Map<string, { semantic: number; keyword: number; content: string }>();
  
  // 语义搜索
  if (queryEmbedding) {
    for (const record of index.records) {
      const semanticScore = cosineSimilarity(queryEmbedding, record.embedding);
      scoreMap.set(record.id, { semantic: semanticScore, keyword: 0, content: record.content });
    }
  }
  
  // 关键词匹配
  for (const record of index.records) {
    const content = record.content.toLowerCase();
    let keywordScore = 0;
    
    for (const keyword of keywords) {
      if (content.includes(keyword.toLowerCase())) {
        keywordScore += 0.3;
      }
    }
    
    keywordScore = Math.min(keywordScore, 1);
    
    const existing = scoreMap.get(record.id);
    if (existing) {
      existing.keyword = keywordScore;
    } else {
      scoreMap.set(record.id, { semantic: 0, keyword: keywordScore, content: record.content });
    }
  }
  
  // 合并分数：语义 70% + 关键词 30%
  const results: Array<{ id: string; score: number; content: string }> = [];
  
  for (const [id, scores] of scoreMap) {
    const combinedScore = scores.semantic * 0.7 + scores.keyword * 0.3;
    if (combinedScore > 0.1) {
      results.push({
        id,
        score: combinedScore,
        content: scores.content,
      });
    }
  }
  
  // 排序并返回 top-K
  results.sort((a, b) => b.score - a.score);
  return results.slice(0, topK);
}

/**
 * 获取所有向量 ID
 */
export function getAllVectorIds(): string[] {
  return index.records.map(r => r.id);
}

/**
 * 获取统计信息
 */
export function getStats(): { count: number; avgContentLength: number } {
  const count = index.records.length;
  const totalLength = index.records.reduce((sum, r) => sum + r.content.length, 0);
  
  return {
    count,
    avgContentLength: count > 0 ? Math.round(totalLength / count) : 0,
  };
}

/**
 * 检查向量是否存在
 */
export function hasVector(id: string): boolean {
  return index.records.some(r => r.id === id);
}

/**
 * 获取单个向量记录
 */
export function getVector(id: string): VectorRecord | undefined {
  return index.records.find(r => r.id === id);
}

/**
 * 更新嵌入配置
 */
export function updateConfig(config: Partial<EmbedderConfig>): void {
  index.config = { ...index.config, ...config };
  saveIndex();
}

/**
 * 获取当前配置
 */
export function getConfig(): EmbedderConfig {
  return index.config;
}

/**
 * 重新构建向量索引（从现有笔记）
 */
export async function rebuildIndex(notes: Array<{ id: string; content: string }>, embedFn: (text: string) => Promise<number[] | null>): Promise<void> {
  index.records = [];
  
  for (const note of notes) {
    const embedding = await embedFn(note.content);
    if (embedding) {
      index.records.push({
        id: note.id,
        embedding,
        content: note.content,
        timestamp: Date.now(),
      });
    }
  }
  
  saveIndex();
  console.log(`[yiliu] Rebuilt index with ${index.records.length} vectors`);
}
