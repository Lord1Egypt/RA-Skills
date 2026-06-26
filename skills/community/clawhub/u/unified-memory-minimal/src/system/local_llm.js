/**
 * Local LLM Support - 本地 GGUF/Ollama 模型支持 v1.0
 * 
 * 支持:
 * - Ollama API (embedding, reranker, LLM)
 * - 本地 GGUF 模型 (llama-cpp-python)
 * - 简单算法回退 (无模型时)
 * 
 * Usage:
 *     import { getEmbedder, getReranker, getLLM } from './system/local_llm.js';
 *     
 *     const embedder = getEmbedder("nomic-embed-text");
 *     const embedding = await embedder.embed("文本");
 *     
 *     const reranker = getReranker();
 *     const results = await reranker.rerank("查询", ["文档1", "文档2"]);
 */

// ============================================================
// Imports
// ============================================================

import { createHash } from 'crypto';
import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';

// ============================================================
// Config
// ============================================================

const MODELS_DIR = join(homedir(), '.cache', 'local-llm', 'models');
const OLLAMA_URL = process.env.OLLAMA_HOST || 'http://localhost:11434';

// Ensure models directory exists
try { mkdirSync(MODELS_DIR, { recursive: true }); } catch {}

// ============================================================
// Embedder
// ============================================================

export class Embedder {
  /**
   * @param {string} text
   * @returns {Promise<number[]|null>}
   */
  async embed(text) {
    throw new Error('Not implemented');
  }

  /**
   * @param {string[]} texts
   * @returns {Promise<(number[]|null)[]>}
   */
  async embedBatch(texts) {
    return Promise.all(texts.map(t => this.embed(t)));
  }
}

export class OllamaEmbedder extends Embedder {
  constructor(model = 'nomic-embed-text:latest') {
    super();
    this.model = model;
    this.available = false;
    this._checkAvailable();
  }

  async _checkAvailable() {
    try {
      const res = await fetch(`${OLLAMA_URL}/api/tags`, { signal: AbortSignal.timeout(5000) });
      this.available = res.ok;
    } catch {
      this.available = false;
    }
  }

