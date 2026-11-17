# Node.js examples

Official SDK: https://github.com/sendpulse/sendpulse-rest-api-node.js
(`npm install sendpulse-api`). Below: zero-dependency `fetch` (Node 18+) with a
Single API Key — no token refresh needed.

## Minimal client

```js
const API = 'https://api.sendpulse.com';

async function api(method, path, body) {
  const res = await fetch(`${API}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${process.env.SENDPULSE_API_KEY}`,
      ...(body ? { 'Content-Type': 'application/json' } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (res.status === 429) throw new Error('Rate limited — retry with backoff');
  if (!res.ok) throw new Error(`SendPulse ${method} ${path}: ${res.status} ${await res.text()}`);
  return res.json();
}
```

## Book → subscribers → campaign

```js
// 1. Create an address book
const { id: bookId } = await api('POST', '/addressbooks', { bookName: 'Newsletter' });

// 2. Add subscribers (upsert: re-adding updates variables; dates YYYY-MM-DD)
await api('POST', `/addressbooks/${bookId}/emails`, {
  emails: [
    { email: 'jane@example.com', variables: { name: 'Jane', city: 'Berlin', signup_date: '2026-07-01' } },
    { email: 'john@example.com', variables: { name: 'John', city: 'Kyiv', signup_date: '2026-07-02' } },
  ],
});

// 3. Pre-flight
const senders = await api('GET', '/senders');            // sender_email must be here & active
const cost = await api('GET', `/addressbooks/${bookId}/cost`);

// 4. Create the campaign (body MUST be Base64; or pass template_id)
const html = '<h1>Hello {{name}}!</h1><p>Our July digest...</p>';
const campaign = await api('POST', '/campaigns', {
  name: 'July digest',
  sender_name: 'My Shop',
  sender_email: 'news@myshop.com',
  subject: 'Your July digest is here',
  body: Buffer.from(html).toString('base64'),
  list_id: bookId,
  send_date: '2026-07-10 10:00:00',   // omit to send ASAP
  stats: { opens: true, clicks: true, utm_campaign: 'july_digest' },
});

// 5. Status — may sit in review first (normal for new accounts).
//    Prefer the task_status_update webhook over polling.
const info = await api('GET', `/campaigns/${campaign.id}`);
```

## Analytics after sending

```js
const stats = await api('GET', `/campaigns/${campaign.id}`);
const countries = await api('GET', `/campaigns/${campaign.id}/countries`);
const links = await api('GET', `/campaigns/${campaign.id}/referrals`);   // clicks per link
const one = await api('GET', `/campaigns/${campaign.id}/email/${encodeURIComponent('jane@example.com')}`);
```

## Opt-out mirroring & suppression

```js
// Unsubscribe from one book
await api('POST', `/addressbooks/${bookId}/emails/unsubscribe`, {
  emails: ['jane@example.com'],
});

// Account-wide blacklist — NOTE: Base64 of a comma-separated STRING, not an array!
await api('POST', '/blacklist', {
  emails: Buffer.from('jane@example.com,spam@example.com').toString('base64'),
  comment: 'opted out in app',
});
```

## Webhook receiver sketch (Express)

```js
app.post('/hooks/sendpulse/:secret', express.json(), (req, res) => {
  if (req.params.secret !== process.env.SP_HOOK_SECRET) return res.sendStatus(403);
  const events = Array.isArray(req.body) ? req.body : [req.body];
  for (const event of events) queue.push(event); // process async; respond fast
  res.sendStatus(200);
});
// worker: unsubscribe/spam -> opt out; hard_bounces -> purge;
//         open/redirect -> engagement; task_status_update -> campaign dashboard
```

## OAuth variant (if not using an API key)

```js
const tok = await (await fetch(`${API}/oauth/access_token`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    grant_type: 'client_credentials',
    client_id: process.env.SENDPULSE_API_ID,
    client_secret: process.env.SENDPULSE_API_SECRET,
  }),
})).json(); // access_token, expires_in=3600 — cache ~55 min, refresh on 401
```
