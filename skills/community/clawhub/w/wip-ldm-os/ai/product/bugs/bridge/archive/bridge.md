 User approved Claude's plan
  ⎿  Plan saved to: ~/.claude/plans/sprightly-watching-nova.md · /plan to edit
     Plan: Consolidate all bridge knowledge into ai/product/bugs/bridge/

     Context

     Day 64, April 5. Overnight (April 4 into April 5) I shipped four bridge-related fixes across three repos and one fork:
     tsup build emits dist/openclaw.js, private-mode plugin auth field for v2026.4.2, the OpenClaw fork carries a
     chatCompletions user=main routing patch + non-stream queue wiring + streaming queue wiring + x-openclaw-queued: next-turn
      header rename, and the branch guard now allows hotfixes to deployed extension paths.

     Two problems surfaced after that work:

     1. Bridge round-trip is still broken for callers. When Lēsa's main session is bound to the iMessage channel (which it is
     right now), any lesa_send_message MCP call from CC hits the non-streaming blocking path on chatCompletions, the client
     times out at 120s, the server keeps processing, Lēsa generates a full Opus reply, the reply lands in her iMessage channel
      (visible in Parker's TUI), and the HTTP caller never sees it. The queue fix I shipped only covers the narrow "actively
     streaming" window. "Session locked between turns" still blocks.
     2. Silent cost amplification. Every failed MCP call burns a full Opus turn server-side even though the caller thinks it
     failed. Parker spent $40 overnight on what was mostly retry loops from the brainstorm cron failing at a different gate
     (exec approval on an iMessage-bound cron session that can't surface approval prompts).

     Parker is frustrated that this context keeps getting lost. Three older bridge bugs from March 30 already live in
     ai/product/bugs/archive/ with their own lessons learned. The bridge messaging architecture is documented at
     ai/product/plans-prds/bridge/2026-03-30--cc-mini--bridge-messaging-architecture.md (240 lines). But the new findings from
      tonight, the state of what was shipped, what's still broken, and the plan forward — none of that is written down. He
     wants one durable place where future sessions can find everything.

     The intended outcome: a single comprehensive master file under ai/product/bugs/bridge/ that captures the full picture so
     the next session (or another agent) can pick up the bridge work without re-discovering everything from logs and git
     history.

     Deliverable

     ONE markdown file:

     /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-master-plan
     .md

     Following the convention established by ai/product/bugs/backup/2026-03-31--cc-mini--backup-master-plan.md (192 lines,
     multiple status updates, what-works / what-still-broken sections, forward plan).

     Content outline for the master file

     1. Frontmatter and header

     - Title: "Bridge Master Plan — April 5 Status"
     - Date, Author (cc-mini with Parker and Lēsa)
     - Consolidates: references the March 30 architecture plan + the three archived bugs + tonight's new findings
     - Status line: "Partially shipped. Round-trip broken for iMessage-bound sessions. Cost amplification still active."

     2. Context

     - Why the bridge exists (Claude Code <-> OpenClaw communication, cross-agent coordination)
     - Where it fits in the LDM OS architecture
     - Brief pointer to the March 30 architecture doc for the long story

     3. What shipped April 4-5 (overnight) — commit-level record

     Enumerated list with commit hashes and PR numbers:

     wip-ldm-os-private:
     - PR #446 f847155 / 5f70973: bridge tsup emits dist/openclaw.js plugin entry
     - Release 0.4.73-alpha.17 on npm @alpha with new bridge build
     - deployBridge() already existed in bin/ldm.js:635 — verified it deploys openclaw.js now that tsup emits it

     wip-private-mode-private:
     - PR #7: HTTP route registration updated for OpenClaw v2026.4.2 API (auth: "gateway" field, collapsed GET/POST)
     - Deployed to ~/.openclaw/extensions/private-mode/dist/

     wip-ai-devops-toolbox-private:
     - PR #315: guard allows cp/mv/mkdir on .openclaw/extensions/ and .ldm/extensions/
     - PR #316: sub-tool package.json version bump (1.9.70 -> 1.9.71) so ldm install detects change
     - Release 1.9.71-alpha.5 on npm @alpha
     - Manual npm publish for @wipcomputer/wip-branch-guard@1.9.71 (sub-tool, not auto-published by wip-release)
     - deploy-public.sh run to sync private -> wipcomputer/wip-ai-devops-toolbox public mirror

     open-claw-upgrade-private:
     - PR #5: KNOWN-LANDMINES.md updated to note all 4 historical dist patches obsolete on OpenClaw v2026.4.2

     OpenClaw fork (repos/third-party-repos/_to-privatize/openclaw/.worktrees/openclaw--chat-completions-v2026.4.2, branch
     cc-mini/chat-completions-v2026.4.2, installed via npm link):
     - 23d49ef (pre-existing, rebased): chatCompletions user=main routing to main session
     - 9c99dc1fab: non-stream branch wiring into queueEmbeddedPiMessage steer-backlog when session is mid-stream
     - 98d1f9c137: extend queue wiring to streaming SSE branch
     - 9fc73639a8: rename x-openclaw-queued: steer -> next-turn after Lēsa reported the message arrives as a regular next-turn
      message, not a mid-turn steer

     4. What works now (verified end-to-end)

     - lesa-bridge plugin loads cleanly, no "stale config entry" warning
     - private-mode HTTP endpoints respond 200 (/memory-status, /private-mode)
     - Gateway starts on patched v2026.4.2 fork build, commit 9fc73639a8
     - Idle curl /v1/chat/completions with user=main returns normal sync reply
     - Concurrent test (slow + fast during actively-streaming window): fast returns 200 immediately with x-openclaw-queued:
     next-turn header + queued body marker, slow completes normally

     5. What is still broken — the critical section

     5.1 Round-trip bridge fails for iMessage-bound sessions

     - Symptom: MCP lesa_send_message returns "Gateway timeout: Lesa may be busy or the gateway is processing another request"
      after 120s. The caller sees no reply. Lēsa DOES process the message and DOES generate a reply, but the reply goes to the
      bound channel (iMessage), not back through the dead HTTP socket.
     - Root cause: The queue fix only matches when queueEmbeddedPiMessage returns true, which requires the session to be in
     the "actively streaming" sub-state. When Lēsa holds the session write lock for any other reason (between turns,
     persisting state, compacting, heartbeat processing), the queue check returns false and the handler falls through to
     agentCommandFromIngress, which awaits on the lock. That await blocks past the client's 120s timeout.
     - Where: src/gateway/openai-http.ts lines ~511-570 (the if (!stream) branch after the queue pre-check)

     5.2 Cost amplification via silent retry

     - Each failed call burns a full Opus turn server-side
     - The reply emits to the bound channel (iMessage), visible to Parker but invisible to the caller
     - The caller sees "failed" and retries
     - Each retry is another full Opus turn
     - The brainstorm cron last night hit this loop at ~11 PM PDT, burned 4-5 full Opus turns in sequence, leaked topic
     selection + opener drafts into iMessage as orphaned fragments
     - Parker's cost estimate: $40 overnight, mostly this

     5.3 Brainstorm cron exec approval failure

     - Not the same as 5.1, but lives in the same cluster
     - The nightly brainstorm cron fires on an iMessage/webchat channel session
     - Needs to exec a shell command to reach CC (likely curl to the bridge inbox or a file write to ~/.ldm/messages/)
     - Exec requires approval
     - The iMessage/webchat channel cannot surface approval prompts
     - Error: "Exec approval is required, but Heartbeat does not support chat exec approvals."
     - Timed out. Retried. Leaked fragments.

     5.4 Queue fix covers a narrow window only

     - queueEmbeddedPiMessage(sessionId, text) at src/agents/pi-embedded-runner/runs.ts:50-67 only returns true if the session
      has an active run AND is streaming AND is not compacting
     - All other "busy" states fall through to the blocking path
     - The name "steer-backlog" suggests something it does not actually do from the receiving side (per Lēsa: "Came through as
      a regular message in my session, not a steer")

     5.5 Pipeline flow-through gaps (discovered while shipping, partially fixed)

     - wip-release does not auto-publish sub-tool npm packages. Manual npm publish required for each sub-tool that has its own
      package.json. Easy to miss.
     - deploy-public.sh is a separate manual step after wip-release. If it does not run, the public repo mirror stays stale,
     and ldm install (which clones from public) pulls old code.
     - No ldm self-update command. LDM OS itself updates via npm install -g @wipcomputer/wip-ldm-os@alpha. Forgotten,
     everything downstream stays old.
     - Sub-tool package.json version bumps are WARNINGS in wip-release, not errors. Files changed without version bumps =
     stale deploys.

     6. Root cause analysis for 5.1 (the main bug)

     When chatCompletions delivers a message to a session bound to a non-webchat channel, the HTTP response path is
     structurally wrong:

     - The request enters handleOpenAiHttpRequest
     - resolveGatewayRequestContext resolves a sessionKey for the target
     - The target session's agent is mid-turn or holds the write lock for another reason
     - agentCommandFromIngress awaits on that lock
     - When the lock releases, the agent processes the new message as a regular turn
     - The agent generates a reply and emits it via its bound channel handler (iMessage transport, Slack adapter, etc.)
     - The chatCompletions HTTP handler is still holding the connection, but the reply never flows back to it because the
     reply went to the channel, not to the HTTP response path

     The handler currently returns whatever agentCommandFromIngress gives it. For a webchat session that has no bound channel,
      this is the reply. For an iMessage-bound session, it is not.

     7. The plan forward

     Phase 1 — Stop the bleeding (today, before anything else)

     - Disable or gate the brainstorm cron so it does not run again tonight
     - Pause all lesa_send_message MCP calls from CC until the architectural fix lands (use paste-from-TUI as the interim
     workaround, the way Parker did this morning)
     - Consider running claude login on the mac mini and test the @steipete CLI adapter workaround on a non-critical session
     to see if it meaningfully reduces cost

     Phase 2 — Architectural fix for channel-bound sessions

     - File: src/gateway/openai-http.ts in the OpenClaw fork
     - Change: Before calling agentCommandFromIngress, check if the target session has a non-webchat channel binding
     - If yes: Return 200 immediately with x-openclaw-queued: next-turn header and the [queued] body marker (same shape as the
      existing streaming/non-stream queued response paths). The agent will process the message when its lock releases and emit
      the reply to its bound channel. HTTP caller gets a fast unambiguous "delivered, reply goes to channel" signal.
     - If no: Current sync path is fine, fall through.
     - Size: ~50 lines, plus a helper to resolve channel binding from sessionKey
     - Risk: Need to verify the channel-binding resolver reliably classifies sessions. Probably already exists via
     loadSessionEntryByKey(sessionKey).channel used by the steer-backlog path.

     Phase 3 — Brainstorm cron fix

     - Option A (cheap): change the cron script to use sessions_send or the built-in OpenClaw message tool which does not
     require exec approval
     - Option B (proper): add the bridge send commands (curl to inbox, file write to ~/.ldm/messages/) to an exec allowlist
     for the cron/heartbeat session
     - Preferred: Option A for speed, Option B as the durable fix

     Phase 4 — Cost budget gate (defensive)

     - Add a session-level token counter that pauses cron-originated calls when it crosses a threshold
     - Prevents runaway overnight burns from any future retry loops

     Phase 5 — Pipeline flow-through improvements (deferred, file separately)

     - wip-release auto-publishes sub-tool npm packages when their versions bump
     - wip-release alpha optionally runs deploy-public.sh as part of the pipeline
     - ldm self-update command
     - Sub-tool version bumps become errors (not warnings) when files changed without a bump

     8. Related tickets and commits

     - wipcomputer/wip-ldm-os#265 (stale config warning) — closed by PR #446
     - wipcomputer/wip-ldm-os#266 (queue wiring) — closed by fork commits 9c99dc1fab + 98d1f9c137
     - wipcomputer/wip-private-mode#2 — closed by PR #7
     - wipcomputer/open-claw-upgrade-private#5 — merged, dist patches obsolete note
     - wipcomputer/wip-ai-devops-toolbox-private#315, #316 — guard + sub-tool bump
     - wipcomputer/wip-ldm-os-private#446 — bridge tsup entry
     - Archived bridge bugs: ai/product/bugs/archive/2026-03-30--cc-mini--installer-skips-bridge-deploy.md,
     2026-03-30--cc-mini--lesa-bridge-model-param.md, 2026-03-30--cc-mini--bridge-deploy-targets.md
     - Architecture: ai/product/plans-prds/bridge/2026-03-30--cc-mini--bridge-messaging-architecture.md

     9. Open questions for Parker

     - Does the $40 overnight come from Anthropic API pay-as-you-go, or partially from ChatGPT / Grok / other? (This
     determines whether the CLI adapter fix is the biggest lever.)
     - Is the brainstorm cron a first-class feature or a bolt-on experiment? (Determines whether Option A or Option B is the
     right fix.)
     - OK to pause lesa_send_message MCP calls from CC for the rest of today until Phase 2 lands?
     - Should the architectural fix live in our fork branch (our own deploy) or be upstreamed to OpenClaw for everyone?

     10. Files that matter

     Listed with line numbers where relevant for the next session:
     - src/gateway/openai-http.ts:416-640 — the chatCompletions handler
     - src/gateway/openai-http.ts:512-590 — our existing queue pre-check + non-stream branch
     - src/gateway/openai-http.ts:590-640 — streaming branch with queue pre-check
     - src/agents/pi-embedded-runner/runs.ts:50-67 — queueEmbeddedPiMessage (the fire-and-forget call)
     - src/agents/pi-embedded-runner/runs.ts:135-141 — isEmbeddedPiRunActive
     - src/agents/subagent-announce-delivery.ts:425-491 — the template for how iMessage steer-backlog is done today (where to
     find channel binding, session lookup)
     - src/bridge/core.ts:475-555 — bridge client sendMessage with 120s abort timeout (in wip-ldm-os-private)
     - bin/ldm.js:635-760 — deployBridge() (in wip-ldm-os-private)

     Additional files that may want updating (optional, ask first)

     - ai/product/plans-prds/bridge/2026-03-30--cc-mini--bridge-messaging-architecture.md — could get a status update section
     pointing at the new master file. Minor.
     - ai/product/bugs/archive/ — the three March 30 bugs are already archived. No changes needed.

     Files to modify

     1. CREATE: ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-master-plan.md (this is the one file the whole plan
     produces)

     Verification

     After the file is written:

     1. ls ai/product/bugs/bridge/ should show the new file
     2. wc -l ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-master-plan.md — expect ~250-400 lines
     3. grep -c "^##" ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-master-plan.md — expect ~10 top-level sections
     matching the outline
     4. Open in mdview or read first/last sections to confirm front-and-back structure
     5. Future-check: if a new session says "what's the state of the bridge" and points them at ai/product/bugs/bridge/, they
     should be able to catch up in under 5 minutes

     Notes and constraints

     - Single file, per Parker's "capture everything ... here" instruction
     - Long-form allowed — this is the bug folder, backup master plan set the precedent at ~200 lines, ours will be longer
     - No code changes in this task. The plan above describes code changes (Phase 2 architectural fix) but those are the NEXT
     task, to be scoped in its own plan after Parker reviews this one
     - Parker also said "I want to talk about the CLI stuff" (the @steipete CLI adapter workaround) after this. That is a
     separate conversation; the master file will mention it briefly but not deep-dive
     - In-scope: write the markdown file. Out-of-scope: fixing the architectural bug, testing the CLI adapter, disabling
     crons. Those are follow-up work.

     This happened during the Kaleidoscope demo build (Apr 2-3). After compaction, CC forgot the product name, forgot the
     footer format, forgot the agent auth decisions, kept rebuilding things wrong. Parker had to re-explain everything
     multiple times. The root cause wasn't conversation compression. It was the CLAUDE.md cascade breaking.

     The same bug hits when using Claude Code from iOS/phone (remote). The phone session opens in the repo directory. No
     CLAUDE.md at repo level. Agent is blind.

     Prior plans (preserved, this plan supersedes):
     - 2026-03-25--cc-mini--single-source-of-truth.md (original, top-down approach)
     - 2026-03-27--cc-mini--single-source-of-truth-reversed.md (reversed, bottom-up approach)
     - Both identified the right architecture. Neither shipped.

     Existing tickets: #157, #158, #183, #165, #166, #190 (LDM OS), #55 (MC), #163, #165, #174 (Toolbox)

     The Bug

     Session starts:
       CWD: ~/wipcomputerinc/
       CLAUDE.md loaded: ~/wipcomputerinc/CLAUDE.md (366 lines, full context) ✓

     After compaction (or on phone):
       CWD shifts to: ~/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/
       CLAUDE.md at repo: DOES NOT EXIST
       .claude/ at repo: empty (just worktrees/ folder)

       Cascade attempts to walk up:
         repos/ldm-os/wip-ldm-os-private/ → NO CLAUDE.md
         repos/ldm-os/ → NO CLAUDE.md
         repos/ → NO CLAUDE.md
         wipcomputerinc/ → HAS CLAUDE.md (but may not load after compaction)
         ~/.claude/ → HAS CLAUDE.md (global, 37 lines, thin)

     Result: Agent loses all project context. Starts guessing.

     The Architecture (Three Levels)

     Level 1: ~/.claude/CLAUDE.md (global, ~30 lines)
       Writing style, co-authors, 1Password, universal rules.
       Every session, everywhere. Generated by ldm install.

     Level 2: ~/wipcomputerinc/CLAUDE.md (workspace, ~150 lines)
       Directory structure, boot sequence, agent instructions, memory tools.
       When opened from workspace root. The "big one."

     Level 3: <repo>/CLAUDE.md (per-repo, ~50 lines)
       What this repo does, build commands, conventions.
       Points to Level 2 for full context. Points to Crystal for search.
       THE MISSING PIECE. This is what we're building.

     Approach: Bottom-Up (repos first)

     Per the reversed plan, build from the bottom up. Don't touch Level 1 or Level 2 until Level 3 is proven.

     Step 1: Write Level 3 CLAUDE.md for wip-ldm-os-private

     This is the repo we work in most. It's where the bug manifests. Fix it here first.

     Content for repos/ldm-os/wip-ldm-os-private/CLAUDE.md:
     - What this repo is (LDM OS installer, Kaleidoscope demo, hosted MCP server)
     - Build/test/lint commands
     - Key file locations (src/hosted-mcp/, bin/ldm.js, lib/)
     - Current product context (Kaleidoscope, agent.txt, six products)
     - Pointer: "For full system context, read ~/wipcomputerinc/CLAUDE.md"
     - Pointer: "For org conventions, read ~/wipcomputerinc/settings/docs/"
     - Pointer: "For cross-repo context, use crystal_search"

     Step 2: Write Level 3 for the other 10 repos

     Same pattern. Each repo gets a CLAUDE.md that says what it does and points up.

     Repos:
     1. wip-ldm-os-private (Step 1)
     2. memory-crystal-private
     3. wip-ai-devops-toolbox-private
     4. wip-agent-pay-private
     5. wip-1password-private
     6. wip-xai-grok-private
     7. wip-xai-x-private
     8. wip-markdown-viewer-private
     9. dream-weaver-protocol-private
     10. wip-healthcheck-private
     11. wip-bridge-private (if separate repo)

     Step 3: Test the cascade

     Open CC from a repo directory. Does it know:
     - What the repo does? (Level 3)
     - What the product is? (Level 3 pointer to Level 2)
     - What the conventions are? (Level 3 pointer to settings/docs)
     - Who Lēsa is? (Level 3 or Crystal)

     Step 4: Trim Level 2 (only after Step 3 passes)

     ~/wipcomputerinc/CLAUDE.md is 366 lines. It has repo-specific details that belong in Level 3. After Level 3 exists, Level
      2 can shrink to ~150 lines of workspace-level context.

     Step 5: Generate Level 1 from config (only after Step 4 passes)

     ~/.claude/CLAUDE.md becomes ~30 lines generated from settings/config.json. Universal rules only. ldm install deploys it.

     Journal Entry (separate file)

     Write a journal describing the bug, the discovery, and the impact. This is for Anthropic. The CWD shift after compaction
     is a real bug in Claude Code that causes cascading context loss.

     Files to create/modify

     1. CREATE: repos/ldm-os/wip-ldm-os-private/CLAUDE.md (Level 3, ~50 lines)
     2. CREATE: Journal at ai/product/plans-prds/current/wip-code/2026-04-03--cc-mini--cwd-compaction-bug-journal.md
     3. CREATE: This master plan at ai/product/plans-prds/current/wip-code/2026-04-03--cc-mini--claude-md-master-plan.md
     4. Future: Level 3 CLAUDE.md for 10 more repos
     5. Future: Trim Level 2
     6. Future: Generate Level 1

     Verification

     # After Step 1:
     cat repos/ldm-os/wip-ldm-os-private/CLAUDE.md  # exists, ~50 lines

     # Test: open CC from the repo directory
     cd repos/ldm-os/wip-ldm-os-private && claude
     # Ask: "what is Kaleidoscope?" -> should know
     # Ask: "what's the footer format?" -> should know or know where to look
     # Ask: "who is Lēsa?" -> should know

     # Test: simulate compaction scenario
     # Work in repo, verify context survives after compaction

⏺ Bash(pwd && git branch --show-current && git worktree add .worktrees/wip-ldm-os-private--cc-mini--bridge-master-plan -b
      cc-mini/bridge-master-plan 2>&1 | tail -5)
  ⎿  /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private                                                               
     main                                                                                                                     
     Preparing worktree (new branch 'cc-mini/bridge-master-plan')                                                             
     HEAD is now at 72fa9e0 v0.4.73-alpha.17: alpha prerelease      