  async embed(text) {
    if (!this.available) return null;

    try {
      const response = await fetch(`${OLLAMA_URL}/api/embeddings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: this.model, prompt: text }),
        signal: AbortSignal.timeout(30000),
      });

      if (response.ok) {
        const data = await response.json();
        return data.embedding || null;
      }
    } catch (e) {
      console.warn(`⚠️ Ollama embedding 失败: ${e.message}`);
    }

    return null;
  }
}

export class LocalGGUFEmbedder extends Embedder {
  constructor(modelPath) {
    super();
    this.modelPath = modelPath;
    this.model = null;
    this._llamaCpp = null;
    this._loadModel();
  }

  _loadModel() {
    try {
      // Try to use llama-cpp-python via node
      // Note: This would require a native binding, so for now we just mark as unavailable
      console.warn('⚠️ GGUF embedding 需要 llama-cpp-python');
    } catch (e) {
      console.warn(`⚠️ 加载 GGUF 模型失败: ${e.message}`);
    }
  }

  async embed(text) {
    if (!this.model) return null;

    try {
      // This would call the Python binding
      return this.model.embed(text);
    } catch (e) {
      console.warn(`⚠️ GGUF embedding 失败: ${e.message}`);
      return null;
    }
  }
}

export class SimpleEmbedder extends Embedder {
  constructor(dim = 768) {
    super();
    this.dim = dim;
    this.vocab = new Map();
  }

  async embed(text) {
    const words = text.toLowerCase().split(/\s+/);
    const embedding = new Array(this.dim).fill(0);

    for (const word of words) {
      const hash = parseInt(createHash('md5').update(word).digest('hex'), 16);
      const idx = hash % this.dim;
      embedding[idx] += 1.0;
    }

    // Normalize
    const norm = Math.sqrt(embedding.reduce((sum, x) => sum + x * x, 0));
    if (norm > 0) {
      for (let i = 0; i < embedding.length; i++) {
        embedding[i] /= norm;
      }
    }

    return embedding;
  }
}

/**
 * Get an embedder
 * @param {string} model - "auto", "ollama:model", "/path/to/model.gguf", "simple"
 * @returns {Embedder}
 */
export function getEmbedder(model = 'auto') {
  if (model === 'simple') {
    return new SimpleEmbedder();
  }

  if (model.startsWith('ollama:')) {
    const modelName = model.split(':', 1)[1];
    return new OllamaEmbedder(modelName);
  }

  if (model.endsWith('.gguf')) {
    return new LocalGGUFEmbedder(model);
  }

  // Auto detection
  // 1. Check default GGUF
  const defaultGGUF = join(MODELS_DIR, 'nomic-embed-text-v1.5.f16.gguf');
  if (existsSync(defaultGGUF)) {
    try {
      return new LocalGGUFEmbedder(defaultGGUF);
    } catch {}
  }

  // 2. Try Ollama
  const ollama = new OllamaEmbedder();
  if (ollama.available) {
    return ollama;
  }

  // 3. Fallback to simple
  console.warn('⚠️ 无可用 embedding 模型，使用简单算法');
  return new SimpleEmbedder();
}

// ============================================================
// Reranker
// ============================================================

export class Reranker {
  /**
   * @param {string} query
   * @param {string[]} documents
   * @param {number} topK
   * @returns {Promise<{index: number, document: string, score: number}[]>}
   */
  async rerank(query, documents, topK = 5) {
    throw new Error('Not implemented');
  }
}

export class OllamaReranker extends Reranker {
  constructor(model = 'qwen2.5:0.5b') {
    super();
    this.model = model;
    this.available = false;
    this._checkAvailable();
  }

  async _checkAvailable() {
    try {
      const res = await fetch(`${OLLAMA_URL}/api/tags`, { signal: AbortSignal.timeout(5000) });
      this.available = res.ok;
    } catch {
      this.available = false;
    }
  }

  async rerank(query, documents, topK = 5) {
    if (!this.available || !documents.length) {
      return documents.slice(0, topK).map((doc, i) => ({
        index: i,
        document: doc,
        score: 0.5,
      }));
    }

    const results = [];

    for (let i = 0; i < documents.length; i++) {
      const doc = documents[i];
      const prompt = `Rate the relevance of this document to the query.\nQuery: ${query}\nDocument: ${doc.slice(0, 500)}\nRelevance score (0.0-1.0):`;

      try {
        const response = await fetch(`${OLLAMA_URL}/api/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            model: this.model,
            prompt,
            stream: false,
            options: { num_predict: 10, temperature: 0.0 },
          }),
          signal: AbortSignal.timeout(10000),
        });

        if (response.ok) {
          const data = await response.json();
          const text = (data.response || '').trim();
          const score = parseFloat(text.split(/\s+/)[0]) || 0.5;
          results.push({
            index: i,
            document: doc,
            score: Math.max(0.0, Math.min(1.0, score)),
          });
        } else {
          results.push({ index: i, document: doc, score: 0.5 });
        }
      } catch (e) {
        console.warn(`⚠️ Ollama rerank 失败: ${e.message}`);
        results.push({ index: i, document: doc, score: 0.5 });
      }
    }

    results.sort((a, b) => b.score - a.score);
    return results.slice(0, topK);
  }
}

export class SimpleReranker extends Reranker {
  async rerank(query, documents, topK = 5) {
    const queryWords = new Set(query.toLowerCase().split(/\s+/));
    const results = [];

    for (let i = 0; i < documents.length; i++) {
      const doc = documents[i];
      const docWords = new Set(doc.toLowerCase().split(/\s+/));

      // Jaccard similarity
      const intersection = [...queryWords].filter(w => docWords.has(w)).length;
      const union = new Set([...queryWords, ...docWords]).size;
      const score = union > 0 ? intersection / union : 0.0;

      results.push({ index: i, document: doc, score });
    }

    results.sort((a, b) => b.score - a.score);
    return results.slice(0, topK);
  }
}

