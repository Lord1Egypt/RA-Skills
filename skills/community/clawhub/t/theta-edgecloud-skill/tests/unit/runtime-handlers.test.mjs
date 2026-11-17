// Offline: every request is intercepted by a mocked fetch or dry-run; nothing is sent to the network.
import assert from 'node:assert/strict';
import test from 'node:test';

import {
  executeThetaRuntimeCommand,
  listThetaRuntimeCommands,
  thetaRuntimeCommandSchemas
} from '../../dist/index.js';

test('runtime command registry exposes expected theta commands and schemas', () => {
  const commands = listThetaRuntimeCommands();
  assert.equal(commands.includes('theta.ondemand.infer'), true);
  assert.equal(commands.includes('theta.ondemand.chat'), true);
  assert.equal(commands.includes('infer'), true);
  assert.equal(commands.includes('list_services'), true);
  assert.equal(commands.includes('get_request_status'), true);
  assert.equal(commands.includes('get_upload_url'), true);
  assert.equal(commands.includes('theta.ai.agent.create'), true);
  assert.equal(commands.includes('theta.ai.agent.document.create'), true);
  assert.equal(commands.includes('theta.deployments.routeProbe'), true);
  assert.equal(commands.includes('theta.deployments.validateDisposable'), true);
  assert.equal(commands.includes('theta.billing.balanceSnapshot'), true);
  assert.equal(commands.includes('theta.inference.ready'), true);
  assert.equal(commands.includes('theta.ondemand.uploadInput'), false);
  assert.equal(commands.includes('theta.health'), true);

  const inferSchema = thetaRuntimeCommandSchemas['theta.ondemand.infer'];
  assert.equal(inferSchema.command, 'theta.ondemand.infer');
  assert.deepEqual(inferSchema.required, ['service', 'payload']);

  const chatSchema = thetaRuntimeCommandSchemas['theta.ondemand.chat'];
  assert.equal(chatSchema.command, 'theta.ondemand.chat');
  assert.deepEqual(chatSchema.required, ['messages']);

  const agentUpdateSchema = thetaRuntimeCommandSchemas['theta.ai.agent.update'];
  assert.deepEqual(agentUpdateSchema.required, ['chatbotId', 'payload']);
});

test('runtime handler validates required fields', async () => {
  await assert.rejects(
    () => executeThetaRuntimeCommand({ command: 'theta.ondemand.infer', service: 'flux' }, { env: { THETA_DRY_RUN: '1' } }),
    /Missing required field: payload/
  );
});

test('runtime handler routes dry-run ondemand infer without token', async () => {
  const result = await executeThetaRuntimeCommand(
    {
      command: 'theta.ondemand.infer',
      service: 'flux',
      payload: { prompt: 'runtime-test' }
    },
    {
      env: { THETA_DRY_RUN: '1' }
    }
  );

  assert.equal(result.dryRun, true);
  assert.equal(result.service, 'flux');
  assert.equal(result.payload.prompt, 'runtime-test');
});

test('runtime handler routes dry-run MCP infer alias without token', async () => {
  const result = await executeThetaRuntimeCommand(
    {
      command: 'infer',
      service: 'flux',
      input: { prompt: 'mcp-alias-test' },
      wait: 0,
      prediction: 'generate_image'
    },
    {
      env: { THETA_DRY_RUN: '1' }
    }
  );

  assert.equal(result.dryRun, true);
  assert.equal(result.service, 'flux');
  assert.deepEqual(result.payload.input, { prompt: 'mcp-alias-test' });
  assert.equal(result.payload.variant, undefined);
  assert.equal(result.requestOptions.wait, 0);
  assert.equal(result.requestOptions.prediction, 'generate_image');
});

test('runtime handler routes MCP infer alias variant and webhook fields', async () => {
  const result = await executeThetaRuntimeCommand(
    {
      command: 'infer',
      service: 'qwen3',
      input: { messages: [{ role: 'user', content: 'hello' }] },
      variant: 'parallax_32b_fp8',
      webhook: 'https://hooks.invalid/hook'
    },
    {
      env: { THETA_DRY_RUN: '1' }
    }
  );

  assert.equal(result.dryRun, true);
  assert.equal(result.payload.variant, 'parallax_32b_fp8');
  assert.equal(result.payload.webhook, 'https://hooks.invalid/hook');
});

test('runtime handler accepts official MCP get_upload_url input_field argument', async () => {
  const result = await executeThetaRuntimeCommand(
    {
      command: 'get_upload_url',
      service: 'whisper',
      input_field: 'audio_filename'
    },
    {
      env: { THETA_DRY_RUN: '1' }
    }
  );

  assert.equal(result.dryRun, true);
  assert.equal(result.service, 'whisper');
  assert.deepEqual(result.inputFields, ['audio_filename']);
});

