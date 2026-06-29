const ALLOWED_EVENTS = new Set([
  'calculator_viewed',
  'calculator_key_activation_clicked',
  'calculator_checkout_clicked',
  'calculator_checkout_unavailable',
  'calculator_compare_plans_clicked',
  'calculator_audit_brief_copied',
  'calculator_magic_link_requested',
  'calculator_magic_link_sent',
  'calculator_magic_link_failed',
  'calculator_oauth_clicked',
  'calculator_oauth_failed',
  'pricing_viewed',
  'pricing_key_activation_clicked',
  'pricing_key_recovery_clicked',
  'pricing_checkout_clicked',
  'pricing_account_clicked',
  'pricing_quickstart_clicked',
  'pricing_oauth_clicked',
  'pricing_oauth_failed',
  'pricing_magic_link_requested',
  'pricing_magic_link_sent',
  'pricing_magic_link_failed',
  'pricing_setup_next_clicked',
  'fusion_viewed',
  'fusion_key_activation_clicked',
  'fusion_checkout_clicked',
  'fusion_quickstart_clicked',
  'fusion_gateway_migration_clicked',
  'fusion_pricing_clicked',
  'fusion_models_clicked',
  'fusion_magic_link_requested',
  'fusion_magic_link_sent',
  'fusion_magic_link_failed',
  'fusion_oauth_clicked',
  'fusion_oauth_failed',
  'gateway_migration_magic_link_requested',
  'gateway_migration_magic_link_sent',
  'gateway_migration_magic_link_failed',
  'gateway_migration_oauth_clicked',
  'gateway_migration_oauth_failed',
  'agent_native_magic_link_requested',
  'agent_native_magic_link_sent',
  'agent_native_magic_link_failed',
  'agent_native_oauth_clicked',
  'agent_native_oauth_failed',
  'integrations_magic_link_requested',
  'integrations_magic_link_sent',
  'integrations_magic_link_failed',
  'integrations_oauth_clicked',
  'integrations_oauth_failed',
  'managed_access_interest_clicked',
  'managed_access_viewed',
  'managed_access_form_started',
  'managed_access_request_submitted',
  'managed_access_request_received',
  'managed_access_quick_request_submitted',
  'managed_access_quick_request_received',
  'managed_access_quick_request_failed',
  'quickstart_viewed',
  'quickstart_account_clicked',
  'quickstart_setup_next_clicked',
  'quickstart_api_reference_clicked',
  'quickstart_gateway_migration_clicked',
  'quickstart_managed_access_clicked',
  'quickstart_models_clicked',
  'quickstart_codex_clicked',
  'quickstart_troubleshooting_clicked',
  'quickstart_pricing_clicked',
  'quickstart_status_clicked',
  'quickstart_oauth_clicked',
  'quickstart_oauth_failed',
  'quickstart_magic_link_requested',
  'quickstart_magic_link_sent',
  'quickstart_magic_link_failed',
  'quickstart_snippet_copied',
  'codex_docs_viewed',
  'codex_docs_key_activation_clicked',
  'codex_docs_account_clicked',
  'codex_docs_api_reference_clicked',
  'codex_docs_quickstart_clicked',
  'codex_docs_troubleshooting_clicked',
  'codex_docs_models_clicked',
  'codex_docs_status_clicked',
  'codex_docs_snippet_copied',
  'codex_docs_magic_link_requested',
  'codex_docs_magic_link_sent',
  'codex_docs_magic_link_failed',
  'api_reference_magic_link_requested',
  'api_reference_magic_link_sent',
  'api_reference_magic_link_failed',
  'api_reference_oauth_clicked',
  'api_reference_oauth_failed',
  'api_troubleshooting_magic_link_requested',
  'api_troubleshooting_magic_link_sent',
  'api_troubleshooting_magic_link_failed',
  'api_troubleshooting_oauth_clicked',
  'api_troubleshooting_oauth_failed',
  'launch_plan_viewed',
  'launch_plan_key_activation_clicked',
  'launch_plan_checkout_clicked',
  'launch_plan_managed_access_clicked',
  'launch_plan_conversion_clicked',
  'launch_plan_magic_link_requested',
  'launch_plan_magic_link_sent',
  'launch_plan_magic_link_failed',
  'launch_plan_oauth_clicked',
  'launch_plan_oauth_failed',
  'gateway_compare_viewed',
  'gateway_compare_key_activation_clicked',
  'gateway_compare_checkout_clicked',
  'gateway_compare_account_clicked',
  'gateway_compare_pricing_clicked',
  'gateway_compare_migration_clicked',
  'gateway_compare_calculator_clicked',
  'gateway_compare_managed_access_clicked',
  'gateway_compare_oauth_clicked',
  'gateway_compare_oauth_failed',
  'gateway_compare_magic_link_requested',
  'gateway_compare_magic_link_sent',
  'gateway_compare_magic_link_failed',
  'content_article_viewed',
  'content_article_inline_offer_viewed',
  'content_article_activation_dock_viewed',
  'content_article_quickstart_clicked',
  'content_article_key_activation_clicked',
  'content_article_key_recovery_clicked',
  'content_article_checkout_clicked',
  'content_article_snippet_copied',
  'content_article_magic_link_requested',
  'content_article_magic_link_sent',
  'content_article_magic_link_failed',
  'content_article_oauth_clicked',
  'content_article_oauth_failed',
  'content_article_compare_clicked',
  'content_article_calculator_clicked',
  'content_article_managed_access_clicked',
  'content_article_launch_plan_clicked',
  'content_article_ollama_clicked',
  'content_article_pricing_clicked',
  'content_article_status_clicked',
  'content_article_codex_clicked',
  'content_article_github_clicked',
  'model_catalog_viewed',
  'model_catalog_search_bucketed',
  'model_catalog_filter_clicked',
  'model_catalog_key_activation_clicked',
  'model_catalog_key_recovery_clicked',
  'model_catalog_account_clicked',
  'model_catalog_quickstart_clicked',
  'model_catalog_pricing_clicked',
  'model_catalog_codex_clicked',
  'model_catalog_gateway_clicked',
  'model_catalog_json_clicked',
  'model_catalog_magic_link_requested',
  'model_catalog_magic_link_sent',
  'model_catalog_magic_link_failed',
  'model_catalog_oauth_clicked',
  'model_catalog_oauth_failed',
  'model_catalog_setup_next_clicked',
  'account_viewed',
  'account_plan_selected',
  'account_signup_options_shown',
  'auth_provider_state_checked',
  'account_auto_oauth_skipped',
  'account_auto_oauth_started',
  'account_key_recovery_viewed',
  'account_setup_handoff_viewed',
  'account_oauth_clicked',
  'account_oauth_failed',
  'account_login_submitted',
  'account_login_succeeded',
  'account_login_failed',
  'account_signup_submitted',
  'account_signup_succeeded',
  'account_signup_failed',
  'account_magic_link_requested',
  'account_magic_link_sent',
  'account_magic_link_failed',
  'login_key_recovery_shown',
  'login_key_recovery_landed',
  'login_key_recovery_clicked',
  'login_key_recovery_same_account_prompted',
  'login_key_recovery_session_redirected',
  'account_activation_nudge_shown',
  'account_activation_nudge_clicked',
  'account_activation_nudge_dismissed',
  'account_next_action_shown',
  'account_next_action_clicked',
  'operator_no_key_followup_copied',
  'operator_no_key_followup_batch_copied',
  'operator_no_key_followup_csv_copied',
  'operator_no_key_followup_mailto_opened',
  'operator_no_key_followup_send_dry_run',
  'operator_no_key_followup_sent',
  'operator_no_key_followup_send_failed',
  'account_email_verification_resend_clicked',
  'account_email_verification_resent',
  'account_preauth_setup_next_clicked',
  'login_wallet_clicked',
  'login_wallet_connected',
  'account_intent_primary_clicked',
  'account_checkout_clicked',
  'account_checkout_key_first_redirected',
  'account_checkout_unavailable',
  'account_checkout_failed',
  'account_checkout_returned',
  'account_billing_portal_clicked',
  'account_billing_portal_failed',
  'account_billing_portal_returned',
  'account_crypto_intent_clicked',
  'account_crypto_intent_created',
  'account_crypto_intent_failed',
  'account_crypto_status_clicked',
  'account_crypto_status_checked',
  'account_crypto_status_failed',
  'account_usage_upgrade_clicked',
  'account_api_key_create_clicked',
  'account_api_key_created',
  'account_api_key_create_failed',
  'account_key_recovery_key_created',
  'account_api_key_revoke_clicked',
  'account_api_key_revoked',
  'account_api_key_revoke_failed',
  'account_key_verify_clicked',
  'account_key_verified',
  'account_first_request_clicked',
  'account_first_request_succeeded',
  'account_post_key_verify_clicked',
  'account_post_key_first_request_clicked',
  'account_post_key_codex_copied',
  'account_snippet_copied',
  'account_support_context_copied',
  'billing_payment_recovery_clicked',
  'billing_account_clicked',
  'billing_pricing_clicked',
  'billing_support_clicked',
  'billing_quickstart_clicked',
  'billing_status_clicked',
  'billing_troubleshooting_clicked',
  'status_key_recovery_clicked',
  'support_key_recovery_clicked',
  'landing_viewed',
  'landing_account_clicked',
  'landing_key_first_direct_clicked',
  'landing_key_recovery_clicked',
  'landing_oauth_clicked',
  'landing_oauth_failed',
  'landing_magic_link_requested',
  'landing_magic_link_sent',
  'landing_magic_link_failed',
  'landing_activation_nudge_shown',
  'landing_activation_nudge_clicked',
  'landing_activation_nudge_dismissed',
  'landing_pricing_clicked',
  'landing_billing_clicked',
  'landing_quickstart_clicked',
  'landing_post_copy_prompt_shown',
  'landing_setup_next_clicked',
  'landing_integrations_clicked',
  'landing_status_clicked',
  'landing_gateway_compare_clicked',
  'landing_article_clicked',
  'landing_models_clicked',
  'landing_calculator_clicked',
  'landing_managed_access_clicked',
  'landing_security_clicked',
  'landing_analytics_clicked',
  'landing_login_clicked',
  'landing_github_clicked',
  'landing_waitlist_submitted',
]);

