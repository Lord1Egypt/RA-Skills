#!/usr/bin/env node
import { promises as fs, constants as fsConstants } from 'node:fs'
import { platform, arch } from 'node:os'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'
import {
  parseArgs,
  requireString,
  optionalString,
  optionalNonNegInt,
  CliError,
} from './argparse.js'
import * as api from './api.js'
import {
  stateDir,
  authFilePath,
  ensureAgentBinding,
  loadAuth,
  saveAuth,
  clearAuth,
  loadBoundAgent,
  saveBoundAgent,
  markNameConfirmed,
  savePendingLogin,
  loadPendingLogin,
  clearPendingLogin,
  claimLoginLock,
  releaseLoginLock,
  resolvedAgentKey,
  pinAgentKey,
  isAuthFileWriteable,
  migrateLegacyState,
  bumpDiscoverSkips,
  resetDiscoverSkips,
  type AgentBinding,
  type AuthState,
} from './state.js'
import { parseInvite } from './invite.js'
import { SKILL_NAME, SKILL_VERSION } from './version.js'


import { cmdDoctor, cmdVerify, cmdSetup } from './diagnostics.js'
import { cmdGuide, cmdHelp } from './guide.js'
import {
  cmdGoOnline, cmdBrainHandback, cmdBrainStatus, cmdOwnerChannel,
  cmdBrainPending, cmdBrainResolve, cmdBrainOutreach, cmdBrainInterrupt,
  cmdDismiss,
} from './brain.js'
import {
  ok, fail, withUpdateNotice, skillDir, updateInstruction,
  requireAuth, requireBoundAgent, isConfirmed, needsConfirmation,
  shareUrlFor, qrUrlFor, qrMarkdownFor, connectCodeFor, verifyShareResolves,
} from './runtime.js'

// ── Real commands ────────────────────────────────────────────────────

// Two-step login. `login` (initiate) requests a device code, stashes it, and
// returns the approval URL immediately — it does NOT poll. `login --finish`,
// run ONLY after the user says they approved, polls once and saves the token.
// This deliberately removes the old blocking poll loop so the agent never
// silently re-drives login (the cause of the re-login loop on hosts without a
// stable state folder).
function wantsFinish(flags: Record<string, string | true>): boolean {
  const v = flags['finish']
  return v === true || v === 'true' || v === ''
}

// qclaw / workbuddy let the owner pick the underlying LLM, and Siobac runs best on
// Deepseek-V4-Pro. That suggestion must be its OWN first step, BEFORE the login link —
// not surfaced alongside it (showing both at once buried the login). So on those hosts
// the FIRST `login` returns ONLY the model-check step and mints no device code; the agent
// handles the suggestion (or skips it silently), then re-runs `login --model-checked` to
// start the real login. This flag marks that second call.
function isModelSuggestionPlatform(): boolean {
  const plat = (process.env.SIOBAC_PLATFORM ?? process.env.OVOCLAW_PLATFORM ?? '').trim().toLowerCase()
  return plat === 'qclaw' || plat === 'workbuddy'
}
function modelChecked(flags: Record<string, string | true>): boolean {
  const v = flags['model-checked'] ?? flags['continue']
  return v === true || v === 'true' || v === ''
}

async function cmdLogin(flags: Record<string, string | true>) {
  if (wantsFinish(flags)) return cmdLoginFinish(flags)

  // Idempotent while an approval is still live: if a non-expired pending login
  // already exists, RE-SHOW its link instead of minting a new device code. A new
  // code would invalidate the link the user is busy approving — the "new link every
  // time" loop. The user just approves THIS link, then runs `login --finish`.
  const live = await loadPendingLogin()
  if (live && live.verificationUriComplete && Date.now() < new Date(live.expiresAt).getTime()) {
    ok({
      status: 'awaiting_user_approval',
      reused: true,
      verification_uri_complete: live.verificationUriComplete,
      verification_uri: live.verificationUri,
      user_code: live.userCode,
      message:
        'A login is ALREADY in progress — do not start a new one. Show the user THIS same link and have them approve it (sign in / sign up, pick the agent, approve).',
      next_step:
        'After the user confirms they approved, run `login --finish` once. Do NOT re-run `login` — it will not change anything while this link is live.',
    })
  }

  // ── Step 0 (qclaw/workbuddy only): the model suggestion is its OWN first step.
  // Return JUST the model-check instruction and mint NO device code / show NO link, so
  // the suggestion and the login never appear at the same time. After the user responds
  // (or immediately, if it doesn't apply and the agent skips it), the agent re-runs
  // `login --model-checked` and falls through to the real login below.
  if (isModelSuggestionPlatform() && !modelChecked(flags)) {
    ok({
      status: 'model_check_first',
      message:
        'FIRST STEP — before any login link: check which model YOU are running. ' +
        'If it is NOT Deepseek-V4-Pro, SUGGEST switching ONCE — a SUGGESTION, not a requirement — with exactly two options ' +
        '("1. ✅ I\'ve already switched" · "2. 👍 Keep the current model"); do NOT name the platform in the owner-facing line ' +
        '(just "I run best on Deepseek-V4-Pro…"). If you are ALREADY on Deepseek-V4-Pro, or the owner already decided this session, ' +
        'SKIP this silently. See references/platform-hints.md → qclaw/workbuddy.',
      next_step:
        'Do NOT show a login link in this step — there is none yet. After the user has responded to the model suggestion ' +
        '(or right away if you skipped it because it did not apply), run `login --model-checked` to start the actual login.',
    })
  }

  // ── Step 1: initiate. Request a device_code, surface the verification URL to
  // the user, stash the code, and STOP. The server-side /oauth/* endpoints
  // landed in phase 2; if a deployment predates them this degrades cleanly to
  // code:server_not_ready.
  //
  // Agent pre-select hint, in priority order:
  //   1. --agent <name-or-id> — the owner told us which agent to share. The
  //      approval page resolves it by id or unique name and auto-selects it.
  //   2. the agent we bound to on a prior login (agent.json) — so every re-login
  //      re-binds the same identity without re-choosing.
  // Either way it's only a hint: an unknown/ambiguous value is ignored
  // server-side and the page falls back to the pick-or-create chooser.
  const explicitAgent = optionalString(flags, 'agent')
  const bound = await loadBoundAgent()
  const agentHint = explicitAgent ?? bound?.agentId

  // Atomically claim the mint slot BEFORE the network call. This closes the
  // TOCTOU window in the guard above (load → mint → save): if a second `login`
  // raced in there, both minted a device code and the second's save clobbered
  // the first's record, orphaning a code and handing the user two rival links
  // (the prod "fail to login"). If the claim fails, a login is already in flight
  // — re-show its link rather than minting a competitor.
  const claimed = await claimLoginLock()
  if (!claimed) {
    const inflight = await loadPendingLogin()
    if (inflight && inflight.verificationUriComplete && Date.now() < new Date(inflight.expiresAt).getTime()) {
      return ok({
        status: 'awaiting_user_approval',
        reused: true,
        verification_uri_complete: inflight.verificationUriComplete,
        verification_uri: inflight.verificationUri,
        user_code: inflight.userCode,
        message: 'A login is ALREADY being set up — do not start another. Show the user THIS link and have them approve it.',
        next_step: 'After the user confirms they approved, run `login --finish` once. Do NOT re-run `login`.',
      })
    }
    return ok({
      status: 'login_in_progress',
      message: 'A login was JUST started in another run and is still being set up. Do NOT mint another.',
      next_step: 'Wait a moment, then run `login` once more to get the link (or `login --finish` if the user already approved).',
    })
  }

  let codeResp: api.DeviceCodeResponse
  try {
    try {
      codeResp = await api.requestDeviceCode(undefined, agentHint)
    } catch (e) {
      const apiErr = e as api.ApiError
      if (apiErr.code === 'server_not_ready') {
        throw api.makeApiError(
          'server_not_ready',
          'login: OAuth device flow endpoints not deployed on the server yet (phase 2 work). The skill is ready; the server side ships next.',
        )
      }
      throw e
    }

    // Persist the device code in this agent's state dir so `login --finish` can
    // poll it from a separate process.
    await savePendingLogin({
      deviceCode: codeResp.device_code,
      interval: codeResp.interval,
      expiresAt: new Date(Date.now() + codeResp.expires_in * 1000).toISOString(),
      agentHint,
      startedAt: new Date().toISOString(),
      // Record the resolved state key so `login --finish` saves the token to the
      // SAME per-agent folder even if it runs from a different working directory.
      agentKey: resolvedAgentKey(),
      verificationUriComplete: codeResp.verification_uri_complete,
      verificationUri: codeResp.verification_uri,
      userCode: codeResp.user_code,
    })
  } finally {
    // Release once the pending record is written (or the mint failed); the
    // pending file itself is the idempotency record for the rest of the window.
    await releaseLoginLock()
  }

  // The qclaw/workbuddy model suggestion already happened as its OWN first step
  // (Step 0 above) — so it is NOT repeated here; the login link stands alone.

  // Show the user the verification link. Prefer verification_uri_complete —
  // opening it pre-fills the code, so the user clicks once and never types.
  // verification_uri + user_code are the manual fallback (different device).
  ok({
    status: 'awaiting_user_approval',
    verification_uri_complete: codeResp.verification_uri_complete,
    verification_uri: codeResp.verification_uri,
    user_code: codeResp.user_code,
    expires_in_seconds: codeResp.expires_in,
    message:
      'Show the user verification_uri_complete and tell them to click it — the code is pre-filled, no manual entry. ' +
      '(Fallback: open verification_uri and enter user_code.) On that page they sign IN — or, if they have no Siobac account yet, SIGN UP right there (a new account creates an agent automatically) — then pick which agent to share and approve.',
    // The whole point of the two-step flow: do NOT poll, do NOT re-run `login`.
    next_step:
      'WAIT for the USER to tell you they finished approving on the page. ONLY THEN run `login --finish` once to complete it. ' +
      'Do NOT poll, and do NOT re-run `login` on your own — if `login --finish` says still-pending, ask the user again and run `login --finish` only after they confirm.',
  })
}

