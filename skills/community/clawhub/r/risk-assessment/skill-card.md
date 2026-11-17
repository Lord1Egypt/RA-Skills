## Description:

Framework-directable information security risk assessment. Identifies threats, evaluates likelihood/impact via a 3x3 matrix, maps findings to any compliance framework, and recommends risk treatment options with prioritization guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dangsllc](https://clawhub.ai/user/dangsllc)

### License/Terms of Use:

MIT-0

## Use Case:

Security, compliance, and engineering teams use this skill to turn system descriptions, asset inventories, questionnaire answers, policies, or uploaded documents into structured information security risk assessments mapped to the selected compliance framework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide sensitive security information, credentials, personal data, or regulated records to an LLM provider while using the skill.

Mitigation: Use only with an approved model and data handling workflow, and avoid submitting live secrets, credentials, unnecessary personal data, or regulated records unless organizational policy permits it.

Risk: Risk scores, framework mappings, and treatment recommendations may be incomplete or unsuitable for a specific organization.

Mitigation: Have qualified security or compliance reviewers validate findings before they are added to a risk register or used for management decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dangsllc/skills/risk-assessment)
- [Publisher profile](https://clawhub.ai/user/dangsllc)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON object with risk findings, scoring, framework mappings, executive summary, and prioritized actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings use a 3x3 likelihood and impact matrix and include treatment recommendations.]

## Skill Version(s):

0.1.3 (source: release metadata; artifact frontmatter lists 2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