const ALLOWED_PLANS = new Set(['lite', 'pro', 'max', 'trial', 'manual']);
const ALLOWED_METADATA_KEYS = new Set([
  'score',
  'volumeBucket',
  'riskLevel',
  'savingsBucket',
  'source',
  'sourceSurface',
  'articlePath',
  'articleTitle',
  'intent',
  'button',
  'state',
  'billing',
  'enabledProviders',
  'disabledProviders',
  'githubEnabled',
  'oauthProviderCount',
  'utmSource',
  'utmMedium',
  'utmCampaign',
  'utmContent',
  'referrerHost',
  'landingPath',
  'setupSource',
  'deployment',
  'monthlyVolume',
  'providerAccess',
  'targetProviderFamily',
  'commercialPreference',
  'supportNeed',
  'targetLaunchWindow',
  'modelFamily',
  'queryBucket',
  'catalogSource',
  'resultCount',
  'snippet',
]);

const DEFAULT_ALLOWED_ORIGIN_HOSTS = new Set([
  'sagerouter.dev',
  'www.sagerouter.dev',
  'app.sagerouter.dev',
  'localhost',
  '127.0.0.1',
]);

const json = (body, status = 200, headers = {}) => new Response(JSON.stringify(body), {
  status,
  headers: { 'content-type': 'application/json; charset=utf-8', ...headers },
});

