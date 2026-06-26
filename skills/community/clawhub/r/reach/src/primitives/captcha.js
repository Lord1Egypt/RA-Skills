import pool from '../browser.js';

/**
 * CAPTCHA detection and solving primitive.
 *
 * Detects Cloudflare Turnstile, reCAPTCHA, and hCaptcha challenges,
 * then solves them via CapSolver API.
 *
 * Requires CAPSOLVER_API_KEY environment variable.
 */

const CAPSOLVER_API_URL = 'https://api.capsolver.com';

/**
 * Detect CAPTCHA type on a page.
 *
 * @param {import('playwright').Page} page - Playwright page instance
 * @returns {object} { type: 'turnstile'|'recaptcha'|'hcaptcha'|'none', sitekey, pageurl }
 */
export async function detectCaptcha(page) {
  const pageurl = page.url();

  // Check for Cloudflare Turnstile
  const turnstile = await page.evaluate(() => {
    // Look for cf-turnstile div
    const el = document.querySelector('.cf-turnstile, [data-sitekey][data-callback]');
    if (el) {
      return { sitekey: el.getAttribute('data-sitekey') };
    }

    // Look for turnstile iframe
    const iframe = document.querySelector('iframe[src*="challenges.cloudflare.com"]');
    if (iframe) {
      const src = iframe.getAttribute('src') || '';
      const match = src.match(/[?&]k=([^&]+)/);
      return { sitekey: match ? match[1] : null };
    }

    // Look for Cloudflare challenge text
    const bodyText = document.body?.innerText || '';
    if (bodyText.includes('Verify you are human') || bodyText.includes('Just a moment')) {
      return { sitekey: null };
    }

    return null;
  });

  if (turnstile) {
    return { type: 'turnstile', sitekey: turnstile.sitekey, pageurl };
  }

  // Check for reCAPTCHA
  const recaptcha = await page.evaluate(() => {
    // reCAPTCHA v2
    const el = document.querySelector('.g-recaptcha, [data-sitekey]');
    if (el) {
      return { sitekey: el.getAttribute('data-sitekey') };
    }

    // reCAPTCHA iframe
    const iframe = document.querySelector('iframe[src*="google.com/recaptcha"], iframe[src*="recaptcha/api"]');
    if (iframe) {
      const src = iframe.getAttribute('src') || '';
      const match = src.match(/[?&]k=([^&]+)/);
      return { sitekey: match ? match[1] : null };
    }

    // reCAPTCHA v3 script
    const script = document.querySelector('script[src*="recaptcha"]');
    if (script) {
      const src = script.getAttribute('src') || '';
      const match = src.match(/[?&]render=([^&]+)/);
      if (match && match[1] !== 'explicit') {
        return { sitekey: match[1] };
      }
    }

    return null;
  });

  if (recaptcha) {
    return { type: 'recaptcha', sitekey: recaptcha.sitekey, pageurl };
  }

  // Check for hCaptcha
  const hcaptcha = await page.evaluate(() => {
    const el = document.querySelector('.h-captcha, [data-sitekey]');
    if (el && (el.classList.contains('h-captcha') || document.querySelector('iframe[src*="hcaptcha.com"]'))) {
      return { sitekey: el.getAttribute('data-sitekey') };
    }

    const iframe = document.querySelector('iframe[src*="hcaptcha.com"]');
    if (iframe) {
      const src = iframe.getAttribute('src') || '';
      const match = src.match(/[?&]sitekey=([^&]+)/);
      return { sitekey: match ? match[1] : null };
    }

    return null;
  });

  if (hcaptcha) {
    return { type: 'hcaptcha', sitekey: hcaptcha.sitekey, pageurl };
  }

  return { type: 'none', sitekey: null, pageurl };
}

/**
 * Solve a CAPTCHA on the page using CapSolver API.
 *
 * @param {import('playwright').Page} page - Playwright page instance
 * @param {string} [solverApiKey] - CapSolver API key (falls back to CAPSOLVER_API_KEY env)
 * @returns {object} { success, type, token?, error? }
 */
export async function solveCaptcha(page, solverApiKey) {
  const apiKey = solverApiKey || process.env.CAPSOLVER_API_KEY;

  if (!apiKey) {
    console.log('[captcha] CAPTCHA solving not configured — set CAPSOLVER_API_KEY in .env');
    return { success: false, type: 'none', error: 'No CAPSOLVER_API_KEY configured' };
  }

  const detection = await detectCaptcha(page);

  if (detection.type === 'none') {
    return { success: true, type: 'none', message: 'No CAPTCHA detected' };
  }

  console.log(`[captcha] Detected ${detection.type} CAPTCHA on ${detection.pageurl}`);

  if (!detection.sitekey) {
    console.log('[captcha] Could not extract sitekey — cannot solve automatically');
    return { success: false, type: detection.type, error: 'Could not extract sitekey' };
  }

  try {
    const token = await solveWithCapSolver(apiKey, detection);

    if (!token) {
      return { success: false, type: detection.type, error: 'Solver returned no token' };
    }

    // Inject the solution token into the page
    const injected = await injectToken(page, detection, token);

    return { success: injected, type: detection.type, token: token.substring(0, 20) + '...' };
  } catch (e) {
    console.log(`[captcha] Solve failed: ${e.message}`);
    return { success: false, type: detection.type, error: e.message };
  }
}

