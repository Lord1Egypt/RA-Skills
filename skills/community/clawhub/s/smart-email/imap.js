/**
 * imap.js — IMAP email fetching (reused from email-bot)
 */

const { ImapFlow } = require('imapflow');
const dns = require('dns').promises;

const MAX_BODY_LEN = 6000;
const CONNECT_TIMEOUT = 20000;

const IMAP_SERVERS = {
  gmail:     { host: 'imap.gmail.com',         port: 993 },
  outlook:   { host: 'outlook.office365.com',  port: 993 },
  workspace: { host: 'imap.gmail.com',         port: 993 },
  yahoo:     { host: 'imap.mail.yahoo.com',    port: 993 },
};

async function detectEmailType(email) {
  const domain = (email.split('@')[1] || '').toLowerCase();

  if (domain === 'gmail.com') return { type: 'gmail', label: 'Gmail' };
  if (['outlook.com', 'hotmail.com', 'live.com', 'msn.com'].includes(domain)) return { type: 'outlook', label: 'Outlook' };
  if (domain.includes('yahoo')) return { type: 'yahoo', label: 'Yahoo' };

  try {
    const mxRecords = await dns.resolveMx(domain);
    const mxHosts = mxRecords.map(r => r.exchange.toLowerCase()).join(' ');

    if (mxHosts.includes('google') || mxHosts.includes('gmail'))
      return { type: 'workspace', label: 'Google Workspace', mx: mxHosts };
    if (mxHosts.includes('outlook') || mxHosts.includes('microsoft') || mxHosts.includes('protection.outlook'))
      return { type: 'outlook', label: 'Microsoft 365', mx: mxHosts };
    if (mxHosts.includes('zoho'))
      return { type: 'custom', label: 'Zoho Mail', host: 'imap.zoho.com', port: 993 };
    if (mxHosts.includes('qq.com') || mxHosts.includes('exmail'))
      return { type: 'custom', label: '腾讯企业邮箱', host: 'imap.exmail.qq.com', port: 993 };
    if (mxHosts.includes('alibaba') || mxHosts.includes('aliyun'))
      return { type: 'custom', label: '阿里企业邮箱', host: 'imap.qiye.aliyun.com', port: 993 };

    return { type: 'unknown', label: '其他', mx: mxHosts, domain };
  } catch {
    return { type: 'unknown', label: '未知', domain };
  }
}

async function fetchNewEmails(email, authConfig, sinceMinutes = 10, emailType) {
  let server;

  if (typeof emailType === 'object' && emailType.host) {
    server = emailType;
    emailType = 'custom';
  } else {
    server = IMAP_SERVERS[emailType] || IMAP_SERVERS.gmail;
  }

  let authObj;
  if (typeof authConfig === 'object' && authConfig.accessToken) {
    authObj = { user: email, accessToken: authConfig.accessToken };
  } else {
    authObj = { user: email, pass: authConfig };
  }

  const client = new ImapFlow({
    host: server.host,
    port: server.port,
    secure: true,
    auth: authObj,
    logger: false,
    tls: { rejectUnauthorized: emailType === 'custom' ? false : true },
  });

  const emails = [];

  try {
    await Promise.race([
      client.connect(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('连接超时')), CONNECT_TIMEOUT)),
    ]);

    const lock = await client.getMailboxLock('INBOX');

    try {
      const since = new Date(Date.now() - sinceMinutes * 60 * 1000);
      const uids = await client.search({ seen: false, since }, { uid: true });

      if (!uids.length) { lock.release(); await client.logout(); return emails; }

      const fetchUids = uids.slice(-20);

      for await (const msg of client.fetch(fetchUids, {
        uid: true,
        envelope: true,
        bodyStructure: true,
        source: { maxBytes: MAX_BODY_LEN * 3 },
      }, { uid: true })) {
        const env = msg.envelope || {};
        const from = env.from?.[0];
        const fromStr = from ? (from.name || `${from.mailbox}@${from.host}`) : 'Unknown';
        const fromAddr = from ? `${from.mailbox}@${from.host}` : '';
        const to = env.to?.[0];
        const toStr = to ? (to.name || `${to.mailbox}@${to.host}`) : '';
        const subject = env.subject || '(No Subject)';
        const date = env.date || new Date();

        let body = '';
        if (msg.source) {
          body = extractTextBody(msg.source.toString('utf8'));
        }

        emails.push({
          uid: String(msg.uid),
          from: fromStr,
          fromAddr,
          to: toStr,
          subject,
          date: date instanceof Date ? date.toISOString() : String(date),
          body: body.substring(0, MAX_BODY_LEN),
        });
      }
    } finally {
      lock.release();
    }

    await client.logout();
  } catch (err) {
    try { await client.logout(); } catch {}
    throw err;
  }

  return emails;
}

