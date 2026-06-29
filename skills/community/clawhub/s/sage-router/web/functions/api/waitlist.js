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

const insert = async (supabaseUrl, serviceKey, table, record) => fetch(`${supabaseUrl.replace(/\/$/, '')}/rest/v1/${table}`, {
  method: 'POST',
  headers: {
    apikey: serviceKey,
    authorization: `Bearer ${serviceKey}`,
    'content-type': 'application/json',
    prefer: 'return=minimal',
  },
  body: JSON.stringify(record),
});

const waitlistConfig = (env) => {
  const supabaseUrl = env.SAGEROUTER_SUPABASE_URL || env.SUPABASE_URL;
  const serviceKey = env.SAGEROUTER_SUPABASE_SERVICE_ROLE || env.SUPABASE_SERVICE_ROLE_KEY;
  const turnstileSecret = env.SAGEROUTER_TURNSTILE_SECRET_KEY || env.TURNSTILE_SECRET_KEY || '';
  const turnstileSiteKey = env.SAGEROUTER_TURNSTILE_SITE_KEY || env.TURNSTILE_SITE_KEY || '';
  return { supabaseUrl, serviceKey, turnstileSecret, turnstileSiteKey };
};

const clientIp = (request) => {
  const cfIp = request.headers.get('cf-connecting-ip');
  if (cfIp) return cfIp;
  const forwarded = request.headers.get('x-forwarded-for') || '';
  return forwarded.split(',')[0].trim();
};

const sanitizedUrl = (value) => {
  if (!value) return null;
  try {
    const url = new URL(value);
    return `${url.origin}${url.pathname}`;
  } catch {
    return null;
  }
};

const configuredAllowedOrigins = (env) => String(env.SAGEROUTER_WAITLIST_ALLOWED_ORIGINS || '')
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

const sanitizeChoice = (value, allowed, fallback = null) => {
  const normalized = String(value || '').trim().toLowerCase();
  return allowed.has(normalized) ? normalized : fallback;
};

