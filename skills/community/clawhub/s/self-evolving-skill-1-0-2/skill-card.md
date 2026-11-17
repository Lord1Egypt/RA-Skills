## Description:

Meta-cognitive self-learning system - Automated skill evolution based on predictive coding and value-driven mechanisms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[86293073](https://clawhub.ai/user/86293073)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to create, execute, analyze, list, save, and load self-evolving OpenClaw skills through CLI, TypeScript, and MCP-style tools. It helps agents analyze embeddings, track execution outcomes, and persist learned skill state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes local state under OpenClaw-related directories, which may retain sensitive context or embeddings.

Mitigation: Install only when local persistence is acceptable, and review or clear its storage after handling sensitive data.

Risk: The skill may run a local Python MCP helper.

Mitigation: Review the local helper configuration before use and run it with only the filesystem access needed for the workflow.

Risk: Some functionality may not work because Python core files referenced by the artifact are absent.

Mitigation: Verify the required core files and dependencies before relying on skill creation, execution, or analysis workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/86293073/skills/self-evolving-skill-1-0-2)
- [Project homepage](https://github.com/whtoo/self-evolving-bot)
- [README](README.md)
- [Installation guide](INSTALLATION.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON responses, CLI text, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local skill state under OpenClaw-related storage paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata); artifact metadata, package.json, and openclaw.yaml report 1.0.2

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
