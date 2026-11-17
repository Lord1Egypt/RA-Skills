## Description:

Travel Master Mini is a minimal Chinese-language travel-planning helper that extracts itinerary fields with local keyword matching and computes a convergence score without external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract basic travel-planning details from Chinese-language trip requests and identify which itinerary fields still need clarification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is minimal and Chinese-oriented, so multilingual or complex itinerary requests may produce incomplete results.

Mitigation: Use it for lightweight Chinese-language field extraction and review the missing fields and status before relying on the result.

Risk: Local keyword matching can miss destinations, budgets, transport modes, or travel intent outside the supported patterns.

Mitigation: Treat extracted fields as a starting point and ask follow-up questions when required fields remain missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timo2026/skills/travel-master-mini)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text with structured field extraction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces extracted itinerary anchors, missing fields, convergence rate, and status for a single user request.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
