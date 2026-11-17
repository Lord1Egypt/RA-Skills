#!/usr/bin/env node
// Validator for a /spec spec directory. Deterministic checks only: it answers
// the questions an agent would otherwise re-derive by hand every turn, and gets
// wrong under compaction.
//
//   node <this-skill>/scripts/check-spec.mjs docs/plans/2026-08-22-my-spec
//
// Exit 0 when clean, 1 when there is at least one problem. Warnings alone do not
// fail: an early spec legitimately has no design.md and no receipts yet.
//
// What it checks, and why each one is here rather than in prose:
//   - approval receipts, by recomputing sha256. A prose instruction to "verify
//     the hashes" is the kind of step that silently degrades into a claim.
//   - downstream invalidation. Voiding requirements must void design and tasks,
//     and that cascade is easy to forget by hand.
//   - requirement coverage both ways: criteria nothing implements, and citations
//     pointing at criteria that do not exist (usually a renumber).
//   - a Verify: line per task, and that an `npm run X` (or bare `npm test`)
//     names a real script. Invented commands are the most common way a task
//     fakes verification.
//   - every `SHALL CONTINUE TO` assertion names a test that exists or that some
//     task creates. An unbacked assertion is a wish, and these sit on money and
//     access-control paths.

import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, resolve } from 'node:path';

const GATED = ['requirements.md', 'design.md', 'tasks.md'];
const CLOSURES = ['implemented', 'merged', 'deployed', 'verified'];

const problems = [];
const warnings = [];
const fail = (m) => problems.push(m);
const warn = (m) => warnings.push(m);

const specDir = process.argv[2];
if (!specDir) {
  console.error('usage: check-spec.mjs <spec-dir>');
  process.exit(2);
}
const dir = resolve(specDir);
if (!existsSync(dir)) {
  console.error(`no such spec dir: ${specDir}`);
  process.exit(2);
}

const read = (f) => (existsSync(join(dir, f)) ? readFileSync(join(dir, f), 'utf8') : null);
const sha = (f) =>
  createHash('sha256')
    .update(readFileSync(join(dir, f)))
    .digest('hex');

// ── phase, derived from the files present, never from stored state ───────────
const present = new Set(readdirSync(dir));
const phase = present.has('tasks.md')
  ? 'tasks'
  : present.has('design.md')
    ? 'design'
    : present.has('requirements.md')
      ? 'requirements'
      : 'new';

// ── ledger ──────────────────────────────────────────────────────────────────
let state = null;
const rawState = read('.spec-state.json');
if (rawState === null) {
  warn('no .spec-state.json: nothing records what was approved or why');
} else {
  try {
    state = JSON.parse(rawState);
  } catch (e) {
    fail(`.spec-state.json does not parse: ${e.message}`);
  }
}
if (state && typeof state !== 'object') {
  fail('.spec-state.json is not an object');
  state = null;
}
if (state?.phase !== undefined) {
  fail(
    '.spec-state.json has a `phase` field: phase is derived from the files, a second copy drifts'
  );
}
if (state?.closure !== undefined && !CLOSURES.includes(state.closure)) {
  fail(`closure "${state.closure}" is not one of ${CLOSURES.join(' | ')}`);
}
if (state?.tier !== undefined && ![1, 2, 3].includes(state.tier)) {
  fail(`tier ${JSON.stringify(state.tier)} is not 1, 2 or 3`);
}

// ── approval receipts ───────────────────────────────────────────────────────
const receipts = Array.isArray(state?.approved) ? state.approved : [];
const approvalOf = new Map();
for (const r of receipts) {
  if (!r || typeof r.file !== 'string' || typeof r.sha256 !== 'string') {
    fail(`malformed receipt in approved[]: ${JSON.stringify(r)}`);
    continue;
  }
  if (!present.has(r.file)) {
    fail(`receipt for ${r.file}, but that file does not exist`);
    continue;
  }
  const actual = sha(r.file);
  approvalOf.set(r.file, { ...r, actual, ok: actual === r.sha256 });
  if (actual !== r.sha256) {
    fail(
      `${r.file} changed after approval: receipt is void, re-open that gate (recorded ${r.sha256.slice(0, 12)}…, actual ${actual.slice(0, 12)}…)`
    );
  }
}
// Downstream cascade: a void upstream approval voids everything after it. The
// hash still matching is not enough: the document it was approved against moved.
let voidedUpstream = null;
for (const f of GATED) {
  const a = approvalOf.get(f);
  if (voidedUpstream && a?.ok) {
    fail(`${f} approval is void too: ${voidedUpstream} changed after it was approved`);
    a.ok = false;
    a.cascaded = voidedUpstream;
  }
  if (a && !a.ok && !a.cascaded) voidedUpstream = f;
}

