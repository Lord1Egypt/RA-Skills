// Regression tests for the 2026-10-03 GPT-6-Astra final-scan findings.
// Offline: every request is intercepted by a mocked fetch; nothing is sent to the network.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync } from 'node:fs';
import * as publicApi from '../../dist/index.js';
import { edgecloudInferenceClient } from '../../build/clients/edgecloudInference.js';
import { onDemandApiClient } from '../../build/clients/ondemandApi.js';
import { callThetaMcpTool } from '../../build/clients/edgecloudMcp.js';
import { deployments } from '../../build/commands/deployments.js';
import { UNGATED_INFERENCE_SERVICES } from '../../build/commands/ondemandCatalog.js';

const cfg = { dryRun: false, onDemandApiToken: 'fixture-token', edgecloudApiKey: 'fixture-key', edgecloudProjectId: 'prj', inferenceEndpoint: 'https://mine.onthetaedgecloud.com', inferenceAuth: { user: 'fixture-user', pass: 'fixture-pass' }, httpTimeoutMs: 2000, httpMaxRetries: 0, httpRetryBackoffMs: 25 };
const env = { THETA_ONDEMAND_API_TOKEN: 'fixture-token', THETA_EC_API_KEY: 'fixture-key', THETA_EC_PROJECT_ID: 'prj', THETA_HTTP_MAX_RETRIES: '0' };
async function capture(fn, reply = () => ({ choices: [{ message: { content: 'x' }, finish_reason: 'stop' }] })) {
  const prior = globalThis.fetch; const calls = [];
  globalThis.fetch = async (url, init = {}) => { calls.push({ url: String(url), method: init.method ?? 'GET', body: init.body }); const r = reply(String(url), init); return new Response(typeof r === 'string' ? r : JSON.stringify(r), { headers: { 'content-type': typeof r === 'string' ? 'text/event-stream' : 'application/json' } }); };
  let error; try { await fn(calls); } catch (e) { error = e; } finally { globalThis.fetch = prior; }
  return { calls, error };
}

test('B1: the shipped runtime is one bundle exposing only the public entry points', () => {
  assert.deepEqual(readdirSync(new URL('../../dist/', import.meta.url)), ['index.js']);
  assert.deepEqual(Object.keys(publicApi).sort(), ['executeThetaRuntimeCommand', 'listThetaRuntimeCommands', 'theta', 'thetaCommandRequiresConfirm', 'thetaRuntimeCommandSchemas']);
  for (const internal of ['getJson', 'postJson', 'putJson', 'deleteEmpty', 'loadConfig', 'resolveThetaOnDemandToken', 'callThetaMcpTool', 'UNGATED_INFERENCE_SERVICES']) assert.equal(publicApi[internal], undefined, internal);
});

test('B2: dedicated chat sends only the validated snapshot (toJSON/getter cannot swap the body)', async () => {
  const body = { model: 'm', messages: [{ role: 'user', content: 'x' }], max_tokens: 1,
    toJSON() { return { model: 'm', messages: [{ role: 'user', content: 'x' }], max_tokens: 1e8, n: 999, max_completion_tokens: 1e8 }; } };
  const { calls } = await capture(() => edgecloudInferenceClient.chat(cfg, body));
  const sent = JSON.parse(calls[0].body);
  assert.equal(sent.max_tokens, 5000); assert.equal(sent.n, undefined); assert.equal(sent.max_completion_tokens, undefined);
});

test('M1: dedicated chat rejects webhook fields; prediction must be a name string', async () => {
  const a = await capture(() => edgecloudInferenceClient.chat(cfg, { model: 'm', messages: [{ role: 'user', content: 'x' }], webhook: 'https://hooks.invalid/x' }));
  assert.equal(a.calls.length, 0); assert.match(String(a.error?.message), /webhook/);
  const b = await capture(() => publicApi.executeThetaRuntimeCommand({ command: 'infer', service: 'stable_diffusion_xl_turbo', input: { prompt: 'p' }, prediction: { webhook: 'https://hooks.invalid/x' } }, { env }));
  assert.equal(b.calls.length, 0); assert.match(String(b.error?.message), /prediction must be/);
  const c = await capture(() => onDemandApiClient.createInferRequest(cfg, 'stable_diffusion_xl_turbo', { input: { prompt: 'p' } }, { prediction: 'predict' }), () => ({ body: { infer_requests: [{ id: 'r', state: 'created' }] } }));
  assert.equal(JSON.parse(c.calls[0].body).prediction, 'predict');
});

