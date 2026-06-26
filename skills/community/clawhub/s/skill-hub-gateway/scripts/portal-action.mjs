#!/usr/bin/env node

import { pathToFileURL } from 'node:url';
import { RUNTIME_DEFAULT_BASE_URL } from './runtime-auth.mjs';
import { resolvePortalUserAuth } from './portal-auth.mjs';
import { DEFAULT_SITE_BASE_URL, normalizeExecutePayload, resolveTrustedSiteBaseUrl } from './attachment-normalize.mjs';

const ACTIONS = {
  'portal.me': { method: 'GET' },
  'portal.balance': { method: 'GET' },
  'portal.ledger.query': { method: 'GET' },
  'portal.usage.query': { method: 'GET' },
  'portal.skill.execute': { method: 'POST' },
  'portal.skill.poll': { method: 'GET' },
  'portal.skill.presentation': { method: 'GET' },
  'portal.voucher.redeem': { method: 'POST', write: true },
  'portal.recharge.create': { method: 'POST', write: true },
  'portal.recharge.get': { method: 'GET' }
};

const WRITE_ACTIONS = new Set(['portal.voucher.redeem', 'portal.recharge.create']);

export async function runPortalAction(params = {}, options = {}) {
  const fetchImpl = options.fetchImpl ?? fetch;
  const emitStderr = options.emitStderr ?? defaultEmitStderr;
  const resolvePortalUserAuthImpl = options.resolvePortalUserAuthImpl ?? resolvePortalUserAuth;
  const normalizeExecutePayloadImpl = options.normalizeExecutePayloadImpl ?? normalizeExecutePayload;

  const action = typeof params.action === 'string' ? params.action.trim() : '';
  if (!ACTIONS[action]) {
    return createLocalResult(400, 'VALIDATION_BAD_REQUEST', `unsupported action: ${action || '<empty>'}`);
  }

  const payload = toObject(params.payload);
  if (WRITE_ACTIONS.has(action) && payload.confirm !== true) {
    return createLocalResult(
      400,
      'VALIDATION_CONFIRM_REQUIRED',
      `${action} requires confirm=true`,
      { action, next_step: 'set payload.confirm=true to continue' }
    );
  }

  let auth;
  try {
    auth = await resolvePortalUserAuthImpl(
      {
        explicitApiKey: params.explicitApiKey,
        baseUrl: params.baseUrl,
        agentUid: params.agentUid,
        ownerUidHint: params.ownerUidHint
      },
      {
        fetchImpl,
        emitStderr
      }
    );
  } catch (error) {
    return createLocalResult(
      Number.isFinite(error?.status) ? error.status : 500,
      typeof error?.code === 'string' ? error.code : 'AUTH_UNAUTHORIZED',
      asMessage(error),
      {
        request_id: typeof error?.requestId === 'string' ? error.requestId : null
      }
    );
  }

  let request;
  try {
    request = await buildActionRequest(action, payload, auth, normalizeExecutePayloadImpl);
  } catch (error) {
    return createLocalResult(
      Number.isFinite(error?.status) ? error.status : 400,
      typeof error?.code === 'string' ? error.code : 'VALIDATION_BAD_REQUEST',
      asMessage(error),
      error?.details
    );
  }

  const response = await fetchImpl(`${auth.baseUrl}${request.path}`, {
    method: request.method,
    headers: {
      Authorization: `Bearer ${auth.userToken}`,
      ...(request.method === 'POST' ? { 'Content-Type': 'application/json' } : {})
    },
    ...(request.body !== undefined ? { body: JSON.stringify(request.body) } : {})
  });

  const body = await response.text();
  const parsed = parseJson(body);

  if (response.ok) {
    emitStderr({
      event: 'portal_action_success',
      action,
      status: response.status
    });
    return {
      ok: true,
      status: response.status,
      body
    };
  }

  const apiError = parseApiError(parsed, body, response.status);
  emitStderr({
    event: 'portal_action_failed',
    action,
    status: response.status,
    code: apiError.code,
    message: apiError.message,
    request_id: apiError.requestId
  });

  if (apiError.code === 'POINTS_INSUFFICIENT') {
    const rechargeUrl =
      parsed &&
      typeof parsed === 'object' &&
      parsed.error &&
      typeof parsed.error === 'object' &&
      parsed.error.details &&
      typeof parsed.error.details === 'object' &&
      typeof parsed.error.details.recharge_url === 'string'
        ? parsed.error.details.recharge_url
        : null;

    emitStderr({
      event: 'portal_action_recharge_hint',
      action,
      recharge_url: rechargeUrl,
      recommended_next_action: rechargeUrl ? 'open recharge_url' : 'portal.recharge.create'
    });
  }

  return {
    ok: false,
    status: response.status,
    body
  };
}

