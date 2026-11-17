## Description:

A self-evolution engine for AI agents. Analyzes runtime history to identify improvements and applies protocol-constrained evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmmoeny](https://clawhub.ai/user/mmmoeny)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent teams use this skill to analyze runtime history, select reusable evolution assets, and generate protocol-bound prompts for auditable agent improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad autonomous code-changing behavior can alter repository contents in ways the operator did not intend.

Mitigation: Run in a disposable or controlled test repository, require a clean Git worktree, and use review or dry-run mode before applying changes.

Risk: External Hub connectivity, bridge execution, auto-publish, and auto-update behavior may expose or distribute sensitive project context.

Mitigation: Disable those features unless explicitly required and avoid exposing private session logs, memory files, credentials, or business-sensitive code.

Risk: Validation and evolution loops can execute commands or repeat changes if operated without boundaries.

Mitigation: Keep validation scoped, use review mode for sensitive environments, and monitor loop execution in controlled runs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mmmoeny/skills/repo2)
- [EvoMap](https://evomap.ai)
- [EvoMap Documentation](https://evomap.ai/wiki)
- [GitHub Releases](https://github.com/autogame-17/evolver/releases)
- [Chinese README](README.zh-CN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain-text guidance with inline shell commands and JSON-backed evolution assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local prompts, reports, and GEP asset updates; review or dry-run mode is recommended before applying changes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
