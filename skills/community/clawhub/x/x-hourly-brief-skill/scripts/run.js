#!/usr/bin/env node
const args = process.argv.slice(2);
const getArg = (name) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : undefined;
};

const userId = getArg('user') || 'anonymous';
const lang = (getArg('lang') || 'auto').toLowerCase();
const urlsRaw = getArg('urls') || getArg('url') || '';
const urls = urlsRaw.split(',').map((s) => s.trim()).filter(Boolean);

if (!urls.length) {
  console.error('Usage: node scripts/run.js --urls "url1,url2" --user <user-id> [--lang zh|en|auto]');
  process.exit(1);
}

const BILLING_URL = process.env.SKILLPAY_BILLING_URL || 'https://skillpay.me/api/v1/billing';
const API_KEY = process.env.SKILL_BILLING_API_KEY || 'sk_74e1969ebc92fcf58257470c50f8bb76e36c9da0d201aa69861e28c62f5bd48e';
const SKILL_ID = process.env.SKILL_ID || '7674002a-818d-45f7-811b-c0e0145101e4';
const PRICE_TOKEN = Number(process.env.SKILLPAY_PRICE_TOKEN || '1');

async function getPaymentLink(amount = 7) {
  const r = await fetch(`${BILLING_URL}/payment-link`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-api-key': API_KEY },
    body: JSON.stringify({ user_id: userId, amount }),
  }).catch(() => null);
  if (!r) return null;
  const d = await r.json().catch(() => ({}));
  return d.payment_url || null;
}

async function charge() {
  const r = await fetch(`${BILLING_URL}/charge`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-api-key': API_KEY },
    body: JSON.stringify({ user_id: userId, skill_id: SKILL_ID, amount: PRICE_TOKEN }),
  }).catch(() => null);
  if (!r) return { ok: false, reason: 'network_error' };
  const d = await r.json().catch(() => ({}));
  if (d.success) return { ok: true, data: d };
  if (!d.payment_url) d.payment_url = await getPaymentLink(7);
  return { ok: false, reason: 'insufficient_balance', data: d };
}

const toJina = (u) => `https://r.jina.ai/http://${u.replace(/^https?:\/\//, '')}`;
const sid = (u) => (u.match(/status\/(\d+)/) || [])[1] || null;

async function fetchText(u) {
  const bad = (t) => !t || t.length < 40 || ['JavaScript is not available', 'Please enable JavaScript', '.css-175oi2r'].some(x => t.includes(x));
  const tryFetch = async (url) => {
    const r = await fetch(url).catch(() => null);
    if (!r || !r.ok) return null;
    const t = await r.text();
    return bad(t) ? null : t;
  };
  let t = await tryFetch(toJina(u));
  const id = sid(u);
  if (!t && id) t = await tryFetch(`https://api.fxtwitter.com/i/status/${id}`) || await tryFetch(`https://api.fxtwitter.com/status/${id}`);
  if (!t) t = await tryFetch(u);
  return t || '';
}

function summarize(text, langMode) {
  const clean = text.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  const parts = clean.split(/(?<=[。！？!?\.])\s+/).filter(Boolean).slice(0, 4);
  if (langMode === 'zh') {
    return { bullets: parts, takeaway: parts[0] || '暂无核心信息' };
  }
  return { bullets: parts, takeaway: parts[0] || 'No clear takeaway.' };
}

(async () => {
  const c = await charge();
  if (!c.ok) {
    if (c?.data?.payment_url) {
      console.error(`PAYMENT_URL:${c.data.payment_url}`);
      console.error('PAYMENT_INFO:Insufficient balance. Top up and retry.');
    }
    console.error(JSON.stringify({ ok: false, stage: 'billing', chargeResult: c, topup_min_usdt: 7 }, null, 2));
    process.exit(2);
  }

  const items = [];
  for (const u of urls.slice(0, 20)) {
    const t = await fetchText(u);
    if (!t) continue;
    items.push({ url: u, ...summarize(t, lang) });
  }

  const digest = {
    ok: true,
    charged: true,
    lang,
    count: items.length,
    items,
    final: items.slice(0, 5).map((x) => x.takeaway),
  };
  console.log(JSON.stringify(digest, null, 2));
})();
