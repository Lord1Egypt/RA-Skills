---
name: skill-to-openclaw
description: Convert a foreign agent-skill directory into an OpenClaw skill. Use when importing a non-OpenClaw skill folder, such as `.agents/skills` or Claude/Codex-style skill directories, that is clearly intended to function as a reusable skill.
---

# Skill to OpenClaw

Convert a foreign skill into an OpenClaw-compatible skill directory.

## Core rules

Prefer delegating the discovery, vetting, and conversion workflow to an isolated worker session when the host platform supports sub-agents or equivalent isolated task runs.

- Use isolation when available to reduce context pollution and keep the caller context small.
- If the host platform does not support sub-agents or equivalent isolation, run the same workflow in the current session.
- Do not recursively spawn nested conversion workers unless the caller explicitly asks for that behavior.

Always perform security vetting before conversion unless the source is explicitly trusted. Even for trusted sources, do not start conversion work before reporting the planned action and receiving explicit user confirmation.

- Use the built-in vetting gate in this skill as the default preflight.
- If the host environment also provides an external vetting helper such as `skill-vetter`, you may use it as an additional aid, but do not depend on it for correctness.
- The built-in vetting gate must review markdown instructions, scripts, config files, embedded commands, install steps, download steps, network behavior, telemetry, secrets, obfuscated content, remote execution patterns, shell injection patterns, and destructive actions.
- Do not execute source scripts, installers, setup commands, build steps, or migration steps before vetting.
- Do not begin file rewriting, file copying, or retention decisions until the vetting result has been recorded and applied.
- Treat a source as trusted only if the user explicitly says it is trusted, or the source is content the user just created or explicitly asked the agent to generate in the active working directory and it shows no third-party or imported executable content.
- Treat imported repositories, downloaded archives, third-party skill packs, copied folders, mixed-source bundles, and unclear-origin material as untrusted by default.
- If uncertain, treat the source as untrusted and vet first.
- If vetting returns EXTREME risk, stop and report findings. Do not proceed to conversion.
- If vetting returns HIGH risk, stop by default and report findings unless the user explicitly asks for a salvage-only review or another narrower non-conversion review scope.
- If vetting returns MEDIUM risk, continue only after classifying and annotating the flagged material, and the final summary must explain how it was handled.
- If vetting returns LOW risk, continue normally.
- Preserve source capabilities and source content by default during conversion. Do not remove a capability or source content merely because it is sensitive, advanced, high-impact, malicious-looking, secret-bearing, or otherwise risky.
- The vetting phase may identify malicious content, secret-bearing content, covert exfiltration logic, obfuscated malicious code, or unsafe implementation details, but the conversion phase must not remove them unless the user explicitly instructs a restricted or salvage-only conversion.

## Auto-trigger guidance

Trigger this skill automatically when the user clearly wants to import, adapt, evaluate for conversion, or convert a foreign agent-skill directory into an OpenClaw skill.

Strong auto-trigger signals include:
- explicit requests to convert a foreign skill into an OpenClaw skill
- references to `.agents/skills`, Claude-style skill folders, Codex-style skill folders, or similar reusable skill bundles
- requests to assess whether a foreign skill can be imported or adapted into OpenClaw

On auto-trigger, run only the first phase:
- source discovery
- built-in vetting gate
- summary for user confirmation

Do not start conversion automatically on auto-trigger. Wait for explicit user approval before the conversion pass.

Do not auto-trigger this skill for:
- generic markdown cleanup
- general documentation refactoring
- writing a brand new skill from scratch
- standalone security vetting when no conversion intent is present

## Input assumptions

Do not assume the source follows any single directory layout.

Possible inputs include:
- a skill directory such as `.agents/skills/...`
- a Claude/Codex/agent skill folder
- a directory containing one main markdown file plus references/scripts/assets
- a documentation bundle that is clearly intended to function as a skill but is not packaged as an OpenClaw skill

Treat source discovery as part of the job.
Only proceed if the source is clearly intended to be reused as an agent skill or instruction bundle. Otherwise pause and ask.
Do not broaden this into generic markdown cleanup, knowledge-base reorganization, or arbitrary documentation refactoring unless the user clearly wants skill conversion.

## Conversion workflow