// ── open decisions ──────────────────────────────────────────────────────────
const decisions = Array.isArray(state?.decisions) ? state.decisions : [];
const open = decisions.filter((d) => d && (d.answer === null || d.answer === undefined));
for (const d of decisions) {
  if (!d || !d.id || !d.title) fail(`decision without id or title: ${JSON.stringify(d)}`);
  else if ((d.answer === null || d.answer === undefined) && !d.recommended) {
    fail(
      `open decision "${d.id}" has no recommended option: a question without a recommendation offloads the work`
    );
  } else if (d.answer && !d.why) {
    warn(`answered decision "${d.id}" has no \`why\`: the reasoning is the point of the ledger`);
  }
}

// ── coverage: criteria <-> task citations ───────────────────────────────────
const reqText = read('requirements.md');
const taskText = read('tasks.md');
const criteria = new Set();
if (reqText) {
  for (const m of reqText.matchAll(/^\s*(?:[-*]\s*)?(\d+\.\d+)[.)]?\s+\S/gm)) criteria.add(m[1]);
  if (criteria.size === 0)
    warn('no `N.M` numbered criteria found in requirements.md: tasks cannot cite them');
}

const cited = new Set();
const declaredFiles = new Set();
let taskCount = 0;
const noVerify = [];
const badScript = [];
if (taskText) {
  // One task = a checkbox line plus the indented lines under it, up to the next
  // checkbox. Verify:/_Requirements:_ belong to the task above them.
  const lines = taskText.split('\n');
  const starts = [];
  lines.forEach((l, i) => {
    if (/^\s*-\s*\[[ xX]\]/.test(l)) starts.push(i);
  });
  taskCount = starts.length;
  for (let s = 0; s < starts.length; s++) {
    const from = starts[s];
    const to = s + 1 < starts.length ? starts[s + 1] : lines.length;
    const block = lines.slice(from, to).join('\n');
    const label = (lines[from].match(/\[[ xX]\]\s*([\d.]+)/) || [, '?'])[1];
    const isParent = s + 1 < starts.length && /^\s*-\s*\[[ xX]\]\s*\d+\.\s/.test(lines[from]);

    // Files: a task declares, so a `Proven by:` test one of them creates is not
    // reported as missing.
    for (const m of block.matchAll(/^\s*[-*]?\s*Files:\s*(.+)$/gim)) {
      for (const p of m[1].split(',')) declaredFiles.add(p.trim().replace(/^`|`$/g, ''));
    }

    const reqM = block.match(/_Requirements:\s*([^_]+)_/);
    if (reqM) {
      for (const tok of reqM[1]
        .split(',')
        .map((t) => t.trim())
        .filter(Boolean)) {
        if (tok !== 'enabler') cited.add(tok);
      }
    }
    // A bare parent heading ("1. Component") carries no work of its own, so it
    // needs neither a Verify: nor a citation.
    if (isParent) continue;
    if (!/\bVerify:/.test(block)) noVerify.push(label);
    if (!reqM) noVerify.push(`${label} (no _Requirements:_ either)`);
    // `npm test` is `npm run test`, so it gets the same existence check.
    for (const m of block.matchAll(/npm (?:run ([a-z0-9:_-]+)|(test)(?![a-z0-9:_-]))/gi))
      badScript.push([label, m[1] ?? m[2]]);
  }
}

