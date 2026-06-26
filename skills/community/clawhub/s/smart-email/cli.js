#!/usr/bin/env node
/**
 * email-cli — OpenClaw Email Skill
 *
 * On-demand email checking with AI summarization.
 *
 * Commands:
 *   check [--max N] [--since M] [--summarize] [--account EMAIL]
 *   read <uid> [--account EMAIL]
 *   digest [--date YYYY-MM-DD] [--account EMAIL]
 *   accounts
 *   setup <email>
 *   remove <email>
 *   config [key] [value]
 */

const path = require('path');
const DATA_DIR = path.join(__dirname, 'data');
const fs = require('fs');
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

const { initDb, addAccount, removeAccount, getAccounts, getAccount,
        addOAuthAccount, updateTokens } = require('./store');
const { fetchNewEmails, detectEmailType, IMAP_SERVERS } = require('./imap');
const { refreshAccessToken, requestDeviceCode, pollForToken, fetchEmailsViaGraph } = require('./oauth');
const { summarizeEmail, summarizeBatch } = require('./ai');
const config = require('./config');

// ─── CLI argument parsing ────────────────────────────────────

const args = process.argv.slice(2);
const command = args[0];

function getFlag(name) {
  const idx = args.indexOf('--' + name);
  if (idx === -1) return undefined;
  return args[idx + 1];
}

function hasFlag(name) {
  return args.includes('--' + name);
}

// ─── Main ────────────────────────────────────────────────────

async function main() {
  initDb();

  switch (command) {
    case 'check': return await cmdCheck();
    case 'read': return await cmdRead();
    case 'digest': return await cmdDigest();
    case 'accounts': return cmdAccounts();
    case 'setup': return await cmdSetup();
    case 'remove': return cmdRemove();
    case 'config': return cmdConfig();
    default:
      console.log(JSON.stringify({ error: 'Unknown command. Use: check, read, digest, accounts, setup, remove' }));
      process.exit(1);
  }
}

// ─── check ───────────────────────────────────────────────────

async function cmdCheck() {
  const max = parseInt(getFlag('max')) || 10;
  const since = parseInt(getFlag('since')) || 60; // minutes
  const doSummarize = hasFlag('summarize');
  const accountFilter = getFlag('account');

  const accounts = getAccounts().filter(a => !accountFilter || a.email === accountFilter);
  if (!accounts.length) {
    console.log(JSON.stringify({ error: 'No accounts configured. Use: setup <email>' }));
    return;
  }

  const results = [];

  for (const acct of accounts) {
    try {
      const emails = await fetchAccountEmails(acct, since);
      const limited = emails.slice(0, max);

      for (const email of limited) {
        const entry = {
          account: acct.email,
          uid: email.uid,
          from: email.from,
          fromAddr: email.fromAddr,
          to: email.to,
          subject: email.subject,
          date: email.date,
          bodyPreview: (email.body || '').substring(0, 300),
        };

        if (doSummarize) {
          entry.summary = await summarizeEmail(email.from, email.subject, email.body);
        }

        results.push(entry);
      }
    } catch (err) {
      results.push({ account: acct.email, error: err.message });
    }
  }

  console.log(JSON.stringify({ emails: results, total: results.length }, null, 2));
}

// ─── read ────────────────────────────────────────────────────

async function cmdRead() {
  const uid = args[1];
  if (!uid) {
    console.log(JSON.stringify({ error: 'Usage: read <uid> [--account EMAIL]' }));
    return;
  }

  const accountFilter = getFlag('account');
  const accounts = getAccounts().filter(a => !accountFilter || a.email === accountFilter);
  if (!accounts.length) {
    console.log(JSON.stringify({ error: 'No accounts configured' }));
    return;
  }

  // Fetch recent emails and find the one with matching uid
  for (const acct of accounts) {
    try {
      const emails = await fetchAccountEmails(acct, 1440); // last 24h
      const match = emails.find(e => e.uid === uid || e.uid === String(uid));
      if (match) {
        const summary = await summarizeEmail(match.from, match.subject, match.body);
        console.log(JSON.stringify({
          account: acct.email,
          uid: match.uid,
          from: match.from,
          fromAddr: match.fromAddr,
          to: match.to,
          subject: match.subject,
          date: match.date,
          body: match.body,
          summary,
        }, null, 2));
        return;
      }
    } catch (err) {
      // try next account
    }
  }

  console.log(JSON.stringify({ error: `Email with uid ${uid} not found` }));
}

// ─── digest ──────────────────────────────────────────────────

async function cmdDigest() {
  const accountFilter = getFlag('account');
  const since = parseInt(getFlag('since')) || 1440; // default 24h
  const accounts = getAccounts().filter(a => !accountFilter || a.email === accountFilter);

  if (!accounts.length) {
    console.log(JSON.stringify({ error: 'No accounts configured' }));
    return;
  }

  const allEmails = [];

  for (const acct of accounts) {
    try {
      const emails = await fetchAccountEmails(acct, since);
      for (const e of emails) {
        allEmails.push({ ...e, account: acct.email });
      }
    } catch (err) {
      allEmails.push({ account: acct.email, error: err.message });
    }
  }

  if (!allEmails.length) {
    console.log(JSON.stringify({ digest: 'No emails found', total: 0 }));
    return;
  }

  const digest = await summarizeBatch(allEmails);
  console.log(JSON.stringify({ digest, total: allEmails.length, emails: allEmails.map(e => ({
    account: e.account,
    from: e.from,
    subject: e.subject,
    date: e.date,
  }))}, null, 2));
}

// ─── accounts ────────────────────────────────────────────────

