const SUPABASE_URL = 'https://awtangrlqqsdpksarhwo.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3dGFuZ3JscXFzZHBrc2FyaHdvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMwMTYzNzEsImV4cCI6MjA4ODU5MjM3MX0.U7TmEJMgYMH0rR8tTWFQ2tzReO5syRwnI3Ytg-BbDaw';
let sageRouterUrl = window.SAGE_ROUTER_API_URL || 'https://api.sagerouter.dev';
let openaiBaseUrl = `${sageRouterUrl}/v1`;
let anthropicBaseUrl = sageRouterUrl;
const DEFAULT_PLAN_ORDER = ['lite', 'pro', 'max'];
const SELECTED_PLAN_STORAGE_KEY = 'sage_router_selected_plan';
const START_ACTION_STORAGE_KEY = 'sage_router_start_action';
const AUTO_CHECKOUT_ATTEMPT_STORAGE_KEY = 'sage_router_auto_checkout_attempt';
const AUTO_KEY_ATTEMPT_STORAGE_KEY = 'sage_router_auto_key_attempt';
const AUTO_OAUTH_ATTEMPT_STORAGE_KEY = 'sage_router_auto_oauth_attempt';
const KEY_RECOVERY_EMAIL_FOCUS_STORAGE_KEY = 'sage_router_key_recovery_email_focus';
const KEY_RECOVERY_SIGNED_IN_PROMPT_STORAGE_KEY = 'sage_router_key_recovery_signed_in_prompt';
const ONBOARDING_CONTEXT_STORAGE_KEY = 'sage_router_onboarding_context';
const ACCOUNT_AUTH_NUDGE_STORAGE_KEY = 'sage_router_account_auth_nudge_dismissed_until';
const FALLBACK_PLANS = {
  lite: { name: 'Lite', price: '$6/month', limits: { monthlyRequests: 10000, rateLimitPerMinute: 60 }, features: ['agent-native routing', 'API keys', 'usage analytics'] },
  pro: { name: 'Pro', price: '$30/month', limits: { monthlyRequests: 50000, rateLimitPerMinute: 180 }, features: ['frontier routing', 'agentic tool-use preference', 'Fusion synthesis', 'analytics snapshots'] },
  max: { name: 'Max', price: '$72/month', limits: { monthlyRequests: 200000, rateLimitPerMinute: 600 }, features: ['highest quality routing', 'Fusion synthesis budget', 'team/automation use'] },
};

const sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
const $ = (id) => document.getElementById(id);
const set = (id, text) => {
  const el = $(id);
  if (el) el.textContent = text;
};
const setAuthStatus = (text, mirrorIntent = false) => {
  set('auth-status', text);
  if (mirrorIntent) set('intent-email-status', text);
};
const show = (id, visible) => {
  const el = $(id);
  if (el) el.classList.toggle('hidden', !visible);
};
const emailInputValue = (preferIntent = false) => {
  const primary = preferIntent ? $('intent-email') : $('email');
  const secondary = preferIntent ? $('email') : $('intent-email');
  return primary?.value.trim() || secondary?.value.trim() || '';
};
const syncEmailInputs = (value) => {
  const email = String(value || '').trim();
  if (!email) return;
  const accountEmail = $('email');
  const intentEmail = $('intent-email');
  if (accountEmail && accountEmail.value.trim() !== email) accountEmail.value = email;
  if (intentEmail && intentEmail.value.trim() !== email) intentEmail.value = email;
};
const focusEmailInput = (preferIntent = false) => {
  const target = preferIntent ? ($('intent-email') || $('email')) : ($('email') || $('intent-email'));
  target?.scrollIntoView?.({ behavior: 'smooth', block: 'center' });
  target?.focus?.();
};
const setElementBusy = (el, busy, label = '') => {
  if (!el) return;
  if (busy) {
    if (!el.dataset.idleText) el.dataset.idleText = el.textContent;
    el.disabled = true;
    if (label) el.textContent = label;
  } else {
    el.disabled = false;
    el.textContent = el.dataset.idleText || el.textContent;
    delete el.dataset.idleText;
  }
};
const setBusy = (id, busy, label = '') => setElementBusy($(id), busy, label);
const esc = (v) => String(v ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const fmtNumber = (value) => Number.isFinite(Number(value)) ? Number(value).toLocaleString() : '';
const OAUTH_LABELS = { discord: 'Discord', github: 'GitHub', google: 'Google' };
const OAUTH_PROVIDER_ORDER = ['github', 'google', 'discord'];

function canonicalAccountPageUrl() {
  const configured = String(window.SAGE_ROUTER_APP_URL || '').replace(/\/$/, '');
  if (configured) return `${configured}/account.html`;
  if (['localhost', '127.0.0.1'].includes(window.location.hostname)) return `${window.location.origin}/account.html`;
  return 'https://app.sagerouter.dev/account.html';
}
const ACCOUNT_PAGE_URL = canonicalAccountPageUrl();

function attributionValue(value) {
  const sanitized = String(value || '')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9._/-]+/g, '-')
    .slice(0, 80);
  return sanitized || null;
}

function currentReferrerHost() {
  try {
    const referrer = document.referrer ? new URL(document.referrer) : null;
    return referrer && referrer.host !== window.location.host ? attributionValue(referrer.host) : null;
  } catch (_error) {
    return null;
  }
}

function onboardingContext(extra = {}) {
  const params = new URLSearchParams(window.location.search || '');
  return {
    sage_router_onboarding: true,
    signup_source: extra.source || 'account',
    auth_method: extra.authMethod || null,
    selected_plan: normalizePlan(extra.plan || selectedPlan) || null,
    utm_source: attributionValue(params.get('utm_source') || params.get('utmSource')),
    utm_medium: attributionValue(params.get('utm_medium') || params.get('utmMedium')),
    utm_campaign: attributionValue(params.get('utm_campaign') || params.get('utmCampaign')),
    utm_content: attributionValue(params.get('utm_content') || params.get('utmContent')),
    source_surface: attributionValue(params.get('source_surface') || params.get('sourceSurface')),
    setup_source: attributionValue(params.get('setup') || params.get('setupSource')),
    referrer_host: currentReferrerHost(),
    landing_path: window.location.pathname,
  };
}

function rememberOnboardingContext(context) {
  try {
    window.localStorage?.setItem(ONBOARDING_CONTEXT_STORAGE_KEY, JSON.stringify(context));
  } catch (_error) {
    // Onboarding can continue without local persistence.
  }
  return context;
}

function normalizePlan(plan) {
  const normalized = String(plan || '').trim().toLowerCase();
  return DEFAULT_PLAN_ORDER.includes(normalized) ? normalized : '';
}

function storedPlan() {
  try {
    return normalizePlan(window.localStorage?.getItem(SELECTED_PLAN_STORAGE_KEY));
  } catch (_error) {
    return '';
  }
}

function rememberSelectedPlan(plan) {
  const normalized = normalizePlan(plan);
  if (!normalized) return '';
  try {
    window.localStorage?.setItem(SELECTED_PLAN_STORAGE_KEY, normalized);
  } catch (_error) {
    // Storage can be unavailable in private or locked-down browser sessions.
  }
  return normalized;
}

function requestedPlanFromUrl() {
  const params = new URLSearchParams(window.location.search || '');
  return normalizePlan(params.get('plan'));
}

function normalizeStartAction(action) {
  const normalized = String(action || '').trim().toLowerCase().replace(/[-\s]+/g, '_');
  return ['checkout', 'create_key'].includes(normalized) ? normalized : '';
}

function requestedStartActionFromUrl() {
  const params = new URLSearchParams(window.location.search || '');
  return normalizeStartAction(params.get('start') || params.get('action'));
}

function inferredStartActionFromReferrer() {
  try {
    const referrer = document.referrer ? new URL(document.referrer) : null;
    if (!referrer) return '';
    const trustedMarketingHosts = new Set(['sagerouter.dev', 'www.sagerouter.dev']);
    return trustedMarketingHosts.has(referrer.hostname) ? 'checkout' : '';
  } catch (_error) {
    return '';
  }
}

function requestedAuthProviderFromUrl() {
  const params = new URLSearchParams(window.location.search || '');
  const provider = String(params.get('auth') || params.get('provider') || '').trim().toLowerCase();
  return OAUTH_PROVIDER_ORDER.includes(provider) ? provider : '';
}

function requestedEmailAuthFromUrl() {
  const params = new URLSearchParams(window.location.search || '');
  const auth = String(params.get('auth') || params.get('provider') || '').trim().toLowerCase();
  return ['email', 'password', 'email_password', 'password_fallback', 'fallback', 'none'].includes(auth);
}

function requestedKeyRecoveryStateFromUrl() {
  const params = new URLSearchParams(window.location.search || '');
  if (requestedEmailAuthFromUrl()) return 'same_email';
  return requestedAuthProviderFromUrl() || String(params.get('auth') || params.get('provider') || 'no_auth_provider').trim().toLowerCase() || 'no_auth_provider';
}

function requestedSetupSourceFromUrl() {
  const params = new URLSearchParams(window.location.search || '');
  return attributionValue(params.get('setup') || params.get('setupSource'));
}

function requestedSourceSurfaceFromUrl() {
  const params = new URLSearchParams(window.location.search || '');
  return attributionValue(params.get('source_surface') || params.get('sourceSurface'));
}

function storedStartAction() {
  try {
    return normalizeStartAction(window.sessionStorage?.getItem(START_ACTION_STORAGE_KEY));
  } catch (_error) {
    return '';
  }
}

function rememberStartAction(action) {
  const normalized = normalizeStartAction(action);
  try {
    if (normalized) window.sessionStorage?.setItem(START_ACTION_STORAGE_KEY, normalized);
    else window.sessionStorage?.removeItem(START_ACTION_STORAGE_KEY);
  } catch (_error) {
    // Checkout intent persistence is best-effort.
  }
  return normalized;
}

function autoCheckoutAttemptKey(plan = selectedPlan) {
  return `${AUTO_CHECKOUT_ATTEMPT_STORAGE_KEY}:${normalizePlan(plan) || 'unknown'}`;
}

function hasAutoCheckoutAttempted(plan = selectedPlan) {
  try {
    return window.sessionStorage?.getItem(autoCheckoutAttemptKey(plan)) === '1';
  } catch (_error) {
    return false;
  }
}

function markAutoCheckoutAttempted(plan = selectedPlan) {
  try {
    window.sessionStorage?.setItem(autoCheckoutAttemptKey(plan), '1');
  } catch (_error) {
    // A missing marker only risks a repeated prompt; checkout still requires Stripe confirmation.
  }
}

function autoKeyAttemptKey(plan = selectedPlan) {
  return `${AUTO_KEY_ATTEMPT_STORAGE_KEY}:${normalizePlan(plan) || 'unknown'}`;
}

function hasAutoKeyAttempted(plan = selectedPlan) {
  try {
    return window.sessionStorage?.getItem(autoKeyAttemptKey(plan)) === '1';
  } catch (_error) {
    return false;
  }
}

function markAutoKeyAttempted(plan = selectedPlan) {
  try {
    window.sessionStorage?.setItem(autoKeyAttemptKey(plan), '1');
  } catch (_error) {
  }
}

function autoOauthAttemptKey(provider = 'github', plan = selectedPlan) {
  return `${AUTO_OAUTH_ATTEMPT_STORAGE_KEY}:${provider}:${normalizePlan(plan) || 'unknown'}:${pendingStartAction || 'none'}`;
}

function hasAutoOauthAttempted(provider = 'github', plan = selectedPlan) {
  try {
    return window.sessionStorage?.getItem(autoOauthAttemptKey(provider, plan)) === '1';
  } catch (_error) {
    return false;
  }
}

function markAutoOauthAttempted(provider = 'github', plan = selectedPlan) {
  try {
    window.sessionStorage?.setItem(autoOauthAttemptKey(provider, plan), '1');
  } catch (_error) {
  }
}

function keyRecoverySessionKey(prefix) {
  return `${prefix}:${normalizePlan(selectedPlan) || 'unknown'}:${requestedKeyRecoveryStateFromUrl()}`;
}

function hasKeyRecoveryMarker(prefix) {
  try {
    return window.sessionStorage?.getItem(keyRecoverySessionKey(prefix)) === '1';
  } catch (_error) {
    return false;
  }
}

function markKeyRecoveryMarker(prefix) {
  try {
    window.sessionStorage?.setItem(keyRecoverySessionKey(prefix), '1');
  } catch (_error) {
  }
}

function planDisplay(plan) {
  return plan ? plan.charAt(0).toUpperCase() + plan.slice(1) : 'Pro';
}

