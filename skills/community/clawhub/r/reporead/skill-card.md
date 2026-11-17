## Description:

RepoRead analyzes GitHub repositories through MCP or REST API access to generate documentation, security audits, architecture summaries, diagrams, and LLM-optimized repository context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdperkins](https://clawhub.ai/user/gdperkins)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect an agent to RepoRead for GitHub repository analysis, documentation generation, security review, architecture diagrams, and LLM-optimized repository summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository URLs, analysis requests, and resulting repository context are sent to the RepoRead external service.

Mitigation: Use the skill for public repositories by default and confirm authorization before analyzing private or proprietary code.

Risk: The skill requires a RepoRead API key for MCP or REST API access.

Mitigation: Store REPOREAD_API_KEY in a protected secret manager or restricted local configuration and avoid committing it or placing it in shared dotfiles.

## Reference(s):

- [RepoRead Homepage](https://www.reporead.com)
- [RepoRead MCP Endpoint](https://api.reporead.com/mcp)
- [RepoRead REST API Base URL](https://api.reporead.com/public/v1)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown, JSON API responses, Mermaid diagrams, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RepoRead API key and sends repository URLs, analysis requests, and repository context to the RepoRead service.]

## Skill Version(s):

1.2.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
