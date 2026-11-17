// Regression tests for every proven finding of the 2026-10-03 independent review.
// Offline: every request is intercepted by a mocked fetch; nothing is sent to the network.
import test from 'node:test';
import assert from 'node:assert/strict';
import { executeThetaRuntimeCommand as run, theta } from '../../dist/index.js';
import { ondemand } from '../../build/commands/ondemand.js';
import { deployments } from '../../build/commands/deployments.js';
import { video } from '../../build/commands/video.js';
import { characterRequest } from '../../build/commands/characters.js';
import { edgecloudControllerClient } from '../../build/clients/edgecloudController.js';
import { thetaVideoClient } from '../../build/clients/thetaVideo.js';
import { onDemandApiClient } from '../../build/clients/ondemandApi.js';
import { callThetaMcpTool } from '../../build/clients/edgecloudMcp.js';
import { edgecloudInferenceClient } from '../../build/clients/edgecloudInference.js';

const cfg = { dryRun: false, onDemandApiToken: 'fixture-token', edgecloudApiKey: 'fixture-key', edgecloudProjectId: 'prj', videoSaId: 'sa', videoSaSecret: 'fixture-secret', charactersApiKey: 'fixture-game', inferenceEndpoint: 'https://mine.thetaedgecloud.com', httpTimeoutMs: 2000, httpMaxRetries: 0, httpRetryBackoffMs: 25 };
const env = { THETA_ONDEMAND_API_TOKEN: 'fixture-token', THETA_EC_API_KEY: 'fixture-key', THETA_EC_PROJECT_ID: 'prj', THETA_HTTP_MAX_RETRIES: '0' };

async function capture(fn) {
  const prior = globalThis.fetch; const calls = [];
  globalThis.fetch = async (url, init = {}) => { calls.push({ url: String(url), method: init.method ?? 'GET', body: init.body }); return new Response(JSON.stringify({ body: { infer_requests: [{ id: 'r', state: 'success', output: {} }] }, choices: [{ message: { content: 'x' }, finish_reason: 'stop' }] })); };
  let error; try { await fn(); } catch (e) { error = e; } finally { globalThis.fetch = prior; }
  return { calls, error };
}

test('B1: chat cannot reach a video/unknown service without confirm (allowUnknownService path)', async () => {
  for (const service of ['seedance_2_5', 'SEEDANCE_2_5', 'wan_2_2', 'kling_v2', 'veo3']) {
    const { calls, error } = await capture(() => run({ command: 'theta.ondemand.chat', service, allowUnknownService: true, messages: [{ role: 'user', content: 'x' }] }, { env }));
    assert.equal(calls.length, 0, service); assert.match(String(error?.message), /confirm:true/);
  }
});

test('M7: inference uses an allowlist; unknown slugs need confirm, listed ones do not', async () => {
  for (const service of ['wan_2_2', 'kling_v2', 'hunyuan_t2v', 'ltx_2', 'veo3', 'step_vid', 'seedance_2_5']) {
    const { calls, error } = await capture(() => run({ command: 'infer', service, input: { prompt: 'p' } }, { env }));
    assert.equal(calls.length, 0, service); assert.match(String(error?.message), /confirm:true/);
  }
  const ok = await capture(() => run({ command: 'infer', service: 'stable_diffusion_xl_turbo', input: { prompt: 'p' } }, { env }));
  assert.equal(ok.calls.length, 1);
});

test('B2: deep imports of every mutating module and client are gated (no request without confirm)', async () => {
  const attempts = [
    () => deployments.create(cfg, {}), () => deployments.delete(cfg, 'prj', 's', 'x'), () => deployments.start(cfg, 'prj', 's', 'x'),
    () => deployments.stop(cfg, 'prj', 's', 'x'), () => deployments.startByBaseId(cfg, 'prj', 'b'), () => deployments.validateDisposable(cfg, { payload: {} }),
    () => deployments.chatbotCreate(cfg, {}), () => deployments.chatbotUpdate(cfg, 'c', {}),
    () => deployments.chatbotDocumentCreate(cfg, 'c', 'prj', { filename: 'a.txt', content: 'x' }),
    () => video.uploadCreate(cfg), () => video.videoCreate(cfg, {}), () => video.streamCreate(cfg, {}), () => video.ingestorSelect(cfg, 'i', {}),
    () => characterRequest(cfg, 'delete', { gameId: 'g', characterId: 'c' }), () => characterRequest(cfg, 'session.message', { sessionId: 's', payload: {} }),
    () => edgecloudControllerClient.createDeployment(cfg, {}), () => edgecloudControllerClient.deleteDeployment(cfg, 'prj', 's', 'x'),
    () => thetaVideoClient.createStream(cfg, {}), () => onDemandApiClient.createInferRequest(cfg, 'seedance_2_5', { input: { prompt: 'p' } }),
    () => onDemandApiClient.createChatCompletionRequest(cfg, { model: 'seedance_2_5', messages: [{ role: 'user', content: 'x' }] }),
    () => callThetaMcpTool(cfg, 'create_gpu_deployment', { project_id: 'prj' }), () => callThetaMcpTool(cfg, 'delete_gpu_deployment', { deployment_id: 'd', confirm: 'true' }),
    () => ondemand.chat(cfg, 'seedance_2_5', [{ role: 'user', content: 'x' }], { allowUnknownService: true })
  ];
  for (const [i, attempt] of attempts.entries()) {
    const { calls, error } = await capture(attempt);
    const writes = calls.filter((c) => c.method !== 'GET');
    assert.equal(writes.length, 0, `attempt ${i} sent ${JSON.stringify(writes)}`);
    assert.match(String(error?.message), /confirm:true/, `attempt ${i}`);
  }
});

