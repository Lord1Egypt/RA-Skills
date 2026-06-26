/**
 * llm-client-json-mode.test.ts — 3.3.12-rc.6 regression test.
 *
 * Verifies that `supportsJsonObjectResponseFormat` correctly identifies
 * OpenAI-compatible providers that honour the `response_format` body field.
 *
 * Why this exists:
 *   z.ai's GLM family silently returns empty `message.content` for the
 *   merged-extraction prompt unless `response_format: {"type": "json_object"}`
 *   is sent. Plugin 3.3.12-rc.5 auto-QA on 2026-05-09 revealed the
 *   extractor returned 0 raw facts on every batch — same bug Hermes hit
 *   in 2.3.1-rc.23 (already fixed Python-side as
 *   `_supports_json_object_response_format`). This test pins the TS port
 *   to the same provider list so a future refactor doesn't silently
 *   regress extraction again.
 *
 * Run with: npx tsx llm-client-json-mode.test.ts
 */

import { supportsJsonObjectResponseFormat } from './llm-client.js';

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

// Providers that MUST receive the hint (Python parity).
const SHOULD_HINT = [
  'https://api.z.ai/api/coding/paas/v4',
  'https://api.z.ai/api/paas/v4',
  'https://api.openai.com/v1',
  'https://api.groq.com/openai/v1',
  'https://openrouter.ai/api/v1',
  'https://api.deepseek.com',
  'https://api.mistral.ai/v1',
  'https://api.x.ai/v1',
  'https://api.together.xyz/v1',
];

// Endpoints that should NOT receive the hint (either non-OpenAI-compat or
// known to reject the field).
const SHOULD_NOT_HINT = [
  'https://api.anthropic.com/v1',
  'https://generativelanguage.googleapis.com/v1beta',
  'http://localhost:11434/v1', // Ollama — generally OK without; conservative no-hint
  '',
];

for (const url of SHOULD_HINT) {
  assert(
    supportsJsonObjectResponseFormat(url) === true,
    `hint set for ${url}`,
  );
}

for (const url of SHOULD_NOT_HINT) {
  assert(
    supportsJsonObjectResponseFormat(url) === false,
    `hint NOT set for ${url || '<empty>'}`,
  );
}

// Case-insensitive match (some configs upcase paths).
assert(
  supportsJsonObjectResponseFormat('HTTPS://API.Z.AI/API/PAAS/V4') === true,
  'case-insensitive match for upcased z.ai URL',
);

// Undefined defensively returns false.
assert(
  supportsJsonObjectResponseFormat(undefined) === false,
  'undefined baseUrl returns false (no crash)',
);

console.log(`\n# tests: ${passed + failed}, passed: ${passed}, failed: ${failed}`);
process.exit(failed > 0 ? 1 : 0);
