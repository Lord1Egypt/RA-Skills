// src/embeddings.ts
import { createHash } from "crypto";
var MAX_EMBEDDINGS_PER_MINUTE = 20;
var DEDUP_COOLDOWN_MS = 3e5;
var TAIL_SAMPLE_K = 10;
var _rateWindows = /* @__PURE__ */ new Map();
var _dedupCache = /* @__PURE__ */ new Map();
var throttleMetrics = {
  throttleCount: 0,
  dedupCount: 0
};
function contentHash(text) {
  return createHash("sha256").update(text).digest("hex");
}
function checkRateLimit(conversationId) {
  const now = Date.now();
  let window = _rateWindows.get(conversationId);
  if (!window || now - window.windowStart > 6e4) {
    window = { count: 0, windowStart: now, tail: [] };
    _rateWindows.set(conversationId, window);
  }
  if (window.count >= MAX_EMBEDDINGS_PER_MINUTE) {
    const sample = window.tail[window.tail.length - 1] ?? [];
    throttleMetrics.throttleCount++;
    return sample;
  }
  return null;
}
function recordInWindow(conversationId, embedding) {
  const window = _rateWindows.get(conversationId);
  if (!window) return;
  window.count++;
  window.tail.push(embedding);
  if (window.tail.length > TAIL_SAMPLE_K) {
    window.tail.shift();
  }
}
function resetThrottleState() {
  _rateWindows.clear();
  _dedupCache.clear();
  throttleMetrics.throttleCount = 0;
  throttleMetrics.dedupCount = 0;
}
async function _generateEmbeddingFromOllama(text, config) {
  const response = await fetch(`${config.ollamaUrl}/api/embeddings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model: config.ollamaModel, prompt: text })
  });
  if (!response.ok) {
    throw new Error(`Ollama error: ${response.status} ${response.statusText}`);
  }
  const data = await response.json();
  return data.embedding;
}
async function generateEmbedding(text, config, conversationId) {
  if (!config.vectorEnabled) {
    throw new Error("Vector search is disabled in configuration");
  }
  if (conversationId) {
    const hash = contentHash(text);
    const cached = _dedupCache.get(hash);
    if (cached && Date.now() < cached.expiresAt) {
      throttleMetrics.dedupCount++;
      return cached.embedding;
    }
    const sampled = checkRateLimit(conversationId);
    if (sampled !== null) {
      return sampled;
    }
    const embedding = await _generateEmbeddingFromOllama(text, config);
    _dedupCache.set(hash, { embedding, expiresAt: Date.now() + DEDUP_COOLDOWN_MS });
    recordInWindow(conversationId, embedding);
    return embedding;
  }
  return _generateEmbeddingFromOllama(text, config);
}
async function generateHypotheticalAnswer(query, config, options = {}) {
  const model = options.model ?? "llama3";
  const prompt = `Answer the following question concisely in 2-3 sentences as if you had perfect knowledge. Do not hedge or say "I don't know".

Question: ${query}

Answer:`;
  const response = await fetch(`${config.ollamaUrl}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model,
      prompt,
      stream: false,
      options: { num_predict: options.maxTokens ?? 150 }
    })
  });
  if (!response.ok) {
    throw new Error(`Ollama generate error: ${response.status} ${response.statusText}`);
  }
  const data = await response.json();
  return data.response.trim();
}
async function generateHyDEExpansion(query, config, options = {}) {
  const original = await generateEmbedding(query, config);
  let hypothetical;
  try {
    hypothetical = await generateHypotheticalAnswer(query, config, {
      model: options.generationModel,
      maxTokens: options.maxTokens
    });
  } catch {
    return { original, expanded: original, hypothetical: query };
  }
  const expanded = await generateEmbedding(hypothetical, config);
  return { original, expanded, hypothetical };
}
function blendEmbeddings(a, b, weightA = 0.4) {
  if (a.length !== b.length) {
    throw new Error("Embeddings must have the same dimension");
  }
  const weightB = 1 - weightA;
  return a.map((val, i) => val * weightA + b[i] * weightB);
}
function cosineSimilarity(a, b) {
  if (a.length !== b.length) {
    throw new Error("Vectors must have the same length");
  }
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}
function serializeEmbedding(embedding) {
  const floatArray = new Float32Array(embedding);
  return Buffer.from(floatArray.buffer);
}
function deserializeEmbedding(buffer) {
  const floatArray = new Float32Array(buffer.buffer, buffer.byteOffset, buffer.length / 4);
  return Array.from(floatArray);
}
async function checkOllamaHealth(config) {
  try {
    const response = await fetch(`${config.ollamaUrl}/api/tags`, {
      method: "GET",
      signal: AbortSignal.timeout(5e3)
    });
    return response.ok;
  } catch {
    return false;
  }
}
async function listAvailableModels(config) {
  try {
    const response = await fetch(`${config.ollamaUrl}/api/tags`);
    if (!response.ok) return [];
    const data = await response.json();
    return data.models?.map((m) => m.name) || [];
  } catch {
    return [];
  }
}

export {
  throttleMetrics,
  resetThrottleState,
  generateEmbedding,
  generateHypotheticalAnswer,
  generateHyDEExpansion,
  blendEmbeddings,
  cosineSimilarity,
  serializeEmbedding,
  deserializeEmbedding,
  checkOllamaHealth,
  listAvailableModels
};
