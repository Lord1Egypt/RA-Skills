#!/usr/bin/env node

// release-gate: allow-env-network
// Shebang uses /usr/bin/env for portability; runtime calls are limited to the configured gateway origin.
import {
  resolveRuntimeAuth,
  refreshRuntimeAuth,
  RUNTIME_DEFAULT_BASE_URL
} from './runtime-auth.mjs';
import { emitTelemetry, extractRequestContext } from './telemetry.mjs';

const defaults = {
  apiKey: '',
  payload:
    '{"message":"feedback from skill script","category":"other","severity":"medium","metadata":{"source":"skill_script"}}',
  baseUrl: RUNTIME_DEFAULT_BASE_URL,
  agentUid: '',
  ownerUidHint: ''
};

const parsed = parseArgs(process.argv.slice(2));
let feedbackInput;
try {
  feedbackInput = JSON.parse(parsed.payload);
} catch {
  console.error('payload must be valid JSON');
  process.exit(1);
}

if (!feedbackInput || typeof feedbackInput !== 'object' || Array.isArray(feedbackInput)) {
  console.error('payload must be a JSON object');
  process.exit(1);
}

const message =
  typeof feedbackInput.message === 'string' && feedbackInput.message.trim()
    ? feedbackInput.message.trim()
    : '';
if (!message) {
  console.error('payload.message is required');
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
  eventName: 'agent.feedback.submit.start',
  status: 'ok'
});

let response = await submitFeedback(auth, feedbackInput, message);
if (response.status === 401 && auth.source !== 'explicit') {
  try {
    auth = await refreshRuntimeAuth({
      explicitApiKey: parsed.apiKey,
      baseUrl: parsed.baseUrl,
      agentUid: parsed.agentUid,
      ownerUidHint: parsed.ownerUidHint
    });
    response = await submitFeedback(auth, feedbackInput, message);
  } catch (error) {
    const messageText = error instanceof Error ? error.message : String(error);
    console.error(`auth refresh failed: ${messageText}`);
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
  const firstLooksLikeJson = typeof first === 'string' && first.trim().startsWith('{');
  if (firstLooksLikeJson) {
    return {
      apiKey: '',
      payload: first,
      baseUrl: args[1] ?? defaults.baseUrl,
      agentUid: args[2] ?? defaults.agentUid,
      ownerUidHint: args[3] ?? defaults.ownerUidHint
    };
  }

  return {
    apiKey: args[0] ?? defaults.apiKey,
    payload: args[1] ?? defaults.payload,
    baseUrl: args[2] ?? defaults.baseUrl,
    agentUid: args[3] ?? defaults.agentUid,
    ownerUidHint: args[4] ?? defaults.ownerUidHint
  };
}

async function submitFeedback(auth, feedbackInput, message) {
  const response = await fetch(`${auth.baseUrl}/feedback/submit`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': auth.apiKey
    },
    body: JSON.stringify({
      category: normalizeEnum(feedbackInput.category, ['bug', 'feature', 'ux', 'other'], 'other'),
      severity: normalizeEnum(feedbackInput.severity, ['low', 'medium', 'high'], 'medium'),
      message,
      ...(typeof feedbackInput.contact === 'string' && feedbackInput.contact.trim()
        ? { contact: feedbackInput.contact.trim() }
        : {}),
      ...(typeof feedbackInput.page_path === 'string' && feedbackInput.page_path.trim()
        ? { page_path: feedbackInput.page_path.trim() }
        : {}),
      ...(typeof feedbackInput.run_id === 'string' && feedbackInput.run_id.trim()
        ? { run_id: feedbackInput.run_id.trim() }
        : {}),
      ...(typeof feedbackInput.capability_id === 'string' && feedbackInput.capability_id.trim()
        ? { capability_id: feedbackInput.capability_id.trim() }
        : {}),
      ...(typeof feedbackInput.request_id_hint === 'string' && feedbackInput.request_id_hint.trim()
        ? { request_id_hint: feedbackInput.request_id_hint.trim() }
        : {}),
      metadata: {
        ...(feedbackInput.metadata && typeof feedbackInput.metadata === 'object' && !Array.isArray(feedbackInput.metadata)
          ? feedbackInput.metadata
          : {}),
        agent_uid: auth.agentUid,
        owner_uid_hint: auth.ownerUidHint
      }
    })
  });

  const body = await response.text();
  const error = parseApiError(body, response.status);
  const context = extractRequestContext(body);
  const requestId = context.requestId ?? error.request_id;
  void emitTelemetry({
    baseUrl: auth.baseUrl,
    apiKey: auth.apiKey,
    agentUid: auth.agentUid,
    ownerUidHint: auth.ownerUidHint,
    eventName: response.ok ? 'agent.feedback.submit.success' : 'agent.feedback.submit.failed',
    status: response.ok ? 'ok' : 'error',
    runId: typeof feedbackInput.run_id === 'string' ? feedbackInput.run_id : undefined,
    requestId,
    properties: response.ok
      ? {
          category: normalizeEnum(feedbackInput.category, ['bug', 'feature', 'ux', 'other'], 'other')
        }
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

function normalizeEnum(raw, allowedValues, fallback) {
  if (typeof raw !== 'string') {
    return fallback;
  }
  const normalized = raw.trim().toLowerCase();
  return allowedValues.includes(normalized) ? normalized : fallback;
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