async function cmdLoginFinish(_flags: Record<string, string | true>) {
  const pending = await loadPendingLogin()
  if (!pending) {
    throw new CliError(
      'No pending login found. If you have NOT started a login yet, run `login` once and have the user approve the link. ' +
      'If you JUST ran `login` and the user approved, the login state did not persist between commands on this host — ' +
      'set a stable SIOBAC_AGENT_KEY (e.g. SIOBAC_AGENT_KEY=my-agent), then run `login` and `login --finish` again. ' +
      'Do NOT loop `login` on your own — that mints a fresh link each time and never completes.',
    )
  }
  // Pin the key recorded at login time so the token saves to the SAME per-agent
  // folder even when `login --finish` runs from a different working directory.
  if (typeof pending.agentKey === 'string') pinAgentKey(pending.agentKey)
  if (Date.now() >= new Date(pending.expiresAt).getTime()) {
    await clearPendingLogin()
    throw api.makeApiError(
      'expired_token',
      'the approval link expired before it was finished. Run `login` again to get a fresh link.',
    )
  }

  let token: api.DeviceTokenResponse
  try {
    token = await api.pollDeviceToken(pending.deviceCode)
  } catch (e) {
    const code = (e as api.ApiError).code
    if (code === 'authorization_pending' || code === 'slow_down') {
      // Not approved yet. Return a SUCCESS (exit 0) so the agent doesn't treat
      // it as a failure and loop — it should just wait for the user.
      ok({
        status: 'awaiting_user_approval',
        pending: true,
        message: 'The user has not finished approving on the login page yet.',
        next_step:
          'Ask the user to complete the approval on the login page (sign in / sign up, pick the agent, approve). ' +
          'Once they CONFIRM they have, run `login --finish` again. Do not loop on your own.',
      })
    }
    if (code === 'access_denied') {
      await clearPendingLogin()
      throw api.makeApiError('access_denied', 'the login was denied on the approval page. Run `login` again if that was a mistake.')
    }
    if (code === 'expired_token') {
      await clearPendingLogin()
      throw api.makeApiError('expired_token', 'the approval link expired. Run `login` again for a fresh one.')
    }
    throw e
  }

  // Approved — persist the token, clear the pending code, then onboard.
  const auth: AuthState = {
    accessToken: token.access_token,
    tokenType: token.token_type,
    expiresAt: new Date(Date.now() + token.expires_in * 1000).toISOString(),
    refreshToken: token.refresh_token,
    scope: token.scope,
    ovoclawAccountId: token.account_id,
    agentId: token.agent_id ?? undefined,
    loggedInAt: new Date().toISOString(),
  }
  await saveAuth(auth)
  await clearPendingLogin()
  const agentName = token.agent_name ?? undefined
  // Remember which agent this login bound to, so the next `login` hints it and
  // auto-confirms the same identity. Survives logout / token expiry.
  if (auth.agentId) {
    await saveBoundAgent({ agentId: auth.agentId, agentName, boundAt: new Date().toISOString() })
  }
  // First-run onboarding: load the agent's profile + directive (best-effort).
  let prof: api.AgentProfile | null = null
  try {
    if (auth.agentId) prof = await api.getAgentProfile(auth.accessToken, auth.agentId)
  } catch { /* ignore */ }
  // An already-DESIGNED (non-new) agent has a confirmed name — record that locally so a
  // fresh state dir on another machine doesn't re-prompt the name step for it.
  if (prof && !prof.is_new) await markNameConfirmed(agentName)
  const rememberLabel = agentName ?? auth.agentId
  const binding = await ensureAgentBinding(false)
  // Ephemeral-FS hosts (doubao): secure persistence NOW, automatically, so the owner
  // never hits the wasteful "log in → filesystem wiped → expired → re-login" round-trip.
  // We mint the portable (non-rotating) token AS PART OF login and hand it to the AGENT to
  // memorize + re-inject as SIOBAC_TOKEN — silently. The owner is NEVER told to run a command
  // or manage a token; they just see "logged in". Only on a genuine fresh login: if
  // SIOBAC_TOKEN is already in play the agent is re-injecting an existing one — don't re-mint.
  const plat = (process.env.SIOBAC_PLATFORM ?? process.env.OVOCLAW_PLATFORM ?? '').trim().toLowerCase()
  const alreadyPortable = !!(process.env.SIOBAC_TOKEN ?? process.env.OVOCLAW_TOKEN ?? '').trim()
  let portableToken: string | null = null
  let portableLogin: string | null = null
  if (plat === 'doubao' && !alreadyPortable) {
    try {
      const pt = await api.issuePortableToken(auth.accessToken)
      portableToken = pt.portable_token
      portableLogin = 'AGENT-ONLY — do NOT explain tokens to the owner, do NOT show this as a command to run. This host wipes its filesystem between runs, so the login is already secured for you: MEMORIZE portable_token and pass it as the SIOBAC_TOKEN env var on EVERY future run (re-inject silently after any idle gap, then retry — never ask the owner to re-login). The owner only needs to hear that login succeeded.'
    } catch { /* non-fatal — login still succeeded; agent can issue-portable-login later if needed */ }
  }
  ok({
    status: 'authenticated',
    portable_token: portableToken,   // doubao only: a non-rotating login the agent re-injects as SIOBAC_TOKEN (null elsewhere)
    portable_login: portableLogin,   // AGENT-ONLY handling note (silent; never shown/explained to the owner)
    scope: auth.scope,
    expires_at: auth.expiresAt,
    account_id: auth.ovoclawAccountId,
    agent_id: auth.agentId,
    agent_name: agentName ?? null,
    note: 'This login is bound to a single agent. All commands act as that agent only.',
    state_binding: { key: binding.key || null, source: binding.source, binding_file: binding.binding_file, state_dir: binding.state_dir },
    profile: prof ? { name: prof.name, description: prof.description, avatar_url: prof.avatar_url } : null,
    directive: prof ? prof.directive : '',
    agent_is_new: prof ? prof.is_new : false,
    setup: prof
      ? (prof.is_new
          ? { state: 'new', guidance: 'New user — agent not set up yet. Lead with the simple product Welcome intro (scripts → Step 0b), NOT setup. Only walk setup (name → profile) if the owner chooses to start; the private directive is OPTIONAL (a default applies).' }
          : { state: 'existing', profile_complete: prof.profile_complete, directive_set: prof.directive_set, guidance: 'This agent already has a profile (shown above). Show it to the owner and ASK whether to update it. (A private directive is optional — offer set-directive only if they want to fine-tune behavior.)' })
      : null,
    auto_go_online: true,
    next_step: prof
      ? (prof.is_new
          ? 'This is a NEW user (agent_is_new) — first time here. Do NOT show the feature menu and do NOT push setup yet (that overwhelms a new user). FIRST relay the simple product INTRO from scripts → "Step 0b — Welcome (first-time user)": one short paragraph on what Siobac is + exactly two options (Let\'s go start · Tell me more), in the owner\'s language. When they proceed ("Let\'s go start" or after "Tell me more"), go to the HOME hub (scripts → "Step 0c") so they pick what to do — do NOT say they are "online" (nothing is shared yet); use the hub\'s not-yet-shared variant. Setup (name → profile, Step 1) is JUST-IN-TIME — it runs only when they pick Share (`share-self` gate) or Find, and needs just those TWO steps (the private directive is OPTIONAL — a default applies). Once shared, the server answers friends automatically (server-driven, references/brain.md).'
          : 'Returning user (already designed). Relay the HOME hub from scripts → "Step 0c — post-login hub": the short numbered menu (what\'s new · share · reach out · find people · manage). Do NOT dump the profile/directive — they can pick "manage" to update. The server already answers friends in character and escalates commitments (server-driven, references/brain.md); `pause` (manual) / `go-online` (resume) steer it; escalations surface via `owner-channel` / `brain-pending`.')
      : 'Logged in. If this is a new user (agent_is_new), relay the simple product intro (scripts → Step 0b — Welcome); otherwise relay the home hub (scripts → Step 0c).',
    remember: rememberLabel
      ? `You are now sharing the Siobac agent "${rememberLabel}" (id ${auth.agentId}). ` +
        `Record this in your durable memory as your Siobac agent. Next time you log in, ` +
        `pass it as \`login --agent "${rememberLabel}"\` to re-bind the same agent without the picker.`
      : undefined,
  }, true)   // home screen → carry the skill-update notice (only place it surfaces)
}

async function cmdLogout() {
  await clearAuth()
  ok({ ok: true, status: 'logged_out', auth_file_path: authFilePath() })
}

// issue-portable-login (#16): mint a non-rotating 7-day token for ephemeral-workspace
// hosts (whose FS is wiped between runs). The agent MEMORIZES it once and supplies it
// every run via SIOBAC_TOKEN — no durable auth.json needed. Requires a normal login first.
async function cmdIssuePortableLogin(_flags: Record<string, string | true>) {
  const { auth } = await requireBoundAgent()
  const r = await api.issuePortableToken(auth.accessToken)
  const days = Math.round(r.portable_expires_in / 86400)
  ok({
    status: 'portable_login_issued',
    portable_token: r.portable_token,
    expires_in_days: days,
    agent_name: r.agent_name ?? null,
    next_step:
      `A PORTABLE login is minted for ${r.agent_name ?? 'this agent'} — a non-rotating token valid ${days} days. ` +
      `This is for an EPHEMERAL-workspace host (the filesystem is wiped between runs, so a normal login can't persist). ` +
      `Tell the owner you'll stay logged in now, and DO THIS: (1) SAVE the token value in your DURABLE memory (it does NOT change); ` +
      `(2) on EVERY run, before any siobac command, make it available as the SIOBAC_TOKEN environment variable (or, if you can only write files, write \`{"refreshToken":"<token>","tokenType":"Bearer","expiresAt":"1970-01-01T00:00:00Z"}\` to ~/.siobac/auth.json). ` +
      `The skill then mints a fresh access token in-memory each run — no re-login. Re-run \`issue-portable-login\` after ${days} days (or run \`revoke-portable\` to kill it). ` +
      `SECURITY: treat this token like a password — it's a bearer credential valid until it expires or is revoked. NEVER show it to anyone the agent talks to. See \`references/platform-hints.md\`.`,
  })
}

// revoke-portable (#16): kill all live portable tokens for this agent (re-issue, or a leak).
async function cmdRevokePortable(_flags: Record<string, string | true>) {
  const { auth } = await requireBoundAgent()
  const r = await api.revokePortableToken(auth.accessToken)
  ok({
    status: 'portable_revoked',
    revoked: r.revoked,
    next_step: r.revoked > 0
      ? `Revoked ${r.revoked} portable login(s) — any memorized SIOBAC_TOKEN will stop working immediately. Tell the owner in plain words; if they still need portable access, run \`issue-portable-login\` for a fresh one.`
      : `No active portable logins to revoke. Tell the owner there was nothing to revoke.`,
  })
}

// ── Owner-side commands (wired to apps/server in phase 3) ──

// Parse a tri-state --requires-approval flag:
//   (absent)                  → undefined (server default: gated/approval-on)
//   --requires-approval       → true
//   --requires-approval=false → false  (open invite, connects immediately)
function parseRequiresApproval(flags: Record<string, string | true>): boolean | undefined {
  const v = flags['requires-approval']
  if (v === undefined) return undefined
  if (v === true) return true
  return !(v === 'false' || v === '0' || v === 'no')
}



