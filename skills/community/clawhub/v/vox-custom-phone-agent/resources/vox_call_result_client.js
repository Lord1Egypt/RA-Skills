'use strict';

const { buildHmacHeaders } = require('./hmac_outbound_client');

const STATUS_QUERY_PATH = '/vox/v1/get/call/status';
const TURNS_QUERY_PATH = '/vox/v1/get/call/turns';

async function queryCallStatus({ credentials, callId, fetchImpl = globalThis.fetch }) {
  const body = await postVoxQuery({ credentials, path: STATUS_QUERY_PATH, callId, fetchImpl });
  const data = body.data || {};
  return {
    ok: body.code === 0,
    httpStatus: body._httpStatus,
    path: STATUS_QUERY_PATH,
    code: body.code,
    msg: body.msg || '',
    callId: data.callId || callId,
    status: data.status || 'unknown',
    body
  };
}

async function queryCallTurns({ credentials, callId, fetchImpl = globalThis.fetch }) {
  const body = await postVoxQuery({ credentials, path: TURNS_QUERY_PATH, callId, fetchImpl });
  const turns = Array.isArray(body.data) ? body.data : [];
  return {
    ok: body.code === 0,
    httpStatus: body._httpStatus,
    path: TURNS_QUERY_PATH,
    code: body.code,
    msg: body.msg || '',
    callId,
    turns,
    transcript: turnsToTranscript(turns),
    body
  };
}

async function postVoxQuery({ credentials, path, callId, fetchImpl = globalThis.fetch }) {
  if (!fetchImpl) throw new Error('fetch is not available. Use Node.js >= 18 or pass fetchImpl.');
  if (!credentials || !credentials.appId || !credentials.secret) throw new Error('formal Vox credentials are required');
  const baseUrl = credentials.callQueryBaseUrl || credentials.queryBaseUrl || process.env.VOX_CALL_QUERY_BASE_URL || credentials.baseUrl || 'https://vox.teddymobile.cn';
  const url = `${baseUrl.replace(/\/$/, '')}${path}`;
  const headers = buildHmacHeaders({ appId: credentials.appId, secret: credentials.secret, method: 'POST', path });
  const response = await fetchImpl(url, {
    method: 'POST',
    headers,
    body: JSON.stringify({ callId, appId: credentials.appId })
  });
  const text = await response.text();
  let body;
  try {
    body = text ? JSON.parse(text) : {};
  } catch (error) {
    body = { code: -1, msg: 'invalid_json', raw: text };
  }
  if (!response.ok) {
    body.code = body.code === undefined ? -1 : body.code;
    body.msg = body.msg || `HTTP ${response.status}`;
  }
  body._httpStatus = response.status;
  body._path = path;
  return body;
}

function turnsToTranscript(turns = []) {
  return turns.flatMap((turn) => {
    const items = [];
    if (turn.userText) {
      items.push({
        turnIndex: turn.turnIndex,
        role: 'callee',
        text: turn.userText,
        playedAt: turn.playbackCompletedAt || null
      });
    }
    if (turn.botText) {
      items.push({
        turnIndex: turn.turnIndex,
        role: 'assistant',
        text: turn.botText,
        playedAt: turn.playbackCompletedAt || null
      });
    }
    return items;
  });
}

module.exports = {
  STATUS_QUERY_PATH,
  TURNS_QUERY_PATH,
  queryCallStatus,
  queryCallTurns,
  turnsToTranscript
};