/**
 * Get a reranker
 * @param {string} model - "auto", "ollama:model", "simple"
 * @returns {Reranker}
 */
export function getReranker(model = 'auto') {
  if (model === 'simple') {
    return new SimpleReranker();
  }

  if (model.startsWith('ollama:')) {
    const modelName = model.split(':', 1)[1];
    return new OllamaReranker(modelName);
  }

  // Auto
  const ollama = new OllamaReranker();
  if (ollama.available) {
    return ollama;
  }

  return new SimpleReranker();
}

// ============================================================
// LLM
// ============================================================

export class LLM {
  /**
   * @param {string} prompt
   * @param {Object} options
   * @returns {Promise<string>}
   */
  async generate(prompt, options = {}) {
    throw new Error('Not implemented');
  }
}

export class OllamaLLM extends LLM {
  constructor(model = 'qwen2.5:7b') {
    super();
    this.model = model;
    this.available = false;
    this._checkAvailable();
  }

  async _checkAvailable() {
    try {
      const res = await fetch(`${OLLAMA_URL}/api/tags`, { signal: AbortSignal.timeout(5000) });
      this.available = res.ok;
    } catch {
      this.available = false;
    }
  }

  async generate(prompt, options = {}) {
    const {
      maxTokens = 512,
      temperature = 0.7,
      stop = [],
    } = options;

    if (!this.available) {
      return `[LLM 不可用] ${prompt.slice(0, 100)}...`;
    }

    try {
      const response = await fetch(`${OLLAMA_URL}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: this.model,
          prompt,
          stream: false,
          options: {
            num_predict: maxTokens,
            temperature,
            stop: stop || [],
          },
        }),
        signal: AbortSignal.timeout(60000),
      });

      if (response.ok) {
        const data = await response.json();
        return data.response || '';
      }
    } catch (e) {
      console.warn(`⚠️ Ollama generate 失败: ${e.message}`);
    }

    return '';
  }

  async *stream(prompt, options = {}) {
    const {
      maxTokens = 512,
      temperature = 0.7,
      stop = [],
    } = options;

    if (!this.available) {
      yield `[LLM 不可用] ${prompt.slice(0, 100)}...`;
      return;
    }

    try {
      const response = await fetch(`${OLLAMA_URL}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: this.model,
          prompt,
          stream: true,
          options: {
            num_predict: maxTokens,
            temperature,
            stop: stop || [],
          },
        }),
      });

      if (!response.ok) {
        yield `[错误] HTTP ${response.status}`;
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const lines = decoder.decode(value).split('\n');
        for (const line of lines) {
          if (line.trim()) {
            try {
              const data = JSON.parse(line);
              if (data.response) {
                yield data.response;
              }
            } catch {}
          }
        }
      }
    } catch (e) {
      yield `[错误] ${e.message}`;
    }
  }
}

export class LocalGGUFLLM extends LLM {
  constructor(modelPath) {
    super();
    this.modelPath = modelPath;
    this.model = null;
    this._loadModel();
  }

  _loadModel() {
    try {
      // Would need llama-cpp-python binding
      console.warn('⚠️ GGUF LLM 需要 llama-cpp-python');
    } catch (e) {
      console.warn(`⚠️ 加载 GGUF 模型失败: ${e.message}`);
    }
  }

  async generate(prompt, options = {}) {
    if (!this.model) return '';
    // Would call Python binding
    return '';
  }
}

/**
 * Get an LLM
 * @param {string} model - "auto", "ollama:model", "/path/to/model.gguf"
 * @returns {LLM}
 */
