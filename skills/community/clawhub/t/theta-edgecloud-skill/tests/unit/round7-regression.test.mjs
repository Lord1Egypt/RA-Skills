// Regression tests for the 0.3.1 file-level promise audit (event streams, tool routing, pricing
// redaction in-module, whitespace-bounded error redaction, nested callbacks, HTTPS-only transport).
import test from 'node:test';
import assert from 'node:assert/strict';
import { executeThetaRuntimeCommand as run } from '../../dist/index.js';
import { onDemandApiClient } from '../../build/clients/ondemandApi.js';
import { getJson } from '../../build/clients/http.js';
import { billing } from '../../build/commands/gpu.js';
import { findCallbackFields } from '../../build/approval.js';
import { sanitizeHttpErrorMessage } from '../../build/errors.js';

const cfg = { dryRun: false, onDemandApiToken: 'fixture-token', edgecloudApiKey: 'fixture-key', httpTimeoutMs: 1000, httpMaxRetries: 0, httpRetryBackoffMs: 25 };
async function capture(handler, fn) {
  const prior = globalThis.fetch; const calls = [];
  globalThis.fetch = async (url, init = {}) => { calls.push({ url: String(url), method: init.method ?? 'GET' }); return handler(String(url), init); };
  try { let error; let result; try { result = await fn(); } catch (e) { error = e; } return { calls, error, result }; } finally { globalThis.fetch = prior; }
}
const chat = () => onDemandApiClient.createChatCompletionRequest(cfg, { model: 'glm_5_3', messages: [{ role: 'user', content: 'x' }] });

test('malformed or mislabelled event streams fail instead of reporting success', async () => {
  for (const [body, headers] of [
    ['data : not-json\n\n', { 'content-type': 'text/plain' }],
    ['event: message\ndata:{broken\n\n', { 'content-type': 'text/event-stream' }],
    ['partial body', { 'content-type': 'text/event-stream; charset=utf-8' }],
    ['data: {"choices":[{"delta":{"content":"a"}}]}\n\n', { 'content-type': 'text/event-stream' }]
  ]) {
    const { error, result, calls } = await capture(() => new Response(body, { status: 200, headers }), chat);
    assert.match(String(error?.message), /Malformed or incomplete Theta event stream/, `${body} -> ${JSON.stringify(result)}`);
    assert.equal(error.retriable, false, 'a possibly billed request is never marked retriable');
    assert.equal(calls.length, 1, 'never resent');
  }
  // Even with retries configured, a malformed stream is sent exactly once.
  const retrying = await capture(() => new Response('data:{broken\n\n', { headers: { 'content-type': 'text/event-stream' } }),
    () => onDemandApiClient.createChatCompletionRequest({ ...cfg, httpMaxRetries: 6 }, { model: 'glm_5_3', messages: [{ role: 'user', content: 'x' }] }));
  assert.equal(retrying.calls.length, 1);
  assert.equal(retrying.error?.code, 'THETA_ONDEMAND_MALFORMED_STREAM');
  // A well-formed terminated stream and a plain-text non-stream body still succeed.
  const ok = await capture(() => new Response('data: {"choices":[{"delta":{"content":"hi"},"finish_reason":"stop"}]}\n\ndata: [DONE]\n\n', { headers: { 'content-type': 'text/event-stream' } }), chat);
  assert.equal(ok.error, undefined, String(ok.error));
  const plain = await capture(() => new Response('ok', { headers: { 'content-type': 'text/plain' } }), chat);
  assert.equal(plain.error, undefined, String(plain.error));
  assert.equal(JSON.stringify(plain.result).includes('"stream":true'), false);
});

test('tools go only to GLM-5.3/Flash unless allowUnverifiedTools is exactly true (retired GPT-OSS included)', async () => {
  const tools = [{ type: 'function', function: { name: 'f', parameters: { type: 'object' } } }];
  for (const allow of [undefined, false, 'true', 1]) {
    const { calls, error } = await capture(() => new Response('{}'), () => onDemandApiClient.createChatCompletionRequest(cfg, { model: 'gpt_oss_120b', messages: [{ role: 'user', content: 'x' }], tools }, { confirm: true, allowUnverifiedTools: allow }));
    assert.match(String(error?.message), /does not return structured tool calls/);
    assert.equal(calls.length, 0);
  }
  const viaRuntime = await capture(() => new Response('{}'), () => run({ command: 'theta.ondemand.chat', service: 'gpt_oss_120b', messages: [{ role: 'user', content: 'x' }], tools, confirm: true }, { env: { THETA_ONDEMAND_API_TOKEN: 'fixture-token', THETA_HTTP_MAX_RETRIES: '0' } }));
  assert.ok(viaRuntime.error, 'runtime refuses GPT-OSS tools');
  assert.equal(viaRuntime.calls.length, 0);
});

test('billing.pricing redacts unknown token values inside the gpu module itself', async () => {
  const sse = (result) => new Response(`event: message\ndata: ${JSON.stringify({ jsonrpc: '2.0', id: 1, result: { content: [{ type: 'text', text: JSON.stringify(result) }] } })}\n\n`, { headers: { 'content-type': 'text/event-stream' } });
  const { error, result } = await capture(() => sse({ chatbot: [{ token: 'prompt_tokens', price: '750' }, { token: 'synthetic-secret', price: '1' }] }), () => billing.pricing(cfg, 'p'));
  assert.equal(error, undefined, String(error));
  assert.equal(result.chatbot[0].usage_type, 'prompt_tokens');
  assert.equal(JSON.stringify(result).includes('synthetic-secret'), false);
});

test('unquoted labelled secrets are redacted through to whitespace, including closing brackets', () => {
  for (const [input, secret] of [['password=alpha)omega', 'omega'], ['token=a]SYN_B', 'SYN_B'], ['secret=x}SYN_C rest', 'SYN_C']]) {
    const out = sanitizeHttpErrorMessage(input);
    assert.equal(out.includes(secret), false, `${input} -> ${out}`);
  }
  assert.equal(sanitizeHttpErrorMessage('password=alpha)omega rest'), 'password=[redacted] rest');
});

test('callback walker reports nested webhook/callback fields inside a matched field', () => {
  const found = findCallbackFields({ webhook: { callback: 'https://example.invalid' } });
  assert.deepEqual(found.map((f) => f.path), ['webhook', 'webhook.callback']);
});

test('shared transport refuses non-https URLs before any request', async () => {
  for (const url of ['http://api.thetavideoapi.com/x', 'ftp://x', 'file:///etc/passwd', '//host/x']) {
    const { calls, error } = await capture(() => new Response('{}'), () => getJson(url, {}));
    assert.match(String(error?.message), /Only https:\/\/ URLs are allowed/);
    assert.equal(calls.length, 0);
  }
});