async function cmdShareSelf(flags: Record<string, string | true>) {
  optionalString(flags, 'description') // accepted for forward-compat; not used by the invite endpoint
  // Approval policy. `explicit` is the owner's EXPLICIT choice (undefined if no
  // flag passed). NEW shares default to AUTO-ACCEPT (no approval) so the first
  // connection just works; the owner can require approval anytime with `set-approval --on`.
  const explicit = parseRequiresApproval(flags)
  const createApproval = explicit ?? false // default: auto-accept
  const { auth, agentId } = await requireBoundAgent()
  // ONE STEP. The owner has already said yes in conversation — the share flow in
  // scripts-en/cn.md has the agent ASK first and OFFER a custom connect code in the
  // SAME breath — so publishing happens directly: no `--confirmed` round-trip and no
  // separate post-share "customize your code" step. If the owner chose a custom handle
  // it arrives as `--code` and is applied as part of this single publish.
  const rawCode = optionalString(flags, 'code')
  const desiredCode = rawCode ? rawCode.replace(/@siobac(\.com)?$/i, '').trim() : undefined

  // Design awareness (NON-blocking): surface — don't gate — a missing public profile.
  // The scripts run profile setup just-in-time before share; this is only a backstop
  // note so a bare agent going live is at least flagged in the result.
  const design = await api.getAgentProfile(auth.accessToken, agentId).catch(() => null)
  const undesigned = design ? !design.profile_complete : false

  let invite = await api.createShare(auth.accessToken, agentId, { requires_approval: createApproval })
  // createShare is idempotent and IGNORES requires_approval on an EXISTING invite.
  // Only change an existing invite's setting when the owner EXPLICITLY chose one.
  if (explicit !== undefined && invite.requires_approval !== explicit) {
    invite = await api.updateShareApproval(auth.accessToken, agentId, explicit)
  }
  // Apply the owner's chosen connect code in the SAME step. A taken/invalid code does
  // NOT block the share — the agent is already live on the auto code and can pick
  // another later with `set-code`; we just report it so the agent can re-ask.
  let codeRejected: { attempted: string; reason: 'code_taken' | 'invalid' } | undefined
  if (desiredCode) {
    try {
      invite = await api.setConnectCode(auth.accessToken, agentId, desiredCode)
    } catch (e) {
      const err = e as api.ApiError
      if (err.status === 409 || err.status === 400) {
        codeRejected = { attempted: connectCodeFor(desiredCode.toLowerCase()), reason: err.status === 409 ? 'code_taken' : 'invalid' }
      } else throw e
    }
  }
  // VERIFY before claiming success: round-trip the slug through the public manifest so
  // we KNOW the QR/link resolves to this agent before handing it to the owner.
  const verified = await verifyShareResolves(invite.slug)
  const linkWorks = verified.resolves && verified.points_back
  ok({
    status: linkWorks ? 'shared' : 'shared_unverified',
    agent_id: agentId,
    // The human-facing handle: `<code>@siobac`, like an email. People can type this
    // OR scan the QR to reach the agent. It is case-insensitive.
    connect_code: connectCodeFor(invite.slug),
    invite: {
      id: invite.id,
      slug: invite.slug,
      requires_approval: invite.requires_approval,
      created_at: invite.created_at,
    },
    share_url: shareUrlFor(invite.slug),
    qr_url: qrUrlFor(invite.slug),
    qr_markdown: qrMarkdownFor(invite.slug),
    // Programmatic proof the link resolves (not just that create returned 200).
    verified: { share_resolves: verified.resolves, points_back: verified.points_back, reason: verified.reason },
    design_warning: undesigned
      ? "No public profile yet — friends would reach an agent that doesn't know who it is. Tell the owner and offer to set one now (set-profile)."
      : undefined,
    code_rejected: codeRejected
      ? `The custom code ${codeRejected.attempted} was ${codeRejected.reason === 'code_taken' ? 'already taken' : 'not valid (use 3–15 letters/numbers)'} — you're LIVE on ${connectCodeFor(invite.slug)} for now. Tell the owner; if they want, ask for another and run \`set-code --code "<choice>"\`.`
      : undefined,
    note: linkWorks
      ? `DISPLAY THE QR INLINE: render it as an image so the user sees a scannable QR, not a link — drop the ready-made \`qr_markdown\` straight into your reply (it is \`![](qr_url)\`). Also give \`share_url\` as a copyable link, AND show the \`connect_code\` (${connectCodeFor(invite.slug)}) — a short email-like handle people can type to reach this agent. Only if your platform cannot render images, fall back to showing \`qr_url\` as a plain link. The link was VERIFIED to resolve to this agent.`
      : `CAUTION: the share was created but did NOT verify — the link did not resolve back to this agent (${verified.reason ?? 'unknown'}). Do NOT tell the owner it is ready. Re-run \`share-self\`, check connectivity with \`doctor\`, or run \`verify\` for detail before handing out the QR.`,
    // Only when the owner did NOT already pick a code in this step — the customization
    // is normally folded into the single share step (the agent offers it up front).
    customize_code: (!desiredCode && linkWorks)
      ? `The connect code is auto-generated (${connectCodeFor(invite.slug)}). If the owner would prefer a memorable one, run \`set-code --code "<their choice>"\` (3–15 letters/numbers) — otherwise leave it.`
      : undefined,
    next_step: linkWorks
      ? 'If you have not already, help the owner set up their agent so others understand who they are: (1) confirm the NAME (`set-profile --name "…"`); (2) PUBLIC profile (`set-profile --description "…"`). That is all that is needed — the agent already replies in character with sensible default ground rules. OPTIONAL: private ground rules with `set-directive --content "…"` (skippable). Then, when a friend connects, use `recall` before replying and `remember` after (see Step 6 in references/guide.md, or run `guide --step serve_incoming`).'
      : 'Share verification FAILED — resolve that first. Run `verify` for the full check, or `doctor` for connectivity, then `share-self` again. Do not surface the QR as working until `verified.share_resolves` and `verified.points_back` are both true.',
  })
}

async function cmdListShares() {
  const auth = await requireAuth()
  const shares = await api.listShares(auth.accessToken)
  // Add a scannable qr_url alongside each share's slug.
  const withQr = shares.map((s) => ({
    ...s,
    qr_url: s.invite?.slug ? qrUrlFor(s.invite.slug) : null,
    qr_markdown: s.invite?.slug ? qrMarkdownFor(s.invite.slug) : null,
  }))
  ok({
    status: 'ok',
    count: withQr.length,
    shares: withQr,
    next_step: withQr.length === 0
      ? 'No active shares. Tell the owner (in their language) they are not shared yet; run `share-self` to publish a QR/link.'
      : "To show a share to the owner, render its `qr_markdown` inline as an IMAGE (it is `![](qr_url)`) so they see a scannable QR, plus `share_url` as a copyable link — never just the raw URL. To change who-can-connect use `set-approval` (same link); to replace it use `regenerate-share`.",
  })
}

async function cmdRevokeShare(flags: Record<string, string | true>) {
  // CONSENT GATE — revoking kills the link/QR the owner already handed out; confirm.
  if (!isConfirmed(flags)) {
    needsConfirmation(
      'revoke-share',
      { will: 'Revoke this agent\'s share. The current link/QR stops working for anyone who has it. People ALREADY connected stay connected. To be reachable again you\'d run `share-self` for a NEW link.' },
      'Revoke your share link so the current QR/link stops working? (people already connected stay connected)',
      'revoke-share --confirmed',
    )
  }
  const { auth, agentId } = await requireBoundAgent()
  const result = await api.revokeShare(auth.accessToken, agentId)
  ok({
    status: 'revoked', agent_id: agentId, ...result,
    next_step: 'Share revoked — tell the owner (in their language) their old link/QR no longer works; people already connected are unaffected. To become reachable again, run `share-self` for a fresh link.',
  })
}

// Toggle whether NEW connections need the owner's approval. Changes the setting
// IN PLACE — the existing share link/QR is UNCHANGED (never regenerate the slug
// just to flip this). --on = require approval, --off = auto-accept.
async function cmdSetApproval(flags: Record<string, string | true>) {
  const truthy = (v: unknown) => v === true || v === 'true' || v === ''
  let requiresApproval: boolean | undefined
  if (truthy(flags['off'])) requiresApproval = false
  else if (truthy(flags['on'])) requiresApproval = true
  else requiresApproval = parseRequiresApproval(flags) // tri-state --requires-approval[=false]
  if (requiresApproval === undefined) {
    throw new CliError(
      'set-approval needs --on (require your approval before someone connects) or --off (auto-accept). Either way your share link/QR is unchanged.',
    )
  }
  const { auth, agentId } = await requireBoundAgent()
  const invite = await api.updateShareApproval(auth.accessToken, agentId, requiresApproval)
  ok({
    status: 'approval_updated',
    agent_id: agentId,
    requires_approval: invite.requires_approval,
    slug: invite.slug,
    share_url: shareUrlFor(invite.slug),
    next_step: invite.requires_approval
      ? "Tell the owner (in their language) that NEW connection requests now need their OK before anyone can talk to the agent — they'll appear via `requests` / `check`. Their existing share link/QR is UNCHANGED; don't re-share or regenerate it."
      : "Tell the owner (in their language) that new connections now AUTO-ACCEPT (no approval needed). Their existing share link/QR is UNCHANGED; don't re-share or regenerate it.",
  })
}

async function cmdRegenerateShare(flags: Record<string, string | true>) {
  // CONSENT GATE — regenerating rotates the slug and REVOKES every old link/QR.
  if (!isConfirmed(flags)) {
    needsConfirmation(
      'regenerate-share',
      { will: 'Mint a NEW share link/QR and REVOKE the old one — every link/QR you already handed out STOPS working. People already connected are unaffected. (To change who-can-connect WITHOUT a new link, use `set-approval` instead.)' },
      'Replace your share link with a new one? Every old QR/link will stop working (existing connections stay).',
      'regenerate-share --confirmed',
    )
  }
  const requiresApproval = parseRequiresApproval(flags)
  const { auth, agentId } = await requireBoundAgent()
  const invite = await api.regenerateShare(auth.accessToken, agentId, { requires_approval: requiresApproval })
  ok({
    status: 'regenerated',
    agent_id: agentId,
    invite: {
      id: invite.id,
      slug: invite.slug,
      requires_approval: invite.requires_approval,
      created_at: invite.created_at,
    },
    share_url: shareUrlFor(invite.slug),
    qr_url: qrUrlFor(invite.slug),
    qr_markdown: qrMarkdownFor(invite.slug),
    note: 'DISPLAY THE QR INLINE: render `qr_markdown` as an image (it is `![](qr_url)`) so the user sees a scannable QR, with `share_url` as the copyable link — do not just paste the URL. Fall back to the plain `qr_url` link only if your platform cannot render images. The previous slug is now revoked; existing connections are unaffected, but old share links / QR codes stop working.',
  })
}

// Set or change the agent's custom connect code (the `<code>@siobac` handle).
// Used both when the owner customises on first share AND to change it later.
// Updated IN PLACE: people already connected keep working; the OLD `<code>@siobac`
// stops resolving for new connects. There is only ever ONE active code.
async function cmdSetConnectCode(flags: Record<string, string | true>) {
  const raw = optionalString(flags, 'code')
  if (!raw) {
    throw new CliError('set-code needs --code "<your choice>" — 3–15 letters or numbers (case-insensitive), e.g. --code "alex". People reach the agent by typing `<code>@siobac` or scanning the QR.')
  }
  // Strip a typed `@siobac` suffix so `--code "alex@siobac"` works too.
  const desired = raw.replace(/@siobac(\.com)?$/i, '').trim()
  const { auth, agentId } = await requireBoundAgent()
  // CONSENT/EXPECTATION GATE — changing an EXISTING code breaks the old handle for
  // anyone who saved it. Confirm before changing (first-time set needs no gate
  // since nothing was handed out yet, but the agent drives that via the offer).
  let current: string | null = null
  try {
    const active = await api.getActiveInvite(auth.accessToken, agentId)
    current = active?.invite?.slug ?? null
  } catch { /* no active invite yet — first-time set */ }
  const isChange = !!current && current.toLowerCase() !== desired.toLowerCase()
  if (isChange && !isConfirmed(flags)) {
    needsConfirmation(
      'set-code',
      { will: `Change the connect code from ${connectCodeFor(current!)} to ${connectCodeFor(desired.toLowerCase())}. People already connected are UNAFFECTED, but anyone who saved the OLD code can no longer reach the agent with it. There is only one active code.` },
      `Change your connect code to ${connectCodeFor(desired.toLowerCase())}? Your old ${connectCodeFor(current!)} will stop working for new connections (people already connected stay connected).`,
      `set-code --code "${desired}" --confirmed`,
    )
  }
  try {
    const invite = await api.setConnectCode(auth.accessToken, agentId, desired)
    ok({
      status: 'code_set',
      agent_id: agentId,
      connect_code: connectCodeFor(invite.slug),
      previous_code: current && current.toLowerCase() !== invite.slug.toLowerCase() ? connectCodeFor(current) : undefined,
      invite: { id: invite.id, slug: invite.slug, requires_approval: invite.requires_approval },
      share_url: shareUrlFor(invite.slug),
      qr_url: qrUrlFor(invite.slug),
      qr_markdown: qrMarkdownFor(invite.slug),
      next_step: `Tell the owner (in their language) their connect code is now ${connectCodeFor(invite.slug)} — people can type that (case doesn't matter) or scan the QR to reach them.${current && current.toLowerCase() !== invite.slug.toLowerCase() ? ` The old ${connectCodeFor(current)} no longer works for NEW connections; anyone already connected is unaffected.` : ''}`,
    })
  } catch (e) {
    const err = e as api.ApiError
    // 409 = taken, 400 = invalid format / reserved. Return a clean, re-promptable
    // result (not a hard failure) so the agent simply asks the owner for another.
    if (err.status === 409 || err.status === 400) {
      const taken = err.status === 409
      ok({
        status: 'code_rejected',
        agent_id: agentId,
        attempted: connectCodeFor(desired.toLowerCase()),
        reason: taken ? 'code_taken' : 'invalid',
        message: taken
          ? `${connectCodeFor(desired.toLowerCase())} is already taken — ask the owner for a different code.`
          : `"${desired}" isn't a valid code. It must be 3–15 letters or numbers (no spaces/symbols), and can't be a reserved word. Ask the owner for another.`,
        next_step: 'Ask the owner for a different connect code, then run `set-code --code "<new choice>"` again.',
      })
    }
    throw e
  }
}

