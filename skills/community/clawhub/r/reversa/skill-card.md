## Description:

Reversa transforms legacy software systems into executable specifications and formal behavior contracts for AI coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Reversa to analyze legacy codebases, generate executable SDD contracts, and audit changes against those contracts before directing AI coding agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-derived analysis results and generated contracts may be shared with a mutable third-party Habilis MCP endpoint with unclear data boundaries.

Mitigation: Use the skill only for repositories suitable for third-party processing, and avoid repositories containing secrets or highly sensitive business logic unless exclusions are enforced.

Risk: The skill requires a Habilis MCP token that could grant access beyond the immediate task if over-scoped or mishandled.

Mitigation: Use a narrowly scoped token, store it in environment variables rather than source files, and rotate it if exposure is suspected.

Risk: MCP-generated contracts, analysis, or commands may be incomplete or misleading.

Mitigation: Treat MCP responses as untrusted suggestions and review generated contracts, file changes, and commands before applying them.

## Reference(s):

- [Reversa research paper](https://arxiv.org/abs/2605.18684)
- [Habilis MCP developer portal](https://xvix.com.br)
- [ClawHub Reversa skill page](https://clawhub.ai/rafacpti23/skills/reversa)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated SDD contracts, analysis summaries, audit guidance, and commands for Hermes or MCP clients.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and clawhub.json report 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
