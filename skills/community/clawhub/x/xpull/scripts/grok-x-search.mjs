#!/usr/bin/env node
/**
 * grok-x-search.mjs — X search via xAI Grok Responses API.
 *
 * Usage:
 *   grok-x-search.mjs thread <url>
 *   grok-x-search.mjs replies <url>
 *   grok-x-search.mjs search <query> [--from handle]
 *
 * Requires XAI_API_KEY in env or .env in current directory.
 * Daily cap: 20 calls (override: GROK_DAILY_CAP).
 */
import https from 'https';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const MODEL = 'grok-4-1-fast-non-reasoning';
const __dirname = dirname(fileURLToPath(import.meta.url));
const STATE = resolve(__dirname, '..', '.grok-state.json');

function getKey() {
  if (process.env.XAI_API_KEY) return process.env.XAI_API_KEY;
  const f = resolve(process.cwd(), '.env');
  if (existsSync(f)) { const m = readFileSync(f, 'utf8').match(/^XAI_API_KEY=(.+)$/m); if (m) return m[1].trim(); }
  return null;
}

function checkBudget() {
  const cap = parseInt(process.env.GROK_DAILY_CAP || '20', 10);
  const today = new Date().toISOString().slice(0, 10);
  let state = { date: today, calls: 0 };
  try { state = JSON.parse(readFileSync(STATE, 'utf8')); if (state.date !== today) state = { date: today, calls: 0 }; } catch {}
  if (state.calls >= cap) throw new Error(`Daily cap reached (${cap}). Resets tomorrow.`);
  state.calls++;
  writeFileSync(STATE, JSON.stringify(state));
}

function post(apiKey, prompt, toolParams = {}) {
  const body = JSON.stringify({
    model: MODEL,
    input: [{ role: 'user', content: prompt }],
    tools: [{ type: 'x_search', ...toolParams }],
  });
  return new Promise((resolve, reject) => {
    const req = https.request('https://api.x.ai/v1/responses', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` },
    }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => res.statusCode === 200 ? resolve(JSON.parse(d)) : reject(new Error(`${res.statusCode}: ${d.slice(0, 200)}`)));
    });
    req.on('error', reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('timeout')); });
    req.write(body); req.end();
  });
}

const PROMPTS = {
  thread: url => `Retrieve the complete thread for this post. OP tweets only, chronological order, full text + media URLs + timestamps. URL: ${url}`,
  replies: url => `Find the top replies to this post sorted by engagement. Include: author, text, likes, retweets. URL: ${url}`,
  search: q => `Search X for: ${q}. Return relevant recent posts with author, text, timestamp, engagement, URL.`,
};

const [cmd, target, ...rest] = process.argv.slice(2);
if (!cmd || !target || !PROMPTS[cmd]) { console.error('Usage: grok-x-search.mjs <thread|replies|search> <url-or-query> [--from handle]'); process.exit(1); }
const key = getKey();
if (!key) { console.error('XAI_API_KEY not set. Export it or place it in a .env file in the current directory. Get one at https://console.x.ai'); process.exit(1); }

try {
  checkBudget();
  const fromIdx = rest.indexOf('--from');
  const toolParams = fromIdx !== -1 && rest[fromIdx + 1] ? { allowed_x_handles: [rest[fromIdx + 1].replace('@', '')] } : {};
  const resp = await post(key, PROMPTS[cmd](target), toolParams);
  console.log(JSON.stringify(resp, null, 2));
} catch (e) { console.error(`Error: ${e.message}`); process.exit(1); }

