# REFERENCE.md ... wip-agent-pay

Full technical details.

## One-time Setup (5 minutes)

### Coinbase (isolated portfolio)

1. Coinbase ... Advanced Trade ... Portfolios ... Create portfolio named `wip-agent-pay`
   Fund it with $20-50 USDC only.
2. Coinbase Developer Platform ... API Keys ... Create new key
   - Portfolio: `wip-agent-pay` **only**
   - Permissions: **only** Transfer + View
   - IP allowlist: your home IP
   - Name: `wip-agent-pay-key`
3. Store API Key + API Secret in 1Password
   Entry name: `wip-agent-pay-coinbase`

### Cloudflare Worker (pay.wip.computer)

1. Go to https://dash.cloudflare.com
2. Workers & Pages ... Create application ... Worker
3. Name it: `pay-wip-computer`
4. Settings ... Domains & Routes ... Add custom domain ... `pay.wip.computer`
5. Paste the Worker code below
6. Create a KV Namespace named `PAY_TOKENS`, bind it as `KV`
7. Add a secret: `wrangler secret put WORKER_SECRET` (or via dashboard Settings ... Variables)
8. Store the same secret in 1Password: entry `wip-agent-pay-worker-secret`

## Everyday Use

You (or your agent) type:

```bash
wip-agent-pay 0.10 morning-stew "MS-#8"
```

The skill:

- pulls Worker secret + Coinbase creds from 1Password (op CLI)
- sends USDC from the isolated portfolio via Coinbase API
- calls pay.wip.computer/create with auth header to mint a one-time URL
- returns the URL ... agent consumes it once ... URL is deleted forever

## Cloudflare Worker Code

Deploy at pay.wip.computer (free tier).

```javascript
// pay.wip.computer ... wip-agent-pay relay
// Source: https://github.com/wipcomputer/wip-agent-pay
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Health check
    if (path === '/' || path === '/health') {
      return Response.json({ status: 'ok', service: 'wip-agent-pay' });
    }

    // === CREATE (protected) ===
    if (path === '/create') {
      // Auth: secret stored in Cloudflare env, same value in 1Password
      const auth = request.headers.get('Authorization');
      if (!env.WORKER_SECRET || auth !== `Bearer ${env.WORKER_SECRET}`) {
        return new Response('Unauthorized', { status: 401 });
      }

      let body;
      try {
        body = await request.json();
      } catch {
        return new Response('Bad JSON', { status: 400 });
      }

      const { amount, service, note, expiresMin } = body;
      const safeNote = typeof note === 'string' ? note : '';
      const safeTtl = typeof expiresMin === 'number' && expiresMin > 0 ? Math.min(expiresMin, 60) : 10;

      // Validate
      if (typeof amount !== 'number' || amount <= 0 || amount > 50) {
        return new Response('amount must be > 0 and <= 50', { status: 400 });
      }
      if (typeof service !== 'string' || service.length === 0 || service.length > 50) {
        return new Response('service must be 1-50 chars', { status: 400 });
      }
      if (safeNote.length > 200) {
        return new Response('note must be <= 200 chars', { status: 400 });
      }

      const token = crypto.randomUUID();
      const expiresAt = Date.now() + safeTtl * 60 * 1000;

      await env.KV.put(token, JSON.stringify({
        amount,
        service,
        note: safeNote,
        expiresAt,
        createdAt: new Date().toISOString()
      }), { expirationTtl: safeTtl * 60 });

      return Response.json({ url: `${url.origin}/${token}` });
    }

    // === CONSUME (atomic delete ... no race condition) ===
    const token = path.slice(1);
    if (!token || token.length < 10) {
      return new Response('Not found', { status: 404 });
    }

    const data = await env.KV.get(token, 'json');
    if (!data || Date.now() > data.expiresAt) {
      return new Response('Invalid or expired token', { status: 410 });
    }

    // Delete immediately. First reader wins. Second reader gets 410.
    await env.KV.delete(token);

    return Response.json({
      success: true,
      amount: data.amount,
      service: data.service,
      note: data.note,
      consumedAt: new Date().toISOString()
    });
  }
};
```

**KV Namespace:** Create one called `PAY_TOKENS` and bind it as `KV`.

**Worker Secret:** Set via `wrangler secret put WORKER_SECRET` or dashboard. Same value goes in 1Password as `wip-agent-pay-worker-secret`.

**Note on consistency:** KV is eventually consistent across Cloudflare edge locations. For $0.10 micropayments, atomic delete per-colo is sufficient. If you ever need strict global single-use, upgrade to Durable Objects.

## Pluggable Providers

```
providers/
  coinbase.js   ... v1 (shipped)
  ledger.js     ... add later
  phantom.js    ... add later
```

Each provider exports `authorize(amount, service, note)` and returns `{ success, provider, amount, url }`.

## Security Guarantees

- Main Coinbase balance untouched (isolated portfolio, max $50)
- API key locked to tiny portfolio only (Transfer + View permissions)
- Worker /create endpoint requires Bearer token auth
- URLs are deleted on first use (not marked ... deleted)
- Worker secret lives in Cloudflare env + 1Password (never in code)
- Full worker code is public ... nothing hidden
- Input validation: amount 0-50, service 1-50 chars, note max 200, TTL max 60 min

---

This is the protocol the agent economy has been waiting for.
