# Deploy pay.wip.computer Worker

## Step 1: Create the Worker

1. Go to https://dash.cloudflare.com
2. Workers & Pages ... Create
3. Click **"Start with Hello World!"**
4. Name it: `pay-wip-computer`
5. Click **Deploy**
6. Click **Edit Code** (opens the editor)
7. Delete the hello world code
8. Paste the full Worker code below
9. Click **Deploy**

## Step 2: Create KV Namespace

1. Go to Workers & Pages ... KV (left sidebar)
2. Click **Create a namespace**
3. Name it: `PAY_TOKENS`
4. Click **Add**

## Step 3: Bind KV to the Worker

1. Go to Workers & Pages ... `pay-wip-computer`
2. Click **Settings**
3. Click **Bindings** (left sidebar, under Variables)
4. Click **Add**
5. Select **KV Namespace**
6. Variable name: `KV`
7. KV Namespace: select `PAY_TOKENS`
8. Click **Save**

## Step 4: Add the Worker Secret

1. Still in Worker Settings
2. Click **Variables** (left sidebar, under Variables)
3. Under **Environment Variables**, click **Add**
4. Variable name: `WORKER_SECRET`
5. Value: generate a strong random string (e.g. run `openssl rand -hex 32` in terminal)
6. Click **Encrypt** (makes it a secret)
7. Click **Save and deploy**

## Step 5: Add Custom Domain

1. Still in Worker Settings
2. Click **Domains & Routes** (left sidebar, under Triggers)
3. Click **Add** ... **Custom Domain**
4. Enter: `pay.wip.computer`
5. Click **Add Domain**
6. Cloudflare handles DNS + SSL automatically (may take a few minutes)

## Step 6: Store the Secret in 1Password

Save the same WORKER_SECRET value you used in Step 4:

```
Vault: Agent Secrets
Entry name: wip-agent-pay-worker-secret
Field: password
Value: (same string from Step 4)
```

## Step 7: Verify

Open in browser or run:

```bash
curl https://pay.wip.computer/
```

Should return:

```json
{"status":"ok","service":"wip-agent-pay"}
```

## Worker Code

Paste this into the Cloudflare editor in Step 1:

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
