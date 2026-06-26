#!/usr/bin/env node

const args = process.argv.slice(2);
const getArg = (name) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : undefined;
};

const url = getArg('url');
const article = getArg('article');
const userId = getArg('user') || 'anonymous';

if ((!url && !article) || (url && article)) {
  console.error('Usage: node scripts/run.js --url <x-status-url> OR --article <x-article-url> --user <user-id>');
  process.exit(1);
}

const BILLING_URL = process.env.SKILLPAY_BILLING_URL || 'https://skillpay.me/api/v1/billing';
const API_KEY = process.env.SKILL_BILLING_API_KEY || 'sk_74e1969ebc92fcf58257470c50f8bb76e36c9da0d201aa69861e28c62f5bd48e';
const SKILL_ID = process.env.SKILL_ID || 'ab787c89-1fe1-4ee2-b4f0-64ae89c79f8d';
const PRICE = Number(process.env.SKILLPAY_PRICE_TOKEN || '1');

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
    body: JSON.stringify({ user_id: userId, skill_id: SKILL_ID, amount: PRICE }),
  }).catch(() => null);
  if (!r) return { ok: false, reason: 'network_error' };
  const d = await r.json().catch(() => ({}));
  if (d.success) return { ok: true, data: d };
  const pay = await getPaymentLink(7);
  if (pay) d.payment_url = pay;
  return { ok: false, reason: 'insufficient_balance', data: d };
}

function statusId(u) {
  const m = u.match(/status\/(\d+)/);
  return m ? m[1] : null;
}

async function fetchTextDirect(u) {
  const r = await fetch(u).catch(() => null);
  if (!r || !r.ok) return null;
  const t = await r.text();
  if (!t || t.length < 40) return null;
  return t;
}

async function fetchViaJina(u) {
  const j = `https://r.jina.ai/http://${u.replace(/^https?:\/\//, '')}`;
  const r = await fetch(j).catch(() => null);
  if (!r || !r.ok) return null;
  const t = await r.text();
  return t && t.length > 40 ? t : null;
}

async function fetchTweet(u) {
  const id = statusId(u);
  if (id) {
    const api = await fetch(`https://api.fxtwitter.com/status/${id}`).catch(() => null);
    if (api && api.ok) {
      const d = await api.json().catch(() => null);
      if (d?.tweet?.text) {
        return {
          mode: 'tweet',
          source: 'fxtwitter',
          data: {
            text: d.tweet.text,
            author: d.tweet.author?.name || null,
            screen_name: d.tweet.author?.screen_name || null,
            likes: d.tweet.likes ?? null,
            retweets: d.tweet.retweets ?? null,
            views: d.tweet.views ?? null,
            created_at: d.tweet.created_timestamp || null,
            original_url: u,
          },
        };
      }
    }
  }

  const txt = await fetchViaJina(u) || await fetchTextDirect(u);
  if (!txt) return null;
  return {
    mode: 'tweet',
    source: 'jina/direct',
    data: {
      text: txt.slice(0, 12000),
      original_url: u,
    },
  };
}

async function fetchArticle(u) {
  const txt = await fetchViaJina(u) || await fetchTextDirect(u);
  if (!txt) return null;
  const lines = txt.split('\n').map(s => s.trim()).filter(Boolean);
  const title = lines.find(x => !x.startsWith('URL Source:') && !x.startsWith('Markdown Content:') && x.length > 10) || 'X Article';
  return {
    mode: 'article',
    source: 'jina/direct',
    data: {
      title,
      full_text: txt.slice(0, 50000),
      original_url: u,
    },
  };
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

  const result = url ? await fetchTweet(url) : await fetchArticle(article);
  if (!result) {
    console.error(JSON.stringify({ ok: false, stage: 'fetch', message: 'fetch_failed' }, null, 2));
    process.exit(3);
  }

  console.log(JSON.stringify({ ok: true, charged: true, ...result }, null, 2));
})();