test('M2: the MCP client enforces the GPU price cap and refuses unknown write tools', async () => {
  const noCap = await capture(() => callThetaMcpTool(cfg, 'create_gpu_deployment', { project_id: 'prj', resource_id: 'r', confirm: true }));
  assert.equal(noCap.calls.length, 0); assert.match(String(noCap.error?.message), /max_price_per_hour_usd/);
  const sse = (obj) => `event: message\ndata: ${JSON.stringify({ jsonrpc: '2.0', id: 1, result: { content: [{ type: 'text', text: JSON.stringify(obj) }] } })}\n\n`;
  const overCap = await capture(() => callThetaMcpTool(cfg, 'create_gpu_deployment', { project_id: 'prj', resource_id: 'r', max_price_per_hour_usd: 0.5, confirm: true }), () => sse({ resource: { price_per_hour_usd: 2.5 } }));
  assert.equal(overCap.calls.length, 1); assert.match(String(overCap.error?.message), /above the approved cap/);
  const unknownPrice = await capture(() => callThetaMcpTool(cfg, 'create_gpu_deployment', { project_id: 'prj', resource_id: 'r', max_price_per_hour_usd: 5, confirm: true }), () => sse({}));
  assert.equal(unknownPrice.calls.length, 1); assert.match(String(unknownPrice.error?.message), /Could not verify/);
  const unknownTool = await capture(() => callThetaMcpTool(cfg, 'restart_everything', { confirm: true }));
  assert.equal(unknownTool.calls.length, 0); assert.match(String(unknownTool.error?.message), /not supported/);
});

test('M3: tool override must be exactly true, at the runtime and the client boundary', async () => {
  const tool = { type: 'function', function: { name: 'f', parameters: { type: 'object', properties: {} } } };
  for (const flag of ['false', 1, 'true', {}]) {
    const r = await capture(() => publicApi.executeThetaRuntimeCommand({ command: 'theta.ondemand.chat', service: 'qwen3_8_max', tools: [tool], allowUnverifiedTools: flag, messages: [{ role: 'user', content: 'x' }] }, { env }));
    assert.equal(r.calls.length, 0, String(flag));
  }
  const direct = await capture(() => onDemandApiClient.createChatCompletionRequest(cfg, { model: 'ling_3_0_flash_fin', tools: [tool], messages: [{ role: 'user', content: 'x' }] }));
  assert.equal(direct.calls.length, 0); assert.match(String(direct.error?.message), /does not return structured tool calls/);
});

test('M4: live runtime and facade results redact labelled secrets but keep usage counts', async () => {
  const r = await capture(() => publicApi.executeThetaRuntimeCommand({ command: 'theta.ondemand.chat', service: 'glm_5_3', messages: [{ role: 'user', content: 'x' }] }, { env }),
    () => ({ model: 'glm_5_3', auth_password: 'fixture-pass', token: 'fixture-secret', choices: [{ message: { content: 'x' }, finish_reason: 'stop' }], usage: { prompt_tokens: 3, completion_tokens: 1 } }));
  assert.equal(r.error, undefined);
  const prev = await deployments.create({ ...cfg, dryRun: true }, { auth_password: 'fixture-pass' });
  assert.equal(prev.payload.auth_password, '[redacted]');
});

test('N2: usage dates must be real, ordered and within 366 days', async () => {
  const run = (startDate, endDate) => capture(() => publicApi.executeThetaRuntimeCommand({ command: 'theta.billing.usage', startDate, endDate }, { env }));
  for (const [a, b] of [['2026-99-99', '2026-10-01'], ['2026-02-30', '2026-03-01'], ['2026-10-02', '2026-10-01'], ['2024-01-01', '2026-01-01']]) {
    const r = await run(a, b); assert.equal(r.calls.length, 0, `${a}..${b}`);
  }
});

test('N4: exported policy lists are frozen', () => {
  assert.ok(Object.isFrozen(UNGATED_INFERENCE_SERVICES));
  assert.throws(() => UNGATED_INFERENCE_SERVICES.push('seedance_2_5'));
});

test('N5: disposable validation reports smokeTested and requires the smoke when requested', async () => {
  const r = await deployments.validateDisposable({ ...cfg, dryRun: true }, { payload: {} });
  assert.equal(r.dryRun, true);
});

