#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { queryDataSource, textOf } from './notionctl_bridge.js';
import { projectState } from './emotion_math.js';

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
  const out = { limit: 1, write: '', stateDsid: null, current: false, at: nowIsoLocal() };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--limit') out.limit = Number(argv[++i] || 1);
    else if (a === '--write') out.write = argv[++i] || '';
    else if (a === '--state-dsid') out.stateDsid = argv[++i] || '';
    else if (a === '--current') out.current = true;
    else if (a === '--at') out.at = argv[++i] || '';
    else throw new Error('Unknown state recall argument: ' + a);
  }
  return out;
}

async function main() {
  const args = parseArgs(process.argv);
  const dsId = args.stateDsid;
  if (!dsId) throw new Error('Missing --state-dsid. Check the workspace AGENTS.md ## Tools section for the value.');
  if (!Number.isInteger(args.limit) || args.limit < 1 || args.limit > 100) throw new Error('limit must be 1..100');
  const pages = (await queryDataSource(dsId, {page_size: args.limit, sorts:[{property:'when',direction:'descending'}]})).results || [];
  const out = pages.map(normalizeStatePage);
  if (args.current) for (const row of out) {
    row.projected_at = args.at;
    row.projected_state = projectState(row.state_json, row.when, args.at);
    row.temporal_scope = 'projection_now_from_recorded_snapshot';
  }
  if (args.write) {
    fs.mkdirSync(path.dirname(args.write), { recursive: true });
    const payload = out[0] || { retrieved_at: nowIsoLocal(), empty: true };
    fs.writeFileSync(args.write, JSON.stringify(payload, null, 2) + '\n', 'utf-8');
  }
  console.log(JSON.stringify(out, null, 2));
}

main().catch(e => { console.error(String(e?.stack || e)); process.exitCode = 1; });
