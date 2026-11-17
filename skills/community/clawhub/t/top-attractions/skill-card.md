## Description:

Discover the most popular and highest-rated attractions in any city, including ticket prices, opening hours, and booking links powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to retrieve current attraction recommendations for a city, format comparison tables, and provide booking links from flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global CLI.

Mitigation: Review before installing and use an environment where global npm installs require explicit approval.

Risk: CLI calls may mishandle user-provided travel queries if arguments are built unsafely.

Mitigation: Execute flyai commands with structured arguments rather than shell interpolation.

Risk: The runbook describes persisting raw user travel queries in a local execution log.

Mitigation: Disable or minimize logging and avoid storing raw travel queries unless users have approved it.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/dingtom336-gif/skills/top-attractions)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown comparison tables with booking links and supporting CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI results and should not expose raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