async function cmdListConnections(flags: Record<string, string | true>) {
  const statusFilter = optionalString(flags, 'status')
  const { auth, agentId } = await requireBoundAgent()
  let conns = await api.listConnections(auth.accessToken, agentId)
  if (statusFilter) conns = conns.filter((c) => c.status === statusFilter)
  ok({
    status: 'ok',
    agent_id: agentId,
    status_filter: statusFilter ?? null,
    count: conns.length,
    connections: conns,
    next_step: conns.length === 0
      ? 'No connections yet. Tell the owner (in their language) nobody has connected on this list.'
      : "These are the people connected to the owner's agent. Summarize for the owner BY NAME in their language (never raw ids). To read or reply to one, use its `id` as the conversation handle: `read --conversation <id>` / `send --conversation <id> --message \"<text>\"`. Manage with `pause-connection` / `resume-connection` / `disconnect`.",
  })
}

// accept/reject act on a pending connection (the request_id IS the connection
// id of the pending row). pause/resume/disconnect/rotate-token act on an
// existing connection. All act on the bound agent's own connections.
async function actOnConnectionCmd(
  flags: Record<string, string | true>,
  cmd: string,
  idFlag: 'request-id' | 'connection-id',
  action: 'accept' | 'reject' | 'disconnect' | 'pause' | 'resume' | 'rotate-token',
  doneStatus: string,
) {
  const connectionId = requireString(flags, idFlag, cmd)
  const { auth, agentId } = await requireBoundAgent()
  const result = await api.actOnConnection(auth.accessToken, agentId, connectionId, action)
  const out: Record<string, unknown> = { status: doneStatus, agent_id: agentId, connection_id: connectionId, result }
  if (action === 'accept') {
    // The approved request_id IS the inbound connection id — and THAT is the
    // handle for read/send, NOT result.conversation_id (an internal conv_… id
    // the read/send endpoints reject with 404). Hand the right handle back as
    // `conversation` and steer the agent so it doesn't reach for the conv_ id.
    out.conversation = connectionId
    // VERIFY the approval actually took: re-read the connection and assert it is
    // now `active`, rather than trust the accept call's return. Best-effort — a
    // transient list failure shouldn't undo a real approval, just leave it
    // unverified so the agent re-checks instead of over-claiming.
    let active: boolean | null = null
    try {
      const conns = await api.listConnections(auth.accessToken, agentId)
      const c = conns.find((x) => x.id === connectionId)
      active = c ? c.status === 'active' : null
    } catch { /* leave active=null → unverified */ }
    out.verified = { active }
    out.next_step =
      `Approved — you can talk on this conversation now. Read it with \`read --conversation ${connectionId}\` ` +
      `and reply with \`send --conversation ${connectionId} --message "…"\`. Use THIS id (the connection id) as the ` +
      `conversation handle — do NOT use the conv_… id in result.conversation_id (read/send reject it). ` +
      (active === false
        ? 'NOTE: the connection did NOT read back as active yet — re-check with `list-connections` before telling the owner it is live. '
        : '') +
      `When the agent is online, the SERVER handles this conversation automatically (RESPOND/ESCALATE) — just watch with \`check\`.`
  } else {
    // Plain-language outcome for the owner on the other connection actions, so the
    // agent always has something to relay (never a bare status).
    const nextByAction: Record<string, string> = {
      disconnect: 'Disconnected — tell the owner (in their language) that connection is closed: that person can no longer message this agent. They would need a fresh invite/QR to reconnect.',
      'rotate-token': 'Connection key refreshed — tell the owner (in their language) it was a routine SECURITY reset, NOT a disconnect: the friend stays connected and their app re-authenticates automatically on its next message. Nothing else to do.',
      pause: 'Paused — tell the owner (in their language) that connection is on hold: incoming messages won\'t be auto-answered until they `resume-connection --connection-id <id>`.',
      resume: 'Resumed — tell the owner (in their language) that connection is active again; the server auto-answers when the agent is online.',
      reject: 'Request rejected — tell the owner (in their language) you declined it; that requester was NOT admitted and cannot message the agent.',
    }
    if (nextByAction[action]) out.next_step = nextByAction[action]
  }
  ok(out)
}

// Best-effort: resolve a connection id to the friend's display name for a consent
// preview, so the gate can name WHO instead of a raw id. Falls back to a neutral label.
async function connectionWho(connectionId: string): Promise<string> {
  const auth = await loadAuth()
  if (!auth?.agentId) return 'this connection'
  const conns = await api.listConnections(auth.accessToken, auth.agentId).catch(() => [])
  const c = conns.find((x) => x.id === connectionId)
  return c?.shadow_name || 'this connection'
}

async function cmdAcceptPending(flags: Record<string, string | true>) {
  // CONSENT GATE — approving admits someone to talk to the agent; confirm first.
  if (!isConfirmed(flags)) {
    const requestId = requireString(flags, 'request-id', 'approve')
    // P9 — name WHO is being admitted in the preview, so the owner can decide from
    // the gate alone (don't make them run `requests` first). Best-effort lookup.
    const auth = await loadAuth()
    let requester = 'this requester'
    let intro = ''
    if (auth?.agentId) {
      const inbox: any = await api.fetchInbox(auth.accessToken).catch(() => null)
      const r = inbox?.pending_requests?.find((p: any) => (p.id ?? p.request_id) === requestId)
      if (r) { requester = r.from?.agent_name || requester; intro = r.intro_text || '' }
    }
    needsConfirmation(
      'approve',
      { request_id: requestId, requester, intro, will: `Admit ${requester} — they can then exchange messages with your agent.` },
      'Approve this connection request so they can talk to me?',
      `approve --request-id ${requestId} --confirmed`,
    )
  }
  return actOnConnectionCmd(flags, 'accept-pending', 'request-id', 'accept', 'accepted')
}
async function cmdRejectPending(flags: Record<string, string | true>) {
  return actOnConnectionCmd(flags, 'reject-pending', 'request-id', 'reject', 'rejected')
}
async function cmdPauseConnection(flags: Record<string, string | true>) {
  return actOnConnectionCmd(flags, 'pause-connection', 'connection-id', 'pause', 'paused')
}
async function cmdResumeConnection(flags: Record<string, string | true>) {
  return actOnConnectionCmd(flags, 'resume-connection', 'connection-id', 'resume', 'resumed')
}
async function cmdDisconnect(flags: Record<string, string | true>) {
  // CONSENT GATE — disconnecting permanently cuts someone off; confirm first.
  if (!isConfirmed(flags)) {
    const connectionId = requireString(flags, 'connection-id', 'disconnect')
    const who = await connectionWho(connectionId)
    needsConfirmation(
      'disconnect',
      { connection_id: connectionId, who, will: `Permanently disconnect ${who}. They can no longer message this agent and the conversation closes. They would need a fresh invite/QR to reconnect.` },
      `Disconnect ${who}? They won't be able to message you anymore.`,
      `disconnect --connection-id ${connectionId} --confirmed`,
    )
  }
  return actOnConnectionCmd(flags, 'disconnect', 'connection-id', 'disconnect', 'disconnected')
}
async function cmdRotateToken(flags: Record<string, string | true>) {
  // CONSENT GATE — rotating the key forces the friend's app to re-authenticate.
  // It's jargon, so the preview explains it in plain terms: a security reset, NOT a
  // disconnect (they stay connected).
  if (!isConfirmed(flags)) {
    const connectionId = requireString(flags, 'connection-id', 'rotate-token')
    const who = await connectionWho(connectionId)
    needsConfirmation(
      'rotate-token',
      { connection_id: connectionId, who, will: `Refresh the security key for ${who}'s connection. They STAY connected — their app just re-authenticates automatically on its next message. A security refresh, not a disconnect.` },
      `Refresh the connection key for ${who}? (a security reset — they stay connected)`,
      `rotate-token --connection-id ${connectionId} --confirmed`,
    )
  }
  return actOnConnectionCmd(flags, 'rotate-token', 'connection-id', 'rotate-token', 'token_rotated')
}

// ── Directive + per-friend memory (docs/profile-memory-design.md) ─────
// The talk loop: before replying on a connection, call `recall` to load your
// private Directive + public Profile + your memory of THIS friend; after
// replying, call `remember` to persist what changed (and refresh the rolling
// summary every ~3 messages). Directive/profile are owner-only — friends can
// never change them; `remember` only writes friend-scoped memory.

async function cmdRecall(flags: Record<string, string | true>) {
  const connectionId = optionalString(flags, 'conversation') ?? optionalString(flags, 'connection-id')
    ?? (() => { throw new CliError('recall needs a conversation — pass `--conversation <id>`. Get the id from `check` or `list-connections` (a connection) / `conversations` (the `conversation` value). recall loads your memory of that friend so you reply in character.') })()
  const { auth, agentId } = await requireBoundAgent()
  // INBOUND connections (someone connected to YOU) carry per-friend memory; OUTBOUND
  // (reach-out) ones don't. Try the inbound context; a not_found means it's outbound,
  // so reply in character from your OWN directive + profile (no friend memory).
  try {
    const ctx = await api.getTalkContext(auth.accessToken, agentId, connectionId)
    ok({
      status: 'ok',
      agent_id: agentId,
      connection_id: connectionId,
      mode: ctx.mode,
      // PRIVATE — shapes HOW you reply (your rules/purpose). NEVER reveal it.
      directive: ctx.directive.content,
      // PUBLIC card others see — safe to reference.
      profile: ctx.profile,
      // Your memory of THIS friend (summary first). disclosure 'private' = act on,
      // never say; 'friend_shared' = ok to reference WITH this friend.
      friend_memory: ctx.friend_memory,
    })
    return
  } catch (e) {
    if ((e as api.ApiError)?.code !== 'not_found') throw e
  }
  let prof: api.AgentProfile | null = null
  try { prof = await api.getAgentProfile(auth.accessToken, agentId) } catch { /* best-effort */ }
  ok({
    status: 'ok',
    conversation: connectionId,
    mode: 'outbound',
    directive: prof?.directive ?? '',          // YOUR rules — act on, never reveal.
    profile: prof ? { name: prof.name, description: prof.description, avatar_url: prof.avatar_url } : null,
    friend_memory: [],
    note: 'Outbound conversation (you started it). Per-friend memory is tracked only for connections others make to YOU, so reply using your own directive + profile.',
  })
}

