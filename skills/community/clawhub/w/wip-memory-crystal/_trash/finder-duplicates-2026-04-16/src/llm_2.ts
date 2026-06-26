// memory-crystal/llm.ts — LLM provider cascade for query expansion + re-ranking.
// Tries local-first (MLX, Ollama), falls back to cloud APIs (Anthropic, OpenAI).
// All providers use OpenAI-compatible HTTP or native APIs.

import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { execSync } from 'node:child_process';

export interface QueryVariation {
  type: 'lex' | 'vec' | 'hyde';
  text: string;
}

export interface RerankResult {
  index: number;
  score: number;
}

export type LLMProvider = 'sampling' | 'mlx' | 'ollama' | 'anthropic' | 'openai' | 'none';

interface ProviderConfig {
  provider: LLMProvider;
  baseURL: string;
  apiKey: string;
  model: string;
}

// ── MCP Sampling Integration ──
// When running as an MCP server inside Claude Code, the server can ask the client
// to generate completions via sampling/createMessage. This uses the user's Max
// subscription (no separate API key needed). Blocked on Claude Code implementing
// MCP sampling (GitHub Issue #1785). The integration is designed and ready.
//
// How it works:
// 1. mcp-server.ts checks if the connected client advertises sampling capability
// 2. If yes, it passes the Server instance to setSamplingServer()
// 3. detectProvider() checks samplingServer first (priority 0, before MLX)
// 4. chatComplete() routes 'sampling' calls through the MCP SDK's createMessage
//
// The server requests low-cost, high-speed models via ModelPreferences:
//   { costPriority: 0.9, speedPriority: 0.8, intelligencePriority: 0.3 }
// This hints the client to use Haiku-class models for expansion/reranking.

let samplingServer: any = null; // Will be Server from @modelcontextprotocol/sdk

/** Called by mcp-server.ts when the client supports sampling. */
export function setSamplingServer(server: any): void {
  samplingServer = server;
}

/** Check if MCP sampling is available. */
export function hasSampling(): boolean {
  return samplingServer !== null;
}

// Cache for expanded queries (same query = same expansions within a session)
const expansionCache = new Map<string, QueryVariation[]>();

let detectedProvider: ProviderConfig | null = null;
let detectionDone = false;

/** Try to fetch an API key from 1Password via the SA token. */
function getOpSecret(itemName: string, fieldLabel: string): string | undefined {
  try {
    const saTokenPath = join(homedir(), '.openclaw/secrets/op-sa-token');
    if (!existsSync(saTokenPath)) return undefined;
    const saToken = readFileSync(saTokenPath, 'utf-8').trim();
    const result = execSync(
      `OP_SERVICE_ACCOUNT_TOKEN="${saToken}" op item get "${itemName}" --vault "Agent Secrets" --fields "${fieldLabel}" --reveal`,
      { encoding: 'utf-8', timeout: 5000, stdio: ['pipe', 'pipe', 'pipe'] }
    ).trim();
    return result || undefined;
  } catch {
    return undefined;
  }
}

