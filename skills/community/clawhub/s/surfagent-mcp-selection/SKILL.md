---
name: surfagent-mcp-selection
description: Selection guide for SurfAgent automation layers, showing when to use perception, platform adapters, MCPs, and raw browser control.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://surfagent.app
    emoji: "🪜"
---

# SurfAgent MCP Selection

> Use this with `browser-operations` first, then the relevant platform skill like `gmail`.

This is the routing guide.

Its job is simple: pick the lightest layer that can solve the task **with proof**.

## 1. The ladder

Default order:
1. perception or state layer first
2. platform adapter second
3. MCP when available and actually better for the task
4. raw browser control last

This is the rule, not a suggestion.

If a cheaper layer can answer the question or perform the action safely, use it.

## 2. What each layer is for

### Layer 1: perception or state
Use this to understand:
- what page or app you are on
- whether the right account is active
- whether the target surface is already open
- what changed after an action
- whether there is a blocker

Good uses:
- classify current browser state
- check inbox vs compose vs sent state
- confirm whether a modal, thread, or draft is actually visible
- inspect only the relevant surface after acting

Do not skip this layer when state is unclear.

### Layer 2: platform adapter
Use this when the site has a stable adapter with meaningful verbs.

Good uses:
- Gmail open, compose, fill, send, sent-mail verification
- site-specific state reads that avoid rediscovering brittle UI structure
- actions with known editor quirks or proof requirements

The adapter should compress complexity, reduce selector brittleness, and save tokens.

### Layer 3: MCP
Use an MCP when it exposes a stronger abstraction than the adapter or raw browser.

Good uses:
- mailbox or platform-native operations already wrapped as reliable verbs
- structured reads that would otherwise require multiple browser probes
- cross-step actions where the MCP already bakes in known platform rules

Do not use MCP just because it exists. Use it when it is the best abstraction for the job.

### Layer 4: raw browser
Use this only when the higher layers cannot do the job.

Good uses:
- one-off UI probes
- narrow render verification
- unsupported site actions
- temporary gap coverage while adapter or MCP support catches up

Raw browser is the sharp knife. Useful, but dumb in careless hands.

## 3. Selection rules

Pick the first layer that satisfies all three:
- can see enough state to avoid guessing
- can perform the needed action reliably
- can produce proof afterward

If a layer can act but cannot prove success, it is not enough.

If a heavier layer gives no reliability or proof advantage, do not use it.

## 4. When not to use the heavier layer

Do **not** jump to an adapter, MCP, or raw browser when:
- a state tool can already answer the question
- the task is only classification or verification
- the action is simple and already covered cleanly by a lighter layer
- the heavier layer would require broad reads, extra navigation, or more token burn without adding confidence

Examples:
- Need to know whether Gmail compose is open, use compose state, not full browser scraping.
- Need to confirm a message rendered in Sent Mail, use the Gmail path first, not generic DOM fishing.
- Need to know which account is active, inspect the smallest relevant state surface before doing anything else.

## 5. Proof rules by layer

Every layer must end in visible evidence.

### Perception/state proof
Good proof:
- the state clearly identifies page, mailbox, dialog, account, or blocker
- post-action state is different in the expected way

Bad proof:
- vague summary with no clear target state
- repeating stale state as if it were current

### Adapter proof
Good proof:
- adapter reports the expected state change
- UI or follow-up state confirms the adapter result

Bad proof:
- adapter call returned success but no visible state changed

### MCP proof
Good proof:
- structured result matches the intended action
- a follow-up state check or render check confirms it

Bad proof:
- trusting the MCP output without checking resulting browser state when user-visible outcome matters

### Raw browser proof
Good proof:
- intended UI change is visible afterward
- resulting page, thread, modal, or render confirms the action

Bad proof:
- click succeeded
- selector existed
- no exception was thrown

## 6. Token-efficiency rules

Prefer:
- structured state over full-page reads
- narrow probes over giant snapshots
- one post-action verification read over repeated whole-page inspections
- adapter or MCP verbs when they compress multiple brittle browser steps safely
- diff-style checks, meaning what changed after the action

Avoid:
- repeated screenshots or giant DOM dumps when only one field matters
- generic browser scraping on apps that already have a platform adapter
- using raw browser actions to rediscover known app workflows every run
- multi-step browser spelunking when an MCP returns the answer in one structured call

Rule of thumb:
- if the layer makes you read more than act, you probably chose the wrong one
- if the layer makes you act without checking state, you definitely chose the wrong one

## 7. Recommended decision flow

1. inspect state
2. choose the narrowest layer that can finish the task with proof
3. act once
4. verify the result on the smallest reliable surface
5. only escalate down the ladder if the current layer is insufficient

Escalate because of evidence, not impatience.

## 8. Example calls

### Example A: “What screen am I on?”
Use perception/state only.

Do not:
- open extra tabs
- call raw browser tools to dump the page
- use a heavier platform flow just to classify state

### Example B: “Send this Gmail message and prove it sent.”
Use:
1. Gmail state
2. Gmail compose tools
3. Gmail send
4. Sent Mail or rendered thread verification

Use raw browser only for narrow render verification if the Gmail layer does not expose enough proof.

### Example C: “Inspect a platform with a strong MCP.”
Use:
1. state to confirm where you are
2. platform adapter if it covers the task
3. MCP if it gives stronger, cleaner structured verbs
4. raw browser only for gaps or render proof

### Example D: “Click this odd UI control that no adapter exposes.”
Use:
1. state to confirm the surface
2. targeted raw browser action
3. immediate verification

That is a legitimate raw-browser case.

## 9. Failure and fallback rules

Before escalating to a heavier layer, ask:
- is the current state actually clear?
- did the current layer fail, or did I skip verification?
- is the blocker about capability, or about page state?

Only move down the ladder when:
- the current layer lacks the action you need
- the current layer cannot produce proof
- the current layer is clearly wrong or incomplete for this surface

Do not escalate just because the first attempt was sloppy.

## 10. Relationship to other docs

Use alongside:
- `browser-operations` for universal browser discipline
- `gmail` for Gmail-specific proof and compose/send rules
- the relevant MCP or adapter docs for concrete verbs

This guide decides **which layer to use**.
Those docs explain **how to use that layer well**.