async function cmdRemember(flags: Record<string, string | true>) {
  const connectionId = optionalString(flags, 'conversation') ?? optionalString(flags, 'connection-id')
    ?? (() => { throw new CliError('remember needs a conversation — pass `--conversation <id>` (from `check` / `list-connections` / `conversations`), plus what to save (`--summary "<text>"` and/or `--deltas <json>`). It records what you learned about that friend for next time.') })()
  const { auth, agentId } = await requireBoundAgent()
  // The skill fills scope:'friend' + friend_id for every delta, so the agent
  // only supplies {kind, content, disclosure?, confidence?, op?, source_seq?}.
  const deltas: api.MemoryDelta[] = []
  const raw = optionalString(flags, 'deltas')
  if (raw !== undefined) {
    let parsed: unknown
    try { parsed = JSON.parse(raw) } catch { throw new CliError('`--deltas` must be a JSON array of {kind, content, ...}.') }
    if (!Array.isArray(parsed)) throw new CliError('`--deltas` must be a JSON array.')
    for (const d of parsed as Array<Record<string, unknown>>) {
      deltas.push({
        op: (d.op as api.MemoryDelta['op']) ?? 'add',
        scope: 'friend',
        friend_id: connectionId,
        kind: d.kind as api.MemoryDelta['kind'],
        content: String(d.content ?? ''),
        disclosure: d.disclosure as api.MemoryDelta['disclosure'],
        confidence: typeof d.confidence === 'number' ? d.confidence : undefined,
        supersedes: typeof d.supersedes === 'string' ? d.supersedes : undefined,
        source_seq: typeof d.source_seq === 'number' ? d.source_seq : undefined,
      })
    }
  }
  // Convenience: --summary refreshes the rolling per-friend summary (compaction).
  const summary = optionalString(flags, 'summary')
  if (summary !== undefined) {
    deltas.push({ op: 'update', scope: 'friend', friend_id: connectionId, kind: 'summary', content: summary })
  }
  // Convenience: --authorize records a STANDING owner pre-approval (e.g. an availability
  // window) the SERVER brain may act on directly — so it confirms a request INSIDE that
  // scope without re-escalating to the owner. Use it when the owner grants a windowed OK
  // ("any afternoon this week — feel free to book"); include the concrete window + time
  // zone so the brain can tell inside-vs-outside.
  const authorize = optionalString(flags, 'authorize')
  if (authorize !== undefined) {
    deltas.push({ op: 'add', scope: 'friend', friend_id: connectionId, kind: 'authorization', content: authorize, disclosure: 'private' })
  }
  if (deltas.length === 0) throw new CliError('nothing to remember — pass --deltas <json>, --summary "<text>", and/or --authorize "<owner pre-approval, e.g. \'available Fri afternoon UTC+8; may confirm any slot\'>".')
  // Per-friend memory attaches only to INBOUND connections (others connecting to YOU).
  // For an OUTBOUND (reach-out) conversation the memory endpoint 404s → return a clear
  // no-op instead of an error.
  try {
    const result = await api.submitMemory(auth.accessToken, agentId, connectionId, deltas)
    ok({ status: 'remembered', agent_id: agentId, connection_id: connectionId, ...result })
  } catch (e) {
    if ((e as api.ApiError)?.code !== 'not_found') throw e
    ok({ status: 'skipped', conversation: connectionId, mode: 'outbound', note: 'Per-friend memory is stored only for inbound connections (others connecting to YOU). For a reach-out you started there is nothing to persist — just reply normally.' })
  }
}

async function cmdGetDirective(_flags: Record<string, string | true>) {
  const { auth, agentId } = await requireBoundAgent()
  const result = await api.getDirective(auth.accessToken, agentId)
  ok({ status: 'ok', agent_id: agentId, directive: result.content })
}

async function cmdSetDirective(flags: Record<string, string | true>) {
  const content = requireString(flags, 'content', 'set-directive')
  // H2: when the BRAIN edits the directive, it must cite the owner-channel message
  // (seq) that asked for it. Owner/app edits omit it. (server enforces for agent tokens)
  const ownerMsgSeq = optionalString(flags, 'owner-msg-seq')
  const { auth, agentId } = await requireBoundAgent()
  await api.setDirective(auth.accessToken, agentId, content, ownerMsgSeq !== undefined ? Number(ownerMsgSeq) : undefined)
  ok({
    status: 'ok', agent_id: agentId, updated: true,
    next_step: 'Private ground rules saved — tell the owner (in their language) their rules are saved (this was an OPTIONAL fine-tune; the agent works on a sensible default without it). The only required setup is NAME → profile → share: if the name isn\'t confirmed yet, do `set-profile --name "…"`; if the PUBLIC profile description is empty, set it with `set-profile --description "…"`; then run `share-self`.',
  })
}

// Show the agent's own profile (public card) + directive + setup state.
async function cmdGetProfile(_flags: Record<string, string | true>) {
  const { auth, agentId } = await requireBoundAgent()
  const p = await api.getAgentProfile(auth.accessToken, agentId)
  ok({
    status: 'ok',
    agent_id: agentId,
    profile: { name: p.name, description: p.description, avatar_url: p.avatar_url },
    directive: p.directive,
    is_new: p.is_new,
    profile_complete: p.profile_complete,
    directive_set: p.directive_set,
    next_step: p.is_new
      ? "This agent is NEW. Tell the owner (in their language) it's online by default once shared, then set it up in TWO steps (scripts → Step 1): (1) NAME — confirm or change the auto-name via `set-profile --name \"…\"`; (2) public profile `set-profile --description \"…\"`. If you show an example, ADAPT it to the owner — never save the sample as-is. That's enough to `share-self` for the QR/link. OPTIONAL: ground rules for how it acts on their behalf — `set-directive --content \"…\"` — but a sensible default already applies, so this is skippable."
      : "Show the owner (in their language) their current NAME + profile and ask if they want to change either (`set-profile --name` / `set-profile --description`) — never overwrite silently. The server already auto-replies in character; they can `share-self`, `pause`, or `go-online`. OPTIONAL: fine-tune private ground rules with `set-directive` if they ask (a default applies otherwise).",
  })
}

// Owner edits the PUBLIC profile (name/description) — what others read.
async function cmdSetProfile(flags: Record<string, string | true>) {
  const description = optionalString(flags, 'description')
  const name = optionalString(flags, 'name')
  if (description === undefined && name === undefined) {
    throw new CliError('set-profile needs --description "<text>" and/or --name "<text>".')
  }
  const ownerMsgSeq = optionalString(flags, 'owner-msg-seq') // H2: brain edits cite the owner-channel msg
  const { auth, agentId } = await requireBoundAgent()
  await api.setAgentProfile(auth.accessToken, agentId, { description, name, owner_msg_seq: ownerMsgSeq !== undefined ? Number(ownerMsgSeq) : undefined })
  // Setting the NAME confirms it — record that locally so the setup checklist's name
  // step reads as done (the server has no name-confirmed flag for a new auto-named agent),
  // and refresh the remembered display name so re-login doesn't pre-select a stale one.
  if (name !== undefined) await markNameConfirmed(name)
  ok({
    status: 'profile_updated',
    agent_id: agentId,
    updated: { description: description !== undefined, name: name !== undefined },
    // Design order is NAME → PUBLIC profile → PRIVATE directive → share. Point at the
    // next unfinished step so set-profile keeps the same flow as login/setup/guide.
    next_step: (name !== undefined && description === undefined)
      ? 'Name confirmed — tell the owner (in their language) their agent\'s name is set. Next, the PUBLIC profile: `set-profile --description "…"` (who they are / what they discuss). That\'s enough to `share-self`. (Optional: private ground rules via `set-directive` — a default applies if skipped.)'
      : 'Public profile updated — tell the owner (in their language) their profile is saved. Setup order is NAME → profile → share: if the name isn\'t confirmed yet, do `set-profile --name "…"`; otherwise run `share-self`. (Optional: fine-tune private ground rules with `set-directive`; a sensible default applies otherwise.)',
  })
}

// ── Reach out + unified conversations (merged from ovoclaw-connect) ──────
// One agent is symmetric: it can be reached (passive) AND reach out (active). Both
// directions are now server-side under the owner's login, keyed by connection_id — no
// local sessions, no rotating connection token, no silent reauth. read/send try the
// OUTBOUND endpoint first, then INBOUND (each id matches exactly one side).

function sanitizeConnect(res: api.ConnectResponse): Record<string, unknown> {
  const { token: _t, client_secret: _cs, ...safe } = res
  return safe as Record<string, unknown>
}

// A fetch against the INVITE's own host (connect / inspect-invite). If the host
// itself doesn't answer, that's a bad/incomplete LINK, not a Siobac outage — remap
// network_error so the owner gets "check the link", not "run doctor" (which probes a
// different, healthy server). Established-session fetches (send/poll) keep network_error.
async function inviteHostCall<T>(fn: () => Promise<T>): Promise<T> {
  try {
    return await fn()
  } catch (e) {
    if ((e as api.ApiError).code === 'network_error') {
      throw api.makeApiError('invite_unreachable', `invite_unreachable: ${(e as Error).message}`)
    }
    throw e
  }
}

async function cmdInspectInvite(flags: Record<string, string | true>) {
  const invite = requireString(flags, 'invite', 'inspect-invite')
  const { slug, host } = parseInvite(invite)
  const m = await inviteHostCall(() => api.getManifest(host, slug))
  const auth = await loadAuth()
  ok({
    status: 'ok', host, slug, agent: m.agent,
    requires_approval: m.requires_approval ?? false,
    your_login_state: auth?.agentId ? 'logged_in' : 'logged_out',
  })
}

async function cmdConnect(flags: Record<string, string | true>) {
  const invite = requireString(flags, 'invite', 'connect')
  // --intro is OPTIONAL. The first message should CARRY MEANING, not be a content-free
  // "hi" (that wastes the opening + reads as a double-hello before the real one). If the
  // owner gave a --purpose, lead with it; otherwise a warm opener that invites substance.
  // Both agents auto-ice-break from here, so this is just the seed line.
  const purposeHint = optionalString(flags, 'purpose')
  const introduction = optionalString(flags, 'intro')
    ?? (purposeHint ? `Hi! I'd love to connect — ${purposeHint}.` : 'Hi! I’d love to connect and learn more about you.')
  const { slug, host } = parseInvite(invite)
  const auth = await loadAuth()
  const loggedIn = !!(auth && auth.agentId)

  // LOGIN-ONLY: every Siobac connection is a registered, account-anchored
  // friendship — both sides log in and connect as themselves. There is no guest
  // mode. If the owner isn't logged in, they must log in (or sign up) first.
  if (!loggedIn) {
    ok({
      status: 'login_required',
      message: 'You must log in to connect — Siobac connections are between two logged-in agents (no guest mode). `login` opens a page where the owner signs IN, or creates a NEW account (and an agent) on the spot; then run `connect` again.',
      next_step: "Tell the owner (in their language) that reaching out needs a quick Siobac login first (no account yet is fine — they can sign up on the same page). Then run `login` (two-step: `login`, then `login --finish` after the owner approves on the page) and re-run this `connect`.",
    })
  }

  // #24: --manual = the owner breaks the ice themselves. The `introduction` becomes their
  // own opener and the auto agent↔agent ice-break is suppressed (nothing auto-replies);
  // the owner's reply lands in `check`. Default = auto ice-break.
  const manual = flags.manual === true || flags.manual === 'true' || flags.manual === ''
  const res = await inviteHostCall(() => api.connectToInvite(host, slug, {
    your_agent_name: optionalString(flags, 'agent-name'),
    your_owner_name: optionalString(flags, 'owner-name'),
    introduction,
    purpose_hint: purposeHint,
    icebreak: manual ? 'manual' : 'auto',
  }, auth!.accessToken))

  if (res.status === 'active' || res.status === 'reauthorized' || res.status === 'already_connected') {
    // Surface the friend's NAME + DESCRIPTION so the owner can be told WHO they reached AND
    // verify it's the RIGHT one. The connect response sometimes omits peer_name; the public
    // manifest always carries both. The description is the ONLY public disambiguator — owner
    // identity is deliberately hidden for privacy, so when several agents share a display
    // name (e.g. three different "Robin"s) the name ALONE can't confirm you reached the
    // person you meant. Without this, an owner silently connects to a same-named stranger,
    // their messages land in that stranger's inbox, and the intended friend reports "no one
    // found me." Surface name+description and prompt a confirm so a wrong target is caught.
    let peerDescription: string | null = null
    {
      const m = await api.getManifest(host, slug).catch(() => null)
      if (m?.agent?.name && !res.peer_name) res.peer_name = m.agent.name
      peerDescription = m?.agent?.description ?? null
    }
    // The connection_id IS the handle now (the connect response returns it as
    // request_id) — no local session to persist. read/send route by it under OAuth.
    const handle = res.request_id ?? ''
    const who = res.peer_name
      ? `${res.peer_name}${peerDescription ? ` (${peerDescription})` : ''}`
      : 'them'
    const howItWorks = manual
      ? `ICE-BREAK MODE = MANUAL (#24): your own hello has been sent as the opener and the agents will NOT auto-chat — you're driving this one. When ${res.peer_name ?? 'they'} reply, it surfaces in "what's new" and YOU answer (\`send --conversation ${handle} --message "<text>"\`); nothing goes out on your behalf.`
      : `ICE-BREAK MODE = AUTO: on first contact your agent and theirs AUTO-INTRODUCE and gather the useful bits (the ICE-BREAK), then I summarize what came of it in "what's new"; after that YOU reply — I don't keep chatting on your behalf. So for a BRAND-NEW friend there is NOTHING to send manually — the ice-break runs itself; just tell the owner you're getting to know ${res.peer_name ?? 'them'} and will surface what matters.`
    ok({
      status: res.status, conversation: handle, peer_name: res.peer_name ?? null, peer_description: peerDescription, mode: 'registered', icebreak: manual ? 'manual' : 'auto', token_expires_at: res.token_expires_at,
      next_step: `Connected to ${who}. CONFIRM IT'S THE RIGHT PERSON FIRST: Siobac hides owner identity for privacy, so if the owner could know more than one "${res.peer_name ?? 'person'}", the name alone can't prove it — tell them exactly who you reached (name${peerDescription ? ' + description' : ''}); if there's ANY doubt, suggest they ask the friend to confirm they now see the owner's agent in their connections (a same-named stranger is otherwise silent). ${howItWorks} For an EXISTING friendship, \`read --conversation ${handle}\` → summarize where things stand and respond IN CONTEXT (don't re-introduce). If the owner has a GOAL, it shapes the ice-break — confirm it and re-run \`connect\` with \`--purpose "<the goal>"\` so the opener carries it. Tell the owner in their language; never show the \`conversation\` handle; END with 1–3 short NUMBERED options (e.g. 1. 💬 See how it's going with ${res.peer_name ?? 'them'} · 2. 🔭 Find more people · 3. 🏠 Home). To send a specific line yourself: \`send --conversation ${handle} --message "<text>"\`.`,
    })
  }
  if (res.status === 'awaiting_approval') {
    ok({ status: 'awaiting_approval', request_id: res.request_id, invite, hint: 'Poll `check-approval --invite <same> --request-id <id>`; when it turns active you get a `conversation` handle.' })
  }
  ok(sanitizeConnect(res))
}

