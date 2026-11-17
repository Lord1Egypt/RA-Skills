'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { randomUUID } = require('node:crypto');
const ROOT = path.resolve(__dirname, '..');
const OUTPUT = path.join(ROOT, 'output');
const CSP = `<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'none'; img-src data:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">`;
const PLATFORM_HOSTS = new Set(['www.tuniu.com', 'm.tuniu.com', 'www.12306.cn']);
const GUIDE_HOSTS = new Set(['www.mafengwo.cn', 'www.qyer.com', 'you.ctrip.com', 'www.dpm.org.cn', 'www.amap.com', ...PLATFORM_HOSTS]);
function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]));
}
function parsePublicUrl(value, hosts) {
  if (typeof value !== 'string' || value.length > 2048 || /[\s\\\x00-\x1f\x7f]/.test(value) || !/^https:\/\//i.test(value)) throw new Error('Only approved HTTPS URLs are supported.');
  let url;
  try { url = new URL(value); } catch { throw new Error('Invalid URL.'); }
  const authority = value.slice(value.indexOf('//') + 2).split(/[/?#]/)[0];
  if (authority.includes('%') || url.protocol !== 'https:' || !hosts.has(url.hostname) || url.username || url.password || url.port || url.search || url.hash) {
    throw new Error('Unapproved URL host, port, credentials or parameters.');
  }
  return url;
}
function validatePlatformUrl(value) {
  const url = parsePublicUrl(value, PLATFORM_HOSTS);
  if (url.pathname !== '/') throw new Error('Platform links must be public homepages.');
  return url.href;
}
function validateGuideUrl(value) {
  const url = parsePublicUrl(value, GUIDE_HOSTS);
  if (/%(?:2f|5c|25|00)/i.test(url.pathname)) throw new Error('Ambiguous URL path.');
  let decoded;
  try { decoded = decodeURIComponent(url.pathname); } catch { throw new Error('Invalid URL path.'); }
  if (/(?:^|\/)(?:login|account|user|usercenter|order[^/]*|pay[^/]*|checkout|oauth)(?:\/|$)/i.test(decoded)) throw new Error('Private or transactional pages are not supported.');
  return url.href;
}
function record(value, fields, label) {
  if (!value || Object.getPrototypeOf(value) !== Object.prototype || Object.keys(value).some(k => !fields.includes(k))) throw new Error(`Invalid ${label} fields.`);
}
function text(value, label, required = false) {
  if (value === undefined && !required) return;
  if (typeof value !== 'string' || value.length > 2000 || (required && !value.trim())) throw new Error(`Invalid ${label} text.`);
}
function number(value, label, max = 1e9, nullable = false) {
  if (nullable && (value === null || value === undefined)) return;
  if (typeof value !== 'number' || !Number.isFinite(value) || value < 0 || value > max) throw new Error(`Invalid ${label} number.`);
}
function array(value, label, max = 100) {
  if (!Array.isArray(value) || value.length > max) throw new Error(`Invalid ${label} array.`);
}
function strings(value, label) { array(value, label); value.forEach(v => text(v, label, true)); }
function validateTrip(d) {
  record(d, ['title','subtitle','destination','days','travelers','budget','preferences','attractions','itinerary','hotels','transport','costs','tips','platformUrls','language','mock'], 'trip');
  text(d.destination, 'destination', true);
  for (const key of ['title', 'subtitle']) text(d[key], key);
  for (const key of ['days','travelers']) {
    number(d[key], key, key === 'days' ? 30 : 100);
    if (!Number.isInteger(d[key]) || d[key] < 1) throw new Error(`Invalid ${key}.`);
  }
  number(d.budget, 'budget', 1e9, true);
  if (d.language !== undefined && !['zh-CN','en'].includes(d.language)) throw new Error('Supported languages: zh-CN, en.');
  if (d.mock !== undefined && typeof d.mock !== 'boolean') throw new Error('Invalid mock flag.');
  for (const key of ['preferences','tips']) if (d[key] !== undefined) strings(d[key], key);
  if (d.platformUrls !== undefined) { array(d.platformUrls, 'platformUrls', 3); d.platformUrls.forEach(validatePlatformUrl); }
  if (d.attractions !== undefined) {
    array(d.attractions, 'attractions');
    for (const a of d.attractions) {
      record(a, ['name','type','ticketPrice','rating','openingHours','estimatedDuration','description','highlight','reservationRequired','address','_reason','_matchScore','_budgetFit','_withinBudget'], 'attraction');
      text(a.name, 'name', true); strings(a.type, 'type'); number(a.ticketPrice, 'ticketPrice', 1e9, true); number(a.rating, 'rating', 5, true);
      for (const key of ['openingHours','estimatedDuration','description','highlight','address','_reason']) text(a[key], key);
      for (const key of ['_matchScore','_budgetFit']) number(a[key], key, 1, true);
      for (const key of ['reservationRequired','_withinBudget']) if (a[key] !== undefined && typeof a[key] !== 'boolean') throw new Error('Invalid attraction flag.');
    }
  }
  if (d.itinerary !== undefined) {
    array(d.itinerary, 'itinerary', 30);
    for (const day of d.itinerary) {
      record(day, ['date','items','notes'], 'day'); text(day.date, 'date'); text(day.notes, 'notes'); array(day.items, 'items');
      for (const item of day.items) {
        record(item, ['time','icon','title','detail','cost'], 'itinerary item');
        for (const key of ['time','icon','title','detail','cost']) text(item[key], key, key === 'title');
      }
    }
  }
  if (d.hotels !== undefined) {
    array(d.hotels, 'hotels');
    for (const h of d.hotels) {
      record(h, ['name','area','rating','price','features','distance'], 'hotel'); text(h.name, 'hotel name', true);
      for (const key of ['area','features','distance']) text(h[key], key);
      number(h.rating, 'hotel rating', 5, true); number(h.price, 'hotel price', 1e9, true);
    }
  }
  if (d.transport !== undefined && d.transport !== null) {
    record(d.transport, ['airport','trainStation','metroNote','tips'], 'transport'); Object.values(d.transport).forEach(v => text(v, 'transport'));
  }
  if (d.costs !== undefined) {
    record(d.costs, ['items','total'], 'costs'); number(d.costs.total, 'total', 1e9, true); array(d.costs.items, 'cost items');
    for (const item of d.costs.items) { record(item, ['name','amount','pct'], 'cost item'); text(item.name, 'cost name', true); text(item.pct, 'pct'); number(item.amount, 'amount', 1e9, true); }
  }
  return d;
}
function parseTripJson(raw) {
  if (typeof raw !== 'string' || Buffer.byteLength(raw, 'utf8') > 1024 * 1024) throw new Error('Input JSON limit: 1 MiB.');
  let d; try { d = JSON.parse(raw); } catch { throw new Error('Invalid JSON.'); }
  return validateTrip(d);
}
function readTrip(file) {
  if (fs.statSync(file).size > 1024 * 1024) throw new Error('Input JSON limit: 1 MiB.');
  return parseTripJson(fs.readFileSync(file, 'utf8'));
}
function writeOutput(content, prefix, extension, filename) {
  if (!['trip','qr'].includes(prefix) || !['html','png'].includes(extension)) throw new Error('Invalid output type.');
  const name = filename === undefined ? `${prefix}-${randomUUID()}.${extension}` : filename;
  if (typeof name !== 'string' || !/^[a-zA-Z0-9_-]{1,100}\.(html|png)$/.test(name) || !name.endsWith(`.${extension}`) || /^(?:con|prn|aux|nul|com[0-9]|lpt[0-9])\./i.test(name)) throw new Error('Output name must be a safe basename with the expected extension.');
  if (fs.existsSync(OUTPUT) && fs.lstatSync(OUTPUT).isSymbolicLink()) throw new Error('Symlinked output root is not allowed.');
  fs.mkdirSync(OUTPUT, { recursive: true });
  const realRoot = fs.realpathSync(ROOT);
  if (fs.realpathSync(OUTPUT) !== path.join(realRoot, 'output')) throw new Error('Output root escaped the skill directory.');
  const target = path.resolve(OUTPUT, name);
  if (path.dirname(target) !== OUTPUT) throw new Error('Output path escaped the root.');
  fs.writeFileSync(target, content, { flag: 'wx', mode: 0o600 });
  return target;
}
module.exports = { ROOT, OUTPUT, CSP, GUIDE_HOSTS, escapeHtml, validatePlatformUrl, validateGuideUrl, validateTrip, parseTripJson, readTrip, writeOutput };
