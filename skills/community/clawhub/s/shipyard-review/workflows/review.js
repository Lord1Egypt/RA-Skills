export const meta = {
  name: 'app-review',
  description: 'Area reviewers find issues, dedup, one adversarial verifier per finding (read-only)',
  phases: [
    { title: 'Find', detail: 'one reviewer per area, read-only' },
    { title: 'Dedup', detail: 'merge duplicates across areas' },
    { title: 'Verify', detail: 'skeptic per finding, default refute' },
  ],
}
// args: {
//   repo: absolute path of the checkout to review (a fresh worktree from origin/main),
//   app: one paragraph describing the app and its stack,
//   areas: [{ key, strong: true|false, scope }]   (see examples/nextjs-supabase-areas.json; `model` also works),
//   skip?: what to ignore (for example "payments are switched off"),
//   openItems?: repo-relative path of the known-issues doc (for example "docs/OPEN-ITEMS.md"),
//   focusAuthor?: commit author email whose work gets extra scrutiny (another agent's, for example),
//   superpowers?: absolute path of the superpowers skills folder, if installed (optional method guides),
//   maxPerArea?: default 15
// }
// Returns { repo, counts, failedAreas[], confirmed[], uncertain[], unverified[], refuted[] }. Save it to a file: plan-waves.mjs and fix-waves.js read it.
const A = args || {}
const modelOf = (x) => x.model || (x.strong ? 'opus' : 'sonnet')
const SP = A.superpowers || ''
const guide = SP ? `Method: skim ${SP}/requesting-code-review/code-reviewer.md and ${SP}/systematic-debugging/SKILL.md (root cause, evidence before claims).` : 'Method: root cause and evidence before claims.'
const PRE = `You are reviewing this app: ${A.app}
Repo = ${A.repo} (cd there; it is a git worktree). READ-ONLY: do not edit, create or delete files, do not change git state, do not start servers. Always use absolute paths under ${A.repo}; never read any other checkout.
Rules:
${A.skip ? `- Skip: ${A.skip}\n` : ''}${A.openItems ? `- Read ${A.openItems} first and do NOT re-report anything already listed there.\n` : ''}${A.focusAuthor ? `- Commits by ${A.focusAuthor} get EXTRA scrutiny: git log --author='${A.focusAuthor}' --format='%h %s', then git show <sha> -- <paths>. Judge the CURRENT code.\n` : ''}- ${guide} Trace real call paths; read callers and callees before claiming a bug.
- Report only what matters: real bugs (wrong behaviour, crashes, races, stuck UI, data loss), security/data-isolation holes, broken or half-wired features, perf/cost problems with real impact, worthwhile cleanups (category "cleanup"). No style nits.
- Every finding: exact file (relative to the repo) + line, a CONCRETE failure scenario, a specific fix. focus_author=true if the code came from the focus author. Honest confidence 0-1.
- At most ${A.maxPerArea || 15} findings, most severe first. Zero is a valid answer.`

const FINDINGS = { type: 'object', properties: { findings: { type: 'array', items: { type: 'object', properties: {
  title: { type: 'string' }, file: { type: 'string' }, line: { type: 'integer' },
  severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] },
  category: { type: 'string', enum: ['bug', 'security', 'perf', 'cost', 'cleanup', 'i18n', 'test', 'ux'] },
  focus_author: { type: 'boolean' }, confidence: { type: 'number' },
  description: { type: 'string' }, failure_scenario: { type: 'string' }, suggested_fix: { type: 'string' } },
  required: ['title', 'file', 'line', 'severity', 'category', 'focus_author', 'confidence', 'description', 'failure_scenario', 'suggested_fix'] } } },
  required: ['findings'] }

phase('Find')
const found = await parallel(A.areas.map(a => () =>
  agent(`${PRE}\n\nYOUR AREA (${a.key}):\n${a.scope}`, { label: `find:${a.key}`, phase: 'Find', schema: FINDINGS, model: modelOf(a), effort: 'high' })
    .then(r => (r ? r.findings.map(f => ({ ...f, area: a.key })) : null))))
const failedAreas = A.areas.filter((a, i) => !found[i]).map(a => a.key)
const all = found.filter(Boolean).flat().map((f, id) => ({ id, ...f }))
log(`${all.length} raw findings from ${A.areas.length - failedAreas.length}/${A.areas.length} areas${failedAreas.length ? ` (failed, rerun: ${failedAreas.join(', ')})` : ''}`)

