const SAGE_ROUTER_ACCOUNT_PAGE_BASE_URL = 'https://app.sagerouter.dev/account.html?plan=pro&start=create_key';
const SAGE_ROUTER_SUPABASE_URL = 'https://awtangrlqqsdpksarhwo.supabase.co';
const SAGE_ROUTER_SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3dGFuZ3JscXFzZHBrc2FyaHdvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMwMTYzNzEsImV4cCI6MjA4ODU5MjM3MX0.U7TmEJMgYMH0rR8tTWFQ2tzReO5syRwnI3Ytg-BbDaw';
const SAGE_ROUTER_HOSTED_SETUP_BUNDLE = `# Sage Router hosted setup
export OPENAI_BASE_URL=https://api.sagerouter.dev/v1
export OPENAI_API_KEY=sk_sage_REPLACE_WITH_GENERATED_KEY

curl https://api.sagerouter.dev/v1/chat/completions \\
  -H "Authorization: Bearer $OPENAI_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"model":"sage-router/auto","messages":[{"role":"user","content":"Route this through Sage Router."}],"max_tokens":80}'`;

function sageRouterActivationSlug(value) {
  const cleaned = String(value || '')
    .replace(/\.html$/i, '')
    .replace(/^\/+|\/+$/g, '')
    .replace(/[^a-z0-9]+/gi, '-')
    .replace(/^-+|-+$/g, '')
    .toLowerCase();
  return cleaned || 'shared-email-activation';
}

function activationSourceSlug() {
  return sageRouterActivationSlug(window.location.pathname || 'shared-email-activation');
}

function activationAccountUrl(content = 'email-setup-link') {
  const sourceParams = new URLSearchParams(window.location.search);
  const target = new URL(SAGE_ROUTER_ACCOUNT_PAGE_BASE_URL);
  const targetParams = target.searchParams;
  targetParams.set('plan', 'pro');
  targetParams.set('start', 'create_key');
  targetParams.set('auth', 'email');
  targetParams.set('utm_source', sourceParams.get('utm_source') || sourceParams.get('utmSource') || activationSourceSlug());
  targetParams.set('utm_medium', sourceParams.get('utm_medium') || sourceParams.get('utmMedium') || 'activation');
  targetParams.set('utm_campaign', sourceParams.get('utm_campaign') || sourceParams.get('utmCampaign') || 'sage-router-launch');
  targetParams.set('utm_content', sourceParams.get('utm_content') || sourceParams.get('utmContent') || content);
  return target.toString();
}

function loadSageRouterSupabaseClient() {
  return new Promise((resolve, reject) => {
    if (window.supabase?.createClient) {
      resolve(window.supabase);
      return;
    }
    const existing = document.querySelector('script[data-supabase-js]');
    if (existing) {
      existing.addEventListener('load', () => resolve(window.supabase), { once: true });
      existing.addEventListener('error', reject, { once: true });
      return;
    }
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
    script.async = true;
    script.defer = true;
    script.dataset.supabaseJs = 'true';
    script.addEventListener('load', () => resolve(window.supabase), { once: true });
    script.addEventListener('error', reject, { once: true });
    document.head.appendChild(script);
  });
}

function sageRouterAttribution(extra = {}) {
  const params = new URLSearchParams(window.location.search);
  let referrerHost = null;
  try {
    const referrer = document.referrer ? new URL(document.referrer) : null;
    referrerHost = referrer && referrer.host !== window.location.host ? referrer.host : null;
  } catch (_error) {
    referrerHost = null;
  }
  return {
    utmSource: params.get('utm_source') || params.get('utmSource') || null,
    utmMedium: params.get('utm_medium') || params.get('utmMedium') || null,
    utmCampaign: params.get('utm_campaign') || params.get('utmCampaign') || null,
    referrerHost,
    landingPath: window.location.pathname,
    ...extra,
  };
}

