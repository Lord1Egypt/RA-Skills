// Offline: every request is intercepted by a mocked fetch; nothing is sent to the network.
import assert from 'node:assert/strict';
import test from 'node:test';

import {
  ONDEMAND_CHAT_SERVICE_SLUGS,
  ONDEMAND_SERVICE_CATALOG,
  isOnDemandChatService,
  listOnDemandServices
} from '../../build/commands/ondemandCatalog.js';
import { buildOnDemandChatPayloadForTest, categorizeOnDemandService, ondemand } from '../../build/commands/ondemand.js';
import { onDemandApiClient } from '../../build/clients/ondemandApi.js';

const cfg = {
  dryRun: false,
  onDemandApiToken: 'test-token',
  httpTimeoutMs: 5000,
  httpMaxRetries: 0,
  httpRetryBackoffMs: 25
};

async function withMockFetch(mock, fn) {
  const original = globalThis.fetch;
  globalThis.fetch = mock;
  try {
    await fn();
  } finally {
    globalThis.fetch = original;
  }
}

test('on-demand catalog includes Qwen3 as a chat service', () => {
  assert.equal(ONDEMAND_SERVICE_CATALOG.qwen3.requiredInputFields.includes('messages'), true);
  assert.equal(ONDEMAND_SERVICE_CATALOG.qwen3.inputSchemaKind, 'chat_messages');
  assert.equal(isOnDemandChatService('qwen3'), true);
  assert.equal(isOnDemandChatService('flux'), false);
  assert.equal(listOnDemandServices().some((service) => service.slug === 'qwen3'), true);
});

test('GLM-5.2 is allowlisted, cataloged, and categorized as text', () => {
  assert.equal(isOnDemandChatService('glm_5_2'), true);
  assert.equal(ONDEMAND_CHAT_SERVICE_SLUGS.includes('glm_5_2'), true);
  assert.equal(ONDEMAND_SERVICE_CATALOG.glm_5_2.defaultPrediction, 'completions');
  assert.equal(ONDEMAND_SERVICE_CATALOG.glm_5_2.maxTokensDefault, 5000);
  assert.equal(ONDEMAND_SERVICE_CATALOG.glm_5_2.contextWindow, 1000000);
  assert.equal(ONDEMAND_SERVICE_CATALOG.glm_5_2.license, 'MIT');
  assert.equal(categorizeOnDemandService({ alias: 'glm_5_2', name: 'GLM 5.2' }), 'text');
  assert.equal(ondemand.listServices({ category: 'text' }).some((service) => service.slug === 'glm_5_2'), true);
});

test('GLM-5.2 dry-run chat preserves enable_thinking', () => {
  const result = ondemand.chat(
    { ...cfg, dryRun: true },
    'glm_5_2',
    [{ role: 'user', content: 'Reply with OK.' }],
    {
      maxTokens: 5000,
      stream: true,
      variant: 'default',
      enableThinking: true
    }
  );

  assert.equal(result.service, 'glm_5_2');
  assert.equal(result.payload.input.enable_thinking, true);
  assert.equal(result.payload.input.max_tokens, 5000);
  assert.equal(result.payload.variant, 'default');
  assert.equal(result.requestOptions.prediction, 'completions');
});

test('unsupported-service errors derive the known service list from the allowlist', () => {
  assert.throws(
    () => ondemand.chat({ ...cfg, dryRun: true }, 'not_a_service', [{ role: 'user', content: 'Hi' }]),
    /Known chat services: glm_5_2, qwen3/
  );
});

test('chat payload builder defaults to Qwen3-compatible non-streaming completions shape', () => {
  const { payload, requestOptions } = buildOnDemandChatPayloadForTest(
    [{ role: 'user', content: 'hello' }],
    { wait: 20 }
  );

  assert.deepEqual(payload.input.messages, [{ role: 'user', content: 'hello' }]);
  assert.equal(payload.input.stream, false);
  assert.equal(payload.input.max_tokens, 500);
  assert.equal(payload.input.temperature, 0.5);
  assert.equal(payload.input.top_p, 0.7);
  assert.equal(requestOptions.wait, 20);
  assert.equal(requestOptions.prediction, 'completions');
});