export function getLLM(model = 'auto') {
  if (model.startsWith('ollama:')) {
    const modelName = model.split(':', 1)[1];
    return new OllamaLLM(modelName);
  }

  if (model.endsWith('.gguf')) {
    return new LocalGGUFLLM(model);
  }

  // Auto
  const ollama = new OllamaLLM();
  if (ollama.available) {
    return ollama;
  }

  console.warn('⚠️ 无可用 LLM');
  return new OllamaLLM();
}

// ============================================================
// Formatting utilities
// ============================================================

/**
 * Format text for embedding based on model type
 * @param {string} text
 * @param {string} model
 * @param {boolean} isQuery
 * @param {string|undefined} title
 * @returns {string}
 */
export function formatForEmbedding(text, model = '', isQuery = false, title = undefined) {
  const modelLower = (model || '').toLowerCase();

  // Qwen3-Embedding format
  if (modelLower.includes('qwen') && modelLower.includes('embed')) {
    if (isQuery) {
      return `Instruct: Retrieve relevant documents for the given query\nQuery: ${text}`;
    }
    return title ? `${title}\n${text}` : text;
  }

  // Nomic format
  if (modelLower.includes('nomic')) {
    if (isQuery) {
      return `task: search result | query: ${text}`;
    }
    return `title: ${title || 'none'} | text: ${text}`;
  }

  // Default: raw text
  return text;
}

// ============================================================
// CLI
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  const action = args[0] || 'embed';
  const modelArg = args.find(a => a.startsWith('--model='))?.split('=')[1] || 'auto';

  if (action === 'list') {
    console.log('📦 可用模型:');
    console.log('  Embedding:');
    console.log('    - nomic-embed-text:latest (Ollama)');
    console.log('    - *.gguf (本地 GGUF)');
    console.log('  LLM:');
    console.log('    - qwen2.5:7b (Ollama)');
    console.log('    - *.gguf (本地 GGUF)');
    return;
  }

  if (action === 'embed') {
    const textArg = args.find(a => a.startsWith('--text='))?.split('=')[1] || '';
    if (!textArg) {
      console.error('❌ 请指定 --text');
      process.exit(1);
    }

    const embedder = getEmbedder(modelArg);
    const embedding = await embedder.embed(textArg);

    if (embedding) {
      console.log(`✅ Embedding 维度: ${embedding.length}`);
      console.log(`   前 10 维: ${embedding.slice(0, 10).map(x => x.toFixed(4)).join(', ')}...`);
    } else {
      console.error('❌ Embedding 失败');
    }
    return;
  }

  if (action === 'rerank') {
    const queryArg = args.find(a => a.startsWith('--query='))?.split('=')[1] || '';
    const docsArg = args.find(a => a.startsWith('--docs='))?.split('=')[1] || '';

    if (!queryArg || !docsArg) {
      console.error('❌ 请指定 --query 和 --docs');
      process.exit(1);
    }

    const docs = docsArg.split(',').map(d => d.trim());
    const reranker = getReranker(modelArg);
    const results = await reranker.rerank(queryArg, docs);

    console.log('✅ Rerank 结果:');
    for (const r of results) {
      console.log(`   [${r.score.toFixed(3)}] ${r.document.slice(0, 50)}...`);
    }
    return;
  }

  if (action === 'generate') {
    const textArg = args.find(a => a.startsWith('--text='))?.split('=')[1] || '';
    if (!textArg) {
      console.error('❌ 请指定 --text');
      process.exit(1);
    }

    const llm = getLLM(modelArg);
    const response = await llm.generate(textArg);
    console.log(response);
    return;
  }
}

const isMain = process.argv[1]?.endsWith('local_llm.js') || process.argv[1]?.endsWith('local_llm.mjs');
if (isMain) {
  main().catch(console.error);
}

export default {
  getEmbedder,
  getReranker,
  getLLM,
  formatForEmbedding,
  Embedder,
  Reranker,
  LLM,
  OllamaEmbedder,
  OllamaReranker,
  OllamaLLM,
  SimpleEmbedder,
  SimpleReranker,
};