/** Detect the best available LLM provider. Cached after first call. */
export async function detectProvider(): Promise<ProviderConfig> {
  if (detectionDone && detectedProvider) return detectedProvider;
  detectionDone = true;

  // 0. MCP Sampling (if client supports it ... uses Max subscription, no API key)
  if (samplingServer) {
    detectedProvider = { provider: 'sampling', baseURL: '', apiKey: '', model: 'client-selected' };
    process.stderr.write('[memory-crystal] LLM provider: MCP Sampling (via client)\n');
    return detectedProvider;
  }

  // 1. MLX server (localhost:8080)
  try {
    const resp = await fetch('http://localhost:8080/v1/models', { signal: AbortSignal.timeout(1000) });
    if (resp.ok) {
      const data = await resp.json() as any;
      const model = data?.data?.[0]?.id || 'default';
      detectedProvider = { provider: 'mlx', baseURL: 'http://localhost:8080/v1', apiKey: 'not-needed', model };
      process.stderr.write(`[memory-crystal] LLM provider: MLX (${model})\n`);
      return detectedProvider;
    }
  } catch {}

  // 2. Ollama (localhost:11434) ... only if a chat model is available
  try {
    const resp = await fetch('http://localhost:11434/api/tags', { signal: AbortSignal.timeout(1000) });
    if (resp.ok) {
      const data = await resp.json() as any;
      const models = (data?.models || []) as Array<{ name: string }>;
      // Look for a chat-capable model (skip embedding-only models like nomic-embed-text)
      const embeddingOnly = ['nomic-embed-text', 'mxbai-embed', 'all-minilm', 'snowflake-arctic-embed'];
      const chatModel = models.find(m => !embeddingOnly.some(e => m.name.startsWith(e)));
      if (chatModel) {
        detectedProvider = { provider: 'ollama', baseURL: 'http://localhost:11434/v1', apiKey: 'ollama', model: chatModel.name };
        process.stderr.write(`[memory-crystal] LLM provider: Ollama (${chatModel.name})\n`);
        return detectedProvider;
      }
    }
  } catch {}

  // 3. OpenAI API (env var first, then 1Password)
  const openaiKey = process.env.OPENAI_API_KEY || getOpSecret('OpenAI API', 'api key');
  if (openaiKey) {
    detectedProvider = { provider: 'openai', baseURL: 'https://api.openai.com/v1', apiKey: openaiKey, model: 'gpt-4o-mini' };
    process.stderr.write('[memory-crystal] LLM provider: OpenAI API\n');
    return detectedProvider;
  }

  // 4. Anthropic API (env var first, then 1Password)
  // Note: OAuth tokens (sk-ant-oat01-) need exchange flow. Direct API keys (sk-ant-api03-) work directly.
  const anthropicKey = process.env.ANTHROPIC_API_KEY || getOpSecret('Anthropic Auth Token - remote bunkers', 'Auth Token');
  if (anthropicKey && !anthropicKey.startsWith('sk-ant-oat')) {
    detectedProvider = { provider: 'anthropic', baseURL: 'https://api.anthropic.com', apiKey: anthropicKey, model: 'claude-haiku-4-5-20251001' };
    process.stderr.write('[memory-crystal] LLM provider: Anthropic API\n');
    return detectedProvider;
  }

  // 5. None
  detectedProvider = { provider: 'none', baseURL: '', apiKey: '', model: '' };
  process.stderr.write('[memory-crystal] LLM provider: none (deep search unavailable)\n');
  return detectedProvider;
}

/** Call an OpenAI-compatible chat completions endpoint. */
async function chatComplete(config: ProviderConfig, messages: Array<{ role: string; content: string }>, maxTokens = 300): Promise<string> {
  if (config.provider === 'sampling') {
    return samplingComplete(messages, maxTokens);
  }
  if (config.provider === 'anthropic') {
    return anthropicComplete(config, messages, maxTokens);
  }

  const resp = await fetch(`${config.baseURL}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${config.apiKey}`,
    },
    body: JSON.stringify({
      model: config.model,
      messages,
      max_tokens: maxTokens,
      temperature: 0.7,
    }),
  });

  if (!resp.ok) throw new Error(`LLM request failed: ${resp.status}`);
  const data = await resp.json() as any;
  return data.choices?.[0]?.message?.content || '';
}

/** Anthropic Messages API (not OpenAI-compatible). */
async function anthropicComplete(config: ProviderConfig, messages: Array<{ role: string; content: string }>, maxTokens: number): Promise<string> {
  // Extract system message if present
  const systemMsg = messages.find(m => m.role === 'system');
  const userMessages = messages.filter(m => m.role !== 'system');

  const body: any = {
    model: config.model,
    max_tokens: maxTokens,
    messages: userMessages,
  };
  if (systemMsg) body.system = systemMsg.content;

  const resp = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': config.apiKey,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify(body),
  });

  if (!resp.ok) throw new Error(`Anthropic request failed: ${resp.status}`);
  const data = await resp.json() as any;
  return data.content?.[0]?.text || '';
}

/** MCP Sampling: ask the client (Claude Code) to generate a completion via the user's subscription. */
async function samplingComplete(messages: Array<{ role: string; content: string }>, maxTokens: number): Promise<string> {
  if (!samplingServer) throw new Error('MCP sampling server not set');

  // Extract system message
  const systemMsg = messages.find(m => m.role === 'system');
  const userMessages = messages.filter(m => m.role !== 'system');

  // Build MCP sampling request
  const result = await samplingServer.createMessage({
    messages: userMessages.map((m: { role: string; content: string }) => ({
      role: m.role as 'user' | 'assistant',
      content: { type: 'text' as const, text: m.content },
    })),
    systemPrompt: systemMsg?.content,
    maxTokens,
    modelPreferences: {
      // Request cheap, fast model (Haiku-class). We don't need Opus for query expansion.
      costPriority: 0.9,
      speedPriority: 0.8,
      intelligencePriority: 0.3,
      hints: [{ name: 'haiku' }],
    },
  });

  // Extract text from response
  if (result?.content?.type === 'text') return result.content.text;
  if (typeof result?.content === 'string') return result.content;
  return '';
}

