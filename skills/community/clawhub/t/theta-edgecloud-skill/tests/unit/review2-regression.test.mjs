import assert from 'node:assert/strict';
import test from 'node:test';
import * as publicApi from '../../dist/index.js';
import { onDemandApiClient } from '../../build/clients/ondemandApi.js';
import { edgecloudControllerClient } from '../../build/clients/edgecloudController.js';
import { thetaVideoClient } from '../../build/clients/thetaVideo.js';
import { edgecloudInferenceClient } from '../../build/clients/edgecloudInference.js';
import { callThetaMcpTool } from '../../build/clients/edgecloudMcp.js';
import { ondemand } from '../../build/commands/ondemand.js';

const cfg = { dryRun: false, onDemandApiToken: 'SYNTH_TOKEN', edgecloudApiKey: 'SYNTH_KEY', videoSaId: 'sa', videoSaSecret: 'SYNTH_SECRET', inferenceEndpoint: 'https://mine.onthetaedgecloud.com', inferenceAuth: { user: 'u', pass: 'SYNTH_PASS' }, httpTimeoutMs: 1000, httpMaxRetries: 0, httpRetryBackoffMs: 25 };
async function capture(fn) {
  const old = globalThis.fetch;
  const calls = [];
  globalThis.fetch = async (url, init = {}) => {
    calls.push({ url: String(url), method: init.method ?? 'GET', headers: init.headers ?? {}, body: init.body });
    return new Response(JSON.stringify({ status: 'success', body: { infer_requests: [{ id: 'r1', state: 'success' }] }, object: 'list', data: [] }), { status: 200, headers: { 'content-type': 'application/json' } });
  };
  try { return await fn(calls); } finally { globalThis.fetch = old; }
}

test('B1 public entry never exports token resolver', () => {
  assert.deepEqual(Object.keys(publicApi).sort(), ['executeThetaRuntimeCommand', 'listThetaRuntimeCommands', 'theta', 'thetaCommandRequiresConfirm', 'thetaRuntimeCommandSchemas'].sort());
});

test('B2 ctx.env endpoint change never inherits operator Basic auth', async () => {
  const keys = ['THETA_INFERENCE_ENDPOINT', 'THETA_INFERENCE_AUTH_USER', 'THETA_INFERENCE_AUTH_PASS'];
  const old = Object.fromEntries(keys.map(k => [k, process.env[k]]));
  Object.assign(process.env, { THETA_INFERENCE_ENDPOINT: cfg.inferenceEndpoint, THETA_INFERENCE_AUTH_USER: 'u', THETA_INFERENCE_AUTH_PASS: 'SYNTH_PASS' });
  try {
    await capture(async calls => {
      await assert.rejects(() => publicApi.executeThetaRuntimeCommand({ command: 'theta.inference.models' }, { env: { THETA_INFERENCE_ENDPOINT: 'https://other-tenant.onthetaedgecloud.com' } }), /endpoint override/i);
      assert.equal(calls.length, 0);
    });
  } finally { for (const k of keys) old[k] === undefined ? delete process.env[k] : process.env[k] = old[k]; }
});

test('B3 nested webhook/callback and getter-shaped webhook are blocked with zero requests', async () => {
  await capture(async calls => {
    const attempts = [
      () => onDemandApiClient.createInferRequest(cfg, 'esrgan', { input: { input_img: 'f', webhook: 'http://hooks.invalid/x' } }),
      () => onDemandApiClient.createInferRequest(cfg, 'esrgan', { input: { callback_url: 'https://hooks.invalid/x' } }),
      () => onDemandApiClient.createChatCompletionRequest(cfg, { model: 'glm_5_3', messages: [{ role: 'user', content: 'x' }], input: { webhook: 'http://hooks.invalid/x' } }),
      () => onDemandApiClient.createInferRequest(cfg, 'esrgan', { input: { input_img: 'f' }, get webhook() { return 'http://hooks.invalid/x'; } })
    ];
    for (const run of attempts) await assert.rejects(async () => run());
    assert.equal(calls.length, 0);
  });
});

