// Diagnostics & onboarding commands: doctor (local runtime), verify (live
// product state), setup (first-run checklist). Extracted from cli.ts.
import { promises as fs } from 'node:fs'
import { platform, arch } from 'node:os'
import * as api from './api.js'
import {
  stateDir, authFilePath, ensureAgentBinding, loadAuth, saveAuth, clearAuth,
  loadBoundAgent, saveBoundAgent, savePendingLogin, loadPendingLogin, clearPendingLogin,
  isAuthFileWriteable, migrateLegacyState, type AgentBinding, type AuthState,
} from './state.js'
import { SKILL_NAME, SKILL_VERSION } from './version.js'
import { ok, withUpdateNotice, skillDir, updateInstruction, requireBoundAgent, shareUrlFor, verifyShareResolves } from './runtime.js'

export interface DoctorCheck {
  ok: boolean
  value?: unknown
  reason?: string
  warning?: string
  note?: string
}

export async function cmdDoctor() {
  const checks: Record<string, DoctorCheck> = {}

  // Node version
  const nodeV = process.versions.node
  const major = Number.parseInt(nodeV.split('.')[0] ?? '0', 10)
  checks.node_version =
    major >= 18
      ? { ok: true, value: `v${nodeV}` }
      : { ok: false, value: `v${nodeV}`, reason: 'requires Node >= 18 for built-in fetch' }

  checks.fetch = typeof fetch === 'function'
    ? { ok: true }
    : { ok: false, reason: 'global fetch unavailable; Node 18+ required' }

  // Per-agent binding + state directory + auth file. The binding shows WHICH
  // agent folder this working directory maps to — the key thing on a platform
  // that runs more than one agent (each must resolve to its OWN folder).
  const binding = await ensureAgentBinding(false)
  const sourceNote: Record<AgentBinding['source'], string> = {
    'env': 'SIOBAC_AGENT_KEY env var (explicit).',
    'local-file': `local binding file ${binding.binding_file}.`,
    'auto-discovered': 'no env var and no .siobac.json here, but exactly ONE logged-in agent exists — reusing it so a command run from another directory still finds the login (no false re-login). Set SIOBAC_AGENT_KEY or keep a .siobac.json to pin it explicitly if you run more than one agent.',
    'default-shared': 'no binding — using the SHARED default folder. Fine for a single agent; if this platform runs more than one agent, run `login` here so each gets its own .siobac.json (or set SIOBAC_AGENT_KEY).',
  }
  checks.agent_binding = {
    ok: true,
    value: { key: binding.key || null, source: binding.source, binding_file: binding.binding_file },
    warning: binding.source === 'default-shared' ? sourceNote['default-shared'] : undefined,
    note: sourceNote[binding.source],
  }
  const authFile = authFilePath()
  const writeCheck = await isAuthFileWriteable()
  checks.state_dir = writeCheck.ok
    ? { ok: true, value: stateDir() }
    : { ok: false, value: stateDir(), reason: writeCheck.reason ?? 'unknown' }

  try {
    const st = await fs.stat(authFile)
    const modeOctal = (st.mode & 0o777).toString(8).padStart(3, '0')
    const tooPermissive = (st.mode & 0o077) !== 0
    checks.auth_file = {
      ok: !tooPermissive,
      value: { path: authFile, mode: modeOctal, exists: true },
      warning: tooPermissive
        ? `auth.json mode ${modeOctal} is group/world readable; expected 600.`
        : undefined,
    }
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code === 'ENOENT') {
      checks.auth_file = {
        ok: true,
        value: { path: authFile, exists: false },
        warning: 'not logged in yet — run `login` to authenticate',
      }
    } else {
      checks.auth_file = { ok: false, value: authFile, reason: (e as Error).message }
    }
  }

  // API base + reachability. Surface WHICH base resolved — prod is the default;
  // a custom base is an explicit opt-in worth flagging so it's never a silent
  // surprise (e.g. an install accidentally left pointed at a non-production host).
  const apiBase = api.getApiBase()
  const apiEnv = api.getApiEnv()
  const envNote =
    apiEnv === 'custom' ? 'using a custom base from SIOBAC_API_BASE/OVOCLAW_API_BASE — NOT the default production server'
    : undefined
  try {
    const u = new URL(apiBase)
    if (u.protocol !== 'http:' && u.protocol !== 'https:') {
      checks.api_base = { ok: false, value: { base: apiBase, env: apiEnv }, reason: `must be http or https; got ${u.protocol}` }
    } else {
      checks.api_base = { ok: true, value: { base: apiBase, env: apiEnv }, warning: envNote, note: envNote }
    }
  } catch {
    checks.api_base = { ok: false, value: { base: apiBase, env: apiEnv }, reason: 'invalid URL' }
  }

  if (checks.api_base.ok) {
    const start = Date.now()
    try {
      const res = await fetch(`${apiBase}/health`, { method: 'GET' })
      checks.api_reachable = {
        ok: true,
        value: { http_status: res.status, response_time_ms: Date.now() - start },
      }
    } catch (e) {
      const cause = (e as Error & { cause?: { code?: string; message?: string } }).cause
      const reason = cause?.code || cause?.message || (e as Error).message
      checks.api_reachable = { ok: false, value: apiBase, reason: `network_error: ${reason}` }
    }
  } else {
    checks.api_reachable = { ok: false, reason: 'skipped — api_base invalid' }
  }

  // Freshness: actively probe the server for the latest version (this is a fresh
  // process, so nothing was captured yet). Report up-to-date vs stale + the exact
  // way to update — so "am I current?" has one reliable answer here.
  const vs = await api.getVersionStatus()
  const skill_freshness = !vs.reachable
    ? { up_to_date: null as boolean | null, your_version: vs.current, note: 'could not reach the server to check for updates (see api_reachable)' }
    : vs.up_to_date
      ? { up_to_date: true, your_version: vs.current, latest_version: vs.latest }
      : {
          up_to_date: false,
          required: vs.required,
          your_version: vs.current,
          latest_version: vs.latest,
          skill_path: skillDir(),
          how_to_update: updateInstruction(vs.update_url),
        }

  // PLATFORM HINTS (#16 / per-host first-run notes). Some hosts have quirks (e.g. an
  // ephemeral filesystem, or a model-option choice) that change setup. If the host/owner
  // set SIOBAC_PLATFORM, point at that platform's note; always point at the hints file so
  // a known-platform agent can read its specific first-run request. The notes themselves
  // live in references/platform-hints.md (data, not code).
  const platformId = (process.env.SIOBAC_PLATFORM ?? process.env.OVOCLAW_PLATFORM ?? '').trim().toLowerCase()
  const portableLoginActive = !!(process.env.SIOBAC_TOKEN ?? process.env.OVOCLAW_TOKEN ?? '').trim()
  // Per-host first-run notes (data lives in references/platform-hints.md; these are the
  // short actionable cue so the agent acts even without opening the file).
  const PLATFORM_NOTES: Record<string, string> = {
    doubao: 'Sandbox recycled on idle — the filesystem (auth.json) AND the env (SIOBAC_TOKEN) are wiped, so a normal login can\'t persist. `login` AUTO-secures this for you: it returns a portable_token. MEMORIZE it and re-inject as SIOBAC_TOKEN before EVERY run (not once per session — you can\'t tell if the sandbox was recycled). If you hit "not authenticated" after an idle gap, re-inject and retry — never ask the owner to re-login or to run a token command, and never explain tokens to them. See references/platform-hints.md → doubao.',
    qclaw: 'On your FIRST run, check which model you are running: if it is NOT Deepseek-V4-Pro, SUGGEST switching for a smoother experience — a SUGGESTION, not a requirement — with two options (1. already switched · 2. keep current). Offer once, don\'t nag. See references/platform-hints.md → qclaw/workbuddy.',
    workbuddy: 'On your FIRST run, check which model you are running: if it is NOT Deepseek-V4-Pro, SUGGEST switching for a smoother experience — a SUGGESTION, not a requirement — with two options (1. already switched · 2. keep current). Offer once, don\'t nag. See references/platform-hints.md → qclaw/workbuddy.',
  }
  const platformHint = platformId
    ? { id: platformId, portable_login_active: portableLoginActive, note: PLATFORM_NOTES[platformId] ?? `Known platform "${platformId}" — read references/platform-hints.md for any host-specific first-run setup.` }
    : { id: null, portable_login_active: portableLoginActive, note: 'No SIOBAC_PLATFORM set. If logins do not persist between runs (filesystem wiped), or your host has known quirks (e.g. an LLM-model choice), see references/platform-hints.md.' }

  // A stale skill isn't a hard doctor failure (commands still run), but a
  // REQUIRED update is — surface it loudly.
  const allOk = Object.values(checks).every((c) => c.ok) && !vs.required
  const report = {
    ok: allOk,
    skill: { name: SKILL_NAME, version: SKILL_VERSION },
    skill_freshness,
    runtime: { node: process.versions.node, platform: platform(), arch: arch() },
    platform_hint: platformHint,
    checks,
    next_step: allOk
      ? 'Local runtime + connectivity look fine. Tell the owner (in their language) the basics check out. (Run `verify` for the full live product check.)'
      : 'A local check FAILED — see each `checks` entry\'s `reason`/`value`. Tell the owner (in their language) what is wrong in plain words and fix it before relying on the agent.',
  }

  if (allOk) ok(report)
  process.stderr.write(JSON.stringify(report, null, 2) + '\n')
  process.exit(1)
}