function extractTextBody(rawEmail) {
  const headerEnd = rawEmail.indexOf('\r\n\r\n');
  if (headerEnd === -1) return stripHtml(rawEmail.substring(0, MAX_BODY_LEN));

  const headers = rawEmail.substring(0, headerEnd).toLowerCase();
  let body = rawEmail.substring(headerEnd + 4);

  const boundaryMatch = headers.match(/boundary="?([^";\r\n]+)"?/);
  if (boundaryMatch) body = extractFromMultipart(body, boundaryMatch[1]);

  const bodyHeaders = body.substring(0, Math.min(500, body.length)).toLowerCase();
  if (bodyHeaders.includes('content-transfer-encoding: base64') || headers.includes('content-transfer-encoding: base64')) {
    body = decodeBase64Part(body);
  } else if (bodyHeaders.includes('quoted-printable') || headers.includes('quoted-printable')) {
    body = decodeQuotedPrintable(body);
  }

  return stripHtml(body);
}

function extractFromMultipart(body, boundary) {
  const parts = body.split('--' + boundary);
  let textPlain = '', textHtml = '';

  for (const part of parts) {
    const partHeaderEnd = part.indexOf('\r\n\r\n');
    if (partHeaderEnd === -1) continue;

    const partHeaders = part.substring(0, partHeaderEnd).toLowerCase();
    let partBody = part.substring(partHeaderEnd + 4);

    const nestedBoundary = partHeaders.match(/boundary="?([^";\r\n]+)"?/);
    if (nestedBoundary) {
      const nested = extractFromMultipart(partBody, nestedBoundary[1]);
      if (nested) return nested;
      continue;
    }

    if (partHeaders.includes('content-transfer-encoding: base64')) partBody = decodeBase64Part(partBody);
    else if (partHeaders.includes('quoted-printable')) partBody = decodeQuotedPrintable(partBody);

    if (partHeaders.includes('text/plain')) textPlain = partBody;
    else if (partHeaders.includes('text/html')) textHtml = partBody;
  }

  if (textPlain.trim()) return textPlain;
  if (textHtml.trim()) return stripHtml(textHtml);
  return '';
}

function decodeBase64Part(text) {
  const lines = text.split('\r\n');
  const base64Lines = [];
  let started = false;
  for (const line of lines) {
    if (!started && line.trim() === '') { started = true; continue; }
    if (started || /^[A-Za-z0-9+/=]+$/.test(line.trim())) {
      started = true;
      if (line.startsWith('--')) break;
      base64Lines.push(line.trim());
    }
  }
  if (!base64Lines.length) {
    const cleaned = text.replace(/^[\s\S]*?\r\n\r\n/, '').replace(/[\r\n\s]/g, '').replace(/--.*/s, '');
    try { return Buffer.from(cleaned, 'base64').toString('utf8'); } catch { return text; }
  }
  try { return Buffer.from(base64Lines.join(''), 'base64').toString('utf8'); } catch { return text; }
}

function decodeQuotedPrintable(str) {
  return str.replace(/=\r?\n/g, '').replace(/=([0-9A-Fa-f]{2})/g, (_, hex) => String.fromCharCode(parseInt(hex, 16)));
}

function stripHtml(text) {
  return text
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<br\s*\/?>/gi, '\n').replace(/<\/p>/gi, '\n').replace(/<\/div>/gi, '\n')
    .replace(/<\/tr>/gi, '\n').replace(/<\/li>/gi, '\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n)))
    .replace(/\n{3,}/g, '\n\n').replace(/[ \t]+/g, ' ')
    .trim();
}

module.exports = { fetchNewEmails, detectEmailType, IMAP_SERVERS };