const sanitizedUrl = (value) => {
  if (!value) return null;
  try {
    const url = new URL(value, 'https://sagerouter.dev');
    return `${url.origin}${url.pathname}`;
  } catch {
    return null;
  }
};

const sanitizePlan = (value) => {
  const plan = String(value || '').trim().toLowerCase();
  return ALLOWED_PLANS.has(plan) ? plan : null;
};

const sanitizeMetadata = (value) => {
  const source = value && typeof value === 'object' && !Array.isArray(value) ? value : {};
  const out = {};
  for (const key of ALLOWED_METADATA_KEYS) {
    if (!Object.prototype.hasOwnProperty.call(source, key)) continue;
    const raw = source[key];
    if (raw === null || raw === undefined) continue;
    if (typeof raw === 'number' && Number.isFinite(raw)) {
      out[key] = raw;
    } else if (typeof raw === 'boolean') {
      out[key] = raw;
    } else {
      out[key] = String(raw).slice(0, 80);
    }
  }
  return out;
};

const smokeValue = (value) => {
  const normalized = String(value ?? '').trim().toLowerCase();
  return normalized === 'true' || normalized === '1' || normalized === 'yes' || normalized === 'smoke' || normalized === 'test';
};

const isSmokePayload = (payload) => {
  const metadata = payload?.metadata && typeof payload.metadata === 'object' && !Array.isArray(payload.metadata)
    ? payload.metadata
    : {};
  return smokeValue(metadata.smoke)
    || smokeValue(metadata.test)
    || smokeValue(metadata.button)
    || smokeValue(metadata.state)
    || String(payload?.sourcePage || '').toLowerCase().includes('smoke=1');
};