function cmdAccounts() {
  const accounts = getAccounts();
  if (!accounts.length) {
    console.log(JSON.stringify({ accounts: [], message: 'No accounts configured. Use: setup <email>' }));
    return;
  }

  console.log(JSON.stringify({
    accounts: accounts.map(a => ({
      email: a.email,
      type: a.email_type,
      auth: a.auth_type,
    })),
  }, null, 2));
}

// ─── setup ───────────────────────────────────────────────────

async function cmdSetup() {
  const email = args[1];
  if (!email || !email.includes('@')) {
    console.log(JSON.stringify({ error: 'Usage: setup <email>' }));
    return;
  }

  const existing = getAccount(email);
  if (existing) {
    console.log(JSON.stringify({ error: `${email} already configured. Use remove first.` }));
    return;
  }

  // Detect type
  const detected = await detectEmailType(email);
  console.error(`Detected: ${detected.label} (${detected.type})`);

  if (detected.type === 'outlook' || detected.type === 'unknown') {
    // For Outlook/M365, try OAuth2
    console.log(JSON.stringify({
      action: 'setup_pending',
      email,
      detected: detected.label,
      auth_options: ['oauth', 'password'],
      message: `Detected ${detected.label}. Use --auth oauth or --auth password --password <APP_PASSWORD>`,
    }));

    const authMethod = getFlag('auth') || 'oauth';

    if (authMethod === 'oauth') {
      return await setupOAuth(email, detected.type === 'unknown' ? 'outlook' : detected.type);
    } else {
      const password = getFlag('password');
      if (!password) {
        console.log(JSON.stringify({ error: 'Password required: --password <APP_PASSWORD>' }));
        return;
      }
      return await setupPassword(email, password, detected);
    }
  }

  // Gmail/Workspace/others need app password
  const password = getFlag('password');
  if (!password) {
    console.log(JSON.stringify({
      action: 'setup_need_password',
      email,
      detected: detected.label,
      message: `Run again with: setup ${email} --password <APP_PASSWORD>`,
    }));
    return;
  }

  await setupPassword(email, password, detected);
}

async function setupPassword(email, password, detected) {
  const serverArg = detected.host
    ? { host: detected.host, port: detected.port || 993 }
    : detected.type;

  try {
    const emails = await fetchNewEmails(email, password, 60, serverArg);
    let storeType = detected.type;
    if (detected.host && !['gmail', 'outlook', 'workspace'].includes(detected.type)) {
      storeType = `custom:${detected.host}:${detected.port || 993}`;
    }
    addAccount(email, password, storeType);
    console.log(JSON.stringify({
      success: true,
      email,
      type: detected.label,
      unread: emails.length,
    }));
  } catch (err) {
    console.log(JSON.stringify({ error: `Connection failed: ${err.message}` }));
  }
}

async function setupOAuth(email, emailType) {
  try {
    const dc = await requestDeviceCode();
    if (dc.error) {
      console.log(JSON.stringify({ error: `OAuth error: ${dc.error_description || dc.error}` }));
      return;
    }

    console.log(JSON.stringify({
      action: 'oauth_pending',
      verification_uri: dc.verification_uri,
      user_code: dc.user_code,
      message: `Open ${dc.verification_uri} and enter code: ${dc.user_code}`,
      expires_in: dc.expires_in,
    }));

    // Poll for token
    const tokens = await pollForToken(dc.device_code, dc.interval || 5, 300);
    const emails = await fetchEmailsViaGraph(tokens.access_token, 60);

    addOAuthAccount(email, emailType, tokens.access_token, tokens.refresh_token, tokens.expires_at);

    console.log(JSON.stringify({
      success: true,
      email,
      type: emailType,
      auth: 'oauth',
      unread: emails.length,
    }));
  } catch (err) {
    console.log(JSON.stringify({ error: `OAuth failed: ${err.message}` }));
  }
}

// ─── remove ──────────────────────────────────────────────────

function cmdRemove() {
  const email = args[1];
  if (!email) {
    console.log(JSON.stringify({ error: 'Usage: remove <email>' }));
    return;
  }

  const removed = removeAccount(email);
  console.log(JSON.stringify({
    success: removed,
    message: removed ? `Removed ${email}` : `${email} not found`,
  }));
}

// ─── config ──────────────────────────────────────────────────

function cmdConfig() {
  const key = args[1];
  const value = args[2];

  if (!key) {
    // Show all config
    const all = config.getAll();
    // Mask sensitive values
    const masked = {};
    for (const [k, v] of Object.entries(all)) {
      masked[k] = (k.includes('key') || k.includes('password') || k.includes('secret'))
        ? String(v).substring(0, 8) + '****'
        : v;
    }
    console.log(JSON.stringify({
      config: masked,
      available_keys: [
        'ai_api_key     — AI API key (DeepSeek / OpenAI compatible)',
        'ai_api_base    — AI API base URL (default: https://api.deepseek.com)',
        'ai_model       — AI model name (default: deepseek-chat)',
        'ms_client_id   — Microsoft OAuth2 Client ID',
        'ms_tenant_id   — Microsoft OAuth2 Tenant ID (default: common)',
      ],
    }, null, 2));
    return;
  }

  if (!value) {
    // Get single value
    const v = config.get(key, null);
    console.log(JSON.stringify({ [key]: v }));
    return;
  }

  // Set value
  config.set(key, value);
  console.log(JSON.stringify({ success: true, message: `${key} updated` }));
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

main().catch(err => {
  console.log(JSON.stringify({ error: err.message }));
  process.exit(1);
});
