#!/usr/bin/env node
/**
 * server.js — Email Skill Web UI
 *
 * Usage: node server.js [--port 3900]
 */

const http = require('http');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');

const DATA_DIR = path.join(__dirname, 'data');
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

const { initDb, addAccount, removeAccount, getAccounts, getAccount,
        addOAuthAccount, updateTokens } = require('./store');
const { fetchNewEmails, detectEmailType, IMAP_SERVERS } = require('./imap');
const { refreshAccessToken, requestDeviceCode, pollForToken, fetchEmailsViaGraph } = require('./oauth');
const { summarizeEmail, summarizeBatch } = require('./ai');
const config = require('./config');

// ─── Args ────────────────────────────────────────────────────

const args = process.argv.slice(2);
function getArg(name, def) {
  const idx = args.indexOf('--' + name);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : def;
}

const PORT = parseInt(getArg('port', '3900'));

// ─── Auth ────────────────────────────────────────────────────

function getOrCreateToken() {
  let token = config.get('web_token', '');
  if (!token) {
    token = crypto.randomBytes(24).toString('hex');
    config.set('web_token', token);
  }
  return token;
}

function checkAuth(req) {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const cookieToken = (req.headers.cookie || '').split(';')
    .map(c => c.trim().split('='))
    .find(([k]) => k === 'token')?.[1];
  const queryToken = url.searchParams.get('token');
  const expected = getOrCreateToken();
  return cookieToken === expected || queryToken === expected;
}

// ─── API Routes ──────────────────────────────────────────────

