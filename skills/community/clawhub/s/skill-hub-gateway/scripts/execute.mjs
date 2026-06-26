#!/usr/bin/env node

// release-gate: allow-env-network
// Shebang uses /usr/bin/env for portability; runtime calls are limited to the configured gateway origin.
import {
  resolveRuntimeAuth,
  refreshRuntimeAuth,
  runtimeHints,
  RUNTIME_DEFAULT_BASE_URL
} from './runtime-auth.mjs';
import { emitTelemetry, extractRequestContext } from './telemetry.mjs';

const CAPABILITIES = new Set([
  'human_detect',
  'image_tagging',
  'tts_report',
  'embeddings',
  'reranker',
  'asr',
  'tts_low_cost',
  'markdown_convert'
]);

const defaults = {
  apiKey: '',
  capability: 'human_detect',
  inputPayload: '{"image_url":"https://example.com/image.png"}',
  baseUrl: RUNTIME_DEFAULT_BASE_URL,
  agentUid: '',
  ownerUidHint: ''
};

const parsed = parseArgs(process.argv.slice(2));
let input;
try {
  input = JSON.parse(parsed.inputPayload);
} catch {
  console.error('input must be valid JSON');
  process.exit(1);
}

let auth;
try {
  auth = await resolveRuntimeAuth({
    explicitApiKey: parsed.apiKey,
    baseUrl: parsed.baseUrl,
    agentUid: parsed.agentUid,
    ownerUidHint: parsed.ownerUidHint
  });
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`auth bootstrap failed: ${message}`);
  process.exit(1);
}

void emitTelemetry({
  baseUrl: auth.baseUrl,
  apiKey: auth.apiKey,
  agentUid: auth.agentUid,
  ownerUidHint: auth.ownerUidHint,
  eventName: 'agent.execute.start',
  status: 'ok',
  capability: parsed.capability
});

let response = await executeOnce(auth, parsed.capability, input);
if (response.status === 401 && auth.source !== 'explicit') {
  try {
    auth = await refreshRuntimeAuth({
      explicitApiKey: parsed.apiKey,
      baseUrl: parsed.baseUrl,
      agentUid: parsed.agentUid,
      ownerUidHint: parsed.ownerUidHint
    });
    response = await executeOnce(auth, parsed.capability, input);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`auth refresh failed: ${message}`);
    process.exit(1);
  }
}

console.log(response.body);
if (!response.ok) {
  process.exit(1);
}

function parseArgs(args) {
  if (args.length === 0) {
    return { ...defaults };
  }

  const [first] = args;
  const firstLooksLikeCapability = CAPABILITIES.has(first ?? '');
  const firstLooksLikeJson = typeof first === 'string' && first.trim().startsWith('{');

  if (firstLooksLikeCapability || firstLooksLikeJson) {
    return {
      apiKey: '',
      capability: firstLooksLikeCapability ? first : defaults.capability,
      inputPayload: firstLooksLikeCapability ? args[1] ?? defaults.inputPayload : first,
      baseUrl: firstLooksLikeCapability ? args[2] ?? defaults.baseUrl : args[1] ?? defaults.baseUrl,
      agentUid: firstLooksLikeCapability ? args[3] ?? defaults.agentUid : args[2] ?? defaults.agentUid,
      ownerUidHint: firstLooksLikeCapability ? args[4] ?? defaults.ownerUidHint : args[3] ?? defaults.ownerUidHint
    };
  }

  return {
    apiKey: args[0] ?? defaults.apiKey,
    capability: args[1] ?? defaults.capability,
    inputPayload: args[2] ?? defaults.inputPayload,
    baseUrl: args[3] ?? defaults.baseUrl,
    agentUid: args[4] ?? defaults.agentUid,
    ownerUidHint: args[5] ?? defaults.ownerUidHint
  };
}

async function executeOnce(auth, capability, input) {
  const response = await fetch(`${auth.baseUrl}/skill/execute`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': auth.apiKey
    },
    body: JSON.stringify({
      capability,
      input,
      agent_uid: auth.agentUid
    })
  });

  const body = await response.text();
  const error = parseApiError(body, response.status);
  const context = extractRequestContext(body);
  const requestId = context.requestId ?? error.request_id;
  const runId = context.runId;
  if (response.ok) {
    const hints = runtimeHints(auth);
    console.error(
      JSON.stringify({
        event: 'skill_execute_auth',
        ...hints
      })
    );
  } else {
    console.error(
      JSON.stringify({
        event: 'skill_execute_failed',
        status: response.status,
        code: error.code,
        message: error.message,
        request_id: error.request_id
      })
    );
  }
  void emitTelemetry({
    baseUrl: auth.baseUrl,
    apiKey: auth.apiKey,
    agentUid: auth.agentUid,
    ownerUidHint: auth.ownerUidHint,
    eventName: response.ok ? 'agent.execute.success' : 'agent.execute.failed',
    status: response.ok ? 'ok' : 'error',
    capability,
    runId,
    requestId,
    properties: response.ok
      ? {}
      : {
          code: error.code,
          message: error.message
        }
  });

  return {
    ok: response.ok,
    status: response.status,
    body
  };
}

function parseApiError(body, status) {
  try {
    const parsed = JSON.parse(body);
    if (!parsed || typeof parsed !== 'object') {
      throw new Error('invalid');
    }
    const requestId = typeof parsed.request_id === 'string' ? parsed.request_id : null;
    const error = parsed.error;
    if (!error || typeof error !== 'object') {
      return {
        code: `HTTP_${status}`,
        message: body,
        request_id: requestId
      };
    }
    return {
      code: typeof error.code === 'string' ? error.code : `HTTP_${status}`,
      message: typeof error.message === 'string' ? error.message : body,
      request_id: requestId
    };
  } catch {
    return {
      code: `HTTP_${status}`,
      message: body,
      request_id: null
    };
  }
}
