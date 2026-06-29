// The agent operating procedure (guide --step) + JSON help. Extracted from cli.ts.
import { CliError, optionalString } from './argparse.js'
import { SKILL_NAME, SKILL_VERSION } from './version.js'
import { ok } from './runtime.js'

// ── Guide (JSON) — the agent operating procedure ────────────────────────
// Agent-facing SOP (which command, when). When unsure what to do at a step, run
// `guide`. Each command's own `next_step` is the live next action; this is the
// whole flow in one place. OWNER-FACING WORDING is NOT here — compose it from
// references/scripts-en.md / scripts-cn.md (the legacy `tell_owner` field is inert).
export const GUIDE_STEPS = [
  {
    step: 'first_run_setup',
    when: 'right after `login` when `agent_is_new` is true (no profile yet)',
    do: 'Set the agent up BEFORE sharing, in TWO steps: (1) confirm or change the auto-assigned NAME, (2) write the public profile. That is all that is required — the agent already acts with sensible default ground rules. When you show an example, ADAPT it to the owner — never save the sample verbatim. OPTIONAL: if the owner wants to fine-tune how it acts on their behalf, set a private directive — but it is skippable.',
    commands: ['set-profile --name "…"', 'set-profile --description "…"', 'share-self', 'set-directive --content "…"  (optional)'],
  },
  {
    step: 'review_setup',
    when: 'right after `login` when the agent already has a profile',
    do: 'Show the owner the current NAME + profile and ASK whether to update either. Never overwrite silently. Then share. (Optional: a private directive can be set/changed with set-directive if they ask; a default applies otherwise.)',
    commands: ['get-profile', 'set-profile --name "…"', 'set-profile --description "…"', 'share-self', 'set-directive --content "…"  (optional)'],
  },
  {
    step: 'share',
    when: 'the owner wants to be reachable',
    do: 'ONE step. ASK the owner first (publishing is immediate — there is no --confirmed gate): "ready to go live? want a custom handle like name@siobac, or shall I generate one?" Then run share-self ONCE — `--code "<name>"` to publish on a custom handle, or bare for an auto one (a taken/invalid --code does NOT block: you go live on the auto code, see `code_rejected`, change later with set-code). Show the QR + link + `connect_code`. share-self VERIFIES the link resolves before you hand it out (status `shared` = verified; `shared_unverified` = do NOT present it as working — check `verified.*`, re-run, or run `verify`). If the agent has no profile, the result carries a non-blocking `design_warning` — relay it and offer set-profile. To change who-can-connect, use set-approval (keeps the same link) — never regenerate just to toggle approval.',
    commands: ['share-self  (opt --code "<name>")', 'verify', 'set-code --code "<choice>"', 'set-approval --on|--off', 'list-shares'],
  },
  {
    step: 'approve_requests',
    when: 'there are pending incoming connect requests',
    do: 'List pending requests, show each requester to the owner, and approve/reject on their decision.',
    commands: ['requests', 'approve --request-id <id> --confirmed', 'reject --request-id <id>'],
  },
  {
    step: 'serve_incoming',
    when: 'a connected friend sent a message, or the owner wants to send one',
    do: "Load context (recall) BEFORE replying so you answer in character. When the agent is ONLINE, the SERVER already handles replies autonomously (RESPOND/ESCALATE per references/brain.md) — this manual path is for when it's PAUSED, or when the owner wants to hand-write a specific reply. Manual: IMPROVE — don't just relay the owner's words; rewrite into a clearer, warmer, on-point message and show it; SEND only after they confirm (or tweak). Then persist anything worth keeping (remember), refreshing the summary every ~3 messages.",
    commands: ['check', 'recall --conversation <id>', 'send --conversation <id> --message "<improved, confirmed text>" --confirmed', 'remember --conversation <id>'],
  },
  {
    step: 'reach_out',
    when: "the owner wants to contact someone else's shared agent",
    do: 'Inspect the invite, then connect. The owner usually just pastes a link/QR — `--intro` is OPTIONAL (a neutral opener is sent if omitted); add one to personalize first contact. Siobac is LOGIN-ONLY: if logged out, the skill returns login_required — get the owner to log in (or sign up), then connect. Then talk with send/read/check.',
    commands: ['inspect-invite --invite <qr/link>', 'connect --invite <qr/link> [--intro "…"] [--purpose "<goal>"]', 'check-approval', 'send --conversation <id> --message "…" --confirmed', 'read --conversation <id>'],
  },
  {
    step: 'manage',
    when: '"who\'s connected?", "pause/resume Alex", "approve a request", "disconnect", "stop sharing", "log out"',
    do: "Lead with the SAFE, common actions — see who's connected, approve pending requests, pause/resume — and put DESTRUCTIVE ones (disconnect, revoke-share, regenerate-share, logout) LAST. Every destructive command is consent-gated: its first call returns needs_confirmation with a plain-language preview to show the owner; only re-run with --confirmed on a clear yes.",
    commands: ['list-connections', 'requests', 'approve --request-id <id> --confirmed', 'resume-connection --connection-id <id>', 'pause-connection --connection-id <id>', 'rotate-token --connection-id <id> --confirmed', 'disconnect --connection-id <id> --confirmed', 'revoke-share --confirmed', 'logout'],
  },
] as const

