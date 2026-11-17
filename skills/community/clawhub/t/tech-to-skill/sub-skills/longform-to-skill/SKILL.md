---
name: longform-to-skill
disable-model-invocation: true
description: |
  Sub-skill of tech-to-skill. Converts engineering long-form content (source code notes, technical ebooks, architecture guides) into agent-callable skills. Invoked by tech-to-skill router when input is HTML/PDF/Markdown with chapters, code blocks, and design discussion.
---

# longform-to-skill

Convert engineering long-form content into skills that preserve actionable detail and trace back to source evidence.

## Input

- HTML page, PDF, or Markdown file
- Typical length: 5,000-50,000 words
- Contains: technical discussion, code examples, architecture descriptions, design tradeoffs

## Before you start

1. Confirm the source file path from the user.
2. Ask the user for an output directory. All generated skills go there.
3. Record `source_title`, `source_author`, `source_url`, `source_date` from the material itself. If the material does not state any of these, ask the user. Do not guess.

## Stage 1 - Structural Recognition

Goal: map the material's own structure. Do not impose a preset template.

1. **Read or scan the full text.** For large files, use grep/sed to locate headings and section boundaries first, then read sections selectively.

2. **Identify natural boundaries.** Look for the author's own structural signals:
   - Markdown headings (`#`, `##`, `###`)
   - HTML tags (`<h1>`-`<h6>`, `<section>`, `<article>`)
   - Numbering patterns ("Chapter 1", "M01", "Step 3", "第三章")
   - Content transitions (theory -> code, problem -> solution, narrative -> analysis)

3. **Produce a boundary list.** For each segment, record:
   - Start and end position (heading text, line number, or character offset)
   - One-sentence topic summary
   - Whether it contains actionable technical content (code, config, commands, design decisions) or is background/narrative

   - Completion criterion: every part of the source is accounted for in the boundary list. No gaps.

4. **Do NOT do these in Stage 1:**
   - Do not classify content into predefined categories (framework/principle/case/etc.)
   - Do not extract candidate skill units yet
   - Do not write any skill files

## Stage 2 - Extract

Goal: identify self-contained technical guidance units that can become skills.

1. **Scan each segment from the boundary list.** For each segment, ask:
   > "If I turned this into a skill, could an agent act on it when facing the corresponding problem?"

   - Yes, and it's self-contained -> candidate unit
   - Yes, but needs another segment to make sense -> merge with that segment, then evaluate
   - No (pure background, definition, or narrative) -> skip

2. **For each candidate unit, record:**
   - Proposed skill title (one phrase, action-oriented)
   - One-sentence description of what problem it solves
   - Source segments it draws from (boundary list positions)
   - What kind of How content it contains (code, config, architecture pattern, decision tree, etc.)

3. **Present the candidate list to the user.** Show:
   - All candidates with title + description + source location
   - Count of candidates

   Ask: "These will become skills. Any to add, remove, or merge?"
   - Completion criterion: user confirms the final list.

4. **Do NOT do these in Stage 2:**
   - Do not write SKILL.md files
   - Do not create ref files
   - Do not do quality gating or filtering (that happens implicitly through the "can the agent act on it?" test)

## Stage 3 - Construct

Goal: build each confirmed candidate into a complete skill.

For each confirmed candidate:

1. **Create each skill's directory:**
   ```
   <skill-slug>/
   ├── SKILL.md
   └── references/
   ```

2. **Fill What (the problem):**
   - Define the problem this skill solves. Base this on what the source material explicitly discusses.
   - List trigger conditions: what situations will the user need this skill?
   - List when NOT to use this skill.
   - If the source does not clearly state the problem, infer it from context but mark it as inferred.

3. **Fill How (the method):**
   - Extract the actionable method from the source. Preserve key names: API names, config fields, command names, file paths (at module/function level, not line numbers).
   - Write steps with checkable completion criteria.
   - If the source contains code examples, reference them in Evidence Index rather than copying large blocks into SKILL.md.
   - If the source does not provide enough detail for the agent to act on, write what IS available and note the gap. Do not fabricate steps.

4. **Fill Why (the rationale):**
   - Extract design rationale from the source: why this approach, what tradeoffs the author discusses.
   - If the source discusses alternatives and why they were rejected, include that.
   - If the source does NOT discuss alternatives, write: "Source does not discuss alternatives."
   - If the source does NOT explain why, write: "Source does not discuss rationale."
   - Record `source_date` and `verified_date` (today's date).

5. **Build Evidence Index:**
   - For each claim, step, or rationale point in SKILL.md that needs source backing, create a ref file.
   - Each ref file contains: source location, original text fragment (preserving format), context, and relation to the skill.
   - Fill the Evidence Index table in SKILL.md with links to ref files.
   - Completion criterion: every non-trivial claim in SKILL.md has at least one ref backing it, OR is marked as inferred.

6. **Faithfulness check (self-audit before Stage 4):**
   - Read through SKILL.md. For every statement, ask: "Did the source actually say this?"
   - If any statement is your inference rather than the source's content, mark it explicitly.
   - If any section is empty because the source doesn't cover it, write the "Source does not discuss..." label. Do not leave blank sections.

   - Completion criterion: all sections (What/How/Why) are filled or explicitly marked as not covered by source. Evidence Index is populated. ref files are created.

## Stage 4 - Validate

Goal: verify the skill is structurally complete and evidence is accurate.

1. **Structural completeness check:**
   - Does SKILL.md have What, How, and Why sections? -> If any missing, back to Stage 3.
   - Does each How step have a completion criterion? -> If any missing, back to Stage 3.
   - Are `source_date` and `verified_date` present in frontmatter? -> If missing, fill them.

2. **Evidence accuracy check:**
   - For each entry in the Evidence Index, open the ref file and verify:
     - The source quote matches the original source material (not paraphrased beyond recognition)
     - The source location pointer is specific enough to find the content
   - If any ref is inaccurate or the quote doesn't match the source -> fix the ref file.

   - Completion criterion: all structural elements present, all ref files verified against source.

3. **Do NOT do these in Stage 4:**
   - Do not run blind testing (deferred)
   - Do not do trigger/decoy testing (deferred)
   - If independent sub-agent is unavailable, label the skill as "structurally validated, not blind-tested" in the Audit section. Do not fake validation results.

## After all skills are constructed

1. **Report to the user:**
   - Number of skills generated
   - Output directory path
   - List of skills with one-line descriptions
   - Any gaps where the source did not provide enough content (be honest)

2. **Ask the user:**
   - Whether to review any skill before finalizing
   - Whether any skill needs adjustment

## Output format

Use `templates/SKILL.md.template` and `templates/ref.md.template` as reference examples, not rigid templates. Required elements: frontmatter fields, What/How/Why sections, Evidence Index. Internal format is flexible - adapt to the source material.

## Key principles

- **Faithful to source.** The source is the ground truth. If it doesn't say something, don't invent it. Mark gaps honestly.
- **Actionable How.** The How section must contain enough detail for an agent to act. Abstract methodology like "consider the tradeoffs" is not enough. But don't fabricate specifics the source doesn't provide.
- **Evidence traces.** Every non-trivial claim in SKILL.md should have a ref file the agent can load for more detail.
- **Objective timestamps.** Record `source_date` and `verified_date` as facts. No guessed expiration.
