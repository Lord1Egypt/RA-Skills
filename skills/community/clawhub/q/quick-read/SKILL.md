---
description: Quickly extract the key points from a book or article and organize them into structured markdown notes. Use this when the user asks for a summary of a book or article, or wants to quickly understand the core content of a paper or book.
name: quick-read
---

# Quick Reading Skill

Extract the key points from books, papers, or articles and organize them into a structured markdown document tailored to a specific target audience, so that it can be easily viewed in mind-mapping tools such as XMind.

## Workflow

### Step 1: Gather Information

The user needs to provide the following information:
- **Book title / article title / paper title**
- **Target audience**: the reader’s background, age, profession, or specific needs
- **Optional additions**:
  - Author information
  - Specific chapters or focal points
  - The user’s particular questions or difficulties

### Step 2: Define the Role and Perspective

Based on the input, determine:
- **Role assumption**: Assume you are the author of the book or a researcher behind the paper
- **Audience positioning**: Reframe the content in language and examples that the target reader can understand

### Step 3: Extract and Organize the Content

Organize the content according to the following structure:

```markdown
# [Book Title / Article Title] Quick Reading Notes

## Basic Information
- Author:
- Publication date:
- Core positioning:

## Core Theme
[Summarize the core viewpoint of the whole book/article in 1–2 sentences]

## Target Audience
[Describe the characteristics of the intended readers]

## Main Content

### Part One: [Chapter Title]
**Core Viewpoint:**
[Refine it into concise language]

**Key Points:**
- Point 1
- Point 2
- Point 3

**Value to the Reader:**
[What the target reader can gain from this section]

### [Continue organizing the remaining sections in the same way...]

## Methodology / Practical Framework
[If the book/article contains a methodology, present it in clear steps]

## Key Quotations
[3–5 of the most inspiring original lines or distilled takeaways]

## Action Suggestions
[Specific actions the target reader can take]

## Further Reading
[Recommended related books or resources]
```

### Step 4: Output Presentation

- Use a clear hierarchical structure (h1 → h2 → h3)
- Keep the language concise and avoid excessive quotation
- Ensure the content is readable and practical for the target audience
- Mark the hierarchy clearly so it can be imported into XMind

## Prompt Template

```text
[Background] [Background information about the book / paper / article]

[Role] Assume you are [author name / researcher], or [the core figure in the book]

[Task] Sort out the content of [book title / article title] and organize it into a detailed summary and set of notes.

[Goal] Help [description of the target reader] quickly and comprehensively understand [core content], as well as [its unique value / methodology].

[Audience] [A specific reader profile, including age, profession, background, and current questions or difficulties]

[Format Requirements] Present the output as a markdown document with a clear hierarchy (distinct h1 / h2 / h3 levels), so that it can be directly imported into XMind for viewing. The topic sentence at each level should be concise and powerful.
```

## Quality Standards

- **Accuracy**: Faithful to the core viewpoints of the original book/article
- **Relevance**: The language style and examples should match the target audience
- **Practicality**: Distill actionable suggestions or methods
- **Structure**: Clear hierarchy, easy to import into a mind map
- **Readability**: The core ideas should be understandable even without reading the original work

## Common Scenarios

| Scenario | Example Input |
|----------|---------------|
| Business books | "Zero to One" — for young people who want to start a business |
| Academic papers | "DeepSeek’s Engram paper" — for a 40-year-old business analyst |
| Children’s education | "The Game of Breaking Bullying" — for an 11-year-old boy experiencing bullying |
| Professional textbooks | "Principles of Economics" — for entrepreneurs with no economics background |
