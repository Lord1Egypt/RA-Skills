'use strict';

const crypto = require('crypto');

async function sendPostCallCallback({ job, result, env = process.env, fetchImpl = globalThis.fetch }) {
  if (!job || !job.callbackUrl) return { ok: false, skipped: true, reason: 'callbackUrl missing' };
  if (!fetchImpl) throw new Error('fetch is not available. Use Node.js >= 18 or pass fetchImpl.');

  const body = buildCallbackBody({ job, result });
  const rawBody = JSON.stringify(body);
  const timestamp = String(Date.now());
  const headers = {
    'Content-Type': 'application/json',
    'X-Skill-Event': body.event,
    'X-Skill-Request-Id': body.requestId,
    'X-Skill-Timestamp': timestamp
  };
  if (job.callbackToken) headers.Authorization = `Bearer ${job.callbackToken}`;
  const secret = env.POST_CALL_CALLBACK_HMAC_SECRET || '';
  if (secret) headers['X-Skill-Signature'] = `sha256=${signCallbackBody({ timestamp, rawBody, secret })}`;

  const response = await fetchWithTimeout(job.callbackUrl, {
    method: 'POST',
    headers,
    body: rawBody
  }, Number(env.POST_CALL_CALLBACK_TIMEOUT_MS || 5000), fetchImpl);

  return { ok: response.ok, httpStatus: response.status, body };
}

function buildCallbackBody({ job, result }) {
  const transcript = job.postCallOptions && job.postCallOptions.includeTranscript === false
    ? undefined
    : result.transcript;
  const body = {
    event: 'vox.call.ended',
    version: '1.0',
    requestId: job.requestId,
    callId: job.callId,
    status: result.status || 'completed',
    calleeMasked: job.calleeMasked,
    startedAt: null,
    endedAt: inferEndedAt(result.turns),
    durationSec: null,
    hangupReason: null,
    goal: job.goal || '',
    role: job.role || '',
    voiceType: job.voiceType || '',
    summary: result.summary || buildSimpleSummary(result.transcript),
    outcome: result.outcome || buildSimpleOutcome(result.transcript),
    recordingUrl: null,
    metadata: job.metadata || {}
  };
  if (transcript !== undefined) body.transcript = transcript;
  return body;
}

function inferEndedAt(turns = []) {
  const values = turns.map((turn) => turn.playbackCompletedAt).filter(Boolean);
  return values.length ? values[values.length - 1] : null;
}

function buildSimpleSummary(transcript = []) {
  if (!transcript || transcript.length === 0) return '通话已结束，暂无通话文本。';
  const calleeTexts = transcript.filter((item) => item.role === 'callee').map((item) => item.text).filter(Boolean);
  return calleeTexts.length
    ? `通话已结束，用户共回复 ${calleeTexts.length} 轮。`
    : '通话已结束，未识别到用户侧回复。';
}

function buildSimpleOutcome(transcript = []) {
  const calleeTexts = transcript.filter((item) => item.role === 'callee').map((item) => item.text).join(' ');
  return {
    reached: transcript.length > 0,
    confirmed: /好的|知道了|确认|可以|同意|没问题/.test(calleeTexts),
    needsHumanFollowUp: /人工|投诉|不满意|稍后|再联系|拒绝/.test(calleeTexts),
    tags: []
  };
}

function signCallbackBody({ timestamp, rawBody, secret }) {
  return crypto.createHmac('sha256', secret).update(`${timestamp}.${rawBody}`, 'utf8').digest('hex');
}

function fetchWithTimeout(url, options, timeoutMs, fetchImpl) {
  const controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
  const timer = controller ? setTimeout(() => controller.abort(), timeoutMs) : null;
  if (timer && timer.unref) timer.unref();
  return fetchImpl(url, { ...options, signal: controller ? controller.signal : undefined })
    .finally(() => {
      if (timer) clearTimeout(timer);
    });
}

module.exports = {
  buildCallbackBody,
  sendPostCallCallback,
  signCallbackBody
};
