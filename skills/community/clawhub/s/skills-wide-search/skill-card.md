## Description:

Searches ClawHub, skills.sh, and SkillsMP for agent skills, ranks candidates by health signals, and returns installation-focused recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trip1ewhy](https://clawhub.ai/user/trip1ewhy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover agent skills across multiple registries, compare candidates using health and security signals, and return ranked recommendations with links and install commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to ClawHub, skills.sh, SkillsMP, and the r.jina.ai proxy.

Mitigation: Avoid using sensitive internal names or confidential search terms when invoking the skill.

Risk: Recommended install commands may include npx commands or commands ending in --yes.

Mitigation: Review each command before execution and prefer pinned or trusted package sources.

Risk: User-provided queries can become unsafe if interpolated directly into shell commands.

Mitigation: Pass queries as inert arguments or URL-encoded parameters instead of string-splicing user text into shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trip1ewhy/skills/skills-wide-search)
- [Publisher profile](https://clawhub.ai/user/trip1ewhy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown recommendations with links, scores, and inline shell install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ranked health scores and install commands for selected skills.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
