/**
 * AI 能力模块
 * 提供文本向量嵌入、摘要生成、自动标签提取
 * 支持云端（OpenAI）和本地（Xenova）嵌入
 */

import type { Note } from '../types/index.js';
import { pipeline, env } from '@xenova/transformers';
import { homedir } from 'os';
import { join } from 'path';

// OpenAI API 配置
const OPENAI_API_KEY = process.env.OPENAI_API_KEY || '';
const OPENAI_BASE_URL = process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1';
const EMBEDDING_MODEL = process.env.EMBEDDING_MODEL || 'text-embedding-3-small';
const CHAT_MODEL = process.env.CHAT_MODEL || 'gpt-4o-mini';

// 本地嵌入配置
const LOCAL_MODEL = process.env.LOCAL_EMBED_MODEL || 'Xenova/all-MiniLM-L6-v2';

// 设置 Xenova 环境（Node.js 优化）
// 使用用户主目录下的缓存，避免中文路径问题
const cacheDir = process.env.XENOVA_CACHE_DIR || join(homedir(), '.cache', 'yiliu', 'models');
env.allowLocalModels = true;
env.useBrowserCache = false; // Node.js 不使用浏览器缓存
env.localModelPath = cacheDir;

// 嵌入提供者类型
export type EmbedderProvider = 'openai' | 'huggingface' | 'local';

// 嵌入配置（存储在内存中）
let embedderConfig: { provider: EmbedderProvider } = { provider: 'openai' };

function updateConfig(config: Partial<{ provider: EmbedderProvider }>): void {
  embedderConfig = { ...embedderConfig, ...config };
}

function getConfig(): { provider: EmbedderProvider } {
  return embedderConfig;
}

// 嵌入结果
export interface EmbeddingResult {
  embedding: number[];
  model: string;
  tokens: number;
}

// AI 增强结果
export interface AIEnhanceResult {
  summary: string;
  tags: string[];
  keywords: string[];
}

// 本地嵌入器引用
let localEmbedder: any = null;
let localEmbedderLoading = false;

/**
 * 获取当前嵌入提供者
 */
export function getEmbedderProvider(): EmbedderProvider {
  // 如果没有 OpenAI API Key，尝试使用本地嵌入
  if (!OPENAI_API_KEY) {
    return 'local';
  }
  
  // 检查配置
  const config = getConfig();
  return config.provider;
}

/**
 * 获取本地嵌入器
 */
async function getLocalEmbedder(): Promise<any> {
  if (localEmbedder) return localEmbedder;
  
  if (localEmbedderLoading) {
    // 等待加载完成
    while (localEmbedderLoading) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    return localEmbedder;
  }
  
  localEmbedderLoading = true;
  
  try {
    // 使用静态导入的 pipeline
    localEmbedder = await pipeline('feature-extraction', LOCAL_MODEL);
    
    console.log(`[yiliu] Local embedder loaded: ${LOCAL_MODEL}`);
    return localEmbedder;
  } catch (error) {
    console.error('[yiliu] Failed to load local embedder:', error);
    return null;
  } finally {
    localEmbedderLoading = false;
  }
}

/**
 * 生成文本向量嵌入（自动选择提供者）
 */
export async function generateEmbedding(text: string): Promise<EmbeddingResult | null> {
  const provider = getEmbedderProvider();
  
  if (provider === 'local' || !OPENAI_API_KEY) {
    return generateLocalEmbedding(text);
  }
  
  return generateOpenAIEmbedding(text);
}

/**
 * 使用 OpenAI API 生成嵌入
 */
async function generateOpenAIEmbedding(text: string): Promise<EmbeddingResult | null> {
  if (!OPENAI_API_KEY) {
    console.warn('[yiliu] OPENAI_API_KEY not set, skipping embedding');
    return null;
  }

  try {
    const response = await fetch(`${OPENAI_BASE_URL}/embeddings`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: EMBEDDING_MODEL,
        input: text.slice(0, 8000), // 限制长度
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      console.error('[yiliu] Embedding API error:', error);
      return null;
    }

    const data = await response.json() as { data: Array<{ embedding: number[] }>; model: string; usage: { total_tokens: number } };
    return {
      embedding: data.data[0].embedding,
      model: data.model,
      tokens: data.usage.total_tokens,
    };
  } catch (error) {
    console.error('[yiliu] Embedding failed:', error);
    return null;
  }
}

/**
 * 使用本地模型生成嵌入
 */
async function generateLocalEmbedding(text: string): Promise<EmbeddingResult | null> {
  try {
    const embedder = await getLocalEmbedder();
    
    if (!embedder) {
      console.warn('[yiliu] Local embedder not available');
      return null;
    }
    
    // 生成嵌入
    const output = await embedder(text.slice(0, 8000), {
      pooling: 'mean',
      normalize: true,
    });
    
    // 转换为数组并确保是 number 类型
    const embedding = Array.from(output.data as number[]);
    
    return {
      embedding,
      model: LOCAL_MODEL,
      tokens: Math.ceil(text.length / 4), // 估算
    };
  } catch (error) {
    console.error('[yiliu] Local embedding failed:', error);
    return null;
  }
}

