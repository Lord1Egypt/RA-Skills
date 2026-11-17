## Description:

Refines vague, ambiguous, incorrect, or incomplete user commands into valid, fact-checked, environment-aware, and verifiable execution plans before the agent acts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Agents and developers use this skill to clarify ambiguous user requests, correct mistaken terminology or assumptions, check environment constraints, and produce a scoped execution plan before running tools or taking system actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reshape ambiguous requests before action, so a wrong interpretation could still lead the agent toward an unintended plan.

Mitigation: For high-impact actions, require explicit assumptions and confirmation before changing, deleting, spending, posting, or using sensitive data.

Risk: Current-data requests may be unreliable if the agent cannot verify recent facts.

Mitigation: Mark unverifiable current information as unknown or outdated and ask for confirmation or use an approved current source before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/user-intent-refinement)
- [Publisher profile](https://clawhub.ai/user/pmuhammadagus-byte)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or concise text with optional command suggestions and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clarified intent, assumptions, risk checks, environment constraints, execution steps, and verification results.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
