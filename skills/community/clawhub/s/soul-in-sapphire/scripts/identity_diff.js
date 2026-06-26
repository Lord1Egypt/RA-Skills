#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

/**
 * Compare current self-description text against a proposed revision.
 * Use this before changing SOUL.md, IDENTITY.md, HEARTBEAT.md, or other
 * self-descriptive files so the change stays explicit and reviewable.
 */
function parseArgs(argv) {
  const out = { current: '', proposed: '', write: '' };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--current') out.current = argv[++i] || '';
    else if (a === '--proposed') out.proposed = argv[++i] || '';
    else if (a === '--write') out.write = argv[++i] || '';
  }
  return out;
}

function readMaybeJsonOrText(p) {
  const raw = fs.readFileSync(p, 'utf-8');
  try { return JSON.parse(raw); } catch { return raw; }
}

function linesOf(v) {
  if (Array.isArray(v)) return v.map(x => String(x));
  if (v && typeof v === 'object') return Object.entries(v).map(([k, val]) => `${k}: ${JSON.stringify(val)}`);
  return String(v || '').split(/\r?\n/).map(x => x.trim()).filter(Boolean);
}

function buildCandidateActions(out) {
  const actions = [];
  if (out.added.length + out.removed.length === 0) {
    actions.push({
      kind: 'ltm_write',
      why: 'No identity diff was detected; preserve the conclusion as memory if the review itself mattered.',
      confidence: 0.44,
      when: 'Use only if the comparison result is worth remembering.',
      risk: 'low',
    });
  } else {
    actions.push({
      kind: 'review_proposed_edit',
      why: 'There is a real self-description change to inspect before applying it.',
      confidence: 0.91,
      when: 'Use before editing the live file.',
      risk: 'medium',
    });
  }
  if (out.added.length + out.removed.length > 6) {
    actions.push({
      kind: 'journal_write',
      why: 'The change is broad; a journal synthesis may explain why the identity shift happened.',
      confidence: 0.72,
      when: 'Use when the proposed rewrite feels larger than a small refinement.',
      risk: 'low',
    });
  }
  return actions;
}

function diff(current, proposed) {
  const a = new Set(linesOf(current));
  const b = new Set(linesOf(proposed));
  const out = {
    ok: true,
    function_name: 'identity_diff',
    description: 'Show explicit additions and removals between current and proposed self-description content.',
    added: Array.from(b).filter(x => !a.has(x)),
    removed: Array.from(a).filter(x => !b.has(x)),
    unchanged_count: Array.from(a).filter(x => b.has(x)).length,
  };
  out.summary = `added=${out.added.length}, removed=${out.removed.length}, unchanged=${out.unchanged_count}`;
  out.candidate_actions = buildCandidateActions(out);
  return out;
}

function main() {
  const args = parseArgs(process.argv);
  if (!args.current || !args.proposed) throw new Error('Use --current <path> --proposed <path>');
  const out = diff(readMaybeJsonOrText(args.current), readMaybeJsonOrText(args.proposed));
  if (args.write) {
    fs.mkdirSync(path.dirname(args.write), { recursive: true });
    fs.writeFileSync(args.write, JSON.stringify(out, null, 2) + '\n', 'utf-8');
  }
  console.log(JSON.stringify(out, null, 2));
}

try { main(); } catch (e) { console.error(String(e?.stack || e)); process.exit(1); }
