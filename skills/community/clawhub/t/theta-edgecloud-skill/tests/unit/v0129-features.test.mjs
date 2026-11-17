// Offline: every request is intercepted by a mocked fetch or dry-run; nothing is sent to the network.
import test from 'node:test';
import assert from 'node:assert/strict';
import { executeThetaRuntimeCommand as run, listThetaRuntimeCommands } from '../../dist/index.js';

const env = { THETA_ONDEMAND_API_TOKEN: 'test-token', THETA_HTTP_MAX_RETRIES: '0' };
const ctrlEnv = { THETA_EC_API_KEY: 'test-project-key', THETA_EC_PROJECT_ID: 'prj_test', THETA_HTTP_MAX_RETRIES: '0' };
const tool = { type: 'function', function: { name: 'multiply', parameters: { type: 'object', properties: {} } } };
async function mockFetch(mock, fn) { const prior = globalThis.fetch; globalThis.fetch = mock; try { await fn(); } finally { globalThis.fetch = prior; } }
function sse(result) { return new Response(`event: message\ndata: ${JSON.stringify({ jsonrpc: '2.0', id: 1, result })}\n\n`, { headers: { 'content-type': 'text/event-stream' } }); }
function textResult(obj) { return { content: [{ type: 'text', text: JSON.stringify(obj) }] }; }

for (const service of ['qwen3_8_max', 'qwen3_8_flash', 'ling_3_0_flash_fin']) test(`${service} routes to OpenAI-compatible chat/completions`, async () => {
  await mockFetch(async (url, init) => {
    assert.equal(url, 'https://ondemand.thetaedgecloud.com/infer_request/chat/completions');
    const body = JSON.parse(init.body);
    assert.equal(body.model, service);
    if (service.startsWith('qwen3_8')) assert.equal(body.enable_thinking, false);
    if (service === 'ling_3_0_flash_fin') assert.equal(body.max_tokens, 2048);
    return new Response(JSON.stringify({ model: service, choices: [{ message: { content: 'OK' }, finish_reason: 'stop' }] }));
  }, async () => {
    const r = await run({ command: 'theta.ondemand.chat', service, enable_thinking: service.startsWith('qwen3_8') ? false : undefined,
      messages: [{ role: 'user', content: 'Reply OK' }] }, { env });
    assert.equal(r.body.infer_requests[0].output.message, 'OK');
  });
});

test('tools on models that silently drop them fail before any paid call', async () => {
  await mockFetch(() => { throw new Error('unexpected network'); }, async () => {
    for (const service of ['qwen3_8_max', 'qwen3_8_flash', 'ling_3_0_flash_fin']) {
      await assert.rejects(run({ command: 'theta.ondemand.chat', service, tools: [tool], messages: [{ role: 'user', content: 'x' }] }, { env }), /does not return structured tool calls/);
    }
  });
});

test('infer sends prediction in body and query for multi-prediction services', async () => {
  await mockFetch(async (url, init) => {
    assert.equal(url, 'https://ondemand.thetaedgecloud.com/infer_request/image_to_image?prediction=background_removal');
    assert.equal(JSON.parse(init.body).prediction, 'background_removal');
    return new Response(JSON.stringify({ body: { infer_requests: [{ id: 'r', state: 'created' }] } }));
  }, async () => {
    await run({ command: 'infer', service: 'image_to_image', prediction: 'background_removal', input: { image_filename: 'f', style_image_filename: '' } }, { env });
  });
});

test('get_upload_url normalises the live presigned_url shape and states the PUT content type', async () => {
  await mockFetch(async () => new Response(JSON.stringify({ status: 'success', body: { input_img: { presigned_url: 'https://uploads.invalid/b/x?sig', filename: 'srvc/prj/input_img_1' } } })), async () => {
    const r = await run({ command: 'get_upload_url', service: 'esrgan', input_field: 'input_img' }, { env });
    assert.deepEqual(r.uploads.input_img, { upload_url: 'https://uploads.invalid/b/x?sig', filename: 'srvc/prj/input_img_1' });
    assert.match(r.uploadInstructions, /application\/octet-stream/);
  });
});