let selectedPlan = requestedPlanFromUrl() || storedPlan() || 'pro';
let pendingStartAction = rememberStartAction(requestedStartActionFromUrl() || inferredStartActionFromReferrer() || storedStartAction());
let availablePlans = FALLBACK_PLANS;
let billingMetadata = null;
let recommendedUpgradePlan = '';
let currentRawKey = '';
let lastManualPaymentIntentId = '';
let billingReturnHandled = false;
let keyVerifiedThisSession = false;
let lastNextActionShownKey = '';
let activationState = {
  signedIn: false,
  emailVerified: true,
  routingEnabled: false,
  keyCount: 0,
  keyVerified: false,
  requestCount: 0,
};

function accountPageUrlWithPlan(plan = selectedPlan, options = {}) {
  const url = new URL(ACCOUNT_PAGE_URL);
  const normalized = normalizePlan(plan);
  if (normalized) url.searchParams.set('plan', normalized);
  const start = normalizeStartAction(options.start || (options.preserveStart === false ? '' : pendingStartAction));
  if (start) url.searchParams.set('start', start);
  return url.toString();
}

let supportContextState = {
  plan: selectedPlan,
  status: 'signed_out',
  routingEnabled: false,
  usage: null,
};
let emailActionAllowed = true;
let verificationEmail = '';
let latestOauthExternalState = null;
let signupOptionsShownTracked = false;

function configuredStripePlans() {
  const configured = billingMetadata?.stripe?.configuredPlans || [];
  return Array.isArray(configured) ? configured.map(normalizePlan).filter(Boolean) : [];
}

function stripeCheckoutReadyForPlan(plan = selectedPlan) {
  const normalized = normalizePlan(plan);
  const stripe = billingMetadata?.stripe || {};
  const configured = configuredStripePlans();
  if (!normalized) return false;
  if (stripe.configured === false || stripe.checkoutReady === false) return false;
  if (configured.length && !configured.includes(normalized)) return false;
  if (availablePlans?.[normalized]?.stripeConfigured === false) return false;
  return true;
}

function stripeCheckoutUnavailableMessage(plan = selectedPlan) {
  const normalized = normalizePlan(plan) || selectedPlan;
  const stripe = billingMetadata?.stripe || {};
  const configured = configuredStripePlans();
  if (stripe.configured === false || stripe.checkoutReady === false) {
    return 'Stripe checkout is not ready yet. Use manual settlement or billing help.';
  }
  if (configured.length && !configured.includes(normalized)) {
    return `${planDisplay(normalized)} checkout is not configured yet. Use manual settlement or billing help.`;
  }
  if (availablePlans?.[normalized]?.stripeConfigured === false) {
    return `${planDisplay(normalized)} checkout is manual for this deployment. Use manual settlement or billing help.`;
  }
  return 'Stripe checkout is temporarily unavailable. Use manual settlement or billing help.';
}

function checkoutNeedsGeneratedKeyFirst() {
  return Boolean(activationState.signedIn && !activationState.keyCount && !hasSessionApiKey());
}

function renderKeyRecoveryDock() {
  const recoveryIntent = isKeyRecoveryIntent();
  const sameEmailRecovery = recoveryIntent && requestedEmailAuthFromUrl();
  show('key-recovery-dock', recoveryIntent && !activationState.signedIn);
  if (!recoveryIntent) return;
  set('key-recovery-dock-copy', sameEmailRecovery
    ? 'Same-email recovery requested. Use the exact email from signup, then this page will create the generated sk_sage setup key before checkout.'
    : 'Key recovery requested. Use the same GitHub/OAuth identity or email from signup, then this page creates the generated sk_sage setup key first.');
  set('key-recovery-dock-status', sameEmailRecovery
    ? 'Recommended: send the same-email magic link, then create the key before checkout.'
    : 'Recommended: use GitHub only if it is the same signup account; otherwise use email.');
  maybeFocusSameEmailRecovery();
}

function maybeFocusSameEmailRecovery() {
  if (!isKeyRecoveryIntent() || activationState.signedIn || !requestedEmailAuthFromUrl()) return;
  if (hasKeyRecoveryMarker(KEY_RECOVERY_EMAIL_FOCUS_STORAGE_KEY)) return;
  markKeyRecoveryMarker(KEY_RECOVERY_EMAIL_FOCUS_STORAGE_KEY);
  window.setTimeout(() => {
    focusEmailInput(true);
    set('intent-email-status', 'Enter the same signup email, then send the magic link to finish the setup key.');
    set('key-recovery-dock-status', 'Same-email setup is focused. Send the magic link, open it, then create the sk_sage key before checkout.');
    trackAccountFunnelEvent('account_key_recovery_email_field_auto', {
      button: 'same_email_recovery_focus',
      target: '#intent-email',
      state: 'same_email_recovery',
    });
  }, 300);
}

function renderAccountIntent() {
  const plan = availablePlans?.[selectedPlan] || {};
  const checkoutReady = stripeCheckoutReadyForPlan(selectedPlan);
  const planName = plan.name || planDisplay(selectedPlan);
  const price = plan.price || (planPriceAmount(plan) ? `$${planPriceAmount(plan)}/month` : '');
  const recoveryIntent = isKeyRecoveryIntent();
  const sameEmailRecovery = recoveryIntent && requestedEmailAuthFromUrl();
  const setupSource = requestedSetupSourceFromUrl();
  renderKeyRecoveryDock();
  show('intent-email-field', !activationState.signedIn);
  set('account-intent-title', recoveryIntent || setupSource ? 'Finish your Sage Router setup key' : `${planName} activation path selected`);
  set('account-intent-plan', price ? `${planName} · ${price}` : planName);
  set('account-intent-checkout', recoveryIntent ? 'Key first, checkout after' : (checkoutReady ? 'Stripe checkout ready' : 'Manual fallback available'));
  if (!activationState.signedIn) {
    set('account-intent-copy', setupSource
      ? 'Setup was copied before account creation. Continue with GitHub or email the setup link, then this page will create the generated sk_sage key first.'
      : recoveryIntent
      ? (sameEmailRecovery
        ? 'Same-email recovery requested. Enter the email used at signup so the magic link opens this existing account and creates the generated sk_sage setup key first. OAuth is available only if it is the same account.'
        : 'This recovery link is set to create the generated sk_sage setup key first. Continue with GitHub, or email yourself the setup link; checkout and routing unlock after the key exists.')
      : 'No provider key or credit card is required until your generated sk_sage key exists. Continue with an enabled OAuth provider, or enter your email for the API key setup link, then create the key first and complete checkout to unlock routing.');
    const intentButton = $('intent-primary');
    if (intentButton) intentButton.textContent = sameEmailRecovery ? 'Send same-email setup link' : (recoveryIntent || setupSource ? 'Email setup key link instead' : 'Email API key setup link');
    return;
  }
  if (!activationState.emailVerified) {
    set('account-intent-copy', activationState.keyCount > 0
      ? 'Your generated key is ready. Verify your email next so checkout and hosted routing can attach safely.'
      : recoveryIntent
      ? 'Key recovery link active. Create the sk_sage setup key now; checkout waits until after the key exists and email is verified.'
      : 'You are signed in. Create the generated key now; it will stay blocked from routing until email verification and checkout are complete.');
    const intentButton = $('intent-primary');
    if (intentButton) intentButton.textContent = activationState.keyCount > 0 ? 'Verify email next' : (recoveryIntent ? 'Create setup key now' : 'Create API key');
    return;
  }
  if (!activationState.routingEnabled) {
    set('account-intent-copy', activationState.keyCount > 0
      ? (checkoutReady
        ? 'Your generated key is ready. Complete the selected paid plan to unlock hosted routing for it.'
        : 'Your generated key is ready. Stripe checkout is not ready for this plan, so use manual settlement or billing help.')
      : recoveryIntent
      ? 'Key recovery link active. Create the sk_sage setup key now; checkout can happen after the key exists.'
      : 'You are signed in. Create an API key now, then complete checkout to unlock hosted routing for it.');
    const intentButton = $('intent-primary');
    if (intentButton) intentButton.textContent = activationState.keyCount > 0 ? (checkoutReady ? 'Continue to Stripe' : 'Open billing options') : (recoveryIntent ? 'Create setup key now' : 'Create API key');
    return;
  }
  set('account-intent-copy', 'Routing is active. Create or verify a generated sk_sage_* key, then send the quickstart request to record first usage.');
  const intentButton = $('intent-primary');
  if (intentButton) intentButton.textContent = activationState.keyCount > 0 ? 'Verify API key' : 'Create API key';
}

function maybePrimeSetupHandoffLanding() {
  const setupSource = requestedSetupSourceFromUrl();
  if (!setupSource) return;
  window.setTimeout(() => {
    trackAccountFunnelEvent('account_setup_handoff_viewed', {
      button: 'setup_handoff',
      target: '#intent-email',
      state: requestedSourceSurfaceFromUrl() || 'unknown',
      snippet: setupSource,
    });
    if (activationState.signedIn) return;
    set('intent-email-status', 'Setup copied. Continue with GitHub or send the setup link, then create the sk_sage key before checkout.');
    focusEmailInput(true);
  }, 300);
}

function updateBillingControls(status = '') {
  const checkoutReady = stripeCheckoutReadyForPlan(selectedPlan);
  const keyFirst = checkoutNeedsGeneratedKeyFirst();
  const portalReady = billingMetadata?.stripe?.billingPortalReady !== false;
  const checkout = $('stripe-checkout');
  const portal = $('stripe-portal');
  if (checkout) {
    checkout.disabled = !keyFirst && (!emailActionAllowed || !checkoutReady);
    checkout.textContent = keyFirst ? 'Create API key first' : 'Continue to Stripe';
    checkout.title = keyFirst
      ? 'Create the generated sk_sage setup key before checkout.'
      : (checkoutReady ? '' : stripeCheckoutUnavailableMessage(selectedPlan));
  }
  if (portal) {
    portal.disabled = !portalReady;
    portal.title = portalReady ? '' : 'Stripe billing management is not ready yet.';
  }
  const next = keyFirst
    ? 'Create API key first'
    : !emailActionAllowed
    ? 'Verify email first'
    : (checkoutReady ? (activationState.signedIn ? 'Continue to Stripe' : 'Sign in to continue to checkout') : 'Manual settlement available');
  set('plan-preview-next', next);
  renderAccountIntent();
  if (status) {
    set('billing-status', status);
  } else if (!checkoutReady && $('billing-status')) {
    set('billing-status', stripeCheckoutUnavailableMessage(selectedPlan));
  }
}

function applyLaunchMetadata(data) {
  if (!data) return;
  if (data.plans) {
    availablePlans = data.plans;
  }
  if (data.billing) {
    billingMetadata = data.billing;
  }
  sageRouterUrl = data.apiBaseUrl || sageRouterUrl;
  openaiBaseUrl = data.openaiBaseUrl || `${sageRouterUrl}/v1`;
  anthropicBaseUrl = data.anthropicBaseUrl || sageRouterUrl;
  set('openai-base-url', `OPENAI_BASE_URL=${openaiBaseUrl}`);
  set('anthropic-base-url', `ANTHROPIC_BASE_URL=${anthropicBaseUrl}`);
  if (data.maxActiveApiKeysPerCustomer) {
    set('key-limit-note', `Limit: ${data.maxActiveApiKeysPerCustomer} active keys per account.`);
  }
  renderPreauthPlanPreview(availablePlans);
  updateBillingControls();
}

function applyOauthButtons(external = {}, status = '') {
  if (!status) latestOauthExternalState = external;
  const enabledProviders = OAUTH_PROVIDER_ORDER.filter((provider) => external[provider] === true);
  const enabledLabels = new Set();
  const sameEmailRecovery = isKeyRecoveryIntent() && requestedEmailAuthFromUrl();
  const recommendedProvider = sameEmailRecovery ? '' : (enabledProviders[0] || '');
  const planName = planDisplay(selectedPlan);
  document.querySelectorAll('[data-oauth]').forEach((button) => {
    const provider = button.dataset.oauth;
    const enabled = external[provider] === true;
    const label = OAUTH_LABELS[provider] || provider;
    button.classList.toggle('hidden', !enabled);
    button.classList.toggle('recommended', enabled && provider === recommendedProvider && button.dataset.intentOauth === 'true');
    button.disabled = !enabled;
    if (button.dataset.intentOauth === 'true') {
      if (sameEmailRecovery && !activationState.signedIn) {
        button.textContent = `${label} only if same account`;
      } else if (isKeyRecoveryIntent() && !activationState.signedIn) {
        button.textContent = provider === recommendedProvider
          ? `Continue with ${label} to create setup key`
          : `${label} setup key`;
      } else {
        button.textContent = provider === recommendedProvider
          ? `Continue with ${label} for ${planName}`
          : `${label} for ${planName}`;
      }
    } else {
      button.textContent = label;
    }
    if (enabled) enabledLabels.add(label);
  });
  const labels = [...enabledLabels];
  set('oauth-status', oauthStatusText(external, labels, status));
  if (!activationState.signedIn && labels.length && !status) {
    set('intent-email-status', sameEmailRecovery
      ? 'Same-email recovery requested. Enter the original signup email; use OAuth only if it is the same account.'
      : isKeyRecoveryIntent()
      ? `Recommended: continue with ${labels[0]} to create the setup key now. Email setup link remains available.`
      : `Recommended: continue with ${labels[0]} for ${planName}. Email magic link remains available.`);
  }
}

