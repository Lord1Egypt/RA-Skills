// worker/index.js
// Cloudflare Worker for wip-agent-pay.
// All payment logic lives here. Local providers just call these routes.
//
// Routes:
//   GET  /                    Health check
//   POST /create              Mint one-time URL (existing Mode B)
//   GET  /:token              Redeem one-time URL
//   POST /x402/pay            x402 flow via Coinbase CDP (Path 1: self-custody)
//   POST /privy/pay           x402 flow via Privy wallet (Path 1: self-custody)
//   POST /pool/pay            Pool Mode A: Stripe checkout + x402 from Parker's float
//   POST /pool/confirm        Pool Mode A: poll for Stripe confirmation + get content
//   POST /wallet/create       Mode C: create Privy wallet by email (over-$25)
//   POST /wallet/pay          Mode C: sign x402 from user's Privy wallet
//   POST /stripe/checkout     Create Stripe Checkout session (funding)
//   POST /stripe/webhook      Stripe payment confirmation
//   GET  /stripe/success      Post-checkout redirect
//   GET  /stripe/cancel       Checkout cancelled
//   POST /balance             Wallet balance
//   POST /history             Transaction history
//   POST /budget              View/set spending limits
//
// Pool Mode pricing:
//   User pays: x402 price + Stripe fees (2.9% + $0.30) + $0.25 flat fee
//   Parker nets: $0.25 per transaction
//   Max pool transaction: $25. Over $25 redirects to Mode C (user's own wallet).
//
// Bindings:
//   KV: PAY_TOKENS, PAY_LEDGER
//   Env: WORKER_SECRET, CDP_API_KEY_ID, CDP_API_KEY_SECRET, CDP_WALLET_SECRET,
//        CDP_ACCOUNT_ADDRESS, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET,
//        PRIVY_APP_ID, PRIVY_APP_SECRET, PRIVY_WALLET_ID, PRIVY_WALLET_ADDRESS

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    // --- Health check ---
    if (path === '/' && method === 'GET') {
      return json({ status: 'ok', service: 'wip-agent-pay' });
    }

    // --- Stripe webhook (no auth ... verified by Stripe signature) ---
    if (path === '/stripe/webhook' && method === 'POST') {
      return handleStripeWebhook(request, env);
    }

    // --- Stripe success/cancel (no auth ... user redirect) ---
    if (path === '/stripe/success' && method === 'GET') {
      return handleStripeSuccess(request, env);
    }
    if (path === '/stripe/cancel' && method === 'GET') {
      return new Response('<h1>Payment cancelled.</h1><p>You can close this window.</p>', {
        headers: { 'Content-Type': 'text/html' },
      });
    }

    // --- All other routes require Worker secret ---
    const authHeader = request.headers.get('Authorization') || '';
    const token = authHeader.replace('Bearer ', '');
    if (token !== env.WORKER_SECRET) {
      return json({ error: 'unauthorized' }, 401);
    }

    // --- Mint one-time URL (existing) ---
    if (path === '/create' && method === 'POST') {
      return handleCreate(request, env, url);
    }

    // --- x402 pay via CDP ---
    if (path === '/x402/pay' && method === 'POST') {
      return handleX402CDP(request, env);
    }

    // --- Stripe checkout (funding) ---
    if (path === '/stripe/checkout' && method === 'POST') {
      return handleStripeCheckout(request, env, url);
    }

    // --- Privy pay ---
    if (path === '/privy/pay' && method === 'POST') {
      return handlePrivyPay(request, env);
    }

    // --- Balance ---
    if (path === '/balance' && method === 'POST') {
      return handleBalance(request, env);
    }

    // --- History ---
    if (path === '/history' && method === 'POST') {
      return handleHistory(request, env);
    }

    // --- Budget ---
    if (path === '/budget' && method === 'POST') {
      return handleBudget(request, env);
    }

    // --- Pool Mode A: pay from Parker's float ---
    if (path === '/pool/pay' && method === 'POST') {
      return handlePoolPay(request, env, url);
    }

    // --- Pool Mode A: confirm payment + get content ---
    if (path === '/pool/confirm' && method === 'POST') {
      return handlePoolConfirm(request, env);
    }

    // --- Mode C: create user wallet ---
    if (path === '/wallet/create' && method === 'POST') {
      return handleWalletCreate(request, env);
    }

    // --- Mode C: pay from user's wallet ---
    if (path === '/wallet/pay' && method === 'POST') {
      return handleWalletPay(request, env);
    }

    // --- Redeem one-time URL ---
    const tokenMatch = path.match(/^\/([a-f0-9-]{36})$/);
    if (tokenMatch && method === 'GET') {
      return handleRedeem(tokenMatch[1], env);
    }

    return json({ error: 'not found' }, 404);
  }
};

// ============================================================
// Helpers
// ============================================================

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function randomToken() {
  return crypto.randomUUID();
}

// ============================================================
// Route: POST /create (existing one-time URL mint)
// ============================================================

async function handleCreate(request, env, url) {
  const { amount, service, note, expiresMin } = await request.json();
  const token = randomToken();
  const ttl = (expiresMin || 3) * 60;

  await env.PAY_TOKENS.put(token, JSON.stringify({
    amount, service, note,
    created: Date.now(),
    type: 'one-time-url',
  }), { expirationTtl: ttl });

  return json({ url: `${url.origin}/${token}` });
}

// ============================================================
// Route: GET /:token (redeem one-time URL)
// ============================================================

async function handleRedeem(token, env) {
  const data = await env.PAY_TOKENS.get(token);
  if (!data) {
    return json({ error: 'gone', message: 'This payment link has already been used or expired.' }, 410);
  }

  // Atomic delete ... single use enforced
  await env.PAY_TOKENS.delete(token);

  const parsed = JSON.parse(data);
  return json({
    status: 'redeemed',
    ...parsed,
  });
}

