## Description:

根据用户需求从多个 Skill 市场查找、比较并评估合适的 Skill，披露来源、信任度和安全风险。用户不知道安装哪个 Skill 时调用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaour](https://clawhub.ai/user/xiaour)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find, compare, and evaluate candidate Skills from multiple marketplaces when they know the capability they need but not which Skill to install.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted marketplace data may influence displayed recommendations, links, or install commands.

Mitigation: Independently verify each source page and command before installing or running any candidate Skill.

Risk: The skill may surface misleading candidate information if source pages are incomplete, hostile, or malformed.

Mitigation: Treat low-trust or unverifiable candidates as unsuitable for recommendation and rely on the disclosed evidence limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaour/skills/skill-kill)
- [Server-resolved GitHub source](https://github.com/xiaour/skill-kill)
- [Candidate schema](artifact/candidate.schema.json)
- [Candidate renderer](artifact/renderer.js)

## Skill Output:

**Output Type(s):** [Markdown, HTML, Shell commands, Guidance]

**Output Format:** [Concise Markdown table by default, or HTML table when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs up to 5 candidate Skills with match score, trust level, risk level, source, permissions, recommendation, and verified install command when available.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
