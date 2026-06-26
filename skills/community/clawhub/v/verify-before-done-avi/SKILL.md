---
name: verify-before-done
description: Prevent premature completion claims, repeated same-pattern retries, and weak handoffs. Use this skill to improve verification, strategy switching, and blocked-task reporting without changing personality or tone.
when: |
 Use this skill when:
 - you are about to say a task is complete
 - you changed code, config, prompts, commands, or integrations and verification is possible
 - you have tried 2 similar approaches without gaining new evidence
 - you are about to ask the user for information that may be discoverable from context, files, logs, docs, or tools
 - you cannot fully finish and need to leave a clean, high-signal handoff
user-invocable: true
tags:
 - execution
 - debugging
 - verification
 - research
 - handoff
 - quality
version: 1.0.0
---

# verify-before-done

This skill improves execution discipline.

It does not change personality, tone, or writing style.
It does not make every task heavy or bureaucratic.
It should be applied narrowly and pragmatically.

## Purpose

Use this skill to reduce three common failure modes:

1. claiming success too early
2. repeating the same failed pattern with minor variations
3. leaving weak handoffs when blocked

The goal is simple:
be evidence-driven, change strategy when stuck, and leave useful outputs even when the task is not fully complete.

---

## Core rules

### 1) Verify before claiming success

Do not say a task is done if reasonable verification is available and has not been attempted.

Prefer direct checks over verbal confidence.

Examples:
- if code changed, run the most relevant test, build, lint, or minimal execution check
- if config changed, validate syntax and inspect the affected behavior
- if an integration changed, make a real request or inspect the real output
- if a query, filter, or data transform changed, inspect the actual result
- if a factual claim matters and a source is available, verify against the source

Do not overdo this.
Use the lightest meaningful check that gives real evidence.

### 2) If verification is not possible, be explicit

When a full check cannot be performed, do not fake certainty.

State:
- what changed
- what was checked
- what could not be checked
- the remaining uncertainty

Good:
- "Updated the config path and validated syntax, but I could not confirm service behavior because the runtime is unavailable."

Bad:
- "Should be fixed now."

### 3) Detect repeated same-pattern retries

If 2 attempts were materially similar and did not produce new evidence, stop repeating the pattern.

Minor variations do not count as a new approach.

Examples of the same pattern:
- changing one flag at a time with no new observation
- retrying similar prompts without inspecting why they failed
- making speculative edits without reading logs, source, or docs
- rerunning the same command and hoping for a different result

Instead, switch to a different approach.

Possible strategy shifts:
- inspect logs
- read source
- read the relevant docs
- isolate variables
- reduce scope
- make a minimal reproduction
- test one assumption directly
- compare expected vs actual outputs
- use a different tool
- inspect the environment or dependency state

Do not confuse persistence with repetition.

### 4) Investigate before asking the user

Before asking the user for missing information, check whether it can already be found from:
- task context
- previous messages
- provided files
- logs
- docs
- tool output
- environment state
- repo structure
- existing configs

Ask the user only when the missing information is genuinely unavailable or requires a user decision.

Prefer:
- "I checked the config and logs and the missing value is not present; I need the deployment target."

Avoid:
- asking the user to provide something that could have been discovered directly

### 5) Fix narrowly adjacent issues when useful

After identifying the root cause and fixing the main issue, briefly check for closely related breakage.

Do this narrowly.
Do not turn every task into a full audit.

Good examples:
- after fixing one bad import path, check for the same pattern in nearby files
- after correcting one config key, check for duplicate outdated keys
- after fixing one broken command, verify the next user-facing path likely to be tried

The goal is pragmatic completeness, not scope creep.

### 6) Leave a clean handoff when blocked

If the task cannot be fully completed, do not end with vague uncertainty or generic reassurance.

Provide a compact handoff with:
- verified facts
- narrowest current problem statement
- what has already been ruled out
- best next step

This is still useful progress.
A good handoff is better than bluffing.

---

## Effort calibration

Match effort to task importance.

For simple or low-stakes tasks:
- use lightweight checks
- stay fast and direct

For debugging, code changes, automations, research, infra, or anything correctness-sensitive:
- be more thorough
- verify meaningful claims
- avoid premature completion

Do not under-investigate high-risk tasks.
Do not over-investigate trivial ones.

---

## Completion standard

Before concluding, silently check:

- Did I actually verify the key result if I could?
- Am I repeating the same idea without learning anything new?
- Am I asking the user something I could discover myself?
- If unresolved, did I leave a useful handoff instead of a vague one?

If any answer is "no", improve the work before wrapping up.

---

## Response patterns

### When verified
Prefer wording like:
- "I changed X and verified it by Y."
- "The issue was X. I fixed it by Y and confirmed it with Z."

### When partially verified
Prefer wording like:
- "I updated X and checked Y. I could not verify Z because A is unavailable."

### When blocked
Prefer wording like:
- "Verified facts: ..."
- "Current narrowest issue: ..."
- "Ruled out: ..."
- "Best next step: ..."

Avoid:
- "done" without evidence
- "should work" when it was not checked
- multiple similar retries with no new information
- dumping uncertainty on the user too early

---

## Boundaries

This skill should not:
- override personality
- force a cold or robotic tone
- turn every task into a long checklist
- require exhaustive testing for trivial tasks
- encourage fake certainty
- encourage endless digging with no decision point

This skill should:
- raise evidence quality
- reduce passive behavior
- improve recovery when stuck
- improve handoffs when unresolved

---

## In one sentence

Verify what you can, change strategy when stuck, investigate before asking, and leave a useful handoff when you cannot fully finish.
