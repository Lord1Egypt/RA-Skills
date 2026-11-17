---
name: project-docs-to-skill
disable-model-invocation: true
description: |
  Sub-skill of tech-to-skill. Extracts development experience from project documentation (ADRs, git logs, retrospectives, issue discussions) into skills reusable across similar projects. Invoked by tech-to-skill router when input is a git repo or project docs directory. Phase 3.
---

# project-docs-to-skill

Extract development experience from project documentation into skills that prevent repeating mistakes and transfer validated practices to new projects.

## Input

Multi-source. Not a single document. Typical inputs:

- ADR directory (`docs/adr/` or similar)
- Retrospective / postmortem documents
- Git log with commit messages
- Issue / PR discussion exports (if accessible)
- README, CONTRIBUTING, project wiki
- Any other markdown/text files the user specifies

The user may provide some or all of these. Ask what's available.

## Before you start

1. Confirm the input paths from the user (directory, repo path, or file list).
2. Ask the user for an output directory.
3. Ask the user what kind of project this is (language, framework, domain). This helps identify which experiences are transferable vs project-specific.
4. Record `source_title` as the project name, `source_author` as the team or organization, `source_url` as the repo URL if available, `source_date` as the date range of the documentation.

## Stage 1 - Structural Recognition

Goal: inventory the available documentation and map what exists.

1. **Scan all provided paths.** List every file found. For each file, identify:
   - File type (ADR, postmortem, retrospective, commit log, README, issue export, etc.)
   - One-sentence summary of what it covers
   - Date or date range (if discernible from content or file metadata)

2. **Classify by experience type:**
   - Success pattern: "what worked" sections, ADR Consequences (positive), retrospective "start/continue" items
   - Bug/debugging lesson: postmortem root cause, bug autopsy, retrospective "stop" items, fix commits with detailed messages
   - Rejected alternative: ADR Alternatives Considered, PR discussion threads where an approach was declined
   - Architecture constraint: ADR Context + Decision, design docs with tradeoff analysis
   - Workflow pattern: retrospective action items, process documentation
   - Other: anything that doesn't fit above

   - Completion criterion: every file is inventoried and classified. No file skipped without noting why.

3. **Do NOT do these in Stage 1:**
   - Do not extract candidate skill units yet
   - Do not merge information across files yet

## Stage 2 - Extract

Goal: identify reusable experience units that can become skills.

1. **Scan each classified item.** For each, ask:
   > "If a new similar project started, would this experience help the agent make better decisions or avoid the same mistakes?"

   - Yes, and it's self-contained -> candidate unit
   - Yes, but needs context from another file -> note the dependency, merge during construction
   - No (project-specific config, one-off task, no transferable insight) -> skip

2. **For each candidate unit, record:**
   - Proposed skill title (action-oriented: "Choosing a database for high-write workloads", not "ADR-003")
   - One-sentence description of what experience it captures
   - Experience type (success pattern | bug lesson | rejected alternative | architecture constraint | workflow pattern)
   - Source files and specific sections it draws from
   - Whether the source provides: root cause, fix, prevention strategy, tradeoff analysis, alternatives

3. **Present the candidate list to the user.** Group by experience type for readability.
   Ask: "These will become skills. Any to add, remove, or merge?"
   - Completion criterion: user confirms the final list.

## Stage 3 - Construct

Goal: build each confirmed candidate into a complete skill.

For each confirmed candidate:

1. **Create the skill directory structure:**
   ```
   <output-dir>/<skill-slug>/
   ├── SKILL.md
   └── references/
   ```

2. **Fill What (the problem):**
   - Define the decision or problem this experience addresses.
   - For success patterns: "When deciding whether to use approach X in scenario Y"
   - For bug lessons: "When encountering symptom X in a system using Y"
   - For rejected alternatives: "When considering approach X for problem Y"
   - List trigger conditions and when NOT to use.