function trackSageRouterActivationEvent(event, source, data = {}) {
  const target = data.target || activationAccountUrl(data.content || 'email-setup-link');
  const payload = JSON.stringify({
    event,
    plan: data.plan || 'pro',
    sourcePage: window.location.href,
    target,
    metadata: sageRouterAttribution({
      source,
      button: data.button || null,
      state: data.state || null,
      snippet: data.snippet || null,
    }),
  });
  try {
    if (navigator.sendBeacon) {
      const blob = new Blob([payload], { type: 'application/json' });
      if (navigator.sendBeacon('/api/funnel-event', blob)) return;
    }
  } catch (_error) {
    // Marketing telemetry must not block activation.
  }
  fetch('/api/funnel-event', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: payload,
    keepalive: true,
    credentials: 'omit',
  }).catch(() => {});
}

async function copySageRouterText(text) {
  if (navigator.clipboard?.writeText && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return true;
  }
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.setAttribute('readonly', '');
  textarea.style.position = 'fixed';
  textarea.style.left = '-9999px';
  document.body.appendChild(textarea);
  textarea.select();
  const copied = document.execCommand('copy');
  textarea.remove();
  if (!copied) throw new Error('copy failed');
  return true;
}

function insertSageRouterSetupCopyButton(form) {
  if (form.querySelector('[data-shared-setup-copy]')) return;
  const eventPrefix = form.dataset.eventPrefix;
  if (!eventPrefix) return;
  const source = form.dataset.source || eventPrefix;
  const emailInput = form.querySelector('input[type="email"]');
  const submitButton = form.querySelector('button[type="submit"]');
  const button = document.createElement('button');
  button.type = 'button';
  button.className = submitButton?.className || 'button secondary';
  button.dataset.sharedSetupCopy = 'true';
  button.textContent = 'Copy setup first';
  button.addEventListener('click', async () => {
    const snippet = `${sageRouterActivationSlug(source)}-hosted-setup`;
    button.disabled = true;
    try {
      await copySageRouterText(SAGE_ROUTER_HOSTED_SETUP_BUNDLE);
      button.textContent = 'Create API key next';
      button.dataset.setupCopied = 'true';
      trackSageRouterActivationEvent('quickstart_snippet_copied', source, {
        button: 'shared-email-activation-copy-setup',
        state: 'copied-before-key',
        snippet,
        target: activationAccountUrl(`${eventPrefix}-copy-setup`),
      });
      setTimeout(() => {
        if (button.dataset.setupCopied === 'true') {
          delete button.dataset.setupCopied;
          button.textContent = 'Copy setup first';
        }
      }, 12000);
    } catch (_error) {
      button.textContent = 'Open quickstart';
      trackSageRouterActivationEvent('quickstart_snippet_copied', source, {
        button: 'shared-email-activation-copy-setup',
        state: 'copy-failed',
        snippet,
        target: '/quickstart',
      });
      setTimeout(() => { window.location.href = '/quickstart'; }, 900);
    } finally {
      button.disabled = false;
    }
  });
  if (submitButton) {
    submitButton.insertAdjacentElement('afterend', button);
  } else if (emailInput) {
    emailInput.insertAdjacentElement('afterend', button);
  } else {
    form.appendChild(button);
  }
}

