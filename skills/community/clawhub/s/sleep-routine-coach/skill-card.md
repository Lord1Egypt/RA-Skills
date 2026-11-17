## Description:

Provides privacy-first, non-diagnostic sleep habit coaching with short setup, consent-gated wind-down reminders, gradual sleep-time adjustment, local sleep records, correction controls, and descriptive weekly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raindongdry](https://clawhub.ai/user/raindongdry)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent for gentle sleep-routine support, consented reminder planning, gradual sleep-time adjustments, local record keeping, corrections, and descriptive trend summaries. It is not intended to diagnose, treat, or cure sleep disorders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the all-data deletion command can delete an arbitrary chosen directory if misused.

Mitigation: Review deletion-control usage before installation and run deletion only against the intended sleep-routine data directory; a safer implementation would validate an app-owned directory and remove only known app files.

Risk: The skill handles user-reported sleep habits and reminder preferences that may be sensitive.

Mitigation: Use the documented local storage controls, obtain explicit storage consent before writing records, and keep live user data outside the skill or repository.

Risk: Sleep guidance could be mistaken for medical advice.

Mitigation: Keep responses non-diagnostic, avoid treatment or cure claims, and refer users to appropriate healthcare professionals for persistent, concerning, or impairing symptoms.

## Reference(s):

- [Sleep Routine Coach on ClawHub](https://clawhub.ai/raindongdry/skills/sleep-routine-coach)
- [Publisher Profile](https://clawhub.ai/user/raindongdry)
- [Skill Homepage](https://github.com/RAINDONGDRY/sleep-routine-coach)
- [Data Schema and Deterministic Rules](references/data-schema.md)
- [Evidence Sources](references/evidence-sources.md)
- [Interaction Protocol](references/interaction-protocol.md)
- [Safety Boundaries](references/safety-boundaries.md)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON outputs from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local user-approved sleep data and optional, separately consented reminder scheduling.]

## Skill Version(s):

0.2.1 (source: server release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
