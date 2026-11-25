export const meta = {
  name: 'content-gaps',
  description: 'Find which shipped features the home page, help, privacy and docs do not mention yet; draft the copy',
  phases: [
    { title: 'Inventory', detail: 'shipped features vs what each surface says' },
    { title: 'Plan', detail: 'gap list with concrete edits' },
  ],
}
// args: {
//   repo: absolute worktree path (a fresh worktree from origin/main),
//   app: one paragraph describing the app,
//   since?: date (YYYY-MM-DD) to focus on features shipped after it,
//   languages?: ["en", "el"]   (every user-facing string needs all of them; default ["en"]),
//   surfaces?: where users read about the app, as paths or folders (default: a Next.js list below),
//   rules?: copy rules the plan must follow (for example "only the free plan may be advertised"),
//   docs?: repo-relative paths of style and glossary docs to follow (DESIGN.md, a translation glossary)
// }
const A = args || {}
const LANGS = A.languages && A.languages.length ? A.languages : ['en']
const RO = `Work in ${A.repo} (cd there first; it is a git worktree). READ-ONLY: do not edit or create files, do not change git state.`
const SURFACES = A.surfaces && A.surfaces.length ? A.surfaces : [
  'home/landing page (src/app/page.tsx and its components)', 'help and about pages', 'privacy and terms pages',
  'pricing page', 'onboarding / connect / setup pages', 'public/llms.txt (and llms-full.txt)',
  'JSON-LD and site metadata (layout.tsx, any SiteJsonLd component)', 'public manifest (manifest.webmanifest or app/manifest.ts)',
  'README.md and docs/*.md', 'translation dictionaries (if the UI has more than one language)',
]

phase('Inventory')
const FEAT = { type: 'object', properties: { features: { type: 'array', items: { type: 'object', properties: {
  name: { type: 'string' }, what_user_gets: { type: 'string' }, status: { type: 'string', description: 'on for all | beta/opt-in (how to turn on) | flagged/owner-only | internal-only' },
  where_in_ui: { type: 'string' }, plans: { type: 'string', description: 'which plans get it, if limited' }, data_captured: { type: 'string', description: 'personal data it stores or sends to an outside processor (AI, email, analytics); empty if none' },
  evidence: { type: 'string', description: 'commit sha / file' } },
  required: ['name', 'what_user_gets', 'status', 'where_in_ui', 'plans', 'data_captured', 'evidence'] } } }, required: ['features'] }
const SURF = { type: 'object', properties: { surfaces: { type: 'array', items: { type: 'object', properties: {
  surface: { type: 'string' }, files: { type: 'array', items: { type: 'string' } }, features_mentioned: { type: 'array', items: { type: 'string' } },
  outdated_or_wrong_claims: { type: 'array', items: { type: 'string' } }, structure_notes: { type: 'string', description: 'how content is organised (sections, translation keys, components) so an editor knows where to add' } },
  required: ['surface', 'files', 'features_mentioned', 'outdated_or_wrong_claims', 'structure_notes'] } } }, required: ['surfaces'] }

const [feat, surf] = await parallel([
  () => agent(`${RO}\nBuild an inventory of USER-VISIBLE features of this app as shipped today: ${A.app}\n${A.since ? `Emphasis on everything added since ${A.since}: git log --since=${A.since} --format='%h %s' (and PR titles via the merge commits). ` : ''}Also read the README, docs/*.md, any open-items or changelog doc, and the code itself to confirm each feature's status (feature flags, env-gated features, opt-in settings, plan limits). Include older core features too. Be precise about status (beta, opt-in, owner-only). For each feature say what personal data it stores or sends to an outside processor. Do not invent features.`, { label: 'features', phase: 'Inventory', schema: FEAT, model: 'sonnet', effort: 'high' }),
  () => agent(`${RO}\nInventory what each public and help surface of this app tells users today. Surfaces (find the real files): ${SURFACES.map((s, i) => `(${i + 1}) ${s}`).join(', ')}. For each: which features it mentions, any claims that are now wrong or outdated (old names, wrong limits, removed features, a language the UI no longer lacks), and how the content is structured so an editor knows where new text goes.`, { label: 'surfaces', phase: 'Inventory', schema: SURF, model: 'sonnet', effort: 'high' }),
])
if (!feat || !surf) return { error: `inventory failed (${!feat ? 'features' : ''}${!feat && !surf ? ', ' : ''}${!surf ? 'surfaces' : ''}); rerun`, features: feat, surfaces: surf }

phase('Plan')
const PLAN = { type: 'object', properties: { edits: { type: 'array', items: { type: 'object', properties: {
  surface: { type: 'string' }, file: { type: 'string' }, priority: { type: 'string', enum: ['must', 'should', 'nice'] },
  change: { type: 'string', description: 'what to add/replace and exactly where (component/section/translation key)' },
  text: { type: 'object', description: 'the new text per language; an empty string for the other languages of English-only files (README, llms.txt)', properties: Object.fromEntries(LANGS.map(l => [l, { type: 'string' }])), required: LANGS },
  reason: { type: 'string' } }, required: ['surface', 'file', 'priority', 'change', 'text', 'reason'] } },
  notes: { type: 'string' } }, required: ['edits', 'notes'] }
const plan = await agent(`${RO}\nYou are the product copy editor for this app. Below are (A) the shipped-feature inventory and (B) what each surface says today. Produce a concrete edit plan so the home page, help, about, privacy, onboarding, llms.txt, JSON-LD/metadata, manifest and README describe the product as it is now, and fix wrong or outdated claims.
Constraints: ${A.docs && A.docs.length ? `read ${A.docs.join(', ')} and ` : ''}match the existing tone and section structure (open the actual files you propose to change). The privacy page must name every kind of personal data captured and every outside processor that receives it. Mark beta features as beta. Don't promise what the code doesn't do; owner-only or flagged features are not advertised as available to everyone. Keep additions short (a home page is not a manual): prefer extending an existing feature list over new sections. Every user-facing UI string needs all of these languages: ${LANGS.join(', ')}.${A.rules ? ` Rules: ${A.rules}` : ''} Give exact placement (component + section or translation key).\n\n(A) FEATURES:\n${JSON.stringify(feat, null, 1)}\n\n(B) SURFACES:\n${JSON.stringify(surf, null, 1)}`, { label: 'copy-plan', phase: 'Plan', schema: PLAN, model: 'opus', effort: 'high' })
return { features: feat, surfaces: surf, plan }
