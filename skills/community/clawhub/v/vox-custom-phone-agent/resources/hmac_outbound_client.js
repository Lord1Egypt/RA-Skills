'use strict';

const crypto = require('crypto');

const OUTBOUND_PATH = '/vox/v1/outbound';
const TRIAL_OUTBOUND_PATH = '/vox/v2/outbound';

function toGMTDate(date = new Date()) {
  return date.toUTCString();
}

function sortUriParams(uriParams = '') {
  if (!uriParams) return '';
  return String(uriParams).split('&').filter(Boolean).sort().join('&');
}

function buildSignatureMessage({ method, path, uriParams, appId, dateGMT }) {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return [
    String(method).toUpperCase(),
    normalizedPath,
    sortUriParams(uriParams),
    appId,
    dateGMT,
    `HMAC-APPID:${appId}`,
    ''
  ].join('\n');
}

function signHmacSha256(message, secret) {
  return crypto.createHmac('sha256', secret).update(message, 'utf8').digest('base64');
}

function buildHmacHeaders({ appId, secret, method = 'POST', path = OUTBOUND_PATH, uriParams = '', date = new Date() }) {
  const dateGMT = toGMTDate(date);
  const message = buildSignatureMessage({ method, path, uriParams, appId, dateGMT });
  const signature = signHmacSha256(message, secret);
  return {
    'Content-Type': 'application/json',
    'HMAC-APPID': appId,
    'HMAC-DATE': dateGMT,
    'HMAC-SIGNATURE': signature,
    'HMAC-ALGORITHM': 'hmac-sha256',
    'HMAC-SIGNED-HEADERS': 'HMAC-APPID'
  };
}

function buildOutboundPayload({ credentials, callee, requestId, voiceType, agentProfile }) {
  const payload = {
    botid: credentials.botId || '',
    callee,
    requestId,
    botType: 'custom',
    extra: JSON.stringify({
      voiceType: String(voiceType),
      agent_profile: agentProfile
    })
  };
  if (credentials.appId) payload.appId = credentials.appId;
  return payload;
}

async function callVoxOutbound({ credentials, payload, fetchImpl = globalThis.fetch }) {
  if (!fetchImpl) throw new Error('fetch is not available. Use Node.js >= 18 or pass fetchImpl.');
  const baseUrl = credentials.baseUrl || 'https://vox.teddymobile.cn';
  const path = credentials.trialMode ? TRIAL_OUTBOUND_PATH : OUTBOUND_PATH;
  const url = `${baseUrl.replace(/\/$/, '')}${path}`;
  const headers = credentials.trialMode
    ? { 'Content-Type': 'application/json' }
    : buildHmacHeaders({ appId: credentials.appId, secret: credentials.secret });
  const response = await fetchImpl(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload)
  });

  const text = await response.text();
  let body;
  try {
    body = text ? JSON.parse(text) : {};
  } catch (error) {
    body = { raw: text };
  }

  return {
    ok: response.ok && (body.code === undefined || body.code === 0),
    httpStatus: response.status,
    requestId: body && body.data ? body.data.requestId : undefined,
    callId: body && body.data ? body.data.callId : undefined,
    status: body && body.data ? body.data.status : undefined,
    body
  };
}

module.exports = {
  OUTBOUND_PATH,
  TRIAL_OUTBOUND_PATH,
  buildHmacHeaders,
  buildOutboundPayload,
  buildSignatureMessage,
  callVoxOutbound,
  signHmacSha256,
  sortUriParams,
  toGMTDate
};