test('createInferRequest wraps bare chat payload and injects stream false', async () => {
  let captured;

  await withMockFetch(async (url, options) => {
    captured = { url: String(url), options };
    return new Response(JSON.stringify({ body: { infer_requests: [{ id: 'infr_test', state: 'success' }] } }), {
      status: 200,
      headers: { 'content-type': 'application/json' }
    });
  }, async () => {
    await onDemandApiClient.createInferRequest(
      cfg,
      'qwen3',
      { messages: [{ role: 'user', content: 'hi' }] },
      { wait: 20, prediction: 'completions' }
    );
  });

  assert.equal(captured.url, 'https://ondemand.thetaedgecloud.com/infer_request/qwen3?wait=20&prediction=completions');
  assert.equal(captured.options.headers.Authorization, 'Bearer test-token');
  assert.deepEqual(JSON.parse(captured.options.body), {
    input: {
      messages: [{ role: 'user', content: 'hi' }],
      stream: false,
      max_tokens: 500
    },
    prediction: 'completions'
  });
});

test('on-demand API honors THETA_API_BASE_URL-compatible config override', async () => {
  let capturedUrl;

  await withMockFetch(async (url) => {
    capturedUrl = String(url);
    return new Response(JSON.stringify({ body: { infer_requests: [{ id: 'infr_custom', state: 'success' }] } }), {
      status: 200,
      headers: { 'content-type': 'application/json' }
    });
  }, async () => {
    await onDemandApiClient.createInferRequest(
      { ...cfg, onDemandApiBaseUrl: 'https://ondemand.thetaedgecloud.com/' },
      'whisper',
      { audio_filename: 'clip.wav' },
      { wait: 0 }
    );
  });

  assert.equal(capturedUrl, 'https://ondemand.thetaedgecloud.com/infer_request/whisper?wait=0');
});