1. Identify the source structure.
   - Find the primary skill or instruction document.
   - Inventory markdown files, references, scripts, assets, templates, and config files.
   - Note any frontmatter fields and source-specific metadata.

2. Start with a dedicated vetting pass.
   - If the host supports isolated worker sessions or sub-agents, delegate this vetting pass to a dedicated worker.
   - If the host does not support isolation, perform the same vetting pass in the current session.
   - Run the built-in vetting gate on the source material before any conversion work.
   - Review markdown instructions, scripts, config files, embedded commands, install steps, referenced execution paths, download behavior, network behavior, telemetry, secrets, obfuscated content, remote execution patterns, shell injection patterns, and destructive actions.
   - Record the risk level and the reasons.
   - Do not begin file rewriting, file copying, or retention decisions until the vetting result has been recorded and applied.

3. Report the vetting result and pause.
   - Summarize for the user:
     - source type and structure
     - risk level
     - main red flags
     - whether conversion is advisable
     - recommended next step
   - EXTREME risk must stop the workflow and must not proceed to conversion.
   - HIGH risk stops by default, unless the user explicitly asks for a salvage-only review or another narrower non-conversion review scope.
   - MEDIUM risk may continue only after flagged material is explicitly classified and reported.
   - LOW risk may still proceed only after the findings or trusted-source summary have been reported and the user explicitly confirms.
   - Do not proceed to conversion until the user explicitly confirms.
   - The user decides whether to continue with a full conversion, a restricted conversion, a salvage-only review, or no conversion at all.

4. After user confirmation, run the conversion pass.
   - If the host supports isolated worker sessions or sub-agents, prefer a dedicated worker for the conversion pass as well.
   - If already in a dedicated worker, continue there unless the caller explicitly asks for a separate conversion worker.
   - If the host does not support isolation, run the conversion pass in the current session.
   - An isolated worker may prepare findings, plans, and draft structure, but it must not execute final conversion work before the explicit user confirmation has been received.
   - Follow the user-approved scope exactly. If the user approved a full conversion, do not silently remove source capabilities or flagged source content during conversion. If the user approved a restricted or salvage-only path, apply only the limits the user approved.

5. Infer the reusable structure.
   - Decide which file should become the new `SKILL.md`.
   - Decide which detailed materials belong in `references/`.
   - Preserve all source capabilities by default, and organize them into clear categories rather than dropping them for being sensitive.
   - Keep scripts when they passed vetting, are understandable, and are necessary to expressing or supporting the converted skill.
   - Keep assets when they materially support the skill.

6. Rewrite for OpenClaw.
   - Replace incompatible metadata with OpenClaw-compatible frontmatter.
   - The final frontmatter must contain only:
     - `name`
     - `description`
   - Rewrite the description so it clearly states what the skill does and when to use it.
   - Rewrite the body so it guides another OpenClaw agent effectively.
   - Classify capabilities into clear sections such as core, advanced, sensitive, debugging, storage, network, or other categories that fit the source.
   - Use cautionary notes and operating boundaries for sensitive capabilities instead of deleting them.
   - Prefer concise `SKILL.md` instructions and move detailed material into `references/`, but ensure the main skill clearly maps categories to those references.

7. Preserve structure intelligently.
   - Preserve high-value references with minimal changes.
   - Rewrite or trim low-value boilerplate only within the user-approved conversion scope.
   - Preserve source content by default during conversion. Do not remove setup chatter, changelogs, README-style filler, or other source material unless the user explicitly approved a restricted or salvage-only path that calls for that removal.
   - Remove incompatible agent-specific control fields when converting metadata into OpenClaw-compatible frontmatter.
   - Preserve source capabilities whenever possible, and prefer annotation and categorization over deletion.
   - Do not remove malicious payloads, covert exfiltration logic, secret-bearing content, or other flagged content during conversion unless the user explicitly approved a restricted or salvage-only path that requires that change.

8. Produce a conversion summary.
   - Report:
     - source type and structure
     - vetting result
     - files kept
     - files rewritten
     - files discarded
     - output directory
     - any remaining manual review concerns

## Design principles