// ── Verify — assert externally-visible state, not just that calls return 200 ──
// `doctor` checks the LOCAL runtime (node, state dir, reachability). `verify` is
// the product-level counterpart: it round-trips the things a real user depends
// on and ASSERTS the result — the server accepts the token, the share link a
// friend scans resolves to THIS agent, presence is readable, outbound tokens are
// alive. Each check says what it asserted + pass/fail. Read-only; safe anytime.
export interface VerifyCheck {
  ok: boolean
  asserted: string
  value?: unknown
  reason?: string
  warning?: string
  skipped?: boolean
}

export async function cmdVerify(_flags: Record<string, string | true>) {
  const checks: Record<string, VerifyCheck> = {}

  // 1. A login bound to an agent exists locally (else nothing else can pass).
  const auth0 = await loadAuth()
  if (!auth0 || !auth0.agentId) {
    checks.login = { ok: false, asserted: 'a login bound to an agent exists', reason: 'not_authenticated — run `login` first' }
    const f0 = { ok: false, skill: { name: SKILL_NAME, version: SKILL_VERSION }, checks, summary: 'Not logged in — run `login`, then `verify` again.' }
    process.stderr.write(JSON.stringify(withUpdateNotice(f0), null, 2) + '\n')
    process.exit(1)
  }
  checks.login = { ok: true, asserted: 'a login bound to an agent exists', value: { agent_id: auth0.agentId } }

  // 2. The server actually ACCEPTS the token and resolves this agent.
  let agentId = auth0.agentId
  let profile: api.AgentProfile | null = null
  try {
    const { auth, agentId: aid } = await requireBoundAgent() // refreshes if near expiry
    agentId = aid
    profile = await api.getAgentProfile(auth.accessToken, aid)
    checks.token_accepted = { ok: true, asserted: 'the server accepts the token and resolves this agent', value: { agent_id: aid, name: profile.name } }
  } catch (e) {
    checks.token_accepted = { ok: false, asserted: 'the server accepts the token and resolves this agent', reason: (e as api.ApiError).code ?? (e as Error).message }
  }

  // 3. The agent is presentable — a PUBLIC PROFILE is set. The private directive is
  //    OPTIONAL (a unified default applies if the owner doesn't set one), so it no
  //    longer gates readiness. Sharing a profile-less agent is the real footgun → warn.
  if (profile) {
    const ready = profile.profile_complete
    checks.profile_ready = {
      ok: true,
      asserted: 'a public profile is set, so the agent represents the owner',
      value: { profile_complete: profile.profile_complete, directive_set: profile.directive_set, is_new: profile.is_new },
      warning: ready ? undefined : 'this agent has no public profile — set one before sharing so friends meet a real persona, not a blank one',
    }
  } else {
    checks.profile_ready = { ok: true, skipped: true, asserted: 'a public profile is set', reason: 'skipped — token not accepted' }
  }

  // 4. THE key product assertion: the share link the owner hands out actually
  //    resolves to THIS agent (round-trip the public manifest a friend hits).
  const authNow = await loadAuth()
  if (authNow) {
    try {
      const shares = await api.listShares(authNow.accessToken)
      const mine = shares.find((s) => s.agent_id === agentId)
      if (!mine) {
        checks.share_resolves = { ok: true, skipped: true, asserted: 'the share link resolves to this agent', reason: 'not shared yet — run `share-self` when ready (nothing to verify)' }
      } else {
        const v = await verifyShareResolves(mine.invite.slug, mine.agent_name)
        const works = v.resolves && v.points_back
        checks.share_resolves = {
          ok: works,
          asserted: 'the share link/QR resolves to THIS agent (what a friend scans)',
          value: { slug: mine.invite.slug, share_url: shareUrlFor(mine.invite.slug), resolves: v.resolves, points_back: v.points_back },
          reason: works ? undefined : (v.reason ?? 'the share did not resolve to this agent'),
        }
      }
    } catch (e) {
      checks.share_resolves = { ok: false, asserted: 'the share link resolves to this agent', reason: (e as api.ApiError).code ?? (e as Error).message }
    }
  }

  // 5. Presence reachable (online vs paused). Informational — never fatal.
  if (authNow) {
    try {
      const p = await api.brainPresence(authNow.accessToken, agentId)
      checks.presence = { ok: true, asserted: 'the server reports this agent autonomous-reply mode', value: { mode: p.mode, online: p.online } }
    } catch (e) {
      checks.presence = { ok: true, asserted: 'the server reports this agent autonomous-reply mode', warning: `could not read presence: ${(e as api.ApiError).code ?? (e as Error).message}` }
    }
  }

  // (Outbound conversations are served server-side under the owner's login now — no
  //  per-connection tokens to health-check; `conversations` / `check` read them live.)

  const allOk = Object.values(checks).every((c) => c.ok)
  const warnings = Object.entries(checks).filter(([, c]) => c.warning).map(([k, c]) => `${k}: ${c.warning}`)
  const report = {
    ok: allOk,
    skill: { name: SKILL_NAME, version: SKILL_VERSION },
    checks,
    summary: allOk
      ? (warnings.length ? `All critical checks passed; ${warnings.length} warning(s) to mention to the owner.` : 'All checks passed — the agent is set up and reachable.')
      : 'One or more critical checks FAILED — fix these before relying on the agent (see each check\'s reason).',
    warnings: warnings.length ? warnings : undefined,
    next_step: allOk
      ? 'All good — tell the owner (in their language) their Siobac setup checks out end-to-end (login, profile, share link). Mention any `warnings` if present.'
      : "A check FAILED — tell the owner (in their language) something isn't working yet and you'll fix it. See each failed check's `reason`; fix before relying on the agent.",
  }
  if (allOk) ok(report)
  process.stderr.write(JSON.stringify(withUpdateNotice(report), null, 2) + '\n')
  process.exit(1)
}