test('live service listing includes normalized category and input examples', async () => {
  await withMockFetch(async () => {
    return new Response(JSON.stringify({
      body: {
        services: [
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
          },
          {
            alias: 'gpt_oss_120b',
            name: 'GPT OSS 120B',
            state: 'public',
            default_prediction: 'completions',
            predictions: {
              completions: {
                input_vars: {
                  messages: { type: 'chat_array', index: 0 },
                  stream: { type: 'bool', default_value: true }
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
  }, async () => {
    const result = await ondemand.listLiveServices(cfg, { category: 'audio' });
    assert.equal(result.source, 'live');
    assert.equal(result.category, 'audio');
    assert.equal(result.services.length, 1);
    assert.equal(result.services[0].alias, 'whisper');
    assert.equal(result.services[0].category, 'audio');
    assert.deepEqual(result.services[0].inputExample, { audio_filename: '<filename from get_upload_url>' });
  });
});

test('createInferRequest preserves explicit stream and top-level variant', async () => {
  let body;

  await withMockFetch(async (_url, options) => {
    body = JSON.parse(options.body);
    return new Response(JSON.stringify({ body: { infer_requests: [{ id: 'infr_test', state: 'success' }] } }), {
      status: 200,
      headers: { 'content-type': 'application/json' }
    });
  }, async () => {
    await onDemandApiClient.createInferRequest(cfg, 'qwen3', {
      input: {
        messages: [{ role: 'user', content: 'hi' }],
        stream: true
      },
      variant: 'parallax_32b_fp8'
    });
  });

  assert.equal(body.input.stream, true);
  assert.equal(body.variant, 'parallax_32b_fp8');
});

test('createInferRequest parses streaming SSE responses into JSON-shaped output', async () => {
  let capturedBody;

  await withMockFetch(async (_url, options) => {
    capturedBody = JSON.parse(options.body);
    const sse = [
      'data: {"id":"chatcmpl_test","model":"default","choices":[{"delta":{"content":"theta-"},"finish_reason":null}],"usage":{"prompt_tokens":4,"completion_tokens":1,"total_tokens":5}}',
      '',
      'data: {"id":"chatcmpl_test","model":"default","choices":[{"delta":{"content":"qwen3-ok"},"finish_reason":"stop"}],"usage":{"prompt_tokens":4,"completion_tokens":2,"total_tokens":6}}',
      '',
      'data: [DONE]',
      ''
    ].join('\n');
    return new Response(sse, {
      status: 200,
      headers: { 'content-type': 'text/event-stream' }
    });
  }, async () => {
    const result = await onDemandApiClient.createInferRequest(cfg, 'qwen3', {
      input: {
        messages: [{ role: 'user', content: 'hi' }],
        stream: true
      },
      variant: 'parallax_32b_fp8'
    });

    const request = result.body.infer_requests[0];
    assert.equal(capturedBody.input.stream, true);
    assert.equal(request.state, 'success');
    assert.equal(request.output.message, 'theta-qwen3-ok');
    assert.equal(request.model, 'default');
    assert.equal(request.finish_reason, 'stop');
  });
});

test('Qwen3 chat defaults to streaming Parallax-safe wait window', async () => {
  let captured;

  await withMockFetch(async (url, options) => {
    captured = { url: String(url), options };
    const sse = [
      'data: {"id":"chatcmpl_qwen","model":"default","choices":[{"delta":{"content":"4"},"finish_reason":"stop"}],"usage":{"prompt_tokens":4,"completion_tokens":1,"total_tokens":5}}',
      '',
      'data: [DONE]',
      ''
    ].join('\n');
    return new Response(sse, {
      status: 200,
      headers: { 'content-type': 'text/event-stream' }
    });
  }, async () => {
    const result = await ondemand.chat(
      cfg,
      'qwen3',
      [{ role: 'user', content: 'What is 2 + 2? Reply with only the number.' }],
      { variant: 'parallax_32b_fp8' }
    );

    const body = JSON.parse(captured.options.body);
    const request = result.body.infer_requests[0];

    assert.equal(captured.url, 'https://ondemand.thetaedgecloud.com/infer_request/qwen3?wait=60&prediction=completions');
    assert.equal(body.input.stream, true);
    assert.equal(body.variant, 'parallax_32b_fp8');
    assert.equal(request.output.message, '4');
  });
});

test('streaming chat timeout fails once instead of retrying into a multi-minute hang', async () => {
  let attempts = 0;
  const timeoutError = new Error('The operation was aborted due to timeout');
  timeoutError.name = 'TimeoutError';

  await withMockFetch(async () => {
    attempts += 1;
    throw timeoutError;
  }, async () => {
    await assert.rejects(
      () => ondemand.chat(
        { ...cfg, httpMaxRetries: 2 },
        'qwen3',
        [{ role: 'user', content: 'What is 2 + 2? Reply with only the number.' }],
        { variant: 'parallax_32b_fp8' }
      ),
      (error) => {
        assert.equal(error.code, 'HTTP_408');
        return /timeout|aborted/i.test(error.message);
      }
    );
  });

  assert.equal(attempts, 1);
});

test('GPT OSS chat uses direct chat/completions endpoint and normalizes OpenAI JSON response', async () => {
  let captured;

  await withMockFetch(async (url, options) => {
    captured = { url: String(url), options };
    return new Response(JSON.stringify({
      id: 'chatcmpl_test',
      object: 'chat.completion',
      model: 'gpt_oss_120b',
      choices: [
        {
          index: 0,
          message: { role: 'assistant', content: '4', reasoning: 'Need answer only.' },
          finish_reason: 'stop'
        }
      ],
      usage: {
        prompt_tokens: 91,
        completion_tokens: 44,
        total_tokens: 135
      }
    }), {
      status: 200,
      headers: { 'content-type': 'application/json' }
    });
  }, async () => {
    const result = await ondemand.chat(
      cfg,
      'gpt_oss_120b',
      [{ role: 'user', content: 'What is 2 + 2? Reply with only the number.' }],
      { stream: false, confirm: true }
    );

    const body = JSON.parse(captured.options.body);
    const request = result.body.infer_requests[0];

    assert.equal(captured.url, 'https://ondemand.thetaedgecloud.com/infer_request/chat/completions');
    assert.equal(captured.options.headers.Authorization, 'Bearer test-token');
    assert.equal(body.model, 'gpt_oss_120b');
    assert.equal(body.stream, false);
    assert.equal(body.max_tokens, 1800);
    assert.equal(body.reasoning_effort, 'low');
    assert.equal(request.id, 'chatcmpl_test');
    assert.equal(request.state, 'success');
    assert.equal(request.output.message, '4');
    assert.equal(request.model, 'gpt_oss_120b');
    assert.deepEqual(request.metadata, {
      reasoning: 'Need answer only.',
      reasoning_length: 17,
      content_length: 1
    });
    assert.deepEqual(request.usage, {
      prompt_tokens: 91,
      completion_tokens: 44,
      total_tokens: 135
    });
  });
});

test('GPT OSS chat preserves explicit max token and reasoning-effort overrides', async () => {
  let body;

  await withMockFetch(async (_url, options) => {
    body = JSON.parse(options.body);
    return new Response(JSON.stringify({
      id: 'chatcmpl_override',
      choices: [
        {
          message: { role: 'assistant', content: 'ok' },
          finish_reason: 'stop'
        }
      ]
    }), {
      status: 200,
      headers: { 'content-type': 'application/json' }
    });
  }, async () => {
    await ondemand.chat(
      cfg,
      'gpt_oss_120b',
      [{ role: 'user', content: 'Reply ok.' }],
      { maxTokens: 512, reasoningEffort: 'medium', stream: false, confirm: true }
    );
  });

  assert.equal(body.max_tokens, 512);
  assert.equal(body.reasoning_effort, 'medium');
});

test('GPT OSS chat/completions parses streaming SSE deltas', async () => {
  await withMockFetch(async (url, options) => {
    assert.equal(String(url), 'https://ondemand.thetaedgecloud.com/infer_request/chat/completions');
    assert.equal(JSON.parse(options.body).stream, true);
    const sse = [
      'data: {"id":"chatcmpl_stream","model":"openai/gpt-oss-120b","choices":[{"delta":{"reasoning":"Compute briefly. "},"finish_reason":null}],"usage":{"prompt_tokens":91,"completion_tokens":1,"total_tokens":92}}',
      '',
      'data: {"id":"chatcmpl_stream","model":"openai/gpt-oss-120b","choices":[{"delta":{"content":"4"},"finish_reason":null}],"usage":{"prompt_tokens":91,"completion_tokens":2,"total_tokens":93}}',
      '',
      'data: {"id":"chatcmpl_stream","model":"openai/gpt-oss-120b","choices":[{"delta":{"reasoning":"Done."},"finish_reason":"stop"}],"usage":{"prompt_tokens":91,"completion_tokens":37,"total_tokens":128}}',
      '',
      'data: [DONE]',
      ''
    ].join('\n');
    return new Response(sse, {
      status: 200,
      headers: { 'content-type': 'text/event-stream' }
    });
  }, async () => {
    const result = await ondemand.chat(
      cfg,
      'gpt_oss_120b',
      [{ role: 'user', content: 'What is 2 + 2? Reply with only the number.' }],
      { stream: true, confirm: true }
    );

    const request = result.body.infer_requests[0];
    assert.equal(request.id, 'chatcmpl_stream');
    assert.equal(request.output.message, '4');
    assert.equal(request.model, 'openai/gpt-oss-120b');
    assert.equal(request.finish_reason, 'stop');
    assert.deepEqual(request.metadata, {
      reasoning: 'Compute briefly. Done.',
      reasoning_length: 22,
      content_length: 1
    });
  });
});

test('on-demand client encodes path segments and rejects blanks', async () => {
  let capturedUrl;

  await withMockFetch(async (url) => {
    capturedUrl = String(url);
    return new Response(JSON.stringify({ body: { infer_requests: [{ id: 'infr_test', state: 'success' }] } }), {
      status: 200,
      headers: { 'content-type': 'application/json' }
    });
  }, async () => {
    await onDemandApiClient.getInferRequest(cfg, 'request/with space');
  });

  assert.equal(capturedUrl, 'https://ondemand.thetaedgecloud.com/infer_request/request%2Fwith%20space');
  assert.throws(
    () => onDemandApiClient.createInferRequest(cfg, '   ', { input: { prompt: 'x' } }),
    /service must be a non-empty string/
  );
});
