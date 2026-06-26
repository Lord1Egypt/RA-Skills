// release-gate: allow-env-network
const DEFAULT_TIMEOUT_MS = 2000;

function parseTimeout(rawValue) {
  const parsed = Number(rawValue);
  if (Number.isFinite(parsed) && parsed > 0) {
    return Math.floor(parsed);
  }
  return DEFAULT_TIMEOUT_MS;
}

function isTelemetryEnabled() {
  const raw = (process.env.SKILL_TELEMETRY_ENABLED ?? 'true').trim().toLowerCase();
  return raw !== '0' && raw !== 'false' && raw !== 'off' && raw !== 'no';
}

function resolveTelemetryBaseUrl(baseUrl) {
  const fromEnv = (process.env.SKILL_TELEMETRY_BASE_URL ?? '').trim();
  return (fromEnv || baseUrl || '').replace(/\/+$/, '');
}

async function postJsonWithTimeout(url, body, headers) {
  const controller = new AbortController();
  const timeoutMs = parseTimeout(process.env.SKILL_TELEMETRY_TIMEOUT_MS);
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...headers
      },
      body: JSON.stringify(body),
      signal: controller.signal
    });

    const text = await response.text();
    return { ok: response.ok, status: response.status, text };
  } finally {
    clearTimeout(timeout);
  }
}

function normalizeRunId(runId) {
  if (typeof runId !== 'string') {
    return undefined;
  }
  const normalized = runId.trim();
  return normalized ? normalized : undefined;
}

function normalizeRequestId(requestId) {
  if (typeof requestId !== 'string') {
    return undefined;
  }
  const normalized = requestId.trim();
  return normalized ? normalized : undefined;
}

function normalizeEventName(eventName) {
  if (typeof eventName !== 'string') {
    return null;
  }
  const normalized = eventName.trim();
  return normalized ? normalized : null;
}

export async function emitTelemetry(params) {
  if (!isTelemetryEnabled()) {
    return false;
  }

  const eventName = normalizeEventName(params?.eventName);
  if (!eventName) {
    return false;
  }

  const telemetryBaseUrl = resolveTelemetryBaseUrl(params.baseUrl);
  if (!telemetryBaseUrl) {
    return false;
  }

  const event = {
    event_name: eventName,
    event_at: new Date().toISOString(),
    status: params.status === 'error' ? 'error' : 'ok',
    ...(normalizeRunId(params.runId) ? { run_id: normalizeRunId(params.runId) } : {}),
    ...(normalizeRequestId(params.requestId) ? { request_id_hint: normalizeRequestId(params.requestId) } : {}),
    ...(typeof params.capability === 'string' && params.capability.trim()
      ? { capability_id: params.capability.trim() }
      : {}),
    properties: {
      ...(params.properties && typeof params.properties === 'object' ? params.properties : {}),
      ...(typeof params.agentUid === 'string' && params.agentUid.trim()
        ? { agent_uid: params.agentUid.trim() }
        : {}),
      ...(typeof params.ownerUidHint === 'string' && params.ownerUidHint.trim()
        ? { owner_uid_hint: params.ownerUidHint.trim() }
        : {})
    }
  };

  const apiKey = typeof params.apiKey === 'string' ? params.apiKey.trim() : '';
  const agentUid = typeof params.agentUid === 'string' ? params.agentUid.trim() : '';

  const endpointPath = apiKey ? '/agent/telemetry/ingest' : '/telemetry/ingest';
  const payload = apiKey
    ? {
        agent_uid: agentUid,
        events: [event]
      }
    : {
        session_id: agentUid ? `skill_${agentUid}` : 'skill_anonymous',
        events: [event]
      };

  const headers = apiKey ? { 'X-API-Key': apiKey } : {};

  try {
    const response = await postJsonWithTimeout(`${telemetryBaseUrl}${endpointPath}`, payload, headers);
    if (!response.ok) {
      console.error(
        JSON.stringify({
          event: 'skill_telemetry_emit_failed',
          telemetry_event: eventName,
          status: response.status,
          body: response.text.slice(0, 200)
        })
      );
      return false;
    }
    return true;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(
      JSON.stringify({
        event: 'skill_telemetry_emit_failed',
        telemetry_event: eventName,
        message
      })
    );
    return false;
  }
}

export function extractRequestContext(body) {
  try {
    const parsed = JSON.parse(body);
    if (!parsed || typeof parsed !== 'object') {
      return { requestId: null, runId: null, status: null };
    }
    const requestId = typeof parsed.request_id === 'string' ? parsed.request_id : null;
    const data = parsed.data && typeof parsed.data === 'object' ? parsed.data : null;
    const runId = data && typeof data.run_id === 'string' ? data.run_id : null;
    const status = data && typeof data.status === 'string' ? data.status : null;
    return { requestId, runId, status };
  } catch {
    return { requestId: null, runId: null, status: null };
  }
}
