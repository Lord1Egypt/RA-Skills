// Offline: every request is intercepted by a mocked fetch or dry-run; nothing is sent to the network.
import test from 'node:test';
import assert from 'node:assert/strict';
import { executeThetaRuntimeCommand as run, listThetaRuntimeCommands } from '../../dist/index.js';

const env = { THETA_ONDEMAND_API_TOKEN: 'test-token', THETA_HTTP_MAX_RETRIES: '0' };
const tool = { type: 'function', function: { name: 'multiply', parameters: { type: 'object', properties: { a: { type: 'integer' }, b: { type: 'integer' } }, required: ['a', 'b'] } } };
async function mockFetch(mock, fn) { const prior = globalThis.fetch; globalThis.fetch = mock; try { await fn(); } finally { globalThis.fetch = prior; } }

for (const service of ['glm_5_3', 'glm_5_3_flash']) test(`${service} direct endpoint preserves tools and continuation`, async () => {
  const call = { id: 'call1', type: 'function', function: { name: 'multiply', arguments: '{"a":17,"b":19}' } };
  await mockFetch(async (url, init) => {
    assert.equal(url, 'https://ondemand.thetaedgecloud.com/infer_request/chat/completions');
    const body = JSON.parse(init.body);
    assert.equal(body.model, service); assert.deepEqual(body.tools, [tool]); assert.equal(body.tool_choice, 'required');
    assert.equal(body.parallel_tool_calls, false); assert.equal(body.messages[1].tool_calls[0].id, 'call1');
    assert.equal(body.messages[2].tool_call_id, 'call1');
    return new Response(JSON.stringify({ model: service, choices: [{ message: { content: null, tool_calls: [call], reasoning_content: 'reason' }, finish_reason: 'tool_calls' }] }));
  }, async () => {
    const r = await run({ command: 'theta.ondemand.chat', service, tools: [tool], tool_choice: 'required', parallel_tool_calls: false,
      messages: [{ role: 'user', content: 'multiply' }, { role: 'assistant', content: null, tool_calls: [call] }, { role: 'tool', content: '323', tool_call_id: 'call1' }] }, { env });
    assert.deepEqual(r.body.infer_requests[0].output.tool_calls, [call]);
    assert.equal(r.body.infer_requests[0].metadata.reasoning, 'reason');
  });
});

test('streaming parallel fragmented tool calls and reasoning_content survive normalization', async () => {
  const chunks = [
    { choices: [{ delta: { reasoning_content: 'thinking', tool_calls: [{ index: 1, id: 'b', function: { name: 'multiply', arguments: '{"a":' } }, { index: 0, id: 'a', function: { name: 'multiply', arguments: '{"a":17,' } }] } }] },
    { choices: [{ delta: { tool_calls: [{ index: 0, function: { arguments: '"b":19}' } }, { index: 1, function: { arguments: '2,"b":3}' } }] }, finish_reason: 'tool_calls' }] }
  ];
  await mockFetch(async () => new Response(chunks.map(c => `data: ${JSON.stringify(c)}\n\n`).join('') + 'data: [DONE]\n\n'), async () => {
    const r = await run({ command: 'theta.ondemand.chat', service: 'glm_5_3', stream: true, messages: [{ role: 'user', content: 'multiply' }] }, { env });
    const item = r.body.infer_requests[0];
    assert.equal(item.metadata.reasoning, 'thinking');
    assert.deepEqual(item.output.tool_calls.map(c => [c.id, JSON.parse(c.function.arguments)]), [['a', {a:17,b:19}], ['b', {a:2,b:3}]]);
  });
});

test('training templates use documented controller route and validate category', async () => {
  await mockFetch(async url => { assert.equal(url, 'https://controller.thetaedgecloud.com/deployment_template/list_standard_templates?category=training'); return new Response('{}'); }, async () => {
    await run({command:'theta.templates.listStandard',category:'training'}, {env:{THETA_EC_API_KEY:'test'}});
    await assert.rejects(run({command:'theta.templates.listStandard',category:'bad'}, {env}), /Invalid template category/);
  });
});

test('new video mutations honor dry-run without networking', async () => {
  await mockFetch(() => {throw new Error('unexpected network');}, async () => {
    for (const command of ['theta.video.uploadCreate','theta.video.create','theta.video.streamCreate','theta.video.ingestorSelect']) {
      assert.ok(listThetaRuntimeCommands().includes(command));
      const r = await run({command,payload:{},body:{},ingestorId:'test'}, {env:{THETA_DRY_RUN:'1'}});
      assert.equal(r.dryRun,true);
    }
  });
});

test('missing tool result correlation is rejected', async () => {
  await assert.rejects(run({command:'theta.ondemand.chat',service:'glm_5_3',messages:[{role:'tool',content:'323'}]}, {env}), /tool_call_id/);
});