/**
 * Create a task on CapSolver and poll for the result.
 */
async function solveWithCapSolver(apiKey, detection) {
  const taskTypeMap = {
    turnstile: 'AntiTurnstileTaskProxyLess',
    recaptcha: 'ReCaptchaV2TaskProxyLess',
    hcaptcha: 'HCaptchaTaskProxyLess',
  };

  const taskType = taskTypeMap[detection.type];
  if (!taskType) {
    throw new Error(`Unsupported CAPTCHA type: ${detection.type}`);
  }

  // Create task
  const createResponse = await globalThis.fetch(`${CAPSOLVER_API_URL}/createTask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      clientKey: apiKey,
      task: {
        type: taskType,
        websiteURL: detection.pageurl,
        websiteKey: detection.sitekey,
      },
    }),
  });

  const createResult = await createResponse.json();

  if (createResult.errorId !== 0) {
    throw new Error(`CapSolver createTask error: ${createResult.errorDescription || createResult.errorCode}`);
  }

  const taskId = createResult.taskId;
  console.log(`[captcha] CapSolver task created: ${taskId}`);

  // Poll for result (max 120 seconds)
  const maxAttempts = 60;
  for (let i = 0; i < maxAttempts; i++) {
    await new Promise(r => setTimeout(r, 2000));

    const getResponse = await globalThis.fetch(`${CAPSOLVER_API_URL}/getTaskResult`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        clientKey: apiKey,
        taskId,
      }),
    });

    const getResult = await getResponse.json();

    if (getResult.errorId !== 0) {
      throw new Error(`CapSolver getTaskResult error: ${getResult.errorDescription || getResult.errorCode}`);
    }

    if (getResult.status === 'ready') {
      console.log(`[captcha] Solution received after ${(i + 1) * 2}s`);
      return getResult.solution?.token || getResult.solution?.gRecaptchaResponse;
    }

    if (getResult.status === 'failed') {
      throw new Error('CapSolver task failed');
    }
  }

  throw new Error('CapSolver timeout — no solution after 120 seconds');
}

/**
 * Inject the solved CAPTCHA token into the page.
 */
async function injectToken(page, detection, token) {
  switch (detection.type) {
    case 'turnstile': {
      await page.evaluate((t) => {
        // Set the hidden input value
        const input = document.querySelector('[name="cf-turnstile-response"], input[name*="turnstile"]');
        if (input) input.value = t;

        // Try calling the Turnstile callback
        const el = document.querySelector('.cf-turnstile, [data-callback]');
        if (el) {
          const callbackName = el.getAttribute('data-callback');
          if (callbackName && typeof window[callbackName] === 'function') {
            window[callbackName](t);
          }
        }

        // Also try the global turnstile object
        if (window.turnstile && typeof window.turnstile._callbacks === 'object') {
          for (const cb of Object.values(window.turnstile._callbacks)) {
            if (typeof cb === 'function') cb(t);
          }
        }
      }, token);
      console.log('[captcha] Turnstile token injected');
      return true;
    }

    case 'recaptcha': {
      await page.evaluate((t) => {
        // Set the textarea value
        const textarea = document.querySelector('#g-recaptcha-response, textarea[name="g-recaptcha-response"]');
        if (textarea) {
          textarea.value = t;
          textarea.style.display = 'block';
        }

        // Call the callback
        if (typeof window.___grecaptcha_cfg !== 'undefined') {
          const clients = window.___grecaptcha_cfg?.clients;
          if (clients) {
            for (const client of Object.values(clients)) {
              // Walk the client tree to find callback
              const walk = (obj) => {
                if (!obj || typeof obj !== 'object') return;
                for (const val of Object.values(obj)) {
                  if (typeof val === 'function') {
                    try { val(t); } catch {}
                  } else if (typeof val === 'object') {
                    walk(val);
                  }
                }
              };
              walk(client);
            }
          }
        }
      }, token);
      console.log('[captcha] reCAPTCHA token injected');
      return true;
    }

    case 'hcaptcha': {
      await page.evaluate((t) => {
        // Set the textarea
        const textarea = document.querySelector('[name="h-captcha-response"], textarea[name="g-recaptcha-response"]');
        if (textarea) textarea.value = t;

        // Set the hidden input
        const input = document.querySelector('[name="h-captcha-response"]');
        if (input) input.value = t;

        // Call hcaptcha callback
        if (window.hcaptcha) {
          try {
            // Trigger the callback registered with hcaptcha
            const iframe = document.querySelector('iframe[src*="hcaptcha.com"]');
            if (iframe) {
              const widgetId = iframe.getAttribute('data-hcaptcha-widget-id');
              if (widgetId) {
                window.hcaptcha.execute(widgetId, { response: t });
              }
            }
          } catch {}
        }
      }, token);
      console.log('[captcha] hCaptcha token injected');
      return true;
    }

    default:
      return false;
  }
}

/**
 * Auto-solve: detect and solve any CAPTCHA on the page.
 * Designed to be called after page navigation in the browser pool.
 *
 * @param {import('playwright').Page} page
 * @returns {object} Result of solve attempt
 */
export async function autoSolveCaptcha(page) {
  const detection = await detectCaptcha(page);
  if (detection.type === 'none') return null;

  console.log(`[captcha] Auto-detected ${detection.type} on ${detection.pageurl}`);
  return solveCaptcha(page);
}
