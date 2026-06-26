'use strict';

const http = require('http');
const https = require('https');
const { createRequestId } = require('./request_id');

const DEFAULT_TIMEOUT_MS = 1500;
const DEFAULT_PORTAL_API_BASE_URL = 'https://vox-test.teddymobile.net/portal-api';
const DEFAULT_SKILL_ID = 'vox-custom-phone-agent';
const DEFAULT_SKILL_NAME = 'Vox Custom Phone Agent Skill';

function getAnalyticsEndpoint(env = process.env) {
  const explicit = env.SKILL_ANALYTICS_ENDPOINT || env.ANALYTICS_ENDPOINT;
  if (explicit) return normalizeAnalyticsEndpoint(explicit);
  const baseUrl = env.PORTAL_API_BASE_URL || DEFAULT_PORTAL_API_BASE_URL;
  return baseUrl ? normalizeAnalyticsEndpoint(baseUrl) : '';
}

function normalizeAnalyticsEndpoint(value) {
  const endpoint = String(value || '').trim().replace(/\/$/, '');
  if (!endpoint) return '';
  if (/\/api\/skill-journeys\/events$/.test(endpoint)) return endpoint;
  if (/\/api\/analytics\/skill-events$/.test(endpoint)) return endpoint.replace(/\/api\/analytics\/skill-events$/, '/api/skill-journeys/events');
  if (/\/api\/skill-journeys\/start$/.test(endpoint)) return endpoint.replace(/\/start$/, '/events');
  return `${endpoint}/api/skill-journeys/events`;
}

function getJourneyStartEndpoint(env = process.env) {
  return getAnalyticsEndpoint(env).replace(/\/events$/, '/start');
}

function getJourneyEventsEndpoint(env = process.env) {
  return getAnalyticsEndpoint(env);
}

function getJourneyFinishEndpoint(skillJourneyId, env = process.env) {
  const eventsEndpoint = getAnalyticsEndpoint(env);
  if (!eventsEndpoint || !skillJourneyId) return '';
  return eventsEndpoint.replace(/\/events$/, `/${encodeURIComponent(skillJourneyId)}/finish`);
}

function normalizeUseMode(useMode) {
  if (useMode === 'formal') return 'production';
  if (useMode === 'production') return 'production';
  if (useMode === 'trial') return 'trial';
  return useMode || undefined;
}

function buildBaseEvent({ eventName, context = {}, properties = {}, env = process.env }) {
  const eventProperties = properties.properties || properties;
  const event = {
    event_name: eventName,
    event_id: properties.event_id || createAnalyticsEventId(context, eventName),
    timestamp: new Date().toISOString(),
    tenant_id: context.tenant_id,
    skill_id: env.SKILL_ID || context.skill_id || DEFAULT_SKILL_ID,
    skill_name: env.SKILL_NAME || context.skill_name || DEFAULT_SKILL_NAME,
    skill_version: env.SKILL_VERSION || context.skill_version || '0.1.0',
    source: context.source || 'unknown',
    distribution_channel: context.distribution_channel || context.source || 'unknown',
    registry: context.registry || 'unknown',
    run_id: context.run_id,
    installation_id: context.installation_id,
    usage_session_id: context.usage_session_id,
    skill_invocation_id: context.skill_invocation_id,
    tool_call_id: context.tool_call_id,
    request_id: context.request_id || context.run_id,
    trace_id: context.trace_id,
    session_id: context.session_id,
    user_id: context.user_id,
    anonymous_id: context.anonymous_id,
    workspace_id: context.workspace_id,
    host: context.host,
    use_mode: normalizeUseMode(context.use_mode),
    use_mode_source: context.use_mode_source,
    entry_strategy: context.entry_strategy,
    scenario: context.scenario,
    voice_type: context.voice_type,
    status: context.status,
    duration_ms: context.duration_ms,
    error_code: context.error_code,
    error_stage: context.error_stage,
    vox_http_status: context.vox_http_status,
    vox_code: context.vox_code === undefined || context.vox_code === null ? context.vox_code : String(context.vox_code),
    prompt_length: context.prompt_length,
    standard_event_type: context.standard_event_type || properties.standard_event_type,
    sensitive_payload: sanitizeSensitivePayload(properties.sensitive_payload || context.sensitive_payload),
    properties: sanitizeProperties(eventProperties)
  };
  delete event.properties.event_id;
  delete event.properties.standard_event_type;
  delete event.properties.sensitive_payload;
  return removeUndefined(event);
}

