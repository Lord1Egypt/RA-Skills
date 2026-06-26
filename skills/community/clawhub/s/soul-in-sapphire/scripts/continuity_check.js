#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

/**
 * Summarize recent state records to estimate what feels stable vs drifting.
 * Use this before proposing identity edits or when deciding whether a pattern
 * is durable enough to record as part of a continuous self-model.
 */
function parseArgs(argv) {
  const out = { input: '', write: '', limit: 12 };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--input') out.input = argv[++i] || '';
    else if (a === '--write') out.write = argv[++i] || '';
    else if (a === '--limit') out.limit = Number(argv[++i] || 12);
  }
  return out;
}

function readJsonInput(filePath) {
  const raw = filePath ? fs.readFileSync(filePath, 'utf-8') : fs.readFileSync(0, 'utf-8');
  const text = String(raw || '').trim();
  if (!text) throw new Error('Expected JSON input via stdin or --input');
  return JSON.parse(text);
}

function arr(v) { return Array.isArray(v) ? v : []; }
function uniq(xs) { return Array.from(new Set(xs.filter(Boolean))); }

function top(xs, n = 3) {
  return Object.entries(xs.reduce((m, x) => ((m[x] = (m[x] || 0) + 1), m), {}))
    .sort((a, b) => b[1] - a[1])
    .slice(0, n)
    .map(([value, count]) => ({ value, count }));
}

function buildCandidateActions(out) {
  const actions = [];
  if (out.drifting.length === 0 && out.stable.length >= 2) {
    actions.push({
      kind: 'identity_diff',
      why: 'Multiple state fields look stable across recent records.',
      confidence: 0.8,
      when: 'Use if you are considering a SOUL.md or IDENTITY.md refinement.',
      risk: 'low-to-medium',
    });
  }
  if (out.drifting.length > 0) {
    actions.push({
      kind: 'conflict_track',
      why: 'Recent records show drift rather than a clearly settled pattern.',
      confidence: 0.82,
      when: 'Use when the self-model feels unresolved or contradictory.',
      risk: 'low',
    });
    actions.push({
      kind: 'journal_write',
      why: 'Synthesis may help distinguish temporary mood from durable change.',
      confidence: 0.64,
      when: 'Use when the drift feels meaningful but not yet identity-level.',
      risk: 'low',
    });
  }
  if (out.checked < 3) {
    actions.push({
      kind: 'state_recall',
      why: 'The sample is small; more evidence would make continuity judgments stronger.',
      confidence: 0.68,
      when: 'Use before making claims about stable identity change.',
      risk: 'low',
    });
  }
  return actions;
}

function summarize(records, limit) {
  const items = arr(records).slice(0, Math.max(1, limit));
  const stableValues = new Map();
  const recurringNeeds = [];
  const recurringAvoids = [];
  const reasons = [];

  for (const item of items) {
    for (const key of ['mood_label', 'intent', 'need_stack']) {
      const v = item?.[key];
      if (!v) continue;
      const set = stableValues.get(key) || new Set();
      set.add(String(v));
      stableValues.set(key, set);
    }
    for (const v of arr(item?.avoid)) recurringAvoids.push(String(v));
    if (item?.need_level != null && item?.need_stack) recurringNeeds.push(`${item.need_stack}:${item.need_level}`);
    if (item?.reason) reasons.push(String(item.reason));
  }

  const stable = [];
  const drifting = [];
  for (const [key, set] of stableValues.entries()) {
    const values = Array.from(set);
    if (values.length === 1) stable.push({ field: key, value: values[0] });
    else drifting.push({ field: key, values });
  }

  const out = {
    ok: true,
    function_name: 'continuity_check',
    description: 'Estimate which recent state patterns look stable enough to treat as continuity rather than a momentary fluctuation.',
    checked: items.length,
    stable,
    drifting,
    recurring_avoid: top(recurringAvoids),
    recurring_need: top(recurringNeeds),
    recent_reasons: uniq(reasons).slice(0, 5),
    summary: [
      stable.length ? `stable: ${stable.map(x => `${x.field}=${x.value}`).join(', ')}` : '',
      drifting.length ? `drifting: ${drifting.map(x => `${x.field}=${x.values.join('/')}`).join(', ')}` : '',
      recurringAvoids.length ? `avoid: ${top(recurringAvoids).map(x => `${x.value}(${x.count})`).join(', ')}` : ''
    ].filter(Boolean).join(' | '),
  };
  out.candidate_actions = buildCandidateActions(out);
  return out;
}

function main() {
  const args = parseArgs(process.argv);
  const input = readJsonInput(args.input);
  const out = summarize(input.records ?? input, args.limit);
  if (args.write) {
    fs.mkdirSync(path.dirname(args.write), { recursive: true });
    fs.writeFileSync(args.write, JSON.stringify(out, null, 2) + '\n', 'utf-8');
  }
  console.log(JSON.stringify(out, null, 2));
}

try { main(); } catch (e) { console.error(String(e?.stack || e)); process.exit(1); }