// ── Query Expansion ──

const EXPAND_PROMPT = `You are a search query expander. Given a search query, generate exactly 3 variations to improve search recall.

Output exactly 3 lines in this format (no other text):
lex: <keyword-focused variation for full-text search>
vec: <semantic variation rephrased for embedding similarity>
hyde: <hypothetical document snippet that would answer this query>

Rules:
- Each variation must contain at least one term from the original query
- Keep variations concise (under 30 words each)
- lex should use specific keywords and synonyms
- vec should rephrase the intent naturally
- hyde should be a short passage as if answering the query`;

export async function expandQuery(query: string): Promise<QueryVariation[]> {
  // Check cache
  const cached = expansionCache.get(query);
  if (cached) return cached;

  const config = await detectProvider();
  if (config.provider === 'none') return [];

  try {
    const result = await chatComplete(config, [
      { role: 'system', content: EXPAND_PROMPT },
      { role: 'user', content: query },
    ], 300);

    const lines = result.trim().split('\n');
    const queryLower = query.toLowerCase();
    const queryTerms = queryLower.replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter(Boolean);

    const hasQueryTerm = (text: string): boolean => {
      const lower = text.toLowerCase();
      if (queryTerms.length === 0) return true;
      return queryTerms.some(term => lower.includes(term));
    };

    const variations: QueryVariation[] = lines.map(line => {
      const colonIdx = line.indexOf(':');
      if (colonIdx === -1) return null;
      const type = line.slice(0, colonIdx).trim();
      if (type !== 'lex' && type !== 'vec' && type !== 'hyde') return null;
      const text = line.slice(colonIdx + 1).trim();
      if (!text || !hasQueryTerm(text)) return null;
      return { type: type as QueryVariation['type'], text };
    }).filter((v): v is QueryVariation => v !== null);

    if (variations.length > 0) {
      expansionCache.set(query, variations);
      return variations;
    }
  } catch (err) {
    process.stderr.write(`[memory-crystal] Query expansion failed: ${(err as Error).message}\n`);
  }

  // Fallback
  const fallback: QueryVariation[] = [
    { type: 'lex', text: query },
    { type: 'vec', text: query },
    { type: 'hyde', text: `Information about ${query}` },
  ];
  return fallback;
}

// ── Re-ranking ──

const RERANK_PROMPT = `You are a search result re-ranker. Given a query and a list of text passages, rate each passage's relevance to the query.

Output one line per passage in this exact format:
<index>: <score>

Where index is the passage number (0-based) and score is a float from 0.0 to 1.0.
- 1.0 = perfectly relevant, directly answers the query
- 0.7 = highly relevant, closely related
- 0.4 = somewhat relevant, tangentially related
- 0.1 = barely relevant
- 0.0 = not relevant at all

Rate ALL passages. Output nothing else.`;

export async function rerankResults(query: string, passages: string[]): Promise<RerankResult[]> {
  const config = await detectProvider();
  if (config.provider === 'none') {
    return passages.map((_, i) => ({ index: i, score: 1.0 - i * 0.01 }));
  }

  try {
    const passageList = passages.map((p, i) => `[${i}] ${p.slice(0, 500)}`).join('\n\n');
    const result = await chatComplete(config, [
      { role: 'system', content: RERANK_PROMPT },
      { role: 'user', content: `Query: ${query}\n\nPassages:\n${passageList}` },
    ], 200);

    const results: RerankResult[] = [];
    for (const line of result.trim().split('\n')) {
      const match = line.match(/^(\d+):\s*([\d.]+)/);
      if (match) {
        results.push({ index: parseInt(match[1]), score: parseFloat(match[2]) });
      }
    }

    // Fill in any missing indices with low scores
    const scored = new Set(results.map(r => r.index));
    for (let i = 0; i < passages.length; i++) {
      if (!scored.has(i)) results.push({ index: i, score: 0.0 });
    }

    return results.sort((a, b) => b.score - a.score);
  } catch (err) {
    process.stderr.write(`[memory-crystal] Reranking failed: ${(err as Error).message}\n`);
    return passages.map((_, i) => ({ index: i, score: 1.0 - i * 0.01 }));
  }
}