function sanitizeProperties(properties = {}) {
  const forbidden = new Set([
    'prompt',
    'full_prompt',
    'callee',
    'phone',
    'VOX_APP_ID',
    'VOX_SECRET',
    'HMAC-SIGNATURE',
    'headers',
    'payload',
    'agent_profile',
    'vox_response_body',
    'stack_trace',
    'file_path'
  ]);
  const safe = {};
  for (const [key, value] of Object.entries(properties || {})) {
    if (!forbidden.has(key)) safe[key] = value;
  }
  return safe;
}

function sanitizeSensitivePayload(payload = undefined) {
  if (!payload || typeof payload !== 'object') return undefined;
  const forbidden = new Set(['VOX_APP_ID', 'VOX_SECRET', 'HMAC-SIGNATURE', 'authorization', 'password', 'token', 'secret', 'headers']);
  const safe = {};
  for (const [key, value] of Object.entries(payload)) {
    if (!forbidden.has(key)) safe[key] = value;
  }
  return Object.keys(safe).length ? safe : undefined;
}

function removeUndefined(value) {
  const result = {};
  for (const [key, val] of Object.entries(value)) {
    if (val !== undefined) result[key] = val;
  }
  return result;
}

function createAnalyticsEventId(context = {}, eventName = 'event') {
  const sequence = (context._analyticsEventSequence = (context._analyticsEventSequence || 0) + 1);
  const stableRunId = context.run_id || context.request_id || context.skill_invocation_id || 'run';
  return ['jevt', stableRunId, safeEventName(eventName), sequence].join('_');
}

function safeEventName(eventName) {
  return String(eventName || 'event').replace(/[^a-zA-Z0-9]+/g, '_').replace(/^_+|_+$/g, '') || 'event';
}

function dispatchAnalyticsEvent(event, options = {}) {
  const env = options.env || process.env;
  if (env.SKILL_ANALYTICS_DISABLED === 'true') return Promise.resolve(false);
  return dispatchJourneyEvent(event, options);
}

async function dispatchJourneyEvent(event, options = {}) {
  const env = options.env || process.env;
  const journeyId = await ensureJourneyStarted(event, options);
  if (!journeyId) return false;
  const payload = JSON.stringify(buildJourneyEventPayload(event, journeyId));
  const response = await postJson(getJourneyEventsEndpoint(env), payload, options);
  if (isDebugEnabled(env)) debugLog(env, response ? 'sent' : 'failed', event.event_name, event.skill_id, event.source);
  return response;
}

function ensureJourneyStarted(event, options = {}) {
  if (event.skill_journey_id) return Promise.resolve(event.skill_journey_id);
  if (options.context && options.context.skill_journey_id) return Promise.resolve(options.context.skill_journey_id);
  if (options.context && options.context._journeyPromise) return options.context._journeyPromise;
  const promise = startJourney(event, options).then((journeyId) => {
    if (options.context && journeyId) options.context.skill_journey_id = journeyId;
    return journeyId;
  });
  if (options.context) options.context._journeyPromise = promise;
  return promise;
}

async function startJourney(event, options = {}) {
  const env = options.env || process.env;
  const response = await postJson(getJourneyStartEndpoint(env), JSON.stringify(buildJourneyStartPayload(event)), options, true);
  const journeyId = response && (response.skill_journey_id || response.skillJourneyId);
  if (isDebugEnabled(env)) debugLog(env, journeyId ? 'journey_started' : 'journey_start_failed', event.skill_id, event.source);
  return journeyId || '';
}

async function finishSkillJourney(skillJourneyId, status = 'finished', finalOutcome = 'completed', options = {}) {
  const env = options.env || process.env;
  if (env.SKILL_ANALYTICS_DISABLED === 'true') return false;
  if (!skillJourneyId) return false;
  const payload = JSON.stringify({ status, final_outcome: finalOutcome });
  return postJson(getJourneyFinishEndpoint(skillJourneyId, env), payload, options);
}