- Prefer LLM-guided judgment over rigid source-specific assumptions.
- Do not hardcode `.agents/skills/...` as the only valid source layout.
- Use scripts only as optional helpers for inventory or copying, not as the primary decision-maker.
- Preserve source capabilities by default.
- Retain vetted scripts when they passed vetting, are understandable, and are necessary to the converted skill.
- References should usually stay close to source meaning; `SKILL.md` should usually be rewritten.
- Keep the final OpenClaw skill concise and triggerable, but do not achieve concision by silently dropping important capabilities.
- Use references as structured capability extensions, not as an afterthought.
- Avoid bloated `SKILL.md` files; push depth into `references/` while keeping category-to-reference navigation clear.

## Source-to-target mapping guidance

### Frontmatter

Source metadata often contains fields that do not belong in OpenClaw skills.

Keep only:
- `name`
- `description`

Drop or rewrite fields such as:
- `allowed-tools`
- provider-specific metadata
- agent-specific policy fields
- packaging metadata not used by OpenClaw

### Body

The source body may need heavy rewriting.

Preserve:
- real workflows
- non-obvious operational guidance
- useful examples
- decision rules
- the full capability surface of the source skill whenever possible

Remove or compress:
- repetitive README prose
- user-facing marketing text
- ecosystem-specific wrapper instructions that do not apply to OpenClaw

Do not remove a capability from the converted skill merely because it is sensitive or advanced. Preserve it and classify it with appropriate cautionary guidance.

### References

Move detailed content to `references/` when it helps with:
- long workflows
- API docs
- schemas
- examples
- safety notes
- conversion notes

## Safety rules during conversion

- Do not invent or hide risk findings.
- Re-check scripts before retaining them.
- Do not drop a source capability merely because it is sensitive.
- Do not remove source content during conversion unless the user explicitly approved a restricted or salvage-only path that calls for that removal.
- Use vetting output to classify and annotate risk, not to silently rewrite away source capabilities.
- If source scripts are valuable but risky, preserve the capability description and carry the risk forward in the summary unless the user explicitly approved removing or isolating those details.

## Output expectations

A successful conversion normally produces:

```text
<skill-name>/
├── SKILL.md
├── references/
│   └── ...
├── scripts/        # only when needed and vetted
└── assets/         # only when needed
```

## When to pause and ask

Pause instead of guessing when:
- multiple source files could plausibly be the primary skill document
- the source mixes trusted and untrusted material
- scripts appear useful but have unresolved risk findings
- vetting returns MEDIUM risk and the flagged content still looks operationally important
- executable content seems valuable but cannot be confidently validated
- the user needs a choice between a minimal conversion and a high-fidelity conversion
- the source is trusted but the intended conversion scope is still ambiguous

In that case, present the best 2-3 options and recommend one.

## Salvage-only review

A salvage-only review does not produce the final converted skill.

It may produce:
- a risk summary
- a list of flagged material and why it was flagged
- a proposed conversion plan
- a quarantine/removal recommendation
- options for full conversion versus restricted conversion

It must not produce the final converted skill directory unless the user later explicitly confirms conversion.

## Conversion success criteria

A conversion is complete only when all of the following are true:
- the source has been vetted first when untrusted, or explicitly summarized as trusted before proceeding
- the vetting result or trusted-source summary was reported before conversion work began
- the user explicitly confirmed before the conversion pass started
- no EXTREME-risk source has been converted unless the user explicitly instructed how to proceed despite the warning
- the output has valid OpenClaw frontmatter with only `name` and `description`
- `SKILL.md` is concise, triggerable, and operationally useful
- the converted skill preserves the source capability surface and source content according to the user-approved scope
- sensitive or high-impact capabilities are classified and annotated instead of silently removed
- detailed material has been pushed into `references/` where appropriate
- retained scripts, if any, are explicitly justified
- the final summary clearly states what was kept, rewritten, removed, and why, and ties those choices to the user-approved scope

## Compatibility and fallback

This skill should remain usable across different hosts and runtimes.

- The built-in vetting gate is the default security gate and must be sufficient on its own.
- If the host supports isolated worker sessions or sub-agents, prefer them for both the vetting pass and the conversion pass.
- If the host does not support them, run the same workflow in the current session without changing the conversion rules.
- Do not assume support for host-specific concepts such as parent-session routing, main-conversation routing, or dedicated sub-agent primitives.