async function submitSageRouterActivationForm(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const emailInput = form.querySelector('input[type="email"]');
  const button = form.querySelector('button[type="submit"]');
  const status = document.getElementById(form.dataset.statusId || '');
  const eventPrefix = form.dataset.eventPrefix;
  const source = form.dataset.source || eventPrefix;
  const email = (emailInput?.value || '').trim();
  const buttonLabel = button?.textContent?.trim() || 'Email API key setup link';

  if (!email) {
    if (status) status.textContent = 'Enter an email address to receive the setup link.';
    emailInput?.focus();
    return;
  }
  if (!eventPrefix) {
    window.location.href = activationAccountUrl('form-no-event-prefix');
    return;
  }

  const accountUrl = activationAccountUrl(`${eventPrefix}-email-setup-link`);
  if (button) {
    button.disabled = true;
    button.textContent = 'Sending...';
  }
  if (status) status.textContent = 'Sending API key setup link...';
  trackSageRouterActivationEvent(`${eventPrefix}_magic_link_requested`, source, {
    button: buttonLabel,
    state: 'email-start',
    target: accountUrl,
  });

  try {
    const api = await loadSageRouterSupabaseClient();
    const client = api.createClient(SAGE_ROUTER_SUPABASE_URL, SAGE_ROUTER_SUPABASE_ANON_KEY);
    const { error } = await client.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: accountUrl,
        data: {
          sage_router_onboarding: true,
          signup_source: source,
          selected_plan: 'pro',
          auth_method: 'magic_link',
        },
      },
    });
    if (error) throw error;
    form.reset();
    trackSageRouterActivationEvent(`${eventPrefix}_magic_link_sent`, source, {
      button: buttonLabel,
      state: 'email-start',
      target: accountUrl,
    });
    if (status) status.textContent = 'Check your email for the API key setup link. It opens generated-key setup with the Pro plan selected.';
  } catch (_error) {
    trackSageRouterActivationEvent(`${eventPrefix}_magic_link_failed`, source, {
      button: buttonLabel,
      state: 'email-start',
      target: accountUrl,
    });
    if (status) status.textContent = 'Email setup is unavailable right now. Opening account setup instead...';
    setTimeout(() => { window.location.href = accountUrl; }, 900);
  } finally {
    if (button) {
      button.disabled = false;
      button.textContent = buttonLabel;
    }
  }
}

function insertSageRouterOauthButton(form) {
  if (form.dataset.oauthActivation !== 'github') return;
  if (!form.dataset.eventPrefix) return;
  if (form.querySelector('[data-oauth-activation]') || form.querySelector('.oauthButton')) return;
  const status = document.getElementById(form.dataset.statusId || '');
  const eventPrefix = form.dataset.eventPrefix;
  const source = form.dataset.source || eventPrefix;
  const emailInput = form.querySelector('input[type="email"]');
  const accountUrl = activationAccountUrl(`${eventPrefix}-github-oauth`);
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'button primary oauthButton';
  button.dataset.oauthActivation = 'github';
  button.textContent = 'Continue with GitHub for Pro';
  button.addEventListener('click', async () => {
    if (status) status.textContent = 'Opening GitHub sign-in for Pro...';
    button.disabled = true;
    trackSageRouterActivationEvent(`${eventPrefix}_oauth_clicked`, source, {
      button: button.textContent,
      state: 'github',
      target: accountUrl,
    });
    try {
      const api = await loadSageRouterSupabaseClient();
      const client = api.createClient(SAGE_ROUTER_SUPABASE_URL, SAGE_ROUTER_SUPABASE_ANON_KEY);
      const { error } = await client.auth.signInWithOAuth({
        provider: 'github',
        options: {
          redirectTo: accountUrl,
        },
      });
      if (error) throw error;
    } catch (_error) {
      trackSageRouterActivationEvent(`${eventPrefix}_oauth_failed`, source, {
        button: button.textContent,
        state: 'github',
        target: accountUrl,
      });
      if (status) status.textContent = 'GitHub sign-in is unavailable right now. Opening account setup instead...';
      window.location.href = accountUrl;
    } finally {
      button.disabled = false;
    }
  });
  if (emailInput) {
    form.insertBefore(button, emailInput);
    return;
  }
  form.prepend(button);
}

document.querySelectorAll('[data-email-activation-form]').forEach((form) => {
  insertSageRouterSetupCopyButton(form);
  insertSageRouterOauthButton(form);
  form.addEventListener('submit', submitSageRouterActivationForm);
});