test('B3 extraInput cannot smuggle tools or webhook into chat', async () => {
  await capture(async calls => {
    await ondemand.chat(cfg, 'qwen3_8_flash', [{ role: 'user', content: 'x' }], { extraInput: { tools: [{ type: 'function' }], webhook: 'http://hooks.invalid/x' } });
    assert.equal(calls.length, 1);
    assert.doesNotMatch(String(calls[0].body), /tools|webhook|hooks\.invalid/);
  });
});

test('B4 deep client writes and inference honor cfg and operator dry-run', async () => {
  await capture(async calls => {
    const dry = { ...cfg, dryRun: true };
    const attempts = [
      () => edgecloudControllerClient.deleteDeployment(dry, 'p', 's', 'x', true),
      () => thetaVideoClient.createStream(dry, {}, true),
      () => callThetaMcpTool(dry, 'delete_gpu_deployment', { confirm: true }),
      () => onDemandApiClient.createInferRequest(dry, 'esrgan', { input: { input_img: 'f' } }),
      () => onDemandApiClient.createChatCompletionRequest(dry, { model: 'glm_5_3', messages: [{ role: 'user', content: 'x' }] }),
      () => onDemandApiClient.createInputPresignedUrls(dry, 'esrgan'),
      () => edgecloudInferenceClient.chat(dry, { model: 'm', messages: [{ role: 'user', content: 'x' }] })
    ];
    for (const run of attempts) await assert.rejects(async () => run(), /dry.run/i);
    process.env.THETA_DRY_RUN = '1';
    try { await assert.rejects(async () => onDemandApiClient.createInferRequest(cfg, 'esrgan', { input: { input_img: 'f' } }), /dry.run/i); }
    finally { delete process.env.THETA_DRY_RUN; }
    assert.equal(calls.length, 0);
  });
});

test('M1 alternate length/fanout keys stripped and wait clamped', async () => {
  await capture(async calls => {
    await onDemandApiClient.createInferRequest(cfg, 'glm_5_3', { max_tokens: 1e6, n: 40, input: { prompt: 'x', max_tokens: 1e6, max_length: 1e6, num_beams: 40 } }, { wait: 1e6 });
    const body = JSON.parse(calls[0].body);
    assert.equal(body.max_tokens, 5000);
    assert.equal(body.input.max_tokens, 5000);
    assert.equal(body.n, undefined);
    assert.equal(body.input.max_length, undefined);
    assert.equal(body.input.num_beams, undefined);
    assert.match(calls[0].url, /wait=60/);
    await assert.rejects(() => onDemandApiClient.createChatCompletionRequest(cfg, { model: 'glm_5_3', messages: 'bad', max_tokens: 1e6 }), /messages/);
    assert.equal(calls.length, 1);
  });
});

test('retired GPT OSS direct chat route requires confirm before any request', async () => {
  await capture(async calls => {
    await assert.rejects(() => onDemandApiClient.createChatCompletionRequest(cfg, { model: 'gpt_oss_120b', messages: [{ role: 'user', content: 'x' }] }), /confirm:true/);
    assert.equal(calls.length, 0);
  });
});

test('M2 facade binds operator config, and offers no caller endpoint parameter', async () => {
  const old = process.env.THETA_INFERENCE_ENDPOINT;
  const oldToken = process.env.THETA_ONDEMAND_API_TOKEN;
  process.env.THETA_INFERENCE_ENDPOINT = cfg.inferenceEndpoint;
  process.env.THETA_ONDEMAND_API_TOKEN = 'fixture-token'; // self-contained: never rely on a real token
  try {
  await capture(async calls => {
    const t = publicApi.theta();
    await t.ondemand.status('r1');
    assert.match(calls[0].url, /\/infer_request\/r1$/);
    await t.inference.models('https://other-tenant.onthetaedgecloud.com');
    assert.match(calls[1].url, /mine\.onthetaedgecloud\.com\/v1\/models$/);
  });
  } finally {
    old === undefined ? delete process.env.THETA_INFERENCE_ENDPOINT : process.env.THETA_INFERENCE_ENDPOINT = old;
    oldToken === undefined ? delete process.env.THETA_ONDEMAND_API_TOKEN : process.env.THETA_ONDEMAND_API_TOKEN = oldToken;
  }
});
