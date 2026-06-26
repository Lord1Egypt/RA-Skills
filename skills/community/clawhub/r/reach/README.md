# Reach

Agent web interface. Gives AI agents the ability to browse websites, fill forms, login to services, sign crypto transactions, send and receive emails, watch for changes, and make payments.

9 primitives. 2 site skills + template. Intelligent router. MCP server for Claude Code. Free agent identity via mfer.one.

## Install

```bash
git clone https://github.com/Potdealer/reach.git
cd reach
npm install
npx playwright install chromium
cp .env.example .env  # Add your keys
```

## Quick Start

```javascript
import { Reach } from './src/index.js';

const reach = new Reach();

// Read a webpage
const page = await reach.fetch('https://example.com');
console.log(page.content);

// Interact with a page (click, type, submit)
await reach.act('https://example.com/form', 'submit', {
  data: { name: 'Ollie', email: 'ollie@exoagent.xyz' }
});

// Natural language
await reach.do('search github for solidity audit tools');

await reach.close();
```

## Free Agent Identity

Register a name on [ExoHost](https://github.com/Potdealer/exohost) and get a complete agent identity — website, email, and onchain naming — for free (5+ character names).

```
myagent.mfer.one     → your website (stored onchain as an NFT)
myagent@mfer.one     → your email inbox (send + receive)
```

```javascript
import { getRemoteInbox, readRemoteEmail, markRemoteRead } from './src/primitives/email.js';

// Check your inbox
const inbox = await getRemoteInbox('myagent');
console.log(`${inbox.total} emails for myagent@mfer.one`);

// Read an email
const email = await readRemoteEmail('myagent', inbox.emails[0].id);
console.log(email.subject, email.body);

// Mark it read
await markRemoteRead('myagent', inbox.emails[0].id);

// Send email from your mfer.one address
await reach.email('client@company.com', 'Audit Report', 'Found 3 critical issues...', {
  from: 'myagent@mfer.one'
});
```

Names are ERC-721 tokens on Base. 5+ characters are free (just gas). Shorter names have pricing tiers. The website content is stored directly on the NFT via Net Protocol.

## Primitives

### fetch(url, options?)

Read any webpage. Tries HTTP first, falls back to browser for JS-rendered sites.

```javascript
// Markdown (default)
const page = await reach.fetch('https://example.com');

// JSON API
const data = await reach.fetch('https://api.example.com/data', { format: 'json' });

// Force browser rendering
const spa = await reach.fetch('https://spa-app.com', { javascript: true });

// Screenshot
const shot = await reach.fetch('https://example.com', { format: 'screenshot' });
```

### act(url, action, params?)

Interact with web pages. Includes error recovery — tries 5 strategies (selector, text, role, aria-label, coordinates) before giving up.

```javascript
// Click by text
await reach.act(url, 'click', { text: 'Sign Up' });

// Click by selector
await reach.act(url, 'click', { selector: '#submit-btn' });

// Type into a field
await reach.act(url, 'type', { text: 'hello', selector: '#search' });

// Submit a form (auto-fills from form memory)
await reach.act(url, 'submit', {
  data: { username: 'ollie', email: 'ollie@exoagent.xyz' }
});

// Select from dropdown
await reach.act(url, 'select', { selector: '#country', value: 'US' });

// Scroll
await reach.act(url, 'scroll', { direction: 'down', amount: 500 });
```

### authenticate(service, method, credentials?)

Login to services and maintain sessions. Supports cookies, browser-based login, and API keys.

```javascript
// Reuse saved cookies
await reach.authenticate('github', 'cookie');

// Browser-based login (handles two-step, CAPTCHA)
await reach.authenticate('upwork', 'login', {
  url: 'https://www.upwork.com/ab/account-security/login',
  email: 'user@example.com',
  password: 'pass'
});

// API key
await reach.authenticate('basescan', 'apikey', {
  apiKey: 'your-key',
  headerName: 'X-API-Key'
});
```

### sign(payload, options?)

Sign messages, transactions, or EIP-712 typed data with an Ethereum wallet.

```javascript
// Sign a message
const sig = await reach.sign('hello from reach');
// { signature: '0x...', address: '0x...', type: 'message' }

// Send a transaction
const tx = await reach.sign({ to: '0x...', value: '1000000000000000' }, { type: 'transaction' });

// EIP-712 typed data
const typed = await reach.sign({ domain: {...}, types: {...}, value: {...} }, { type: 'typed' });
```

### observe(target, options?, callback)

Watch URLs, APIs, WebSocket feeds, or contract events for changes.

```javascript
// Poll a URL every 30 seconds, fire on change
const watcher = await reach.observe('https://api.example.com/price', {
  interval: 30000,
  field: 'data.price',
}, (event) => console.log('Changed:', event.newState));

// Price threshold alert
const alert = await reach.observe('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd', {
  interval: 60000,
  field: 'ethereum.usd',
  threshold: 5000,
  direction: 'above',
}, (event) => console.log('ETH above $5000!'));

// Watch contract events
const contract = await reach.observe('0x1234...', {
  event: 'Transfer',
  abi: ['event Transfer(address indexed from, address indexed to, uint256 value)'],
}, (event) => console.log('Transfer:', event.args));

// WebSocket
const ws = await reach.observe('wss://stream.example.com', {}, (event) => {
  console.log('Message:', event.data);
});

// Stop watching
watcher.stop();
```

### pay(recipient, amount, options?)

Send ETH, ERC-20 tokens, or handle x402 HTTP payment flows.

```javascript
// Send ETH
await reach.pay('0x1234...', '0.01');

// Send USDC
await reach.pay('0x1234...', '10', { token: 'USDC' });

// Send any ERC-20 by address
await reach.pay('0x1234...', '100', { token: '0xTokenAddress...' });

// x402 payment (URL returns 402, Reach pays and retries)
const content = await reach.pay('https://premium-api.com/data', '0.001', {
  x402: true
});
```

Known tokens on Base: `USDC`, `WETH`, `DAI`, `USDbC`.

### persist(key, value) / recall(key) / forget(key)

Local state memory with optional TTL.

```javascript
reach.persist('last-check', new Date().toISOString());
reach.persist('config', { retries: 3 }, { ttl: 3600 }); // expires in 1 hour

const val = reach.recall('last-check');
reach.forget('old-key');
const keys = reach.listKeys();
```

### see(url, question?)

Screenshot + accessibility tree extraction for visual reasoning.

```javascript
const view = await reach.see('https://example.com');
// { screenshot: '/path/to/file.png', description: '...', elements: [...], title: '...' }
```

### email(to, subject, body, options?)

Send and receive email. Agents get their own inbox at `name@mfer.one`.

**Sending:**

```javascript
// Send from default address
await reach.email('client@company.com', 'Audit Report', 'Found 3 critical issues...');

// Send from a mfer.one address
await reach.email('user@example.com', 'Hello', 'gm from the chain', { from: 'myagent@mfer.one' });

// HTML email
await reach.email('user@example.com', 'Welcome', '<h1>Hello</h1>', { html: true });
```

**Receiving (via webhook):**

Incoming email to `*@mfer.one` is routed through a Cloudflare Email Worker, which POSTs JSON to the Reach webhook server at `/email`. Start the webhook server to receive:

```javascript
import { WebhookServer } from './src/utils/webhook-server.js';
const server = new WebhookServer({ port: 8430 });
await server.start(); // /email handler is registered automatically
```

**Remote inbox (Cloudflare KV):**

Read emails stored in the remote inbox without running a local webhook server:

```javascript
import { getRemoteInbox, readRemoteEmail, markRemoteRead } from './src/primitives/email.js';

// List emails
const inbox = await getRemoteInbox('myagent', { unread: true, limit: 10 });

// Read a specific email
const email = await readRemoteEmail('myagent', messageId);

// Mark as read
await markRemoteRead('myagent', messageId);
```

**Local inbox:**

```javascript
// Check unread count
const count = reach.getUnreadCount();

// List emails
const emails = reach.getInbox({ unread: true, limit: 10 });

// Read full email (including body)
const email = reach.readEmail(messageId);

// Mark as read
reach.markRead(messageId);
```

**Replying (threads correctly via In-Reply-To/References headers):**

```javascript
await reach.replyEmail(messageId, 'Thanks for reaching out. Here is the audit report...');
```

**Event-driven (react to incoming email):**

```javascript
reach.onEmail((email) => {
  console.log(`New email from ${email.from}: ${email.subject}`);
  // Agent decides how to respond
});
```

Emails are persisted to `data/inbox/` as individual JSON files with an index. Inbox caps at 1000 emails.

## Site Skills

### Included

Two built-in site skills for common platforms:

```javascript
// GitHub (API-first, no browser needed)
const repo = await reach.sites.github.getRepoInfo('Potdealer', 'exoskeletons');
const issues = await reach.sites.github.listIssues('Potdealer', 'exoskeletons');
const code = await reach.sites.github.search('ERC-6551', 'code');

// Exoskeletons (onchain — reads NFT data, reputation, ELO)
const profile = await reach.sites.exoskeletons.getProfile(tokenId);
const reputation = await reach.sites.exoskeletons.getReputation(tokenId);
const elo = await reach.sites.exoskeletons.getELO(tokenId);
```

### Write Your Own

Copy `src/sites/example.js` as a template. Each site skill exports functions for login, search, form submission, and page reading. Drop your file in `src/sites/` and it gets picked up by the router.

```javascript
// src/sites/my-platform.js
export const name = 'my-platform';
export const domain = 'my-platform.com';

export async function login(reach, credentials) { /* ... */ }
export async function search(reach, query) { /* ... */ }
```

Private site skills go in `private-sites/` (gitignored).

## CAPTCHA Solving

Reach handles CAPTCHAs automatically during browser interactions via [CapSolver](https://www.capsolver.com/). Supports reCAPTCHA v2/v3, hCaptcha, and FunCaptcha.

```javascript
// Automatic — CAPTCHA solving kicks in during authenticate() and act()
await reach.authenticate('upwork', 'login', credentials);

// Manual
import { solveCaptcha } from './src/primitives/captcha.js';
const token = await solveCaptcha({ type: 'recaptchav2', sitekey: '...', url: '...' });
```

Requires `CAPSOLVER_API_KEY` in `.env`.

## Session Recording

Record and replay everything Reach does:

```javascript
// Record
reach.startRecording('my-audit');
await reach.fetch('https://code4rena.com/audits');
await reach.act(url, 'click', { text: 'View Scope' });
const log = reach.stopRecording();

// Replay
const session = loadRecording('my-audit');
console.log(formatTimeline(session));
```

```bash
# CLI
node src/cli.js replay                    # List recordings
node src/cli.js replay my-audit           # Replay a session
```

## Form Memory

Reach remembers form fields and auto-fills on repeat visits:

```javascript
// Automatic: when act('submit') is used, form data is saved
// Next time: known fields are pre-filled from memory

// Manual
import { saveForm, recallForm, listForms } from './src/utils/form-memory.js';
saveForm('https://example.com/apply', [{ name: 'email', value: 'ollie@exoagent.xyz' }]);
```

## Error Recovery

When an interaction fails, Reach tries 5 strategies before giving up:

1. **Selector** — CSS selector match
2. **Text** — visible text content match
3. **Role** — ARIA role lookup
4. **Aria-label** — accessibility label match
5. **Coordinates** — pixel position click as last resort

This means `act()` calls are resilient to minor DOM changes across page versions.

## Router

The router picks the optimal interaction layer for each task:

```
Priority: API > HTTP > Browser > Vision
```

```javascript
// Auto-route
const plan = reach.route({ type: 'read', url: 'https://api.github.com/repos/...' });
// { primitive: 'fetch', layer: 'api', reason: 'Known API for api.github.com' }

// Teach the router about new sites
reach.learnSite('https://myapp.com', { needsJS: true, needsAuth: true });

// Execute through router
await reach.execute({ type: 'read', url: 'https://myapp.com/dashboard' });
```

## Natural Language

Parse and execute commands without code:

```javascript
// Parse only
const plan = reach.parseCommand('search github for solidity jobs');
// { primitive: 'site', method: 'search', site: 'github', params: { query: 'solidity jobs' } }

// Parse and execute
const result = await reach.do('go to github');
const result2 = await reach.do('send 0.01 ETH to 0x1234...');
const result3 = await reach.do('watch api.coingecko.com every 60s');
```

Supported patterns: `go to`, `search X for Y`, `click`, `type`, `email`, `send`, `watch`, `remember`, `recall`, `screenshot`, `login to`.

## Webhook Server

Listen for incoming webhooks (email, GitHub events, Stripe, etc.):

```javascript
import { WebhookServer } from './src/utils/webhook-server.js';

const server = new WebhookServer({ port: 8430 });
server.on('/github', (payload) => console.log('Push event:', payload));
server.on('/stripe', (payload) => console.log('Payment:', payload));
await server.start();
```

```bash
# Standalone
node src/webhook-start.js

# CLI
node src/cli.js webhook --port 8430 --on /github --on /stripe
```

## Exoskeleton Identity

Reach integrates with [Exoskeletons](https://exoagent.xyz) for onchain agent identity. Middleware can gate access by NFT ownership, reputation score, or ELO rating.

```javascript
import { exoIdentityMiddleware } from './src/utils/exo-identity.js';

// Require caller to own an Exoskeleton
const middleware = exoIdentityMiddleware({ requireExo: true, minReputation: 10 });
```

## MCP Server

Expose Reach as MCP tools for Claude Code:

```bash
node src/mcp.js
```

Add to your Claude Code config:
```json
{
  "mcpServers": {
    "reach": {
      "command": "node",
      "args": ["/path/to/reach/src/mcp.js"]
    }
  }
}
```

Tools: `web_fetch`, `web_act`, `web_authenticate`, `web_sign`, `web_see`, `web_email`

## CLI

```bash
# Primitives
node src/cli.js fetch <url> [--format markdown|html|json|screenshot] [--js]
node src/cli.js act <url> <click|type|submit|select> [target]
node src/cli.js auth <service> [cookie|login]
node src/cli.js sign <message>
node src/cli.js store <key> [value]
node src/cli.js see <url>

# Navigation
node src/cli.js sessions
node src/cli.js route <url> [--type read|interact|auth]
node src/cli.js learn <url> [--needsJS] [--needsAuth]

# Natural language
node src/cli.js do "go to github"
node src/cli.js parse "search github for solidity"

# Recording
node src/cli.js replay [session-file]
node src/cli.js forms

# Email
node src/cli.js email <to> <subject> <body> [--from agent@mfer.one]
node src/cli.js inbox [--unread] [--from addr] [--limit N]
node src/cli.js read <messageId>
node src/cli.js reply <messageId> <body>

# Webhook
node src/cli.js webhook [--port 8430] [--on /path]

# Cookies
node src/cli.js import-cookies <service> <file> [format]
node src/cli.js export-instructions [chrome|firefox]
```

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `PRIVATE_KEY` | For sign/pay | Ethereum wallet private key |
| `RPC_URL` | No | RPC endpoint (default: Base mainnet) |
| `RESEND_API_KEY` | For email | Resend API key (send from @exoagent.xyz or @mfer.one) |
| `CAPSOLVER_API_KEY` | For CAPTCHA | CapSolver API key |
| `GITHUB_TOKEN` | For GitHub API | GitHub personal access token |

## License

MIT