// Do the npm-script existence check once, against the repo root.
if (badScript.length) {
  let scripts = {};
  try {
    scripts = JSON.parse(readFileSync(resolve('package.json'), 'utf8')).scripts || {};
  } catch {
    warn('could not read package.json to validate Verify: commands');
    badScript.length = 0;
  }
  for (const [label, name] of badScript) {
    if (!(name in scripts))
      fail(
        `task ${label} verifies with \`npm run ${name}\`, which is not a script in package.json`
      );
  }
}

const uncovered = [...criteria].filter((c) => !cited.has(c));
const orphans = [...cited].filter((c) => !criteria.has(c));
if (taskText && criteria.size) {
  if (uncovered.length) fail(`criteria no task implements: ${uncovered.join(', ')}`);
  if (orphans.length)
    fail(`tasks cite criteria that do not exist (renumbered?): ${orphans.join(', ')}`);
}
for (const t of noVerify) fail(`task ${t} has no Verify: line: that is not a task`);

// ── non-regression assertions ───────────────────────────────────────────────
// Every `SHALL CONTINUE TO` names the test that proves it. The test may not
// exist yet, but then some task must create it: an assertion backed by neither
// is the one most likely to be quietly dropped, and these sit on money and
// access-control paths. Checked here because "each assertion has a real test"
// is precisely the kind of claim that survives a hand review unexamined.
let assertions = 0;
if (reqText) {
  for (const block of reqText.split(/\n(?=[ \t]*[-*][ \t])/)) {
    if (!/SHALL CONTINUE TO/.test(block)) continue;
    assertions++;
    const label = block.trim().replace(/\s+/g, ' ').slice(0, 58);
    const m = block.match(/Proven by:\s*`?([^`\n]+?)`?\s*$/m);
    if (!m) {
      fail(`non-regression assertion has no \`Proven by:\` line: "${label}…"`);
      continue;
    }
    const p = m[1].trim();
    if (!existsSync(resolve(p)) && !declaredFiles.has(p)) {
      fail(`\`Proven by: ${p}\` does not exist and no task's Files: creates it`);
    }
  }
}

// ── archive safety ──────────────────────────────────────────────────────────
const archived = GATED.some((f) => (read(f) || '').includes('> Archived '));
if (archived && state?.closure && !['deployed', 'verified'].includes(state.closure)) {
  fail(
    `spec is marked Archived at closure "${state.closure}": archive only at deployed or verified`
  );
}

// ── report ──────────────────────────────────────────────────────────────────
const dim = (s) => `\x1b[2m${s}\x1b[0m`;
console.log(`spec    ${specDir}`);
console.log(`phase   ${phase} ${dim('(derived from files present)')}`);
console.log(`tier    ${state?.tier ?? dim('unset')}    closure  ${state?.closure ?? dim('open')}`);
console.log(`files   ${GATED.filter((f) => present.has(f)).join(', ') || dim('none')}`);
if (receipts.length) {
  console.log('\napprovals');
  for (const f of GATED) {
    const a = approvalOf.get(f);
    if (!a) continue;
    const why = a.cascaded ? dim(` (${a.cascaded} moved under it)`) : '';
    console.log(
      `  ${a.ok ? '\x1b[32mok\x1b[0m  ' : '\x1b[31mVOID\x1b[0m'} ${f} ${dim(a.at || '')}${why}`
    );
  }
}
if (criteria.size || taskCount) {
  console.log('\ncoverage');
  console.log(
    `  criteria ${criteria.size}   cited ${cited.size}   tasks ${taskCount}   assertions ${assertions}   open decisions ${open.length}`
  );
}
if (warnings.length) {
  console.log('');
  for (const w of warnings) console.log(`  \x1b[33mwarn\x1b[0m  ${w}`);
}
if (problems.length) {
  console.log('');
  for (const p of problems) console.log(`  \x1b[31mfail\x1b[0m  ${p}`);
}
console.log(
  `\n${problems.length ? `\x1b[31m${problems.length} problem(s)\x1b[0m` : '\x1b[32mclean\x1b[0m'}${warnings.length ? dim(`, ${warnings.length} warning(s)`) : ''}`
);
process.exit(problems.length ? 1 : 0);