function oauthStatusText(external = {}, enabledLabels = [], status = '') {
  if (status) return status;
  if (isKeyRecoveryIntent() && requestedEmailAuthFromUrl()) {
    return enabledLabels.length
      ? 'Same-email recovery requested. OAuth is available only if it matches the original signup account.'
      : 'Same-email recovery requested. Use magic link or password to recover the setup-key flow.';
  }
  if (enabledLabels.length) {
    return `OAuth enabled: ${enabledLabels.join(', ')}. Email sign-in is also available.`;
  }
  if (external.github === false) {
    return 'GitHub sign-in is pending owner setup. Use email magic link or password.';
  }
  return 'OAuth is temporarily unavailable. Use email magic link or password.';
}

function summarizeOauthProviderState(external = {}) {
  const enabledProviders = OAUTH_PROVIDER_ORDER.filter((provider) => external[provider] === true);
  const disabledProviders = OAUTH_PROVIDER_ORDER.filter((provider) => external[provider] !== true);
  return {
    enabledProviders: enabledProviders.join(',') || 'none',
    disabledProviders: disabledProviders.join(',') || 'none',
    githubEnabled: external.github === true,
    oauthProviderCount: enabledProviders.length,
  };
}

function trackAuthProviderState(external = {}, state = 'loaded') {
  trackAccountFunnelEvent('auth_provider_state_checked', {
    target: '/auth/v1/settings',
    state,
    ...summarizeOauthProviderState(external),
  });
  trackSignupOptionsShown(external, state);
}

function trackSignupOptionsShown(external = {}, state = 'loaded') {
  if (signupOptionsShownTracked) return;
  signupOptionsShownTracked = true;
  trackAccountFunnelEvent('account_signup_options_shown', {
    button: 'account_auth_panel',
    target: '#intent-oauth-actions',
    state,
    ...summarizeOauthProviderState(external),
  });
}

async function applyAuthSettings() {
  applyOauthButtons({}, 'Checking enabled OAuth providers...');
  try {
    const res = await fetch(`${SUPABASE_URL}/auth/v1/settings`, { headers: { apikey: SUPABASE_ANON_KEY } });
    if (!res.ok) {
      applyOauthButtons({}, 'OAuth status is unavailable. Use email magic link or password.');
      trackAuthProviderState({}, 'unavailable');
      return;
    }
    const external = (await res.json()).external || {};
    applyOauthButtons(external);
    trackAuthProviderState(external, 'loaded');
    maybeStartOauthFromIntent(external);
  } catch (_error) {
    applyOauthButtons({}, 'OAuth status is unavailable. Use email magic link or password.');
    trackAuthProviderState({}, 'unavailable');
  }
}

function trackAccountFunnelEvent(event, data = {}) {
  const params = new URLSearchParams(window.location.search);
  let referrerHost = null;
  try {
    const referrer = document.referrer ? new URL(document.referrer) : null;
    referrerHost = referrer && referrer.host !== window.location.host ? referrer.host : null;
  } catch (_error) {
    referrerHost = null;
  }
  const payload = JSON.stringify({
    event,
    plan: data.plan || selectedPlan || null,
    sourcePage: window.location.href,
    target: data.target || null,
    metadata: {
      source: 'account',
      button: data.button || null,
      state: data.state || null,
      billing: data.billing || null,
      enabledProviders: data.enabledProviders || null,
      disabledProviders: data.disabledProviders || null,
      githubEnabled: data.githubEnabled ?? null,
      oauthProviderCount: data.oauthProviderCount ?? null,
      snippet: data.snippet || null,
      utmSource: params.get('utm_source') || params.get('utmSource') || null,
      utmMedium: params.get('utm_medium') || params.get('utmMedium') || null,
      utmCampaign: params.get('utm_campaign') || params.get('utmCampaign') || null,
      utmContent: params.get('utm_content') || params.get('utmContent') || null,
      sourceSurface: params.get('source_surface') || params.get('sourceSurface') || null,
      setupSource: params.get('setup') || params.get('setupSource') || null,
      referrerHost,
      landingPath: window.location.pathname,
    },
  });
  try {
    if (navigator.sendBeacon) {
      const blob = new Blob([payload], { type: 'application/json' });
      if (navigator.sendBeacon('/api/funnel-event', blob)) return;
    }
  } catch (_error) {
    // Funnel telemetry must never block customer onboarding.
  }
  fetch('/api/funnel-event', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: payload,
    keepalive: true,
    credentials: 'omit',
  }).catch(() => {});
}

function billingFailureState(error, fallback = 'billing_action_failed') {
  const message = String(error?.message || '').toLowerCase();
  if (message.includes('stripe_not_configured') || message.includes('stripe is not configured') || message.includes('not configured')) return 'stripe_not_configured';
  if (message.includes('stripe_customer_missing') || message.includes('complete stripe checkout')) return 'stripe_customer_missing';
  if (message.includes('crypto_not_configured')) return 'crypto_not_configured';
  if (message.includes('401') || message.includes('sign in') || message.includes('unauthorized')) return 'unauthorized';
  if (message.includes('403') || message.includes('forbidden')) return 'forbidden';
  if (message.includes('409') || message.includes('conflict')) return 'conflict';
  if (message.includes('429') || message.includes('rate limit')) return 'rate_limited';
  if (message.includes('503') || message.includes('unavailable')) return 'service_unavailable';
  if (message.includes('http')) return 'http_error';
  return fallback;
}

async function session() {
  const { data } = await sb.auth.getSession();
  return data?.session || null;
}

async function api(path, options = {}) {
  const s = await session();
  if (!s) throw new Error('Sign in first.');
  const res = await fetch(`${sageRouterUrl}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${s.access_token}`,
      ...(options.headers || {})
    }
  });
  const raw = await res.text();
  let data = {};
  try {
    data = raw ? JSON.parse(raw) : {};
  } catch (_error) {
    data = { message: raw.slice(0, 240) };
  }
  if (!res.ok) throw new Error(data.message || data.error || `HTTP ${res.status}`);
  return data;
}

function markStep(id, done) {
  const el = $(id);
  if (el) el.textContent = done ? 'ok' : el.dataset.step || el.textContent;
}

function activationBadge(id, done) {
  const el = $(id);
  if (el) el.textContent = done ? 'Ready' : 'Waiting';
}

function hasSessionApiKey() {
  return Boolean(($('test-api-key')?.value.trim() || currentRawKey || '').trim());
}

function focusApiKeyVerifier(message = 'Paste an existing sk_sage key or create a new one first.') {
  set('post-key-activation-status', message);
  const target = $('test-api-key') || $('create-key');
  target?.scrollIntoView?.({ behavior: 'smooth', block: 'center' });
  target?.focus?.();
}

function isKeyRecoveryIntent() {
  return pendingStartAction === 'create_key';
}

function signedInNextActionState() {
  if (!activationState.signedIn) {
    return {
      title: 'Sign in to start',
      copy: 'Create an account, then Sage Router will guide you to a generated key and first routed request.',
      label: 'Sign in',
      state: 'sign_in',
      target: '#auth-panel',
    };
  }
  if (!activationState.keyCount && !hasSessionApiKey()) {
    if (isKeyRecoveryIntent()) {
      return {
        title: 'Finish key recovery',
        copy: 'This recovery link is ready to create your hosted sk_sage setup key now. Checkout and email verification can follow after the key exists.',
        label: 'Create setup key now',
        state: 'create_key',
        target: '/account/api-keys',
      };
    }
    return {
      title: 'Finish activation: create API key',
      copy: activationState.emailVerified
        ? 'Create the generated sk_sage setup key now. The raw key is shown once, inserted into setup snippets, and becomes the fastest path to first routed request.'
        : 'Create the setup key now. It remains blocked from routing until email verification and checkout are complete, but the key step no longer has to wait.',
      label: 'Create setup key now',
      state: 'create_key',
      target: '/account/api-keys',
    };
  }
  if (!activationState.emailVerified) {
    return {
      title: 'Verify email next',
      copy: 'Your generated key exists. Email verification unlocks checkout and hosted routing for it.',
      label: 'Resend verification email',
      state: 'verify_email',
      target: '#resend-verification-email',
    };
  }
  if (!activationState.routingEnabled) {
    return {
      title: 'Unlock routing for this key',
      copy: stripeCheckoutReadyForPlan(selectedPlan)
        ? `Your generated key exists. Continue to ${planDisplay(selectedPlan)} checkout so it can route hosted traffic.`
        : 'Your generated key exists. Stripe checkout is not ready, so use manual settlement or billing help.',
      label: stripeCheckoutReadyForPlan(selectedPlan) ? `Continue to ${planDisplay(selectedPlan)} checkout` : 'Open billing options',
      state: 'checkout',
      target: stripeCheckoutReadyForPlan(selectedPlan) ? '/billing/stripe/checkout' : '#billing',
    };
  }
  if (!(activationState.keyVerified || activationState.requestCount > 0)) {
    return {
      title: 'Verify public edge access',
      copy: 'Check /v1/models with your generated key before wiring Codex, OpenAI SDKs, or agents.',
      label: 'Verify /v1/models',
      state: 'verify_key',
      target: '/v1/models',
    };
  }
  if (!activationState.requestCount) {
    return {
      title: 'Send the first routed request',
      copy: 'One browser Responses API test proves sage-router/frontier is working and records first-request activation.',
      label: 'Send first request',
      state: 'first_request',
      target: '/v1/responses',
    };
  }
  return {
    title: 'Activation complete',
    copy: `${fmtNumber(activationState.requestCount)} routed request${activationState.requestCount === 1 ? '' : 's'} recorded. Keep setup snippets handy for agents and production clients.`,
    label: 'Open dashboard',
    state: 'dashboard',
    target: '/analytics.html',
  };
}

function renderSignedInNextAction() {
  const action = signedInNextActionState();
  set('signed-in-next-title', action.title);
  set('signed-in-next-copy', action.copy);
  const button = $('signed-in-next-button');
  if (button) {
    button.textContent = action.label;
    button.dataset.nextAction = action.state;
    button.dataset.nextTarget = action.target;
  }
  const actionKey = [
    action.state,
    action.target,
    activationState.signedIn ? 'in' : 'out',
    activationState.emailVerified ? 'verified' : 'unverified',
    activationState.keyCount > 0 ? 'has-key' : 'no-key',
    activationState.routingEnabled ? 'routing' : 'blocked',
    activationState.requestCount > 0 ? 'used' : 'unused',
  ].join('|');
  if (actionKey !== lastNextActionShownKey) {
    lastNextActionShownKey = actionKey;
    trackAccountFunnelEvent('account_next_action_shown', {
      button: action.label,
      target: action.target,
      state: action.state,
    });
    if (action.state === 'create_key' && activationState.signedIn && !activationState.keyCount && !isKeyRecoveryIntent()) {
      trackAccountFunnelEvent('account_key_recovery_viewed', {
        button: 'signed_in_no_key_prompt',
        target: '/account/api-keys',
        state: 'in_app_no_key_prompt',
      });
    }
    if (action.state === 'create_key' && activationState.signedIn && !activationState.keyCount && isKeyRecoveryIntent() && !hasKeyRecoveryMarker(KEY_RECOVERY_SIGNED_IN_PROMPT_STORAGE_KEY)) {
      markKeyRecoveryMarker(KEY_RECOVERY_SIGNED_IN_PROMPT_STORAGE_KEY);
      window.setTimeout(() => {
        $('signed-in-next-action')?.scrollIntoView?.({ behavior: 'smooth', block: 'center' });
        set('launch-next-action', 'Recovery sign-in complete. Create the sk_sage setup key now; checkout and routing unlock after the key exists.');
        trackAccountFunnelEvent('account_key_recovery_signed_in_prompt_shown', {
          button: 'signed_in_key_recovery_prompt',
          target: '/account/api-keys',
          state: requestedKeyRecoveryStateFromUrl(),
        });
      }, 250);
    }
  }
}

