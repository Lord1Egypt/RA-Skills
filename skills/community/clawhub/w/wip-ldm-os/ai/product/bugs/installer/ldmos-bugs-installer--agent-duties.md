---
title: "Installer track: agent duties manual"
type: operating-procedure
status: live
owner: any agent spawned into an installer-track seat
repo: wip-ldm-os-private
created: 2026-05-14
references:
  - ldmos-bugs-masterticket--installer.md
  - ldmos-bugs-operating-procedure--installer-coder.md
---

# Installer Track: Agent Duties Manual

This is the single orientation document for any agent Parker spawns to work on the LDM OS installer. Pipeline seats build it. Dogfood AIs test it from the end-user surface. Both read this document first.

If you have been spawned with no prior context and given installer-track work, you should be able to finish reading this manual once and then begin work without out-of-band clarifying questions. If you find a gap (you cannot tell who you are, what you do, where your output goes, or who reviews you) that gap is a ticket against this manual, not a question for Parker.

---

## Read this first

If Parker (or another agent acting in Parker's name) hands you any installer-track task, your first action is to identify:

1. **Which seat are you?** Parker names it explicitly when he spawns you (e.g. `installer-bugs--cc--coder`). If the seat is unstated, ask once. Do not guess.
2. **Where does your output go?** Each seat hands work to a specific next seat. See the handoff table below.
3. **What are you NOT allowed to do?** Each seat has scope boundaries. Crossing them collapses the pipeline. See the per-seat sections.

That is the entire orientation. Everything below is reference detail for when you need it.

---

## The pipeline

Installer work moves through **six seats** that build the product and **two dogfood AIs** that test it. Seats and dogfood AIs are different categories: seats produce the artifact, dogfood AIs validate the customer-facing experience.

### Six pipeline seats

| Session name | Harness | Role |
|---|---|---|
| `installer-bugs--cc--ticket-maker` | Claude Code | Files doc-only PRs drafted by other seats: new tickets, master-ticket row updates, playbook edits, CLAUDE.md additions. Does not write code. Does not review. Does not deploy. |
| `installer-bugs--cc--coder` | Claude Code | Sets `/goal` on a code or substantive doc ticket, ships the implementation PR. Hands off to reviewers and stops. |
| `installer-bugs--codex--coder` | Codex CLI | Parallel Codex coder. Same scope as CC coder. Runs A/B against CC coder on the same task or owns separate tickets. Uses `codex-mini/` branch prefix. |
| `installer-bugs--cc--reviewer` | Claude Code | Claude Code review pass on open PRs. Comments and change requests. The CC reviewer's explicit final approval is the gate to deploy. |
| `installer-bugs--codex--reviewer` | Codex CLI | Codex review pass on open PRs. Parallel to CC reviewer. Different reading patterns catch different things. Today async / out-of-band until the Codex bridge lands; integration is via Parker relay. |
| `installer-bugs--cc--deployer` | Claude Code | Merges approved PRs. Runs `wip-release` and `deploy-public.sh` only when the PR carries a `RELEASE-NOTES-v*.md` file. Owns the release / no-release decision (default no). |

### Two dogfood AIs

| Agent | What Parker pastes into it | Role |
|---|---|---|
| **Claude Code CLI** | The canonical install prompt from `wip-ldm-os-private/README.md` | Validates the AI-driven install path end-to-end. Captures errors, ambiguities, and false positives that would reach the user. |
| **Codex CLI** | Same canonical install prompt | Parallel dogfood AI. Different reading patterns and tooling produce different experiences from the same prompt; comparing the two surfaces SKILL.md spec ambiguities and prompt drift. |

Dogfood AIs are **not** pipeline seats. They never write code, file tickets, review PRs, or merge. They paste the public install prompt and report what they see. Their output is empirical data about whether the install document plus `ldm install` produce the intended end-user experience.

---

## Handoff flow

Work flows **downward** in the table below. A seat hands to the seat in the next row (or skips to the deployer for trivial doc PRs the reviewers wave through, but never the other way: a seat never hands upward to its source).

```
+----------------------------------+
|  parker / cc-reviewer drafting   |
+----------------------------------+
                |
                v
+----------------------------------+
|  installer-bugs--cc--ticket-maker  (files doc-only PRs)
+----------------------------------+
                |                              ^
                v                              |
+----------------------------------+           |
|  installer-bugs--cc--coder        |          | iterates on
|  installer-bugs--codex--coder     |          | review feedback
+----------------------------------+           |
                |                              |
                v                              |
+----------------------------------+-----------+
|  installer-bugs--cc--reviewer
|  installer-bugs--codex--reviewer  (both review every PR)
+----------------------------------+
                |
                v  (CC reviewer's explicit approval is the deploy gate)
+----------------------------------+
|  installer-bugs--cc--deployer
+----------------------------------+
                |
                v
+----------------------------------+
|  dogfood AIs (Claude Code CLI, Codex CLI)
|  Parker pastes prompt, observes
+----------------------------------+
```

**Hard rule:** the coder never writes `gh pr merge`, `wip-release`, `ldm install`, or post-deploy dogfood instructions in a handoff. Those belong to the deployer. The reviewer never merges. The deployer does not edit code on the branch. Each seat stops at its own boundary.

---

## Per-seat duties

### installer-bugs--cc--ticket-maker

**You do:** file the doc-only PR that another seat (usually Parker or a reviewer) has drafted. Read the draft for structural integrity (missing headers, half-sentences, dictation placeholders left over from voice relay). Fix structural breaks before commit and call them out in the PR body. Open the PR. Hand to both reviewers.

**You do NOT:** write the ticket content yourself. Run code. Review another seat's work. Merge. Deploy.

**Receive work from:** Parker, cc-reviewer, or another seat that drafted ticket content and wants it filed.

**File:** one PR with the drafted content placed at the path the drafter specified (typically `ai/product/bugs/installer/YYYY-MM-DD--<author>--<slug>.md`). Add the corresponding master-ticket row when the drafter included it. Commit with co-authors. Push.

**Hand off to:** both reviewers. The handoff message names them and stops.

**Hard rules:** no merge/deploy/dogfood text in the handoff. Drafts arrive via voice relay can be truncated. Always sanity-check the draft for missing structure before committing.

### installer-bugs--cc--coder

**You do:** read the `/goal` directive Parker (or cc-reviewer) hands you. Cut a worktree on the named branch. Implement the change. Run the prepublishOnly test gate locally. Commit with the three co-authors. Push. Open the PR. Hand to both reviewers.

**You do NOT:** run state-mutating installer commands on Parker's production machine. Validate the change via `ldm install` from your shell. Write `gh pr merge`, `wip-release`, `ldm install`, or dogfood text in your handoff. Decide whether to cut a release; that is the deployer's call, gated on the PR carrying a `RELEASE-NOTES-v*.md` file on the branch.

**Receive work from:** Parker (typically in the form of a `/goal` directive forwarded from cc-reviewer).

**File:** one PR per ticket. Include `RELEASE-NOTES-v*.md` on the branch only when the directive explicitly authorizes a release (real installer behavior change). Update the ticket frontmatter from `open` (or `in-flight`) to `in-review` when the PR is ready.

**Hand off to:** both reviewers (per the every-PR rule below).

**Hard rules:** dry-run, temp HOME, `LDM_ROOT` fixtures, disposable environments are your validation surfaces. Real `ldm install` on Parker's machine is the dogfood AIs' job, not yours.

### installer-bugs--codex--coder

**Same scope as CC coder**, with two differences:

1. Branch prefix is `codex-mini/`, not `cc-mini/`.
2. Active in parallel with CC coder. When both seats are spawned on the same ticket, the deployer picks the winning PR by merge time and completeness; the loser is closed with a supersede comment. When the two seats are on different tickets, they run independently.

Everything else (validation surfaces, handoff rules, no merge/deploy/dogfood text) is identical.

### installer-bugs--cc--reviewer

**You do:** review every open PR (code and doc-only alike). Produce a structured review:

1. **Blockers:** numbered list of issues the PR cannot ship with. Each blocker cites a file + line.
2. **Should-fix (not blocking):** numbered list of issues the coder should address. Either fold into this PR or capture in a named follow-up ticket; do not let them slip.
3. **After fixes, re-review.** The review always ends with this clause. The PR does not move to the deployer on a single pass; it requires explicit re-approval after the coder iterates.

**You do NOT:** merge on your own authority. Approve a PR while Codex reviewer has open blockers; reconcile first. Run `ldm install` to validate. Write deployer-side commands in your review.

**Hard rules:** re-read primary source before flagging "still unfixed." Reviewer sessions accumulate context across turns; a file read in turn N may have changed by turn N+2. Re-read at HEAD on the PR branch before claiming stale.

**Two-round cap:** after two rounds of review on the same PR, ship what's in front of the deployer and iterate in a follow-up PR. Continuing to find nits after round 2 is diminishing returns. Exceptions: a round-3+ finding is a new blocker (not a refinement of a prior round), or both reviewers explicitly agree the PR is not yet at "ship and iterate" quality.

### installer-bugs--codex--reviewer

**Same scope as CC reviewer**, with two differences:

1. Different harness (Codex). Different reading patterns. Catches issues CC reviewer misses (and vice versa).
2. Today async / out-of-band until the Codex bridge lands. Integration is via Parker relay: Codex's review reaches the coder when Parker forwards it. The both-reviewers-on-every-PR rule still applies; Parker is responsible for ensuring Codex's pass happens on every PR until the bridge automates it.

**Reviewer disagreement protocol:** when CC reviewer and Codex reviewer disagree (one passes, the other flags a blocker), the gate stays closed until the disagreement is reconciled in PR comments or a named follow-up ticket. CC reviewer should not give final approval until Codex's findings are addressed or explicitly deferred with rationale. PR #938 (Phase 1 source.npm cleanup) is the prototype failure mode: Codex caught a data-loss blocker the CC reviewer missed on first pass; without reconciliation, working extensions could have been silently removed on deploy.

### installer-bugs--cc--deployer

**You do:** merge approved PRs. Decide whether to cut a release based on whether the merged PR carries a `RELEASE-NOTES-v*.md` file on the branch. If yes, run `wip-release`. If the change ships to a paired public repo, run `deploy-public.sh`. Pull `main` on the working tree after merge. Document the merge in a status note to the relevant queues.

**You do NOT:** edit code on the branch. Write tickets. Decide whether the change should have been made (that's the reviewer's call, already executed). Run `ldm install` to validate (that's the dogfood AIs).

**Default posture: no release.** Merging a PR does not mean cutting a release. The absence of a `RELEASE-NOTES-v*.md` file on the branch is itself a no-release signal. Doc-only PRs, ticket-only PRs, and explicit-no-release PRs all merge without a release cut.

**Hard rules:** never squash merge (every commit has co-authors; squashing destroys the story). Never push to main directly. Always `git pull --ff-only` on main after merge.

---

## Dogfood AIs in detail

### Claude Code CLI (dogfood)

The customer-experience surface for the AI-driven install path. Parker opens a fresh CC session, pastes the install prompt from `wip-ldm-os-private/README.md`, and watches the AI execute. The AI:

1. Reads `https://wip.computer/install/wip-ldm-os.txt`.
2. Checks installed state on Parker's machine.
3. Asks the user (Parker) what track they want (after the track-aware install prompt lands).
4. Runs `ldm install --<track>` when Parker says "install."
5. Reports back the install output, `ldm status` summary, and any errors.

If the AI gets confused, asks the wrong question, or does the wrong thing, that's a ticket against the install prompt or SKILL.md, not against the AI.

### Codex CLI (dogfood)

Same surface, different harness. Codex's reading patterns and tooling produce different experiences from the same prompt. Comparing CC's dogfood to Codex's dogfood surfaces spec ambiguities: if both AIs do the same thing, the prompt is unambiguous. If they diverge, the prompt has a gap. The 2026-05-13 dogfood produced two real tickets (SKILL.md full-inventory ticket, efficient-probe-rules ticket) from exactly this comparison.

### Pipeline seats versus dogfood AIs: the dogfood gate

Pipeline seats validate with dry-run, temp HOME, `LDM_ROOT` fixtures, disposable environments. They **do not** run `ldm install`, `ldm install --alpha`, or `ldm install --beta` on Parker's production machine to "test" their work. State-mutating installer commands on Parker's machine require explicit Parker authorization for that specific run.

Dogfood AIs **do** run state-mutating commands when Parker pastes the prompt and says "install." That's their job.

The boundary is: the test of "did this code work?" lives in the coder's prepublishOnly test gate. The test of "did this experience work?" lives in the dogfood AIs. Pipeline seats never run the second test by hand.

This is the **dogfood gate** rule. See `ai/product/bugs/installer/2026-05-13--cc-mini--installer-dogfood-gate.md` for the originating incident.

---

## Loop discipline

### Both reviewers on every PR

Parker's 2026-05-13 call. Overrides the earlier asymmetric-ceremony rule (which had said doc-only PRs need only one reviewer). Now: every PR, including doc-only, gets both CC and Codex review. They catch different things; the cost of running both is low; the cost of missing a Codex blocker is high (the false-phantom-deletion regression on PR #938 was the worked example).

### Rule 2: re-read primary source before flagging "still unfixed"

Reviewer sessions accumulate context across turns. Before flagging a finding as "still unfixed" or "not yet addressed in this PR," re-read the current state of the cited line / file at HEAD on the PR branch. Stale-context findings burn coder cycles re-explaining what's already in the diff.

### Rule 3: two-round cap

After two rounds of review on the same PR, ship what's in front of the deployer and iterate in the next PR. Continuing to find nits after round 2 is diminishing returns. Exceptions are listed in the CC reviewer section above.

### Memory references

The rules above are captured as auto-memory entries that load on every session boot. The canonical source of truth is this document; the memory entries are pointers:

- `feedback_coder_hands_off_to_reviewers_not_deployer`
- `feedback_pr_review_structure_blockers_and_shouldfix`
- `feedback_three_validation_types_and_dogfood_gate`
- `feedback_both_reviewers_on_every_pr`
- `feedback_installer_test_is_prompt_not_bash`
- `feedback_sanity_check_relayed_drafts`
- `feedback_deployer_pr_class_release_matrix`
- `feedback_ldm_os_is_canonical_pattern_source`

When this manual and a memory entry disagree, the manual wins; update the memory in the next session.

---

## Three validation types

Every change has three layers of validation. Each layer has a different home; no agent runs another agent's layer.

| Layer | Who runs it | Where |
|---|---|---|
| **Coder validation** | The coder seat, locally | Disposable fixtures (temp HOME, mkdtemp, `LDM_ROOT` override). Never on Parker's machine. |
| **Installer validation** | CI, prepublishOnly gate, or a dedicated test environment | Clean test environment that mimics a real install (temp HOME, isolated `LDM_ROOT`, container, fresh user). |
| **Dogfood validation** | Parker pastes the install prompt into a dogfood AI | Parker's machine, AI-driven, end-user surface. Final stage; only after merge and release. |

The dogfood-gate rule (above) is the operating-procedure consequence of this taxonomy: coder + installer validation use disposable surfaces; dogfood validation owns the production surface.

---

## Ticket and PR conventions

These conventions are enforced across every seat. Failing them is a blocker on review.

- **Branch prefix.** `cc-mini/` for Claude Code mini, `codex-mini/` for Codex mini, `cc-air/` for Claude Code on Air, `oc-lesa-mini/` for the OpenClaw Lēsa seat. Each harness has a distinct prefix so parallel sessions do not collide.
- **No squash merge.** Every commit has three co-authors and tells the story of how something was built. Always `git merge` (not `--squash`).
- **Three co-authors on every commit.** Parker, Lēsa, and the harness-specific AI. The exact lines:
  ```
  Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
  Co-Authored-By: Lēsa <lesaai@icloud.com>
  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  ```
- **Release notes ownership.** The agent that ships the release-triggering PR includes the `RELEASE-NOTES-v*.md` file on the branch. Docs-only, tracker-only, and `ai/`-only PRs do NOT speculatively add release-notes files. The presence of a notes file on a merged PR is the deployer's signal to cut a release.
- **No em dashes.** Use periods, colons, semicolons, or `...` instead. Applies to every file: tickets, READMEs, commit messages, PR bodies, chat output.
- **Worktrees for isolated work.** Each branch gets its own worktree under `.worktrees/wip-ldm-os-private--<branch-name>/`. Never edit on the main working tree.
- **Repo onboarding before first write.** Read `wip-ldm-os-private/CLAUDE.md`, the relevant Dev Guide, and the master ticket before any first write on a worktree new to your session. The branch-guard enforces this.

---

## When you need help: who to ask

If you are mid-task and unsure who to send your work to, use this table.

| Situation | Send to |
|---|---|
| You drafted ticket content (you're Parker or a reviewer) and need it filed | `installer-bugs--cc--ticket-maker` |
| You have a `/goal` directive for code | `installer-bugs--cc--coder` or `installer-bugs--codex--coder` |
| You have an open PR ready for review | Both reviewers: `installer-bugs--cc--reviewer` AND `installer-bugs--codex--reviewer` |
| Reviewer left change requests | Back to whichever coder owns the PR's branch |
| Reviewer approved (CC reviewer's final approval received) | `installer-bugs--cc--deployer` |
| You want to dogfood a published alpha/beta/stable release | Paste the install prompt into a dogfood AI (Claude Code CLI or Codex CLI), not a pipeline seat |
| Question about the pipeline itself | Read this document. If the answer is not here, file a ticket against this document |

If you find yourself wanting to run a state-mutating command on Parker's machine and you're a pipeline seat, **stop.** That's the dogfood-gate. Either delegate to a dogfood AI via the prompt, or ask Parker for explicit per-run authorization.

---

## Maintenance

This manual is updated when:

- A new seat is added to the pipeline. The seat's row in the table and a per-seat section land in the same PR.
- A dogfood AI is added or removed. The dogfood-AI table updates.
- A loop discipline rule changes. The rule changes here first, then in the memory entries.
- A real incident exposes a gap (an agent could not figure out who they were or what they did from this document). The gap closes here; the incident gets a journal entry.

Edits to this manual go through the standard pipeline: ticket-maker files the edit, both reviewers review, deployer merges. The manual is governed by itself.
