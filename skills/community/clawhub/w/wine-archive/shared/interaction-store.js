const fs = require('fs');
const path = require('path');
const { DatabaseSync } = require('node:sqlite');

const DB_PATH = process.env.LLM_LOG_DB_PATH || path.resolve(process.cwd(), 'data', 'llm-interactions.sqlite');
const MAX_LOG_CHARS = 10_000;

const PRICING_USD_PER_MILLION_TOKENS = Object.freeze({
  'claude-opus-4': { input: 15, output: 75 },
  'claude-sonnet-4': { input: 3, output: 15 },
  'claude-haiku-4': { input: 1, output: 5 },
  'gpt-4.1': { input: 2, output: 8 },
  'gpt-4o': { input: 2.5, output: 10 },
  'gpt-4o-mini': { input: 0.15, output: 0.6 },
});

let db;
let insertStmt;

function ensureDb() {
  if (db) return db;
  fs.mkdirSync(path.dirname(DB_PATH), { recursive: true });
  db = new DatabaseSync(DB_PATH);
  db.exec('PRAGMA journal_mode = WAL;');
  db.exec(`
    CREATE TABLE IF NOT EXISTS llm_calls (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      timestamp TEXT NOT NULL,
      provider TEXT,
      model TEXT,
      caller TEXT,
      prompt TEXT,
      response TEXT,
      input_tokens INTEGER,
      output_tokens INTEGER,
      cost_estimate REAL,
      duration_ms INTEGER,
      ok INTEGER NOT NULL,
      error TEXT
    );
  `);
  insertStmt = db.prepare(`
    INSERT INTO llm_calls (
      timestamp, provider, model, caller, prompt, response,
      input_tokens, output_tokens, cost_estimate, duration_ms, ok, error
    ) VALUES (
      @timestamp, @provider, @model, @caller, @prompt, @response,
      @input_tokens, @output_tokens, @cost_estimate, @duration_ms, @ok, @error
    )
  `);
  return db;
}

function truncate(text, max = MAX_LOG_CHARS) {
  if (text == null) return text;
  const value = String(text);
  if (value.length <= max) return value;
  return `${value.slice(0, max)}…[truncated ${value.length - max} chars]`;
}

function redactSecrets(text) {
  if (text == null) return text;
  return String(text)
    .replace(/\b(sk-[A-Za-z0-9_-]{12,})\b/g, '[REDACTED_API_KEY]')
    .replace(/\b(ANTHROPIC_API_KEY|OPENAI_API_KEY|CLAUDE_CODE_OAUTH_TOKEN)\s*=\s*([^\s"']+)/gi, '$1=[REDACTED]')
    .replace(/\bBearer\s+[A-Za-z0-9._-]{16,}\b/gi, 'Bearer [REDACTED]')
    .replace(/\b(?:oauth|token|api[_-]?key|secret)\b\s*[:=]\s*(["'])?([A-Za-z0-9._-]{16,})\1?/gi, (m, q, token) => m.replace(token, '[REDACTED]'));
}

function estimateTokensFromChars(input) {
  if (input == null) return 0;
  return Math.max(1, Math.ceil(String(input).length / 4));
}

function normalizeModelForPricing(model) {
  if (!model) return null;
  const raw = String(model).replace(/^anthropic\//i, '').replace(/^openai\//i, '');
  const lower = raw.toLowerCase();
  if (lower.includes('claude-opus-4')) return 'claude-opus-4';
  if (lower.includes('claude-sonnet-4')) return 'claude-sonnet-4';
  if (lower.includes('claude-haiku-4')) return 'claude-haiku-4';
  if (lower.includes('gpt-4.1')) return 'gpt-4.1';
  if (lower.includes('gpt-4o-mini')) return 'gpt-4o-mini';
  if (lower.includes('gpt-4o')) return 'gpt-4o';
  return raw;
}

function estimateCostUsd({ model, inputTokens = 0, outputTokens = 0 }) {
  const pricing = PRICING_USD_PER_MILLION_TOKENS[normalizeModelForPricing(model)];
  if (!pricing) return null;
  return Number((((inputTokens / 1_000_000) * pricing.input) + ((outputTokens / 1_000_000) * pricing.output)).toFixed(6));
}

function logLlmCall(entry) {
  const payload = {
    timestamp: new Date().toISOString(),
    provider: entry.provider || null,
    model: entry.model || null,
    caller: entry.caller || null,
    prompt: truncate(redactSecrets(entry.prompt || '')),
    response: truncate(redactSecrets(entry.response || '')),
    input_tokens: entry.inputTokens ?? estimateTokensFromChars(entry.prompt || ''),
    output_tokens: entry.outputTokens ?? estimateTokensFromChars(entry.response || ''),
    cost_estimate: entry.costEstimate ?? estimateCostUsd({
      model: entry.model,
      inputTokens: entry.inputTokens ?? estimateTokensFromChars(entry.prompt || ''),
      outputTokens: entry.outputTokens ?? estimateTokensFromChars(entry.response || ''),
    }),
    duration_ms: entry.durationMs ?? null,
    ok: entry.ok ? 1 : 0,
    error: truncate(redactSecrets(entry.error || '')),
  };

  setImmediate(() => {
    try {
      ensureDb();
      insertStmt.run(payload);
    } catch (error) {
      console.error('[interaction-store] Failed to log LLM call:', error);
    }
  });
}

module.exports = {
  DB_PATH,
  PRICING_USD_PER_MILLION_TOKENS,
  ensureDb,
  estimateTokensFromChars,
  estimateCostUsd,
  logLlmCall,
  redactSecrets,
  truncate,
};
