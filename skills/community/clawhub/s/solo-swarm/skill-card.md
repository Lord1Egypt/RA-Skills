## Description:

Launches three parallel research agents focused on market, user, and technical analysis to investigate an idea and produce research.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunto2](https://clawhub.ai/user/fortunto2)

### License/Terms of Use:

MIT

## Use Case:

Developers and product builders use this skill to rapidly research an idea from market, user, and technical perspectives, then synthesize the findings into a repository research report with a GO, NO-GO, or PIVOT recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search prior conversations, project metadata, and code across available projects when Solograph or similar internal search tools are connected.

Mitigation: Install and run it only in environments where that access is acceptable, and scope or disable internal search tools unless a specific project or session needs them.

Risk: The workflow writes docs/research.md in the current repository.

Mitigation: Review the generated report and repository diff before accepting or sharing the results.

Risk: Bash access may broaden what the agent can inspect or execute during research.

Mitigation: Disable Bash for routine use unless shell access is required for the investigation.

## Reference(s):

- [Swarm ClawHub release](https://clawhub.ai/fortunto2/skills/solo-swarm)
- [SearXNG Tavily adapter](https://github.com/fortunto2/searxng-docker-tavily-adapter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes docs/research.md in the current project when the workflow completes.]

## Skill Version(s):

1.6.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
