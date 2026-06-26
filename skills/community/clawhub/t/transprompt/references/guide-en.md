# TransPrompt | Turn plain-language requests into copy-ready AI prompts with one command

TransPrompt is an OpenClaw skill for people who know what they want, but do not want to spend time hand-crafting prompts.

Its job is simple:
- you write a natural-language request
- you prefix it with `@prt` or `@prompt`
- it turns that request into a cleaner, more usable prompt for AI tools

## Why install it?

### 1. One-command trigger
You do not need a separate app, UI, or prompt editor.

Just write:

```text
@prt Help me write a Python script to rename files by date
@prompt Design a landing page prototype for indie developers
@prt帮我查找近五年管理学论文，并给我硕士选题思路
```

It supports:
- attached trigger forms
- single-space trigger forms
- multi-space trigger forms

### 2. It only transforms when transformation is actually useful
Many prompt tools over-trigger and try to template everything.

TransPrompt is different:
- when prompt conversion is useful, it generates a copy-ready prompt
- when prompt conversion is unnecessary, it simply replies normally

That means inputs like:
- `@prt hi`
- `@prt what's the weather tomorrow?`
- `@prt are you there?`

will not be forced into an awkward prompt template.

### 3. Output is practical, not noisy
Default output includes:
1. one copy-ready prompt
2. one short `Prompt 关键处理` summary

It avoids:
- long prompt-engineering lectures
- internal routing jargon
- unnecessary numbered option menus

### 4. Tested through real iterations
This release was refined through:
- real chat testing
- dirty-input regression testing
- release smoke tests
- repeated edge-case fixes

Important issues fixed before release include:
- topic stickiness after generation
- internal wording leaking into bypass replies
- overlong endings
- attached-trigger boundary bugs
- over-questioning during clarification
- mistaking `@prt` requests for real execution requests

## Who is it for?

TransPrompt is useful for:
- people who are not good at writing prompts
- users who want better prompts for GPT / Claude / Gemini / Cursor / Claude Code
- anyone who wants to reduce AI trial-and-error
- people who want prompt conversion to feel lightweight and conversational

## Install

```bash
clawhub install transprompt
```

## Ongoing updates

This skill will continue to evolve with real-world usage and edge-case feedback.

If you find it useful, please consider giving it a **star** on ClawHub.