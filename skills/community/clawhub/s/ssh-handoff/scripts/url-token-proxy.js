#!/usr/bin/env node
const http = require('http');
const net = require('net');
const { URL } = require('url');
const crypto = require('crypto');

const listenHost = process.env.LISTEN_HOST || '127.0.0.1';
const listenPort = Number(process.env.LISTEN_PORT || '0');
const upstreamHost = process.env.UPSTREAM_HOST || '127.0.0.1';
const upstreamPort = Number(process.env.UPSTREAM_PORT || '7681');
const token = process.env.ACCESS_TOKEN || '';
const ttlMs = Number(process.env.TTL_MS || String(30 * 60 * 1000));
const writableCookie = process.env.SESSION_COOKIE || 'ssh_handoff_session';
const sessionSecret = process.env.SESSION_SECRET || token;
const secureCookie = /^(1|true|yes|on)$/i.test(process.env.COOKIE_SECURE || '');
const expectedHost = process.env.EXPECTED_HOST || '';
const expectedOrigin = process.env.EXPECTED_ORIGIN || '';
const allowedClientIp = process.env.ALLOWED_CLIENT_IP || '';

if (!token) {
  console.error('Missing ACCESS_TOKEN');
  process.exit(1);
}

let sessionEstablished = false;
let bootstrapUntil = 0;
const expiresAt = Date.now() + ttlMs;
let shuttingDown = false;
const sockets = new Set();

function sha256(value) {
  return crypto.createHash('sha256').update(String(value)).digest('hex');
}

function log(event, details = {}) {
  const payload = {
    ts: new Date().toISOString(),
    event,
    ...details,
  };
  try {
    process.stderr.write(`${JSON.stringify(payload)}\n`);
  } catch {
    process.stderr.write(`{"ts":"${new Date().toISOString()}","event":"log-error"}\n`);
  }
}

function respond(res, statusCode, message) {
  res.statusCode = statusCode;
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.end(message);
}

function unauthorized(res) {
  respond(res, 403, 'Forbidden');
}

function expired(res) {
  respond(res, 410, 'Link expired');
}

function badRequest(res, message = 'Bad request') {
  respond(res, 400, message);
}

function parseCookies(req) {
  const raw = req.headers.cookie || '';
  const out = {};
  for (const part of raw.split(';')) {
    const idx = part.indexOf('=');
    if (idx === -1) continue;
    const k = part.slice(0, idx).trim();
    const v = part.slice(idx + 1).trim();
    out[k] = v;
  }
  return out;
}

function normalizeHost(value) {
  return String(value || '').trim().toLowerCase();
}

function normalizeOrigin(value) {
  return String(value || '').trim().replace(/\/$/, '').toLowerCase();
}

function getRemoteAddress(reqOrSocket) {
  return (
    reqOrSocket.socket?.remoteAddress ||
    reqOrSocket.connection?.remoteAddress ||
    reqOrSocket.remoteAddress ||
    ''
  );
}

function ipAllowed(remoteAddress) {
  if (!allowedClientIp) return true;
  if (!remoteAddress) return false;
  const normalized = remoteAddress.replace(/^::ffff:/, '');
  return normalized === allowedClientIp;
}

function hostAllowed(hostHeader) {
  if (!expectedHost) return true;
  return normalizeHost(hostHeader) === normalizeHost(expectedHost);
}

function originAllowed(originHeader) {
  if (!expectedOrigin) return true;
  if (!originHeader) return false;
  return normalizeOrigin(originHeader) === normalizeOrigin(expectedOrigin);
}

function setSessionCookie(res) {
  const parts = [
    `${writableCookie}=${sessionSecret}`,
    'HttpOnly',
    'SameSite=Strict',
    'Path=/',
  ];
  if (secureCookie) parts.push('Secure');
  res.setHeader('Set-Cookie', parts.join('; '));
}

function shutdown() {
  if (shuttingDown) return;
  shuttingDown = true;
  log('shutdown', { reason: 'ttl-or-signal' });
  for (const socket of sockets) {
    socket.destroy();
  }
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 1000).unref();
}

function validateRequest(req, res) {
  const remoteAddress = getRemoteAddress(req);
  if (!ipAllowed(remoteAddress)) {
    log('reject-ip', { remoteAddress });
    if (res) unauthorized(res);
    return { ok: false };
  }

  const hostHeader = req.headers.host || '';
  if (!hostAllowed(hostHeader)) {
    log('reject-host', { hostHeader, remoteAddress });
    if (res) badRequest(res, 'Invalid host');
    return { ok: false };
  }

  const upgrade = String(req.headers.upgrade || '').toLowerCase();
  const connection = String(req.headers.connection || '').toLowerCase();
  const isWebSocket = upgrade === 'websocket' || connection.includes('upgrade');
  if (isWebSocket) {
    const originHeader = req.headers.origin || '';
    if (!originAllowed(originHeader)) {
      log('reject-origin', { originHeader, remoteAddress });
      if (res) unauthorized(res);
      return { ok: false };
    }
  }

  return { ok: true, remoteAddress, isWebSocket };
}