const attributionValue = (value) => {
  const sanitized = String(value || '')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9._/-]+/g, '-')
    .slice(0, 80);
  return sanitized || null;
};

const configuredAllowedOrigins = (env) => String(env.SAGEROUTER_FUNNEL_ALLOWED_ORIGINS || '')
  .split(',')
  .map((origin) => origin.trim().replace(/\/$/, '').toLowerCase())
  .filter(Boolean);

const originForHeader = (value) => {
  if (!value) return null;
  try {
    const url = new URL(value);
    return `${url.protocol}//${url.host}`.toLowerCase();
  } catch {
    return null;
  }
};

const originForRequest = (request) => {
  return originForHeader(request.headers.get('origin'));
};

const allowedOrigin = (origin, env) => {
  if (!origin) return null;
  const configured = configuredAllowedOrigins(env);
  if (configured.includes(origin)) return origin;
  try {
    const url = new URL(origin);
    if (DEFAULT_ALLOWED_ORIGIN_HOSTS.has(url.hostname)) return origin;
    if (url.hostname.endsWith('.sage-router-web.pages.dev')) return origin;
    return null;
  } catch {
    return null;
  }
};

const corsHeadersForOrigin = (origin) => ({
  'access-control-allow-origin': origin,
  'access-control-allow-methods': 'GET,POST,OPTIONS',
  'access-control-allow-headers': 'content-type',
  'access-control-max-age': '86400',
  vary: 'Origin',
});

const funnelConfig = (env) => {
  const supabaseUrl = env.SAGEROUTER_SUPABASE_URL || env.SUPABASE_URL;
  const serviceKey = env.SAGEROUTER_SUPABASE_SERVICE_ROLE || env.SUPABASE_SERVICE_ROLE_KEY;
  return { supabaseUrl, serviceKey };
};

const insert = async (supabaseUrl, serviceKey, record) => fetch(`${supabaseUrl.replace(/\/$/, '')}/rest/v1/sage_router_funnel_events`, {
  method: 'POST',
  headers: {
    apikey: serviceKey,
    authorization: `Bearer ${serviceKey}`,
    'content-type': 'application/json',
    prefer: 'return=minimal',
  },
  body: JSON.stringify(record),
});

