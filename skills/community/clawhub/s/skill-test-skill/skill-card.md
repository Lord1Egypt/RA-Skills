## Description:

Tests and scores Agent Skills against the Agent Skills specification, producing a concise compliance report with findings, scores, and improvement guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youngfreefjs](https://clawhub.ai/user/youngfreefjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to audit an Agent Skill directory or SKILL.md file for specification compliance, content quality, progressive disclosure, and trigger readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to read every file in the selected skill directory, which can expose secrets or unrelated private content if the target is too broad.

Mitigation: Use the skill only on trusted, scoped skill folders and avoid targets containing .env files, private keys, credentials, unrelated repositories, or symlinks unless additional redaction guardrails are in place.

Risk: Audit findings and improvement suggestions may be incorrect or misleading if applied without review.

Mitigation: Review the generated report and scan the target skill before deploying or publishing changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/youngfreefjs/skills/skill-test-skill)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Anthropic Skill Creator Guide](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Specification Summary](artifact/references/spec-summary.md)
- [Scoring Rubric](artifact/references/scoring-rubric.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report language follows the user's request when English or Chinese is detected.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
