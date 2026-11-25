export const meta = {
  name: 'diff-review',
  description: 'Fresh reviewers check the fix diff per area for regressions, verify each, fix confirmed ones, rerun all checks',
  phases: [
    { title: 'Review', detail: 'fresh reviewers per area hunt regressions' },
    { title: 'Verify', detail: 'skeptic per finding' },
    { title: 'Fix', detail: 'disjoint file clusters in parallel' },
    { title: 'Check', detail: 'typecheck + all tests' },
  ],
}
// args: {
//   repo: absolute worktree path (changes uncommitted, or committed on a branch, compared with `base`),
//   base?: what the changes are compared with (default origin/main),
//   groups: { areaName: [changedFile, ...] }   (git diff --name-only origin/main plus new untracked files from
//           git ls-files --others --exclude-standard, grouped by area; deleted files as "path (deleted)"),
//   context?: absolute paths of files describing intent (the saved review and fix results),
//   notes?: deploy facts reviewers must know (for example "new migrations are NOT applied yet; code must work without them"),
//   checks?: shell commands for the final check (default: tsc + npm test),
//   superpowers?: absolute path of the superpowers skills folder, if installed
// }
// Run it once per big change set. On a real 282-file release it found 14 regressions that the first-round fixes had introduced.
const A = args || {}
const SP = A.superpowers || ''
const BASE = A.base || 'origin/main'
// Paths relative to the repo, so the same file named two ways still counts as one file below.
const REPO = String(A.repo || '').replace(/\\/g, '/').replace(/\/+$/, '')
const rel = (f) => { let x = String(f || '').trim().replace(/\\/g, '/').replace(/ \(.*$/, '').replace(/:\d+(?::\d+)?$/, ''); if (REPO && x.startsWith(`${REPO}/`)) x = x.slice(REPO.length + 1); return x.replace(/^\.\//, '') }
const RO = `Work in ${A.repo} (cd there; absolute paths; never read another checkout). READ-ONLY: no edits, no git state changes, no servers/builds.`
const FIND = { type: 'object', properties: { findings: { type: 'array', items: { type: 'object', properties: {
  title: { type: 'string' }, file: { type: 'string' }, line: { type: 'integer' },
  severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] },
  kind: { type: 'string', enum: ['regression', 'incomplete-fix', 'new-bug', 'i18n', 'security', 'deploy-risk'] },
  scenario: { type: 'string' }, fix: { type: 'string' } },
  required: ['title', 'file', 'line', 'severity', 'kind', 'scenario', 'fix'] } } }, required: ['findings'] }

phase('Review')
const areas = Object.entries(A.groups)
const reviewed = await parallel(areas.map(([k, files]) => () =>
  agent(`${RO}
Independent senior reviewer. Other agents just made a large batch of fixes. Find what these CHANGES broke or got wrong: regressions, half-done fixes, new bugs, new security holes, behaviour changes that hurt real users, deploy risks (code needing a migration/env var that may not exist in production without a fallback), missing translations for new user-facing strings, broken backward compatibility (old clients, sent links, existing rows). Don't review untouched code; no style nits.
Area "${k}", changed files: ${files.join(', ')}. Read \`git diff ${BASE} -- <file>\`; new files may be untracked and then do not show in git diff, so read them whole. Also read the callers needed to judge.
${A.context ? `Intent: ${A.context}\n` : ''}${A.notes ? `Facts: ${A.notes}\n` : ''}${SP ? `Method: ${SP}/requesting-code-review/code-reviewer.md and ${SP}/verification-before-completion/SKILL.md. ` : ''}Evidence, not guesses. Zero findings is fine.`,
    { label: `review:${k}`, phase: 'Review', schema: FIND, model: 'opus', effort: 'high' })
    .then(r => (r ? r.findings.map(f => ({ ...f, area: k })) : null))))
const failedAreas = areas.filter((a, i) => !reviewed[i]).map(([k]) => k)
const found = reviewed.filter(Boolean).flat()
log(`${found.length} candidate regressions${failedAreas.length ? ` (reviewers failed, rerun: ${failedAreas.join(', ')})` : ''}`)

phase('Verify')
const VERD = { type: 'object', properties: { real: { type: 'boolean' }, reasoning: { type: 'string' }, fix: { type: 'string' }, files: { type: 'array', items: { type: 'string' } } }, required: ['real', 'reasoning', 'fix', 'files'] }
const checked = await parallel(found.map(f => () =>
  agent(`${RO}\nAdversarially verify this claimed problem in the current tree vs ${BASE}. Try to refute it (code, callers, fallbacks, tests). Default real=false without concrete evidence. If real: minimal precise fix and the files it touches, as paths relative to the repo.\nClaim (${f.area}, ${f.kind}, ${f.severity}): ${f.title}\nWhere: ${f.file}:${f.line}\nScenario: ${f.scenario}\nProposed fix: ${f.fix}`,
    { label: `verify:${f.file.split('/').pop()}:${f.line}`, phase: 'Verify', schema: VERD, model: f.severity === 'low' ? 'sonnet' : 'opus', effort: 'high' })))
const verified = found.map((f, i) => (checked[i] && checked[i].real ? { ...f, v: checked[i] } : null)).filter(Boolean)
// A regression whose verifier failed is kept, not counted as "not real": check it again by hand.
const unverified = found.filter((f, i) => !checked[i]).map(f => ({ title: f.title, where: `${f.file}:${f.line}`, sev: f.severity, kind: f.kind, scenario: f.scenario, fix: f.fix }))
log(`${verified.length} confirmed${unverified.length ? `, ${unverified.length} not verified (verifier failed; see "unverified")` : ''}`)
if (!verified.length) return { found: found.length, failedAreas, confirmed: [], unverified, fixes: [], check: 'nothing to fix' }

phase('Fix')
// Findings that touch a common file go to the same fixer (union-find over files), so no two fixers edit one file.
const par = new Map()
const root = (a) => { const p = par.get(a); if (p === a) return a; const r = root(p); par.set(a, r); return r }
verified.forEach(f => { f.fs = [...new Set([f.file, ...(f.v.files || [])].map(rel).filter(Boolean))]; f.fs.forEach(x => { if (!par.has(x)) par.set(x, x) }); f.fs.slice(1).forEach(x => { par.set(root(x), root(f.fs[0])) }) })
const byRoot = new Map()
verified.forEach(f => { const r = root(f.fs[0]); if (!byRoot.has(r)) byRoot.set(r, []); byRoot.get(r).push(f) })
const clusters = [...byRoot.values()]
const FIXR = { type: 'object', properties: { results: { type: 'array', items: { type: 'object', properties: { title: { type: 'string' }, status: { type: 'string', enum: ['fixed', 'skipped'] }, summary: { type: 'string' }, files: { type: 'array', items: { type: 'string' } } }, required: ['title', 'status', 'summary', 'files'] } } }, required: ['results'] }
const fixes = await parallel(clusters.map((c, ci) => () =>
  agent(`Fix these verified problems. WORK ONLY IN ${A.repo} (absolute paths; no commits/git state changes; no builds). Others are fixing OTHER files right now; edit only: ${[...new Set(c.flatMap(f => f.fs))].join(', ')} (plus new test files). Minimal changes in the surrounding style; unit-test pure logic. Run relevant tests and \`npx tsc --noEmit\` (ignore errors outside your files).
${c.map((f, j) => `\n${j + 1}. ${f.title} (${f.file}:${f.line})\nScenario: ${f.scenario}\nVerifier: ${f.v.reasoning}\nFix: ${f.v.fix}`).join('\n')}`,
    { label: `fix:cluster${ci}`, phase: 'Fix', schema: FIXR, model: 'opus', effort: 'high' })))

phase('Check')
const check = await agent(`In ${A.repo} (no edits unless a check fails from an obvious mistake in the changes; then fix minimally and say so): run ${A.checks || '`npx tsc --noEmit` and `npm test`'}. Report pass/fail counts and failure output verbatim.`, { label: 'check', phase: 'Check', model: 'sonnet', effort: 'medium' })
return { found: found.length, failedAreas, confirmed: verified.map(f => ({ title: f.title, where: `${f.file}:${f.line}`, sev: f.severity, kind: f.kind, fix: f.v.fix })), unverified, fixes: fixes.filter(Boolean), clusters: clusters.length, check }
