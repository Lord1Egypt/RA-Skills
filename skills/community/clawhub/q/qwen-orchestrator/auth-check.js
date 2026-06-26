/**
 * Qwen Chat auth checker.
 * Uses Qwen-specific URL and DOM signals.
 */

const URL_PATTERNS = {
  LOGIN: [/login/i, /signin/i, /sign-in/i, /auth/i, /passport/i, /account/i],
  CAPTCHA: [/captcha/i, /challenge/i, /verify/i],
  RATE_LIMIT: [/rate.?limit/i, /too.?many/i],
};

async function checkAuth(page) {
  const result = {
    status: 'unknown',
    needsLogin: false,
    hasCaptcha: false,
    score: 0,
    details: {},
  };

  let pageUrl = '';
  try {
    pageUrl = page.url();
    result.details.url = pageUrl;
  } catch (e) {
    result.status = 'error';
    result.details.urlError = e.message;
    return result;
  }

  for (const pattern of URL_PATTERNS.LOGIN) {
    if (pattern.test(pageUrl)) {
      result.needsLogin = true;
      result.score -= 10;
      result.details.urlMatch = `login pattern: ${pattern}`;
      break;
    }
  }
  for (const pattern of URL_PATTERNS.CAPTCHA) {
    if (pattern.test(pageUrl)) {
      result.hasCaptcha = true;
      result.score -= 10;
      result.details.urlMatch = `captcha pattern: ${pattern}`;
      break;
    }
  }

  let domData;
  try {
    domData = await page.evaluate(() => {
      const bodyText = document.body?.innerText?.toLowerCase() || '';
      const hasComposer = !!(
        document.querySelector('#chat-input') ||
        document.querySelector('textarea#chat-input') ||
        document.querySelector('textarea[placeholder*="message" i]') ||
        document.querySelector('textarea[placeholder*="ask" i]') ||
        document.querySelector('textarea') ||
        document.querySelector('div[contenteditable="true"]') ||
        document.querySelector('div[role="textbox"]')
      );
      const hasSendButton = !!(
        document.querySelector('#send-message-button') ||
        document.querySelector('button[type="submit"]') ||
        document.querySelector('[data-testid="send"]') ||
        document.querySelector('button[aria-label*="send" i]')
      );
      const hasLoginForm = !!(
        document.querySelector('input[type="password"]') ||
        document.querySelector('input[name*="email" i]') ||
        document.querySelector('input[autocomplete="username"]') ||
        document.querySelector('form')?.innerText?.toLowerCase()?.includes('login')
      );
      const hasCaptcha = !!(
        document.querySelector('[class*="captcha" i]') ||
        document.querySelector('[id*="captcha" i]') ||
        document.querySelector('iframe[src*="captcha"]') ||
        bodyText.includes('captcha') ||
        bodyText.includes('verify you are human')
      );
      const hasQwenChatMarkers = !!(
        document.querySelector('[class*="message" i]') ||
        document.querySelector('[class*="markdown" i]') ||
        bodyText.includes('qwen') ||
        bodyText.includes('new chat')
      );
      return {
        bodyTextLen: bodyText.length,
        hasComposer,
        hasSendButton,
        hasLoginForm,
        hasCaptcha,
        hasQwenChatMarkers,
      };
    });
    result.details.dom = domData;
  } catch (e) {
    result.details.domError = e.message;
  }

  if (domData?.hasComposer) result.score += 5;
  if (domData?.hasSendButton) result.score += 2;
  if (domData?.hasQwenChatMarkers) result.score += 2;
  if (pageUrl.includes('chat.qwen.ai')) result.score += 2;
  if (/\/c\//.test(pageUrl)) result.score += 3;

  if (domData?.hasLoginForm) result.score -= 5;
  if (domData?.hasCaptcha) {
    result.hasCaptcha = true;
    result.score -= 10;
  }

  if (result.needsLogin || result.hasCaptcha || result.score < -2) {
    result.status = 'not_authenticated';
    result.needsLogin = true;
  } else if (result.score > 2 || domData?.hasComposer) {
    result.status = 'authenticated';
  } else {
    result.status = 'uncertain';
    result.details.uncertainReason = `score=${result.score}, hasComposer=${!!domData?.hasComposer}`;
  }

  return result;
}

async function requireAuth(page, tracer = null, logFn = console.log) {
  const auth = await checkAuth(page, tracer);

  const color = auth.status === 'authenticated' ? '\x1b[32m' : '\x1b[31m';
  const reset = '\x1b[0m';
  const icon = auth.status === 'authenticated' ? '✅' : auth.hasCaptcha ? '🚫' : '⚠️';

  logFn(`${color}${icon} [AUTH] ${auth.status}${reset} (score: ${auth.score})`);
  if (auth.details.url) logFn(`   URL: ${auth.details.url}`);
  if (auth.details.domError) logFn(`   DOM check failed: ${auth.details.domError}`);
  if (auth.status === 'uncertain') logFn(`   ⚠️ Неопределённое состояние: ${auth.details.uncertainReason}`);

  if (auth.needsLogin || auth.hasCaptcha) {
    logFn(`\x1b[31mТребуется авторизация в Qwen Chat. Запусти ask-qwen.sh --visible --wait --dry-run, войди вручную, затем повтори запрос.\x1b[0m`);
    return false;
  }

  return true;
}

module.exports = { checkAuth, requireAuth, AUTH_URL_PATTERNS: URL_PATTERNS };
