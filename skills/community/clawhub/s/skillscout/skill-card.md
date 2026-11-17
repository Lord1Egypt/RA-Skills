## Description:

Find and evaluate OpenClaw AI skills by trust score and security reviews before installation or recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nashbot67](https://clawhub.ai/user/nashbot67)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and reviewers use SkillScout to search a curated catalog of OpenClaw skills, compare trust scores, and inspect security review details before installing or recommending a skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill recommendations rely on mutable remote or registry content, so catalog entries and trust scores may become stale or poisoned.

Mitigation: Treat SkillScout as a screening aid, require user confirmation before installing recommended skills, and independently review original sources for high-risk use.

Risk: Validation gaps in the review or publishing process could affect which recommendations users or agents trust.

Mitigation: Prefer pinned MCP and package versions, verify review details before acting on them, and avoid automatic installation based only on catalog status.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nashbot67/skills/skillscout)
- [Publisher Profile](https://clawhub.ai/user/nashbot67)
- [SkillScout Catalog](https://nashbot67.github.io/skillscout)
- [SkillScout Catalog API](https://nashbot67.github.io/skillscout/data/skills.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and catalog entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Catalog results may include trust scores, ratings, categories, authors, descriptions, install commands, and review links.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
