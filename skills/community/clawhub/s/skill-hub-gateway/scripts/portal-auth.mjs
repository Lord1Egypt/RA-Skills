#!/usr/bin/env node
// release-gate: allow-env-network

import { pathToFileURL } from 'node:url';
import {
  resolveRuntimeAuth,
  refreshRuntimeAuth,
  runtimeHints,
  RUNTIME_DEFAULT_BASE_URL
} from './runtime-auth.mjs';

export async function resolvePortalUserAuth(params = {}, options = {}) {
  const fetchImpl = options.fetchImpl ?? fetch;
  const emitStderr = options.emitStderr ?? defaultEmitStderr;

  let runtimeAuth;
  try {
    runtimeAuth = await resolveRuntimeAuth({
      explicitApiKey: params.explicitApiKey,
      baseUrl: params.baseUrl,
      agentUid: params.agentUid,
      ownerUidHint: params.ownerUidHint
    });
  } catch (error) {
    throw createPortalAuthError(500, 'AUTH_BOOTSTRAP_FAILED', asMessage(error));
  }

  let bridged = await bridgeAuth(runtimeAuth, fetchImpl);
  if (!bridged.ok && bridged.status === 401 && runtimeAuth.source !== 'explicit') {
    runtimeAuth = await refreshRuntimeAuth({
      explicitApiKey: '',
      baseUrl: runtimeAuth.baseUrl,
      agentUid: runtimeAuth.agentUid,
      ownerUidHint: runtimeAuth.ownerUidHint
    });
    bridged = await bridgeAuth(runtimeAuth, fetchImpl);
  }

  if (!bridged.ok) {
    const event = {
      event: 'portal_auth_failed',
      status: bridged.status,
      code: bridged.error.code,
      message: bridged.error.message,
      request_id: bridged.error.requestId,
      step: bridged.error.step
    };
    emitStderr(event);
    throw createPortalAuthError(
      bridged.status,
      bridged.error.code,
      bridged.error.message,
      bridged.error.requestId,
      { step: bridged.error.step }
    );
  }

  const hints = runtimeHints(runtimeAuth);
  emitStderr({
    event: 'portal_auth_ready',
    ...hints,
    user_id: bridged.userId
  });

  return {
    userToken: bridged.userToken,
    userId: bridged.userId,
    agentUid: runtimeAuth.agentUid,
    apiKey: runtimeAuth.apiKey,
    ownerUidHint: runtimeAuth.ownerUidHint,
    baseUrl: runtimeAuth.baseUrl,
    source: runtimeAuth.source
  };
}

async function bridgeAuth(runtimeAuth, fetchImpl) {
  const meResponse = await requestAgentMe(runtimeAuth, fetchImpl);
  if (!meResponse.ok) {
    return {
      ok: false,
      status: meResponse.status,
      error: {
        ...meResponse.error,
        step: 'agent_me'
      }
    };
  }

  const loginResponse = await requestApiKeyLogin(runtimeAuth, meResponse.userId, fetchImpl);
  if (!loginResponse.ok) {
    return {
      ok: false,
      status: loginResponse.status,
      error: {
        ...loginResponse.error,
        step: 'api_key_login'
      }
    };
  }

  return {
    ok: true,
    userToken: loginResponse.userToken,
    userId: meResponse.userId
  };
}

async function requestAgentMe(runtimeAuth, fetchImpl) {
  const response = await fetchImpl(`${runtimeAuth.baseUrl}/agent/me`, {
    method: 'GET',
    headers: {
      'X-API-Key': runtimeAuth.apiKey,
      'x-agent-uid': runtimeAuth.agentUid
    }
  });

  const body = await response.text();
  const parsed = parseJson(body);
  if (!response.ok) {
    return {
      ok: false,
      status: response.status,
      error: parseApiError(parsed, body, response.status)
    };
  }

  const userId = typeof parsed?.data?.user_id === 'string' ? parsed.data.user_id.trim() : '';
  if (!userId) {
    return {
      ok: false,
      status: 502,
      error: {
        code: 'UPSTREAM_BAD_RESPONSE',
        message: 'agent/me returned empty user_id',
        requestId: typeof parsed?.request_id === 'string' ? parsed.request_id : null
      }
    };
  }

  return {
    ok: true,
    userId
  };
}