test('runtime handler passes category filter and THETA_API_BASE_URL into service listing', async () => {
  const original = globalThis.fetch;
  let capturedUrl;
  globalThis.fetch = async (url) => {
    capturedUrl = String(url);
    return new Response(JSON.stringify({
      body: {
        services: [
          {
            alias: 'stable_diffusion_xl_turbo',
            name: 'Stable Diffusion XL Turbo',
            state: 'public',
            default_prediction: 'predict',
            predictions: {
              predict: {
                input_vars: {
                  prompt: { type: 'string', index: 0 }
                }
              }
            }
          },
          {
            alias: 'whisper',
            name: 'Whisper',
            state: 'public',
            default_prediction: 'stt',
            predictions: {
              stt: {
                input_vars: {
                  audio_filename: { type: 'filename', index: 0 }
                }
              }
            }
          }
        ]
      }
    }), {
      status: 200,
      headers: { 'content-type': 'application/json' }
    });
  };

  try {
    const result = await executeThetaRuntimeCommand(
      {
        command: 'list_services',
        category: 'image'
      },
      {
        env: {
          THETA_API_BASE_URL: 'https://ondemand.thetaedgecloud.com/'
        }
      }
    );

    assert.equal(capturedUrl, 'https://ondemand.thetaedgecloud.com/service/list?expand=template_id');
    assert.equal(result.source, 'live');
    assert.equal(result.category, 'image');
    assert.equal(result.services.length, 1);
    assert.equal(result.services[0].alias, 'stable_diffusion_xl_turbo');
    assert.equal(result.services[0].category, 'image');
  } finally {
    globalThis.fetch = original;
  }
});

test('runtime handler routes dry-run Qwen3 chat without token', async () => {
  const result = await executeThetaRuntimeCommand(
    {
      command: 'theta.ondemand.chat',
      messages: [{ role: 'user', content: 'hello' }],
      wait: 12
    },
    {
      env: { THETA_DRY_RUN: '1' }
    }
  );

  assert.equal(result.dryRun, true);
  assert.equal(result.service, 'qwen3');
  assert.equal(result.payload.input.stream, true);
  assert.equal(result.payload.input.messages[0].content, 'hello');
  assert.equal(result.requestOptions.wait, 12);
  assert.equal(result.requestOptions.prediction, 'completions');
});

test('runtime handler routes allowlisted GLM-5.2 chat with enable_thinking', async () => {
  const result = await executeThetaRuntimeCommand(
    {
      command: 'theta.ondemand.chat',
      service: 'glm_5_2',
      messages: [{ role: 'user', content: 'hello' }],
      max_tokens: 5000,
      stream: true,
      enable_thinking: true
    },
    {
      env: { THETA_DRY_RUN: '1' }
    }
  );

  assert.equal(result.dryRun, true);
  assert.equal(result.service, 'glm_5_2');
  assert.equal(result.payload.input.enable_thinking, true);
  assert.equal(result.payload.input.max_tokens, 5000);
  assert.equal(result.payload.input.stream, true);
  assert.equal(result.requestOptions.prediction, 'completions');
});

test('runtime handler routes dry-run deployment lifecycle and disposable validator', async () => {
  const stopped = await executeThetaRuntimeCommand(
    {
      command: 'theta.deployments.stop',
      shard: 'shard-a',
      suffix: 'suffix-b'
    },
    {
      env: {
        THETA_DRY_RUN: '1',
        THETA_EC_PROJECT_ID: 'prj_test'
      }
    }
  );

  assert.equal(stopped.dryRun, true);
  assert.equal(stopped.action, 'stop');
  assert.equal(stopped.projectId, 'prj_test');

  const disposable = await executeThetaRuntimeCommand(
    {
      command: 'theta.deployments.validateDisposable',
      payload: {
        project_id: 'prj_test',
        deployment_template_id: 'img_test',
        auth_password: 'supersecret-password'
      },
      probe: 'gradio'
    },
    {
      env: {
        THETA_DRY_RUN: '1'
      }
    }
  );

  assert.equal(disposable.dryRun, true);
  assert.equal(disposable.probe, 'gradio');
  assert.equal(disposable.payload.auth_password.includes('supersecret-password'), false);
});

test('runtime handler rejects dedicated inference endpoint overrides', async () => {
  await assert.rejects(
    () => executeThetaRuntimeCommand(
      {
        command: 'theta.inference.models',
        endpoint: 'https://attacker.invalid'
      },
      {
        env: {
          THETA_DRY_RUN: '1',
          THETA_INFERENCE_ENDPOINT: 'https://valid.thetaedgecloud.com'
        }
      }
    ),
    /args\.endpoint override is disabled/
  );
});