export async function onRequestOptions({ request, env }) {
  const requestOrigin = originForRequest(request);
  const acceptedOrigin = allowedOrigin(requestOrigin, env);
  if (!acceptedOrigin) return json({ error: 'origin_not_allowed' }, 403);
  return new Response(null, {
    status: 204,
    headers: corsHeadersForOrigin(acceptedOrigin),
  });
}

export async function onRequestGet({ env }) {
  const { supabaseUrl, serviceKey } = funnelConfig(env);
  if (!supabaseUrl || !serviceKey) return json({ ok: false, error: 'supabase_not_configured' }, 500);
  return json({
    ok: true,
    service: 'sage-router-funnel-event',
    storage: 'supabase',
    primaryTable: 'sage_router_funnel_events',
    allowedEvents: Array.from(ALLOWED_EVENTS).sort(),
    allowedPlans: Array.from(ALLOWED_PLANS).sort(),
    privacy: {
      containsEmails: false,
      promptsStored: false,
      messageBodiesStored: false,
      containsApiKeys: false,
      containsProviderCredentials: false,
    },
    writeGuard: {
      browserOriginRequired: true,
      refererFallbackAccepted: false,
      allowedHosts: Array.from(DEFAULT_ALLOWED_ORIGIN_HOSTS).sort(),
      previewHostSuffix: '.sage-router-web.pages.dev',
      configurableOriginsEnv: 'SAGEROUTER_FUNNEL_ALLOWED_ORIGINS',
    },
    dataQuality: {
      smokeEventsPersisted: false,
      smokeDetection: ['metadata.smoke', 'metadata.test', 'metadata.button=smoke', 'metadata.state=smoke', 'sourcePage.smoke=1'],
    },
  });
}

export async function onRequestPost({ request, env }) {
  const requestOrigin = originForRequest(request);
  const acceptedOrigin = allowedOrigin(requestOrigin, env);
  if (!acceptedOrigin) return json({ error: 'origin_not_allowed' }, 403);

  let payload;
  try {
    payload = await request.json();
  } catch {
    return json({ error: 'invalid_json' }, 400);
  }

  const event = String(payload.event || '').trim().toLowerCase();
  if (!ALLOWED_EVENTS.has(event)) return json({ error: 'invalid_event' }, 400);
  if (isSmokePayload(payload)) {
    return json({ ok: true, skipped: 'smoke' }, 200, corsHeadersForOrigin(acceptedOrigin));
  }

  const { supabaseUrl, serviceKey } = funnelConfig(env);
  if (!supabaseUrl || !serviceKey) return json({ error: 'supabase_not_configured' }, 500);

  const record = {
    event,
    plan: sanitizePlan(payload.plan),
    source_page: sanitizedUrl(payload.sourcePage) || 'https://sagerouter.dev',
    target: sanitizedUrl(payload.target),
    metadata: {
      ...sanitizeMetadata(payload.metadata),
      utmSource: attributionValue(payload.metadata?.utmSource),
      utmMedium: attributionValue(payload.metadata?.utmMedium),
      utmCampaign: attributionValue(payload.metadata?.utmCampaign),
      referrerHost: attributionValue(payload.metadata?.referrerHost),
      landingPath: attributionValue(payload.metadata?.landingPath),
      user_agent: String(request.headers.get('user-agent') || '').slice(0, 160) || null,
      referer: sanitizedUrl(request.headers.get('referer')),
      origin: sanitizedUrl(request.headers.get('origin')),
    },
  };

  const response = await insert(supabaseUrl, serviceKey, record);
  if (!response.ok) {
    const details = await response.text();
    return json({ error: 'supabase_insert_failed', details }, 502, corsHeadersForOrigin(acceptedOrigin));
  }

  return json({ ok: true }, 200, corsHeadersForOrigin(acceptedOrigin));
}