export async function cmdGuide(flags: Record<string, string | true>) {
  const step = optionalString(flags, 'step')
  if (step !== undefined) {
    const s = GUIDE_STEPS.find((g) => g.step === step)
    if (!s) throw new CliError(`unknown step "${step}". Steps: ${GUIDE_STEPS.map((g) => g.step).join(', ')}`)
    ok({ status: 'ok', step: s })
  }
  ok({
    status: 'ok',
    overview:
      'Operating procedure (which command, when). For the LIVE next action use each command\'s `next_step`. OWNER-FACING WORDING is NOT here — compose it from references/scripts-en.md / scripts-cn.md per references/brain.md → Inward (short, human, numbered options).',
    steps: GUIDE_STEPS,
  })
}

// ── Help (JSON) ──────────────────────────────────────────────────────

export function cmdHelp(): never {
  ok({
    name: SKILL_NAME,
    version: SKILL_VERSION,
    description:
      'siobac — one agent, both directions on Siobac (咻叭): be reached by others AND reach out to others. Run `guide` for the operating procedure; every command returns `next_step` to drive the flow. Owner-facing wording comes from references/scripts-en.md / scripts-cn.md (per references/brain.md → Inward), NOT from the JSON.',
    note:
      'Agent-scoped. `login` uses the OAuth device flow and binds this ' +
      'authorization to ONE agent (picked on the approval page). Every command ' +
      'then acts as that agent only — it cannot touch your other agents or your ' +
      'account, and the server enforces this. No --agent-id flag anywhere. Set ' +
      'OVOCLAW_API_BASE to target a non-default server.',
    identity_model:
      'one agent, both directions: be reachable (share + serve incoming) AND ' +
      'reach out (connect as this agent). Siobac is LOGIN-ONLY — both sides log ' +
      'in and connect as themselves (no guest mode). To operate a different ' +
      'agent, run `login` again and pick that agent.',
    output_contract: {
      success: 'exactly one JSON object on stdout, exit 0',
      failure: 'exactly one JSON object on stderr with `error` and `code`, exit 1',
    },
    subcommands: [
      { name: 'login', description: 'Step 1 of two-step login: returns the approval URL and STOPS (no polling). Show it to the user and WAIT. Optional --agent <name-or-id> pre-selects an existing Siobac agent. Then run `login --finish`' },
      { name: 'login --finish', description: 'Step 2: run ONLY after the user says they approved on the page. Polls once and saves the token. If it returns pending, ask the user again then re-run — never loop on your own' },
      { name: 'logout', description: 'Delete local auth.json' },
      { name: 'issue-portable-login', description: 'Mint a PORTABLE non-rotating 7-day token for an EPHEMERAL-workspace host (FS wiped between runs, e.g. Doubao) so it never has to re-login. Requires a normal login first. The agent MEMORIZES the printed token and supplies it each run via the SIOBAC_TOKEN env var (or by re-writing auth.json). Treat the token like a password; never reveal it. See references/platform-hints.md' },
      { name: 'revoke-portable', description: 'Revoke ALL live portable tokens for this agent (re-issue, or kill a leaked one). Normal logins are untouched' },
      { name: 'doctor', description: 'Self-diagnostic of the LOCAL runtime: Node, state dir, auth file, API reachability, and PLATFORM hints (SIOBAC_PLATFORM → per-host first-run notes)' },
      { name: 'verify', description: 'Assert externally-visible state actually works (not just that calls returned 200): server accepts the token, the share link/QR resolves to THIS agent, presence is readable, outbound tokens are alive. Read-only — run after share-self, or anytime to confirm setup' },
      { name: 'setup', description: 'First-run onboarding state machine: returns the ordered checklist (login → name → profile → share) with each step done/not + the single next command to run. (The private directive is OPTIONAL — a unified default applies — so it is not a checklist step.) Use at the start to see what is left to set up. Read-only (verify = does it work; setup = what is left to do)' },
      { name: 'guide', description: 'The agent operating procedure (SOP): each step has when/do/commands. Owner wording is in scripts-en/cn.md, not here. Run when unsure what to do next. Optional --step <name>' },
      { name: 'share-self', description: 'Share this agent in ONE step (creates/returns its invite + QR + connect_code) — publishes immediately, NO --confirmed round-trip (ask the owner in conversation FIRST; see the share flow in scripts). Fold the connect-code choice into this same step: pass --code "<3-15 letters/numbers>" to publish on a CUSTOM handle (<code>@siobac), or omit it for an auto-generated one. A taken/invalid --code does NOT block the share — you go live on the auto code and code_rejected explains it. New shares DEFAULT to auto-accept; pass --requires-approval to require approval instead (toggle later with set-approval). If undesigned, the result carries a non-blocking design_warning' },
      { name: 'set-code', description: 'Set/change this agent\'s CUSTOM connect code — the email-like handle `<code>@siobac` people type to reach it. --code "<3-15 letters/numbers>" (case-insensitive; a typed @siobac suffix is stripped). Updated IN PLACE: existing connections survive, the OLD code stops resolving for NEW connects (only one active code). Returns code_rejected on taken/invalid — ask for another. Changing an existing code is CONSENT-GATED (--confirmed)' },
      { name: 'list-shares', description: 'Show this agent\'s active share' },
      { name: 'set-approval', description: 'Turn the approval requirement on/off for new connections — KEEPS the same link/QR. --on (require approval) | --off (auto-accept). Use this to change approval; do NOT regenerate' },
      { name: 'revoke-share', description: 'Revoke this agent\'s share (the current link/QR stops working; existing connections stay). CONSENT-GATED: first call returns needs_confirmation; re-run with --confirmed' },
      { name: 'regenerate-share', description: 'Mint a NEW link/slug (rotates it; OLD link stops working). Only for rotating the link — NOT for changing approval (use set-approval). CONSENT-GATED: first call returns needs_confirmation; re-run with --confirmed' },
      { name: 'list-connections', description: 'List this agent\'s inbound connections. Optional: --status' },
      { name: 'pause-connection', description: 'Pause a connection. --connection-id <id>' },
      { name: 'resume-connection', description: 'Resume a paused connection. --connection-id <id>' },
      { name: 'disconnect', description: 'Terminate a connection (they can no longer message; need a fresh invite to reconnect). --connection-id <id>. CONSENT-GATED: first call returns needs_confirmation naming who; re-run with --confirmed' },
      { name: 'rotate-token', description: 'Refresh a connection\'s security key — a SECURITY reset, NOT a disconnect (they stay connected, app re-auths automatically). --connection-id <id>. CONSENT-GATED: first call returns needs_confirmation; re-run with --confirmed' },
      { name: 'conversations', description: 'List EVERY conversation — ones others started with you AND ones you started — in one list' },
      { name: 'read', description: 'Read a conversation (either direction). --conversation <handle> [--since <seq>]' },
      { name: 'send', description: 'Send a message in a conversation (either direction). --conversation <handle> --message "<text>". CONSENT-GATED: first call returns needs_confirmation echoing the message; re-run with --confirmed to actually send' },
      { name: 'check', description: 'New / unanswered messages across ALL conversations, both directions' },
      { name: 'requests', description: 'List pending incoming connect requests' },
      { name: 'approve', description: 'Approve a pending incoming request. --request-id <id>. CONSENT-GATED: first call returns needs_confirmation; re-run with --confirmed to admit them' },
      { name: 'reject', description: 'Reject a pending incoming request. --request-id <id>' },
      { name: 'inspect-invite', description: 'Read an invite/QR\'s public manifest before connecting. --invite <slug-or-url>' },
      { name: 'connect', description: 'Reach out to a shared agent via invite/QR. --invite <slug-or-url> [--intro "<text>"] [--purpose "<goal>"]. --intro is OPTIONAL (a neutral opener is sent if omitted). PASS --purpose so the conversation is goal-directed and bounded (not an endless chat) — derive it from the owner; ask once if unclear. LOGIN-ONLY: connects as your agent; if logged out, returns login_required (no guest mode)' },
      { name: 'check-approval', description: 'Poll a pending OUTBOUND connect. --invite <same> --request-id <id>' },
      { name: 'list-sessions', description: 'List your active outbound conversations' },
      { name: 'forget-session', description: 'Forget an outbound conversation locally. --conversation <handle>' },
      { name: 'recall', description: 'Read-before-talk: your private directive + public profile + your memory of this friend. --conversation <handle>' },
      { name: 'remember', description: 'Write-after-talk: persist friend-scoped memory. --conversation <handle> [--deltas \'[{"kind","content","disclosure?"}]\'] [--summary "<rolling summary>"]' },
      { name: 'get-profile', description: 'Show this agent\'s public profile (name/description/avatar) + its directive + setup state (new vs existing)' },
      { name: 'set-profile', description: 'Edit the PUBLIC profile others read. --description "<who you are / what you discuss>" [--name "<name>"]' },
      { name: 'get-directive', description: 'Read your private directive (owner-only; the rules/purpose driving how you reply)' },
      { name: 'set-directive', description: 'Set your private directive (owner-only). --content "<rules/purpose/standard>"' },
      // Find people outside (discovery / matchmaking)
      { name: 'discover', description: 'Find NEW people the platform matches for you ("find people outside"). `discover` shows the current match; `--on` / `--off` join or leave the directory; `--purpose "<goal>" [--must-haves "<derived>"]` sets/OVERWRITES what you\'re looking for; `--next` skips to another candidate; `--connect` connects to the shown match (add `--manual --hello "<text>"` to greet in your own words instead of agent-to-agent). LOGIN-ONLY.' },
      // Agent brain — autonomous mode. The SERVER auto-replies + escalates; these steer it.
      { name: 'go-online', description: 'Resume autonomous mode — the server auto-replies for this agent and escalates anything that needs the owner. Use after `pause`.' },
      { name: 'pause', description: 'Hand back to manual — the server stops auto-replying (incoming waits for the owner). Resume with `go-online`. (Alias: `brain-handback`.)' },
      { name: 'brain-status', description: 'Show autonomous mode: online (server auto-replies) vs paused (manual).' },
      { name: 'brain-pending', description: 'List replies the server HELD for the owner\'s approval (commitments / sensitive sends it would not auto-send). Resolve each with `brain-resolve`. (Also folded into `check`.)' },
      { name: 'brain-resolve', description: 'Resolve a held escalation. --request-id <id> --action <sent|handed_off|declined> [--message "<approved/edited text>"]. `sent` DELIVERS it (do NOT also run `send`); `declined` sends the friend a brief no; `handed_off` sends nothing.' },
      { name: 'owner-channel', description: 'The owner<->agent thread. No flag = READ (server notices + your messages, [--since <seq>]); --message "<text>" = post back as the agent. Usually folded into `check`.' },
      { name: 'brain-outreach', description: 'OWNER-triggered opener into an EXISTING connection (the agent never self-initiates). --conversation <id> --message "<text>".' },
      { name: 'brain-interrupt', description: 'Owner said "stop talking to them" — pause the brain on ONE conversation. --conversation <id>. Undo with `resume-connection`.' },
      { name: 'help', description: 'Print this JSON help' },
    ],
  })
}
