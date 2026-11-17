## Description:

Universal Expert provides Chinese-oriented expert analysis, decision support, and information verification for broad-domain deep analysis requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azazlf09](https://clawhub.ai/user/azazlf09)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to trigger structured, source-aware expert analysis for complex decisions, evaluations, and fact-checking tasks. It is intended for deep analysis requests rather than casual conversation or simple question answering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may browse or search before answering and could encounter private, account-based, or sensitive data.

Mitigation: Require confirmation before any tool accesses sensitive or logged-in data, and review use in private or account-based workflows.

Risk: Expert-style guidance could be over-relied on for legal, financial, life-safety, or other safety-critical decisions.

Mitigation: Require human review for safety-critical, legal, and major financial decisions, especially when confidence is low or source quality is limited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/azazlf09/skills/universal-expert)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Analysis]

**Output Format:** [Markdown with confidence labels and source references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires fact gathering before substantive analysis and calls for human review on life-safety, major financial, or legal decisions.]

## Skill Version(s):

5.3.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
