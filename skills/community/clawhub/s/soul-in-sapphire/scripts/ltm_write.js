#!/usr/bin/env node
import { requireIds, httpJson } from './notionctl_bridge.js';

const propTitle = s => ({ title: [{ type: 'text', text: { content: String(s) } }] });
const propRich = s => ({ rich_text: [{ type: 'text', text: { content: String(s || '') } }] });
const propSelect = n => ({ select: n ? { name: String(n) } : null });
const propMulti = a => ({ multi_select: (a || []).filter(Boolean).map(n => ({ name: String(n) })) });
const propUrl = u => ({ url: u ? String(u) : null });

async function readStdinJson() {
  const chunks = [];
  for await (const c of process.stdin) chunks.push(c);
  const raw = Buffer.concat(chunks).toString('utf-8').trim();
  if (!raw) throw new Error('Expected JSON on stdin');
  return JSON.parse(raw);
}

function parseArgs(argv) {
  const out = { memDsid: null, memDbid: null };
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === '--mem-dsid') out.memDsid = argv[++i] || '';
    else if (argv[i] === '--mem-dbid') out.memDbid = argv[++i] || '';
  }
  return out;
}

async function main() {
  const args = parseArgs(process.argv);
  const cfg = { data_source_id: args.memDsid, database_id: args.memDbid };
  requireIds(cfg);
  const obj = await readStdinJson();
  const title = String(obj.title || '').trim();
  if (!title) throw new Error('Missing title');

  const props = {
    Name: propTitle(title),
    Type: propSelect(String(obj.type || '').trim() || null),
    Tags: propMulti(obj.tags || []),
    Content: propRich(String(obj.content || '').trim()),
  };
  if (obj.source) props.Source = propUrl(obj.source);
  if (obj.confidence) props.Confidence = propSelect(String(obj.confidence || '').trim() || null);

  const page = httpJson('POST', '/pages', { parent: { database_id: cfg.database_id }, properties: props });
  console.log(JSON.stringify({ ok: true, id: page.id, url: page.url }, null, 2));
}

main().catch(e => { console.error(String(e?.stack || e)); process.exit(1); });
