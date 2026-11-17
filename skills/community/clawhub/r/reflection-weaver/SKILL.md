---
name: reflection-weaver
description: "Turn a reflection, draft essay, or voice-note transcript into a woven knowledge object by preserving the voice, extracting stable concepts, and strengthening backlinks."
tags: [reflection, essay, vault, knowledge-management, writing]
---

# Reflection Weaver

Use this skill when writing enters your knowledge base as lived material rather than already-normalized concepts.

## Core job

1. Decide what the text is:
   - reflection / essay
   - concept note seed
   - synthesis seed
   - some combination of the above
2. Preserve the reflection as writing first.
3. Extract only the concepts that are genuinely stable and reusable.
4. Weave natural links into the reflection body.
5. Strengthen rediscovery through backlinks from surrounding notes.

## Reuse and reruns

Work only in the knowledge destination and folders authorized for this task.
Identify the canonical reflection by its existing path or stable document ID;
rerunning that reflection updates the same object rather than importing another
copy. Preserve its wording, punctuation, whitespace, and paragraph order.
Link markup may wrap existing words without changing their displayed text;
do not add new prose to make a link fit.

Before creating a concept, search existing titles, aliases, stable IDs, and
related links within that scope. Read candidate notes to establish that they
mean the same concept, rather than matching a word alone. Reuse the existing
canonical path/ID even if its title differs from the essay's phrase. If several
notes could mean the concept, leave that link unresolved and report the choices;
do not invent a competing note, merge notes, or overwrite a colliding slug.
Create a concept only after establishing that no suitable one exists.

Detect existing links by **resolved target**, not just their displayed label:

- For `[[note]]`, `[[note|label]]`, and heading/block links, resolve the target
  to the host's existing canonical note. Preserve aliases and fragments.
- For Markdown links, resolve paths relative to the containing note, decoding
  URL escapes and separating fragments; check reference-style links through
  their definitions too. A different label can still point to the same note.
- Leave existing link markup intact. Do not nest a link or add a second link
  to the same concept merely because the essay mentions it again. Prefer at
  most one inline link per concept in this pass unless the user requests more.
- For explicit backlinks, scan the concept's existing body/backlink section
  for the same canonical reflection target, regardless of label or fragment.
  Reuse that entry; add one only if absent. If the host already supplies the
  required automatic backlink, do not add a redundant manual entry.

Plan only missing concept notes, inline targets, and backlink targets. Re-read
before applying if a file changed since inspection; preserve the new user edit
and revise the plan. Do not normalize or rewrite unrelated links/formatting.
On a second pass with unchanged inputs, the plan should be empty: no new note,
no repeated inline link/backlink, and no prose change. Report actual changes or
an empty plan; never claim a rerun was tested unless it was performed.

See [rerun-example.md](references/rerun-example.md) for a worked two-pass case.

## Non-negotiable rules

- Do not turn a reflection into a hub note.
- Do not replace singularity with general theory.
- Do not add explanatory prose inside the reflection unless the user asks.
- Prefer light embedded links in the reflection body and stronger backlink work elsewhere.

## Splitting policy

If a single draft is doing multiple jobs, split it into:
- reflection / essay
- concept note(s)
- synthesis or cluster note if needed

The essay remains canonical for the lived material.

## Good extraction targets

- phrases that name a mechanism
- repeated patterns that appear elsewhere in the vault
- tensions that are broader than a single incident

Do not extract every good line.

## Linking policy

- Use meaningful nouns and pressure phrases.
- Avoid visible overlinking.
- The note should still read as prose with links turned on.

## Output goal

The result should feel like:
- preserved writing
- clearer graph structure
- no loss of voice
