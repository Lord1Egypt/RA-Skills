## Description:

Evaluate and improve code with Topos. Use for complexity reduction, security checks, refactor verification, and PLATINUM/GOLD goals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krv-labs](https://clawhub.ai/user/krv-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding agents use Topos to assess structural code quality, find complexity and security issues, guide focused refactors, and check whether those changes improve project scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Topos structural scores and refactor suggestions do not prove that code behavior is correct or provide complete security assurance.

Mitigation: Test and review proposed changes; pair structural security findings with dedicated security tooling for high-stakes code.

Risk: Installation can execute a downloaded installer, add GitNexus, or register agent integrations.

Mitigation: Review the installer, trust dependencies before installing them, choose only needed integrations, and analyze the intended repository.

## Reference(s):

- [Topos documentation](https://docs.krv.ai/topos/)
- [Topos agent contract](https://docs.krv.ai/topos/agents.html)
- [Topos on ClawHub](https://clawhub.ai/krv-labs/skills/topos)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands]

**Output Format:** [CLI tables and ranked file lists; MCP structured JSON payloads and per-function details]

**Output Parameters:** [Single-stream output scoped to a file or repository]

**Other Properties Related to Output:** [Provides structural scores, verdicts, and refactor guidance; does not establish functional correctness.]

## Skill Version(s):

1.0.27 (ClawHub release; source skill frontmatter: 0.15.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