// ============================================================
// Route: POST /x402/pay (Coinbase CDP x402 flow)
// ============================================================

async function handleX402CDP(request, env) {
  const { url: targetUrl } = await request.json();
  if (!targetUrl) return json({ error: 'url is required' }, 400);

  // Step 1: Hit the paywalled URL
  const initialRes = await fetch(targetUrl, { redirect: 'manual' });

  // If not 402, return whatever we got
  if (initialRes.status !== 402) {
    const body = await initialRes.text();
    return json({
      status: 'no-paywall',
      httpStatus: initialRes.status,
      content: body,
    });
  }

  // Step 2: Parse 402 payment requirements
  const paymentReqs = await parse402Response(initialRes);
  if (!paymentReqs) {
    return json({ error: 'Could not parse 402 payment requirements' }, 502);
  }

  // Step 3: Sign EIP-3009 transferWithAuthorization via CDP
  const signature = await signWithCDP(env, paymentReqs);
  if (!signature) {
    return json({ error: 'CDP signing failed' }, 502);
  }

  // Step 4: Build payment proof and retry
  const paymentProof = buildPaymentProof(paymentReqs, signature, env.CDP_ACCOUNT_ADDRESS);

  const retryRes = await fetch(targetUrl, {
    headers: {
      'X-PAYMENT': paymentProof,
    },
  });

  const content = await retryRes.text();

  if (!retryRes.ok) {
    return json({
      error: 'Payment submitted but content fetch failed',
      httpStatus: retryRes.status,
      content,
    }, 502);
  }

  // Step 5: Mint one-time token with content
  const token = randomToken();
  await env.PAY_TOKENS.put(token, JSON.stringify({
    type: 'x402-content',
    content,
    amount: paymentReqs.amount,
    service: new URL(targetUrl).hostname,
    paidAt: Date.now(),
  }), { expirationTtl: 300 }); // 5 min TTL for content tokens

  return json({
    status: 'paid',
    amount: paymentReqs.amount,
    network: paymentReqs.network,
    service: new URL(targetUrl).hostname,
    token,
  });
}

/**
 * Parse a 402 response to extract payment requirements.
 * Supports x402 protocol headers and JSON body.
 */
async function parse402Response(res) {
  // Try x402 headers first
  const payTo = res.headers.get('x-payment-address') || res.headers.get('x-pay-to');
  const amount = res.headers.get('x-payment-amount') || res.headers.get('x-amount');
  const network = res.headers.get('x-payment-network') || res.headers.get('x-network');
  const token = res.headers.get('x-payment-token') || res.headers.get('x-token');
  const contract = res.headers.get('x-payment-contract') || res.headers.get('x-token-contract');

  if (payTo && amount) {
    return {
      payTo,
      amount,
      network: network || 'base',
      token: token || 'USDC',
      contract,
    };
  }

  // Try JSON body
  try {
    const body = await res.json();
    return {
      payTo: body.payTo || body.address || body.recipient,
      amount: body.amount || body.price,
      network: body.network || body.chain || 'base',
      token: body.token || body.currency || 'USDC',
      contract: body.contract || body.tokenContract,
    };
  } catch {
    return null;
  }
}

/**
 * Sign EIP-3009 transferWithAuthorization via Coinbase CDP.
 */
async function signWithCDP(env, paymentReqs) {
  const { apiKeyId, apiKeySecret, walletSecret, accountAddress } =
    getCDPCreds(env);

  if (!apiKeyId) return null;

  // Determine chain ID from network
  const chainId = getChainId(paymentReqs.network);

  // Build EIP-712 typed data for transferWithAuthorization
  const nonce = '0x' + Array.from(crypto.getRandomValues(new Uint8Array(32)))
    .map(b => b.toString(16).padStart(2, '0')).join('');
  const now = Math.floor(Date.now() / 1000);

  const typedData = {
    domain: {
      name: 'USD Coin',
      version: '2',
      chainId: String(chainId),
      verifyingContract: paymentReqs.contract || getUSDCContract(paymentReqs.network),
    },
    types: {
      TransferWithAuthorization: [
        { name: 'from', type: 'address' },
        { name: 'to', type: 'address' },
        { name: 'value', type: 'uint256' },
        { name: 'validAfter', type: 'uint256' },
        { name: 'validBefore', type: 'uint256' },
        { name: 'nonce', type: 'bytes32' },
      ],
    },
    primaryType: 'TransferWithAuthorization',
    message: {
      from: accountAddress,
      to: paymentReqs.payTo,
      value: toSmallestUnit(paymentReqs.amount),
      validAfter: '0',
      validBefore: String(now + 300),
      nonce,
    },
  };

  // Call CDP signTypedData
  const cdpUrl = `https://api.cdp.coinbase.com/platform/v2/evm/accounts/${accountAddress}/sign-typed-data`;
  const body = JSON.stringify({ typed_data: typedData });

  const headers = await createCDPAuthHeaders(
    { apiKeyId, apiKeySecret, walletSecret },
    'POST', cdpUrl, body
  );

  const res = await fetch(cdpUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': headers.authorization,
      'X-Wallet-Auth': headers.walletAuth,
    },
    body,
  });

  if (!res.ok) {
    console.error('CDP sign failed:', res.status, await res.text());
    return null;
  }

  const result = await res.json();
  return result.signature;
}

/**
 * Build x402 payment proof header.
 */
function buildPaymentProof(paymentReqs, signature, fromAddress) {
  const proof = {
    type: 'eip-3009',
    signature,
    from: fromAddress,
    to: paymentReqs.payTo,
    amount: paymentReqs.amount,
    network: paymentReqs.network,
  };
  return btoa(JSON.stringify(proof));
}