function renderPostKeyActivationPanel() {
  const keyVerified = activationState.keyVerified || activationState.requestCount > 0;
  const canUseSessionKey = hasSessionApiKey();
  setBusy('post-key-verify-button', false);
  setBusy('post-key-first-request-button', false);
  const verifyButton = $('post-key-verify-button');
  const firstRequestButton = $('post-key-first-request-button');
  if (verifyButton) verifyButton.disabled = !activationState.signedIn || (!activationState.keyCount && !canUseSessionKey);
  if (firstRequestButton) firstRequestButton.disabled = !activationState.signedIn || (!activationState.keyCount && !canUseSessionKey);

  if (!activationState.signedIn) {
    set('post-key-activation-status', 'Sign in first, then generate the hosted key.');
  } else if (!activationState.emailVerified) {
    set('post-key-activation-status', activationState.keyCount || canUseSessionKey
      ? 'Setup key created. Verify your email before checkout or hosted routing can use it.'
      : 'Create the setup key now; it remains blocked from routing until email verification and checkout are complete.');
  } else if (!activationState.keyCount && !canUseSessionKey) {
    set('post-key-activation-status', 'Create a generated sk_sage key first; the raw key is shown once and inserted into these setup snippets.');
  } else if (!canUseSessionKey) {
    set('post-key-activation-status', 'An active key exists. Paste it into the verifier or create a fresh key to populate setup snippets.');
  } else if (!activationState.routingEnabled) {
    set('post-key-activation-status', 'Verify the key now, then finish checkout so the first routed request can pass.');
  } else if (!keyVerified) {
    set('post-key-activation-status', 'Next: verify /v1/models, then send the first sage-router/frontier request.');
  } else if (!activationState.requestCount) {
    set('post-key-activation-status', 'Next: send the first sage-router/frontier request or copy Codex setup.');
  } else {
    set('post-key-activation-status', `Activated: ${fmtNumber(activationState.requestCount)} routed request${activationState.requestCount === 1 ? '' : 's'} recorded.`);
  }
}

function renderLaunchNextAction(patch = {}) {
  activationState = { ...activationState, ...patch };
  const keyVerified = activationState.keyVerified || activationState.requestCount > 0;
  activationBadge('launch-auth-status', activationState.signedIn);
  activationBadge('launch-plan-status', activationState.routingEnabled);
  activationBadge('launch-key-status', activationState.keyCount > 0);
  activationBadge('launch-verify-status', keyVerified);
  activationBadge('launch-first-request-status', activationState.requestCount > 0);
  markStep('step-auth', activationState.signedIn);
  markStep('step-plan', activationState.routingEnabled);
  markStep('step-key', activationState.keyCount > 0);
  markStep('step-verify', keyVerified);
  markStep('step-first-request', activationState.requestCount > 0);

  if (!activationState.signedIn) {
    set('launch-next-action', 'Next: sign in or create an account.');
  } else if (!activationState.keyCount) {
    set('launch-next-action', 'Next: create an API key so setup can be copied before checkout.');
  } else if (!activationState.emailVerified) {
    set('launch-next-action', 'Next: verify your email so checkout and routing can unlock the generated key.');
  } else if (!activationState.routingEnabled) {
    set('launch-next-action', 'Next: choose a paid plan or finish checkout so generated keys can route.');
  } else if (!keyVerified) {
    set('launch-next-action', 'Next: test the key against /v1/models using the verifier below.');
  } else if (!activationState.requestCount) {
    set('launch-next-action', 'Next: send the first sage-router/frontier Responses request from this page or copy the quickstart.');
  } else {
    set('launch-next-action', `Activated: ${fmtNumber(activationState.requestCount)} routed request${activationState.requestCount === 1 ? '' : 's'} recorded this period.`);
  }
  renderPostKeyActivationPanel();
  renderSignedInNextAction();
  renderSupportContext();
}

function applyEmailVerificationState(state = {}) {
  const required = state.required === true;
  const verified = state.verified !== false;
  const email = state.email || 'your email';
  const blocked = required && !verified;
  verificationEmail = blocked ? String(state.email || '').trim() : '';
  emailActionAllowed = !blocked;
  const message = blocked
    ? `Verify ${email} before checkout or hosted routing. You can still create a setup key first.`
    : (required ? 'Email verified.' : 'Email verification is not required for this deployment.');
  set('email-verification-status', message);
  const status = $('email-verification-status');
  if (status) status.classList.toggle('danger', blocked);
  show('resend-verification-email', blocked && Boolean(verificationEmail));
  ['crypto-intent'].forEach((id) => {
    const button = $(id);
    if (button) button.disabled = blocked;
  });
  updateBillingControls();
  return !blocked;
}

function quickstartText(key = 'sk_sage_your_key_here') {
  return `export OPENAI_BASE_URL="${openaiBaseUrl}"
export OPENAI_API_KEY="${key}"

curl "$OPENAI_BASE_URL/chat/completions" \\
  -H "Authorization: Bearer $OPENAI_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "sage-router/frontier",
    "messages": [{"role": "user", "content": "Say hello from Sage Router"}]
  }'`;
}

function openaiSdkSetupText(key = 'sk_sage_your_key_here') {
  return `import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "${openaiBaseUrl}",
  apiKey: "${key}",
});

const response = await client.chat.completions.create({
  model: "sage-router/frontier",
  messages: [{ role: "user", content: "Route this through Sage Router" }],
});`;
}

function codexSetupText(key = 'sk_sage_your_key_here') {
  return `mkdir -p ~/.codex
cat >> ~/.codex/config.toml <<'TOML'
[model_providers.sage-router-hosted]
name = "Sage Router Hosted"
base_url = "${openaiBaseUrl}/"
env_key = "OPENAI_API_KEY"
wire_api = "responses"

[profiles.sage-router-frontier]
model_provider = "sage-router-hosted"
model = "sage-router/frontier"
TOML

export OPENAI_API_KEY="${key}"
codex --profile sage-router-frontier`;
}

function anthropicSetupText(key = 'sk_sage_your_key_here') {
  return `export ANTHROPIC_BASE_URL="${anthropicBaseUrl}"
export ANTHROPIC_API_KEY="${key}"

curl "$ANTHROPIC_BASE_URL/v1/messages" \\
  -H "x-api-key: $ANTHROPIC_API_KEY" \\
  -H "anthropic-version: 2023-06-01" \\
  -H "content-type: application/json" \\
  -d '{
    "model": "sage-router/frontier",
    "max_tokens": 128,
    "messages": [{"role": "user", "content": "Say hello from Sage Router"}]
  }'`;
}

function renderQuickstart(key) {
  currentRawKey = key || currentRawKey;
  if (currentRawKey && $('test-api-key') && !$('test-api-key').value) {
    $('test-api-key').value = currentRawKey;
  }
  const displayKey = currentRawKey || 'sk_sage_your_key_here';
  set('preauth-setup-code', quickstartText('sk_sage_your_key_here'));
  set('quickstart-code', quickstartText(displayKey));
  set('client-openai-code', openaiSdkSetupText(displayKey));
  set('client-codex-code', codexSetupText(displayKey));
  set('client-anthropic-code', anthropicSetupText(displayKey));
  renderPostKeyActivationPanel();
}

function supportUsageSummary(usage) {
  if (!usage) return null;
  return {
    period: usage.period || null,
    plan: usage.plan || null,
    requests: Number.isFinite(Number(usage.requests)) ? Number(usage.requests) : 0,
    quota: usage.unlimited ? 'unlimited' : (Number.isFinite(Number(usage.quota)) ? Number(usage.quota) : null),
    remaining: usage.unlimited ? 'unlimited' : (Number.isFinite(Number(usage.remaining)) ? Number(usage.remaining) : null),
    rateLimitPerMinute: Number.isFinite(Number(usage.rateLimitPerMinute)) ? Number(usage.rateLimitPerMinute) : null,
    resetAt: usage.resetAt || usage.reset_at || null,
  };
}

function safeSupportContext() {
  return {
    service: 'sage-router-hosted',
    generatedAt: new Date().toISOString(),
    api: {
      openaiBaseUrl,
      anthropicBaseUrl,
      model: 'sage-router/frontier',
      apiKeyPrefix: 'sk_sage_',
    },
    account: {
      signedIn: Boolean(activationState.signedIn),
      emailVerified: Boolean(activationState.emailVerified),
      plan: supportContextState.plan || selectedPlan || 'unknown',
      status: supportContextState.status || 'unknown',
      routingEnabled: Boolean(supportContextState.routingEnabled || activationState.routingEnabled),
    },
    activation: {
      activeKeyCount: Number(activationState.keyCount || 0),
      keyVerified: Boolean(activationState.keyVerified || activationState.requestCount > 0),
      routedRequestCount: Number(activationState.requestCount || 0),
    },
    usage: supportUsageSummary(supportContextState.usage),
    supportPaths: {
      support: 'https://sagerouter.dev/support',
      status: 'https://sagerouter.dev/status',
      troubleshooting: 'https://sagerouter.dev/api-troubleshooting',
      account: 'https://app.sagerouter.dev/account.html',
    },
    safeFields: ['plan', 'status', 'routingEnabled', 'activeKeyCount', 'keyVerified', 'routedRequestCount', 'usageQuota', 'rateLimitPerMinute'],
    redactionNotice: 'Do not include prompts, provider credentials, OAuth tokens, generated API keys, private keys, cookies, raw provider responses, or customer data.',
  };
}

function renderSupportContext(patch = {}) {
  supportContextState = { ...supportContextState, ...patch };
  const el = $('support-context-code');
  if (el) el.textContent = JSON.stringify(safeSupportContext(), null, 2);
}

function planLabel(plans, name) {
  return plans?.[name]?.name || (name ? name.charAt(0).toUpperCase() + name.slice(1) : 'plan');
}

function planPriceAmount(plan = {}) {
  const explicit = Number(plan.monthlyPriceUsd ?? plan.priceUsd ?? plan.priceAmount);
  if (Number.isFinite(explicit) && explicit > 0) return explicit;
  const match = String(plan.price || '').match(/([0-9]+(?:\.[0-9]+)?)/);
  return match ? Number(match[1]) : 0;
}

function costPerThousandRequests(plan = {}) {
  const quota = Number(plan.limits?.monthlyRequests || 0);
  const price = planPriceAmount(plan);
  if (!quota || !price) return '';
  return `$${((price / quota) * 1000).toFixed(2)}`;
}

function renderPreauthPlanPreview(plans = availablePlans) {
  availablePlans = plans || FALLBACK_PLANS;
  const order = DEFAULT_PLAN_ORDER.filter(name => availablePlans?.[name]);
  if (!order.length) return;
  if (!order.includes(selectedPlan)) {
    selectedPlan = rememberSelectedPlan(order.includes('pro') ? 'pro' : order[0]);
  }
  const chooser = $('preauth-plans');
  if (chooser) {
    chooser.innerHTML = order.map((name) => {
      const plan = availablePlans[name] || {};
      return `<button class="preauthPlan ${selectedPlan === name ? 'active' : ''}" data-preauth-plan="${esc(name)}" type="button">
        <strong>${esc(plan.name || planDisplay(name))}</strong>
        <span>${esc(plan.price || '')}</span>
      </button>`;
    }).join('');
  }
  document.querySelectorAll('[data-preauth-plan]').forEach(button => button.classList.toggle('active', button.dataset.preauthPlan === selectedPlan));
  document.querySelectorAll('.planCard').forEach(card => card.classList.toggle('active', card.dataset.plan === selectedPlan));
  const plan = availablePlans[selectedPlan] || {};
  const limits = plan.limits || {};
  set('plan-preview-selected', plan.name || planDisplay(selectedPlan));
  set('plan-preview-price', plan.price || 'Manual');
  set('plan-preview-quota', limits.monthlyRequests ? `${fmtNumber(limits.monthlyRequests)}/month` : 'Manual');
  set('plan-preview-rate', limits.rateLimitPerMinute ? `${fmtNumber(limits.rateLimitPerMinute)}/min` : 'Manual');
  set('plan-preview-route-cost', costPerThousandRequests(plan) || 'Manual');
  updateBillingControls();
}

function nextPaidPlan(currentPlan, plans = FALLBACK_PLANS) {
  const available = DEFAULT_PLAN_ORDER.filter(name => plans?.[name]);
  if (!available.length) return '';
  const index = available.indexOf(currentPlan);
  if (index < 0) return available[0];
  return available[Math.min(index + 1, available.length - 1)] || '';
}

