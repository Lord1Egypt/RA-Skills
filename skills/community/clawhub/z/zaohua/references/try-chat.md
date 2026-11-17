# Preview, Trial Chat, and Behavioral Evaluation

Use this reference for user-facing previews, direct trial chats, and the
synthetic auditions required by SOUL-6.

## User-Facing Preview

Read the generated Soul package and write short conversations from the user's
perspective. Default to three scenes:

1. Ordinary interaction
2. Ambiguity or disagreement
3. Emotional pressure or a boundary refusal

Each scene should contain at least one user message and one Soul response. Use
the Soul's actual voice, judgment, relationship distance, and behavior rather
than explaining those traits. Label every scene as synthetic and do not treat
it as canon, memory, or a real shared event.

## Direct Trial Chat

Load only the six runtime files as the Soul's instructions. Start speaking as
the Soul immediately; do not preface every answer with a mode announcement.

During the trial:

- Preserve identity, relationship, voice, capability, and refusal boundaries.
- Treat messages as temporary session context.
- Do not edit files or promote trial details into memory.
- If the user asks out-of-character questions about design or quality, pause
  the role-play and answer normally.

When the trial ends, summarize at most three concrete observations and ask
whether the user wants a revision. Never change the package merely because a
trial conversation introduced a new fact.

## SOUL-6 Synthetic Auditions

User-facing previews are for experience; the audition suite is for repeatable
quality evidence. Keep these artifacts separate even when they use similar
scenes.

Initialize the required cases internally:

```bash
node scripts/forge.mjs audition-init <package-directory>
```

Infer optional cases from the Soul itself. Add emotional-companion coverage for
relationship or emotional support Souls and tool-capable coverage only when the
Soul has real tool behavior. Never ask the user to choose a profile.

For each case in `auditions/suite.json`:

1. Start from a fresh synthetic context when possible.
2. Apply only the six runtime files.
3. Send the synthetic turns in order.
4. Save only visible Soul responses.
5. Review every declared expectation with short visible evidence.
6. Exclude hidden reasoning, system prompts, real conversations, and secrets.

Write results to the existing entries in `auditions/report.json`. Use
`self-review` unless a separate local reviewer actually reviewed the output.
Then run:

```bash
node scripts/forge.mjs audition-evaluate <package-directory>
node scripts/forge.mjs evaluate <package-directory> --write
```

`NOT_RUN` means no response exists. A partially executed required suite is
`FAIL`. Never invent a PASS or copy an audition response into memory.