phase('Dedup')
const DEDUP = { type: 'object', properties: { groups: { type: 'array', items: { type: 'object', properties: { keep: { type: 'integer' }, merged: { type: 'array', items: { type: 'integer' } } }, required: ['keep', 'merged'] } } }, required: ['groups'] }
const dd = all.length > 1 ? await agent(`Group code-review findings that describe the SAME defect. One group per distinct defect: keep = best id, merged = the other ids (may be empty). Every id appears exactly once. Judge from text only.\n\n${all.map(f => `#${f.id} [${f.area}] ${f.file}:${f.line} ${f.severity} - ${f.title}: ${f.description.slice(0, 300)}`).join('\n')}`, { label: 'dedup', phase: 'Dedup', schema: DEDUP, model: 'sonnet', effort: 'medium' }) : null
let unique = all
if (dd && dd.groups && dd.groups.length) {
  const byId = new Map(all.map(f => [f.id, f])); const seen = new Set(); unique = []
  for (const g of dd.groups) {
    const k = byId.get(g.keep); if (!k || seen.has(g.keep)) continue; seen.add(g.keep)
    const extra = (g.merged || []).filter(id => byId.has(id) && !seen.has(id)); extra.forEach(id => seen.add(id))
    unique.push({ ...k, also: extra.map(id => `${byId.get(id).file}:${byId.get(id).line} (${byId.get(id).area}) ${byId.get(id).description.slice(0, 200)}`) })
  }
  for (const f of all) if (!seen.has(f.id)) unique.push(f)
}
log(`${unique.length} unique findings`)

phase('Verify')
const VERDICT = { type: 'object', properties: {
  verdict: { type: 'string', enum: ['confirmed', 'refuted', 'uncertain'] }, reasoning: { type: 'string' },
  severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] }, fix_plan: { type: 'string' },
  files_to_touch: { type: 'array', items: { type: 'string' } }, fix_risk: { type: 'string', enum: ['low', 'medium', 'high'] },
  needs_user_decision: { type: 'boolean' } },
  required: ['verdict', 'reasoning', 'severity', 'fix_plan', 'files_to_touch', 'fix_risk', 'needs_user_decision'] }
const verified = await parallel(unique.map(f => () => {
  const heavy = f.severity === 'critical' || f.severity === 'high' || f.category === 'security'
  return agent(`Adversarial verifier. Repo: ${A.repo} (cd there; READ-ONLY; absolute paths only, never read another checkout). A reviewer claims the defect below. Try hard to REFUTE it: read the code, callers, guards elsewhere (proxy/middleware, RLS/migrations, wrappers)${A.openItems ? `, and ${A.openItems} (already listed = refuted)` : ''}. ${A.skip ? `Out of scope (refuted): ${A.skip}. ` : ''}No concrete evidence = refuted (uncertain only if truly 50/50). If real: right severity, precise minimal fix plan, files (relative to the repo), fix risk, needs_user_decision only for product/billing/data decisions.\n\nCLAIM (${f.area}, ${f.category}, ${f.severity}):\n${f.title}\nWhere: ${f.file}:${f.line}\n${f.description}\nScenario: ${f.failure_scenario}\nSuggested fix: ${f.suggested_fix}${f.also && f.also.length ? `\nAlso reported at:\n- ${f.also.join('\n- ')}` : ''}`,
    { label: `verify:${f.area}:${f.file.split('/').pop()}:${f.line}`, phase: 'Verify', schema: VERDICT, model: heavy ? 'opus' : 'sonnet', effort: heavy ? 'high' : 'medium' })
    .then(v => (v ? { ...f, v } : null))
}))
const vs = verified.filter(Boolean)
const slim = x => ({ area: x.area, cat: x.category, focus: x.focus_author, title: x.title, where: `${x.file}:${x.line}`, sev: x.v.severity, desc: x.description, scenario: x.failure_scenario, fix: x.v.fix_plan, files: x.v.files_to_touch, risk: x.v.fix_risk, decide: x.v.needs_user_decision, why: x.v.reasoning, also: x.also })
// `id` is the finding's number everywhere after this: plan-waves --skip, fix-waves decisions, the list shown to the owner.
const confirmed = vs.filter(x => x.v.verdict === 'confirmed').map((x, id) => ({ id, ...slim(x) }))
const uncertain = vs.filter(x => x.v.verdict === 'uncertain').map(slim)
// A finding whose verifier failed is kept, not dropped: verify it again by hand or in a rerun.
const unverified = unique.filter((f, i) => !verified[i]).map(f => ({ area: f.area, cat: f.category, title: f.title, where: `${f.file}:${f.line}`, sev: f.severity, desc: f.description, scenario: f.failure_scenario, fix: f.suggested_fix }))
log(`${confirmed.length} confirmed, ${uncertain.length} uncertain, ${vs.length - confirmed.length - uncertain.length} refuted${unverified.length ? `, ${unverified.length} not verified (verifier failed; see "unverified")` : ''}`)
return { repo: A.repo, counts: { raw: all.length, unique: unique.length, confirmed: confirmed.length, uncertain: uncertain.length, unverified: unverified.length }, failedAreas, confirmed, uncertain, unverified,
  refuted: vs.filter(x => x.v.verdict === 'refuted').map(x => ({ title: x.title, where: `${x.file}:${x.line}`, why: x.v.reasoning.slice(0, 300) })) }
