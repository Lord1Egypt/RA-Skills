## Description:

A voice-learning writing assistant that helps users communicate in their own style by learning from writing examples, audience context, and corrections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanl1](https://clawhub.ai/user/evanl1)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external communicators, and writers use this skill to draft emails, replies, documents, reports, and team feedback in a style calibrated from their own writing samples and corrections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and persists broad personal writing samples, profile data, audience context, and possibly team-member information.

Mitigation: Use it only with writing samples and profile data the user is comfortable storing; confirm memory scope before use and review or delete voice profile data when possible.

Risk: Drafting confidential emails, documents, or reviews can expose sensitive personal or workplace information through memory-backed style calibration.

Mitigation: Avoid confidential or regulated content unless memory access, retention, and deletion controls have been confirmed for the deployment.

## Reference(s):

- [Sage project homepage](https://github.com/nicholasgasior/sage)
- [Sage Voice on ClawHub](https://clawhub.ai/evanl1/skills/sage-voice)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown writing drafts, replies, document structures, feedback text, and calibration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on and update sage-cognitive memory for voice profiles, audience-specific registers, corrections, and recent draft context.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
