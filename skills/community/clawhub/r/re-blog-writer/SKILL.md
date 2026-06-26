---
name: blog-writer
description: Research a topic using the browser then write a complete blog post saved as a .md file in ~/blogs. Use when the user provides a subject and wants a full, human-sounding blog post researched from Google, Reddit, and other sources, written in a specific casual-direct style with a 5-part structure, no clichés, no em dashes, and a target of 1200-1500 words.
---

# Blog Writer

Use this skill to research and write one complete blog post per run.
It assumes browser access for research and writes the final post to `~/blogs/<slug>.md`.

If the user did not provide a subject, ask for one before proceeding.

## Inputs to infer

- `SUBJECT`: the topic or angle to write about
- Optional: specific angle, contrarian take, or audience focus
- Optional: any sources the user already has

## Workflow

1. Run `openclaw browser start` to open the openclaw managed browser. CRITICAL NON-NEGOTIABLE: always use this command. Never open a browser any other way.
2. Research the subject thoroughly using that same browser window before writing a single word.
   - Search Google, Reddit, and Hacker News directly in that browser window.
   - Do not close the browser between research and writing.
   - Read [references/research.md](references/research.md) for the exact search order and what to collect.
3. Take notes offline. Pull concrete facts, reactions, one surprising detail, one honest critique.
4. Write the blog post following the 5-part structure exactly.
   - Read [references/structure.md](references/structure.md) for every part's requirements.
   - Read [references/writing-style.md](references/writing-style.md) for style rules. Every rule applies to every sentence.
5. Run the self-editing checklist in [references/writing-style.md](references/writing-style.md) before saving.
6. Save the final post to `~/blogs/<subject-slug>.md`.
   - Use a lowercase hyphenated slug. Example: `vector-databases.md`.
   - Create the `~/blogs/` directory if it does not exist.
   - CRITICAL NON-NEGOTIABLE: do NOT include an `# H1` title at the top of the file. The post starts directly with the first sentence of Part 1. Title metadata is handled separately by the `re-blog-meta` skill.
7. Close all browser tabs opened during research.

## Quality bar

- CRITICAL NON-NEGOTIABLE: do NOT add an `# H1` title at the top of the post. Start the file directly with the first sentence of Part 1. Title is handled by the `re-blog-meta` skill.
- CRITICAL NON-NEGOTIABLE: target 1200-1500 words. If short, add a mini-story. If long, cut any paragraph that feels like a list.
- CRITICAL NON-NEGOTIABLE: no em dashes anywhere in the post.
- CRITICAL NON-NEGOTIABLE: no clichés. See the banned words list in writing-style.md.
- CRITICAL NON-NEGOTIABLE: never start with a day or time reference like "last Sunday," "today morning," or "this week."
- CRITICAL NON-NEGOTIABLE: start Part 1 with a real-world example, fact, or documented reaction found during research.
- CRITICAL NON-NEGOTIABLE: apply every writing style rule without exception. Do not relax any rule unless the user explicitly asks.
- CRITICAL NON-NEGOTIABLE: the post must sound like a person who had a real reaction to the topic. Read [references/human-voice.md](references/human-voice.md) and run the voice check in writing-style.md before saving.

## Completion report

At the end, report:

- Subject covered
- File saved to
- Word count
- Sources used during research
- Confirmation that all browser tabs are closed
