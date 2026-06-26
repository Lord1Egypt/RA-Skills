# Execution Rules & Checklists

## I. Scope Locking Rules

1. Every chapter must explicitly reference the target vendor, solution model, and application scenario.
2. Prohibited: generalized industry analysis without tying back to the specific solution.
3. If a section cannot be populated with solution-specific information, mark `[Info Missing]` rather than filling with generic content.

## II. Source Attribution Rules

1. **Fact**: Information directly from vendor documentation, patents, whitepapers, or verified technical specs. Annotate as `[Public: Source]`.
2. **Derivation**: Information inferred from similar solutions, industry standards, or logical deduction. Annotate as `[Derived]`.
3. **Gap**: Information unavailable from any public source. Annotate as `[Info Missing]`.
4. Never present derivations as facts. Never present gaps as anything other than gaps.

## III. Granularity Compliance Rules

1. Entry-level: Module name + high-level function only.
2. Advanced: Module name + function + working principle + key interfaces.
3. Extreme: Module name + function + working principle + component-level details + algorithm logic + interface protocols.
4. Match output depth to user-specified granularity. Do not over-elaborate or under-deliver.

## IV. No Marketing Fluff Rules

1. Strip all promotional adjectives (e.g., "industry-leading", "cutting-edge", "revolutionary").
2. Replace with objective technical descriptions (e.g., "achieves 99.9% uptime through dual-redundant architecture").
3. If source material is primarily marketing, note this and extract only verifiable technical claims.

## V. Logical Consistency Rules

1. Cross-reference all chapters for consistency (e.g., hardware interfaces mentioned in Chapter 2 must align with co-design interfaces in Chapter 4).
2. If contradictions are found between sources, note the discrepancy and cite both sources.
3. Maintain a running gap log throughout all steps.

## VI. Terminology Definition Rules (Executed per User Preference)

Based on the "Terminology Explanation Preference" selected in the onboarding questionnaire:

- **A. Zero Explanation**: Do not provide any additional explanation for any term; assume reader has domain knowledge.
- **B. Minimal Contextual Explanation**: For the first occurrence of non-generic technical terms, add a parenthetical note of ≤15 words directly relevant to this solution. Example: `uses a proportional servo valve (a high-precision hydraulic valve for continuous flow control)`.
- **C. Full Definition**: Provide a 2-3 sentence definition and relevance to this solution for key terms.

If the user uses quick-start mode (`--quick`), default to option B.

## VII. Exception Handling Checklist

| Scenario | Handling |
| :--- | :--- |
| Playwright interaction failure (tab not found) | Record gap, insert `[Info Missing]`, aggregate in Appendix A. |
| All scraping sub-Skills return empty | Pause workflow, request user to provide private sources or adjust keywords. |
| Output judged as vague or marketing fluff | Re-invoke step prompt with additional emphasis directive. |
| Contradictory information between sources | Note discrepancy, cite both sources, use most recent/authoritative. |
| User requests granularity beyond available info | Degrade to best available level, inform user of limitation. |
| Token limit approached during generation | Prioritize core chapters (1-4), compress Chapter 5, omit optional appendices. |
