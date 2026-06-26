#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

/**
 * Record an unresolved inner tension without forcing it into an identity edit.
 * Use this when the self-model feels split, unstable, or not yet ready for a
 * durable conclusion.
 */
function parseArgs(argv) {
  const out = { write: '', append: '' };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--write') out.write = argv[++i] || '';
    else if (a === '--append') out.append = argv[++i] || '';
  }
  return out;
}

function readPayload() {
  const raw = fs.readFileSync(0, 'utf-8').trim();
  if (!raw) throw new Error('Expected JSON on stdin');
  const obj = JSON.parse(raw);
  if (!obj.tension) throw new Error('Missing tension');
  return {
    when: obj.when || new Date().toISOString(),
    tension: String(obj.tension),
    side_a: String(obj.side_a || ''),
    side_b: String(obj.side_b || ''),
    evidence: Array.isArray(obj.evidence) ? obj.evidence.map(String) : [],
    current_pull: String(obj.current_pull || ''),
    note: String(obj.note || ''),
    next_signal: String(obj.next_signal || ''),
  };
}

function buildCandidateActions(record) {
  const actions = [
    {
      kind: 'journal_write',
      why: 'Conflicts often become clearer after narrative synthesis.',
      confidence: 0.66,
      when: 'Use when this tension shaped the tone of the day or session.',
      risk: 'low',
    }
  ];
  if (record.evidence.length >= 2 || record.next_signal) {
    actions.push({
      kind: 'continuity_check',
      why: 'The conflict has enough repeated evidence to compare against recent state patterns.',
      confidence: 0.74,
      when: 'Use when the same tension keeps returning.',
      risk: 'low',
    });
  }
  return actions;
}

function main() {
  const args = parseArgs(process.argv);
  const record = readPayload();
  const out = {
    ok: true,
    function_name: 'conflict_track',
    description: 'Capture unresolved inner tensions without prematurely collapsing them into identity changes.',
    record,
    candidate_actions: buildCandidateActions(record),
  };
  if (args.write) {
    fs.mkdirSync(path.dirname(args.write), { recursive: true });
    fs.writeFileSync(args.write, JSON.stringify(record, null, 2) + '\n', 'utf-8');
  }
  if (args.append) {
    fs.mkdirSync(path.dirname(args.append), { recursive: true });
    fs.appendFileSync(args.append, JSON.stringify(record) + '\n', 'utf-8');
  }
  console.log(JSON.stringify(out, null, 2));
}

try { main(); } catch (e) { console.error(String(e?.stack || e)); process.exit(1); }