// ── Setup — the first-run onboarding state machine ───────────────────────
// One explicit entry point for "where am I in setup, what's next" — instead of
// the agent inferring readiness from scattered login/share output. Returns an
// ordered checklist (login → name → profile → share) with each step's done
// state and the single next command. (The private directive is OPTIONAL — a unified
// default applies — so it is NOT a checklist step.) The agent gathers the content from
// the owner (e.g. via AskUserQuestion) and runs that command. Read-only.
export async function cmdSetup(_flags: Record<string, string | true>) {
  let auth = await loadAuth()
  // Portable token (#16): on an ephemeral-FS host there's no auth.json, but a non-rotating
  // token supplied via SIOBAC_TOKEN still authenticates. Resolve it so `setup` doesn't
  // falsely report "not logged in" and send the agent to re-login it doesn't need.
  if ((!auth || !auth.agentId) && (process.env.SIOBAC_TOKEN || process.env.OVOCLAW_TOKEN)) {
    try { auth = (await requireBoundAgent()).auth } catch { /* still not authed → fall through */ }
  }
  if (!auth || !auth.agentId) {
    ok({
      status: 'setup_incomplete',
      logged_in: false,
      complete: false,
      steps: [
        { step: 'login', done: false, label: 'Log in (bind this skill to your Siobac agent)', command: 'login' },
        { step: 'name', done: false, label: 'Confirm the agent\'s name', command: 'set-profile --name "…"' },
        { step: 'profile', done: false, label: 'Public profile (what others see)', command: 'set-profile --description "…"' },
        { step: 'share', done: false, label: 'Share (become reachable via QR/link)', command: 'share-self --confirmed' },
      ],
      next_action: 'login',
      next_step: 'Tell the owner (in their language) you\'ll get them set up on Siobac, starting with a quick login. Then run `login` (two-step: `login`, then `login --finish` after the owner approves), then set up in order — name → profile — then `share-self`. (Optional: private ground rules via `set-directive`; a sensible default applies if skipped.)',
    })
    return
  }
  // Refresh the session like every other command — don't read state with the raw
  // stored access token, which may be expired-but-refreshable (that produced a
  // false `setup_unknown` even though the login was fine).
  let agentId = auth.agentId
  let token = auth.accessToken
  try {
    const bound = await requireBoundAgent()
    agentId = bound.agentId
    token = bound.auth.accessToken
  } catch (e) {
    ok({
      status: 'setup_unknown', logged_in: true, agent_id: agentId,
      reason: `logged in, but could not refresh the session to read setup state (${(e as api.ApiError).code ?? (e as Error).message})`,
      next_step: "Logged in, but the session couldn't be refreshed to read setup state. Tell the owner (in their language) you'll retry, or they may need a quick re-login. Run `doctor` to check connectivity, or `login` again if the session expired, then `setup`.",
    })
    return
  }
  // Best-effort reads — if the server is unreachable, say so rather than guess.
  let profile: api.AgentProfile | null = null
  let shared = false
  let reachErr: string | undefined
  try {
    profile = await api.getAgentProfile(token, agentId)
    const shares = await api.listShares(token)
    shared = shares.some((s) => s.agent_id === agentId)
  } catch (e) {
    reachErr = (e as api.ApiError).code ?? (e as Error).message
  }
  if (!profile) {
    // not_found = the bound agent no longer exists (deleted). That's NOT a connectivity
    // blip — re-login/doctor won't help; the owner needs a different or fresh agent.
    if (reachErr === 'not_found' || reachErr === 'not_authenticated') {
      ok({
        status: 'agent_missing', logged_in: true, agent_id: agentId,
        reason: 'this login is bound to an agent that no longer exists (it was deleted).',
        next_step: "The agent this login was bound to no longer exists — it was deleted, so there's nothing to set up here. Tell the owner (in their language), then either create a new agent in the Siobac app, or run `login` again and pick a DIFFERENT agent to manage. Do NOT keep retrying `setup`/`doctor` — the agent is gone, not unreachable.",
      })
      return
    }
    ok({
      status: 'setup_unknown', logged_in: true, agent_id: agentId,
      reason: `logged in, but could not reach the server to read setup state (${reachErr})`,
      next_step: "Logged in, but Siobac is unreachable right now to read setup state. Tell the owner (in their language) you'll retry shortly. Run `doctor` to check connectivity, then `setup` again.",
    })
    return
  }
  // Name step: the server has no "name confirmed" flag (a new agent ships with an
  // auto-name), so confirmation is tracked locally (set by `set-profile --name`). An
  // EXISTING (non-new) agent was already designed, so treat its name as confirmed.
  const bound = await loadBoundAgent()
  const nameConfirmed = !profile.is_new || !!bound?.nameConfirmedAt
  const steps = [
    { step: 'login', done: true, label: 'Logged in' },
    { step: 'name', done: nameConfirmed, label: 'Confirm the agent\'s name', command: 'set-profile --name "…"' },
    { step: 'profile', done: profile.profile_complete, label: 'Public profile (what others see)', command: 'set-profile --description "…"' },
    { step: 'share', done: shared, label: 'Shared (reachable via QR/link)', command: 'share-self --confirmed' },
  ]
  const next = steps.find((s) => !s.done)
  ok({
    status: next ? 'setup_incomplete' : 'setup_complete',
    logged_in: true, agent_id: agentId, complete: !next,
    steps,
    next_action: next?.command ?? null,
    next_step: next
      ? `Next step — ${next.label}. Ask the owner for the content (AskUserQuestion is good for structured choices), then run \`${next.command}\`. Remaining steps follow in order; re-run \`setup\` to recheck.`
      : 'Setup complete — tell the owner (in their language) they are all set: logged in, profile set, and shared. (Optional: fine-tune private ground rules with `set-directive`; a sensible default applies otherwise.) Run `verify` anytime to confirm it all still works end-to-end.',
  })
}

