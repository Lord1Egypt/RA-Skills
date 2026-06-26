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

const argv = process.argv.slice(2);
const hasExplicitApiKey =
  argv.length >= 2 &&
  !(argv[0] ?? '').startsWith('run_') &&
  (argv[1] ?? '').startsWith('run_');
const explicitApiKey = hasExplicitApiKey ? argv[0] ?? '' : '';
const offset = hasExplicitApiKey ? 1 : 0;
const runId = argv[offset];
const baseUrl = (argv[offset + 1] ?? RUNTIME_DEFAULT_BASE_URL).replace(/\/+$/, '');
const agentUid = argv[offset + 2] ?? '';
const ownerUidHint = argv[offset + 3] ?? '';

if (!runId || !runId.startsWith('run_')) {
  console.error('usage: node poll.mjs [api_key] <run_id> [base_url] [agent_uid] [owner_uid_hint]');
  process.exit(1);
}

async function fetchRun(apiKey) {
  return await fetch(`${baseUrl}/skill/runs/${encodeURIComponent(runId)}`, {
    method: 'GET',
    headers: {
      'X-API-Key': apiKey
    }
  });
}

let auth = await resolveRuntimeAuth({
  explicitApiKey,
  baseUrl,
  agentUid,
  ownerUidHint
});

void emitTelemetry({
  baseUrl: auth.baseUrl,
  apiKey: auth.apiKey,
  agentUid: auth.agentUid,
  ownerUidHint: auth.ownerUidHint,
  eventName: 'agent.poll.start',
  status: 'ok',
  runId
});

let response = await fetchRun(auth.apiKey);

if (!response.ok && response.status === 401 && auth.source !== 'explicit') {
  auth = await refreshRuntimeAuth({
    explicitApiKey: '',
    baseUrl,
    agentUid: auth.agentUid ?? agentUid,
    ownerUidHint: auth.ownerUidHint ?? ownerUidHint
  });
  response = await fetchRun(auth.apiKey);
}

const body = await response.text();
const error = parseApiError(body, response.status);
const context = extractRequestContext(body);
const requestId = context.requestId ?? error.request_id;
console.log(body);
if (response.ok) {
  console.error(
    JSON.stringify({
      event: 'skill_poll_auth',
      ...runtimeHints(auth)
    })
  );
} else {
  console.error(
    JSON.stringify({
      event: 'skill_poll_failed',
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
  eventName: response.ok ? 'agent.poll.terminal' : 'agent.poll.failed',
  status: response.ok ? 'ok' : 'error',
  runId,
  requestId,
  properties: response.ok
    ? {
        run_status: context.status
      }
    : {
        code: error.code,
        message: error.message
      }
});

if (!response.ok) {
  process.exit(1);
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
