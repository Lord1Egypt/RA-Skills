#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { queryRecent, textOf } from './notionctl_bridge.js';

function nowIsoLocal() { return new Date().toISOString(); }
function parseStateJson(s) { try { return s ? JSON.parse(s) : {}; } catch { return { _raw: s }; } }

function normalizeStatePage(page) {
  const p = page?.properties || {};
  return {
    page_id: page?.id,
    retrieved_at: nowIsoLocal(),
    when: textOf(p.when),
    mood_label: textOf(p.mood_label),
    intent: textOf(p.intent),
    need_stack: textOf(p.need_stack),
    need_level: textOf(p.need_level),
    avoid: textOf(p.avoid),
    reason: textOf(p.reason),
    state_json: parseStateJson(textOf(p.state_json)),
  };
}

function parseArgs(argv) {
  const out = { limit: 1, write: '', stateDsid: null };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--limit') out.limit = Number(argv[++i] || 1);
    else if (a === '--write') out.write = argv[++i] || '';
    else if (a === '--state-dsid') out.stateDsid = argv[++i] || '';
  }
  return out;
}

function main() {
  const args = parseArgs(process.argv);
  const dsId = args.stateDsid;
  if (!dsId) throw new Error('Missing --state-dsid. Check TOOLS.md for the value.');
  const pages = queryRecent(dsId, Math.max(1, args.limit));
  const out = pages.map(normalizeStatePage);
  if (args.write) {
    fs.mkdirSync(path.dirname(args.write), { recursive: true });
    const payload = out[0] || { retrieved_at: nowIsoLocal(), empty: true };
    fs.writeFileSync(args.write, JSON.stringify(payload, null, 2) + '\n', 'utf-8');
  }
  console.log(JSON.stringify(out, null, 2));
}

try { main(); } catch (e) { console.error(String(e?.stack || e)); process.exit(1); }
