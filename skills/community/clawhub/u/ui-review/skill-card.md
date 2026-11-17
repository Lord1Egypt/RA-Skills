## Description:

Runs a structured UI/UX heuristic review based on Nielsen's 10 usability principles for screenshots, mockups, wireframes, product pages, app screens, and design comps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dawen-ye](https://clawhub.ai/user/dawen-ye)

### License/Terms of Use:

MIT-0

## Use Case:

Product designers, developers, and UX reviewers use this skill to evaluate UI screenshots and design comps against Nielsen's usability heuristics. It helps produce prioritized findings, explicit assumptions, and concrete recommendations tied to visible interface elements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The review can be misleading when a screenshot is cropped, blurry, or missing important flow context.

Mitigation: Ask a short clarification round first, state assumptions when context is missing, and label low-confidence findings.

Risk: The agent could overreach by treating inferred product intent as fact.

Mitigation: Separate visible evidence from inference and tie recommendations to specific UI elements.

Risk: The skill could be asked to access credentials, execute commands, or inspect unrelated local data even though that is unnecessary for UI review.

Mitigation: Keep use limited to provided UI images or screens and do not request credentials, command execution, or unrelated local data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dawen-ye/skills/ui-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown review with context summary, assumptions, prioritized findings, heuristic coverage, priority actions, and open questions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity ratings and confidence notes when screenshot evidence is ambiguous.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
