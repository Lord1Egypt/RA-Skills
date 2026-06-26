const DEFAULT_PORTAL_API_BASE_URL = 'https://vox-test.teddymobile.net/portal-api';
const PORTAL_API_BASE_URL = (process.env.PORTAL_API_BASE_URL || DEFAULT_PORTAL_API_BASE_URL).replace(/\/$/, '');
const SKILL_ANALYTICS_ENDPOINT = process.env.SKILL_ANALYTICS_ENDPOINT || process.env.ANALYTICS_ENDPOINT || '';
const SKILL_ANALYTICS_TIMEOUT_MS = Number(process.env.SKILL_ANALYTICS_TIMEOUT_MS || 2000);

function isDisabled() {
  return ['1', 'true', 'yes'].includes(String(process.env.SKILL_ANALYTICS_DISABLED || '').toLowerCase());
}

function analyticsUrl(path) {
  if (isDisabled() || !PORTAL_API_BASE_URL) return null;
  return `${PORTAL_API_BASE_URL}${path}`;
}

function eventAnalyticsUrl() {
  if (isDisabled()) return null;
  return SKILL_ANALYTICS_ENDPOINT || analyticsUrl('/api/skill-journeys/events');
}

async function fetchWithTimeout(fetchImpl, url, options) {
  if (!SKILL_ANALYTICS_TIMEOUT_MS || typeof AbortController !== 'function') {
    return fetchImpl(url, options);
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), SKILL_ANALYTICS_TIMEOUT_MS);
  try {
    return await fetchImpl(url, { ...options, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

function nowIso() {
  return new Date().toISOString();
}

function createEventId(prefix = 'jevt') {
  return `${prefix}_${Date.now()}_${Math.random().toString(16).slice(2, 10)}`;
}

function getFetch(fetchImpl) {
  return fetchImpl || (typeof fetch === 'function' ? fetch : null);
}

function shouldWarn() {
  return Boolean(PORTAL_API_BASE_URL && process.env.SKILL_ANALYTICS_DEBUG === '1');
}

async function startSkillJourney(input, options = {}) {
  const url = analyticsUrl('/api/skill-journeys/start');
  const fetchImpl = getFetch(options.fetchImpl);
  if (!url || !fetchImpl) return { disabled: true };

  const response = await fetchWithTimeout(fetchImpl, url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      tenant_id: input.tenantId,
      user_id: input.userId,
      skill_id: input.skillId,
      skill_version: input.skillVersion,
      installation_id: input.installationId,
      entry_event: input.entryEvent || 'usage_started',
      external_journey_key: input.externalJourneyKey,
      metadata: input.metadata || {},
    }),
  });

  if (!response.ok) throw new Error(`startSkillJourney failed: ${response.status}`);
  return response.json();
}

async function reportJourneyEvent(input, options = {}) {
  const url = eventAnalyticsUrl();
  const fetchImpl = getFetch(options.fetchImpl);
  if (!url || !fetchImpl || !input.skillJourneyId) return { disabled: true };

  const response = await fetchWithTimeout(fetchImpl, url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      event_id: input.eventId || createEventId(),
      skill_journey_id: input.skillJourneyId,
      tenant_id: input.tenantId,
      user_id: input.userId,
      skill_id: input.skillId,
      skill_version: input.skillVersion,
      event_type: input.eventType,
      standard_event_type: input.standardEventType,
      installation_id: input.installationId,
      usage_session_id: input.sessionId,
      skill_invocation_id: input.skillInvocationId,
      run_id: input.runId,
      tool_call_id: input.toolCallId,
      request_id: input.requestId,
      trace_id: input.traceId,
      status: input.status,
      duration_ms: input.durationMs,
      error_code: input.errorCode,
      error_message: input.errorMessage,
      timestamp: input.timestamp || nowIso(),
      metadata: input.metadata || {},
      sensitive_payload: input.sensitivePayload || undefined,
    }),
  });

  if (!response.ok) throw new Error(`reportJourneyEvent failed: ${response.status}`);
  return response.json();
}

async function finishSkillJourney(input, options = {}) {
  const url = analyticsUrl(`/api/skill-journeys/${encodeURIComponent(input.skillJourneyId)}/finish`);
  const fetchImpl = getFetch(options.fetchImpl);
  if (!url || !fetchImpl || !input.skillJourneyId) return { disabled: true };

  const response = await fetchWithTimeout(fetchImpl, url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      status: input.status || 'finished',
      final_outcome: input.finalOutcome || 'completed',
    }),
  });

  if (!response.ok) throw new Error(`finishSkillJourney failed: ${response.status}`);
  return response.json();
}

async function safeStartSkillJourney(input, options) {
  try {
    return await startSkillJourney(input, options);
  } catch (error) {
    if (shouldWarn()) console.warn('[skill-analytics] start failed', error && error.message ? error.message : error);
    return { ok: false, skipped: true };
  }
}

async function safeReportJourneyEvent(input, options) {
  try {
    return await reportJourneyEvent(input, options);
  } catch (error) {
    if (shouldWarn()) console.warn('[skill-analytics] report failed', error && error.message ? error.message : error);
    return { ok: false, skipped: true };
  }
}

async function safeFinishSkillJourney(input, options) {
  try {
    return await finishSkillJourney(input, options);
  } catch (error) {
    if (shouldWarn()) console.warn('[skill-analytics] finish failed', error && error.message ? error.message : error);
    return { ok: false, skipped: true };
  }
}

module.exports = {
  createEventId,
  nowIso,
  startSkillJourney,
  reportJourneyEvent,
  finishSkillJourney,
  safeStartSkillJourney,
  safeReportJourneyEvent,
  safeFinishSkillJourney,
};