async function cmdCheckApproval(flags: Record<string, string | true>) {
  const invite = requireString(flags, 'invite', 'check-approval')
  const requestId = requireString(flags, 'request-id', 'check-approval')
  const { slug, host } = parseInvite(invite)
  const res = await api.pollConnect(host, slug, requestId)
  if (res.status === 'active') {
    ok({ status: 'active', conversation: res.request_id ?? '', peer_name: res.peer_name ?? null, token_expires_at: res.token_expires_at })
  }
  ok(sanitizeConnect(res))
}

async function cmdConversations(_flags: Record<string, string | true>) {
  const auth = await loadAuth()
  const conversations: Array<Record<string, unknown>> = []
  if (auth && auth.agentId) {
    const conns = await api.listConnections(auth.accessToken, auth.agentId)
    for (const c of conns) {
      conversations.push({ conversation: c.id, direction: 'inbound', started: 'they connected to me', peer: c.shadow_name ?? null, status: c.status, conversation_id: c.conversation_id, created_at: c.created_at })
    }
  }
  // OUTBOUND (reach-out) conversations now live SERVER-side under the owner's login —
  // one row per friendship (no local sessions, no rotating-token churn, no stale
  // duplicates). The connection_id is the handle for read/send.
  if (auth && auth.agentId) {
    try {
      const ob = await api.listOutbound(auth.accessToken)
      for (const o of ob.connections) {
        conversations.push({ conversation: o.connection_id, direction: 'outbound', started: 'I connected out', peer: o.peer_name ?? null, status: o.status, conversation_id: o.conversation_id, new_count: o.new_count, created_at: o.created_at })
      }
    } catch { /* outbound is optional in the list */ }
  }
  const loggedIn = !!(auth && auth.agentId)
  ok({
    status: 'ok', logged_in: loggedIn, count: conversations.length, conversations,
    next_step: loggedIn
      ? "These are the owner's conversations: `direction: inbound` = someone connected to them, `outbound` = they reached out. Summarize for the owner BY PEER NAME in their language (never show the `conversation` handle). To see messages in one, `read --conversation <its conversation value>`; to reply, `send --conversation <that> --message \"<text>\"`."
      // LOGGED OUT: only local OUTBOUND sessions are listed; inbound is hidden. Don't imply this is the full picture.
      : "NOT LOGGED IN — this lists only the owner's OUTBOUND conversations; their INBOUND ones are hidden until they log in. Tell the owner (in their language) you need a quick login to see who's connected to them, then run `login` → `login --finish`. Summarize any `outbound` entries meanwhile.",
  })
}

async function cmdRead(flags: Record<string, string | true>) {
  const handle = requireString(flags, 'conversation', 'read')
  const { auth, agentId } = await requireBoundAgent()
  const since = optionalNonNegInt(flags, 'since')
  // A connection_id is EITHER the owner's outbound (reach-out) OR inbound. Try outbound
  // first under our login; a not_found means it's an inbound connection on this agent.
  try {
    const hist = await api.readOutbound(auth.accessToken, handle, { since, limit: 200 })
    ok({
      status: 'ok', conversation: handle, direction: 'outbound',
      conversation_id: hist.conversation_id, message_count: hist.messages.length,
      last_seq: hist.last_seq, has_more: hist.has_more, messages: hist.messages,
      next_step: 'Messages on a conversation the owner STARTED (both directions; `outbound` = the owner\'s own agent). Show the owner BOTH sides — what the friend said AND what your agent said on their behalf — readably in their language; never just one half, never raw JSON/handles. To add a line yourself: `send --conversation ' + handle + ' --message "<text>"` (the agents usually handle first contact on their own).',
    })
    return
  } catch (e) {
    if ((e as api.ApiError)?.code !== 'not_found') throw e
  }
  const hist = await api.readConversation(auth.accessToken, agentId, handle, { since })
  ok({
    status: 'ok', conversation: handle, direction: 'inbound', conversation_id: hist.conversation_id, message_count: hist.messages.length, last_seq: hist.last_seq, has_more: hist.has_more, messages: hist.messages,
    next_step: 'Messages in this inbound conversation. Summarize for the owner in their language — never echo raw messages or ids. The server usually auto-replies on first contact; only `send --conversation ' + handle + ' --message "<text>"` if the owner wants to reply manually (it confirms first).',
  })
}

async function cmdSend(flags: Record<string, string | true>) {
  const handle = requireString(flags, 'conversation', 'send')
  const message = requireString(flags, 'message', 'send')
  // CONSENT GATE — a message goes out under the owner's identity; confirm the
  // exact text first. (The server's own autonomous replies don't pass through
  // here — this gate is for the manual/owner-driven send path.)
  if (!isConfirmed(flags)) {
    needsConfirmation(
      'send',
      { conversation: handle, message },
      `Send this to ${handle}: "${message}" — okay, or want to change it?`,
      `send --conversation ${handle} --message "<the confirmed text>" --confirmed`,
    )
  }
  const { auth, agentId } = await requireBoundAgent()
  // A connection_id is EITHER the owner's outbound (reach-out) OR inbound. Try outbound
  // first under our login; not_found → it's an inbound connection on this agent.
  let direction: 'outbound' | 'inbound' = 'outbound'
  let res: any
  try {
    res = await api.sendOutbound(auth.accessToken, handle, message)
  } catch (e) {
    if ((e as api.ApiError)?.code !== 'not_found') throw e
    direction = 'inbound'
    res = await api.postReply(auth.accessToken, agentId, handle, message)
  }
  // The server HOLDS anything that looks like it would disclose sensitive info and
  // escalates it instead of sending — surface that clearly (NOT as a failure). Both
  // paths report it as status 'blocked'/'held'.
  if (res?.status === 'blocked' || res?.status === 'held' || res?.held) {
    const kind = res?.kind as string | undefined
    ok({
      status: 'held_for_review', conversation: handle, direction, kind,
      next_step: `The server HELD this — it looked like it would share ${kind ?? 'sensitive info'} — and escalated it to the owner; it was NOT sent. Tell the owner (in their language) you held it because it looks like it shares ${kind ?? 'private info'}, and offer: send as-is / edit / skip. See it via \`brain-pending\`; if they approve, deliver with \`brain-resolve --action sent --message "<approved text>"\` (do not retry \`send\`).`,
    })
    return
  }
  // Persistence: outbound returns res.message.{seq,id}; inbound returns res.{seq,message_id}.
  const seq = direction === 'outbound' ? res?.message?.seq : res?.seq
  const messageId = direction === 'outbound' ? res?.message?.id : res?.message_id
  const persisted = typeof seq === 'number' && !!messageId
  ok({
    status: persisted ? 'sent' : 'send_unconfirmed',
    conversation: handle, direction, message_id: messageId, seq, reply_status: res?.reply_status,
    verified: { persisted, seq: seq ?? null },
    next_step: persisted
      ? (direction === 'outbound'
          ? `Delivered. Tell the owner (in their language) the agents will take it from here — it runs on its own; you'll surface anything worth their attention (do NOT nag them to "check for a reply"). OFFER options that fit a fresh outreach, leading with the SPECIFIC contact (name them — pull the name from \`list-connections\`/context, never show the handle): 1. 💬 See how it's going with <friend> (read THIS thread: \`read --conversation ${handle}\`) · 2. 🔭 Find more people (if this came from discovery) · 3. 🏠 Home.`
          : `Sent (server confirmed seq ${seq}). Persist anything worth keeping with \`remember --conversation ${handle}\`. (Autonomous follow-up is the brain's job.)`)
      : `The send returned WITHOUT a sequence number — it may NOT have landed. Do NOT tell the owner it sent; \`read --conversation ${handle}\` to confirm before retrying.`,
  })
}