const validateTurnstile = async ({ token, request, turnstileSecret }) => {
  if (!turnstileSecret) return { ok: true, configured: false };
  if (!token) return { ok: false, status: 403, error: 'turnstile_required' };
  const randomUUID = globalThis.crypto?.randomUUID?.bind(globalThis.crypto);

  let response;
  try {
    response = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        secret: turnstileSecret,
        response: token,
        remoteip: clientIp(request) || undefined,
        idempotency_key: randomUUID ? randomUUID() : undefined,
      }),
    });
  } catch {
    return { ok: false, status: 502, error: 'turnstile_unavailable' };
  }

  let body = {};
  try {
    body = await response.json();
  } catch {
    return { ok: false, status: 502, error: 'turnstile_invalid_response' };
  }

  if (!response.ok || body.success !== true) {
    return {
      ok: false,
      status: 403,
      error: 'turnstile_failed',
      codes: Array.isArray(body['error-codes']) ? body['error-codes'].slice(0, 5) : [],
    };
  }

  return { ok: true, configured: true };
};

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
  const { supabaseUrl, serviceKey, turnstileSecret, turnstileSiteKey } = waitlistConfig(env);
  if (!supabaseUrl || !serviceKey) return json({ ok: false, error: 'supabase_not_configured' }, 500);
  return json({
    ok: true,
    service: 'sage-router-waitlist',
    storage: 'supabase',
    primaryTable: 'sage_router_waitlist',
    fallbackTable: 'funnel_leads',
    turnstileRequired: Boolean(turnstileSecret),
    turnstileSiteKey: turnstileSecret ? turnstileSiteKey || null : null,
    turnstileReady: !turnstileSecret || Boolean(turnstileSiteKey),
    allowedQualificationBuckets: {
      deployment: ['hosted-edge', 'tailnet-private', 'hybrid', 'unsure'],
      monthlyVolume: ['under-50k', '50k-200k', '200k-1m', '1m-plus'],
      providerAccess: ['byok', 'local-ollama', 'enterprise-contracts', 'needs-managed-access'],
      targetProviderFamily: ['mixed-frontier', 'ollama', 'openai', 'anthropic', 'byok-compatible'],
      commercialPreference: ['one-subscription', 'byok-plus-routing', 'private-contract'],
      supportNeed: ['implementation-support', 'private-deployment', 'migration-help', 'managed-provider-review'],
      targetLaunchWindow: ['this-week', 'this-month', 'this-quarter', 'exploring'],
      intent: ['max-implementation', 'private-deployment', 'gateway-migration', 'one-subscription', 'ollama', 'openai', 'anthropic'],
    },
    writeGuard: {
      browserOriginRequired: true,
      refererFallbackAccepted: false,
      allowedHosts: Array.from(DEFAULT_ALLOWED_ORIGIN_HOSTS).sort(),
      previewHostSuffix: '.sage-router-web.pages.dev',
      configurableOriginsEnv: 'SAGEROUTER_WAITLIST_ALLOWED_ORIGINS',
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

  const email = String(payload.email || '').trim().toLowerCase();
  const company = String(payload.company || '').trim().slice(0, 200);
  const website = String(payload.website || '').trim();
  const interestValue = String(payload.interest || 'general').trim().toLowerCase();
  const interest = /^[a-z0-9-]{1,80}$/.test(interestValue) ? interestValue : 'general';
  const deployment = sanitizeChoice(payload.deployment, new Set(['hosted-edge', 'tailnet-private', 'hybrid', 'unsure']));
  const monthlyVolume = sanitizeChoice(payload.monthlyVolume, new Set(['under-50k', '50k-200k', '200k-1m', '1m-plus']));
  const providerAccess = sanitizeChoice(payload.providerAccess, new Set(['byok', 'local-ollama', 'enterprise-contracts', 'needs-managed-access']));
  const targetProviderFamily = sanitizeChoice(payload.targetProviderFamily, new Set(['mixed-frontier', 'ollama', 'openai', 'anthropic', 'byok-compatible']));
  const commercialPreference = sanitizeChoice(payload.commercialPreference, new Set(['one-subscription', 'byok-plus-routing', 'private-contract']));
  const supportNeed = sanitizeChoice(payload.supportNeed, new Set(['implementation-support', 'private-deployment', 'migration-help', 'managed-provider-review']));
  const targetLaunchWindow = sanitizeChoice(payload.targetLaunchWindow, new Set(['this-week', 'this-month', 'this-quarter', 'exploring']));
  const intent = sanitizeChoice(payload.intent, new Set(['max-implementation', 'private-deployment', 'gateway-migration', 'one-subscription', 'ollama', 'openai', 'anthropic']));
  const sourcePage = sanitizedUrl(payload.sourcePage) || 'https://sagerouter.dev';
  const turnstileToken = String(payload.turnstileToken || payload['cf-turnstile-response'] || '').trim();

  if (website) return json({ ok: true }, 200, corsHeadersForOrigin(acceptedOrigin));
  if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return json({ error: 'invalid_email' }, 400, corsHeadersForOrigin(acceptedOrigin));
  }

  const { supabaseUrl, serviceKey, turnstileSecret } = waitlistConfig(env);
  if (!supabaseUrl || !serviceKey) return json({ error: 'supabase_not_configured' }, 500, corsHeadersForOrigin(acceptedOrigin));
  const turnstile = await validateTurnstile({ token: turnstileToken, request, turnstileSecret });
  if (!turnstile.ok) return json({ error: turnstile.error, codes: turnstile.codes || [] }, turnstile.status, corsHeadersForOrigin(acceptedOrigin));

  const metadata = {
    product: 'sage-router',
    form: 'site_waitlist',
    interest,
    user_agent: String(request.headers.get('user-agent') || '').slice(0, 300) || null,
    referer: sanitizedUrl(request.headers.get('referer')),
    origin: sanitizedUrl(request.headers.get('origin')),
    turnstile: turnstile.configured ? 'verified' : 'not_configured',
    deployment,
    monthly_volume: monthlyVolume,
    provider_access: providerAccess,
    target_provider_family: targetProviderFamily,
    commercial_preference: commercialPreference,
    support_need: supportNeed,
    target_launch_window: targetLaunchWindow,
    intent,
  };

  const waitlistRecord = {
    source_page: sourcePage,
    email,
    company: company || null,
    metadata,
  };

  let response = await insert(supabaseUrl, serviceKey, 'sage_router_waitlist', waitlistRecord);

  if (response.status === 409) return json({ ok: true }, 200, corsHeadersForOrigin(acceptedOrigin));

  if (!response.ok && response.status === 404) {
    response = await insert(supabaseUrl, serviceKey, 'funnel_leads', {
      ...waitlistRecord,
      cta_type: 'sage_router_waitlist',
    });
  }

  if (response.status === 409) return json({ ok: true }, 200, corsHeadersForOrigin(acceptedOrigin));

  if (!response.ok) {
    const details = await response.text();
    return json({ error: 'supabase_insert_failed', details }, 502, corsHeadersForOrigin(acceptedOrigin));
  }

  return json({ ok: true }, 200, corsHeadersForOrigin(acceptedOrigin));
}