function selectPlan(plan, status = '') {
  const normalized = normalizePlan(plan);
  if (!normalized) return;
  selectedPlan = rememberSelectedPlan(normalized);
  document.querySelectorAll('.planCard').forEach(card => card.classList.toggle('active', card.dataset.plan === selectedPlan));
  renderPreauthPlanPreview(availablePlans);
  updateBillingControls(status);
  if (latestOauthExternalState) applyOauthButtons(latestOauthExternalState);
}

function applyRequestedPlanFromUrl() {
  const requested = requestedPlanFromUrl();
  if (!requested) return '';
  selectedPlan = rememberSelectedPlan(requested);
  renderPreauthPlanPreview(availablePlans);
  updateBillingControls(`${planDisplay(selectedPlan)} selected. Sign in or continue to checkout when ready.`);
  return selectedPlan;
}

function renderUpgradeRecommendation(usage, plans = FALLBACK_PLANS, currentPlan = 'free', routingEnabled = false) {
  const button = $('usage-upgrade');
  const current = currentPlan || usage?.plan || 'free';
  const nextPlan = nextPaidPlan(current, plans);
  recommendedUpgradePlan = '';
  if (button) button.classList.add('hidden');
  set('usage-recommendation', '');

  if (!routingEnabled) {
    recommendedUpgradePlan = nextPlan || 'lite';
    set('usage-recommendation', `Upgrade to ${planLabel(plans, recommendedUpgradePlan)} to enable generated-key routing.`);
  } else if (usage && !usage.unlimited) {
    const used = Number(usage.requests || 0);
    const quota = Number(usage.quota || 0);
    const percent = quota > 0 ? (used / quota) * 100 : 0;
    if (percent >= 90 && nextPlan && nextPlan !== current) {
      recommendedUpgradePlan = nextPlan;
      set('usage-recommendation', `Usage is above 90% of this period. Select ${planLabel(plans, nextPlan)} before quota blocks agent traffic.`);
    } else if (percent >= 75 && nextPlan && nextPlan !== current) {
      recommendedUpgradePlan = nextPlan;
      set('usage-recommendation', `Usage is above 75% of this period. ${planLabel(plans, nextPlan)} gives more request headroom.`);
    } else if (percent >= 90 && current === 'max') {
      set('usage-recommendation', 'Usage is above 90% of Max. Use billing management or manual support before adding more production traffic.');
    }
  }

  if (button && recommendedUpgradePlan) {
    button.textContent = `Select ${planLabel(plans, recommendedUpgradePlan)}`;
    button.classList.remove('hidden');
  }
}

function renderUsage(usage, plans = FALLBACK_PLANS, currentPlan = '', routingEnabled = true) {
  renderSupportContext({ usage, plan: currentPlan || usage?.plan || supportContextState.plan, routingEnabled });
  const fill = $('usage-fill');
  if (!usage) {
    set('usage-status', 'Usage is unavailable.');
    set('usage-used', '--');
    set('usage-remaining', '--');
    set('usage-rate', '--');
    if (fill) fill.style.width = '0%';
    recommendedUpgradePlan = '';
    $('usage-upgrade')?.classList.add('hidden');
    set('usage-recommendation', '');
    return;
  }
  const used = Number(usage.requests || 0);
  const quota = Number(usage.quota || 0);
  const remaining = usage.unlimited ? null : Number(usage.remaining || 0);
  const percent = quota > 0 ? Math.min(100, Math.max(0, (used / quota) * 100)) : 0;
  set('usage-status', usage.unlimited
    ? `${usage.period || 'Current period'} · ${usage.plan || 'free'} has no monthly cap configured.`
    : `${usage.period || 'Current period'} · ${fmtNumber(quota)} requests included.`);
  set('usage-used', fmtNumber(used));
  set('usage-remaining', usage.unlimited ? 'Unlimited' : fmtNumber(remaining));
  set('usage-rate', usage.rateLimitPerMinute ? `${fmtNumber(usage.rateLimitPerMinute)}/min` : '--');
  if (fill) fill.style.width = `${percent}%`;
  renderUpgradeRecommendation(usage, plans, currentPlan, routingEnabled);
}

function applyManualPaymentIntent(intent = {}) {
  if (!intent?.id) return;
  lastManualPaymentIntentId = intent.id;
  show('crypto-status-check', true);
  set('crypto-status', describeManualPaymentIntent(intent));
}

async function maybeStartCheckoutFromIntent({ emailVerified, routingEnabled } = {}) {
  if (pendingStartAction !== 'checkout') return;
  if (!activationState.signedIn || !emailVerified || routingEnabled || !activationState.keyCount) return;
  if (!stripeCheckoutReadyForPlan(selectedPlan)) return;
  if (hasAutoCheckoutAttempted(selectedPlan)) return;
  markAutoCheckoutAttempted(selectedPlan);
  set('billing-status', `Opening ${planDisplay(selectedPlan)} checkout from your saved activation intent...`);
  await stripeCheckout({ button: 'auto_checkout', state: 'saved_checkout_intent' });
}

async function maybeCreateKeyFromIntent({ emailVerified, keyCount } = {}) {
  if (!activationState.signedIn || Number(keyCount || 0) > 0) return false;
  if (hasAutoKeyAttempted(selectedPlan)) return false;
  const fromSavedIntent = ['checkout', 'create_key'].includes(pendingStartAction);
  const fromKeyRecoveryIntent = pendingStartAction === 'create_key';
  set('key-once', fromKeyRecoveryIntent
    ? 'Creating your sk_sage key from the saved key-recovery link...'
    : fromSavedIntent
    ? 'Creating your sk_sage key from the saved activation intent...'
    : 'Creating your first sk_sage setup key...');
  $('create-key')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  trackAccountFunnelEvent('account_intent_create_key_clicked', {
    button: fromKeyRecoveryIntent ? 'saved_key_recovery_intent' : (fromSavedIntent ? 'saved_activation_intent' : 'first_signed_in_auto_setup'),
    target: '/account/api-keys',
    state: fromKeyRecoveryIntent ? 'saved_key_recovery_auto_key' : (fromSavedIntent ? 'saved_intent_auto_key' : 'first_signed_in_auto_key')
  });
  const created = await createKey();
  if (!created) return false;
  markAutoKeyAttempted(selectedPlan);
  $('key-once')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  return true;
}

async function refresh() {
  const s = await session();
  show('auth-panel', !s);
  show('account-panel', !!s);
  show('sign-out', !!s);
  renderLaunchNextAction({ signedIn: !!s, emailVerified: !s, routingEnabled: false, keyCount: 0, keyVerified: keyVerifiedThisSession, requestCount: 0 });
  renderSupportContext({ plan: selectedPlan, status: s ? 'loading' : 'signed_out', routingEnabled: false, usage: null });
  try {
    const metadata = await fetch(`${sageRouterUrl}/pricing`).then(response => response.ok ? response.json() : null);
    applyLaunchMetadata(metadata);
  } catch (_error) {
    applyLaunchMetadata(null);
  }
  renderPreauthPlanPreview(availablePlans);
  renderQuickstart();
  if (!s) return;
  set('account-status', 'Loading account...');
  set('email-verification-status', '');
  renderUsage(null, FALLBACK_PLANS, selectedPlan, false);
  try {
    const [accountData, keys, planData, usageData, paymentStatusData] = await Promise.all([
      api('/account'),
      api('/account/api-keys'),
      api('/account/plan').catch(() => null),
      api('/account/usage').catch(() => null),
      api('/billing/crypto/status').catch(() => null),
    ]);
    const customer = accountData.customer || {};
    const emailVerification = accountData.emailVerification || planData?.emailVerification || usageData?.emailVerification || {};
    const emailVerified = applyEmailVerificationState(emailVerification);
    applyLaunchMetadata(planData);
    renderQuickstart();
    const accountPlan = planData?.plan || customer.plan || 'free';
    const accountStatus = planData?.status || customer.status || 'inactive';
    const routingEnabled = planData?.routing_enabled ?? ['active', 'trialing', 'manual'].includes(accountStatus);
    renderSupportContext({ plan: accountPlan, status: accountStatus, routingEnabled });
    set('account-status', `${customer.email || customer.user_id} · ${accountPlan} · ${accountStatus}`);
    set('routing-status', routingEnabled ? 'Routing enabled for generated API keys.' : 'Upgrade required before generated API keys can route paid traffic.');
    const plans = planData?.plans || FALLBACK_PLANS;
    availablePlans = plans;
    renderPreauthPlanPreview(plans);
    renderPlans(plans, accountPlan);
    const usage = usageData?.usage || null;
    const activation = usageData?.activation || {};
    const keyCount = Number.isFinite(Number(activation.activeKeyCount)) ? Number(activation.activeKeyCount) : (keys.api_keys || []).length;
    const requestCount = Number(activation.requestCount ?? usage?.requests ?? 0);
    const keyVerified = keyVerifiedThisSession || requestCount > 0;
    renderUsage(usage, plans, accountPlan, routingEnabled);
    $('keys').innerHTML = renderKeys(keys.api_keys || []);
    applyManualPaymentIntent(paymentStatusData?.intent || {});
    renderLaunchNextAction({
      signedIn: true,
      emailVerified,
      routingEnabled: Boolean(activation.routingEnabled ?? (accountPlan !== 'free' && routingEnabled)),
      keyCount,
      keyVerified,
      requestCount,
    });
    const autoKeyCreated = await maybeCreateKeyFromIntent({
      emailVerified,
      keyCount,
    });
    if (autoKeyCreated) return;
    await maybeStartCheckoutFromIntent({
      emailVerified,
      routingEnabled: Boolean(activation.routingEnabled ?? (accountPlan !== 'free' && routingEnabled)),
    });
  } catch (error) {
    set('account-status', error.message);
    renderPlans(FALLBACK_PLANS, 'free');
    renderUsage(null, FALLBACK_PLANS, 'free', false);
    renderLaunchNextAction({ signedIn: true, emailVerified: true, routingEnabled: false, keyCount: 0, keyVerified: keyVerifiedThisSession, requestCount: 0 });
  }
}

function handleBillingReturn() {
  if (billingReturnHandled) return;
  billingReturnHandled = true;
  const params = new URLSearchParams(window.location.search || '');
  const state = params.get('checkout');
  const billing = params.get('billing');
  const requested = normalizePlan(params.get('plan'));
  if (requested) selectedPlan = rememberSelectedPlan(requested);
  if (state || billing) {
    pendingStartAction = rememberStartAction('');
  }
  if (!state && !billing) return;
  if (state) {
    if (state === 'success') {
      trackAccountFunnelEvent('account_checkout_returned', { state, target: window.location.href });
      set('billing-status', `Stripe checkout returned for ${planDisplay(selectedPlan)}. Activation can take a moment while the webhook confirms the subscription.`);
      setTimeout(() => refresh(), 3000);
      setTimeout(() => refresh(), 10000);
    } else if (state === 'cancel') {
      trackAccountFunnelEvent('account_checkout_returned', { state, target: window.location.href });
      set('billing-status', `Checkout cancelled. ${planDisplay(selectedPlan)} is still selected.`);
    }
  } else if (billing === 'portal') {
    trackAccountFunnelEvent('account_billing_portal_returned', { billing, target: window.location.href });
    set('billing-status', 'Returned from Stripe billing management.');
    setTimeout(() => refresh(), 1500);
  }
  const cleanUrl = `${window.location.origin}${window.location.pathname}`;
  window.history.replaceState({}, document.title, cleanUrl);
}

function renderPlans(plans, currentPlan) {
  const el = $('plans');
  if (!el) return;
  const order = DEFAULT_PLAN_ORDER.filter(name => plans?.[name]);
  if (!order.includes(selectedPlan)) {
    selectedPlan = rememberSelectedPlan(order.includes(currentPlan) ? currentPlan : 'pro');
  }
  el.innerHTML = order.map((name) => {
    const plan = plans[name] || {};
    const limits = plan.limits || {};
    const limitItems = [
      limits.monthlyRequests ? `${fmtNumber(limits.monthlyRequests)} requests/month` : '',
      limits.rateLimitPerMinute ? `${fmtNumber(limits.rateLimitPerMinute)} requests/minute` : '',
    ].filter(Boolean);
    const featureItems = [...limitItems, ...(plan.features || [])].slice(0, 4);
    const features = featureItems.map(feature => `<li>${esc(feature)}</li>`).join('');
    const configured = plan.stripeConfigured === undefined || plan.stripeConfigured;
    const badge = currentPlan === name ? 'Current' : (configured ? 'Ready' : 'Manual');
    return `<button class="planCard ${selectedPlan === name ? 'active' : ''}" data-plan="${esc(name)}" type="button">
      <div class="planName"><span>${esc(plan.name || name)}</span><span class="pill">${esc(badge)}</span></div>
      <div class="price">${esc(plan.price || '')}</div>
      <ul class="features">${features}</ul>
    </button>`;
  }).join('');
}

