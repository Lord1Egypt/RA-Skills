/**
 * oauth.js — Microsoft OAuth2 Device Code Flow + Graph API
 */

const https = require('https');
const { get } = require('./config');

function getOAuthConfig() {
  return {
    clientId: get('ms_client_id', ''),
    tenantId: get('ms_tenant_id', 'common'),
    scopes: get('ms_scopes', 'https://graph.microsoft.com/Mail.Read offline_access'),
  };
}

function httpsRequest(method, url, body, headers = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const data = body ? (typeof body === 'string' ? body : new URLSearchParams(body).toString()) : '';
    const reqHeaders = { ...headers };
    if (method === 'POST' && !headers['Content-Type']) {
      reqHeaders['Content-Type'] = 'application/x-www-form-urlencoded';
      reqHeaders['Content-Length'] = Buffer.byteLength(data);
    }
    const req = https.request({
      hostname: u.hostname,
      path: u.pathname + u.search,
      method,
      headers: reqHeaders,
    }, (res) => {
      let buf = '';
      res.on('data', d => buf += d);
      res.on('end', () => {
        try { resolve(JSON.parse(buf)); } catch { resolve({ raw: buf }); }
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

async function requestDeviceCode() {
  const { clientId, tenantId, scopes } = getOAuthConfig();
  if (!clientId) throw new Error('ms_client_id not configured. Run: node cli.js config ms_client_id <YOUR_CLIENT_ID>');
  return await httpsRequest('POST', `https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/devicecode`, {
    client_id: clientId,
    scope: scopes,
  });
}

async function pollForToken(deviceCode, interval = 5, timeout = 300) {
  const { clientId, tenantId } = getOAuthConfig();
  const url = `https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`;
  const start = Date.now();

  while (Date.now() - start < timeout * 1000) {
    await new Promise(r => setTimeout(r, interval * 1000));

    const result = await httpsRequest('POST', url, {
      grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
      client_id: clientId,
      device_code: deviceCode,
    });

    if (result.access_token) {
      return {
        access_token: result.access_token,
        refresh_token: result.refresh_token,
        expires_at: Date.now() + (result.expires_in || 3600) * 1000,
      };
    }

    if (result.error === 'authorization_pending') continue;
    if (result.error === 'slow_down') { interval += 5; continue; }
    if (result.error === 'expired_token') throw new Error('Authorization timeout');
    if (result.error) throw new Error(result.error_description || result.error);
  }

  throw new Error('Authorization timeout');
}

async function refreshAccessToken(refreshToken) {
  const { clientId, tenantId, scopes } = getOAuthConfig();
  const result = await httpsRequest('POST', `https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`, {
    grant_type: 'refresh_token',
    client_id: clientId,
    refresh_token: refreshToken,
    scope: scopes,
  });

  if (result.error) throw new Error(result.error_description || result.error);

  return {
    access_token: result.access_token,
    refresh_token: result.refresh_token || refreshToken,
    expires_at: Date.now() + (result.expires_in || 3600) * 1000,
  };
}

async function fetchEmailsViaGraph(accessToken, sinceMinutes = 10) {
  const since = new Date(Date.now() - sinceMinutes * 60 * 1000).toISOString();
  const filter = encodeURIComponent(`isRead eq false and receivedDateTime ge ${since}`);
  const select = 'id,subject,from,toRecipients,receivedDateTime,body,bodyPreview,isRead';
  const url = `https://graph.microsoft.com/v1.0/me/messages?$filter=${filter}&$top=20&$orderby=receivedDateTime desc&$select=${select}`;

  const result = await httpsRequest('GET', url, null, {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  });

  if (result.error) throw new Error(result.error.message || result.error.code || 'Graph API error');

  const emails = [];
  for (const msg of (result.value || [])) {
    const from = msg.from?.emailAddress;
    const to = msg.toRecipients?.[0]?.emailAddress;

    let body = '';
    if (msg.body) {
      body = msg.body.contentType === 'text' ? (msg.body.content || '') : stripHtml(msg.body.content || '');
    }
    if (!body && msg.bodyPreview) body = msg.bodyPreview;

    emails.push({
      uid: msg.id,
      from: from?.name || from?.address || 'Unknown',
      fromAddr: from?.address || '',
      to: to?.name || to?.address || '',
      subject: msg.subject || '(No Subject)',
      date: msg.receivedDateTime || new Date().toISOString(),
      body: body.substring(0, 6000),
    });
  }

  return emails;
}

function stripHtml(text) {
  return text
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<br\s*\/?>/gi, '\n').replace(/<\/p>/gi, '\n').replace(/<\/div>/gi, '\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/\n{3,}/g, '\n\n').replace(/[ \t]+/g, ' ')
    .trim();
}

module.exports = { requestDeviceCode, pollForToken, refreshAccessToken, fetchEmailsViaGraph };