function proxyHttp(req, res) {
  const options = {
    host: upstreamHost,
    port: upstreamPort,
    method: req.method,
    path: req.url,
    headers: {
      ...req.headers,
      host: `${upstreamHost}:${upstreamPort}`,
    },
  };

  delete options.headers.origin;

  const upstream = http.request(options, (upstreamRes) => {
    res.writeHead(upstreamRes.statusCode || 502, upstreamRes.headers);
    upstreamRes.pipe(res);
  });

  upstream.on('error', (err) => {
    log('upstream-http-error', { message: err.message });
    respond(res, 502, 'Upstream error');
  });

  req.pipe(upstream);
}

const server = http.createServer((req, res) => {
  if (Date.now() > expiresAt) return expired(res);

  const validation = validateRequest(req, res);
  if (!validation.ok) return;

  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const cookies = parseCookies(req);
  const hasSession = cookies[writableCookie] === sessionSecret;
  const presentedToken = url.searchParams.get('token');

  if (!hasSession) {
    const tokenValid = presentedToken === token;
    const inBootstrapWindow = sessionEstablished && Date.now() <= bootstrapUntil;
    if (!tokenValid && !inBootstrapWindow) {
      log(sessionEstablished ? 'reject-expired-sessionless' : 'reject-no-auth', {
        remoteAddress: validation.remoteAddress,
      });
      return sessionEstablished ? expired(res) : unauthorized(res);
    }
    if (tokenValid && !sessionEstablished) {
      sessionEstablished = true;
      bootstrapUntil = Date.now() + 10000;
      log('session-established', {
        remoteAddress: validation.remoteAddress,
        tokenHash: sha256(token).slice(0, 12),
      });
    }
    setSessionCookie(res);
    if (url.searchParams.has('token')) {
      url.searchParams.delete('token');
      res.statusCode = 302;
      res.setHeader('Location', url.pathname + (url.searchParams.toString() ? `?${url.searchParams}` : ''));
      res.end();
      return;
    }
  }

  proxyHttp(req, res);
});

server.on('connection', (socket) => {
  sockets.add(socket);
  socket.on('close', () => sockets.delete(socket));
});

server.on('upgrade', (req, socket) => {
  if (Date.now() > expiresAt) {
    socket.destroy();
    return;
  }

  const validation = validateRequest(req);
  if (!validation.ok) {
    socket.destroy();
    return;
  }

  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const cookies = parseCookies(req);
  const hasSession = cookies[writableCookie] === sessionSecret;
  const presentedToken = url.searchParams.get('token');

  if (!hasSession) {
    const tokenValid = presentedToken === token;
    const inBootstrapWindow = sessionEstablished && Date.now() <= bootstrapUntil;
    if (!tokenValid && !inBootstrapWindow) {
      log(sessionEstablished ? 'reject-ws-expired-sessionless' : 'reject-ws-no-auth', {
        remoteAddress: validation.remoteAddress,
      });
      socket.destroy();
      return;
    }
    if (tokenValid && !sessionEstablished) {
      sessionEstablished = true;
      bootstrapUntil = Date.now() + 10000;
      log('session-established-ws', {
        remoteAddress: validation.remoteAddress,
        tokenHash: sha256(token).slice(0, 12),
      });
    }
  }

  const upstream = net.connect(upstreamPort, upstreamHost, () => {
    const headers = {
      ...req.headers,
      host: `${upstreamHost}:${upstreamPort}`,
    };
    delete headers.origin;
    upstream.write(
      `${req.method} ${req.url} HTTP/${req.httpVersion}\r\n` +
      Object.entries(headers).map(([k, v]) => `${k}: ${v}`).join('\r\n') +
      '\r\n\r\n'
    );
    socket.pipe(upstream).pipe(socket);
  });

  upstream.on('error', () => {
    log('upstream-ws-error', { remoteAddress: validation.remoteAddress });
    socket.destroy();
  });
});

server.on('error', (err) => {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
});

process.on('uncaughtException', (err) => {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
});

process.on('unhandledRejection', (err) => {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
});

const ttlTimer = setTimeout(shutdown, Math.max(0, ttlMs));
ttlTimer.unref();
process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

server.listen(listenPort, listenHost, () => {
  const addr = server.address();
  console.log(JSON.stringify({
    ready: true,
    host: addr.address,
    port: addr.port,
    expiresAt,
    expectedHost: expectedHost || null,
    expectedOrigin: expectedOrigin || null,
    cookieSecure: secureCookie,
    clientIpRestricted: allowedClientIp || null,
  }));
  log('ready', {
    host: addr.address,
    port: addr.port,
    expiresAt: new Date(expiresAt).toISOString(),
    expectedHost: expectedHost || null,
    expectedOrigin: expectedOrigin || null,
    cookieSecure: secureCookie,
    clientIpRestricted: allowedClientIp || null,
  });
});
