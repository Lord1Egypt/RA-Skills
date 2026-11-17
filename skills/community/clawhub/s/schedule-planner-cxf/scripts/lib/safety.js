'use strict';
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { randomUUID } = require('node:crypto');
const ROOT = path.resolve(__dirname, '../..');
const CSP = `<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">`;
function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
function validatePlatformUrl(value) {
  if (typeof value !== 'string' || value.length > 200 || /[\s\\\x00-\x1f]/.test(value)) throw new Error('Invalid platform URL.');
  let url;
  try { url = new URL(value); } catch { throw new Error('Invalid platform URL.'); }
  // Only public home pages: no order IDs, redirect parameters, payment pages or embedded credentials.
  if (url.protocol !== 'https:' || !['m.tuniu.com', 'www.tuniu.com', 'www.12306.cn'].includes(url.hostname) ||
      url.username || url.password || url.port || url.pathname !== '/' || url.search || url.hash) {
    throw new Error('Only approved HTTPS platform home pages are supported.');
  }
  return url.href;
}
function object(value, fields, label) {
  if (!value || Object.getPrototypeOf(value) !== Object.prototype || Object.keys(value).some(k => !fields.includes(k))) {
    throw new Error(`Invalid ${label} object or unsupported field.`);
  }
}
function text(value, label, required = false) {
  if (value === undefined && !required) return;
  if (typeof value !== 'string' || value.length > 2000 || (required && !value.trim())) throw new Error(`Invalid ${label} text.`);
}
function array(value, label, max = 100) {
  if (!Array.isArray(value) || value.length > max) throw new Error(`Invalid ${label} array.`);
}
function number(value, label) {
  if (typeof value !== 'number' || !Number.isFinite(value) || value < 0 || value > 1e9) throw new Error(`Invalid ${label} number.`);
}
function validateTrip(data) {
  object(data, ['tripType', 'destination', 'duration', 'segments', 'dailyPlan', 'costs', 'tips', 'platformUrl', 'mock', 'language'], 'trip');
  for (const key of ['tripType', 'destination', 'duration']) text(data[key], key, true);
  if (data.language !== undefined && !['zh-CN', 'en'].includes(data.language)) throw new Error('Unsupported page language.');
  if (data.mock !== undefined && typeof data.mock !== 'boolean') throw new Error('Invalid mock flag.');
  array(data.segments, 'segments');
  const fields = ['type', 'segmentNo', 'trainNo', 'flightNo', 'departure', 'arrival', 'date', 'price', 'seat', 'duration', 'name', 'address', 'roomType', 'checkIn', 'checkOut', 'nights'];
  for (const segment of data.segments) {
    object(segment, fields, 'segment');
    if (!['train', 'flight', 'hotel'].includes(segment.type)) throw new Error('Unsupported segment type.');
    for (const [key, value] of Object.entries(segment)) {
      if (['price', 'nights'].includes(key)) number(value, key); else text(value, key);
    }
    for (const key of segment.type === 'hotel' ? ['name'] : ['departure', 'arrival']) text(segment[key], key, true);
  }
  if (data.dailyPlan !== undefined) {
    array(data.dailyPlan, 'dailyPlan');
    for (const day of data.dailyPlan) {
      object(day, ['day', 'title', 'items'], 'day');
      text(day.day, 'day', true); text(day.title, 'title', true); array(day.items, 'items');
      day.items.forEach(item => text(item, 'item', true));
    }
  }
  object(data.costs, ['total', 'train', 'train1', 'train2', 'flight', 'flightOutbound', 'flightReturn', 'hotel', 'ticket', 'other'], 'costs');
  number(data.costs.total, 'total');
  Object.values(data.costs).forEach(value => number(value, 'cost'));
  if (data.tips !== undefined) { array(data.tips, 'tips'); data.tips.forEach(tip => text(tip, 'tip', true)); }
  if (data.platformUrl !== undefined) validatePlatformUrl(data.platformUrl);
  return data;
}
function readJson(file) {
  if (fs.statSync(file).size > 1024 * 1024) throw new Error('Input JSON exceeds 1 MiB.');
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch { throw new Error('Input must be readable UTF-8 JSON.'); }
}
function outputDirectory(desktop = false) {
  const dir = desktop ? path.join(os.homedir(), 'Desktop') : path.join(ROOT, 'output');
  if (desktop) console.warn('Writing itinerary files to Desktop (--desktop).');
  if (fs.existsSync(dir) && fs.lstatSync(dir).isSymbolicLink()) throw new Error('Output directory must not be a symlink.');
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}
function writeOutput(content, prefix = 'trip', extension = 'html', desktop = false) {
  if (!/^[a-z0-9-]+$/.test(prefix) || !['html', 'json'].includes(extension)) throw new Error('Invalid output filename.');
  const file = path.join(outputDirectory(desktop), `${prefix}-${randomUUID()}.${extension}`);
  fs.writeFileSync(file, content, { encoding: 'utf8', flag: 'wx', mode: 0o600 });
  return file;
}
module.exports = { ROOT, CSP, escapeHtml, validatePlatformUrl, validateTrip, readJson, writeOutput, object, text, array, number };