test('billing balance uses hosted MCP with project key and returns USD', async () => {
  await mockFetch(async (url, init) => {
    assert.equal(url, 'https://controller.thetaedgecloud.com/mcp');
    assert.equal(init.headers['x-api-key'], 'test-project-key');
    const rpc = JSON.parse(init.body);
    assert.equal(rpc.method, 'tools/call');
    assert.deepEqual(rpc.params, { name: 'get_billing_balance', arguments: { project_id: 'prj_test' } });
    return sse(textResult({ currency: 'USD', credit_balance: 100, balance_usd: 1 }));
  }, async () => {
    const r = await run({ command: 'theta.billing.balance' }, { env: ctrlEnv });
    assert.equal(r.source, 'theta-hosted-mcp');
    assert.equal(r.balance_usd, 1);
  });
});

test('GPU resource listing filters and sorts by USD price', async () => {
  const resources = [
    { resource_id: 'a', provider: 'community', gpu_model: 'NVIDIA-GeForce-RTX-5090', price_per_hour_usd: 0.715, gpu_count_available: 1 },
    { resource_id: 'b', provider: 'community', gpu_model: 'NVIDIA-GeForce-RTX-5060', price_per_hour_usd: 0.143, gpu_count_available: 1 },
    { resource_id: 'c', provider: 'hosted', gpu_model: 'H100', price_per_hour_usd: 2.5, gpu_count_available: 0 }
  ];
  await mockFetch(async () => sse(textResult({ environment: 'prod', resources })), async () => {
    const r = await run({ command: 'theta.gpu.resources.list', maxPricePerHourUsd: 1, availableOnly: true }, { env: ctrlEnv });
    assert.deepEqual(r.resources.map((x) => x.resource_id), ['b', 'a']);
    assert.equal(r.totalResources, 3);
  });
});

test('GPU create requires a price cap and confirm, and refuses an over-cap resource', async () => {
  await mockFetch(() => { throw new Error('unexpected network'); }, async () => {
    await assert.rejects(run({ command: 'theta.gpu.deployments.create', name: 'n', deploymentTemplateId: 't', resourceId: 'r', maxPricePerHourUsd: 0, confirm: true }, { env: ctrlEnv }), /maxPricePerHourUsd is required/);
    await assert.rejects(run({ command: 'theta.gpu.deployments.create', name: 'n', deploymentTemplateId: 't', resourceId: 'r', maxPricePerHourUsd: 1 }, { env: ctrlEnv }), /confirm:true/);
  });
  const calls = [];
  await mockFetch(async (_url, init) => {
    const rpc = JSON.parse(init.body); calls.push(rpc.params.name);
    return sse(textResult({ resource_id: 'r', price_per_hour_usd: 2.5 }));
  }, async () => {
    await assert.rejects(run({ command: 'theta.gpu.deployments.create', name: 'n', deploymentTemplateId: 't', resourceId: 'r', maxPricePerHourUsd: 1, confirm: true }, { env: ctrlEnv }), /above the approved cap/);
    assert.deepEqual(calls, ['get_gpu_resource']);
  });
});

test('GPU mutations dry-run without networking and MCP errors surface', async () => {
  await mockFetch(() => { throw new Error('unexpected network'); }, async () => {
    const r = await run({ command: 'theta.gpu.deployments.delete', deploymentId: 'd' }, { env: { ...ctrlEnv, THETA_DRY_RUN: '1' } });
    assert.equal(r.dryRun, true);
    assert.equal(r.tool, 'delete_gpu_deployment');
  });
  await mockFetch(async () => sse({ content: [{ type: 'text', text: 'deployment not found' }], isError: true }), async () => {
    await assert.rejects(run({ command: 'theta.gpu.deployments.logs', deploymentId: 'd' }, { env: ctrlEnv }), /get_gpu_deployment_logs failed: deployment not found/);
  });
});

test('billing usage validates dates; new commands are registered', async () => {
  await assert.rejects(run({ command: 'theta.billing.usage', startDate: '09/26/2026' }, { env: ctrlEnv }), /YYYY-MM-DD/);
  for (const c of ['theta.billing.usage', 'theta.billing.topUps', 'theta.billing.pricing', 'theta.gpu.resources.list', 'theta.gpu.resources.get',
    'theta.gpu.templates.list', 'theta.gpu.deployments.get', 'theta.gpu.deployments.events', 'theta.gpu.deployments.logs', 'theta.gpu.deployments.create']) {
    assert.ok(listThetaRuntimeCommands().includes(c), c);
  }
});