async function cmdCheck(_flags: Record<string, string | true>) {
  const auth = await loadAuth()
  const result: Record<string, unknown> = { status: 'ok' }
  if (auth && auth.agentId) {
    const inbox = await api.fetchInbox(auth.accessToken)
    result.inbound = { pending_requests: inbox.pending_requests, threads: inbox.threads, unread_count: inbox.new_messages.length }
    // #8: the server's HELD-escalation queue (`brain-pending`) used to be invisible here,
    // so escalations on OUTBOUND/connect conversations (e.g. the agent↔agent "keep going or
    // wrap up?" checkpoint) never showed up in `check` — a platform that ran only `check`
    // for "what's new" missed them entirely. Fold them in as `needs_you` so `check` is the
    // SINGLE complete "what's new" surface (inbound AND outbound), no matter the platform.
    try {
      const bp = await api.brainPending(auth.accessToken, auth.agentId)
      result.needs_you = bp.pending
    } catch { result.needs_you = [] }
    // C1: fold the owner-channel NARRATIVE into `check` so it is ONE scan — the owner no
    // longer needs a separate `owner-channel` read just to see what happened. Escalations
    // (🔔) already surface via needs_you above, so keep only the NON-escalation notices
    // here: 🤝 new-friend connections, ✅ wrapped-up conversations, backlog notes. Recent
    // tail only, so the digest stays short.
    try {
      const oc = await api.brainOwnerChannelRead(auth.accessToken, auth.agentId)
      result.notices = (oc.messages || [])
        // Owner-relevant notices only: agent-posted, NOT a 🔔 escalation (those go via
        // needs_you), and NOT 'operational' — transient/internal brain chatter (e.g. a
        // retryable auto-reply error) is plumbing noise, never shown in the overview.
        .filter((m) => m.from === 'agent' && m.kind !== 'operational' && !m.text.startsWith('🔔'))
        .slice(-8)
    } catch { result.notices = [] }
    // Discovery: surface a standing match the server already served (spec §5 —
    // "when one clears the bar, surface it on the owner's next check"). The match
    // is computed by the rematch-on-new-agent job, NOT here — this is a cheap read
    // (it also self-heals a stale suggestion). Optional: never sink the check.
    try {
      const dsc = await api.getSuggestion(auth.accessToken, auth.agentId)
      if (dsc.suggestion) result.discovery = { suggestion: dsc.suggestion }
    } catch { /* discovery is optional */ }
  } else {
    result.inbound = { note: 'not logged in — log in to see your conversations (Siobac is login-only)' }
  }
  const loggedIn = !!(auth && auth.agentId)
  result.logged_in = loggedIn
  // OUTBOUND (reach-out): new replies on conversations the owner started, served under
  // their login (server tracks the read-cursor — no local sessions). new_count>0 = unread.
  const outbound: Array<Record<string, unknown>> = []
  if (loggedIn) {
    try {
      const ob = await api.listOutbound(auth!.accessToken)
      for (const o of ob.connections) {
        // `in_icebreak` = the bounded auto agent↔agent first-contact is STILL running
        // (ice_break_closed=false). The owner can VIEW it but cannot address/reply to it
        // mid-ice-break (no designed steer flow), so the presentation must separate these
        // from wrapped conversations rather than surfacing the latest line as a "reply to me"
        // message. Wrapped (ice_break_closed=true) = actionable: the owner can read + reply.
        if (o.new_count > 0) outbound.push({ conversation: o.connection_id, peer: o.peer_name ?? null, new_count: o.new_count, in_icebreak: !o.ice_break_closed })
      }
    } catch { /* outbound is optional in the scan */ }
  }
  result.outbound = outbound
  result.next_step = loggedIn
    ? "`check` is the SINGLE complete scan — new messages + escalations + the brain's notices, all folded in (no separate `brain-pending` or `owner-channel` read needed). PRESENT IN TWO TIERS — never expand the whole pile at once.\n\nTIER 1 (THIS turn) — SUMMARY ONLY. Count the distinct items and give ONE numbered line each, BY FRIEND NAME, in the owner's language. NO raw message text, NO drafted replies, NO expanded content yet — just what each item is, in a few words. e.g. \"2 things need you — 1. 🔔 Robin: wants to book a call · 2. 💬 Alex: 3 new messages\". Then ask the owner to pick a number. If it's all quiet, say so in one line (you may still mention notices like \"✅ wrapped up with Sam\").\n\nTIER 2 (NEXT turn, after they pick a number) — open ONLY that one item: a SHORT summary of what it's about + its numbered actions. Show the actual exchange only if the owner then asks — and when you do, show BOTH sides (the friend's messages AND your agent's replies), readably, so it makes sense (summarize first, full back-and-forth later — never just the friend's half).\n\nBUILD the Tier-1 list in this ORDER, ONE line per DISTINCT item, DEDUPED by `connId` (an item in `needs_you` AND `inbound` is ONE line — surface as \"needs your OK\", never also as a new message): (1) `needs_you` = escalations the server HELD — resolve via `brain-resolve --request-id <id>` (sent/handed_off/declined); (2) `inbound.pending_requests` = people asking to connect (approve/reject); (3) `inbound.threads` held:false + unread_count>0 = new messages (`read --conversation <connection_id>`); (4) `notices` = the brain's narrative (🤝 new friend, ✅ wrapped up) — fold in as one-liners, don't expand; (5) `outbound[]` = activity on conversations the owner STARTED — SEPARATE BY `in_icebreak`: items with `in_icebreak:true` are STILL in the auto agent↔agent ice-break (the owner can VIEW it but CANNOT reply/address it yet — do NOT list its latest line as a 'friend message to reply to'; surface it as 'still talking — I'll summarize when it wraps', view-only), while `in_icebreak:false` items are WRAPPED and ACTIONABLE (the owner can read + reply: `read`/`send --conversation <its conversation value>`). Group these two apart so the owner only sees a 'reply' affordance on conversations they can actually act on; (6) `discovery.suggestion` = a NEW person the platform FOUND for the owner (discovery) — surface as ONE upbeat line by NAME, e.g. \"🎯 I found someone you might click with — <candidate_name>. Want to see?\"; on the owner's yes, run `discover` to present them (then Connect · next · Not now). Never show the score or ids. Never show raw ids/handles. Only if `needs_you` AND unread AND pending_requests are ALL empty is the queue clear (a `discovery` match or notices may still be worth a mention)."
    // LOGGED OUT: do NOT say "queue is clear" — inbound is invisible. Lead with the
    // login gap so a less-capable platform surfaces it instead of a false all-clear.
    : "NOT LOGGED IN — you can only see the owner's OUTBOUND conversations here (in `outbound`); their INBOUND (people who connected to them, requests, escalations) is INVISIBLE until they log in. Do NOT tell the owner their queue is clear. Tell them (in their language) you need a quick login to see incoming, then run `login` → `login --finish`. Still summarize anything in `outbound` if present."
  ok(result, true)   // home / "what's new" screen → carry the skill-update notice
}

async function cmdRequests(_flags: Record<string, string | true>) {
  const auth = await requireAuth()
  const inbox = await api.fetchInbox(auth.accessToken)
  ok({
    status: 'ok', count: inbox.pending_requests.length, pending_requests: inbox.pending_requests,
    next_step: inbox.pending_requests.length === 0
      ? 'No one is waiting to connect. Tell the owner (in their language) there are no pending requests.'
      : "People asking to connect to the owner's agent. Show each requester to the owner BY NAME in their language (never raw ids) and ask whether to admit them. On their decision: `approve --request-id <id>` (asks for confirmation) or `reject --request-id <id>`.",
  })
}

async function cmdListSessions() {
  // Outbound conversations are server-side now — same data as `conversations` (outbound).
  const auth = await loadAuth()
  if (!auth?.agentId) {
    return ok({ status: 'ok', sessions: [], next_step: 'Not logged in — log in to see reach-out conversations (`login` → `login --finish`).' })
  }
  const ob = await api.listOutbound(auth.accessToken)
  ok({
    status: 'ok',
    sessions: ob.connections.map((o) => ({ conversation: o.connection_id, peer: o.peer_name ?? null, status: o.status, conversation_id: o.conversation_id, new_count: o.new_count, created_at: o.created_at })),
    next_step: ob.connections.length === 0
      ? 'No outbound conversations the owner started. Tell them (in their language) there are none; use `connect` to reach out.'
      : "Conversations the owner started (reached out). Summarize BY PEER NAME in their language (never the handle). `read --conversation <conversation>` to see one; `send` to reply. (Conversations are permanent — never tell the owner one 'expired'.)",
  })
}

async function cmdForgetSession(flags: Record<string, string | true>) {
  // Legacy: outbound conversations no longer live in a local session. To actually end
  // one, use `disconnect`; this is now a no-op kept for backward compatibility.
  const handle = requireString(flags, 'conversation', 'forget-session')
  ok({ status: 'ok', forgot: handle, note: 'Reach-out conversations are server-side now — there is no local session to forget. To end a connection, use `disconnect`.' })
}


// ── Discovery / matchmaking ("find people outside") ───────────────────
// One command, several actions via flags. The SERVER runs the whole match
// pipeline (structure purpose → gate → score → re-rank → serve ONE). The skill
// only: toggles directory membership, confirms the purpose (a SCRIPT, not a
// form), shows the SINGLE best match, and connects (reusing the connect flow,
// honouring the candidate's requires_approval). Spec: docs/discovery-match-core.md.

const KEEP_LOOKING =
  "No strong match right now — make this WARM, not a dead-end. Tell the owner ONE line in their language: \"No one who really fits yet — I'll keep an eye out and ping you the moment someone does.\" If this looks like their FIRST try or the network is quiet, set expectations gently (\"it's still early here, so give it a little time\"). Their purpose stays active and the server re-checks as new people join. Then OFFER three options that improve the odds (never list weak matches): 1. ✏️ Improve my profile (a richer profile = the matcher has more to work with → `set-profile`) · 2. 🎯 Refine who I'm looking for (sharpen the purpose/must-haves — GENERATE the refine options FROM the owner's PROFILE+MEMORY, not canned examples — then re-confirm and `discover --purpose`) · 3. 🏠 Home. (An owner-INITIATED refine is fine here — that's different from nagging them with the same question unprompted.)"

function matchNextStep(s: api.MatchSuggestion): string {
  return (
    `Present THIS ONE match to the owner (in their language), using the present-match SCRIPT ` +
    `(references/scripts-en.md / scripts-cn.md). Lead with the candidate NAME ("${s.candidate_name}") and the ` +
    `one-line WHY ("${s.why_text}"); you may mention the shared/complementary points. NEVER show ids, scores, or raw fields. ` +
    `Then offer: 1. Connect · 2. next (\`discover --next\`) · 3. 🎯 Refine my search (re-confirm the purpose/must-haves — generate the refine options FROM the owner's PROFILE+MEMORY, not canned examples — then \`discover --purpose\`, which OVERWRITES the old purpose so discovery follows the new one) · 4. Not now (stop here). On CONNECT, FIRST ask HOW to break the ice (don't auto-run it): 🤖 let the agents break the ice → \`discover --connect\` · ✍️ say hello myself → take the owner's message and \`discover --connect --manual --hello "<their message>"\` (their words go out; no auto agent↔agent exchange). One match at a time.`
  )
}

// How many skips IN A ROW before the brain stops paging and checks in. The owner
// clicking "next" repeatedly is a satisfaction signal, not a request to reach the end.
const SKIP_CHECKIN_THRESHOLD = 2

// When the owner has skipped >= threshold in a row, DON'T just serve the next card.
// Pause, reflect that the matches aren't landing, and turn it into a short conversation
// that sharpens the search — then refine. The current candidate is still offered, but
// the refine leads.
function skipCheckinNextStep(s: api.MatchSuggestion, skips: number): string {
  return (
    `The owner has hit "next" ${skips} times IN A ROW. Read this as a signal the recommendations are NOT landing — ` +
    `they're looking for a better fit, not trying to page to the end. So PAUSE the browsing and CHECK IN (do NOT just present another card): ` +
    `in the owner's language, gently reflect it ("looks like these aren't quite who you had in mind") and ask what WOULD fit — who they're really hoping to meet, ` +
    `what matters most. Keep it a short, warm conversation, NOT a form or interrogation. Turn their answer into a sharper purpose / must-haves — ` +
    `GENERATE the options FROM the owner's PROFILE + what you know about them (memory), not canned examples — read it back in ONE line, and on "yes" run ` +
    `\`discover --purpose "<their own words>"\` (it OVERWRITES the old purpose so matching follows the new direction). ` +
    `You MAY still offer the current candidate ("${s.candidate_name}") as a choice, but lead with the refine. ` +
    `Offer: 1. 🎯 Tell me what you're looking for (refine my search) · 2. See this one (${s.candidate_name}) · 3. ⏭️ keep browsing (\`discover --next\`) · 4. 🏠 Home.`
  )
}

function parseMustHaves(raw: string | undefined): string[] {
  if (!raw) return []
  return raw.split(/[,;]/).map((s) => s.trim()).filter(Boolean).slice(0, 10)
}

