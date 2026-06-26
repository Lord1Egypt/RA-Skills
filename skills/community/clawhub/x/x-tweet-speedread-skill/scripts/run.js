#!/usr/bin/env node
/**
 * X Tweet Speedread Skill (Direct mode, no custom backend)
 * 1) Charge via SkillPay
 * 2) Fetch X post text with fallback
 * 3) Output English speedread summary
 */

const args = process.argv.slice(2);
const getArg = (name) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : undefined;
};

const url = getArg('url');
const userId = getArg('user') || 'anonymous';

if (!url) {
  console.error('Usage: node scripts/run.js --url <x-status-url> --user <user-id>');
  process.exit(1);
}

const BILLING_URL = process.env.SKILLPAY_BILLING_URL || 'https://skillpay.me/api/v1/billing';
const SKILL_BILLING_API_KEY = process.env.SKILL_BILLING_API_KEY || 'sk_74e1969ebc92fcf58257470c50f8bb76e36c9da0d201aa69861e28c62f5bd48e';
const SKILL_ID = process.env.SKILL_ID || '607813fc-caa5-4bd6-86fb-651f4cc6deb9';
const SKILLPAY_PRICE_TOKEN = Number(process.env.SKILLPAY_PRICE_TOKEN || '1');

async function getPaymentLink(userId, amount = 7) {
  const endpoint = `${BILLING_URL}/payment-link`;
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-api-key': SKILL_BILLING_API_KEY,
    },
    body: JSON.stringify({ user_id: userId, amount }),
  }).catch(() => null);
  if (!res) return null;
  try {
    const data = await res.json();
    return data?.payment_url || null;
  } catch {
    return null;
  }
}

async function charge() {
  if (!SKILL_BILLING_API_KEY || !SKILL_ID) {
    return { ok: false, reason: 'missing_billing_config' };
  }

  const endpoint = `${BILLING_URL}/charge`;
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-api-key': SKILL_BILLING_API_KEY,
    },
    body: JSON.stringify({
      user_id: userId,
      skill_id: SKILL_ID,
      amount: SKILLPAY_PRICE_TOKEN,
      meta: { source: 'x-tweet-speedread-skill' },
    }),
  }).catch(() => null);

  if (!res) return { ok: false, reason: 'network_error' };
  let data = null;
  try { data = await res.json(); } catch {}
  if (!res.ok || !data) return { ok: false, reason: 'charge_failed', data };
  if (data.success) return { ok: true, data };

  const paymentUrl = await getPaymentLink(userId, 7);
  if (paymentUrl) data.payment_url = paymentUrl;
  return { ok: false, reason: 'insufficient_balance', data };
}

function toJina(u) {
  return `https://r.jina.ai/http://${u.replace(/^https?:\/\//, '')}`;
}

function extractStatusId(u) {
  const m = u.match(/status\/(\d+)/);
  return m ? m[1] : null;
}

async function fetchText() {
  const attempts = [];

  const looksBad = (t) => {
    if (!t || t.length < 40) return true;
    const badMarkers = [
      'JavaScript is not available',
      'stylesheet-group',
      'Please enable JavaScript',
      '.css-175oi2r',
    ];
    return badMarkers.some((m) => t.includes(m));
  };

  const tryFetch = async (label, target) => {
    const r = await fetch(target).catch(() => null);
    if (!r || !r.ok) {
      attempts.push({ label, ok: false });
      return null;
    }
    const t = await r.text();
    if (looksBad(t)) {
      attempts.push({ label, ok: false, reason: 'bad_content' });
      return null;
    }
    attempts.push({ label, ok: true });
    return t;
  };

  let text = await tryFetch('jina', toJina(url));

  const sid = extractStatusId(url);
  if (!text && sid) {
    text = await tryFetch('fxtwitter-i', `https://api.fxtwitter.com/i/status/${sid}`);
    if (!text) text = await tryFetch('fxtwitter', `https://api.fxtwitter.com/status/${sid}`);
  }

  if (!text) text = await tryFetch('direct', url);

  return { text: text || '', attempts };
}

function clean(raw) {
  return raw
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .replace(/Title:\s*/gi, '')
    .trim();
}

function splitSentences(text) {
  return text
    .split(/(?<=[。！？!?\.])\s+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

function summarizeEn(text) {
  const s = splitSentences(text);
  const picks = s.slice(0, 5);
  const core = picks[0] || 'No clear core point found.';
  return {
    bullets: picks,
    core,
    risks: [
      'The post may contain subjective bias and should be verified.',
      'Income/performance claims may be non-reproducible.',
      'Use small-scale validation before any paid or trading action.',
    ],
    actions: [
      'Run a low-cost reproducibility test first.',
      'Split workflow into input → processing → output → billing.',
      'Track 7-day data before scaling effort or spend.',
    ],
  };
}

(async () => {
  const chargeResult = await charge();
  if (chargeResult.ok !== true) {
    const paymentUrl = chargeResult?.data?.payment_url || null;
    if (paymentUrl) {
      console.error(`PAYMENT_URL:${paymentUrl}`);
      console.error('PAYMENT_INFO:Insufficient balance. Top up and retry this same command.');
    }
    console.error(JSON.stringify({
      ok: false,
      stage: 'billing',
      code: chargeResult?.reason || 'billing_failed',
      message: 'Billing required: charge failed, config missing, or insufficient balance',
      payment_url: paymentUrl,
      topup_min_usdt: 7,
      chargeResult,
    }, null, 2));
    process.exit(2);
  }

  const { text, attempts } = await fetchText();
  if (!text) {
    console.error(JSON.stringify({ ok: false, stage: 'fetch', attempts }, null, 2));
    process.exit(3);
  }

  const cleaned = clean(text);
  const summary = summarizeEn(cleaned);

  console.log(JSON.stringify({
    ok: true,
    charged: true,
    billing: chargeResult,
    attempts,
    input: url,
    summary,
  }, null, 2));
})();