3. **Fill How (the method):** This varies by experience type.

   **For success patterns:**
   - Extract the validated practice as actionable steps or a decision tree.
   - Include conditions: "IF team size < 3 THEN stop at step 2. IF team size >= 3 THEN continue to step 3."
   - Include verification: how to confirm the practice is working.

   **For bug/debugging lessons:**
   - Extract in this structure:
     - Symptom: what the problem looks like
     - Investigation path: steps from symptom to root cause (the actual debugging journey, not a generic "check logs")
     - Root cause: what was actually wrong
     - Fix: what resolved it
     - Prevention: what process change prevents recurrence
   - If the source does not provide all five elements, fill what's available and note gaps. Do not fabricate missing elements.

   **For rejected alternatives:**
   - Extract: what was considered, why it was rejected, under what conditions
   - Frame as: "Do not use X when Y, because Z (source: ADR-003)"

   **For architecture constraints:**
   - Extract: the constraint, the decision, the tradeoff
   - Frame as: "System is constrained by X. Chose Y over Z because..."

   - Write all steps with checkable completion criteria.
   - Do not fabricate details the source doesn't provide.

4. **Fill Why (the rationale):**
   - Extract the real story: what happened, what was tried, what failed, what worked.
   - For success patterns: why this practice worked in this project's context
   - For bug lessons: why the bug occurred, why it wasn't caught earlier (detection gap), why the fix works
   - For rejected alternatives: why the alternative was rejected, what consequences were anticipated
   - If the source provides consequences (positive or negative) from ADRs or postmortems, include them.
   - If the source does NOT explain why, write: "Source does not discuss rationale."
   - Record `source_date` and `verified_date` (today's date).

5. **Build Evidence Index:**
   - For each claim, step, or story in SKILL.md, create a ref file pointing to the source document.
   - Ref files for project docs typically contain:
     - ADR Context/Decision/Consequences sections
     - Postmortem root cause analysis
     - Retrospective entries
     - Commit messages with detailed rationale
     - PR discussion threads
   - Each ref file records: source file, original text, context, relation to skill.
   - Completion criterion: every non-trivial claim has at least one ref backing it, OR is marked as inferred.

6. **Faithfulness check:**
   - For every statement, ask: "Did the source document actually say this?"
   - Pay special attention to causality claims: do not state "X caused Y" unless the postmortem/ADR explicitly establishes this.
   - Do not generalize project-specific findings into universal laws. If something worked in this project, say "worked in this project" not "always works."

   - Completion criterion: all sections filled or marked as not covered. Evidence Index populated. ref files created.

## Stage 4 - Validate

Same as other sub-skills:

1. **Structural completeness check:** What, How, Why all present. Each How step has completion criterion. Timestamps present.
2. **Evidence accuracy check:** Each ref file's quote matches the source document. Source location pointers include file name and section.
3. If independent sub-agent unavailable, label as "structurally validated, not blind-tested."

## After all skills are constructed

1. **Report to the user:**
   - Number of skills generated, grouped by experience type
   - Output directory path
   - Any source files that were not used (and why)
   - Any experience type that was underrepresented in the source (e.g., "No postmortems found - bug lesson skills may be limited")

2. **Ask the user** whether to review or adjust any skill.

## Key principles (differences from longform-to-skill and paper-to-skill)

- **Multi-source input.** Unlike longform and paper (single document), project docs are scattered across files. Stage 1 inventories all sources before extracting.
- **Experience types drive How structure.** Success patterns use decision trees/checklists. Bug lessons use symptom-investigation-rootcause-fix-prevention. Rejected alternatives use do-not-use-when framing. Architecture constraints use constraint-decision-tradeoff framing.
- **Real stories, not theory.** The Why section draws from actual events (postmortems, ADR consequences, retrospective outcomes), not theoretical reasoning. If the source is a story of what happened, keep it as a story.
- **Project-specific, not universal.** Do not generalize "this worked in our project" into "this always works." Mark the context clearly.
- **Actionable, not advisory.** "Communication needs improvement" is not a skill. "Add a daily 15-minute sync when cross-team dependencies exist" is. If the source only contains advisory conclusions, note that the experience is advisory-level, not actionable.
- **Faithful to source.** Same as all sub-skills: do not fabricate. If the postmortem doesn't identify root cause, say so.