test('0.1.30: every resource mutation is code-gated on confirm:true outside dry-run', async () => {
  const { thetaCommandRequiresConfirm, thetaRuntimeCommandSchemas } = await import('../../dist/index.js');
  const gated = Object.keys(thetaRuntimeCommandSchemas).filter(thetaCommandRequiresConfirm);
  for (const c of ['theta.deployments.create', 'theta.deployments.delete', 'theta.deployments.startByBaseId', 'theta.deployments.validateDisposable',
    'theta.ai.agent.create', 'theta.ai.agent.document.update', 'theta.video.create', 'theta.video.streamCreate', 'theta.characters.delete',
    'theta.characters.session.create', 'theta.characters.session.context', 'theta.gpu.deployments.create', 'theta.gpu.deployments.delete']) {
    assert.ok(gated.includes(c), c);
    assert.match(thetaRuntimeCommandSchemas[c].description, /requires confirm:true/);
  }
  for (const c of ['theta.ondemand.chat', 'infer', 'theta.billing.balance', 'theta.gpu.resources.list']) assert.ok(!gated.includes(c), c);
  assert.ok(gated.includes('theta.characters.session.message'));
  await mockFetch(() => { throw new Error('unexpected network'); }, async () => {
    const env = { ...ctrlEnv, THETA_VIDEO_SA_ID: 'x', THETA_VIDEO_SA_SECRET: 'y', THETA_CHARACTERS_API_KEY: 'z' };
    await assert.rejects(run({ command: 'theta.deployments.delete', shard: 's', suffix: 'x' }, { env }), /confirm:true/);
    await assert.rejects(run({ command: 'theta.ai.agent.create', payload: {} }, { env }), /confirm:true/);
    await assert.rejects(run({ command: 'theta.video.create', payload: {} }, { env }), /confirm:true/);
    await assert.rejects(run({ command: 'theta.characters.delete', gameId: 'g', characterId: 'c' }, { env }), /confirm:true/);
    const preview = await run({ command: 'theta.deployments.delete', shard: 's', suffix: 'x' }, { env: { ...env, THETA_DRY_RUN: '1' } });
    assert.equal(preview.dryRun, true);
  });
});

test('0.1.30: theta() facade exposes no mutation helpers', async () => {
  const { theta } = await import('../../dist/index.js');
  const t = theta();
  for (const m of ['create', 'start', 'stop', 'delete', 'startByBaseId', 'validateDisposable', 'chatbotCreate', 'chatbotUpdate', 'chatbotDocumentCreate']) assert.equal(t.deploy[m], undefined, m);
  for (const m of ['uploadCreate', 'videoCreate', 'streamCreate', 'ingestorSelect']) assert.equal(t.video[m], undefined, m);
  assert.equal(typeof t.deploy.list, 'function');
});

test('0.1.30: video inference requires confirm; image/chat inference does not', async () => {
  await mockFetch(() => { throw new Error('unexpected network'); }, async () => {
    for (const command of ['infer', 'theta.ondemand.infer']) {
      await assert.rejects(run({ command, service: 'seedance_2_5', input: { prompt: 'p', duration: 4 }, payload: { input: { prompt: 'p' } } }, { env }), /high-cost.*confirm:true/);
    }
  });
  await mockFetch(async (url, init) => {
    assert.equal(JSON.parse(init.body).input.prompt, 'p');
    return new Response(JSON.stringify({ body: { infer_requests: [{ id: 'r', state: 'created' }] } }));
  }, async () => {
    await run({ command: 'infer', service: 'seedance_2_5', input: { prompt: 'p', duration: 4 }, confirm: true }, { env });
    await run({ command: 'infer', service: 'stable_diffusion_xl_turbo', input: { prompt: 'p' } }, { env });
  });
});

test('0.1.32: theta() cannot infer/chat/upload and module-level video gate holds on every path', async () => {
  const { theta } = await import('../../dist/index.js');
  const t = theta();
  for (const m of ['infer', 'chat', 'inputPresignedUrls']) assert.equal(t.ondemand[m], undefined, m);
  assert.equal(t.inference.chat, undefined);
  assert.equal(typeof t.ondemand.listLiveServices, 'function');
  const { ondemand } = await import('../../build/commands/ondemand.js');
  await mockFetch(() => { throw new Error('unexpected network'); }, async () => {
    assert.throws(() => ondemand.infer({ dryRun: false }, 'seedance_2_5', { input: { prompt: 'p' } }), /high-cost.*confirm:true/);
  });
});

test('self-reference import of internals is not exported', async () => {
  await assert.rejects(import('theta-edgecloud-skill/dist/commands/ondemand.js'), /ERR_PACKAGE_PATH_NOT_EXPORTED|not exported/i);
  const pkg = await import('theta-edgecloud-skill');
  assert.equal(typeof pkg.executeThetaRuntimeCommand, 'function');
});