test('B3: theta() never returns credential values', () => {
  const t = theta();
  assert.equal(t.cfg, undefined);
  const text = JSON.stringify(t.configured);
  for (const secret of ['fixture', 'key', 'token', 'secret']) assert.ok(!text.toLowerCase().includes(secret + '"'), text);
  assert.equal(typeof t.configured.onDemand, 'boolean');
});

test('M1: every chat path clamps max_tokens to 5000 and strips fan-out/length fields', async () => {
  const msgs = [{ role: 'user', content: 'x' }];
  const paths = [
    () => run({ command: 'theta.ondemand.chat', service: 'glm_5_3', max_tokens: 10000000, extraInput: { max_completion_tokens: 1e6, n: 64, max_new_tokens: 2e5 }, messages: msgs }, { env }),
    () => run({ command: 'infer', service: 'glm_5_3', input: { messages: msgs, max_tokens: 1e6, n: 64 } }, { env }),
    () => run({ command: 'theta.ondemand.chat', service: 'qwen3', stream: false, extraInput: { max_new_tokens: 2e5, best_of: 9 }, messages: msgs }, { env }),
    () => edgecloudInferenceClient.chat(cfg, { model: 'm', messages: msgs, max_tokens: 1e7, n: 64 })
  ];
  for (const [i, p] of paths.entries()) {
    const { calls } = await capture(p);
    const body = JSON.parse(calls.find((c) => c.method === 'POST').body);
    const input = body.input ?? body;
    assert.ok(input.max_tokens >= 1 && input.max_tokens <= 5000, `path ${i}: ${input.max_tokens}`);
    for (const k of ['max_completion_tokens', 'n', 'max_new_tokens', 'best_of']) assert.equal(input[k], undefined, `path ${i} ${k}`);
  }
});

test('M3: webhooks require https and confirm', async () => {
  const a = await capture(() => run({ command: 'infer', service: 'stable_diffusion_xl_turbo', input: { prompt: 'p' }, payload: { input: { prompt: 'p' }, webhook: 'https://hooks.invalid/x' } }, { env }));
  assert.equal(a.calls.length, 0); assert.match(String(a.error?.message), /confirm:true/);
  const b = await capture(() => run({ command: 'infer', service: 'stable_diffusion_xl_turbo', payload: { input: { prompt: 'p' }, webhook: 'http://hooks.invalid/x' }, confirm: true }, { env }));
  assert.equal(b.calls.length, 0); assert.match(String(b.error?.message), /https/);
});

test('MINOR 1: caller ctx.env cannot switch off an operator-enabled dry-run', async () => {
  const prior = process.env.THETA_DRY_RUN; process.env.THETA_DRY_RUN = '1';
  try {
    const { calls } = await capture(() => run({ command: 'infer', service: 'stable_diffusion_xl_turbo', input: { prompt: 'p' } }, { env: { ...env, THETA_DRY_RUN: '0' } }));
    assert.equal(calls.length, 0);
  } finally { if (prior === undefined) delete process.env.THETA_DRY_RUN; else process.env.THETA_DRY_RUN = prior; }
});

test('MINOR 2: prototype command names are rejected cleanly', async () => {
  for (const command of ['__proto__', 'constructor', 'toString', 'hasOwnProperty']) {
    await assert.rejects(run({ command }, { env }), /Unsupported theta runtime command/);
  }
});

test('MINOR 9: dedicated chat validates its body', async () => {
  const { calls, error } = await capture(() => edgecloudInferenceClient.chat(cfg, { model: 'm' }));
  assert.equal(calls.length, 0); assert.match(String(error?.message), /messages/);
});
