(function () {
  const SUPABASE_URL = 'https://awtangrlqqsdpksarhwo.supabase.co';
  const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3dGFuZ3JscXFzZHBrc2FyaHdvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMwMTYzNzEsImV4cCI6MjA4ODU5MjM3MX0.U7TmEJMgYMH0rR8tTWFQ2tzReO5syRwnI3Ytg-BbDaw';
  const SUPABASE_JS_URL = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
  const path = window.location.pathname || '/';
  const title = (document.querySelector('h1')?.textContent || document.title || 'Sage Router').trim();
  const articleSlug = attributionValue(path)?.replace(/^\/+/, '').replace(/\/+/g, '-') || 'article';
  const accountUrl = `https://app.sagerouter.dev/account.html?plan=pro&start=create_key&utm_source=article-dock&utm_medium=activation&utm_campaign=sage-router-launch&source_surface=article&utm_content=${encodeURIComponent(`${articleSlug}-pro-key`)}`;
  const accountEmailUrl = `https://app.sagerouter.dev/account.html?plan=pro&start=create_key&utm_source=article-dock&utm_medium=activation&utm_campaign=sage-router-launch&source_surface=article&utm_content=${encodeURIComponent(`${articleSlug}-email`)}`;
  const recoveryUrl = `https://app.sagerouter.dev/login.html?plan=pro&start=create_key&utm_source=article-dock&utm_medium=recovery&utm_campaign=signup_to_key_recovery&auth=email&source_surface=article&utm_content=${encodeURIComponent(`${articleSlug}-returning-user`)}`;
  const quickstartUrl = `/quickstart?utm_source=article-dock&utm_medium=activation&utm_campaign=sage-router-launch&utm_content=${encodeURIComponent(`${articleSlug}-quickstart`)}`;
  const calculatorUrl = `/model-routing-calculator?utm_source=article-dock&utm_medium=activation&utm_campaign=sage-router-launch&utm_content=${encodeURIComponent(`${articleSlug}-calculator`)}`;
  const managedAccessUrl = `/managed-access?intent=max-implementation&utm_source=article-dock&utm_medium=activation&utm_campaign=sage-router-launch&utm_content=${encodeURIComponent(`${articleSlug}-max-review`)}`;
  const hostedSetupBundle = `# Sage Router hosted setup
export OPENAI_BASE_URL=https://api.sagerouter.dev/v1
export OPENAI_API_KEY=sk_sage_REPLACE_WITH_GENERATED_KEY

# Create the generated key before checkout:
# ${accountUrl}

# OpenAI-compatible smoke test:
curl https://api.sagerouter.dev/v1/models \\
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Agent profile:
# model: sage-router/frontier
# Docs: https://sagerouter.dev/quickstart`;

  function attributionValue(value) {
    const sanitized = String(value || '')
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9._/-]+/g, '-')
      .slice(0, 100);
    return sanitized || undefined;
  }

  function accountUrlWithSetup(setup) {
    const url = new URL(accountUrl);
    if (setup) url.searchParams.set('setup', setup);
    return url.toString();
  }

  function track(event, extra = {}) {
    const params = new URLSearchParams(window.location.search);
    let referrerHost = '';
    try {
      referrerHost = document.referrer ? new URL(document.referrer).hostname : '';
    } catch {
      referrerHost = '';
    }
    const payload = JSON.stringify({
      event,
      plan: extra.plan || 'pro',
      sourcePage: window.location.href,
      source_page: window.location.href,
      target: extra.target || null,
      metadata: {
        source: 'article-dock',
        sourceSurface: 'article',
        articlePath: attributionValue(path),
        articleTitle: attributionValue(title),
        button: attributionValue(extra.button),
        state: attributionValue(extra.state),
        snippet: attributionValue(extra.snippet),
        utmSource: attributionValue(params.get('utm_source')),
        utmMedium: attributionValue(params.get('utm_medium')),
        utmCampaign: attributionValue(params.get('utm_campaign')),
        referrerHost: attributionValue(referrerHost),
      },
    });
    if (navigator.sendBeacon?.('/api/funnel-event', new Blob([payload], { type: 'application/json' }))) {
      return;
    }
    fetch('/api/funnel-event', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: payload,
      credentials: 'omit',
      keepalive: true,
    }).catch(() => {});
  }

  function loadSupabaseClient() {
    if (window.supabase?.createClient) {
      return Promise.resolve(window.supabase);
    }
    if (window.__sageRouterArticleSupabasePromise) {
      return window.__sageRouterArticleSupabasePromise;
    }
    window.__sageRouterArticleSupabasePromise = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = SUPABASE_JS_URL;
      script.async = true;
      script.onload = () => window.supabase?.createClient ? resolve(window.supabase) : reject(new Error('Supabase client unavailable'));
      script.onerror = () => reject(new Error('Supabase client failed to load'));
      document.head.appendChild(script);
    });
    return window.__sageRouterArticleSupabasePromise;
  }

  function makeLink(label, href, className, event, button) {
    const link = document.createElement('a');
    link.href = href;
    link.className = className;
    link.textContent = label;
    link.addEventListener('click', () => track(event, { target: href, button }));
    return link;
  }

  function makeStartKeyLink(id, label = 'Create API key') {
    const link = document.createElement('a');
    link.href = accountUrl;
    link.className = 'articleDockPrimary';
    link.textContent = label;
    link.addEventListener('click', () => track('content_article_key_activation_clicked', {
      target: accountUrl,
      button: id,
      state: 'direct-key-first',
    }));
    return link;
  }

  function upgradePlainAccountLinks() {
    document.querySelectorAll('a[href="https://app.sagerouter.dev/account.html"]').forEach((link) => {
      link.href = accountUrl;
      link.addEventListener('click', () => track('content_article_key_activation_clicked', {
        target: accountUrl,
        button: link.textContent?.trim() || 'account-nav',
        state: 'upgraded-account-link',
      }));
    });
    document.querySelectorAll('a[href*="app.sagerouter.dev/account.html?plan=pro&start=checkout"]').forEach((link) => {
      if (link.dataset.articleDockUpgraded === 'true') return;
      const upgraded = new URL(link.href);
      upgraded.searchParams.set('start', 'create_key');
      upgraded.searchParams.set('utm_source', upgraded.searchParams.get('utm_source') || 'article-dock');
      upgraded.searchParams.set('utm_medium', upgraded.searchParams.get('utm_medium') || 'activation');
      upgraded.searchParams.set('utm_campaign', upgraded.searchParams.get('utm_campaign') || 'sage-router-launch');
      upgraded.searchParams.set('utm_content', upgraded.searchParams.get('utm_content') || `${articleSlug}-checkout-upgrade`);
      link.href = upgraded.toString();
      link.dataset.articleDockUpgraded = 'true';
      link.addEventListener('click', () => track('content_article_key_activation_clicked', {
        target: upgraded.toString(),
        button: link.textContent?.trim() || 'article-account-link',
        state: 'upgraded-checkout-link',
      }));
    });
    document.querySelectorAll('a[href*="app.sagerouter.dev/account.html?"]').forEach((link) => {
      if (link.dataset.articleDockUpgraded === 'true') return;
      const upgraded = new URL(link.href);
      if (upgraded.searchParams.get('start') !== 'create_key') return;
      if (upgraded.searchParams.get('utm_source')) return;
      const button = attributionValue(link.dataset.articleButton || link.dataset.button || link.textContent || 'article-account-link') || 'article-account-link';
      upgraded.searchParams.set('utm_source', 'article-dock');
      upgraded.searchParams.set('utm_medium', 'activation');
      upgraded.searchParams.set('utm_campaign', 'sage-router-launch');
      upgraded.searchParams.set('utm_content', `${articleSlug}-${button}`);
      link.href = upgraded.toString();
      link.dataset.articleDockUpgraded = 'true';
      link.addEventListener('click', () => track('content_article_key_activation_clicked', {
        target: upgraded.toString(),
        button,
        state: 'upgraded-create-key-link',
      }));
    });
  }

  function makeOauthButton(id) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'articleDockSecondary articleDockButton';
    button.textContent = 'Continue with GitHub for Pro';
    button.addEventListener('click', async () => {
      button.disabled = true;
      track('content_article_oauth_clicked', {
        target: accountUrl,
        button: id,
        state: 'github',
      });
      try {
        const api = await loadSupabaseClient();
        const client = api.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        const { error } = await client.auth.signInWithOAuth({
          provider: 'github',
          options: { redirectTo: accountUrl },
        });
        if (error) throw error;
      } catch (_error) {
        track('content_article_oauth_failed', {
          target: accountUrl,
          button: id,
          state: 'github',
        });
        window.location.href = accountUrl;
      } finally {
        button.disabled = false;
      }
    });
    return button;
  }

  async function copyText(text) {
    if (navigator.clipboard?.writeText) {
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

  function makeCopyButton(id, label) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'articleDockSecondary articleDockButton';
    button.textContent = label;
    button.addEventListener('click', async () => {
      if (button.dataset.setupCopied === 'true') {
        const target = accountUrlWithSetup('article-hosted-setup');
        track('content_article_key_activation_clicked', {
          target,
          button: `${id}-create-key-next`,
          state: 'after-copy',
          snippet: 'article-hosted-setup',
        });
        window.location.href = target;
        return;
      }
      button.disabled = true;
      try {
        await copyText(hostedSetupBundle);
        button.dataset.setupCopied = 'true';
        button.textContent = 'Create API key next';
        track('content_article_snippet_copied', {
          target: accountUrlWithSetup('article-hosted-setup'),
          button: id,
          state: 'copied',
          snippet: 'article-hosted-setup',
        });
        setTimeout(() => {
          if (button.dataset.setupCopied === 'true') {
            delete button.dataset.setupCopied;
            button.textContent = label;
          }
        }, 12000);
      } catch (_error) {
        button.textContent = 'Open quickstart';
        track('content_article_quickstart_clicked', {
          target: quickstartUrl,
          button: id,
          state: 'copy-failed',
        });
        setTimeout(() => { window.location.href = quickstartUrl; }, 900);
      } finally {
        button.disabled = false;
      }
    });
    return button;
  }

  function makeEmailForm(id, buttonLabel) {
    const form = document.createElement('form');
    form.id = id;
    form.className = 'articleDockEmailForm';
    form.innerHTML = `
      <input type="email" name="email" autocomplete="email" inputmode="email" placeholder="work email" aria-label="Email address for Sage Router setup link" required>
      <button type="submit">${buttonLabel}</button>
      <small id="${id}-status" class="articleDockEmailStatus" aria-live="polite"></small>
    `;
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const emailInput = form.querySelector('input[type="email"]');
      const button = form.querySelector('button');
      const status = form.querySelector('.articleDockEmailStatus');
      const email = String(emailInput?.value || '').trim();
      if (!email) {
        status.textContent = 'Enter an email to get the setup link.';
        emailInput?.focus();
        return;
      }
      button.disabled = true;
      button.textContent = 'Sending...';
      status.textContent = 'Sending API key setup link...';
      track('content_article_magic_link_requested', {
        target: accountEmailUrl,
        button: id,
        state: 'email-start',
      });
      try {
        const api = await loadSupabaseClient();
        const client = api.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        const { error } = await client.auth.signInWithOtp({
          email,
          options: {
            emailRedirectTo: accountEmailUrl,
            data: {
              sage_router_onboarding: true,
              signup_source: 'article-dock',
              selected_plan: 'pro',
              auth_method: 'magic_link',
            },
          },
        });
        if (error) throw error;
        form.reset();
        track('content_article_magic_link_sent', {
          target: accountEmailUrl,
          button: id,
          state: 'email-start',
        });
        status.textContent = 'Check your email for the API key setup link.';
      } catch (_error) {
        track('content_article_magic_link_failed', {
          target: accountEmailUrl,
          button: id,
          state: 'email-start',
        });
        status.textContent = 'Email setup failed. Opening account setup...';
        setTimeout(() => { window.location.href = accountEmailUrl; }, 900);
      } finally {
        button.disabled = false;
        button.textContent = buttonLabel;
      }
    });
    return form;
  }

  function mountInlineOffer() {
    if (document.getElementById('article-activation-inline')) return;
    const main = document.querySelector('main');
    const firstSection = main?.querySelector('section');
    if (!main || !firstSection) return;

    const style = document.createElement('style');
    style.textContent = `
      #article-activation-inline{display:grid;grid-template-columns:minmax(220px,1fr) auto auto auto auto;gap:12px;align-items:center;margin:24px 0;padding:18px;border:1px solid rgba(141,240,178,.28);border-radius:14px;background:linear-gradient(135deg,rgba(141,240,178,.13),rgba(138,180,255,.08));box-shadow:0 18px 60px rgba(0,0,0,.18)}
      #article-activation-inline strong,#article-activation-inline span{display:block}
      #article-activation-inline strong{color:#edfdf5;font:900 18px/1.2 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
      #article-activation-inline span{margin-top:4px;color:#a9c5b8;font:500 14px/1.35 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
      #article-activation-inline a,#article-activation-inline .articleDockButton{min-height:44px;display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:0 16px;text-decoration:none;font:900 13px/1 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;white-space:nowrap}
      #article-activation-inline .articleDockButton{border:0;cursor:pointer}
      #article-activation-inline .articleDockPrimary{background:linear-gradient(135deg,#8df0b2,#50d891);color:#04150d}
      #article-activation-inline .articleDockSecondary{border:1px solid rgba(166,255,207,.2);background:rgba(255,255,255,.065);color:#edfdf5}
      #article-activation-inline .articleDockButton:disabled{opacity:.72;cursor:wait}
      .articleDockEmailForm{display:grid;grid-template-columns:minmax(160px,1fr) auto;gap:8px;align-items:center;min-width:min(100%,390px)}
      .articleDockEmailForm input{min-height:44px;border:1px solid rgba(166,255,207,.22);border-radius:999px;background:rgba(3,12,9,.72);color:#edfdf5;padding:0 14px;font:600 13px/1 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
      .articleDockEmailForm input::placeholder{color:#789184}
      .articleDockEmailForm button{min-height:44px;border:0;border-radius:999px;background:linear-gradient(135deg,#8df0b2,#50d891);color:#04150d;padding:0 14px;font:900 13px/1 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;cursor:pointer;white-space:nowrap}
      .articleDockEmailForm button:disabled{opacity:.72;cursor:wait}
      .articleDockEmailStatus{grid-column:1/-1;color:#a9c5b8;font:600 12px/1.25 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;min-height:15px}
      @media(max-width:820px){#article-activation-inline{grid-template-columns:1fr}#article-activation-inline a{width:100%}}
      @media(max-width:520px){.articleDockEmailForm{grid-template-columns:1fr}.articleDockEmailForm button{width:100%}}
    `;
    document.head.appendChild(style);

    const offer = document.createElement('aside');
    offer.id = 'article-activation-inline';
    offer.setAttribute('aria-label', 'Start Sage Router from this article');
    const copy = document.createElement('div');
    copy.innerHTML = '<strong>Create the generated key first.</strong><span>Then copy setup or finish checkout after the sk_sage key exists.</span>';
    offer.appendChild(copy);
    offer.appendChild(makeStartKeyLink('inline-direct-api-key', 'Create API key'));
    offer.appendChild(makeCopyButton('inline-copy-setup', 'Copy 60-second setup'));
    offer.appendChild(makeOauthButton('inline-github-pro'));
    offer.appendChild(makeEmailForm('article-activation-email-form', 'Email API key setup link'));
    offer.appendChild(makeLink('Already signed up? Finish key', recoveryUrl, 'articleDockSecondary', 'content_article_key_recovery_clicked', 'inline-returning-user'));
    offer.appendChild(makeLink('Request Max review', managedAccessUrl, 'articleDockSecondary', 'content_article_managed_access_clicked', 'inline-max-review'));
    firstSection.insertAdjacentElement('afterend', offer);
    track('content_article_inline_offer_viewed', { state: 'mounted' });
  }

  function mountDock() {
    if (document.getElementById('article-activation-dock')) return;
    const style = document.createElement('style');
    style.textContent = `
      #article-activation-dock{position:fixed;left:50%;bottom:18px;z-index:60;display:grid;grid-template-columns:minmax(220px,1fr) auto auto auto auto auto;gap:10px;align-items:center;width:min(1240px,calc(100vw - 32px));padding:12px;border:1px solid rgba(141,240,178,.35);border-radius:999px;background:rgba(7,16,13,.94);box-shadow:0 20px 80px rgba(0,0,0,.45);backdrop-filter:blur(18px)}
      #article-activation-dock strong,#article-activation-dock span{display:block}
      #article-activation-dock strong{color:#edfdf5;font:900 14px/1.2 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
      #article-activation-dock span{color:#a9c5b8;font:500 13px/1.25 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
      #article-activation-dock a,#article-activation-dock .articleDockButton{min-height:42px;display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:0 16px;text-decoration:none;font:900 13px/1 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;white-space:nowrap}
      #article-activation-dock .articleDockButton{border:0;cursor:pointer}
      #article-activation-dock .articleDockPrimary{background:linear-gradient(135deg,#8df0b2,#50d891);color:#04150d}
      #article-activation-dock .articleDockSecondary{border:1px solid rgba(166,255,207,.18);background:rgba(255,255,255,.055);color:#edfdf5}
      #article-activation-dock .articleDockButton:disabled{opacity:.72;cursor:wait}
      @media(max-width:920px){body{padding-bottom:240px!important}#article-activation-dock{grid-template-columns:1fr;border-radius:24px;align-items:stretch}#article-activation-dock a,#article-activation-dock .articleDockButton{width:100%}}
    `;
    document.head.appendChild(style);

    const dock = document.createElement('aside');
    dock.id = 'article-activation-dock';
    dock.setAttribute('aria-label', 'Sage Router activation');
    const copy = document.createElement('div');
    copy.innerHTML = '<strong>Create the key first.</strong><span>Get the generated sk_sage key before checkout; setup copy stays one click away.</span>';
    dock.appendChild(copy);
    dock.appendChild(makeStartKeyLink('sticky-direct-api-key', 'Create API key'));
    dock.appendChild(makeCopyButton('sticky-copy-setup', 'Copy 60-second setup'));
    dock.appendChild(makeOauthButton('sticky-github-pro'));
    dock.appendChild(makeEmailForm('article-activation-sticky-email-form', 'Email API key setup'));
    dock.appendChild(makeLink('Finish setup key', recoveryUrl, 'articleDockSecondary', 'content_article_key_recovery_clicked', 'sticky-returning-user'));
    dock.appendChild(makeLink('Estimate fit', calculatorUrl, 'articleDockSecondary', 'content_article_calculator_clicked', 'sticky-estimate-fit'));
    document.body.appendChild(dock);
    track('content_article_activation_dock_viewed', { state: 'mounted' });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      upgradePlainAccountLinks();
      mountInlineOffer();
      mountDock();
    }, { once: true });
  } else {
    upgradePlainAccountLinks();
    mountInlineOffer();
    mountDock();
  }
})();