test('runtime handler applies dedicated inference auth from runtime env', async () => {
  const original = globalThis.fetch;
  let capturedAuth;
  globalThis.fetch = async (_url, init) => {
    capturedAuth = init?.headers?.Authorization;
    return new Response(JSON.stringify({ data: [{ id: 'model-a' }] }), {
      status: 200,
      headers: { 'content-type': 'application/json' }
    });
  };

  try {
    const result = await executeThetaRuntimeCommand(
      {
        command: 'theta.inference.models'
      },
      {
        env: {
          THETA_INFERENCE_ENDPOINT: 'https://runtime-auth-test.tec-s1.onthetaedgecloud.com',
          THETA_INFERENCE_AUTH_USER: 'runtime-user',
          THETA_INFERENCE_AUTH_PASS: 'runtime-pass'
        }
      }
    );

    assert.deepEqual(result.data, [{ id: 'model-a' }]);
    assert.equal(capturedAuth, `Basic ${Buffer.from('runtime-user:runtime-pass').toString('base64')}`);
  } finally {
    globalThis.fetch = original;
  }
});

test('runtime handler routes dry-run dedicated readiness probe', async () => {
  const result = await executeThetaRuntimeCommand(
    {
      command: 'theta.inference.ready',
      probe: 'gradio',
      timeoutMs: 5000,
      intervalMs: 1000
    },
    {
      env: {
        THETA_DRY_RUN: '1',
        THETA_INFERENCE_ENDPOINT: 'https://example.thetaedgecloud.com'
      }
    }
  );

  assert.equal(result.dryRun, true);
  assert.equal(result.probe, 'gradio');
  assert.equal(result.timeoutMs, 5000);
});

test('runtime handler routes dry-run AI agent create and document create', async () => {
  const agent = await executeThetaRuntimeCommand(
    {
      command: 'theta.ai.agent.create',
      projectId: 'prj_test',
      payload: {
        name: 'Runtime test agent',
        max_tokens: 1000,
        temperature: 0.2,
        system_prompt: 'Answer from the supplied knowledge base.',
        settings: {
          'retriever.type': 'rerank',
          'agent.tools': { web_search: false, text_to_sql: true }
        }
      }
    },
    { env: { THETA_DRY_RUN: '1' } }
  );

  assert.equal(agent.dryRun, true);
  assert.equal(agent.payload.project_id, 'prj_test');
  assert.equal(agent.payload.settings['agent.tools'].text_to_sql, true);

  const document = await executeThetaRuntimeCommand(
    {
      command: 'theta.ai.agent.document.create',
      projectId: 'prj_test',
      chatbotId: 'chatbot_123',
      file: {
        filename: 'runtime-test.txt',
        content: 'fresh knowledge',
        contentType: 'text/plain'
      },
      metadata: {
        query_type: 'text',
        description: 'Runtime test document'
      }
    },
    { env: { THETA_DRY_RUN: '1' } }
  );

  assert.equal(document.dryRun, true);
  assert.equal(document.chatbotId, 'chatbot_123');
  assert.equal(document.file.content, '[redacted]');
  assert.equal(document.metadata.query_type, 'text');
});

test('runtime handler requires token for non-dry-run on-demand chat', async () => {
  const saved = {
    THETA_ONDEMAND_API_TOKEN: process.env.THETA_ONDEMAND_API_TOKEN,
    THETA_ONDEMAND_API_KEY: process.env.THETA_ONDEMAND_API_KEY,
    THETA_API_KEY: process.env.THETA_API_KEY
  };

  delete process.env.THETA_ONDEMAND_API_TOKEN;
  delete process.env.THETA_ONDEMAND_API_KEY;
  delete process.env.THETA_API_KEY;

  try {
    await assert.rejects(
      () => executeThetaRuntimeCommand(
        {
          command: 'theta.ondemand.chat',
          messages: [{ role: 'user', content: 'hello' }]
        },
        { env: {} }
      ),
      /THETA_ONDEMAND_API_TOKEN missing/
    );
  } finally {
    for (const [key, value] of Object.entries(saved)) {
      if (value === undefined) delete process.env[key];
      else process.env[key] = value;
    }
  }
});

test('runtime handler rejects unknown command', async () => {
  await assert.rejects(
    () => executeThetaRuntimeCommand({ command: 'theta.unknown' }, { env: { THETA_DRY_RUN: '1' } }),
    /Unsupported theta runtime command/
  );
});
