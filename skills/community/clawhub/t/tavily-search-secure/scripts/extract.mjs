#!/usr/bin/env node

import net from 'node:net';

function usage() {
  console.error('Usage: extract.mjs "url1" ["url2" ...] [--timeout 25000]');
  process.exit(2);
}

function fail(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}

function cleanText(input, maxLen = 12000) {
  return String(input ?? '')
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, maxLen);
}

function isPrivateIPv4(ip) {
  const parts = ip.split('.').map((x) => Number.parseInt(x, 10));
  if (parts.length !== 4 || parts.some((n) => !Number.isFinite(n) || n < 0 || n > 255)) return false;
  const [a, b] = parts;
  if (a === 10) return true;
  if (a === 127) return true;
  if (a === 169 && b === 254) return true;
  if (a === 172 && b >= 16 && b <= 31) return true;
  if (a === 192 && b === 168) return true;
  if (a === 0) return true;
  return false;
}

function isBlockedHost(hostnameRaw) {
  const hostname = String(hostnameRaw ?? '').toLowerCase().trim();
  if (!hostname) return true;

  if (
    hostname === 'localhost' ||
    hostname.endsWith('.local') ||
    hostname.endsWith('.internal') ||
    hostname.endsWith('.localhost')
  ) {
    return true;
  }

  const ipType = net.isIP(hostname);
  if (ipType === 4) return isPrivateIPv4(hostname);
  if (ipType === 6) {
    const h = hostname;
    if (h === '::1' || h.startsWith('fc') || h.startsWith('fd') || h.startsWith('fe80')) return true;
  }

  return false;
}

function validateUrl(raw) {
  let u;
  try {
    u = new URL(raw);
  } catch {
    throw new Error(`Geçersiz URL: ${raw}`);
  }

  if (!['http:', 'https:'].includes(u.protocol)) {
    throw new Error(`Sadece http/https izinli: ${raw}`);
  }

  if (u.username || u.password) {
    throw new Error(`URL kullanıcı bilgisi içeremez: ${raw}`);
  }

  if (isBlockedHost(u.hostname)) {
    throw new Error(`Güvenlik nedeniyle engellenen host: ${u.hostname}`);
  }

  return u.toString();
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes('-h') || args.includes('--help')) usage();

let timeoutMs = 25000;
const rawUrls = [];

for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '--timeout') {
    timeoutMs = Number.parseInt(args[i + 1] ?? '25000', 10);
    i++;
    continue;
  }
  if (!a.startsWith('-')) rawUrls.push(a);
}

if (rawUrls.length === 0) fail('No URLs provided', 2);
if (rawUrls.length > 5) fail('Tek istekte en fazla 5 URL desteklenir.');

timeoutMs = Math.max(3000, Math.min(Number.isFinite(timeoutMs) ? timeoutMs : 25000, 60000));

const urls = rawUrls.map(validateUrl);

const apiKey = String(process.env.TAVILY_API_KEY ?? '').trim();
if (!apiKey) fail('Missing TAVILY_API_KEY');

const controller = new AbortController();
const timer = setTimeout(() => controller.abort(), timeoutMs);

let resp;
try {
  resp = await fetch('https://api.tavily.com/extract', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      api_key: apiKey,
      urls,
    }),
    signal: controller.signal,
  });
} catch (err) {
  clearTimeout(timer);
  fail(`Tavily isteği başarısız: ${err?.name === 'AbortError' ? 'zaman aşımı' : 'ağ hatası'}`);
}
clearTimeout(timer);

if (!resp.ok) {
  const text = await resp.text().catch(() => '');
  fail(`Tavily Extract failed (${resp.status}): ${cleanText(text, 240)}`);
}

const data = await resp.json();
const results = Array.isArray(data?.results) ? data.results : [];
const failed = Array.isArray(data?.failed_results) ? data.failed_results : [];

for (const r of results) {
  const url = cleanText(r?.url, 1200);
  const content = cleanText(r?.raw_content, 12000);
  if (!url) continue;

  console.log(`# ${url}\n`);
  console.log(content || '(no content extracted)');
  console.log('\n---\n');
}

if (failed.length > 0) {
  console.log('## Failed URLs\n');
  for (const f of failed) {
    const furl = cleanText(f?.url, 1200);
    const ferr = cleanText(f?.error, 240);
    console.log(`- ${furl}: ${ferr || 'unknown error'}`);
  }
}