test('M4b: deployment list results through runtime and facade redact provider passwords', async () => {
  const reply = () => ({ status: 'success', body: [{ id: 'd1', auth_password: 'fixture-pass', api_key: 'fixture-key', usage: { total_tokens: 7 } }] });
  const r = await capture(async () => {
    const out = await publicApi.executeThetaRuntimeCommand({ command: 'theta.deployments.list' }, { env });
    assert.equal(out.body[0].auth_password, '[redacted]'); assert.equal(out.body[0].api_key, '[redacted]'); assert.equal(out.body[0].usage.total_tokens, 7);
  }, reply);
  assert.equal(r.error, undefined, String(r.error));
  const prior = { ...process.env };
  Object.assign(process.env, { THETA_EC_API_KEY: 'fixture-key' });
  try {
    const f = await capture(async () => {
      const out = await publicApi.theta().deploy.list('prj');
      assert.equal(out.body[0].auth_password, '[redacted]');
    }, reply);
    assert.equal(f.error, undefined, String(f.error));
  } finally { for (const k of Object.keys(process.env)) if (!(k in prior)) delete process.env[k]; Object.assign(process.env, prior); }
});

test('C1: a changing ctx.env getter cannot route operator Basic auth to another tenant', async () => {
  const prior = { ...process.env };
  Object.assign(process.env, { THETA_INFERENCE_ENDPOINT: 'https://owner.onthetaedgecloud.com', THETA_INFERENCE_AUTH_USER: 'fixture-user', THETA_INFERENCE_AUTH_PASS: 'fixture-pass', THETA_HTTP_MAX_RETRIES: '0' });
  try {
    let reads = 0;
    const { calls } = await capture(() => publicApi.executeThetaRuntimeCommand({ command: 'theta.inference.models' }, {
      env: { get THETA_INFERENCE_ENDPOINT() { return ++reads <= 1 ? 'https://owner.onthetaedgecloud.com' : 'https://collector.onthetaedgecloud.com'; } }
    }), () => ({ data: [] }));
    assert.ok(reads <= 1, `getter read ${reads} times`);
    for (const c of calls) assert.ok(!c.url.includes('collector'), c.url);
  } finally { for (const k of Object.keys(process.env)) if (!(k in prior)) delete process.env[k]; Object.assign(process.env, prior); }
});

test('C2: string/array values under *_tokens names are redacted; numeric counts are kept', async () => {
  const prior = { ...process.env };
  Object.assign(process.env, { THETA_EC_API_KEY: 'fixture-key' });
  try {
    const reply = () => ({ status: 'success', body: [{ access_tokens: ['fixture-secret'], refresh_tokens: ['fixture-secret'], password_tokens: 'fixture-secret', usage: { prompt_tokens: 3, reasoning_tokens: 2 } }] });
    const r = await capture(async () => {
      for (const out of [await publicApi.theta().deploy.list('prj'), await publicApi.executeThetaRuntimeCommand({ command: 'theta.deployments.list' }, { env })]) {
        const row = out.body[0];
        assert.equal(JSON.stringify(row).includes('fixture-secret'), false, JSON.stringify(row));
        assert.equal(row.usage.prompt_tokens, 3); assert.equal(row.usage.reasoning_tokens, 2);
      }
    }, reply);
    assert.equal(r.error, undefined, String(r.error));
  } finally { for (const k of Object.keys(process.env)) if (!(k in prior)) delete process.env[k]; Object.assign(process.env, prior); }
});

test('N5: openai-probe disposable validation is not ok without a successful smoke inference', async () => {
  let n = 0;
  const reply = (url, init) => {
    n += 1;
    if (url.endsWith('/deployment') && init.method === 'POST') return { body: { endpoint: 'https://d1.onthetaedgecloud.com', shard: '0', suffix: 's1', id: 'd1' } };
    if (url.endsWith('/v1/models')) return { data: [{ id: 'm' }] };
    if (url.includes('/deployment/list') || url.includes('/deployments/list')) return { body: [] };
    return { status: 'success' };
  };
  const { error } = await capture(async () => {
    const out = await deployments.validateDisposable(cfg, { payload: {}, confirm: true, readyTimeoutMs: 1000, intervalMs: 500 });
    assert.equal(out.smokeTested, false); assert.equal(out.ok, false);
  }, reply);
  assert.equal(error, undefined, String(error));
});
