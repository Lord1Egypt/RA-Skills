## Description:

Guides agents through Tribunal commands for TDD enforcement, quality gates, secret scanning, Agent Teams hooks, CI integration, MCP tools, and plugin packs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koshaji](https://clawhub.ai/user/koshaji)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to run and configure Tribunal quality gates across local development, CI pipelines, Claude Code hook workflows, MCP integrations, and multi-agent handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tribunal and plugin packs may execute or configure quality-gate behavior in development and CI environments.

Mitigation: Review the Tribunal package and any plugin packs before use, and prefer pinned versions or trusted sources.

Risk: .tribunal audit logs may contain file paths, agent IDs, or operational details.

Mitigation: Keep .tribunal audit logs out of source control when those details are sensitive.

## Reference(s):

- [Tribunal documentation](https://tribunal.dev)
- [Tribunal repository](https://github.com/thebotclub/tribunal)
- [ClawHub skill page](https://clawhub.ai/koshaji/skills/tribunal-usage)
- [Publisher profile](https://clawhub.ai/user/koshaji)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JSON, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides usage instructions for an external Tribunal CLI and related project configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