async function buildActionRequest(action, payload, auth, normalizeExecutePayloadImpl) {
  switch (action) {
    case 'portal.me':
      return {
        method: 'GET',
        path: '/user/me'
      };
    case 'portal.balance':
      return {
        method: 'GET',
        path: '/user/points/balance'
      };
    case 'portal.ledger.query':
      return {
        method: 'GET',
        path: buildPathWithQuery('/user/points/ledger', pickQuery(payload, ['date_from', 'date_to']))
      };
    case 'portal.usage.query':
      return {
        method: 'GET',
        path: buildPathWithQuery('/user/usage', pickQuery(payload, ['date_from', 'date_to', 'service_id']))
      };
    case 'portal.skill.execute': {
      const trustedSiteBaseUrl = resolveTrustedSiteBaseUrl(process.env.SKILL_SITE_BASE_URL ?? DEFAULT_SITE_BASE_URL);
      const normalized = await normalizeExecutePayloadImpl(payload, {
        siteBaseUrl: trustedSiteBaseUrl,
        requestedSiteBaseUrl: typeof payload.site_base_url === 'string' ? payload.site_base_url : undefined,
        userToken: auth.userToken,
        pathPrefix: typeof payload.path_prefix === 'string' ? payload.path_prefix : undefined
      });

      const capability = readRequiredString(normalized.capability, 'capability is required');
      const input = toObject(normalized.input);
      if (Object.keys(input).length === 0) {
        throw createActionError(400, 'VALIDATION_BAD_REQUEST', 'input must be an object');
      }

      const body = {
        capability,
        input
      };

      const requestId = typeof normalized.request_id === 'string' ? normalized.request_id.trim() : '';
      if (requestId) {
        body.request_id = requestId;
      }

      return {
        method: 'POST',
        path: '/user/skills/execute',
        body
      };
    }
    case 'portal.skill.poll': {
      const runId = resolveIdentifier(payload, ['run_id', 'runId'], 'run_id is required');
      return {
        method: 'GET',
        path: `/user/skills/runs/${encodeURIComponent(runId)}`
      };
    }
    case 'portal.skill.presentation': {
      const runId = resolveIdentifier(payload, ['run_id', 'runId'], 'run_id is required');
      const includeFiles = payload.include_files === undefined ? true : payload.include_files;
      return {
        method: 'GET',
        path: buildPathWithQuery(
          `/user/skills/runs/${encodeURIComponent(runId)}/presentation`,
          pickQuery({ ...payload, include_files: includeFiles }, ['channel', 'include_files'])
        )
      };
    }
    case 'portal.voucher.redeem': {
      const voucherCode = resolveIdentifier(payload, ['voucher_code', 'voucherCode'], 'voucher_code is required');
      return {
        method: 'POST',
        path: '/user/vouchers/redeem',
        body: {
          voucher_code: voucherCode
        }
      };
    }
    case 'portal.recharge.create': {
      const points = readRequiredPositiveInteger(payload.points, 'points must be a positive integer');
      return {
        method: 'POST',
        path: '/user/recharge/orders',
        body: {
          points
        }
      };
    }
    case 'portal.recharge.get': {
      const orderId = resolveIdentifier(payload, ['order_id', 'orderId'], 'order_id is required');
      return {
        method: 'GET',
        path: `/user/recharge/orders/${encodeURIComponent(orderId)}`
      };
    }
    default:
      throw createActionError(400, 'VALIDATION_BAD_REQUEST', `unsupported action: ${action}`);
  }
}

