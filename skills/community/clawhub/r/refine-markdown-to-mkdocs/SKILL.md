---
name: refine-markdown-to-mkdocs
description: Refines raw reading notes by merging similar ideas, removing noise, and summarizing key points. Outputs structured markdown with different format (mkdocs materials style), e.g., Admonitions, bullet points, hightlights, blockquotes and so on. Use for "clean up notes", "summarize reading", "refine bookmarks", "get highlight cores".
---

# refine-markdown-to-mkdocs

Transforms raw, scattered reading notes into structured, high-density knowledge modules. Unlike the Formatter, this Skill **IS ALLOWED** to delete, merge, add (minor), or rewrite content flexibily for clarity and brevity.

**Core Principle**: Domain-Adaptive Structuring, Category-Specific Logic, Controlled Fidelity and High-Density Output.

## Workflow

### Step 1: Read & Detect category or content type

Read the input file. Identify the source material (Book Title, Author, Nation, Chapter, Genre, Style).

You MUST classify it into the following categories (quick reference):

1. **Philosophy theory, thoughts**
2. **Plays** (tragedy, comedy, stage play etc)
3. **Novels**
4. **Poetry** (epic, sonnet,lyric, narrative, satirical etc.)
5. **Literary Theory and Criticism** (poem/novel/prose/play etc. theories)
6. **Prose**
7. **History and history notes**
8. **Art Theory and collections**
9. **Biography** (philosophers, celebrities, leaders etc.)
10. **Programming and Computer Science** (Artificial Intelligence, Deep Learning, Large Language Models etc.)
11. **Mathematical models and theory** (Operations Research, Linear Algebra, Calculus, Algorithms etc)
12. **Integration of materials without a clear focus**
13. **Others** (notes that don't belong to any of the above)

**Sure about category**:
Pause and ask the user for confirmation to continue, present:

```markdown
One category detected.

- [Category A]:

Confirm, or choose a custom category: (Y/N)
```

`Y` for `yes` and `N` for `no`. If `N`, If not, enumrate the full categories to user with numebr in front and ask user to pick one. Note your recommended one with `(recommended)`.

**Not sure or ambigous about category**:
Pause and ask the user: "Mutliple categories covered. What genre or category do you believe it belongs to?" Generate 2~3 different categories candidates, present to user:

```
Pick a genre:

1. [Category A] - (recommend)
2. [Category B] - (category note)
3. [Category C] - (category note)

Enter number, or type a custom category:
```

The category you present and user select MUST be in the given categories. If not, enumrate the full categories to user with numebr in front and ask user to pick one. Note your recommended one with `(recommended)`

### Step 2: Semantic Clustering (Analysis)

Based on category chosen in Step.1, view the classification rules of the specific category in [references/notes_classify.md](references/notes_classify.md). The category-specific **Primary Focus** and High/Medium/Low Value Classification Rules are the guidelines you follow.

For example, category `Novels` follows:

```markdown
**Primary Focus:** Narrative voice, character development, thematic depth, and stylistic devices.

**Classification Rules:**

1.  **High Value:** Character arcs (psychological evolution), narrative perspective shifts, symbolic imagery, author's stylistic signatures, critical reception. -> **Keep & Polish**
2.  **Medium Value:** Plot points, setting details, secondary character profiles, timeline of events. -> **Merge & Summarize**
3.  **Low Value:** Minor plot details, redundant summaries, subjective emotional rants without textual evidence. -> **Delete (Log in report)**
```

After your analysis and cluster, save your plans in the **Output Plan File**: `{filename}-plan.md`

Structure:

```markdown
# Refinement Plan

## Cluster 1: [Theme Name]

- Source snippets: [Line numbers or quotes]
- Action: Merge into 1/2/3 Admonition block
- Draft Summary: [One sentence]

## Cluster 2: [Theme Name]

...

## Deletion List

- [Snippet content] -> Reason: Redundant/Unclear
```

**Pause for User Confirmation:**
Show the plan. Ask: "Proceed with this refinement structure? (Yes/No/Edit)"

### Step 3: Content Reconstruction (The Core)

Generate the refined content based on the approved plan.

**Writing Rules:**

1. **One Block, One Idea**: Each semantic cluster becomes **one Admonition block**.
2. **Summary First**: Every Admonition must start with a **1-sentence summary** (bolded or as title).
3. **Merge Smoothly**: When combining snippets, rewrite transitions so it reads like a coherent paragraph, not a list of quotes.
4. **Preserve Voice**: If it's literature, keep the emotional tone. If non-fiction, keep the logical precision, if philosophy, follow strict logic, etc.
5. **No Hallucination**: Do not add new knowledge not found in the notes. Only clarify existing knowledge.

Apply formatting guided by the Step 2 analysis to make markdown text prettier. Encouraged to use different styles to make text prettier. The goal is making the content scannable and the key points impossible to miss.

**Formatting toolkit:**

| Element         | When to use                                                           | Format                                                 |
| --------------- | --------------------------------------------------------------------- | ------------------------------------------------------ |
| Headings        | Natural topic boundaries, section breaks                              | `##`, `###` hierarchy                                  |
| Bold            | Key conclusions, important terms, core takeaways                      | `**bold**`                                             |
| Unordered lists | Parallel items, feature lists, examples                               | `- item`                                               |
| Ordered lists   | Sequential steps, ranked items, procedures                            | `1. item`                                              |
| Highlights      | Critical details, important comparisons for quick and short attention | `==text==`                                             |
| Color highlight | Colored emphasis where standard bold are insufficient                 | `<span style="color:red;font-weight:bold">text</span>` |
| Tables          | Comparisons, structured data, option matrices                         | Markdown table                                         |
| Code            | Commands, file paths, technical terms, variable names                 | `` `inline` `` or fenced blocks                        |
| Blockquotes     | Notable quotes, important warnings, cited text                        | `> blockquotes`                                        |
| Admonition      | More notable quotes, definition, examples, conclusion                 | Follow **Admonition Syntax Rules** below.              |
| Separators      | Major topic transitions                                               | `---`                                                  |

For Unordered lists, Ordered lists (e.g., `- TEXT` and `1. TEXT`), there MUST be one empty line before the very beginning and one empty line after the end.

- Correct Format:

```markdown
This is the previous text.

- This is bullet point 1; (correct, 1 empty line before)
- This is bullet point 2;

This is the line afterwards (correct. ).
```

- Incorrect Format (DO NOT DO THIS):

```
This is the previous text.
- This is bullet point 1; (Wrong! MUST be 1 empty line)
- This is bullet point 2;
This is the line afterwards (Wrong! No empty line away from bullet points).
```

For Admonition you created, strictly follows **Admonition Syntax Rules** below.

**Admonition Syntax Rules**

Strict Enforcement. When using MkDocs-style admonitions (e.g., `!!! note`, `!!! example`, `!!! warning`), you must follow these indentation rules strictly. Markdown parsers require content inside blocks to be indented.

- Correct Format:

```markdown
!!! note "Title Text"

    This is the content. It must start with 4 spaces, and the above line is empty.

    This is a second paragraph. It also needs **4** spaces indentation.

    - List items also follows. The end line should have an empty line with no indent below.
    - List items follows too.

This is the line outside admonition (correct).
```

- Incorrect Format (DO NOT DO THIS):

```markdown
!!! note "Title Text"
This content has no indent. (Wrong - breaks indent rule)

!!! note "Title Text"

    First paragraph ok.

Second paragraph has no indent. (Wrong - breaks the block)
```

Syntax rules:

1. **Indentation**: All content belonging to the admonition must be indented **4 spaces** relative to the `!!!`.
2. **Paragraph Breaks**: Blank lines inside the block must also be indented (or simply ensure the next paragraph starts with 4 spaces).
3. **Nested Lists/Code**: If using lists or code inside an admonition, indent them **8 spaces** total.
4. **Consistency**: Do not mix tabs and spaces. Use 4 spaces consistently.

```

### Step 4: Save & Backup

Save as `{filename}-refined.md`.
Backup existing refined file if present (same logic as Formatter).

### Step 5: Completion Report

Report specifically on **Content Changes**:

```

**Refinement Complete**

**Stats:**

- Original Snippets: X
- Refined Blocks: Y
- Deletion Rate: Z%

**Major Mergers:**

- [Theme A]: Merged 5 snippets into 1 block
- [Theme B]: Merged 3 snippets into 1 block

**Deleted Content (Summary):**

- Removed 10+ repetitive observations about [Character X]
- Removed incomplete thoughts regarding [Topic Y]

**Files:**

- Plan: {filename}-plan.md
- Refined: {filename}-refined.md

```

## Notes

- **Safety**: Never delete a direct quote without marking it as deleted in the report.
- **Category-Specific Mode**: based on the category you detected (user selected), cluster contents via different standards and perspectives without diminish the inner cores.
- **Admonition Integrity**: Must generate correct structure initially to avoid parsing errors.

```