function getCDPCreds(env) {
  return {
    apiKeyId: env.CDP_API_KEY_ID || '',
    apiKeySecret: env.CDP_API_KEY_SECRET || '',
    walletSecret: env.CDP_WALLET_SECRET || '',
    accountAddress: env.CDP_ACCOUNT_ADDRESS || '',
  };
}

function getChainId(network) {
  const chains = {
    'base': 8453,
    'base-sepolia': 84532,
    'ethereum': 1,
    'monad': 10143,
    'monad-testnet': 10143,
    'polygon': 137,
    'arbitrum': 42161,
    'optimism': 10,
  };
  return chains[network?.toLowerCase()] || 8453;
}

function getUSDCContract(network) {
  const contracts = {
    'base': '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    'ethereum': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    'polygon': '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359',
    'arbitrum': '0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
    'optimism': '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85',
  };
  return contracts[network?.toLowerCase()] || contracts['base'];
}

function toSmallestUnit(amount) {
  // USDC has 6 decimals
  return String(Math.round(parseFloat(amount) * 1_000_000));
}

// ============================================================
// CDP Auth (Ed25519 JWT ... inline for Worker)
// ============================================================

function base64url(buffer) {
  const bytes = new Uint8Array(buffer);
  let str = '';
  for (const b of bytes) str += String.fromCharCode(b);
  return btoa(str).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

async function importEd25519Key(base64Secret) {
  const raw = Uint8Array.from(atob(base64Secret), c => c.charCodeAt(0));
  const pkcs8Prefix = new Uint8Array([
    0x30, 0x2e, 0x02, 0x01, 0x00, 0x30, 0x05, 0x06,
    0x03, 0x2b, 0x65, 0x70, 0x04, 0x22, 0x04, 0x20
  ]);
  const pkcs8 = new Uint8Array(pkcs8Prefix.length + raw.length);
  pkcs8.set(pkcs8Prefix);
  pkcs8.set(raw, pkcs8Prefix.length);
  return crypto.subtle.importKey('pkcs8', pkcs8, { name: 'Ed25519' }, false, ['sign']);
}

async function signJWT(payload, key) {
  const header = { alg: 'EdDSA', typ: 'JWT' };
  const enc = new TextEncoder();
  const headerB64 = base64url(enc.encode(JSON.stringify(header)));
  const payloadB64 = base64url(enc.encode(JSON.stringify(payload)));
  const signingInput = `${headerB64}.${payloadB64}`;
  const signature = await crypto.subtle.sign('Ed25519', key, enc.encode(signingInput));
  return `${signingInput}.${base64url(signature)}`;
}

async function createCDPAuthHeaders(creds, method, url, body = '') {
  const now = Math.floor(Date.now() / 1000);
  const parsed = new URL(url);
  const uri = `${method.toUpperCase()} ${parsed.host}${parsed.pathname}`;

  const apiKey = await importEd25519Key(creds.apiKeySecret);
  const walletKey = await importEd25519Key(creds.walletSecret);

  const enc = new TextEncoder();
  const bodyHash = await crypto.subtle.digest('SHA-256', enc.encode(body));

  const [bearer, walletAuth] = await Promise.all([
    signJWT({
      sub: creds.apiKeyId,
      iss: 'cdp',
      aud: ['cdp_service'],
      nbf: now,
      exp: now + 120,
      uris: [uri],
    }, apiKey),
    signJWT({
      iat: now,
      nbf: now,
      exp: now + 120,
      jti: crypto.randomUUID(),
      uris: [uri],
      reqHash: base64url(bodyHash),
    }, walletKey),
  ]);

  return {
    authorization: `Bearer ${bearer}`,
    walletAuth,
  };
}

// ============================================================
// Route: POST /stripe/checkout (create funding session)
// ============================================================

async function handleStripeCheckout(request, env, url) {
  const { amount, wallet } = await request.json();
  if (!amount || amount <= 0) return json({ error: 'amount must be positive' }, 400);

  const fundId = randomToken();

  // Store pending fund in KV
  await env.PAY_TOKENS.put(`fund:${fundId}`, JSON.stringify({
    type: 'pending-fund',
    amount,
    wallet: wallet || 'cdp',
    status: 'pending',
    created: Date.now(),
  }), { expirationTtl: 3600 }); // 1 hour to complete checkout

  // Create Stripe Checkout session
  const res = await fetch('https://api.stripe.com/v1/checkout/sessions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.STRIPE_SECRET_KEY}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      'line_items[0][price_data][currency]': 'usd',
      'line_items[0][price_data][product_data][name]': 'Agent Pay Wallet Funding',
      'line_items[0][price_data][unit_amount]': String(Math.round(amount * 100)),
      'line_items[0][quantity]': '1',
      'mode': 'payment',
      'success_url': `${url.origin}/stripe/success?fund_id=${fundId}`,
      'cancel_url': `${url.origin}/stripe/cancel`,
      'metadata[fund_id]': fundId,
      'metadata[wallet]': wallet || 'cdp',
      'payment_method_types[0]': 'card',
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    return json({ error: `Stripe error: ${err}` }, 502);
  }

  const session = await res.json();
  return json({ checkoutUrl: session.url, fundId });
}

// ============================================================
// Route: POST /stripe/webhook (payment confirmation)
// ============================================================

async function handleStripeWebhook(request, env) {
  const body = await request.text();
  const sig = request.headers.get('stripe-signature');

  if (!sig || !env.STRIPE_WEBHOOK_SECRET) {
    return json({ error: 'missing signature' }, 400);
  }

  // Verify webhook signature
  const verified = await verifyStripeSignature(body, sig, env.STRIPE_WEBHOOK_SECRET);
  if (!verified) {
    return json({ error: 'invalid signature' }, 400);
  }

  const event = JSON.parse(body);

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const fundId = session.metadata?.fund_id;
    const poolId = session.metadata?.pool_id;

    if (fundId) {
      // Mark fund as complete
      const fundData = await env.PAY_TOKENS.get(`fund:${fundId}`);
      if (fundData) {
        const parsed = JSON.parse(fundData);
        parsed.status = 'funded';
        parsed.paidAt = Date.now();
        parsed.stripeSessionId = session.id;
        await env.PAY_TOKENS.put(`fund:${fundId}`, JSON.stringify(parsed), {
          expirationTtl: 86400, // 24h
        });
      }
    }

    if (poolId) {
      // Pool Mode: Stripe payment confirmed. Mark as stripe-paid.
      // The actual x402 signing happens when /pool/confirm is called.
      const poolData = await env.PAY_TOKENS.get(`pool:${poolId}`);
      if (poolData) {
        const parsed = JSON.parse(poolData);
        parsed.stripePaid = true;
        parsed.stripePaidAt = Date.now();
        await env.PAY_TOKENS.put(`pool:${poolId}`, JSON.stringify(parsed), {
          expirationTtl: 600,
        });
      }
    }
  }

  return json({ received: true });
}

