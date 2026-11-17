# Node.js examples

Official SDK: https://github.com/sendpulse/sendpulse-rest-api-node.js
(`npm install sendpulse-api`). Below: a modern zero-dependency client using
`fetch` (Node 18+). For classic SMTP relay via nodemailer see
[../references/smtp-relay.md](../references/smtp-relay.md).

## Minimal client with token caching

```js
const API_BASE = 'https://api.sendpulse.com';

let tokenCache = { token: null, expiresAt: 0 };

async function getToken() {
  if (tokenCache.token && Date.now() < tokenCache.expiresAt) {
    return tokenCache.token;
  }
  const res = await fetch(`${API_BASE}/oauth/access_token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'client_credentials',
      client_id: process.env.SENDPULSE_API_ID,
      client_secret: process.env.SENDPULSE_API_SECRET,
    }),
  });
  if (!res.ok) throw new Error(`SendPulse auth failed: ${res.status} ${await res.text()}`);
  const data = await res.json();
  tokenCache = {
    token: data.access_token,
    expiresAt: Date.now() + (data.expires_in - 60) * 1000, // refresh 1 min early
  };
  return tokenCache.token;
}

async function api(method, path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${await getToken()}`,
      ...(body ? { 'Content-Type': 'application/json' } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (res.status === 429) throw new Error('Rate limited — retry with backoff');
  if (!res.ok) throw new Error(`SendPulse ${method} ${path} failed: ${res.status} ${await res.text()}`);
  return res.json();
}

async function sendEmail({ subject, fromName, fromEmail, toName = '', toEmail, html, text }) {
  const result = await api('POST', '/smtp/emails', {
    email: {
      subject,
      from: { name: fromName, email: fromEmail },
      to: [{ name: toName, email: toEmail }],
      html: Buffer.from(html).toString('base64'), // html MUST be base64
      text,
    },
  });
  if (!result.result) throw new Error(`SendPulse rejected the email: ${JSON.stringify(result)}`);
  return result.id; // store it for status lookups
}

const id = await sendEmail({
  subject: 'Order confirmed',
  fromName: 'My Shop',
  fromEmail: 'noreply@myshop.com', // verified sender!
  toName: 'Jane',
  toEmail: 'jane@example.com',
  html: '<h1>Hello!</h1><p>Your order #1234 is confirmed.</p>',
  text: 'Hello! Your order #1234 is confirmed.',
});
console.log('Message id:', id);
```

## Template with variables & attachment

```js
import { readFile } from 'node:fs/promises';

const pdf = await readFile('invoice.pdf');

await api('POST', '/smtp/emails', {
  email: {
    subject: 'Your invoice',
    from: { name: 'My Shop', email: 'billing@myshop.com' },
    to: [{ email: 'jane@example.com' }],
    template: { id: 12345, variables: { name: 'Jane', order_id: '1234' } },
    attachments_binary: { 'invoice.pdf': pdf.toString('base64') },
  },
});
```

## Hygiene: blocklist check, status, bounces

```js
// 1. Never send to unsubscribed addresses
const check = await api('GET',
  `/smtp/unsubscribe/search?email=${encodeURIComponent('jane@example.com')}`);

// 2. Delivery status of a sent message
const status = await api('GET', `/smtp/emails/${id}`);

// 3. Daily cron: pull bounces, purge hard bounces from your own database
const bounces = await api('GET', '/smtp/bounces/day');

// 4. User opted out in your app -> mirror it to SendPulse
await api('POST', '/smtp/unsubscribe', {
  emails: [{ email: 'jane@example.com', comment: 'opted out in app' }],
});
```

## Notes

- On 429 retry with exponential backoff (`await setTimeout(2 ** attempt * 1000)`
  from `node:timers/promises`); don't retry 4xx validation errors.
- Bulk status: `POST /smtp/emails/info` with `{ emails: [id1, id2, ...] }` — up to
  500 ids per call.
