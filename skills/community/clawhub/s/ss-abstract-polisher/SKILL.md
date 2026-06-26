---
name: Social Science Journal Abstract Polisher
description: Reusable prompt for refining social science academic abstracts to align with peer-reviewed journal requirements including APA 7th edition compliance
metadata:
  openclaw:
    category: "Academic Writing Support"
    label: "Social Science Journal Abstract Polisher"
---

# Social Science Journal Abstract Polisher

## Purpose

Refine social science academic abstracts to meet peer-reviewed journal standards without altering core research content.

## Instructions

When a user provides an English abstract for a social science manuscript, apply the following transformations systematically:

### 1. APA 7th Edition Compliance
- Ensure the abstract is a single paragraph (unless the target journal specifies structured format).
- Keep the abstract within 150–250 words (adjust per journal guidelines if specified).
- Use active voice as the default; passive voice only when the action is more important than the actor.
- Eliminate contractions, colloquialisms, and informal phrasing.
- Verify that terminology, statistical notation, and citation style (if any references appear) conform to APA 7th conventions.
- Do not include author names, institutional affiliations, or raw reference entries in the abstract body.

### 2. Logical Cohesion Across Four Components
Restructure or resequence sentences so the abstract flows through four integrated sections:

- **Background** — Establish the research problem, gap, or motivation in 1–2 sentences. Anchor the study in existing literature without over-citing.
- **Method** — Describe the research design, sample, and analytical approach concisely. Specify methodology (qualitative, quantitative, or mixed) and key procedural details.
- **Findings** — Report the principal results with precision. Include effect sizes, statistical significance, or thematic categories where applicable. Avoid vague qualifiers (e.g., "results showed some effect").
- **Implications** — State the theoretical or practical significance in 1–2 sentences. Connect findings back to the gap identified in the Background.

Use transitional phrasing to link sections (e.g., "To address this gap, …"; "Results indicated that …"; "These findings suggest …"). Avoid abrupt jumps between components.

### 3. Formal Academic Tone
- Replace informal or tentative language with precise academic equivalents (e.g., "looked at" → "examined"; "a lot of" → "a substantial proportion of"; "seems to" → "appears to").
- Maintain an objective, third-person perspective throughout.
- Use hedging appropriately (e.g., "suggests," "indicates," "provides evidence for") without over-qualifying to the point of meaninglessness.

### 4. Redundancy Elimination
- Remove repetitive phrases, redundant modifiers, and filler constructions (e.g., "in order to" → "to"; "due to the fact that" → "because"; "it is important to note that" → delete and restructure).
- Consolidate overlapping sentences.
- Ensure every sentence carries unique informational weight.

## Input

The user provides a draft abstract (plain English text).

## Output

Return the polished abstract as a single coherent paragraph (or structured format if specified), followed by a brief change summary listing the major revisions made (category: APA compliance / logical flow / tone / redundancy).

## Constraints

- Do not introduce new claims, data, or references not present in the input.
- Do not alter the study's core findings, methodology, or conclusions.
- If the input is too short to evaluate flow, flag this and suggest expansion areas rather than fabricating content.
- If the input exceeds the target word count, prioritize cuts in redundancy and verbosity before compressing content.