function renderKeys(keys) {
  if (!keys.length) return '<p class="muted">No API keys yet.</p>';
  return `<table><thead><tr><th>Name</th><th>Prefix</th><th>Status</th><th>Plan</th><th>Routing</th><th></th></tr></thead><tbody>${keys.map(k => {
    const routing = k.routing_enabled ? 'Ready' : 'Blocked';
    return `<tr><td>${esc(k.name)}</td><td><span class="pill">${esc(k.prefix)}</span></td><td>${esc(k.status)}</td><td>${esc(k.plan || 'free')}</td><td>${esc(routing)}</td><td><button class="btn ghost" data-revoke="${esc(k.id)}">Revoke</button></td></tr>`;
  }).join('')}</tbody></table>`;
}

async function oauthLogin(provider, options = {}) {
  const mirrorIntent = Boolean(options.mirrorIntent);
  const button = options.button || provider;
  setAuthStatus(`Opening ${provider} sign-in...`, mirrorIntent);
  rememberOnboardingContext(onboardingContext({ authMethod: provider }));
  trackAccountFunnelEvent('account_oauth_clicked', { button, target: '/auth/v1/authorize', state: provider });
  const redirectTo = accountPageUrlWithPlan();
  const { error } = await sb.auth.signInWithOAuth({ provider, options: { redirectTo } });
  if (error) {
    trackAccountFunnelEvent('account_oauth_failed', { button, target: '/auth/v1/authorize', state: provider });
    setAuthStatus(error.message, mirrorIntent);
  }
}

async function maybeStartOauthFromIntent(external = {}) {
  if (!['checkout', 'create_key'].includes(pendingStartAction)) return;
  const currentSession = await session();
  if (currentSession) return;
  if (requestedEmailAuthFromUrl()) {
    setAuthStatus('Use same-email magic link or password to finish key setup.', true);
    trackAccountFunnelEvent('account_auto_oauth_skipped', {
      button: pendingStartAction === 'create_key' ? 'email_key_recovery' : 'email_activation',
      target: '#intent-email',
      state: 'email_auth_requested',
    });
    focusEmailInput(true);
    return;
  }
  const provider = requestedAuthProviderFromUrl() || 'github';
  if (external[provider] !== true) return;
  if (hasAutoOauthAttempted(provider, selectedPlan)) return;
  markAutoOauthAttempted(provider, selectedPlan);
  const isKeyRecovery = pendingStartAction === 'create_key';
  setAuthStatus(`Opening ${OAUTH_LABELS[provider] || provider} sign-in from your saved ${isKeyRecovery ? 'key-recovery' : 'activation'} intent...`, true);
  trackAccountFunnelEvent('account_auto_oauth_started', {
    button: isKeyRecovery ? 'auto_key_recovery_oauth' : 'auto_checkout_oauth',
    target: '/auth/v1/authorize',
    state: provider,
  });
  window.setTimeout(() => {
    oauthLogin(provider, { button: isKeyRecovery ? 'auto_key_recovery_oauth' : 'auto_checkout_oauth', mirrorIntent: true });
  }, 900);
}

async function passwordLogin() {
  set('auth-status', 'Signing in...');
  const email = $('email')?.value.trim();
  const password = $('password')?.value;
  if (!email) {
    set('auth-status', 'Enter your email first.');
    return;
  }
  if (!password) {
    set('auth-status', 'Enter a password, or use Send magic link.');
    return;
  }
  trackAccountFunnelEvent('account_login_submitted', { button: 'password_login', target: '/auth/v1/token', state: 'password' });
  const { error } = await sb.auth.signInWithPassword({ email, password });
  set('auth-status', error ? error.message : 'Signed in.');
  if (error) {
    trackAccountFunnelEvent('account_login_failed', { button: 'password_login', target: '/auth/v1/token', state: 'password' });
    return;
  }
  trackAccountFunnelEvent('account_login_succeeded', { button: 'password_login', target: ACCOUNT_PAGE_URL, state: 'password' });
  refresh();
}

async function passwordSignup() {
  set('auth-status', 'Creating account...');
  const email = emailInputValue(false);
  syncEmailInputs(email);
  const password = $('password')?.value;
  if (!email) {
    set('auth-status', 'Enter your email first.');
    focusEmailInput(false);
    return;
  }
  if (!password) {
    set('auth-status', 'Enter a password for the new account.');
    $('password')?.focus();
    return;
  }
  if (password.length < 8) {
    set('auth-status', 'Use at least 8 characters for the password.');
    return;
  }
  trackAccountFunnelEvent('account_signup_submitted', { button: 'password_signup', target: '/auth/v1/signup', state: 'password' });
  const metadata = onboardingContext({ authMethod: 'password' });
  rememberOnboardingContext(metadata);
  const { data, error } = await sb.auth.signUp({
    email,
    password,
    options: { emailRedirectTo: accountPageUrlWithPlan(metadata.selected_plan), data: metadata },
  });
  if (error) {
    trackAccountFunnelEvent('account_signup_failed', { button: 'password_signup', target: '/auth/v1/signup', state: 'password' });
    set('auth-status', error.message);
    return;
  }
  trackAccountFunnelEvent('account_signup_succeeded', { button: 'password_signup', target: ACCOUNT_PAGE_URL, state: data?.session ? 'signed_in' : 'email_confirmation' });
  set('auth-status', data?.session ? 'Account created and signed in.' : 'Account created. Check your email to confirm, then sign in.');
  refresh();
}

async function magicLogin(options = {}) {
  if (options?.preventDefault) options = {};
  const button = options.button || 'magic_login';
  const preferIntent = Boolean(options.preferIntent || button === 'intent_primary');
  const email = emailInputValue(preferIntent);
  if (!email) {
    setAuthStatus(preferIntent ? 'Enter your email above, then Sage Router will send the setup link.' : 'Enter your email first.', preferIntent);
    focusEmailInput(preferIntent);
    return;
  }
  syncEmailInputs(email);
  setAuthStatus('Sending magic link...', preferIntent);
  trackAccountFunnelEvent('account_magic_link_requested', { button, target: '/auth/v1/otp', state: 'email' });
  const metadata = onboardingContext({ authMethod: 'magic_link' });
  rememberOnboardingContext(metadata);
  const { error } = await sb.auth.signInWithOtp({ email, options: { emailRedirectTo: accountPageUrlWithPlan(metadata.selected_plan), data: metadata } });
  setAuthStatus(error ? error.message : 'Magic link sent. Check your email.', preferIntent);
  if (error) {
    trackAccountFunnelEvent('account_magic_link_failed', { button, target: '/auth/v1/otp', state: 'email' });
    return;
  }
  trackAccountFunnelEvent('account_magic_link_sent', { button, target: ACCOUNT_PAGE_URL, state: 'email' });
}

function dismissAccountAuthNudge() {
  try {
    window.localStorage?.setItem(ACCOUNT_AUTH_NUDGE_STORAGE_KEY, String(Date.now() + 7 * 24 * 60 * 60 * 1000));
  } catch (_error) {
    // Dismissal persistence is best-effort.
  }
  trackAccountFunnelEvent('account_activation_nudge_dismissed', {
    button: 'account_activation_nudge_dismiss',
    target: '#auth-panel',
    state: 'dismissed',
  });
  document.getElementById('account-auth-nudge')?.remove();
}