/**
 * Verify Stripe webhook signature using HMAC-SHA256.
 */
async function verifyStripeSignature(body, sigHeader, secret) {
  try {
    const parts = Object.fromEntries(
      sigHeader.split(',').map(p => {
        const [k, ...v] = p.split('=');
        return [k, v.join('=')];
      })
    );

    const timestamp = parts.t;
    const expectedSig = parts.v1;
    if (!timestamp || !expectedSig) return false;

    // Check timestamp freshness (5 min tolerance)
    const age = Math.abs(Date.now() / 1000 - parseInt(timestamp));
    if (age > 300) return false;

    const enc = new TextEncoder();
    const key = await crypto.subtle.importKey(
      'raw', enc.encode(secret),
      { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
    );

    const payload = `${timestamp}.${body}`;
    const sig = await crypto.subtle.sign('HMAC', key, enc.encode(payload));
    const sigHex = Array.from(new Uint8Array(sig))
      .map(b => b.toString(16).padStart(2, '0')).join('');

    return sigHex === expectedSig;
  } catch {
    return false;
  }
}

// ============================================================
// Route: GET /stripe/success (post-checkout redirect)
// ============================================================

async function handleStripeSuccess(request, env) {
  const url = new URL(request.url);
  const fundId = url.searchParams.get('fund_id');
  const poolId = url.searchParams.get('pool_id');

  const isPool = !!poolId;
  const title = isPool ? 'Payment Complete' : 'Wallet Funded';
  const message = isPool
    ? 'Your agent is fetching the content now. You can close this window.'
    : 'Your agent\'s wallet has been funded. You can close this window.';
  const refId = poolId || fundId;

  return new Response(`
    <!DOCTYPE html>
    <html>
    <head><title>${title}</title>
    <style>
      body { font-family: -apple-system, sans-serif; display: flex; justify-content: center;
             align-items: center; height: 100vh; margin: 0; background: #f5f5f5; }
      .card { background: white; padding: 40px; border-radius: 12px; text-align: center;
              box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 400px; }
      h1 { font-size: 24px; margin: 0 0 8px; }
      p { color: #666; margin: 4px 0; }
      .check { font-size: 48px; margin-bottom: 16px; }
    </style>
    </head>
    <body>
      <div class="card">
        <div class="check">&#10003;</div>
        <h1>${title}</h1>
        <p>${message}</p>
        ${refId ? `<p style="font-size:12px;color:#999;">ID: ${refId}</p>` : ''}
      </div>
    </body>
    </html>
  `, { headers: { 'Content-Type': 'text/html' } });
}

// ============================================================
// Route: POST /privy/pay (x402 via Privy wallet)
// ============================================================

async function handlePrivyPay(request, env) {
  const { url: targetUrl } = await request.json();
  if (!targetUrl) return json({ error: 'url is required' }, 400);

  // Step 1: Hit the paywalled URL
  const initialRes = await fetch(targetUrl, { redirect: 'manual' });

  if (initialRes.status !== 402) {
    const body = await initialRes.text();
    return json({
      status: 'no-paywall',
      httpStatus: initialRes.status,
      content: body,
    });
  }

  // Step 2: Parse 402 payment requirements
  const paymentReqs = await parse402Response(initialRes);
  if (!paymentReqs) {
    return json({ error: 'Could not parse 402 payment requirements' }, 502);
  }

  // Step 3: Sign via Privy RPC
  const signature = await signWithPrivy(env, paymentReqs);
  if (!signature) {
    return json({ error: 'Privy signing failed' }, 502);
  }

  // Step 4: Retry with payment proof
  const paymentProof = buildPaymentProof(paymentReqs, signature, env.PRIVY_WALLET_ADDRESS || '');

  const retryRes = await fetch(targetUrl, {
    headers: { 'X-PAYMENT': paymentProof },
  });

  const content = await retryRes.text();

  if (!retryRes.ok) {
    return json({
      error: 'Payment submitted but content fetch failed',
      httpStatus: retryRes.status,
      content,
    }, 502);
  }

  // Step 5: Mint token with content
  const token = randomToken();
  await env.PAY_TOKENS.put(token, JSON.stringify({
    type: 'x402-content',
    content,
    amount: paymentReqs.amount,
    service: new URL(targetUrl).hostname,
    paidAt: Date.now(),
    wallet: 'privy',
  }), { expirationTtl: 300 });

  return json({
    status: 'paid',
    amount: paymentReqs.amount,
    network: paymentReqs.network,
    service: new URL(targetUrl).hostname,
    token,
    wallet: 'privy',
  });
}

/**
 * Sign EIP-712 typed data via Privy RPC.
 */
async function signWithPrivy(env, paymentReqs) {
  if (!env.PRIVY_APP_ID || !env.PRIVY_APP_SECRET || !env.PRIVY_WALLET_ID) {
    return null;
  }

  const chainId = getChainId(paymentReqs.network);
  const nonce = '0x' + Array.from(crypto.getRandomValues(new Uint8Array(32)))
    .map(b => b.toString(16).padStart(2, '0')).join('');
  const now = Math.floor(Date.now() / 1000);

  const typedData = {
    domain: {
      name: 'USD Coin',
      version: '2',
      chainId: String(chainId),
      verifyingContract: paymentReqs.contract || getUSDCContract(paymentReqs.network),
    },
    types: {
      EIP712Domain: [
        { name: 'name', type: 'string' },
        { name: 'version', type: 'string' },
        { name: 'chainId', type: 'uint256' },
        { name: 'verifyingContract', type: 'address' },
      ],
      TransferWithAuthorization: [
        { name: 'from', type: 'address' },
        { name: 'to', type: 'address' },
        { name: 'value', type: 'uint256' },
        { name: 'validAfter', type: 'uint256' },
        { name: 'validBefore', type: 'uint256' },
        { name: 'nonce', type: 'bytes32' },
      ],
    },
    primaryType: 'TransferWithAuthorization',
    message: {
      from: env.PRIVY_WALLET_ADDRESS || '',
      to: paymentReqs.payTo,
      value: toSmallestUnit(paymentReqs.amount),
      validAfter: '0',
      validBefore: String(now + 300),
      nonce,
    },
  };

  const privyUrl = `https://api.privy.io/v1/wallets/${env.PRIVY_WALLET_ID}/rpc`;
  const authString = btoa(`${env.PRIVY_APP_ID}:${env.PRIVY_APP_SECRET}`);

  const res = await fetch(privyUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Basic ${authString}`,
      'privy-app-id': env.PRIVY_APP_ID,
    },
    body: JSON.stringify({
      method: 'eth_signTypedData_v4',
      caip2: `eip155:${chainId}`,
      params: { typed_data: typedData },
    }),
  });

  if (!res.ok) {
    console.error('Privy sign failed:', res.status, await res.text());
    return null;
  }

  const result = await res.json();
  return result.data?.signature || result.signature;
}

// ============================================================
// Route: POST /balance (wallet balance)
// ============================================================

async function handleBalance(request, env) {
  const { wallet } = await request.json();
  const w = wallet || 'cdp';

  if (w === 'cdp') {
    // Query CDP wallet balance
    const creds = getCDPCreds(env);
    if (!creds.apiKeyId || !creds.accountAddress) {
      return json({ balance: '0.00', wallet: w, error: 'CDP wallet not configured' });
    }

    const balanceUrl = `https://api.cdp.coinbase.com/platform/v2/evm/accounts/${creds.accountAddress}/balances`;
    const headers = await createCDPAuthHeaders(creds, 'GET', balanceUrl);

    const res = await fetch(balanceUrl, {
      headers: {
        'Authorization': headers.authorization,
        'X-Wallet-Auth': headers.walletAuth,
      },
    });

    if (!res.ok) {
      return json({ balance: '0.00', wallet: w, error: `CDP balance query failed: ${res.status}` });
    }

    const data = await res.json();
    // Find USDC balance
    const usdc = data.balances?.find(b => b.asset === 'USDC' || b.symbol === 'USDC');
    return json({
      balance: usdc?.amount || '0.00',
      wallet: w,
      address: creds.accountAddress,
    });
  }

  if (w === 'privy') {
    // Privy balance ... query via RPC
    if (!env.PRIVY_APP_ID || !env.PRIVY_WALLET_ID) {
      return json({ balance: '0.00', wallet: w, error: 'Privy wallet not configured' });
    }

    return json({
      balance: 'query via on-chain RPC',
      wallet: w,
      address: env.PRIVY_WALLET_ADDRESS || 'not set',
    });
  }

  return json({ error: `Unknown wallet: ${w}` }, 400);
}

// ============================================================
// Route: POST /history (transaction history)
// ============================================================

async function handleHistory(request, env) {
  const { wallet, limit } = await request.json();
  const w = wallet || 'cdp';
  const max = Math.min(limit || 20, 100);

  // Read from PAY_LEDGER KV
  const ledgerKey = `ledger:${w}`;
  const ledgerData = await env.PAY_LEDGER?.get(ledgerKey);

  if (!ledgerData) {
    return json({ wallet: w, transactions: [] });
  }

  const ledger = JSON.parse(ledgerData);
  const transactions = ledger.slice(-max).reverse(); // Most recent first

  return json({ wallet: w, transactions });
}

/**
 * Record a transaction in the ledger.
 * Called internally after successful payments/funding.
 */
async function recordTransaction(env, wallet, tx) {
  const ledgerKey = `ledger:${wallet}`;
  const existing = await env.PAY_LEDGER?.get(ledgerKey);
  const ledger = existing ? JSON.parse(existing) : [];

  ledger.push({
    ...tx,
    timestamp: Date.now(),
    id: randomToken(),
  });

  // Keep last 1000 transactions
  const trimmed = ledger.slice(-1000);
  await env.PAY_LEDGER?.put(ledgerKey, JSON.stringify(trimmed));
}

// ============================================================
// Route: POST /budget (view/set spending limits)
// ============================================================

async function handleBudget(request, env) {
  const { wallet, daily, perTx, total } = await request.json();
  const w = wallet || 'cdp';
  const budgetKey = `budget:${w}`;

  // If setting new budget
  if (daily !== undefined || perTx !== undefined || total !== undefined) {
    const existing = await env.PAY_LEDGER?.get(budgetKey);
    const current = existing ? JSON.parse(existing) : {};

    if (daily !== undefined) current.daily = daily;
    if (perTx !== undefined) current.perTx = perTx;
    if (total !== undefined) current.total = total;

    await env.PAY_LEDGER?.put(budgetKey, JSON.stringify(current));
    return json({ wallet: w, ...current, status: 'updated' });
  }

  // View current budget
  const budgetData = await env.PAY_LEDGER?.get(budgetKey);
  const budgetObj = budgetData ? JSON.parse(budgetData) : {};

  // Calculate spent today
  const ledgerKey = `ledger:${w}`;
  const ledgerData = await env.PAY_LEDGER?.get(ledgerKey);
  let spentToday = 0;

  if (ledgerData) {
    const ledger = JSON.parse(ledgerData);
    const todayStart = new Date();
    todayStart.setHours(0, 0, 0, 0);
    const todayMs = todayStart.getTime();

    spentToday = ledger
      .filter(tx => tx.timestamp >= todayMs && tx.type !== 'fund')
      .reduce((sum, tx) => sum + (parseFloat(tx.amount) || 0), 0);
  }

  const remainingToday = budgetObj.daily
    ? Math.max(0, budgetObj.daily - spentToday).toFixed(2)
    : 'unlimited';

  return json({
    wallet: w,
    daily: budgetObj.daily || null,
    perTx: budgetObj.perTx || null,
    total: budgetObj.total || null,
    spentToday: spentToday.toFixed(2),
    remainingToday,
  });
}

/**
 * Check if a transaction is within budget.
 * Returns { allowed: true } or { allowed: false, reason: '...' }
 */
async function checkBudget(env, wallet, amount) {
  const budgetKey = `budget:${wallet}`;
  const budgetData = await env.PAY_LEDGER?.get(budgetKey);
  if (!budgetData) return { allowed: true }; // No budget set

  const budget = JSON.parse(budgetData);

  // Per-transaction limit
  if (budget.perTx && parseFloat(amount) > budget.perTx) {
    return { allowed: false, reason: `Exceeds per-transaction limit of $${budget.perTx}` };
  }

  // Daily limit
  if (budget.daily) {
    const ledgerKey = `ledger:${wallet}`;
    const ledgerData = await env.PAY_LEDGER?.get(ledgerKey);

    if (ledgerData) {
      const ledger = JSON.parse(ledgerData);
      const todayStart = new Date();
      todayStart.setHours(0, 0, 0, 0);
      const todayMs = todayStart.getTime();

      const spentToday = ledger
        .filter(tx => tx.timestamp >= todayMs && tx.type !== 'fund')
        .reduce((sum, tx) => sum + (parseFloat(tx.amount) || 0), 0);

      if (spentToday + parseFloat(amount) > budget.daily) {
        return { allowed: false, reason: `Would exceed daily limit of $${budget.daily} (spent: $${spentToday.toFixed(2)})` };
      }
    }
  }

  return { allowed: true };
}

// ============================================================
// Pool Mode constants
// ============================================================

const POOL_MAX_AMOUNT = 25.00;  // Max x402 price for pool mode
const POOL_FEE = 0.25;          // Parker's flat fee per transaction

function calculatePoolTotal(x402Amount) {
  const amount = parseFloat(x402Amount);
  // Stripe takes 2.9% of the final charge + $0.30. To net the right amount,
  // we solve: charge = (amount + fee + $0.30) / (1 - 0.029)
  const subtotal = amount + POOL_FEE + 0.30;
  const total = subtotal / (1 - 0.029);
  const stripeFee = total - amount - POOL_FEE;
  return {
    x402Amount: amount.toFixed(2),
    poolFee: POOL_FEE.toFixed(2),
    stripeFee: stripeFee.toFixed(2),
    totalCharge: total.toFixed(2),
  };
}

// ============================================================
// Route: POST /pool/pay (Pool Mode A: Stripe + x402 from float)
// ============================================================

async function handlePoolPay(request, env, workerUrl) {
  const { url: targetUrl } = await request.json();
  if (!targetUrl) return json({ error: 'url is required' }, 400);

  // Step 1: Hit the paywalled URL
  const initialRes = await fetch(targetUrl, { redirect: 'manual' });

  // If not 402, return content (it's free)
  if (initialRes.status !== 402) {
    const body = await initialRes.text();
    return json({ status: 'no-paywall', httpStatus: initialRes.status, content: body });
  }

  // Step 2: Parse 402 payment requirements
  const paymentReqs = await parse402Response(initialRes);
  if (!paymentReqs) {
    return json({ error: 'Could not parse 402 payment requirements' }, 502);
  }

  const amount = parseFloat(paymentReqs.amount);
  const service = new URL(targetUrl).hostname;

  // Step 3: Check pool limit
  if (amount > POOL_MAX_AMOUNT) {
    return json({
      status: 'over-pool-limit',
      error: `Transaction $${amount.toFixed(2)} exceeds pool limit of $${POOL_MAX_AMOUNT}. Use your own wallet (Mode C).`,
      amount: paymentReqs.amount,
      service,
      poolMax: POOL_MAX_AMOUNT,
      network: paymentReqs.network,
    }, 400);
  }

  // Step 4: Calculate pricing
  const pricing = calculatePoolTotal(paymentReqs.amount);

  // Step 5: Create a payment ID and store pending payment
  const paymentId = randomToken();
  await env.PAY_TOKENS.put(`pool:${paymentId}`, JSON.stringify({
    type: 'pool-pending',
    targetUrl,
    amount: paymentReqs.amount,
    pricing,
    service,
    paymentReqs,
    status: 'pending',
    created: Date.now(),
  }), { expirationTtl: 600 }); // 10 min to complete

  // Step 6: Create Stripe Checkout session (payment goes to us)
  const checkoutParams = new URLSearchParams({
    'line_items[0][price_data][currency]': 'usd',
    'line_items[0][price_data][product_data][name]': `${service} via Agent Pay`,
    'line_items[0][price_data][unit_amount]': String(Math.round(parseFloat(pricing.totalCharge) * 100)),
    'line_items[0][quantity]': '1',
    'mode': 'payment',
    'payment_method_types[0]': 'card',
    'success_url': `${workerUrl.origin}/stripe/success?pool_id=${paymentId}`,
    'cancel_url': `${workerUrl.origin}/stripe/cancel`,
    'metadata[pool_id]': paymentId,
    'metadata[type]': 'pool',
    'metadata[x402_amount]': paymentReqs.amount,
    'metadata[service]': service,
  });

  const stripeRes = await fetch('https://api.stripe.com/v1/checkout/sessions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.STRIPE_SECRET_KEY}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: checkoutParams,
  });

  if (!stripeRes.ok) {
    const err = await stripeRes.text();
    return json({ error: `Stripe error: ${err}` }, 502);
  }

  const session = await stripeRes.json();

  // Update payment record with Stripe session
  const poolData = JSON.parse(await env.PAY_TOKENS.get(`pool:${paymentId}`));
  poolData.stripeSessionId = session.id;
  await env.PAY_TOKENS.put(`pool:${paymentId}`, JSON.stringify(poolData), { expirationTtl: 600 });

  return json({
    status: 'checkout-ready',
    checkoutUrl: session.url,
    paymentId,
    amount: paymentReqs.amount,
    pricing,
    service,
  });
}

