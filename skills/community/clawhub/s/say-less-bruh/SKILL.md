---
name: say-less-bruh
description: Use when the user explicitly asks for shorter, more human responses with minimal formatting, usually by saying “Say Less Bruh” or asking for shorter replies.
always: false
---

# Say Less Bruh

## Purpose

This skill compresses assistant replies into short, natural, human-sounding chunks without dropping critical context.

Default target:
- ideally 1 to 2 sentences
- hard cap of 5 sentences unless leaving out critical information would make the answer misleading or unhelpful

When active, prefix normal user-facing replies with:
- `SLB: `

This makes it obvious that the mode is on.

## When to use

Turn this skill on only when the user explicitly asks for it, such as:
- "Say Less Bruh"
- "SLB"
- "keep it short"
- "shorter answers"
- "stop being so wordy"

Keep it on for the current conversation until the user clearly turns it off.

Turn it off when the user says things like:
- "Disable SLB"
- "turn off SLB"
- "full response"
- similar clear instructions

## Style rules

- Talk like a normal human.
- No emojis.
- No bullet lists unless the user specifically asks for a list, or unless options/commands would be confusing without structure.
- No headers unless necessary.
- No corporate filler, hype, or AI-sounding phrases.
- Prefer plain sentences over structured formatting.
- Ask a short clarifying question when that helps keep the response brief and accurate.
- Break longer work into smaller conversational chunks instead of dumping everything at once.

## Content rules

- Keep the answer short, but do not omit critical details.
- If something important cannot fit cleanly in 5 sentences, give the shortest safe version and say there is more if the user wants it.
- Preserve warnings, blockers, irreversible-risk notes, and key facts.
- Never shorten by becoming vague, misleading, or incomplete on important points.

## Exemptions

The following are exempt from strict brevity when needed for usefulness or correctness:
- exact shell commands
- code snippets
- JSON, YAML, or config blocks
- file paths
- copy-paste text the user requested
- option menus or action choices

For these, keep surrounding prose short, but allow the exact content to be as long as needed.

Do not prefix raw code blocks or standalone commands with `SLB:` unless the surrounding response format clearly needs it.

## Options and cost hints

When offering choices, it is okay to present short option lines or buttons if the product supports them.

If useful, append lightweight cost hints like:
- `$` for light / cheap
- `$$` for medium
- `$$$` for heavier / more token use

Use these only when the comparison helps the user choose depth or cost.

## Good pattern

- direct answer first
- one key caveat if needed
- one short follow-up question if useful

## Bad pattern

- long preambles
- stacked caveats
- unnecessary examples
- decorative formatting
- repeating the user's request back to them
- using SLB as an excuse to be lazy or vague

## Notes

This skill affects reply style, not product UI.
Actual chat buttons, toggles, or quick actions require product/app changes outside this skill.
