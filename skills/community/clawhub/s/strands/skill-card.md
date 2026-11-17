## Description:

Build and run Python-based AI agents using the AWS Strands SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trippingkelsea](https://clawhub.ai/user/trippingkelsea)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, configure, and run Python Strands agents with local, hosted, or AWS-backed model providers. It also supports custom tools, MCP integration, multi-agent patterns, session persistence, and generated agent scaffolds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agents can be scaffolded with broad file and shell access.

Mitigation: Run generated agents in a sandbox or disposable workspace, inspect generated Python before execution, and avoid granting access to credentials or private files.

Risk: Untrusted prompts, model IDs, or MCP servers can change agent behavior or expand the effective tool surface.

Mitigation: Use trusted inputs, pin dependency and MCP server versions, and review provider and MCP configuration before running an agent.

## Reference(s):

- [Strands SDK repository](https://github.com/strands-agents/sdk-python)
- [Strands SDK Cheatsheet](references/cheatsheet.md)
- [ClawHub skill page](https://clawhub.ai/trippingkelsea/skills/strands)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and shell examples; helper scripts can generate Python project files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated agent scaffolds may include file-read, file-write, and shell-command tools.]

## Skill Version(s):

2.0.3 (source: ClawHub release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