/**
 * 批量生成向量嵌入
 */
export async function generateEmbeddings(texts: string[]): Promise<number[][]> {
  const provider = getEmbedderProvider();
  
  if (provider === 'local' || !OPENAI_API_KEY) {
    return generateLocalEmbeddings(texts);
  }
  
  return generateOpenAIEmbeddings(texts);
}

/**
 * 批量 OpenAI 嵌入
 */
async function generateOpenAIEmbeddings(texts: string[]): Promise<number[][]> {
  if (!OPENAI_API_KEY || texts.length === 0) {
    return [];
  }

  try {
    const response = await fetch(`${OPENAI_BASE_URL}/embeddings`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: EMBEDDING_MODEL,
        input: texts.map(t => t.slice(0, 8000)),
      }),
    });

    if (!response.ok) {
      console.error('[yiliu] Batch embedding API error:', await response.text());
      return [];
    }

    const data = await response.json() as { data: Array<{ index: number; embedding: number[] }> };
    return data.data
      .sort((a, b) => a.index - b.index)
      .map((d) => d.embedding);
  } catch (error) {
    console.error('[yiliu] Batch embedding failed:', error);
    return [];
  }
}

/**
 * 批量本地嵌入
 */
async function generateLocalEmbeddings(texts: string[]): Promise<number[][]> {
  if (texts.length === 0) return [];
  
  try {
    const embedder = await getLocalEmbedder();
    if (!embedder) return [];
    
    const embeddings: number[][] = [];
    
    for (const text of texts) {
      const output = await embedder(text.slice(0, 8000), {
        pooling: 'mean',
        normalize: true,
      });
      embeddings.push(Array.from(output.data));
    }
    
    return embeddings;
  } catch (error) {
    console.error('[yiliu] Batch local embedding failed:', error);
    return [];
  }
}

/**
 * AI 增强笔记：生成摘要、标签、关键词
 */
export async function enhanceNote(content: string): Promise<AIEnhanceResult | null> {
  if (!OPENAI_API_KEY) {
    console.warn('[yiliu] OPENAI_API_KEY not set, skipping AI enhancement');
    return null;
  }

  const systemPrompt = `你是一个笔记整理助手。分析用户笔记，提取结构化信息。
返回 JSON 格式，包含：
- summary: 一句话摘要（不超过50字）
- tags: 标签数组（3-5个，简洁）
- keywords: 关键词数组（重要实体）

只返回 JSON，不要其他内容。`;

  try {
    const response = await fetch(`${OPENAI_BASE_URL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: CHAT_MODEL,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: content.slice(0, 4000) },
        ],
        temperature: 0.3,
        response_format: { type: 'json_object' },
      }),
    });

    if (!response.ok) {
      console.error('[yiliu] AI enhancement API error:', await response.text());
      return null;
    }

    const data = await response.json() as { choices: Array<{ message: { content: string } }> };
    const result = JSON.parse(data.choices[0].message.content) as AIEnhanceResult;
    
    return {
      summary: result.summary || '',
      tags: result.tags || [],
      keywords: result.keywords || [],
    };
  } catch (error) {
    console.error('[yiliu] AI enhancement failed:', error);
    return null;
  }
}

/**
 * 从查询生成搜索关键词
 */
export async function expandSearchQuery(query: string): Promise<string[]> {
  if (!OPENAI_API_KEY) {
    return [query];
  }

  const systemPrompt = `你是一个搜索优化助手。将用户的自然语言查询扩展为多个相关关键词。
返回 JSON 数组格式，包含原词和相关词，最多5个。
只返回 JSON 数组，不要其他内容。`;

  try {
    const response = await fetch(`${OPENAI_BASE_URL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: CHAT_MODEL,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: query },
        ],
        temperature: 0.3,
        response_format: { type: 'json_array' },
      }),
    });

    if (!response.ok) {
      return [query];
    }

    const data = await response.json() as { choices: Array<{ message: { content: string } }> };
    return JSON.parse(data.choices[0].message.content) as string[];
  } catch {
    return [query];
  }
}

/**
 * 检查 AI 服务是否可用
 */
export function isAIAvailable(): boolean {
  return !!OPENAI_API_KEY;
}

/**
 * 检查是否有本地嵌入能力
 */
export async function isLocalEmbeddingAvailable(): Promise<boolean> {
  try {
    const embedder = await getLocalEmbedder();
    return embedder !== null;
  } catch {
    return false;
  }
}

/**
 * 获取当前嵌入模型信息
 */
export function getEmbeddingModelInfo(): { provider: string; model: string; isLocal: boolean } {
  const provider = getEmbedderProvider();
  const config = getConfig();
  
  return {
    provider,
    model: provider === 'local' ? LOCAL_MODEL : EMBEDDING_MODEL,
    isLocal: provider === 'local',
  };
}

/**
 * 切换嵌入提供者
 */
export function setEmbedderProvider(provider: EmbedderProvider): void {
  updateConfig({ provider });
  console.log(`[yiliu] Embedder provider set to: ${provider}`);
}
