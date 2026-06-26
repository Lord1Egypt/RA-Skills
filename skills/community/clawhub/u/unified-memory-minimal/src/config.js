/**
 * config.js - 配置管理
 */

import { readFileSync, existsSync, mkdirSync, appendFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_CACHE_DIR = join(MEMORY_DIR, 'vector_cache');
const LOG_DIR = join(MEMORY_DIR, 'logs');

// ─── Provider 配置 ───
// 每个 provider 独立 baseURL + model，支持 env 覆盖
// EMBED_xxx: 向量 embedding 专用
// LLM_xxx: LLM 专用
// CUSTOM_xxx: 自定义 provider 专用（baseURL + model 完全用户指定）

const EMBED_PROVIDERS = [
  {
    name: 'ollama',
    baseURL: process.env.EMBED_BASE_URL || process.env.OLLAMA_BASE_URL || process.env.OLLAMA_HOST || 'http://localhost:11434',
    model: process.env.EMBED_MODEL || process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text',
    apiKey: null,
  },
  {
    name: 'openai',
    baseURL: process.env.EMBED_BASE_URL || 'https://api.openai.com/v1',
    model: process.env.EMBED_MODEL || 'text-embedding-3-small',
    apiKey: process.env.OPENAI_API_KEY || null,
  },
  {
    name: 'jina',
    baseURL: process.env.EMBED_BASE_URL || 'https://api.jina.ai/v1',
    model: process.env.EMBED_MODEL || 'jina-embeddings-v3',
    apiKey: process.env.JINA_API_KEY || null,
  },
  {
    name: 'siliconflow',
    baseURL: process.env.EMBED_BASE_URL || 'https://api.siliconflow.cn/v1',
    model: process.env.EMBED_MODEL || 'BAAI/bge-m3',
    apiKey: process.env.SILICONFLOW_API_KEY || null,
  },
  {
    name: 'custom',
    baseURL: process.env.EMBED_BASE_URL || '',
    model: process.env.EMBED_MODEL || '',
    apiKey: null,
  },
];

const LLM_PROVIDERS = [
  {
    name: 'ollama',
    baseURL: process.env.LLM_BASE_URL || process.env.OLLAMA_BASE_URL || process.env.OLLAMA_HOST || 'http://localhost:11434',
    model: process.env.LLM_MODEL || process.env.OLLAMA_LLM_MODEL || 'qwen2.5:7b',
    apiKey: null,
  },
  {
    name: 'openai',
    baseURL: process.env.LLM_BASE_URL || 'https://api.openai.com/v1',
    model: process.env.LLM_MODEL || 'gpt-4o-mini',
    apiKey: process.env.OPENAI_API_KEY || null,
  },
  {
    name: 'siliconflow',
    baseURL: process.env.LLM_BASE_URL || 'https://api.siliconflow.cn/v1',
    model: process.env.LLM_MODEL || 'Qwen/Qwen2.5-7B-Instruct',
    apiKey: process.env.SILICONFLOW_API_KEY || null,
  },
  {
    name: 'custom',
    baseURL: process.env.LLM_BASE_URL || '',
    model: process.env.LLM_MODEL || '',
    apiKey: null,
  },
];

// ─── Pluggable Engine Config ───
// EMBED_PROVIDER: 'ollama' | 'openai' | 'jina' | 'siliconflow' | 'custom' | 'none'
// LLM_PROVIDER:   'ollama' | 'openai' | 'siliconflow' | 'custom' | 'none'
// VECTOR_ENGINE:  'lancedb' | 'ollama' | 'none' (控制是否启用向量)
const VECTOR_ENGINE = process.env.VECTOR_ENGINE || 'lancedb';
const EMBED_PROVIDER = process.env.EMBED_PROVIDER || 'ollama';
const LLM_PROVIDER   = process.env.LLM_PROVIDER   || 'ollama';

// ─── v4.3: Vector Store Backend Selection ───
// VECTOR_STORE_TYPE: 'lancedb' (default) | 'sqlite'
// When 'sqlite': uses SQLite with sqlite-vec extension for L0+L1 dual-layer storage
const VECTOR_STORE_TYPE = process.env.VECTOR_STORE_TYPE || 'lancedb';
const SQLITE_DB_PATH = process.env.SQLITE_DB_PATH || join(MEMORY_DIR, 'memory.db');

// Resolve active embed provider by name
function resolveEmbedProvider(name) {
  if (name === 'none') return null;
  return EMBED_PROVIDERS.find(p => p.name === name) || null;
}

// Resolve active LLM provider by name
function resolveLlmProvider(name) {
  if (name === 'none') return null;
  return LLM_PROVIDERS.find(p => p.name === name) || null;
}

const activeEmbedProvider = (() => {
  if (VECTOR_ENGINE === 'none') return null;
  return resolveEmbedProvider(EMBED_PROVIDER);
})();

const activeLlmProvider = resolveLlmProvider(LLM_PROVIDER);

const defaultConfig = {
  memoryDir: MEMORY_DIR,
  memoryFile: join(MEMORY_DIR, 'memories.json'),
  vectorCacheDir: VECTOR_CACHE_DIR,
  logDir: LOG_DIR,
  logLevel: process.env.LOG_LEVEL || 'info',  // debug/info/warn/error
  topK: 10,
  rrfK: 60,
  embedProviders: EMBED_PROVIDERS,
  llmProviders: LLM_PROVIDERS,

  // ─── Pluggable Engine Switches ───
  vectorEngine:     VECTOR_ENGINE,   // 'lancedb' | 'ollama' | 'none'
  embedProvider:    EMBED_PROVIDER,  // 'ollama' | 'openai' | 'jina' | 'siliconflow' | 'custom' | 'none'
  llmProvider:     LLM_PROVIDER,    // 'ollama' | 'openai' | 'siliconflow' | 'custom' | 'none'
  activeEmbedProvider,
  activeLlmProvider,

  // ─── v4.3: Vector Store Backend ───
  VECTOR_STORE_TYPE,    // 'lancedb' | 'sqlite'
  SQLITE_DB_PATH,        // SQLite database path

  // ─── v4.0: 四层管线配置 (借鉴 memory-tencentdb) ───
  pipeline: {
    enabled: true,                    // 是否启用自动管线
    everyNConversations: 5,           // 每 N 轮对话触发 L1
    enableWarmup: true,               // Warm-up 模式: 1→2→4→8→...→N
    l1IdleTimeoutSeconds: 60,         // 用户停止对话后多久触发 L1
    l2DelayAfterL1Seconds: 90,        // L1 完成后延迟多久触发 L2
    l2MinIntervalSeconds: 300,        // 同一 session 两次 L2 的最小间隔
    l2MaxIntervalSeconds: 1800,       // 活跃 session 的 L2 最大轮询间隔
    sessionActiveWindowHours: 24,     // 超过此时间不活跃的 session 停止 L2 轮询
    l3TriggerEveryN: 50,              // 每 N 条新记忆触发 L3
  },

  // ─── v4.1: 数据清理配置 (借鉴 memory-tencentdb) ───
  cleaner: {
    enabled: false,                   // 是否启用自动清理
    retentionDays: 0,                 // 保留天数，0 = 禁用清理
    cleanTime: '03:00',               // 每日清理时间 (HH:mm)
    allowAggressiveCleanup: false,    // 是否允许 1-2 天的高风险清理
  },

  // ─── v4.1.2: 本地 Embedding 配置 (移植自 memory-tencentdb) ───
  localEmbedding: {
    enabled: true,                    // 是否启用本地 Embedding
    preferLocal: true,                // 优先使用本地 Embedding
    modelPath: '',                    // GGUF 模型路径 (默认: embeddinggemma-300m)
    modelCacheDir: '',                // 模型缓存目录
    autoWarmup: true,                 // 是否自动预热
    waitForReady: false,              // 是否等待就绪 (false = 回退到远程)
    dimensions: 768,                  // 向量维度 (embeddinggemma-300m = 768)
  },

  // ─── v4.0: 中文支持配置 ───
  chinese: {
    enabled: true,                    // 是否启用中文优化
    segmenter: 'jieba',               // 分词器: 'jieba' | 'fallback'
  },

  // ─── v4.0: 零配置默认值 ───
  zeroConfig: {
    enabled: true,                    // 是否启用零配置模式
    autoDetectOllama: true,           // 自动检测 Ollama
    autoDetectOpenAI: true,           // 自动检测 OpenAI API Key
    defaultStrategy: 'keyword',       // 默认搜索策略: 'keyword' | 'hybrid' | 'embedding'
  },

  // ─── Backward-compat aliases (used by existing code) ───
  get ollamaUrl() {
    const p = this.activeEmbedProvider;
    return p ? p.baseURL : null;
  },
  get embedModel() {
    const p = this.activeEmbedProvider;
    return p ? p.model : null;
  },
  get llmModel() {
    const p = this.activeLlmProvider;
    return p ? p.model : null;
  },
  get llmUrl() {
    const p = this.activeLlmProvider;
    return p ? p.baseURL : null;
  },

  // ─── Phase 3: Search Backend ───
  qmd: {
    enabled: false,  // true = use QMD CLI, false = use built-in BM25+vector
    collections: ['workspace', 'daily-logs', 'projects', 'intelligence'],
  },

  // ─── Phase 3: Git Integration ───
  git: {
    enabled: false,
    repo_path: join(MEMORY_DIR, '.git-repo'),
    remote_url: null,
    auto_commit: false,  // auto-commit on each memory write
  },

  // ─── Phase 3: Cloud Backup ───
  cloud: {
    enabled: false,
    provider: 'supermemory',  // 'supermemory' | 'custom'
    supermemory_api_key: null,
    supermemory_endpoint: 'https://api.supermemory.ai',
    rest_endpoint: null,
    rest_api_key: null,
  },

  // ─── Phase 3: Weibull Decay ───
  weibull_decay: {
    shape: 1.5,   // 形状参数 k (1.0-3.0，越大记忆越持久)
    scale: 30,    // 尺度参数 λ（天数，越大衰减越慢）
  },
};

// Load config from file
function loadConfig() {
  const configFile = join(MEMORY_DIR, 'config.json');
  if (existsSync(configFile)) {
    try {
      return JSON.parse(readFileSync(configFile, 'utf-8'));
    } catch { }
  }
  return {};
}

export const config = { ...defaultConfig, ...loadConfig() };

// ─── LLM Call Helper (used by extract.js, profile.js) ────────────────────────
// Uses the active LLM provider (OLLAMA_BASE_URL/LLM_MODEL env vars or config)
let _llmClient = null;

async function getLlmClientAsync() {
  if (_llmClient) return _llmClient;
  try {
    const { LLMProviderFactory } = await import('./system/llm_provider.js').catch(() => ({ LLMProviderFactory: null }));
    if (!LLMProviderFactory) return null;
    const provider = config.llmProvider || 'ollama';
    _llmClient = LLMProviderFactory.create(provider, {
      baseUrl: config.llmUrl,
      model: config.llmModel,
      apiKey: null,
    });
    return _llmClient;
  } catch {
    return null;
  }
}

/**
 * LLM call helper: returns the raw text response from the active LLM.
 * Compatible with the llmCall(text, { prompt, signal }) interface used by extract.js.
 * @param {string} prompt
 * @param {{ prompt?: string, signal?: AbortSignal }} [_opts]
 * @returns {Promise<string>}
 */
/**
 * LLM call helper.
 * Signature compatible with extractMemories: llmCall(text, { prompt: SYSTEM_PROMPT, signal })
 * - text = user message to analyze
 * - opts.prompt = system prompt template (we append text to it)
 */
export async function llmCall(text, _opts = {}) {
  // extractMemories passes: llmCall(text, { prompt: EXTRACT_PROMPT, signal })
  // So _opts.prompt is the system/instruction part, text is the content to analyze
  const systemPrompt = _opts.prompt || '';
  const fullPrompt = systemPrompt ? `${systemPrompt}\n\n${text}` : text;
  const signal = _opts.signal;

  const client = await getLlmClientAsync();
  if (!client) {
    // Fallback: direct Ollama /api/generate
    const url = config.llmUrl || 'http://localhost:11434';
    const model = config.llmModel || 'qwen2.5:7b';
    try {
      const res = await fetch(`${url}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model, prompt: fullPrompt, stream: false }),
        signal: signal || AbortSignal.timeout(30000),
      });
      if (!res.ok) throw new Error(`Ollama ${res.status}`);
      const data = await res.json();
      return data.response || '';
    } catch (e) {
      throw new Error(`llmCall failed: ${e.message}`);
    }
  }
  const result = await client.generate(fullPrompt);
  return result.content || '';
}

// Ensure directories exist
for (const dir of [MEMORY_DIR, VECTOR_CACHE_DIR, LOG_DIR]) {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

export function log(/** @type {string} */ level, /** @type {string} */ msg) {
  const now = new Date().toISOString();
  const line = `[${now}] [${level}] ${msg}`;
  if (process.env.NODE_ENV !== 'test') {
    try {
      const logFile = join(LOG_DIR, `mcp-${new Date().toISOString().slice(0, 10)}.log`);
      appendFileSync(logFile, line + '\n');
    } catch { }
  }
  if (level === 'ERROR') {
    console.error(line);
  }
}
