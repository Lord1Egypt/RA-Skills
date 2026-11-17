## Description:

Quality audit for AI Agent Skills that scores SKILL.md files across five dimensions and returns actionable improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webkong](https://clawhub.ai/user/webkong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, and reviewers use this skill to evaluate local or remote SKILL.md files before installation, after authoring, or before ClawHub/SkillHub submission. It produces a quality score, dimension subscores, and prioritized improvement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A quality score could be mistaken for a security guarantee.

Mitigation: Use this skill as a quality review aid and pair it with security vetting before installing or deploying a skill.

Risk: Audit recommendations may be incomplete or misleading if the target SKILL.md or source URL is wrong.

Mitigation: Point the agent at a specific local SKILL.md or known source and review proposed changes before applying them.

## Reference(s):

- [Audit Rules](references/audit-rules.md)
- [Skill Writing Best Practices](references/best-practices.md)
- [Claude Prompt Engineering Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [OpenClaw Skill Creator](https://github.com/openclaw/openclaw/tree/main/skills/skill-creator)
- [Cursor Agent and Skills Documentation](https://cursor.com/docs/agent)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Martin Fowler: Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with scores and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes overall score, five dimension subscores, P0/P1/P2 recommendations, and install guidance.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