function mountAccountAuthNudge() {
  if (activationState.signedIn || document.getElementById('account-auth-nudge')) return;
  try {
    const dismissedUntil = Number(window.localStorage?.getItem(ACCOUNT_AUTH_NUDGE_STORAGE_KEY) || 0);
    if (dismissedUntil && dismissedUntil > Date.now()) return;
  } catch (_error) {
    // A missing dismissal marker should not block the conversion prompt.
  }

  const style = document.createElement('style');
  style.textContent = `
    #account-auth-nudge{position:fixed;right:18px;bottom:18px;z-index:40;display:grid;gap:10px;width:min(380px,calc(100vw - 36px));padding:18px;border:1px solid rgba(116,224,163,.35);border-radius:8px;background:linear-gradient(180deg,rgba(17,26,28,.97),rgba(8,13,16,.97));box-shadow:0 24px 80px rgba(0,0,0,.45);backdrop-filter:blur(18px)}
    #account-auth-nudge strong,#account-auth-nudge span{display:block}
    #account-auth-nudge strong{color:#edf6f7;font:900 18px/1.2 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    #account-auth-nudge span{color:#9fb2b8;font:600 14px/1.35 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    #account-auth-nudge .nudgeActions{display:grid;grid-template-columns:1fr 1fr;gap:8px}
    #account-auth-nudge button{min-height:42px;border:0;border-radius:8px;padding:0 12px;font:900 13px/1 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;cursor:pointer}
    #account-auth-nudge .nudgePrimary{background:linear-gradient(135deg,#74e0a3,#48c97f);color:#04150d}
    #account-auth-nudge .nudgeSecondary{background:rgba(255,255,255,.055);color:#edf6f7;border:1px solid rgba(182,210,218,.18)}
    #account-auth-nudge .nudgeClose{position:absolute;top:8px;right:8px;min-height:28px;width:28px;padding:0;border-radius:999px;background:rgba(255,255,255,.07);color:#9fb2b8;font-size:20px}
    @media(max-width:560px){#account-auth-nudge{left:18px;right:18px;width:auto}#account-auth-nudge .nudgeActions{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const nudge = document.createElement('aside');
  nudge.id = 'account-auth-nudge';
  nudge.setAttribute('aria-label', 'Start Sage Router account activation');
  nudge.innerHTML = `
    <button class="nudgeClose" type="button" aria-label="Dismiss account activation prompt">×</button>
    <div><strong>Create the key before checkout.</strong><span>Continue with GitHub, or jump to email setup. No provider key or card is required before the generated sk_sage key exists.</span></div>
    <div class="nudgeActions"><button class="nudgePrimary" type="button" data-account-nudge-oauth>Continue with GitHub</button><button class="nudgeSecondary" type="button" data-account-nudge-email>Email setup link</button></div>
  `;
  nudge.querySelector('.nudgeClose')?.addEventListener('click', dismissAccountAuthNudge);
  nudge.querySelector('[data-account-nudge-oauth]')?.addEventListener('click', () => {
    trackAccountFunnelEvent('account_activation_nudge_clicked', {
      button: 'account_activation_nudge_github',
      target: '/auth/v1/authorize',
      state: 'github',
    });
    oauthLogin('github', { button: 'account_activation_nudge_github', mirrorIntent: true });
  });
  nudge.querySelector('[data-account-nudge-email]')?.addEventListener('click', () => {
    trackAccountFunnelEvent('account_activation_nudge_clicked', {
      button: 'account_activation_nudge_email',
      target: '#intent-email',
      state: 'email',
    });
    focusEmailInput(true);
    setAuthStatus('Enter your email, then Sage Router will send the API key setup link.', true);
  });
  document.body.appendChild(nudge);
  trackAccountFunnelEvent('account_activation_nudge_shown', {
    button: 'account_activation_nudge',
    target: '#auth-panel',
    state: 'signed_out',
  });
}

function scheduleAccountAuthNudge() {
  window.setTimeout(() => {
    if (!activationState.signedIn) mountAccountAuthNudge();
  }, 6500);
}

async function resendVerificationEmail() {
  if (!verificationEmail) {
    set('email-verification-status', 'Refresh account state, then try resending verification.');
    return;
  }
  setBusy('resend-verification-email', true, 'Sending...');
  try {
    trackAccountFunnelEvent('account_email_verification_resend_clicked', { button: 'resend_verification_email', target: '/auth/v1/resend', state: 'signup' });
    const { error } = await sb.auth.resend({
      type: 'signup',
      email: verificationEmail,
      options: { emailRedirectTo: accountPageUrlWithPlan() },
    });
    if (error) {
      set('email-verification-status', error.message);
      return;
    }
    trackAccountFunnelEvent('account_email_verification_resent', { button: 'resend_verification_email', target: ACCOUNT_PAGE_URL, state: 'sent' });
    set('email-verification-status', 'Verification email sent. Check your inbox, then return to this page.');
  } catch (error) {
    set('email-verification-status', error.message || 'Could not resend verification email.');
  } finally {
    setBusy('resend-verification-email', false);
  }
}

async function createKey() {
  set('key-once', '');
  set('test-api-key-status', '');
  set('test-chat-status', '');
  setBusy('create-key', true, 'Creating...');
  const recoveryIntent = isKeyRecoveryIntent();
  try {
    const name = $('key-name')?.value || 'Default';
    trackAccountFunnelEvent('account_api_key_create_clicked', { button: 'create_key', target: '/account/api-keys', state: 'create' });
    const data = await api('/account/api-keys', { method: 'POST', body: JSON.stringify({ name }) });
    const key = data.key || '';
    renderQuickstart(key);
    trackAccountFunnelEvent('account_api_key_created', { button: 'create_key', target: '/account/api-keys', state: 'created' });
    if (recoveryIntent) {
      trackAccountFunnelEvent('account_key_recovery_key_created', { button: 'key_recovery_link', target: '/account/api-keys', state: 'created' });
    }
    const keyOnceCopy = recoveryIntent
      ? 'Key recovered. Copy this sk_sage setup key now; it is only shown once. Verify email and checkout can follow after the key exists.'
      : 'Copy now. This key is only shown once. Next, test it against <code>/v1/models</code>, then send the first routed request.';
    $('key-once').innerHTML = `<p>${keyOnceCopy}</p><div class="codeBox"><pre id="raw-api-key-once">${esc(key)}</pre><div class="copyRow"><button class="btn ghost" data-copy-target="raw-api-key-once" data-copy-label="Copy key">Copy key</button><button class="btn ghost" data-copy-target="quickstart-code" data-copy-label="Copy quickstart">Copy quickstart</button><button class="btn ghost" data-after-key-action="test-key">Test this key</button><button class="btn ghost" data-after-key-action="first-request">Send first request</button></div></div>`;
    renderLaunchNextAction({ keyCount: Math.max(1, Number(activationState.keyCount || 0)), keyVerified: false });
    if (recoveryIntent) {
      set('post-key-activation-status', 'Key recovered. Copy the sk_sage setup key now; then verify email and finish checkout to unlock hosted routing.');
    }
    trackAccountFunnelEvent('account_next_action_shown', { button: 'post_key_next_action', target: '/v1/models', state: 'verify_key' });
    refresh();
    return true;
  } catch (error) {
    trackAccountFunnelEvent('account_api_key_create_failed', {
      button: 'create_key',
      target: '/account/api-keys',
      state: billingFailureState(error, 'key_create_failed'),
    });
    set('key-once', error.message);
    return false;
  } finally {
    setBusy('create-key', false);
  }
}

function explainModelProbeFailure(status, data = {}) {
  const detail = data.error || data.message || `HTTP ${status}`;
  if (status === 401 || status === 403) {
    return `${detail}. Check that this is an active sk_sage key and has not been revoked.`;
  }
  if (status === 402) {
    return `${detail}. Choose a plan or finish checkout before routing generated keys.`;
  }
  if (status === 429) {
    return `${detail}. The key is valid, but the current rate limit or quota was reached.`;
  }
  if (status >= 500) {
    return `${detail}. The public edge or selected backend is degraded; check /status before retrying.`;
  }
  return detail;
}

async function testApiKey() {
  const key = $('test-api-key')?.value.trim() || currentRawKey;
  if (!key) {
    set('test-api-key-status', 'Create a key or paste an sk_sage key first.');
    return;
  }
  trackAccountFunnelEvent('account_key_verify_clicked', { button: 'test_api_key', target: '/v1/models', state: 'models' });
  set('test-api-key-status', 'Checking /v1/models through the public edge...');
  setBusy('test-api-key-button', true, 'Testing...');
  try {
    const res = await fetch(`${openaiBaseUrl}/models`, {
      headers: {
        Authorization: `Bearer ${key}`,
        Accept: 'application/json',
      },
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      set('test-api-key-status', explainModelProbeFailure(res.status, data));
      return;
    }
    const models = Array.isArray(data.data) ? data.data : [];
    const suffix = models.length ? ` ${fmtNumber(models.length)} models visible.` : ' The key reached the model API.';
    keyVerifiedThisSession = true;
    set('test-api-key-status', `Success: /v1/models returned HTTP ${res.status}.${suffix}`);
    trackAccountFunnelEvent('account_key_verified', { button: 'test_api_key', target: '/v1/models', state: 'success' });
    renderLaunchNextAction({ keyVerified: true });
  } catch (_error) {
    set('test-api-key-status', 'Could not reach the public edge from this browser. Check network access, CORS, or https://app.sagerouter.dev/status.');
  } finally {
    setBusy('test-api-key-button', false);
  }
}

async function sendTestChat() {
  const key = $('test-api-key')?.value.trim() || currentRawKey;
  if (!key) {
    set('test-chat-status', 'Create a key or paste an sk_sage key first.');
    return;
  }
  currentRawKey = key;
  trackAccountFunnelEvent('account_first_request_clicked', { button: 'test_chat', target: '/v1/responses', state: 'sage-router/frontier' });
  set('test-chat-status', 'Sending sage-router/frontier through the public edge Responses API...');
  setBusy('test-chat-button', true, 'Sending...');
  try {
    const res = await fetch(`${openaiBaseUrl}/responses`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${key}`,
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({
        model: 'sage-router/frontier',
        input: 'Reply with one short sentence confirming Sage Router is working.',
        max_output_tokens: 96,
      }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      set('test-chat-status', explainModelProbeFailure(res.status, data));
      return;
    }
    const text = data?.output_text || data?.output?.[0]?.content?.[0]?.text || data?.choices?.[0]?.message?.content || 'Completion returned.';
    keyVerifiedThisSession = true;
    set('test-chat-status', `First routed completion succeeded: ${String(text).slice(0, 220)}`);
    trackAccountFunnelEvent('account_first_request_succeeded', { button: 'test_chat', target: '/v1/responses', state: 'success' });
    renderLaunchNextAction({ keyVerified: true, requestCount: Math.max(1, Number(activationState.requestCount || 0)) });
    setTimeout(() => refresh(), 2500);
    setTimeout(() => refresh(), 9000);
  } catch (_error) {
    set('test-chat-status', 'Could not send the test request from this browser. Check network access, CORS, or https://app.sagerouter.dev/status.');
  } finally {
    setBusy('test-chat-button', false);
  }
}

async function runSignedInNextAction() {
  const action = signedInNextActionState();
  trackAccountFunnelEvent('account_next_action_clicked', {
    button: 'signed_in_next_action',
    target: action.target,
    state: action.state,
  });
  if (action.state === 'sign_in') {
    $('auth-panel')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }
  if (action.state === 'verify_email') {
    $('resend-verification-email')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    if (verificationEmail) await resendVerificationEmail();
    return;
  }
  if (action.state === 'create_key') {
    $('create-key')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    await createKey();
    return;
  }
  if (action.state === 'checkout') {
    if (stripeCheckoutReadyForPlan(selectedPlan)) await stripeCheckout({ button: 'signed_in_next_action', state: 'next_action_checkout' });
    else $('crypto-intent')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }
  if (action.state === 'verify_key') {
    if (!hasSessionApiKey()) {
      focusApiKeyVerifier('Paste the sk_sage key shown once above, or create a fresh key to populate the verifier.');
      return;
    }
    await testApiKey();
    return;
  }
  if (action.state === 'first_request') {
    if (!hasSessionApiKey()) {
      focusApiKeyVerifier('Paste the sk_sage key shown once above, or create a fresh key to send the first request.');
      return;
    }
    await sendTestChat();
    return;
  }
  if (action.state === 'dashboard') {
    window.location.href = '/analytics.html';
  }
}

