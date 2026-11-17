---
name: paper-to-skill
disable-model-invocation: true
description: |
  Sub-skill of tech-to-skill. Converts academic papers and technical blog posts into agent-callable skills. Invoked by tech-to-skill router when input is a paper PDF or blog post with abstract/method/experiment structure. Phase 2.
---

# paper-to-skill

Convert academic papers and technical blog posts into skills that preserve the method's algorithmic detail, research insight, and experimental evidence.

## Input

- Paper PDF, arXiv preprint, or technical blog post
- Typical length: 3,000-20,000 words
- Contains: problem motivation, proposed method, algorithm/pseudocode, experimental results, comparison with baselines
- Optional: associated code repository URL

## Before you start

1. Confirm the source file path or URL from the user.
2. Ask the user for an output directory.
3. If the user provides a code repository URL alongside the paper, note it. The repo can help verify algorithm details during construction but is not required.
4. Record `source_title`, `source_author`, `source_url`, `source_date` from the paper itself (title page, header, or metadata).

## Stage 1 - Structural Recognition

Goal: map the paper's own structure. Most papers follow IMRaD but not all. Map what exists.

1. **Read or scan the full text.** For PDFs, extract text first. For large papers, locate sections by heading keywords (Abstract, Introduction, Method, Experiment, Conclusion, Related Work).

2. **Identify natural boundaries.** Look for:
   - Standard section headings (Abstract, Introduction, Method/Approach, Experiments/Evaluation, Discussion, Conclusion)
   - Non-standard headings (some papers use domain-specific section names)
   - Subsections within methods (algorithm descriptions, architecture components)
   - Tables and figures with captions (these are often self-contained evidence units)
   - Equations and pseudocode blocks

3. **Produce a boundary list.** For each segment, record:
   - Section name and position
   - One-sentence summary
   - Content type: motivation | method | algorithm | experiment | analysis | background

   - Completion criterion: every section of the paper is accounted for. No gaps.

## Stage 2 - Extract

Goal: identify self-contained method units that can become skills.

1. **Scan segments, focusing on Method and Algorithm sections.** For each, ask:
   > "If an agent encountered the problem this method solves, could it follow this guidance to apply the method?"

   - Yes, the method is self-contained and actionable -> candidate unit
   - Yes, but the method spans multiple sections -> merge those sections, then evaluate
   - No (pure literature review, dataset description, or experimental setup without reusable method) -> skip, but note as potential Evidence Index material

2. **For each candidate unit, record:**
   - Proposed skill title (named after the method or algorithm, not the paper title)
   - One-sentence description of what problem it solves
   - Source sections it draws from
   - Whether the source includes: pseudocode, equations, code examples, experimental validation

3. **Present the candidate list to the user.**
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
   - Define the problem this method solves. Draw from the paper's Introduction and Motivation sections.
   - List trigger conditions: what situations will a user need this method?
   - List when NOT to use this skill (e.g., "Do not use for X if the paper states it was not validated for X").

3. **Fill How (the method):**
   - Extract the algorithm or method steps from the paper. Preserve:
     - Mathematical formulations (in KaTeX/LaTeX notation)
     - Pseudocode (preserve the paper's own pseudocode format)
     - Key parameter names and their roles
     - Input/output specifications
   - Write steps with checkable completion criteria.
   - If the paper provides code examples, reference them in Evidence Index.
   - If the paper's method description is too abstract to act on (e.g., "use a neural network to encode the input" without architecture detail), write what IS available and note: "Source does not provide implementation-level detail for this step."
   - Do not fabricate architecture details not in the paper.

4. **Fill Why (the rationale):** This is the most distinctive section for papers.

   - **Why hasn't this been solved before?** What gap did the paper identify? What limitations did prior approaches have? Draw from Introduction and Related Work.
   - **How does this method address it?** What is the core insight or mechanism? Why does this approach work where others didn't?
   - **What's better?** What advantage does this method have over alternatives? Draw from Experiments (comparison tables, ablation studies). Include specific numbers if the paper provides them.

   - If the paper does NOT discuss prior limitations, write: "Source does not discuss prior work limitations."
   - If the paper does NOT include comparative experiments, write: "Source does not include comparative experiments."
   - Do not fabricate comparisons the paper didn't make.

   - Record `source_date` and `verified_date` (today's date).

5. **Build Evidence Index:**
   - For each algorithm step, rationale claim, or experimental result referenced in SKILL.md, create a ref file.
   - Ref files for papers typically contain:
     - Algorithm pseudocode from the paper
     - Experimental result tables
     - Equations with surrounding context
     - Related work comparison passages
   - Each ref file records: source section, original text/table/equation, context, relation to skill.
   - Completion criterion: every non-trivial claim in SKILL.md has at least one ref backing it, OR is marked as inferred.

6. **Faithfulness check:**
   - For every statement in SKILL.md, ask: "Did the paper actually say this?"
   - Pay special attention to experimental claims: do not state "X outperforms Y" unless the paper explicitly shows this in a comparison.
   - If a statement is your interpretation rather than the paper's explicit claim, mark it as inferred.

   - Completion criterion: all sections filled or marked as not covered. Evidence Index populated. ref files created.

## Stage 4 - Validate

Same as longform-to-skill:

1. **Structural completeness check:** What, How, Why all present. Each How step has completion criterion. Timestamps present.
2. **Evidence accuracy check:** Each ref file's quote matches the paper. Source location pointers are specific (section name, table number, equation number).
3. If independent sub-agent unavailable, label as "structurally validated, not blind-tested."

## After all skills are constructed

1. **Report to the user:**
   - Number of skills generated
   - Output directory path
   - List of skills with one-line descriptions
   - Any gaps where the paper did not provide enough detail

2. **Ask the user** whether to review or adjust any skill.

## Key principles (differences from longform-to-skill)

- **Why focuses on research contribution, not just design tradeoff.** The three sub-questions: why hasn't this been solved, how does this method solve it, what's better. Experimental data supports these claims but is not the Why itself.
- **Preserve mathematical formulation.** Equations and pseudocode are first-class content, not optional. Use KaTeX/LaTeX notation in SKILL.md.
- **Experimental claims need exact sourcing.** "X outperforms Y by 12% on dataset Z (Table 3)" is acceptable. "X is better than Y" without specific source is not.
- **Faithful to source.** Same as all sub-skills: do not fabricate. If the paper doesn't discuss something, say so.