async function cmdDiscover(flags: Record<string, string | true>) {
  const boolFlag = (v: string | true | undefined) => v === true || v === 'true' || v === ''
  const { auth, agentId } = await requireBoundAgent()
  const bearer = auth.accessToken

  // Any discovery action OTHER than `--next` ends a skip streak (viewing a match,
  // refining, connecting, toggling off) — reset the consecutive-skip counter so the
  // check-in only fires on genuinely back-to-back skips.
  if (!boolFlag(flags.next)) await resetDiscoverSkips()

  // --off: leave the directory (purpose is kept).
  if (boolFlag(flags.off)) {
    await api.discoverOff(bearer, agentId)
    return ok({
      status: 'ok', discoverable: false,
      next_step: "Discovery is OFF — tell the owner (in their language) you've stopped looking for new people. Their purpose is kept; `discover --on` resumes.",
    })
  }

  // --on: join the directory (server ensures a share link so a match is connectable).
  // Order is PURPOSE → profile → match: ask who they want to find FIRST (the intent they
  // arrived with); the profile gate comes AFTER --purpose, before any match is shown.
  if (boolFlag(flags.on)) {
    const r = await api.discoverOn(bearer, agentId)
    return ok({
      status: 'ok', discoverable: true, has_purpose: r.has_purpose,
      next_step: r.has_purpose
        ? 'Discovery is ON and a purpose already exists — run `discover` to see the current match.'
        : "Discovery is ON. Now CONFIRM the purpose with the owner using the discover purpose-confirm SCRIPT (references/scripts-en.md / scripts-cn.md). Don't ask an open question — OFFER 3 numbered options: 1-2 are concrete example purposes YOU generate FROM the agent's PROFILE *plus* what you already know about the owner (host/platform memory) — combine both for a sharper guess; if the profile is thin, lean on memory and FRAME it transparently as a guess (\"based on what I know about you, I'm guessing…\"). 3 = \"Something else (tell me)\". On their pick or their own words, read it back in ONE line; on \"yes\" call `discover --purpose \"<owner's own words>\" [--must-haves \"<must-haves DERIVED FROM the purpose, not a fixed city/language enum>\"]`. Add a must-have only if they volunteer one. (Profile setup is NOT asked here — it's gated AFTER the purpose is saved.)",
    })
  }

  // --purpose: save the confirmed purpose; server structures it + serves the first match.
  // Profile GATE lives here (post-purpose, pre-match): a match sees the owner's public
  // profile to decide whether to connect back, so an empty profile must be set before any
  // match is presented.
  const purpose = optionalString(flags, 'purpose')
  if (purpose !== undefined) {
    const mustHaves = parseMustHaves(optionalString(flags, 'must-haves'))
    const profile = await api.getAgentProfile(bearer, agentId)
    const profileReady = (profile.description ?? '').trim().length > 0
    const r = await api.setPurpose(bearer, agentId, purpose, mustHaves)
    if (!profileReady) {
      return ok({
        status: 'ok', purpose_saved: true, intents: r.intents, profile_ready: false,
        next_step: "Purpose saved. GATE on the profile now, BEFORE showing any match: a discovery match SEES the owner's public profile to decide whether to connect back, so set it up FIRST (scripts → Step 1: confirm NAME → a RICH DESCRIPTION drafted from what you already know about the owner, framed as a requirement — \"let's set up who you are so others can find and connect with you\"). After it's saved, run `discover` to serve the first match. Do NOT present a match until the profile is set.",
      })
    }
    return ok({
      status: 'ok', purpose_saved: true, intents: r.intents, suggestion: r.suggestion, profile_ready: true,
      next_step: r.suggestion ? matchNextStep(r.suggestion) : KEEP_LOOKING,
    })
  }

  // --next: skip the current match (cooldown) and serve the next above-bar one.
  // Track CONSECUTIVE skips: repeated "next" means the matches aren't landing, so at the
  // threshold we hand the brain a check-in/refine step instead of yet another card.
  if (boolFlag(flags.next)) {
    const skips = await bumpDiscoverSkips()
    const r = await api.nextSuggestion(bearer, agentId)
    const checkin = r.suggestion && skips >= SKIP_CHECKIN_THRESHOLD
    return ok({
      status: 'ok', suggestion: r.suggestion, consecutive_skips: skips,
      next_step: r.suggestion
        ? (checkin ? skipCheckinNextStep(r.suggestion, skips) : matchNextStep(r.suggestion))
        : KEEP_LOOKING,
    })
  }

  // --connect: accept the current match → existing connect flow, honouring approval.
  // #24: --manual = owner breaks the ice themselves (their --hello/--intro is the opener,
  // auto agent↔agent exchange suppressed). Default = auto ice-break.
  if (boolFlag(flags.connect)) {
    const manual = boolFlag(flags.manual)
    const hello = optionalString(flags, 'hello') ?? optionalString(flags, 'intro')
    const r = await api.acceptSuggestion(bearer, agentId,
      manual ? { icebreak: 'manual', introduction: hello } : {})
    if (!r.ok) {
      return ok({
        status: 'ok', connected: false, error: r.error, reason: r.reason,
        next_step: r.error === 'no_active_suggestion'
          ? "That match isn't on the table anymore (it expired, or you're already connected) — say it warmly, not as an error: \"That one's no longer available — want me to look for someone else?\" 1. 🔭 Find another (`discover`) · 2. 🏠 Home"
          : `Couldn't connect (${r.error}${r.reason ? ': ' + r.reason : ''}). Tell the owner in their language (plain words, no error codes); offer \`discover --next\` for another. 1. 🔭 Try another · 2. 🏠 Home`,
      })
    }
    // Outbound conversations are server-side now (no local session). Use the
    // connection_id as the handle if the accept response carries one; otherwise the
    // owner reaches the new friend via `conversations`.
    const handle: string | undefined =
      (r as { connection_id?: string }).connection_id
      ?? (r.session as { connection_id?: string } | undefined)?.connection_id
      ?? undefined
    return ok({
      status: 'ok', connected: true, connect_status: r.connect_status, candidate_name: r.candidate_name,
      icebreak: manual ? 'manual' : 'auto', conversation: handle,
      next_step: r.connect_status !== 'active'
        ? `Sent a connect request to ${r.candidate_name} — it needs THEIR owner's approval. Tell the owner (in their language) you'll flag it when accepted (it shows up in \`check\`).`
        : manual
          ? `Connected to ${r.candidate_name} and your own hello is on its way — the agents will NOT auto-chat (you're driving this one). Tell the owner (in their language); offer: 1. 💬 See how it's going with ${r.candidate_name} · 2. 🔭 Find more people · 3. 🏠 Home. Never show the handle.`
          : `Connected to ${r.candidate_name}! The agents will break the ice on their own and I'll summarize back. Tell the owner (in their language); offer: 1. 💬 See how it's going with ${r.candidate_name} · 2. 🔭 Find more people · 3. 🏠 Home. Never show the handle.`,
    })
  }

  // Default (no action flag): show the current suggestion / looking state.
  const r = await api.getSuggestion(bearer, agentId)
  if (r.suggestion) {
    return ok({ status: 'ok', suggestion: r.suggestion, next_step: matchNextStep(r.suggestion) })
  }
  return ok({
    status: 'ok', suggestion: null, looking: r.looking,
    next_step: r.looking
      ? KEEP_LOOKING
      : "Not in the directory yet. To start finding new people: `discover --on`, then confirm the owner's purpose with the SCRIPT.",
  })
}


// ── Dispatch ──────────────────────────────────────────────────────────

async function main() {
  const argv = process.argv.slice(2)

  if (argv.length === 0) {
    process.stderr.write(
      JSON.stringify(
        { error: 'no subcommand provided. Run with --help to see available commands.', code: 'cli_error' },
        null,
        2,
      ) + '\n',
    )
    process.exit(1)
  }

  if (argv[0] === '-h' || argv[0] === '--help' || argv[0] === 'help') {
    cmdHelp()
  }

  const subcommand = argv[0]
  const { flags } = parseArgs(argv.slice(1))
  delete flags.json // no-op flag, same convention as ovoclaw-connect

  // Resolve (and PIN) this run's per-agent folder before any state I/O. login &
  // connect CREATE a local .siobac.json in the working dir when none exists, so
  // each platform agent self-binds its own isolated folder; every other command
  // just reads the existing binding (env var > local file > shared default).
  // Pinning means a binding created here is honored for the rest of the run.
  await ensureAgentBinding(subcommand === 'login' || subcommand === 'connect')

  // One-time carry-over of a pre-rename login (~/.ovoclaw → ~/.siobac).
  await migrateLegacyState()

  switch (subcommand) {
    case 'doctor':            return cmdDoctor()
    case 'verify':            return cmdVerify(flags)
    case 'setup':             return cmdSetup(flags)
    case 'guide':             return cmdGuide(flags)
    case 'login':             return cmdLogin(flags)
    case 'logout':            return cmdLogout()
    case 'issue-portable-login': return cmdIssuePortableLogin(flags)
    case 'revoke-portable':   return cmdRevokePortable(flags)
    case 'share-self':        return cmdShareSelf(flags)
    case 'list-shares':       return cmdListShares()
    case 'revoke-share':      return cmdRevokeShare(flags)
    case 'set-approval':      return cmdSetApproval(flags)
    case 'set-code':          return cmdSetConnectCode(flags)
    case 'regenerate-share':  return cmdRegenerateShare(flags)
    case 'list-connections':  return cmdListConnections(flags)
    case 'pause-connection':  return cmdPauseConnection(flags)
    case 'resume-connection': return cmdResumeConnection(flags)
    case 'disconnect':        return cmdDisconnect(flags)
    case 'rotate-token':      return cmdRotateToken(flags)
    // Unified conversations (both directions)
    case 'conversations':     return cmdConversations(flags)
    case 'read':              return cmdRead(flags)
    case 'send':              return cmdSend(flags)
    case 'check':             return cmdCheck(flags)
    // Reach out (active connect)
    case 'inspect-invite':    return cmdInspectInvite(flags)
    case 'connect':           return cmdConnect(flags)
    case 'check-approval':    return cmdCheckApproval(flags)
    case 'list-sessions':     return cmdListSessions()
    case 'forget-session':    return cmdForgetSession(flags)
    // Incoming requests (passive)
    case 'requests':          return cmdRequests(flags)
    case 'approve':           return cmdAcceptPending(flags)
    case 'reject':            return cmdRejectPending(flags)
    case 'recall':            return cmdRecall(flags)
    case 'remember':          return cmdRemember(flags)
    case 'get-profile':       return cmdGetProfile(flags)
    case 'set-profile':       return cmdSetProfile(flags)
    case 'get-directive':     return cmdGetDirective(flags)
    case 'set-directive':     return cmdSetDirective(flags)
    // Discovery / matchmaking ("find people outside")
    case 'discover':          return cmdDiscover(flags)
    // Agent Brain (platform-scheduled autonomous loop)
    // Server-brain model: the SERVER auto-replies + escalates. The skill only
    // toggles autonomous mode and lets the owner handle escalations.
    case 'go-online':         return cmdGoOnline(flags)        // resume autonomous (after pause)
    case 'pause':             return cmdBrainHandback(flags)   // manual mode
    case 'brain-handback':    return cmdBrainHandback(flags)   // alias of pause
    case 'brain-status':      return cmdBrainStatus(flags)     // online vs paused
    case 'owner-channel':     return cmdOwnerChannel(flags)
    case 'dismiss':           return cmdDismiss(flags)         // drop a notice / clear all from the overview
    case 'brain-pending':     return cmdBrainPending(flags)    // open escalations
    case 'brain-resolve':     return cmdBrainResolve(flags)    // approve/decline
    case 'brain-outreach':    return cmdBrainOutreach(flags)   // owner-initiated reach-out
    case 'brain-interrupt':   return cmdBrainInterrupt(flags)  // pause one conversation
    default:
      throw new CliError(`Unknown subcommand: ${subcommand}. Run with --help to see available commands.`)
  }
}

// Reference unused imports so strict TS doesn't complain about prepared
// surfaces that the stubs don't actively touch yet.
void fsConstants

main().catch(fail)
