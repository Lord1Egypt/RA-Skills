## Description:

Install the full Solo Factory toolkit: 23 startup skills plus the optional solograph MCP server for code intelligence, knowledge-base search, session search, and web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunto2](https://clawhub.ai/user/fortunto2)

### License/Terms of Use:

MIT

## Use Case:

Developers and startup builders use this skill to install and configure a Solo Factory agent toolkit for researching, validating, building, deploying, reviewing, and promoting startup projects. It can also guide optional setup of the solograph MCP server for project code intelligence and searchable knowledge sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs broad, persistent third-party installations and may add user-scoped agent tooling that can access project code, session history, or knowledge-base content.

Mitigation: Review the upstream repositories and package sources before installing, prefer pinned versions or immutable commits, and enable the Claude plugin, hooks, or solograph MCP server only when that access is acceptable.

Risk: The artifact includes a direct remote script execution command for installing uv.

Mitigation: Avoid running curl-to-shell commands directly; inspect the installer first or use a trusted package-manager installation path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fortunto2/skills/solo-factory)
- [Solo Factory repository](https://github.com/fortunto2/solo-factory)
- [solograph repository](https://github.com/fortunto2/solograph)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask whether to enable optional MCP setup when no install mode is provided.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