function buildPathWithQuery(path, query) {
  const entries = Object.entries(query).filter((entry) => {
    const value = entry[1];
    return typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean';
  });
  if (entries.length === 0) {
    return path;
  }
  const search = new URLSearchParams();
  for (const [key, value] of entries) {
    search.set(key, String(value));
  }
  return `${path}?${search.toString()}`;
}

function pickQuery(payload, fields) {
  const picked = {};
  for (const field of fields) {
    const value = payload[field];
    if (value !== undefined && value !== null) {
      picked[field] = value;
    }
  }
  return picked;
}

function readRequiredString(value, message) {
  if (typeof value !== 'string' || !value.trim()) {
    throw createActionError(400, 'VALIDATION_BAD_REQUEST', message);
  }
  return value.trim();
}

function readRequiredPositiveInteger(value, message) {
  if (!Number.isInteger(value) || Number(value) <= 0) {
    throw createActionError(400, 'VALIDATION_BAD_REQUEST', message);
  }
  return Number(value);
}

function resolveIdentifier(payload, keys, message) {
  for (const key of keys) {
    const value = payload[key];
    if (typeof value === 'string' && value.trim()) {
      return value.trim();
    }
  }
  throw createActionError(400, 'VALIDATION_BAD_REQUEST', message);
}

function createActionError(status, code, message, details) {
  const error = new Error(message);
  error.status = status;
  error.code = code;
  error.details = details;
  return error;
}

function createLocalResult(status, code, message, details = undefined) {
  const body = JSON.stringify({
    request_id: '',
    data: null,
    error: {
      code,
      message,
      ...(details ? { details } : {})
    }
  });

  return {
    ok: false,
    status,
    body
  };
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

function parseJson(body) {
  try {
    const parsed = JSON.parse(body);
    return parsed && typeof parsed === 'object' ? parsed : null;
  } catch {
    return null;
  }
}

function toObject(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    return {};
  }
  return { ...value };
}

function defaultEmitStderr(event) {
  process.stderr.write(`${JSON.stringify(event)}\n`);
}

function asMessage(error) {
  return error instanceof Error ? error.message : String(error);
}

function parseCliArgs(args) {
  if (args.length === 0) {
    return {
      explicitApiKey: '',
      action: 'portal.me',
      payloadJson: '{}',
      baseUrl: RUNTIME_DEFAULT_BASE_URL,
      agentUid: '',
      ownerUidHint: ''
    };
  }

  const first = args[0] ?? '';
  const firstLooksLikeAction = Boolean(ACTIONS[first]);

  if (firstLooksLikeAction) {
    return {
      explicitApiKey: '',
      action: first,
      payloadJson: args[1] ?? '{}',
      baseUrl: args[2] ?? RUNTIME_DEFAULT_BASE_URL,
      agentUid: args[3] ?? '',
      ownerUidHint: args[4] ?? ''
    };
  }

  return {
    explicitApiKey: first,
    action: args[1] ?? 'portal.me',
    payloadJson: args[2] ?? '{}',
    baseUrl: args[3] ?? RUNTIME_DEFAULT_BASE_URL,
    agentUid: args[4] ?? '',
    ownerUidHint: args[5] ?? ''
  };
}

async function main() {
  const parsed = parseCliArgs(process.argv.slice(2));

  let payload;
  try {
    payload = JSON.parse(parsed.payloadJson);
  } catch {
    const result = createLocalResult(400, 'VALIDATION_BAD_REQUEST', 'payload_json must be valid JSON object');
    process.stdout.write(`${result.body}\n`);
    process.exit(1);
  }

  const result = await runPortalAction({
    explicitApiKey: parsed.explicitApiKey,
    action: parsed.action,
    payload,
    baseUrl: parsed.baseUrl,
    agentUid: parsed.agentUid,
    ownerUidHint: parsed.ownerUidHint
  });

  process.stdout.write(`${result.body}\n`);
  if (!result.ok) {
    process.exit(1);
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  await main();
}
