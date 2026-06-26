---
name: discord
description: Discord platform skill for SurfAgent, covering route-aware state checks, extraction-first workflows, blockers, and when to use the Discord adapter over raw browser control.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://surfagent.app
    emoji: "💬"
---

# Discord

> Discord-specific operating skill. Use this with the core `browser-operations` skill.

This skill teaches agents how to work Discord without pretending the surface is stable when it is not.

## 1. Use this skill for

- route-aware Discord state checks
- visible channel and message extraction
- login and gate detection
- forum and thread surface recognition
- blocker-aware workflow decisions
- deciding when to use the Discord adapter instead of raw browser control

## 2. Tool preference

Use this order:
1. Discord adapter state tools
2. Discord adapter extraction tools
3. targeted browser evaluation only when needed
4. raw generic browser actions as fallback

Discord punishes selector guessing. Use site-aware tools first.

## 3. Discord truths that matter

Discord is a dynamic SPA with moving surface state.

It has:
- route changes that do not behave like normal page loads
- login, verification, and hCaptcha gates
- channel/thread/forum layouts that shift by context
- unstable internal structure that punishes brittle selectors

Important: login or verification state is a real outcome, not an error to hand-wave away.

## 4. Core Discord loop

Default loop:
1. confirm Discord state
2. classify the surface you are actually on
3. detect blockers before acting
4. extract visible structured state
5. choose one deliberate next action
6. verify the visible result

Do not blast clicks into Discord because the tab "looks about right".

## 5. Proof rules

For Discord, success usually requires:
1. correct server/channel/thread surface is visible
2. login or gate state is explicitly known
3. extracted state matches the visible UI
4. post-action state visibly changed in the expected way

Do not claim success from only:
- a selector match
- a click returning ok
- the absence of an error
- stale content that may belong to a different route

## 6. When to use the Discord adapter

Prefer the Discord adapter for:
- opening Discord in the managed browser
- route-aware page state detection
- login/register/hCaptcha gate detection
- visible message extraction
- visible channel extraction
- visible thread or forum row extraction

Current Discord adapter strengths:
- state detection first
- read-first extraction
- honest blocker reporting

## 7. When raw browser control is acceptable

Use targeted browser control only when:
- you need a narrow probe not covered by the adapter
- the action is clearly visible and low risk
- you can verify the visible result immediately

Even then:
- keep calls targeted
- re-check route state before acting
- stop if the surface changes under you

## 8. Common Discord blockers

Watch for:
- login screen
- register/onboarding flow
- hCaptcha or verification wall
- wrong guild or channel route
- stale or half-loaded thread state
- hidden message composer state
- account mismatch

When blocked:
- name the blocker plainly
- say whether it is retryable, adapter-fixable, or human-blocked
- do not fake progress on a gated surface

## 9. Token-efficiency rules for Discord

Prefer:
- state checks over giant DOM reads
- visible extraction over broad scraping
- route classification before content reads
- one action followed by verification

Avoid:
- raw HTML dumps of the whole app
- repeated full-page reads on unchanged state
- selector fishing across the entire Discord shell

## 10. Minimal Discord checklist

Before claiming a Discord task done, confirm:
- correct account or logged-out state
- correct server/channel/thread surface
- blocker state known
- intended state extracted or action completed
- visible result verified afterward

## 11. Relationship to other docs

Use alongside:
- `browser-operations` for universal browser rules
- the Discord adapter repo for concrete MCP/tool surface
- runtime wrappers when working from Claude Code, Codex, Cursor, Hermes, and others