// ============================================================
// Route: POST /pool/confirm (check Stripe payment + sign x402)
// ============================================================

async function handlePoolConfirm(request, env) {
  const { paymentId } = await request.json();
  if (!paymentId) return json({ error: 'paymentId is required' }, 400);

  const poolData = await env.PAY_TOKENS.get(`pool:${paymentId}`);
  if (!poolData) {
    return json({ error: 'Payment not found or expired' }, 404);
  }

  const payment = JSON.parse(poolData);

  // Already paid and content cached
  if (payment.status === 'paid') {
    return json({
      success: true,
      status: 'paid',
      content: payment.content,
      amount: payment.amount,
      service: payment.service,
    });
  }

  // Still pending. Check Stripe.
  if (payment.status === 'pending') {
    if (!payment.stripeSessionId) {
      return json({ success: false, error: 'pending', status: 'pending' });
    }

    const stripeRes = await fetch(
      `https://api.stripe.com/v1/checkout/sessions/${payment.stripeSessionId}`,
      { headers: { 'Authorization': `Bearer ${env.STRIPE_SECRET_KEY}` } }
    );

    if (!stripeRes.ok) {
      return json({ success: false, error: 'pending', status: 'pending' });
    }

    const session = await stripeRes.json();
    if (session.payment_status !== 'paid') {
      return json({ success: false, error: 'pending', status: 'pending' });
    }

    // Stripe confirmed. Now sign x402 from pool wallet and get content.
    const paymentReqs = payment.paymentReqs;

    // Try CDP first (pool wallet), then Privy fallback
    let signature = await signWithCDP(env, paymentReqs);
    let fromAddress = env.CDP_ACCOUNT_ADDRESS;

    if (!signature) {
      signature = await signWithPrivy(env, paymentReqs);
      fromAddress = env.PRIVY_WALLET_ADDRESS || '';
    }

    if (!signature) {
      return json({
        error: 'Pool wallet signing failed. Stripe payment collected but x402 not completed. Contact support.',
        paymentId,
      }, 502);
    }

    // Build proof and replay
    const proof = buildPaymentProof(paymentReqs, signature, fromAddress);
    const retryRes = await fetch(payment.targetUrl, {
      headers: { 'X-PAYMENT': proof },
    });

    const content = await retryRes.text();

    if (retryRes.status === 402) {
      // Payment proof rejected. This is bad ... Stripe already charged.
      return json({
        error: 'x402 payment proof rejected by server. Stripe payment collected. Contact support.',
        paymentId,
        httpStatus: retryRes.status,
      }, 502);
    }

    // Success. Cache content and record transaction.
    payment.status = 'paid';
    payment.paidAt = Date.now();
    payment.content = content;
    await env.PAY_TOKENS.put(`pool:${paymentId}`, JSON.stringify(payment), { expirationTtl: 300 });

    await recordTransaction(env, 'pool', {
      type: 'pay',
      amount: payment.amount,
      service: payment.service,
      pricing: payment.pricing,
      paymentId,
    });

    return json({
      success: true,
      status: 'paid',
      content,
      amount: payment.amount,
      service: payment.service,
    });
  }

  return json({ success: false, error: `Unexpected status: ${payment.status}` });
}