async function stripeCheckout(options = {}) {
  let redirecting = false;
  const button = options.button || 'stripe_checkout';
  if (checkoutNeedsGeneratedKeyFirst()) {
    set('billing-status', 'Create the generated sk_sage setup key first. Checkout unlocks routing after the key exists.');
    trackAccountFunnelEvent('account_checkout_key_first_redirected', {
      button,
      target: '/account/api-keys',
      state: 'checkout_key_first',
    });
    $('create-key')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    const created = await createKey();
    if (created && !activationState.emailVerified) {
      set('email-verification-status', 'Setup key created. Verify your email next so checkout and hosted routing can unlock it.');
      $('resend-verification-email')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    return;
  }
  if (!stripeCheckoutReadyForPlan(selectedPlan)) {
    const message = stripeCheckoutUnavailableMessage(selectedPlan);
    set('billing-status', message);
    trackAccountFunnelEvent('account_checkout_unavailable', { button, target: '/billing/stripe/checkout', state: 'checkout_unavailable' });
    return;
  }
  setBusy('stripe-checkout', true, 'Opening...');
  try {
    set('billing-status', `Opening ${selectedPlan} checkout...`);
    trackAccountFunnelEvent('account_checkout_clicked', { button, target: '/billing/stripe/checkout', state: options.state || null });
    const data = await api('/billing/stripe/checkout', { method: 'POST', body: JSON.stringify({ plan: selectedPlan }) });
    if (data.checkout_url) {
      redirecting = true;
      window.location.href = data.checkout_url;
    }
  } catch (error) {
    trackAccountFunnelEvent('account_checkout_failed', {
      button,
      target: '/billing/stripe/checkout',
      state: billingFailureState(error, 'checkout_failed'),
    });
    set('billing-status', `${error.message}. If Stripe is not configured yet, use crypto/manual settlement or try again after billing setup is complete.`);
  } finally {
    if (!redirecting) setBusy('stripe-checkout', false);
  }
}

async function billingPortal() {
  let redirecting = false;
  setBusy('stripe-portal', true, 'Opening...');
  try {
    set('billing-status', 'Opening Stripe billing management...');
    trackAccountFunnelEvent('account_billing_portal_clicked', { button: 'stripe_portal', target: '/billing/stripe/portal' });
    const data = await api('/billing/stripe/portal', { method: 'POST', body: '{}' });
    if (data.portal_url) {
      redirecting = true;
      window.location.href = data.portal_url;
    }
  } catch (error) {
    trackAccountFunnelEvent('account_billing_portal_failed', {
      button: 'stripe_portal',
      target: '/billing/stripe/portal',
      state: billingFailureState(error, 'billing_portal_failed'),
    });
    set('billing-status', `${error.message}. Complete Stripe checkout before opening billing management.`);
  } finally {
    if (!redirecting) setBusy('stripe-portal', false);
  }
}

function describeManualPaymentIntent(intent = {}) {
  const metadata = intent.metadata || {};
  if (intent.status === 'settled_manual_review') {
    return `Manual payment settled for ${planDisplay(metadata.plan || selectedPlan)}. Routing activation can take a moment to refresh.`;
  }
  const pieces = [
    intent.status || 'pending_manual_review',
    `Send ${intent.amount || 'the agreed amount'} ${intent.asset || ''}`.trim(),
    intent.network ? `on ${intent.network}` : '',
    intent.address ? `to ${intent.address}` : '',
    intent.id ? `with intent id ${intent.id}` : '',
  ].filter(Boolean);
  return `${pieces.join(' ')}. Settlement is manual until an operator approves the payment.`;
}

async function cryptoIntent() {
  setBusy('crypto-intent', true, 'Creating...');
  try {
    set('crypto-status', 'Creating manual payment intent...');
    trackAccountFunnelEvent('account_crypto_intent_clicked', { button: 'crypto_intent', target: '/billing/crypto/intent' });
    const data = await api('/billing/crypto/intent', { method: 'POST', body: JSON.stringify({ note: `Sage Router ${selectedPlan} subscription`, plan: selectedPlan }) });
    const i = data.intent || {};
    lastManualPaymentIntentId = i.id || '';
    show('crypto-status-check', Boolean(lastManualPaymentIntentId));
    set('crypto-status', describeManualPaymentIntent(i));
    trackAccountFunnelEvent('account_crypto_intent_created', { button: 'crypto_intent', target: '/billing/crypto/intent', state: i.status || 'pending_manual_review' });
  } catch (error) {
    trackAccountFunnelEvent('account_crypto_intent_failed', {
      button: 'crypto_intent',
      target: '/billing/crypto/intent',
      state: billingFailureState(error, 'manual_payment_intent_failed'),
    });
    set('crypto-status', error.message);
  } finally {
    setBusy('crypto-intent', false);
  }
}

async function cryptoStatus() {
  if (!lastManualPaymentIntentId) {
    set('crypto-status', 'Create a manual payment intent before checking status.');
    return;
  }
  setBusy('crypto-status-check', true, 'Checking...');
  try {
    trackAccountFunnelEvent('account_crypto_status_clicked', { button: 'crypto_status', target: '/billing/crypto/status', state: 'manual_payment' });
    const data = await api(`/billing/crypto/status?id=${encodeURIComponent(lastManualPaymentIntentId)}`);
    const intent = data.intent || {};
    set('crypto-status', describeManualPaymentIntent(intent));
    trackAccountFunnelEvent('account_crypto_status_checked', { button: 'crypto_status', target: '/billing/crypto/status', state: intent.status || 'unknown' });
    if (intent.status === 'settled_manual_review') refresh();
  } catch (error) {
    trackAccountFunnelEvent('account_crypto_status_failed', {
      button: 'crypto_status',
      target: '/billing/crypto/status',
      state: billingFailureState(error, 'manual_payment_status_failed'),
    });
    set('crypto-status', error.message);
  } finally {
    setBusy('crypto-status-check', false);
  }
}

document.querySelectorAll('[data-oauth]').forEach((button) => button.addEventListener('click', () => {
  if (!button.disabled) {
    oauthLogin(button.dataset.oauth, {
      button: button.dataset.intentOauth ? `intent_${button.dataset.oauth}` : button.dataset.oauth,
      mirrorIntent: button.dataset.intentOauth === 'true',
    });
  }
}));
$('password-signup')?.addEventListener('click', passwordSignup);
$('password-login')?.addEventListener('click', passwordLogin);
$('magic-login')?.addEventListener('click', magicLogin);
$('resend-verification-email')?.addEventListener('click', resendVerificationEmail);
$('create-key')?.addEventListener('click', createKey);
$('test-api-key-button')?.addEventListener('click', testApiKey);
$('test-chat-button')?.addEventListener('click', sendTestChat);
$('stripe-checkout')?.addEventListener('click', stripeCheckout);
$('stripe-portal')?.addEventListener('click', billingPortal);
$('crypto-intent')?.addEventListener('click', cryptoIntent);
$('crypto-status-check')?.addEventListener('click', cryptoStatus);
$('signed-in-next-button')?.addEventListener('click', runSignedInNextAction);
$('key-recovery-email-focus')?.addEventListener('click', () => {
  trackAccountFunnelEvent('account_key_recovery_same_email_selected', {
    button: 'key_recovery_email_focus',
    target: '#intent-email',
    state: requestedKeyRecoveryStateFromUrl(),
  });
  set('key-recovery-dock-status', 'Enter the same signup email, then send the setup magic link.');
  focusEmailInput(true);
});
$('key-recovery-github')?.addEventListener('click', async () => {
  trackAccountFunnelEvent('account_key_recovery_github_selected', {
    button: 'key_recovery_github',
    target: '/auth/v1/authorize',
    state: 'github',
  });
  if (latestOauthExternalState?.github === false) {
    set('key-recovery-dock-status', 'GitHub OAuth is not enabled right now. Use the same-email magic link.');
    focusEmailInput(true);
    return;
  }
  set('key-recovery-dock-status', 'Opening GitHub. Continue only if it is the same signup account.');
  await oauthLogin('github', { button: 'key_recovery_github', mirrorIntent: true });
});
async function handleIntentPrimary(event) {
  event?.preventDefault?.();
  trackAccountFunnelEvent('account_intent_primary_clicked', {
    button: 'intent_primary',
    state: activationState.signedIn ? (activationState.routingEnabled ? 'routing_active' : 'signed_in') : 'signed_out',
    target: activationState.signedIn ? (activationState.keyCount ? '#billing' : '#create-key') : '#intent-email',
  });
  if (!activationState.signedIn) {
    await magicLogin({ button: 'intent_primary', preferIntent: true });
    return;
  }
  if (!activationState.keyCount) {
    const intentButton = $('intent-primary');
    setElementBusy(intentButton, true, 'Creating API key...');
    set('key-once', 'Creating your sk_sage key...');
    $('create-key')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    trackAccountFunnelEvent('account_intent_create_key_clicked', {
      button: 'intent_primary',
      target: '/account/api-keys',
      state: 'create_key_direct'
    });
    try {
      const created = await createKey();
      $('key-once')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      if (created && !activationState.emailVerified) {
        set('email-verification-status', 'Setup key created. Verify your email next so checkout and hosted routing can unlock it.');
        $('resend-verification-email')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    } finally {
      setElementBusy(intentButton, false);
    }
    return;
  }
  if (!activationState.emailVerified) {
    $('resend-verification-email')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }
  if (!activationState.routingEnabled) {
    if (stripeCheckoutReadyForPlan(selectedPlan)) {
      stripeCheckout();
    } else {
      $('crypto-intent')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    return;
  }
  const target = activationState.keyCount > 0 ? $('test-api-key') : $('create-key');
  target?.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
$('intent-email-form')?.addEventListener('submit', handleIntentPrimary);
if (!$('intent-email-form')) $('intent-primary')?.addEventListener('click', handleIntentPrimary);
$('sign-out')?.addEventListener('click', async () => { await sb.auth.signOut(); refresh(); });
$('plans')?.addEventListener('click', (event) => {
  const button = event.target?.closest?.('[data-plan]');
  if (!button) return;
  const plan = normalizePlan(button.dataset.plan);
  selectPlan(plan, `Selected ${planDisplay(plan)}.`);
  trackAccountFunnelEvent('account_plan_selected', { plan, button: 'plan_card' });
});
$('preauth-plans')?.addEventListener('click', (event) => {
  const button = event.target?.closest?.('[data-preauth-plan]');
  if (!button) return;
  const plan = normalizePlan(button.dataset.preauthPlan);
  selectPlan(plan);
  trackAccountFunnelEvent('account_plan_selected', { plan, button: 'preauth_plan' });
  set('auth-status', `Selected ${planDisplay(plan)}. Sign in to continue to checkout.`);
});
$('usage-upgrade')?.addEventListener('click', () => {
  if (!recommendedUpgradePlan) return;
  trackAccountFunnelEvent('account_usage_upgrade_clicked', { plan: recommendedUpgradePlan, button: 'usage_upgrade', state: 'quota_upgrade' });
  selectPlan(recommendedUpgradePlan, `Selected ${planDisplay(recommendedUpgradePlan)}. Continue to Stripe when ready.`);
  trackAccountFunnelEvent('account_plan_selected', { plan: recommendedUpgradePlan, button: 'usage_upgrade' });
  $('stripe-checkout')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
});
$('keys')?.addEventListener('click', async (event) => {
  const button = event.target?.closest?.('[data-revoke]');
  const id = button?.dataset?.revoke;
  if (!id) return;
  trackAccountFunnelEvent('account_api_key_revoke_clicked', { button: 'revoke_key', target: '/account/api-keys/{id}/revoke', state: 'revoke' });
  setElementBusy(button, true, 'Revoking...');
  try {
    await api(`/account/api-keys/${encodeURIComponent(id)}/revoke`, { method: 'POST', body: '{}' });
    trackAccountFunnelEvent('account_api_key_revoked', { button: 'revoke_key', target: '/account/api-keys/{id}/revoke', state: 'revoked' });
    refresh();
  } catch (error) {
    trackAccountFunnelEvent('account_api_key_revoke_failed', { button: 'revoke_key', target: '/account/api-keys/{id}/revoke', state: 'failed' });
    set('account-status', error.message);
    setElementBusy(button, false);
  }
});

function snippetIdForCopyTarget(targetId = '') {
  const snippets = {
    'raw-api-key-once': 'raw-api-key',
    'preauth-setup-code': 'preauth-setup-before-signup',
    'quickstart-code': 'quickstart-curl',
    'client-openai-code': 'openai-sdk',
    'client-codex-code': 'codex-cli',
    'client-anthropic-code': 'anthropic-compatible',
    'support-context-code': 'safe-support-context',
  };
  return snippets[targetId] || String(targetId || 'unknown').replace(/-code$/, '').slice(0, 80);
}

function trackAccountSnippetCopy(copyTarget, button, fallbackState = 'copied', originalLabel = '') {
  const isSupportContext = copyTarget === 'support-context-code';
  const label = button?.dataset?.copyLabel || originalLabel || button?.textContent || 'Copy';
  trackAccountFunnelEvent(isSupportContext ? 'account_support_context_copied' : 'account_snippet_copied', {
    button: label,
    target: `#${copyTarget}`,
    state: fallbackState,
    snippet: snippetIdForCopyTarget(copyTarget),
  });
  if (copyTarget === 'client-codex-code') {
    trackAccountFunnelEvent('account_post_key_codex_copied', {
      button: label || 'Copy Codex setup',
      target: '#client-codex-code',
      state: fallbackState,
      snippet: 'codex-cli',
    });
  }
}

document.addEventListener('click', async (event) => {
  const afterKeyButton = event.target?.closest?.('[data-after-key-action]');
  if (afterKeyButton) {
    if (afterKeyButton.dataset.afterKeyAction === 'first-request') {
      await sendTestChat();
    } else {
      await testApiKey();
    }
    return;
  }
  const postKeyButton = event.target?.closest?.('[data-post-key-action]');
  if (postKeyButton) {
    const action = postKeyButton.dataset.postKeyAction;
    if (!hasSessionApiKey()) {
      trackAccountFunnelEvent(action === 'first-request' ? 'account_post_key_first_request_clicked' : 'account_post_key_verify_clicked', {
        button: postKeyButton.textContent.trim() || action,
        target: action === 'first-request' ? '/v1/responses' : '/v1/models',
        state: 'missing_session_key',
      });
      focusApiKeyVerifier('Paste an existing sk_sage key or create a fresh key before running this step.');
      return;
    }
    if (action === 'first-request') {
      trackAccountFunnelEvent('account_post_key_first_request_clicked', { button: postKeyButton.textContent.trim() || 'Send first request', target: '/v1/responses', state: 'sage-router/frontier' });
      await sendTestChat();
    } else {
      trackAccountFunnelEvent('account_post_key_verify_clicked', { button: postKeyButton.textContent.trim() || 'Verify /v1/models', target: '/v1/models', state: 'models' });
      await testApiKey();
    }
    return;
  }
  const preauthNext = event.target?.closest?.('[data-preauth-focus-email]');
  if (preauthNext) {
    trackAccountFunnelEvent('account_preauth_setup_next_clicked', {
      button: preauthNext.textContent.trim() || 'Email setup link next',
      target: '#intent-email',
      state: 'preauth_setup_next',
      snippet: 'preauth-setup-before-signup',
    });
    set('intent-email-status', 'Enter your email to send the API key setup link.');
    focusEmailInput(true);
    return;
  }
  const button = event.target?.closest?.('[data-copy-target]');
  if (!button) return;
  const copyTarget = button.dataset.copyTarget;
  const target = $(copyTarget);
  const text = target?.textContent || '';
  if (!text) return;
  const original = button.textContent;
  const isSupportContext = copyTarget === 'support-context-code';
  try {
    await navigator.clipboard.writeText(text);
    button.textContent = 'Copied';
    if (isSupportContext) set('support-context-status', 'Safe support context copied.');
    trackAccountSnippetCopy(copyTarget, button, 'copied', original);
    if (button.id === 'post-key-copy-codex-button') {
      set('post-key-activation-status', 'Codex setup copied. Export the shown API key in your shell before running Codex.');
    }
  } catch (_error) {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(target);
    selection.removeAllRanges();
    selection.addRange(range);
    button.textContent = 'Selected';
    if (isSupportContext) set('support-context-status', 'Clipboard unavailable; safe support context selected.');
    trackAccountSnippetCopy(copyTarget, button, 'selected', original);
    if (button.id === 'post-key-copy-codex-button') {
      set('post-key-activation-status', 'Codex setup selected. Copy the selected text, then export the shown API key in your shell before running Codex.');
    }
  }
  setTimeout(() => { button.textContent = button.dataset.copyLabel || original || 'Copy'; }, 1200);
});
sb.auth.onAuthStateChange(() => refresh());
applyRequestedPlanFromUrl();
trackAccountFunnelEvent('account_viewed', {
  button: requestedPlanFromUrl() ? 'pricing_plan_link' : 'direct',
  state: requestedPlanFromUrl() ? 'plan_prefilled' : 'default',
});
if (pendingStartAction === 'create_key') {
  trackAccountFunnelEvent('account_key_recovery_viewed', {
    button: 'key_recovery_link',
    target: '/account.html',
    state: requestedKeyRecoveryStateFromUrl(),
  });
}
maybePrimeSetupHandoffLanding();
refresh();
handleBillingReturn();
applyAuthSettings();
scheduleAccountAuthNudge();