function buildJourneyStartPayload(event) {
  const userId = resolveJourneyUserId(event);
  return removeUndefined({
    tenant_id: event.tenant_id || '',
    user_id: userId,
    skill_id: event.skill_id,
    skill_version: event.skill_version,
    installation_id: event.installation_id,
    entry_event: 'usage_started',
    external_journey_key: event.external_journey_key || buildExternalJourneyKey(event, userId),
    metadata: sanitizeProperties({
      channel: event.source,
      source: event.source,
      distribution_channel: event.distribution_channel,
      registry: event.registry,
      host: event.host,
      usage_session_id: event.usage_session_id || event.session_id,
      anonymous_id: event.anonymous_id,
      trigger: 'skill_runtime'
    })
  });
}

function buildJourneyEventPayload(event, journeyId) {
  const mapped = mapJourneyEvent(event.event_name);
  return removeUndefined({
    event_id: event.event_id,
    skill_journey_id: journeyId,
    tenant_id: event.tenant_id || '',
    user_id: resolveJourneyUserId(event),
    skill_id: event.skill_id,
    skill_version: event.skill_version,
    event_type: mapped.event_type,
    standard_event_type: event.standard_event_type || mapped.standard_event_type,
    installation_id: event.installation_id,
    usage_session_id: event.usage_session_id || event.session_id,
    skill_invocation_id: event.skill_invocation_id,
    run_id: event.run_id,
    tool_call_id: event.tool_call_id,
    request_id: event.request_id || event.run_id,
    trace_id: event.trace_id,
    status: normalizeJourneyStatus(event.status, event.event_name),
    duration_ms: event.duration_ms,
    timestamp: event.timestamp,
    metadata: sanitizeProperties({
      source: event.source,
      distribution_channel: event.distribution_channel,
      registry: event.registry,
      host: event.host,
      original_event_name: event.event_name,
      use_mode: event.use_mode,
      use_mode_source: event.use_mode_source,
      entry_strategy: event.entry_strategy,
      scenario: event.scenario,
      voice_type: event.voice_type,
      prompt_length: event.prompt_length,
      error_code: event.error_code,
      error_stage: event.error_stage,
      vox_http_status: event.vox_http_status,
      vox_code: event.vox_code,
      ...(event.properties || {})
    }),
    sensitive_payload: event.sensitive_payload
  });
}

function mapJourneyEvent(eventName) {
  const map = {
    skill_invoked: { event_type: 'skill_invoked', standard_event_type: 'skill_invoked' },
    skill_needs_input: { event_type: 'vox.needs_input', standard_event_type: 'skill_needs_input' },
    skill_safety_blocked: { event_type: 'vox.safety_blocked', standard_event_type: 'skill_safety_blocked' },
    skill_credentials_missing: { event_type: 'vox.credentials_missing', standard_event_type: 'skill_credentials_missing' },
    skill_task_ready: { event_type: 'vox.task_ready', standard_event_type: 'skill_task_ready' },
    skill_run_started: { event_type: 'run_started', standard_event_type: 'skill_run_started' },
    skill_run_completed: { event_type: 'run_completed', standard_event_type: 'skill_run_completed' },
    skill_run_failed: { event_type: 'run_failed', standard_event_type: 'skill_run_failed' },
    skill_registration_prompted: { event_type: 'vox.registration_prompted', standard_event_type: 'skill_registration_prompted' },
    skill_tool_call_started: { event_type: 'vox.outbound_call_started', standard_event_type: 'tool_call_started' },
    skill_tool_call_completed: { event_type: 'vox.outbound_call_completed', standard_event_type: 'tool_call_completed' },
    skill_tool_call_failed: { event_type: 'vox.outbound_call_failed', standard_event_type: 'tool_call_failed' },
    skill_input_received: { event_type: 'vox_custom_phone_agent.input_received', standard_event_type: 'business_step_completed' },
    skill_trial_auto_selected: { event_type: 'vox.trial_auto_selected', standard_event_type: 'business_step_completed' },
    skill_intent_parsed: { event_type: 'vox_custom_phone_agent.intent_parsed', standard_event_type: 'business_step_completed' },
    skill_policy_checked: { event_type: 'vox_custom_phone_agent.policy_checked', standard_event_type: 'business_step_completed' }
  };
  return map[eventName] || { event_type: eventName, standard_event_type: undefined };
}

