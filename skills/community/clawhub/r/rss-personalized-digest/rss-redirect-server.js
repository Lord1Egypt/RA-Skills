#!/usr/bin/env node
const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');

const PORT = 7890;
const LOG_FILE = '/tmp/rss-clicks.log';
const TUNNEL_URL = 'https://7a2805742f5e03bb-123-234-101-41.serveousercontent.com';
const PID_FILE = '/tmp/serveo_tunnel.pid';
const LOG_TUNNEL = '/tmp/serveo_tunnel.log';

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  if (pathname.startsWith('/go/')) {
    const encoded = pathname.slice(4);
    let originalUrl = '(decode error)';
    try {
      const base64 = encoded.replace(/-/g, '+').replace(/_/g, '/');
      const padded = base64 + '='.repeat((4 - base64.length % 4) % 4);
      originalUrl = Buffer.from(padded, 'base64').toString('utf-8');
    } catch (e) { /* ignore */ }

    const ts = new Date().toISOString().replace('T', ' ').substring(0, 19);
    fs.appendFileSync(LOG_FILE, `[${ts}] FROM:${req.socket.remoteAddress} -> ${originalUrl}\n`);

    res.writeHead(302, {
      'Location': originalUrl,
      'Cache-Control': 'no-store, no-cache, must-revalidate',
      'Pragma': 'no-cache'
    });
    res.end();
    return;
  }

  if (pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('OK\nTunnel: ' + TUNNEL_URL);
    return;
  }

  if (pathname === '/clicks') {
    res.writeHead(200, { 'Content-Type': 'text/plain', 'Access-Control-Allow-Origin': '*' });
    try { res.end(fs.readFileSync(LOG_FILE, 'utf8')); } catch (e) { res.end(''); }
    return;
  }

  if (pathname === '/clear') {
    fs.writeFileSync(LOG_FILE, '');
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Cleared');
    return;
  }

  if (pathname === '/newclicks') {
    // 返回新增的点击（上次查询后新增的）
    const since = parsedUrl.query.since || '0';
    const sinceTime = new Date(parseInt(since));
    try {
      const data = fs.readFileSync(LOG_FILE, 'utf8');
      const lines = data.trim().split('\n').filter(l => {
        const ts = l.match(/^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]/);
        return ts && new Date(ts[1]) > sinceTime;
      });
      res.end(lines.join('\n'));
    } catch (e) { res.end(''); }
    return;
  }

  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('RSS Click Logger\nTunnel: ' + TUNNEL_URL + '/go/<base64url>\n');
});

// 启动隧道
function startTunnel() {
  const tunnel = require('child_process').spawn('ssh', [
    '-o', 'StrictHostKeyChecking=no',
    '-o', 'ServerAliveInterval=30',
    '-R', '80:localhost:' + PORT,
    'serveo.net'
  ], { stdio: 'pipe' });

  tunnel.stdout.on('data', (d) => {
    const out = d.toString();
    fs.appendFileSync(LOG_TUNNEL, out);
    process.stdout.write(out);
    // 提取 URL
    const m = out.match(/Forwarding HTTP traffic from (https:\/\/[^\s]+)/);
    if (m) {
      fs.writeFileSync('/tmp/tunnel_url.txt', m[1]);
    }
  });
  tunnel.stderr.on('data', (d) => fs.appendFileSync(LOG_TUNNEL, d.toString()));

  tunnel.on('exit', (code) => {
    console.log(`Tunnel exited with code ${code}, restarting in 5s...`);
    setTimeout(startTunnel, 5000);
  });

  fs.writeFileSync(PID_FILE, tunnel.pid.toString());
  return tunnel;
}

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Server on port ${PORT}`);
  startTunnel();
});
