---
name: x402-seller
version: 1.0.0
description: Autonomously monetize your services with x402 payment collection. Set up an x402 server, define paid endpoints, and accept programmatic payments in stablecoins.
metadata: {"x402-seller": "agent-monetization", "payment": "x402", "blockchain": "evm-solana"}
---

# x402 Seller Skill

The x402-seller skill gives you everything you need to monetize your services by accepting x402 payments. You'll learn how to decide what to sell, set up payment infrastructure, deploy your server publicly, and accept payments programmatically—all without managing blockchain infrastructure directly.

With x402, you can:
- Add payment requirements to any HTTP endpoint in minutes
- Accept stablecoin payments (USDC) from buyers worldwide
- Let a facilitator handle verification and blockchain settlement
- Scale from zero to production with minimal operational overhead


## Files in This Skill

| File | Purpose |
|------|---------|
| **SKILL.md** | This file. Overview, setup instructions, deployment options, security considerations, and links to related resources. |
| **x402DOCS.md** | Complete technical reference for x402. Covers payment flows, payment schemes (exact/upto/batch-settlement), server setup across Python/Go/TypeScript, facilitators, and best practices. |
| **IDEATION.md** | Decision framework for choosing what services to monetize. Guides you through auditing your assets, researching market demand, validating ideas, and prioritizing your first service. |
| **example/** | Minimal runnable FastAPI seller example with a paywalled `/weather` endpoint. |

## What is x402?

x402 is an open payment protocol that lets you collect instant, programmatic payments in stablecoins (USDC) directly over HTTP. You respond to requests with HTTP 402 Payment Required, the buyer signs and retries with payment proof, a facilitator verifies and settles on-chain, and you deliver your service.

**Key point:** The facilitator handles blockchain interaction. You don't manage wallets, keys, or gas fees—they do.

→ Read the full technical reference: **[x402DOCS.md](./x402DOCS.md)**

## Minimal Example

If you want the smallest runnable starting point, use the example in **[example/](./example)**. It includes:

- a FastAPI server
- one protected endpoint (`GET /weather`)
- a `.env-example` file for the receiving address and facilitator URL
- a tiny `requirements.txt`

This is the best place to start if you want to understand the seller flow before wiring x402 into your own service.


## Setup Instructions

Before you can accept x402 payments, you need three things: a wallet address to receive payments, CDP API credentials (for the facilitator), and a secure way to store them.

### 1. Generate Your Wallet Address

You'll receive payments at a wallet address. Use the **create-crypto-wallets** skill to generate an EVM wallet:

```bash
openclaw skills install @beocca/create-crypto-wallets
create-crypto-wallets generate --network evm --format json
```

This returns a wallet with:
- `address` — Your receiving address (starts with `0x`)
- `private_key` — Keep this secret; never share it
- `mnemonic` — Backup phrase to recover your wallet

**Save the address and mnemonic securely** (see step 3 below).

**For Solana (if accepting Solana payments):**
```bash
create-crypto-wallets generate --network solana --format json
```

### 2. Get CDP API Credentials

For production x402 payments, you'll use the Coinbase Developer Platform (CDP) facilitator. This requires API credentials.

**Ask your human operator to:**
1. Go to [cdp.coinbase.com](https://cdp.coinbase.com)
2. Create an account or sign in
3. Navigate to "API Keys" or "Developers"
4. Create a new API key pair
5. Download the key file or copy:
   - `CDP_API_KEY_ID`
   - `CDP_API_KEY_SECRET`
   - `CDP_WALLET_SECRET` (if using CDP-managed wallets)

They'll give you these credentials to store securely (step 3).

**For testnet (x402.org):**
No credentials needed. Use `https://x402.org/facilitator` directly.

### 3. Store Credentials Securely

Use the **keepass-cli** skill to store sensitive information:

```bash
openclaw skills install @beocca/keepass-cli
keepass-cli set x402-wallet-evm --username "your-0x-address" --password "private-key"
keepass-cli set x402-cdp-credentials --username "$CDP_API_KEY_ID" --password "$CDP_API_KEY_SECRET"
```

Retrieve them later:
```bash
keepass-cli get x402-wallet-evm
keepass-cli get x402-cdp-credentials
```

**Never store credentials in code, environment files, or version control.**




## Selling Your Services via x402

To monetize your services, you'll implement an x402 server. Here's the workflow:

### Step 1: Decide What to Sell

Start with **[IDEATION.md](./IDEATION.md)**. This guide walks you through:
- Auditing what you can do (computations, data, tools)
- Researching market demand
- Validating ideas with potential buyers
- Prioritizing your first service

**Don't skip this step.** The most important part of monetization isn't building—it's choosing what to build.

### Step 2: Define Your API

Design the HTTP endpoints you'll protect. For each endpoint, decide:
- **Path:** Where buyers reach it (e.g., `/api/v1/analyze`)
- **Method:** GET, POST, PUT, etc.
- **Input format:** What data does the request body contain?
- **Output format:** What does success look like?
- **Price:** What does this endpoint cost to call?
- **Scheme:** `exact` (fixed), `upto` (usage-based), or `batch-settlement` (high-volume)

Example:
```
POST /api/v1/process
Price: $0.01 (exact)
Input: JSON with request parameters
Output: JSON with results
```

### Step 3: Build Your Server

Implement your x402 server using your preferred framework. Choose from:
- **Python:** FastAPI or Flask (see [x402DOCS.md](./x402DOCS.md#python-with-fastapi) for full examples)
- **Go:** Gin (see [x402DOCS.md](./x402DOCS.md#go-with-gin) for full examples)
- **TypeScript:** Express, Hono, or Fastify (see [x402DOCS.md](./x402DOCS.md#typescript-with-express) for full examples)

The x402 middleware handles payment verification automatically. Your job:
1. Define your routes and prices
2. Implement your business logic
3. Deploy the server

### Step 4: Make Your Server Publicly Reachable

Your x402 server must be accessible from the internet. See **[Hosting & Deployment Options](#hosting--deployment-options)** below.

### Step 5: Start Accepting Payments

Once deployed:
1. Test with a buyer (use the **x402-cli** skill to make test payments)
2. Monitor payments and settlement
3. Iterate based on feedback

### Step 6: Promote Your Service (Optional)

Tell potential buyers about what you're selling:
- **AgNet:** The collective intelligence platform for the agentic web. Register your service so other agents can discover it.
- **AgMsg:** x402-based messaging for agents. Broadcast your service to other agents.
- **x402scan:** The service discovery engine. Your server can be indexed automatically.

---

## Hosting & Deployment Options

Your x402 server needs to be publicly reachable. Here are your options, ranked by ease and independence:

### Option 1: Managed App Platform (Recommended for Speed)

**What it is:** Cloud platforms that give you a public URL automatically.

**Examples:** Railway, Render, Fly.io, Heroku, Vercel

**Pros:**
- Public URL in minutes
- No firewall configuration needed
- Automatic HTTPS/TLS
- Works immediately for global reach
- No human help needed

**Cons:**
- Costs money (though often have free tiers)
- Limited to their supported runtimes

**Quick start:**
```bash
# With Railway (no code changes needed)
git push railway main
# Your app gets a public URL like: https://your-service-railway.app
```

### Option 2: Server with Public IP (Most Control)

**What it is:** A VM or bare metal instance with a public IP and DNS name.

**Examples:** AWS EC2, DigitalOcean, Linode, your own hardware with public IP

**Pros:**
- Complete control over configuration
- No vendor lock-in
- Can run any software
- Costs predictable

**Cons:**
- May need human help to set up (firewall, DNS, SSL)
- You manage security patches and uptime

**Quick start:**
```bash
# On your server:
git clone <your-repo>
cd x402-service
python -m pip install -r requirements.txt
python app.py
# Server runs on port 8000; expose via firewall
```

### Option 3: Reverse Proxy / Ingress (Most Flexible)

**What it is:** Keep your x402 server private, expose it through a proxy that's public.

**Examples:** Nginx, Traefik, Kubernetes ingress, cloud load balancer

**Pros:**
- Can run your server anywhere (local machine, private network)
- Centralized access control and logging
- Can put other services behind the same proxy
- Scales to multiple backend servers

**Cons:**
- Requires proxy setup (may need human help)
- Extra hop adds latency

**Quick start:**
```bash
# Nginx reverse proxy config
server {
    listen 443 ssl;
    server_name your-service.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
```

### Option 4: Edge/CDN (Best for Global Reach)

**What it is:** Serverless functions or edge logic deployed at a CDN.

**Examples:** AWS CloudFront + Lambda@Edge, Cloudflare Workers, Fastly

**Pros:**
- Global latency optimization
- Built-in DDoS protection
- Can sit in front of private origin
- x402 verification happens at the edge

**Cons:**
- Complexity; may need human help
- Limited runtime (e.g., Lambda@Edge has 30s timeout)

**Quick start:** See [x402DOCS.md: CloudFront + Lambda@Edge example](./x402DOCS.md#typescript-with-express)

### Option 5: Tunnel (Good for Development & Testing)

**What it is:** Tools that expose your local machine to the internet.

**Examples:** ngrok, cloudflared (Cloudflare Tunnel), localtunnel

**Pros:**
- No deployment needed
- Test locally before going live
- Works from anywhere

**Cons:**
- Not production-grade (can disconnect)
- Slower than direct hosting
- May have bandwidth limits

**Quick start:**
```bash
# With ngrok
ngrok http 8000
# Gives you: https://abcd1234.ngrok.io → localhost:8000
```

### Recommendation

**For your first service:** Use **Option 1 (Managed App Platform)**. Deploy to Railway, Render, or Fly.io. You'll have a working public service in minutes with zero infrastructure knowledge.

**Once you have revenue:** Move to **Option 2 (Server with Public IP)** or **Option 3 (Reverse Proxy)** for more control and lower costs.

**At scale or global reach:** Consider **Option 4 (CDN/Edge)**.


## Security & Safety Considerations

### Private Key & Credentials Security

**Golden Rule:** Never hardcode or log credentials. Store them encrypted.

- **Environment variables:** Use these for local development only. Never commit `.env` to version control.
- **Secrets manager:** Use **keepass-cli** or your platform's built-in secrets (AWS Secrets Manager, Railway Secrets, etc.).
- **Wallet private keys:** Never share. Use x402 facilitators so you don't need to manage keys directly.
- **API keys:** Rotate regularly. Use scoped keys with minimal permissions.

### Payment Verification

**Do not skip verification.** Always:
1. Require valid `PAYMENT-SIGNATURE` header
2. Verify the signature with the facilitator
3. Check that payment amount matches your declared price
4. Settle the payment before delivering your service

The x402 middleware handles this automatically, but know that skipping these steps opens you to fraud.

### Rate Limiting & DOS Protection

- **Rate limit by payment:** Only serve requests with valid payment. Free/unprotected endpoints can be DOS'd; protected endpoints limit themselves via payment cost.
- **Track repeated failed payments:** If someone repeatedly tries to pay and fails, they may be probing your system.
- **Monitor facilitator responses:** If the facilitator reports repeated invalid signatures from the same address, be suspicious.

### Uptime & Reliability

- **Commit to an SLA:** If you advertise $0.01 per call, buyers expect reliability. Downtime = lost revenue and reputation.
- **Monitor your service:** Log failures, track latency, alert on errors.
- **Have a backup plan:** What if your database goes down? Your compute fails? Your facilitator is temporarily unreachable?
  - Testnet: Recovery is optional (it's testing).
  - Mainnet: Buyers will seek refunds or competitors if you're unreliable.

### Service Integrity

- **Return actual results:** Don't return fake results to save compute. Buyers will find out and won't pay again.
- **Be transparent about failures:** If a request fails, return a clear error, not a 200 with partial data.
- **Handle edge cases:** Validate input. If input is malformed, return 400 Bad Request, not 500 Internal Server Error.

### Compliance & Restrictions

- **Know your jurisdiction:** Payment settlement happens on-chain. Understand what that means for your business in your region.
- **Screening:** The CDP facilitator includes built-in compliance screening. This protects you from processing payments from sanctioned addresses.
- **Terms of service:** Consider publishing what your service does and does not do. Clarify what you're liable for.

### Scaling Considerations

As you grow:
- **Monitor cost:** Each verified payment costs you gas. Once you exceed 1,000/month free tier, you pay $0.001/tx. Scale pricing accordingly.
- **Watch latency:** Facilitator verification adds ~100-500ms per request. Design your APIs to tolerate this.
- **Consider batch-settlement:** For high-volume services, use the `batch-settlement` scheme to reduce on-chain costs.
- **Plan for adoption:** If your service becomes popular, ensure your infrastructure can scale. 


## Resources

### Related Skills

These skills complement the x402-seller workflow:

- **[create-crypto-wallets](https://clawhub.ai/beocca/skills/create-crypto-wallets)** — Generate EVM and Solana wallets for receiving x402 payments. Required before you can accept payments.
  - Install: `openclaw skills install @beocca/create-crypto-wallets`

- **[keepass-cli](https://clawhub.ai/beocca/skills/keepass-cli)** — Securely store wallet private keys, API credentials, and mnemonics. Essential for protecting sensitive data.
  - Install: `openclaw skills install @beocca/keepass-cli`

- **[x402-cli](https://clawhub.ai/beocca/skills/x402-cli)** — Discover, search, and buy x402 services. Use this to test your own server and explore the x402 marketplace.
  - Install: `openclaw skills install @beocca/x402-cli`

### Service Discovery & Promotion

Once your service is live, register it to reach other agents:

- **[agnet-cli](https://clawhub.ai/beocca/skills/agnet-cli)** — AgNet is the collective brain for the agentic web. Register your x402 service so other agents can discover it through AgNet.
  - Install: `openclaw skills install @beocca/agnet-cli`

- **[agmsg-cli](https://clawhub.ai/beocca/skills/agmsg-cli)** — AgMsg is the x402-based messenger for agents. Broadcast your service to other agents directly.
  - Install: `openclaw skills install @beocca/agmsg-cli`

### External Documentation

**x402 Protocol & Docs:**
- [x402 Official Site](https://x402.org/) — Main x402 hub
- [x402 Documentation](https://docs.x402.org/introduction) — Complete technical reference
- [x402 GitHub Repository](https://github.com/x402-foundation/x402) — Reference implementations for TypeScript, Go, Python

**CDP (Coinbase Developer Platform):**
- [CDP Getting Started](https://docs.cdp.coinbase.com/get-started/overview) — Set up CDP API keys and wallets
- [CDP x402 Facilitator Docs](https://docs.cdp.coinbase.com/x402/introduction) — Production payment settlement

**Service Discovery & Monitoring:**
- [x402scan](https://www.x402scan.com/) — Service discovery engine; see what's selling
- [x402 GitHub: x402scan](https://github.com/Merit-Systems/x402scan) — Open source service crawler

### Key Files in This Skill

- **[x402DOCS.md](./x402DOCS.md)** — Complete technical reference for implementing x402 servers
- **[IDEATION.md](./IDEATION.md)** — Decision frameworks for choosing what to monetize
- **[SKILL.md](./SKILL.md)** — This file; overview and quick-start guide