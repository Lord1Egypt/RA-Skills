# Review Rules

## Evidence Classes

Classify every material value before using it:

- **Confirmed**: explicitly present in source text or a readable source table.
- **Derived**: calculated directly from confirmed values; show the calculation.
- **Ambiguous**: present, but scope, role, unit, revision, or table relationship is unclear.
- **Missing**: not found in the reviewed material.

Do not convert ambiguous or missing values into confirmed facts.

## Source Priority

Use this order only when the document set itself defines no stronger precedence:

1. Latest signed or approved revision
2. Project-specific drawing or schedule
3. Project-specific technical requirement
4. Main body of the current plan
5. Appendix or copied template content

Flag disagreement instead of silently selecting a value. Ask the user which revision controls when approval status is unclear.

## Safety-Critical Review

Always inspect whether the material addresses the risks that are actually present, including as applicable:

- Fire, hot work, oxygen enrichment, oil contamination, cryogenic exposure
- Lifting, work at height, temporary electricity, confined spaces
- Equipment isolation, commissioning, evacuation, rescue, and emergency contacts
- Named responsible roles and a clear notification path
- Daily or staged work nodes when a detailed schedule was requested

This is a completeness check, not a legal or engineering compliance opinion. Do not add a standard number from memory. Verify any standard against an authoritative current source before citing it.

## Personal And Customer Data

- Keep source files and extracted text on the local machine by default.
- Do not publish names, phone numbers, pricing, drawings, or customer documents with a skill package.
- Redact examples before screenshots, demos, repository commits, or public issue reports.

## Final Review

Before external delivery, a human should confirm:

- Correct project and revision
- All names and roles
- Dates, quantities, units, and durations
- Safety and emergency measures
- Tables after formatting or OCR
- Any statement that affects construction, cost, schedule, or liability
