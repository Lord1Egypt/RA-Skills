---
name: social-science-journal-abstract-polisher
description: "Reusable prompt for refining social science academic abstracts to align with peer-reviewed journal requirements including APA 7th edition compliance. Use when polishing, editing, or improving an abstract for a social science journal submission, or when asked to make an abstract conform to APA style and peer-review standards."
---

# Social Science Journal Abstract Polisher

## Task

Refine the provided social science abstract for peer-reviewed journal submission without altering the core research content.

## Procedure

1. **Read** the input abstract in full. Identify the four functional segments (Background, Method, Findings, Implications). If any segment is missing or conflated, flag it and reconstruct from context.

2. **APA 7th Edition Compliance**
   - Abstract word count: 150–250 words (unless a specific journal requires otherwise).
   - Use past tense or present perfect for methods and results; present tense for implications and general conclusions.
   - No citations, footnotes, or abbreviations without prior definition within the abstract.
   - Numerals for numbers 10 and above; words for zero through nine (except measurements, ages, percentages, and sample sizes).
   - Active voice preferred; passive only where the action, not the actor, is the focus.
   - No first-person pronouns; rephrase to maintain an objective register.

3. **Logical Cohesion Across Segments**
   - **Background → Method**: The method must clearly follow from the research gap or question stated in the background. Add a transitional phrase if the jump feels abrupt.
   - **Method → Findings**: Findings should directly answer the method's inquiry. Ensure the dependent variable(s) in the method are the same ones reported in the findings.
   - **Findings → Implications**: Implications must stem from reported findings, not from aspirational claims. If an implication overreaches, scale it back; if a finding lacks an implication, add one grounded in the data.
   - Use lexical cohesion (repetition of key terms, synonym chains) across segments rather than introducing new terminology mid-abstract.

4. **Academic Register**
   - Replace informal or conversational phrasing with formal academic equivalents.
   - Eliminate hedging language that undermines clarity ("somewhat," "arguably," "it could be said that") unless the evidence genuinely warrants uncertainty.
   - Remove filler phrases ("It is important to note that," "In this study, we aimed to," "The purpose of this paper is to").

5. **Conciseness**
   - Delete redundant modifiers, tautological constructions, and restatements.
   - Merge sentences that convey overlapping information.
   - Preserve all substantive content; cut only rhetorical padding.

6. **Output Format**
   - Return the polished abstract as a single continuous paragraph (or structured format if the target journal specifies labeled sections).
   - Append a brief change log listing the three to five most significant revisions made (e.g., "Removed first-person pronoun," "Added transitional phrase between method and findings").
   - Confirm final word count.

## Constraints

- Do not introduce new empirical claims, data points, or theoretical frameworks not present in the input.
- Do not alter the study's design, sample, or findings.
- If the input abstract is fundamentally flawed (e.g., missing findings entirely), note the deficiency and revise what is available rather than fabricating content.
