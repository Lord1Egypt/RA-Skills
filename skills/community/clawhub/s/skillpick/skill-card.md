## Description:

SkillPick helps agents and users compare AI skills, find strong candidates, inspect alternatives, and decide which skill is worth installing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjihua007-rgb](https://clawhub.ai/user/huangjihua007-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and skill marketplace users use this skill to browse top skills, search by intent, compare alternatives, assemble workflow recommendations, and inspect quality scores before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports suspicious behavior because the skill encourages installing unrelated skills through an unpinned third-party CLI.

Mitigation: Review installation guidance before use and prefer official, direct, pinned, and verifiable installation channels.

Risk: Local query logs may be written when a data directory is present.

Mitigation: Use the skill only where local query logging is acceptable, or remove and monitor the data directory before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huangjihua007-rgb/skills/skillpick)
- [ClawHub Publisher Profile](https://clawhub.ai/user/huangjihua007-rgb)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text CLI recommendations and browser-rendered recommendation views, sometimes including installation commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a bundled local skill catalog for recommendations.]

## Skill Version(s):

6.9.4 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