async function requestApiKeyLogin(runtimeAuth, userId, fetchImpl) {
  const response = await fetchImpl(`${runtimeAuth.baseUrl}/user/api-key-login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId,
      api_key: runtimeAuth.apiKey
    })
  });

  const body = await response.text();
  const parsed = parseJson(body);
  if (!response.ok) {
    return {
      ok: false,
      status: response.status,
      error: parseApiError(parsed, body, response.status)
    };
  }

  const userToken = typeof parsed?.data?.token === 'string' ? parsed.data.token.trim() : '';
  if (!userToken) {
    return {
      ok: false,
      status: 502,
      error: {
        code: 'UPSTREAM_BAD_RESPONSE',
        message: 'user/api-key-login returned empty token',
        requestId: typeof parsed?.request_id === 'string' ? parsed.request_id : null
      }
    };
  }

  return {
    ok: true,
    userToken
  };
}

function parseJson(body) {
  try {
    const parsed = JSON.parse(body);
    return parsed && typeof parsed === 'object' ? parsed : null;
  } catch {
    return null;
  }
}

function parseApiError(parsed, body, status) {
  const requestId = typeof parsed?.request_id === 'string' ? parsed.request_id : null;
  const error = parsed?.error;
  if (error && typeof error === 'object') {
    return {
      code: typeof error.code === 'string' ? error.code : `HTTP_${status}`,
      message: typeof error.message === 'string' ? error.message : body,
      requestId
    };
  }

  return {
    code: `HTTP_${status}`,
    message: body,
    requestId
  };
}

function createPortalAuthError(status, code, message, requestId = null, details = undefined) {
  const error = new Error(message);
  error.status = status;
  error.code = code;
  error.requestId = requestId;
  error.details = details;
  return error;
}

function asMessage(error) {
  return error instanceof Error ? error.message : String(error);
}

function defaultEmitStderr(event) {
  process.stderr.write(`${JSON.stringify(event)}\n`);
}

function isHttpBaseUrl(value) {
  try {
    const parsed = new URL(value);
    return parsed.protocol === 'http:' || parsed.protocol === 'https:';
  } catch {
    return false;
  }
}

function parseCliArgs(args) {
  if (args.length === 0) {
    return {
      explicitApiKey: '',
      baseUrl: RUNTIME_DEFAULT_BASE_URL,
      agentUid: '',
      ownerUidHint: ''
    };
  }

  const first = args[0] ?? '';
  const firstLooksLikeBaseUrl = isHttpBaseUrl(first);

  if (firstLooksLikeBaseUrl) {
    return {
      explicitApiKey: '',
      baseUrl: first,
      agentUid: args[1] ?? '',
      ownerUidHint: args[2] ?? ''
    };
  }

  return {
    explicitApiKey: first,
    baseUrl: args[1] ?? RUNTIME_DEFAULT_BASE_URL,
    agentUid: args[2] ?? '',
    ownerUidHint: args[3] ?? ''
  };
}

async function main() {
  const parsed = parseCliArgs(process.argv.slice(2));
  try {
    const auth = await resolvePortalUserAuth(parsed);
    console.log(
      JSON.stringify({
        user_token: auth.userToken,
        user_id: auth.userId,
        agent_uid: auth.agentUid,
        base_url: auth.baseUrl,
        owner_uid_hint: auth.ownerUidHint,
        source: auth.source
      })
    );
  } catch (error) {
    const status = Number.isFinite(error?.status) ? error.status : 500;
    const code = typeof error?.code === 'string' ? error.code : 'SYSTEM_INTERNAL_ERROR';
    const message = asMessage(error);
    const requestId = typeof error?.requestId === 'string' ? error.requestId : null;
    process.stderr.write(
      `${JSON.stringify({
        event: 'portal_auth_failed',
        status,
        code,
        message,
        request_id: requestId
      })}\n`
    );
    process.exit(1);
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  await main();
}
