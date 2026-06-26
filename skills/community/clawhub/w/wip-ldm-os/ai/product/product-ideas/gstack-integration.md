# Product Idea: gstack Integration into LDM OS

**Date:** 2026-03-27
**Source:** Parker, inspired by Garry Tan's gstack (github.com/garrytan/gstack)
**Status:** Idea captured, needs architecture decision

## The Idea

Wrap Garry Tan's gstack skills into LDM OS so that CC proactively suggests relevant workflows based on what we're currently doing. Not replacing our existing tools. Complementing them with a suggestion layer.

Example: Parker says "let's add this feature" and CC recognizes the pattern and says "Hey, should we run /office-hours first to scope this?" or "Looks like we're about to ship. Want to run /qa?"

The key insight: these tools run differently than ours. We have tools that do similar things, but the gstack skills add structured gates (CEO review, eng review, design review) that we currently do ad-hoc.

## Context

- gstack is MIT licensed, 21 skills, all markdown-based prompt templates
- Garry Tan (YC CEO) ships 10,000-20,000 LOC/day using this system
- Skills follow a sprint workflow: Think, Plan, Build, Review, Test, Ship, Reflect
- Source: github.com/parkertoddbrooks/gstack (Parker's fork)
- DevOps Toolkit is being renamed to "code" and would be the home for code-related skills

## Key Decisions Needed

1. **Where does this live?** DevOps Toolkit (renamed to "code") is the home for all code skills. gstack skills would be wrapped there.
2. **Wrap vs. fork?** Don't fork and diverge. Wrap so upstream updates still flow in.
3. **Collision avoidance:** Our tools do similar things differently. Need clear routing: when to use ours vs. gstack's.
4. **Proactive suggestion engine:** The real value. CC should recognize context and suggest the right workflow without being asked.

## 1:1 Skill Mapping: gstack vs. WIP

| gstack Skill | What It Does | WIP Equivalent | Gap |
|---|---|---|---|
| /office-hours | YC startup diagnostic, brainstorming, design doc | None | **NEW** |
| /plan-ceo-review | CEO-level plan review (scope, vision, 10-star product) | None | **NEW** |
| /plan-eng-review | Eng manager plan review (architecture, edge cases, tests) | None | **NEW** |
| /plan-design-review | Designer plan review (before implementation) | None | **NEW** |
| /design-consultation | Full design system creation (colors, typography, layout) | /frontend-design | **OVERLAP.** Complementary: gstack creates the design system, ours builds UI. |
| /review | Pre-landing PR review (SQL safety, LLM trust boundaries) | None (manual) | **NEW** |
| /design-review | Live site visual QA + fixes | /frontend-design (partial) | **NEW** |
| /qa | QA test + fix loop (real Chromium browser) | None | **NEW** |
| /qa-only | QA report only (no fixes) | None | **NEW** |
| /investigate | Root cause debugging (4 phases, auto-freeze) | None | **NEW** |
| /ship | Release workflow (tests, diff, version, changelog, PR) | /wip-release | **OVERLAP.** Ours is better: private/public sync, deploy-public. |
| /document-release | Post-ship doc updates (README, ARCHITECTURE, CHANGELOG) | None (manual) | **NEW** |
| /retro | Weekly engineering retrospective with trend tracking | None | **NEW** |
| /browse | Headless Chromium browser (daemon, persistent state) | Playwright MCP | **OVERLAP.** We already have Playwright. gstack's is a compiled Bun daemon. |
| /setup-browser-cookies | Import cookies from real browser | None | **NEW** |
| /careful | Safety guardrails for destructive commands | /wip-file-guard (partial) | **OVERLAP.** Ours protects identity files. gstack's is broader. |
| /freeze | Directory-scoped edits (restrict to one folder) | None | **NEW** |
| /guard | /careful + /freeze combined | None | **NEW** |
| /unfreeze | Clear freeze boundary | None | **NEW** |
| /codex | OpenAI Codex second opinion (cross-model review) | None | **NEW** |
| /gstack-upgrade | Self-updater | /universal-installer | **OVERLAP.** Different approach. |

## Summary

- **13 skills are NEW** (no WIP equivalent)
- **5 skills OVERLAP** with existing WIP tools
- **3 skills are infrastructure** (freeze/unfreeze/guard)

## Biggest Gaps (High Value to Adopt)

1. **/office-hours** ... structured ideation/scoping before building
2. **/plan-ceo-review + /plan-eng-review + /plan-design-review** ... multi-perspective plan gates
3. **/review** ... automated PR review with security focus
4. **/qa + /qa-only** ... browser-based QA testing
5. **/investigate** ... structured debugging with auto-freeze
6. **/retro** ... weekly engineering retrospective
7. **/document-release** ... auto-update docs after shipping

## Where Our Tools Are Better

1. **/wip-release** ... handles private/public sync, npm publish, deploy-public. gstack's /ship is simpler.
2. **/wip-file-guard** ... identity-aware file protection (SOUL.md, agreements). gstack's /careful is generic.
3. **/universal-installer** ... agent-native installer that discovers and installs all interfaces.
4. **/wip-repos** ... manifest-driven repo organization. gstack has no equivalent.
5. **/wip-license-hook + /wip-license-guard** ... license compliance. gstack has no equivalent.

## Architecture Options

### Option A: Vendored Skills with Wrappers (Recommended)
- Install gstack as a dependency or git submodule
- Write thin LDM OS wrappers that add our context (boot sequence awareness, memory crystal integration, workspace conventions)
- Upstream updates flow in via npm/git update
- Wrappers add the "suggestion engine" layer
- Our release pipeline (/wip-release, /deploy-public) stays as-is; gstack's /ship is skipped

### Option B: Fork and Merge
- Fork relevant skills into our skill format
- Lose upstream updates
- Full control over behavior
- More maintenance work

### Option C: Side-by-side
- Install gstack globally alongside LDM OS
- Add a routing layer in CLAUDE.md that suggests gstack skills when appropriate
- Least integration work but also least cohesive

## Next Steps

1. Decide on architecture (A, B, or C)
2. Build priority list of which gstack skills to adopt first
3. Design the proactive suggestion engine (CLAUDE.md rules or hook-based?)
4. Prototype with /office-hours (highest value, no collision with existing tools)
