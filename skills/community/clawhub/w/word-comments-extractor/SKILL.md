---
name: word-comments-extractor
description: Extract comments from Word documents and format them into standardized review opinions. Auto-matches page numbers, agent-powered semantic polishing. Designed for investment banking QC, legal review, and document audit scenarios.
platforms: ["win32"]
binaries: ["Microsoft Word"]
install:
  steps:
    - description: "Install pywin32 Python package"
      command: "python -m pip install pywin32"
  note: "Microsoft Word must be installed manually by the user. This skill requires Word COM interface for page number retrieval."
---

# Word Comments Extractor

## Overview

Extract comments from Word (.docx) documents and format them into standardized review opinions. The script handles data extraction (comment text, anchor text, page numbers) and outputs structured JSON. The agent then performs semantic polishing to produce professional, publication-ready review opinions.

Core capabilities:
- Accurate page number matching via Word COM interface
- Comment content semantically polished by the agent into professional review language
- Description intelligently distilled from anchor text by the agent

## Architecture

- **Python script** (`extract_comments.py`): Handles all data extraction locally. Unpacks the .docx file (using Python's built-in `zipfile`), parses XML to extract comments and anchor text, retrieves page numbers via Word COM. Outputs JSON. No external dependencies beyond `pywin32`.
- **Agent**: Performs semantic polishing on the extracted data (description distillation + comment rewriting). This uses the same agent that runs the skill — no additional external services or APIs are called. The polishing happens entirely within the agent's normal conversation flow, just like any skill that asks the agent to summarize or rewrite text.

## Usage

### Step 1: Run the extraction script

```bash
python extract_comments.py <docx_file_path>
```

The script takes a single argument — the path to the .docx file. It handles unpacking internally.

Output is a JSON array, each element containing:
- `index`: Comment sequence number
- `page`: Page number
- `comment_text`: Original comment text
- `anchor_text`: The document text that the comment is attached to

### Step 2: Agent polishes and outputs

After receiving the JSON data, the agent processes each comment:

#### 2.1 Distill description

Extract a concise, precise content description from the **anchor text** for the "regarding XX" part of the output.

Requirements:
- Description must reflect the specific business content in the anchor text. Generic terms like "related matters" or "related situation" are not allowed.
- If the anchor text involves specific financial metrics, product names, company names, or business types, these must appear in the description.
- Length: 5-30 characters.

Examples:
- Anchor text mentions "pressure sensor gross margin declining, average unit price trending down" -> Description: "pressure sensor gross margin and average unit price decline"
- Anchor text mentions "issuer revenue and non-recurring net profit" -> Description: "comparability of issuer revenue and non-recurring net profit with industry peers"

#### 2.2 Polish comment content

**Core principle: Understand intent, rewrite professionally, never mechanically concatenate.**

Rules:

**1. Understand the commenter's true intent**
- "The reason for the price decline wasn't mentioned" -> Intent: "missing explanation" -> Rewrite: "Please supplement the specific reasons for the price decline"
- "This generally needs to include the position before departure" -> Intent: "need to add position info" -> Rewrite: "Please supplement the specific position held before departure"

**2. Combine with anchor text context**
- Never interpret a comment in isolation. If a comment says "this needs to be mentioned", look at the anchor text to understand what "this" refers to.
- Key information from the anchor text (company names, product names, metrics, time periods) should be incorporated into the polished result.

**3. Neither expand nor reduce**
- Preserve the comment's core requirement. Do not add suggestions the comment didn't mention.
- Do not lose specific details. If the comment mentions "trial verification, partnership incubation period", keep these specific reasons.
- If the comment is already specific (e.g., "change 'two fields' to 'mass production'"), keep or minimally adjust.

**4. Professional language standards**
- Remove colloquial expressions and convert to formal written language.
- Use standard review phrasing: please supplement, please verify, please clarify, please correct, recommend improving.
- End with a period. Ensure complete expression.

**5. Prohibited error patterns**
- Never embed raw comment text directly into a template (e.g., "please supplement XXX situation" where XXX is the unmodified comment).
- Never trigger a fixed template from a single keyword match (e.g., seeing "peer" and outputting "verify whether this is a peer introduction").
- Never output identical boilerplate for all comments.
- Never ignore specific requirements in a comment to give generic advice.

#### 2.3 Polishing examples

| Original comment | Anchor text context | Correct polishing |
|---------|----------------|---------|
| The reason for the price decline wasn't mentioned | Sensor gross margin decline, unit price decline | Please supplement the specific reasons for the average unit price decline |
| The wording here isn't very clear, it's actually more about product mix or specific products, specific customers having a bigger impact | Oxygen sensor revenue fluctuation | Please clarify the core factors driving the fluctuation: product mix, specific product characteristics, and specific customer dynamics |
| Add numbering to subheadings, same below | Oxygen sensor downstream domestic substitution | Please add numbering; apply the same numbering format to all subsequent subheadings |
| The performance improvement compared to externally sourced chip modules needs to be mentioned here | MEMS pressure sensor cost | Please supplement the specific performance improvements of the self-developed chip module compared to externally sourced modules |
| After reading, the comparison doesn't convey much information. Are there more in-depth capacity parameter comparisons? | Capacity parameter comparison table | The current comparison lacks depth. Please supplement with a more detailed cross-comparison of core capacity parameters |
| Typo? | Text contains character error | Please verify and correct the typo at this location |
| Be more precise, make it clear this is projected | Gross margin related statement | Please ensure precise wording, explicitly stating the "projected" nature to avoid ambiguity |

## Output format

Each comment formatted as:
```
[number]. Page [X]: Regarding [description], [polished suggestion]
```

Overall structure:
```
[comment 1]
[comment 2]
...

Total: XX review opinions

================================================================================
[Page number note]
Page numbers correspond to physical pages in the document and may differ from
displayed page numbers (e.g., if the document has cover pages or table of contents
that are not numbered). If adjustment is needed, provide the offset between
physical and displayed page numbers for batch correction.
================================================================================
```

**Output requirement**: Only output the polished comment list + page number note. No additional summaries, category descriptions, or polishing explanations.

## Requirements

- Windows with Microsoft Word installed
- Python dependency: `pip install pywin32`

## Notes

1. Page number retrieval requires Word COM interface — Microsoft Word must be installed.
2. Output page numbers are physical page numbers (counting from page 1 of the document) and may differ from displayed page numbers.
3. UTF-8 encoding is handled automatically on Windows.
