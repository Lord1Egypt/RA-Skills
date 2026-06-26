import { createHash } from 'node:crypto';
import { emitTelemetry } from './telemetry.mjs';

const DEFAULT_BASE_URL = 'https://gateway-api.binaryworks.app';

function normalizeBaseUrl(baseUrlRaw) {
  const candidate = (baseUrlRaw ?? DEFAULT_BASE_URL).trim();
  if (!candidate) {
    return DEFAULT_BASE_URL;
  }
  try {
    const parsed = new URL(candidate);
    if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
      throw new Error('invalid protocol');
    }
    return parsed.toString().replace(/\/+$/, '');
  } catch {
    throw new Error(`invalid base_url: ${baseUrlRaw}`);
  }
}

function normalizeIdentifier(raw, fallback) {
  const value = (raw ?? '').trim().toLowerCase();
  return value || fallback;
}

function buildStableLocalId(prefix) {
  const digest = sha256Hex(`${prefix}:${process.cwd()}`).slice(0, 24);
  return `${prefix}_local_${digest}`;
}

function normalizeOwnerUidHint(raw) {
  return normalizeIdentifier(raw, buildStableLocalId('owner'));
}

function normalizeAgentUid(raw) {
  return normalizeIdentifier(raw, buildStableLocalId('agent'));
}

function sha256Hex(input) {
  return createHash('sha256').update(input).digest('hex');
}

async function postJson(baseUrl, path, body, headers = {}) {
  const response = await fetch(`${baseUrl}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...headers
    },
    body: JSON.stringify(body)
  });

  const text = await response.text();
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    parsed = null;
  }

  return {
    ok: response.ok,
    status: response.status,
    text,
    parsed
  };
}

function extractApiError(parsed, status, fallbackText) {
  if (parsed && typeof parsed === 'object') {
    const requestId = typeof parsed.request_id === 'string' ? parsed.request_id : null;
    const error = parsed.error;
    if (error && typeof error === 'object') {
      const code = typeof error.code === 'string' ? error.code : `HTTP_${status}`;
      const message = typeof error.message === 'string' ? error.message : fallbackText;
      return { code, message, requestId, status };
    }
  }
  return {
    code: `HTTP_${status}`,
    message: fallbackText,
    requestId: null,
    status
  };
}

function formatApiError(prefix, error) {
  const requestSuffix = error.requestId ? ` request_id=${error.requestId}` : '';
  return `${prefix}: ${error.code} ${error.message} (status=${error.status})${requestSuffix}`;
}

async function issueInstallCode(baseUrl, ownerUidHint) {
  const response = await postJson(baseUrl, '/agent/install-code/issue', {
    channel: 'local',
    owner_uid_hint: ownerUidHint
  });

  if (!response.ok || !response.parsed || typeof response.parsed !== 'object') {
    const error = extractApiError(response.parsed, response.status, response.text);
    throw new Error(formatApiError('install-code issue failed', error));
  }

  const data = response.parsed.data;
  if (!data || typeof data !== 'object') {
    const requestId = typeof response.parsed.request_id === 'string' ? response.parsed.request_id : '';
    throw new Error(
      `install-code issue failed: missing data${requestId ? ` request_id=${requestId}` : ''}`
    );
  }

  const installCode = typeof data.install_code === 'string' ? data.install_code.trim() : '';
  const ownerUid = typeof data.owner_uid === 'string' ? data.owner_uid.trim() : '';
  if (!installCode || !ownerUid) {
    throw new Error('install-code issue failed: install_code/owner_uid missing');
  }

  return {
    installCode,
    ownerUid
  };
}

async function bootstrapAgent(baseUrl, installCode, agentUid) {
  const response = await postJson(baseUrl, '/agent/bootstrap', {
    agent_uid: agentUid,
    install_code: installCode
  });

  if (!response.ok || !response.parsed || typeof response.parsed !== 'object') {
    const error = extractApiError(response.parsed, response.status, response.text);
    throw new Error(formatApiError('bootstrap failed', error));
  }

  const data = response.parsed.data;
  if (!data || typeof data !== 'object') {
    const requestId = typeof response.parsed.request_id === 'string' ? response.parsed.request_id : '';
    throw new Error(`bootstrap failed: missing data${requestId ? ` request_id=${requestId}` : ''}`);
  }

  const apiKey = typeof data.api_key === 'string' ? data.api_key.trim() : '';
  if (!apiKey) {
    throw new Error('bootstrap failed: missing api_key');
  }

  const ownerUid = typeof data.owner_uid === 'string' ? data.owner_uid.trim() : '';
  return {
    apiKey,
    ownerUid
  };
}

async function fetchBootstrapApiKey(baseUrl, ownerUidHint, agentUid) {
  const issued = await issueInstallCode(baseUrl, ownerUidHint);
  const bootstrapped = await bootstrapAgent(baseUrl, issued.installCode, agentUid);
  return {
    apiKey: bootstrapped.apiKey,
    ownerUidHint: bootstrapped.ownerUid || issued.ownerUid
  };
}

export async function resolveRuntimeAuth(params) {
  const baseUrl = normalizeBaseUrl(params.baseUrl);
  const agentUid = normalizeAgentUid(params.agentUid);
  const ownerUidHint = normalizeOwnerUidHint(params.ownerUidHint);

  const explicitApiKey = (params.explicitApiKey ?? '').trim();
  if (explicitApiKey) {
    const auth = {
      apiKey: explicitApiKey,
      baseUrl,
      agentUid,
      ownerUidHint,
      source: 'explicit'
    };
    void emitTelemetry({
      baseUrl,
      apiKey: explicitApiKey,
      agentUid,
      ownerUidHint,
      eventName: 'agent.auth.explicit',
      status: 'ok'
    });
    return auth;
  }

  try {
    const bootstrapped = await fetchBootstrapApiKey(baseUrl, ownerUidHint, agentUid);
    const auth = {
      apiKey: bootstrapped.apiKey,
      baseUrl,
      agentUid,
      ownerUidHint: bootstrapped.ownerUidHint,
      source: 'bootstrap'
    };
    void emitTelemetry({
      baseUrl,
      apiKey: bootstrapped.apiKey,
      agentUid,
      ownerUidHint: bootstrapped.ownerUidHint,
      eventName: 'agent.bootstrap.success',
      status: 'ok'
    });
    return auth;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    void emitTelemetry({
      baseUrl,
      apiKey: '',
      agentUid,
      ownerUidHint,
      eventName: 'agent.bootstrap.failed',
      status: 'error',
      properties: { message }
    });
    throw error;
  }
}

export async function refreshRuntimeAuth(params) {
  return await resolveRuntimeAuth({ ...params, forceRefresh: true });
}

export function runtimeHints(auth) {
  return {
    agent_uid: auth.agentUid,
    owner_uid_hint: auth.ownerUidHint,
    auth_source: auth.source,
    base_url: auth.baseUrl
  };
}

export const RUNTIME_DEFAULT_BASE_URL = DEFAULT_BASE_URL;