// ============================================================
// Route: POST /wallet/create (Mode C: create Privy wallet by email)
// ============================================================

async function handleWalletCreate(request, env) {
  const { email } = await request.json();
  if (!email) return json({ error: 'email is required' }, 400);

  if (!env.PRIVY_APP_ID || !env.PRIVY_APP_SECRET) {
    return json({ error: 'Privy not configured on this Worker' }, 400);
  }

  const authString = btoa(`${env.PRIVY_APP_ID}:${env.PRIVY_APP_SECRET}`);

  // Create user via Privy API
  const createRes = await fetch('https://auth.privy.io/api/v1/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Basic ${authString}`,
      'privy-app-id': env.PRIVY_APP_ID,
    },
    body: JSON.stringify({
      create_ethereum_wallet: true,
      linked_accounts: [{ type: 'email', address: email }],
    }),
  });

  if (!createRes.ok) {
    const err = await createRes.text();
    return json({ error: `Privy user creation failed: ${err}` }, 502);
  }

  const user = await createRes.json();

  // Extract wallet address from linked accounts
  const wallet = user.linked_accounts?.find(a => a.type === 'wallet');
  const walletAddress = wallet?.address || null;

  // Store user wallet mapping
  await env.PAY_LEDGER?.put(`user-wallet:${email}`, JSON.stringify({
    privyUserId: user.id,
    walletAddress,
    email,
    created: Date.now(),
  }));

  return json({
    success: true,
    email,
    walletAddress,
    privyUserId: user.id,
    fundingInstructions: walletAddress
      ? `Send USDC to ${walletAddress} on Base or use Coinbase Onramp.`
      : 'Wallet creation pending. Check back shortly.',
  });
}