function normalizeJourneyStatus(status, eventName) {
  if (eventName === 'skill_run_failed' || eventName === 'skill_safety_blocked') return 'failed';
  if (eventName === 'skill_run_started') return 'running';
  if (eventName === 'skill_run_completed') return 'success';
  return status;
}

function resolveJourneyUserId(event) {
  return event.user_id || event.anonymous_id || event.session_id || event.usage_session_id || 'anonymous_skillhub_user';
}

function buildExternalJourneyKey(event, userId) {
  const stableSession = event.usage_session_id || event.session_id || event.run_id;
  return [event.skill_id, userId, event.source, stableSession].filter(Boolean).join(':');
}

function postJsonWithNode(endpoint, payload, timeoutMs, parseBody = false) {
  return new Promise((resolve) => {
    let url;
    try {
      url = new URL(endpoint);
    } catch (_) {
      resolve(parseBody ? null : false);
      return;
    }
    const client = url.protocol === 'http:' ? http : https;
    const request = client.request({
      method: 'POST',
      hostname: url.hostname,
      port: url.port || undefined,
      path: `${url.pathname}${url.search}`,
      timeout: timeoutMs,
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) }
    }, (response) => {
      const chunks = [];
      response.on('data', (chunk) => chunks.push(chunk));
      response.on('end', () => {
        const ok = response.statusCode >= 200 && response.statusCode < 300;
        if (!parseBody) return resolve(ok);
        if (!ok) return resolve(null);
        try {
          const text = Buffer.concat(chunks).toString('utf8');
          resolve(text ? JSON.parse(text) : {});
        } catch (_) {
          resolve(null);
        }
      });
    });
    request.on('timeout', () => request.destroy());
    request.on('error', () => resolve(parseBody ? null : false));
    request.write(payload);
    request.end();
  });
}

async function postJson(endpoint, payload, options = {}, parseBody = false) {
  if (!endpoint) return parseBody ? null : false;
  const env = options.env || process.env;
  const fetchImpl = options.fetchImpl || globalThis.fetch;
  const timeoutMs = Number(env.SKILL_ANALYTICS_TIMEOUT_MS || DEFAULT_TIMEOUT_MS);
  if (!fetchImpl) return postJsonWithNode(endpoint, payload, timeoutMs, parseBody);
  const controller = typeof AbortController === 'function' ? new AbortController() : null;
  const timer = controller ? setTimeout(() => controller.abort(), timeoutMs) : null;
  try {
    const response = await fetchImpl(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: payload,
      signal: controller ? controller.signal : undefined
    });
    if (!response || !response.ok) return parseBody ? null : false;
    if (!parseBody) return true;
    if (typeof response.json === 'function') return response.json();
    if (typeof response.text === 'function') {
      const text = await response.text();
      return text ? JSON.parse(text) : {};
    }
    return {};
  } catch (error) {
    if (isDebugEnabled(env)) debugLog(env, 'failed', error && error.message ? error.message : error);
    return parseBody ? null : false;
  } finally {
    if (timer) clearTimeout(timer);
  }
}

function isDebugEnabled(env = process.env) {
  return env.SKILL_ANALYTICS_DEBUG === 'true';
}

function debugLog(env, ...args) {
  if (isDebugEnabled(env)) console.log('[skill analytics]', ...args);
}

function trackSkillEvent(eventName, context = {}, properties = {}, options = {}) {
  const env = options.env || process.env;
  const event = buildBaseEvent({ eventName, context, properties, env });
  const dispatchOptions = { ...options, context };
  if (options.awaitAnalytics) return dispatchAnalyticsEvent(event, dispatchOptions);
  void dispatchAnalyticsEvent(event, dispatchOptions);
  return Promise.resolve(true);
}

module.exports = {
  DEFAULT_SKILL_ID,
  DEFAULT_SKILL_NAME,
  DEFAULT_PORTAL_API_BASE_URL,
  buildBaseEvent,
  dispatchAnalyticsEvent,
  getJourneyEventsEndpoint,
  getJourneyFinishEndpoint,
  getJourneyStartEndpoint,
  finishSkillJourney,
  getAnalyticsEndpoint,
  normalizeAnalyticsEndpoint,
  normalizeUseMode,
  sanitizeSensitivePayload,
  trackSkillEvent
};
