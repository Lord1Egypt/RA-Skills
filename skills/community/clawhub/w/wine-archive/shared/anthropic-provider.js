const fs = require('fs');
const path = require('path');
const Anthropic = require('@anthropic-ai/sdk');
const { logLlmCall, estimateTokensFromChars } = require('./interaction-store');
const { normalizeAnthropicModel } = require('./model-utils');

const DEFAULT_TIMEOUT_MS = Number(process.env.ANTHROPIC_AGENT_TIMEOUT_MS || 60_000);
const SMOKE_TEST_TIMEOUT_MS = 20_000;
const SMOKE_TEST_PROMPT = 'Reply with exactly AUTH_OK and nothing else.';
const DEFAULT_MAX_TOKENS = Number(process.env.ANTHROPIC_MAX_TOKENS || 2048);

let smokeTestPromise = null;
let cachedClient = null;

function parseDotEnv(dotEnvPath = path.resolve(process.cwd(), '.env')) {
  if (!fs.existsSync(dotEnvPath)) return {};
  const raw = fs.readFileSync(dotEnvPath, 'utf8');
  const result = {};

  for (const line of raw.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const match = trimmed.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/);
    if (!match) continue;
    let [, key, value] = match;
    value = value.trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    result[key] = value;
  }

  return result;
}

function resolveApiKey() {
  const envApiKey = process.env.ANTHROPIC_API_KEY?.trim();
  const dotEnv = parseDotEnv();
  const fileApiKey = dotEnv.ANTHROPIC_API_KEY?.trim();
  const apiKey = envApiKey || fileApiKey;
  const oauthToken = process.env.CLAUDE_CODE_OAUTH_TOKEN?.trim() || dotEnv.CLAUDE_CODE_OAUTH_TOKEN?.trim();

  if (oauthToken) {
    throw new Error('Standard API-key mode requires CLAUDE_CODE_OAUTH_TOKEN to be unset. Remove it before using the Anthropic API-key wrapper.');
  }

  if (!apiKey) {
    throw new Error('Missing ANTHROPIC_API_KEY. Set it in the environment or .env before using the Anthropic API-key wrapper.');
  }

  return apiKey;
}

function getAnthropicClient() {
  if (cachedClient) return cachedClient;
  const apiKey = resolveApiKey();
  cachedClient = new Anthropic({ apiKey });
  return cachedClient;
}

function extractTextFromResponse(response) {
  if (!response || !Array.isArray(response.content)) return '';
  return response.content
    .map((block) => (block && block.type === 'text' && typeof block.text === 'string' ? block.text : ''))
    .filter(Boolean)
    .join('\n')
    .trim();
}

async function collectMessageText({ model, prompt, timeoutMs, maxTokens = DEFAULT_MAX_TOKENS, signal }) {
  const client = getAnthropicClient();
  const response = await client.messages.create(
    {
      model,
      max_tokens: maxTokens,
      messages: [{ role: 'user', content: prompt }],
    },
    {
      signal,
      timeout: timeoutMs,
    }
  );

  return {
    text: extractTextFromResponse(response),
    usage: response.usage || {},
  };
}

async function runSmokeTestIfNeeded() {
  if (process.env.ANTHROPIC_AGENT_SKIP_SMOKE_TEST === '1') return;
  if (!smokeTestPromise) {
    smokeTestPromise = (async () => {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(new Error('Smoke test timed out')), SMOKE_TEST_TIMEOUT_MS);

      try {
        resolveApiKey();
        const { text } = await collectMessageText({
          model: normalizeAnthropicModel(process.env.ANTHROPIC_AGENT_SMOKE_TEST_MODEL || 'claude-sonnet-4'),
          prompt: SMOKE_TEST_PROMPT,
          timeoutMs: SMOKE_TEST_TIMEOUT_MS,
          maxTokens: 32,
          signal: controller.signal,
        });

        if (!/\bAUTH_OK\b/.test(text)) {
          throw new Error(`Anthropic smoke test failed: expected AUTH_OK, got ${JSON.stringify(text)}`);
        }
      } catch (error) {
        smokeTestPromise = null;
        throw new Error(`Anthropic API-key smoke test failed. Check ANTHROPIC_API_KEY and Anthropic API access. Cause: ${error.message}`);
      } finally {
        clearTimeout(timer);
      }
    })();
  }

  return smokeTestPromise;
}

async function runAnthropicPrompt({ model, prompt, timeoutMs = DEFAULT_TIMEOUT_MS, caller = 'unknown', maxTurns = 1, skipLog = false } = {}) {
  if (!prompt) throw new Error('runAnthropicPrompt requires a prompt.');
  void maxTurns;

  const startedAt = Date.now();
  const normalizedModel = normalizeAnthropicModel(model || 'claude-sonnet-4');
  resolveApiKey();

  await runSmokeTestIfNeeded();

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(new Error(`Anthropic API call timed out after ${timeoutMs}ms`)), timeoutMs);

  try {
    const { text, usage } = await collectMessageText({
      model: normalizedModel,
      prompt,
      timeoutMs,
      signal: controller.signal,
    });

    const inputTokens = usage.input_tokens ?? estimateTokensFromChars(prompt);
    const outputTokens = usage.output_tokens ?? estimateTokensFromChars(text);
    const durationMs = Date.now() - startedAt;
    if (!skipLog) {
      logLlmCall({
        provider: 'anthropic',
        model: normalizedModel,
        caller,
        prompt,
        response: text,
        inputTokens,
        outputTokens,
        durationMs,
        ok: true,
      });
    }

    return { text, provider: 'anthropic', model: normalizedModel };
  } catch (error) {
    const durationMs = Date.now() - startedAt;
    if (!skipLog) {
      logLlmCall({
        provider: 'anthropic',
        model: normalizedModel,
        caller,
        prompt,
        response: '',
        inputTokens: estimateTokensFromChars(prompt),
        outputTokens: 0,
        durationMs,
        ok: false,
        error: error.message,
      });
    }
    throw error;
  } finally {
    clearTimeout(timer);
  }
}

module.exports = {
  extractTextFromResponse,
  parseDotEnv,
  resolveApiKey,
  runAnthropicPrompt,
};