// ============================================================
// Route: POST /wallet/pay (Mode C: pay from user's Privy wallet)
// ============================================================

async function handleWalletPay(request, env) {
  const { url: targetUrl, email } = await request.json();
  if (!targetUrl) return json({ error: 'url is required' }, 400);
  if (!email) return json({ error: 'email is required' }, 400);

  // Look up user wallet
  const userData = await env.PAY_LEDGER?.get(`user-wallet:${email}`);
  if (!userData) {
    return json({
      error: 'No wallet found for this email. Create one first with /wallet/create.',
    }, 400);
  }

  const userWallet = JSON.parse(userData);
  if (!userWallet.walletAddress) {
    return json({ error: 'Wallet address not available yet.' }, 400);
  }

  // Hit the paywalled URL
  const initialRes = await fetch(targetUrl, { redirect: 'manual' });

  if (initialRes.status !== 402) {
    const body = await initialRes.text();
    return json({ status: 'no-paywall', httpStatus: initialRes.status, content: body });
  }

  // Parse 402
  const paymentReqs = await parse402Response(initialRes);
  if (!paymentReqs) {
    return json({ error: 'Could not parse 402 payment requirements' }, 502);
  }

  // Sign from user's Privy wallet
  // Note: this requires the user's wallet to be a server wallet we can sign from.
  // For now, we use the Privy server wallet API with the user's wallet ID.
  if (!env.PRIVY_APP_ID || !env.PRIVY_APP_SECRET) {
    return json({ error: 'Privy not configured' }, 400);
  }

  const chainId = getChainId(paymentReqs.network);
  const nonce = '0x' + Array.from(crypto.getRandomValues(new Uint8Array(32)))
    .map(b => b.toString(16).padStart(2, '0')).join('');
  const now = Math.floor(Date.now() / 1000);

  const typedData = {
    domain: {
      name: 'USD Coin',
      version: '2',
      chainId: String(chainId),
      verifyingContract: paymentReqs.contract || getUSDCContract(paymentReqs.network),
    },
    types: {
      EIP712Domain: [
        { name: 'name', type: 'string' },
        { name: 'version', type: 'string' },
        { name: 'chainId', type: 'uint256' },
        { name: 'verifyingContract', type: 'address' },
      ],
      TransferWithAuthorization: [
        { name: 'from', type: 'address' },
        { name: 'to', type: 'address' },
        { name: 'value', type: 'uint256' },
        { name: 'validAfter', type: 'uint256' },
        { name: 'validBefore', type: 'uint256' },
        { name: 'nonce', type: 'bytes32' },
      ],
    },
    primaryType: 'TransferWithAuthorization',
    message: {
      from: userWallet.walletAddress,
      to: paymentReqs.payTo,
      value: toSmallestUnit(paymentReqs.amount),
      validAfter: '0',
      validBefore: String(now + 300),
      nonce,
    },
  };

  // Sign via Privy using the user's wallet
  const authString = btoa(`${env.PRIVY_APP_ID}:${env.PRIVY_APP_SECRET}`);
  const privyUrl = `https://api.privy.io/v1/wallets/${userWallet.privyUserId}/rpc`;

  const signRes = await fetch(privyUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Basic ${authString}`,
      'privy-app-id': env.PRIVY_APP_ID,
    },
    body: JSON.stringify({
      method: 'eth_signTypedData_v4',
      caip2: `eip155:${chainId}`,
      params: { typed_data: typedData },
    }),
  });

  if (!signRes.ok) {
    const err = await signRes.text();
    return json({ error: `Wallet signing failed: ${err}` }, 502);
  }

  const signResult = await signRes.json();
  const signature = signResult.data?.signature || signResult.signature;

  if (!signature) {
    return json({ error: 'No signature returned from wallet' }, 502);
  }

  // Replay with proof
  const proof = buildPaymentProof(paymentReqs, signature, userWallet.walletAddress);
  const retryRes = await fetch(targetUrl, {
    headers: { 'X-PAYMENT': proof },
  });

  const content = await retryRes.text();
  const service = new URL(targetUrl).hostname;

  if (retryRes.status === 402) {
    return json({ error: 'Payment proof rejected by server', httpStatus: 402 }, 502);
  }

  await recordTransaction(env, `user:${email}`, {
    type: 'pay',
    amount: paymentReqs.amount,
    service,
    wallet: 'privy-user',
  });

  return json({
    status: 'paid',
    amount: paymentReqs.amount,
    network: paymentReqs.network,
    service,
    content,
    wallet: 'user-privy',
  });
}
