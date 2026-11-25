export const meta = {
  name: 'fix-waves',
  description: 'Fix verified findings in waves of batches that never share a file, then a knip dead-code sweep',
  phases: [{ title: 'Fix' }, { title: 'Sweep', detail: 'knip-driven dead code removal' }],
}
// args: {
//   repo: absolute worktree path,
//   reviewJson: absolute path of the saved review.js result ({ confirmed: [{ id, ... }] }),
//   batches: [{ k, strong, ids: [..], files: [..] }]   (scripts/review/plan-waves.mjs builds these; `model` also works),
//   waves: [[batchKey, ...], ...]                        (batches in one wave share no file),
//   decisions?: { [id]: "owner decision text" },
//   rules?: extra project rules for fixers (languages, billing, and so on),
//   superpowers?: absolute path of the superpowers skills folder, if installed,
//   sweep?: true (default) to run the knip sweep at the end
// }
const A = args || {}
const SP = A.superpowers || ''
const modelOf = (b) => b.model || (b.strong ? 'opus' : 'sonnet')
const RESULT = { type: 'object', properties: {
  results: { type: 'array', items: { type: 'object', properties: {
    id: { type: 'integer' }, status: { type: 'string', enum: ['fixed', 'partial', 'skipped'] },
    summary: { type: 'string' }, files_changed: { type: 'array', items: { type: 'string' } },
    tests: { type: 'string' }, open_item: { type: 'string', description: 'deferred part / owner action / migration to apply; empty if none' } },
    required: ['id', 'status', 'summary', 'files_changed', 'tests', 'open_item'] } },
  checks: { type: 'string' } }, required: ['results', 'checks'] }

function prompt(b, forbidden) {
  const dec = b.ids.filter(id => A.decisions && A.decisions[id]).map(id => `- #${id}: ${A.decisions[id]}`).join('\n')
  return `Fix verified code-review findings. WORK ONLY IN ${A.repo} (cd there; absolute paths; never touch any other checkout). No commits, no git state changes (no stash/checkout/reset), no builds or dev servers.
Batch "${b.k}", ids ${JSON.stringify(b.ids)}: the findings with those "id" values in the "confirmed" array of ${A.reviewJson} (read it with node). FIRST re-check each finding against the CURRENT code; skip with a reason if it is not real or already fixed.
${dec ? `Owner decisions (follow them):\n${dec}\n` : ''}Other fixers are editing these files RIGHT NOW, do not edit them: ${forbidden.length ? forbidden.join(', ') : '(none)'}. If a fix truly needs one, do the rest and report partial with an open_item.
How: ${SP ? `read ${SP}/systematic-debugging/SKILL.md and ${SP}/test-driven-development/SKILL.md; ` : ''}unit-test pure logic first (watch it fail, then fix). Minimal changes in the surrounding style; no drive-by refactors; delete dead code rather than comment it out. Keep backward compatibility (old clients, sent links, existing rows, existing auth methods: deprecate with a log line, don't break). No DB migration unless a decision says so; if one is needed, make the code work without it and report it as an open_item. Never change the deploy build pipeline (build script, deploy workflow, hosting config).${A.rules ? `\nProject rules: ${A.rules}` : ''}
Finally run \`npx tsc --noEmit\` (ignore errors in files outside your batch) and the relevant tests. Report per finding.`
}

phase('Fix')
const all = []
for (let w = 0; w < A.waves.length; w++) {
  const inWave = A.waves[w].map(k => A.batches.find(b => b.k === k)).filter(Boolean)
  const res = await parallel(inWave.map(b => () => {
    const forbidden = [...new Set(inWave.filter(o => o !== b).flatMap(o => o.files))].filter(f => !b.files.includes(f))
    return agent(prompt(b, forbidden), { label: `fix:${b.k}`, phase: 'Fix', schema: RESULT, model: modelOf(b), effort: 'high' })
  }))
  const named = inWave.map((b, i) => ({ area: b.k, ...(res[i] || { results: [], checks: 'agent failed: inspect its partial diff and resume this batch' }) }))
  all.push(...named)
  log(`wave ${w + 1}/${A.waves.length}: ${named.map(r => `${r.area} ${r.results.filter(x => x.status === 'fixed').length}/${r.results.length}`).join(', ')}`)
}

let sweep = null
if (A.sweep !== false) {
  phase('Sweep')
  sweep = await agent(`Dead-code sweep. WORK ONLY IN ${A.repo} (absolute paths; no commits/git state changes; no builds/dev server). Keep the fixes already in the working tree.
1. Run \`npx -y knip@5 --no-progress\`. If it misreads entry points, add or fix a small knip.json (Next.js: app route/page/layout files, proxy.ts or middleware.ts, next.config, scripts referenced from package.json, e2e, tests; ignore separately built folders such as desktop/, mobile/ or a standalone package) and keep it.
2. Verify every unused file/export/dependency by grep (dynamic imports, string paths, CSS classes, tests, scripts, other packages) before removing. Only remove what is certainly dead: drop unused \`export\` keywords, delete unused definitions; remove unused deps only if nothing imports them anywhere, then \`npm install --package-lock-only --ignore-scripts\`. Never touch build/install scripts.
3. List (don't fix) junk tracked by git (.DS_Store, *.tsbuildinfo, stray logs).
4. \`npx tsc --noEmit\` and all test suites must pass.
Report removed items with evidence, items left and why, and check results.`, { label: 'sweep:knip', phase: 'Sweep', model: 'sonnet', effort: 'high' })
}
return { fixes: all, sweep }
