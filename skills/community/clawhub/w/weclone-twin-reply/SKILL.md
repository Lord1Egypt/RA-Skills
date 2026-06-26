---
name: weclone-twin-reply
description: Build a review-gated digital twin reply from persona markdown, persona examples, and live conversation context. Use when you need to imitate a specific user's chat style, draft a reply on the user's behalf, or generate a persona-consistent message candidate from an existing persona pack.
version: 0.1.0
emoji: "✍️"
homepage: "https://github.com/xming521/WeClone-Skill"
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# WeClone Twin Reply

Assemble an isolated prompt package that lets a separate model imitate one user's messaging style, personality, values, and worldview from markdown persona files and persona examples. Draft first, review second, send last.

## Expected Inputs

- A prepared persona directory. Default to `ai_twin/` at the repo root, containing `profile.md`, `persona_examples.md`, `guardrails.md`, and optional `state.md`.
- Runtime context: one short scene summary and one dialogue window.
- Explicit approval from the user before any outbound send.

If the persona directory does not exist yet, use `$weclone-init-twin` first to scaffold the default `ai_twin/` directory, then ask the user to fill the generated templates before drafting.

## Core Workflow

1. Confirm that the persona pack already exists.
   If `profile.md`, `persona_examples.md`, or `guardrails.md` are missing, stop and hand off to `$weclone-init-twin`. Confirm that the persona files are filled with real content rather than placeholders.
2. Gather the minimum high-signal context.
   Include who the other person is, what the current situation is, and the recent messages that the reply must answer.
   Before drafting, determine whether the available context is sufficient to answer faithfully and safely.
   If key facts are missing or the likely reply would change materially depending on missing context, stop and ask the user whether to collect more information before proceeding.
   Write that context into two runtime files:
   - `scene.md`: a short summary of background facts that are necessary for the reply but may not be obvious from the raw chat. Include who the other person is, the relationship, the current situation, the platform or app where the reply will be sent, the user's likely goal or constraint, and any reply-specific caution such as "do not commit yet".
   - `dialogue.md`: the active message window, usually the recent turns that the candidate reply is directly answering. Keep the original wording and speaker attribution when possible.
   Use `scene.md` for distilled context and `dialogue.md` for raw conversation. Do not dump the entire chat history into `scene.md`.
3. Render the prompt package.
   Run `python3 skills/weclone-twin-reply/scripts/render_clone_prompt.py --scene <scene.md> --dialogue <dialogue.md> [--extra-context <file>]`. By default it reads persona files from `ai_twin/`; pass `--persona-dir <dir>` only when overriding that location.
   The script injects `scene.md` into the `Runtime Scene` section of the final prompt and `dialogue.md` into `Active Dialogue`. 
   Treat the rendered prompt as the entire allowed context for that generation.
5. Return a reviewable draft.
   Show the user the candidate reply plus risk flags. Do not send on the user's behalf yet.
6. Send only after explicit approval.
   If the user edits or rejects the draft, revise it and repeat the review step.

## Execution Rules

- Keep the clone run isolated.
  Use a separate model call or isolated agent run that receives only the rendered clone prompt. Do not mix in unrelated notes, hidden scratchpad, or other task memory from the current thread.
- Load persona files intentionally.
  Use `profile.md` for stable identity, personality, values, worldview, and decision logic; `state.md` for recent status and goals; `persona_examples.md` for style imitation plus behavioral evidence; and `guardrails.md` for hard limits. Load extra `*.md` files in the persona directory only when they materially improve the reply.

## Guardrails

- Treat `guardrails.md` as the persona pack's source of truth for hard limits.
- The renderer template adds runtime guardrails for promises, privacy, reputation, ambiguity, and reviewer handoff.
- If the request is close to the boundary, bias toward a shorter, safer draft and stop at draft stage unless a human review step is guaranteed.
- If the available context is not enough for a defensible draft, do not fill the gaps by guesswork. Ask whether to gather more information first.

## Files And Resources

- `assets/clone_prompt_template.md`: single source of truth for the isolated clone prompt seen by the downstream model.
- `scripts/render_clone_prompt.py`: compile persona files and runtime context into the template, reading `ai_twin/` by default.

## Runtime Context Format

Use a short `scene.md` like:

```md
# Scene

Other person: former coworker, familiar but not close lately.
Situation: they asked this morning whether the user can refer them this week.
Platform: WeChat private chat.
User goal: stay polite and leave room without making a commitment.
Reply caution: do not promise a referral or a timeline.
```

Use a short `dialogue.md` like:

```md
# Dialogue

Them: Hey, are you free to refer me for the role we talked about?
User: I saw your message just now.
Them: No rush, but they are moving quickly this week.
```

If some fact materially changes the likely reply but does not belong in either file, pass it as `--extra-context <file>` instead of bloating `scene.md`.

## Output Contract

Use this skill to produce a candidate reply for review, not a silent auto-send. The exact handoff structure is defined in `assets/clone_prompt_template.md`.

If the user asks to automate sending, keep the approval gate in place and make the send step conditional on explicit confirmation.