async function handleApi(req, res, pathname, body) {
  const json = (data, status = 200) => {
    res.writeHead(status, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
  };

  // Auth check
  if (pathname !== '/api/login') {
    if (!checkAuth(req)) return json({ error: 'Unauthorized' }, 401);
  }

  try {
    // POST /api/login
    if (pathname === '/api/login' && req.method === 'POST') {
      const { token } = JSON.parse(body);
      if (token === getOrCreateToken()) {
        res.writeHead(200, {
          'Content-Type': 'application/json',
          'Set-Cookie': `token=${token}; Path=/; HttpOnly; SameSite=Strict; Max-Age=31536000`,
        });
        res.end(JSON.stringify({ success: true }));
      } else {
        json({ error: 'Invalid token' }, 401);
      }
      return;
    }

    // GET /api/config
    if (pathname === '/api/config' && req.method === 'GET') {
      const all = config.getAll();
      const masked = {};
      for (const [k, v] of Object.entries(all)) {
        if (k === 'web_token') continue;
        masked[k] = (k.includes('key') || k.includes('password') || k.includes('secret'))
          ? (String(v).substring(0, 8) + '****') : v;
      }
      return json({ config: masked });
    }

    // POST /api/config
    if (pathname === '/api/config' && req.method === 'POST') {
      const { key, value } = JSON.parse(body);
      if (!key) return json({ error: 'key required' }, 400);
      config.set(key, value);
      return json({ success: true });
    }

    // GET /api/accounts
    if (pathname === '/api/accounts') {
      const accounts = getAccounts();
      return json({
        accounts: accounts.map(a => ({
          email: a.email,
          type: a.email_type,
          auth: a.auth_type,
        })),
      });
    }

    // POST /api/accounts/add
    if (pathname === '/api/accounts/add' && req.method === 'POST') {
      const { email, password, auth } = JSON.parse(body);
      if (!email) return json({ error: 'email required' }, 400);

      if (getAccount(email)) return json({ error: `${email} already exists` }, 400);

      const detected = await detectEmailType(email);

      if (auth === 'oauth') {
        const dc = await requestDeviceCode();
        if (dc.error) return json({ error: dc.error_description || dc.error }, 500);
        // Return device code for user to authorize
        return json({
          action: 'oauth_pending',
          email,
          detected: detected.label,
          verification_uri: dc.verification_uri,
          user_code: dc.user_code,
          device_code: dc.device_code,
          interval: dc.interval || 5,
        });
      }

      if (!password) return json({ error: 'password required', detected: detected.label }, 400);

      const serverArg = detected.host
        ? { host: detected.host, port: detected.port || 993 }
        : detected.type;

      const emails = await fetchNewEmails(email, password, 60, serverArg);
      let storeType = detected.type;
      if (detected.host && !['gmail', 'outlook', 'workspace'].includes(detected.type)) {
        storeType = `custom:${detected.host}:${detected.port || 993}`;
      }
      addAccount(email, password, storeType);
      return json({ success: true, email, type: detected.label, unread: emails.length });
    }

    // POST /api/accounts/oauth-poll
    if (pathname === '/api/accounts/oauth-poll' && req.method === 'POST') {
      const { email, device_code, interval } = JSON.parse(body);
      const tokens = await pollForToken(device_code, interval || 5, 300);
      const emails = await fetchEmailsViaGraph(tokens.access_token, 60);
      const detected = await detectEmailType(email);
      addOAuthAccount(email, detected.type || 'outlook', tokens.access_token, tokens.refresh_token, tokens.expires_at);
      return json({ success: true, email, unread: emails.length });
    }

    // POST /api/accounts/remove
    if (pathname === '/api/accounts/remove' && req.method === 'POST') {
      const { email } = JSON.parse(body);
      const removed = removeAccount(email);
      return json({ success: removed });
    }

    // POST /api/check
    if (pathname === '/api/check' && req.method === 'POST') {
      const { account, max = 10, since = 60, summarize = false } = JSON.parse(body || '{}');
      const accounts = getAccounts().filter(a => !account || a.email === account);
      if (!accounts.length) return json({ error: 'No accounts configured' }, 400);

      const results = [];
      for (const acct of accounts) {
        try {
          const emails = await fetchAccountEmails(acct, since);
          for (const email of emails.slice(0, max)) {
            const entry = {
              account: acct.email,
              uid: email.uid,
              from: email.from,
              fromAddr: email.fromAddr,
              subject: email.subject,
              date: email.date,
              bodyPreview: (email.body || '').substring(0, 300),
            };
            if (summarize) {
              entry.summary = await summarizeEmail(email.from, email.subject, email.body);
            }
            results.push(entry);
          }
        } catch (err) {
          results.push({ account: acct.email, error: err.message });
        }
      }
      return json({ emails: results, total: results.length });
    }

    // POST /api/read
    if (pathname === '/api/read' && req.method === 'POST') {
      const { uid, account } = JSON.parse(body);
      const accounts = getAccounts().filter(a => !account || a.email === account);

      for (const acct of accounts) {
        try {
          const emails = await fetchAccountEmails(acct, 1440);
          const match = emails.find(e => e.uid === uid || e.uid === String(uid));
          if (match) {
            const summary = await summarizeEmail(match.from, match.subject, match.body);
            return json({ ...match, account: acct.email, summary });
          }
        } catch {}
      }
      return json({ error: 'Email not found' }, 404);
    }

    // POST /api/digest
    if (pathname === '/api/digest' && req.method === 'POST') {
      const { account, since = 1440 } = JSON.parse(body || '{}');
      const accounts = getAccounts().filter(a => !account || a.email === account);
      const allEmails = [];

      for (const acct of accounts) {
        try {
          const emails = await fetchAccountEmails(acct, since);
          for (const e of emails) allEmails.push({ ...e, account: acct.email });
        } catch {}
      }

      if (!allEmails.length) return json({ digest: '没有新邮件', total: 0 });
      const digest = await summarizeBatch(allEmails);
      return json({ digest, total: allEmails.length });
    }

    json({ error: 'Not found' }, 404);
  } catch (err) {
    json({ error: err.message }, 500);
  }
}

// ─── Helpers ─────────────────────────────────────────────────

async function fetchAccountEmails(acct, sinceMinutes) {
  if (acct.auth_type === 'oauth') {
    let accessToken = acct.access_token;
    const needsRefresh = !accessToken || (acct.token_expires && Date.now() > acct.token_expires - 300000);
    if (needsRefresh) {
      const newTokens = await refreshAccessToken(acct.refresh_token);
      accessToken = newTokens.access_token;
      updateTokens(acct.email, newTokens.access_token, newTokens.refresh_token, newTokens.expires_at);
    }
    return await fetchEmailsViaGraph(accessToken, sinceMinutes);
  }

  let serverArg = acct.email_type || 'gmail';
  if (serverArg.startsWith('custom:')) {
    const p = serverArg.split(':');
    serverArg = { host: p[1], port: parseInt(p[2]) || 993 };
  }
  return await fetchNewEmails(acct.email, acct.password, sinceMinutes, serverArg);
}

// ─── HTML UI ─────────────────────────────────────────────────

function getHtml() {
  return fs.readFileSync(path.join(__dirname, 'ui.html'), 'utf-8');
}

// ─── Server ──────────────────────────────────────────────────

initDb();

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const pathname = url.pathname;

  // Collect body
  let body = '';
  if (req.method === 'POST') {
    for await (const chunk of req) body += chunk;
  }

  // API
  if (pathname.startsWith('/api/')) {
    return handleApi(req, res, pathname, body);
  }

  // UI
  if (pathname === '/' || pathname === '/index.html') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(getHtml());
    return;
  }

  res.writeHead(404);
  res.end('Not Found');
});

server.listen(PORT, () => {
  const token = getOrCreateToken();
  console.log(`\n📧 Email Skill Web UI`);
  console.log(`   http://localhost:${PORT}?token=${token}\n`);
  console.log(`   Share this URL to give access (token included).\n`);
});
