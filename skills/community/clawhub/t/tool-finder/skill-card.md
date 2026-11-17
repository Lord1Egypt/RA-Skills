## Description:

Searches ClawHub skills and Smithery MCP servers, ranks results, labels sources, and supports guided installation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lironghai](https://clawhub.ai/user/lironghai)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to discover relevant skills or MCP servers across ClawHub and Smithery, compare ranked results, and receive command-line guidance for installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags persistent agent routing rules that can steer future tool discovery behavior.

Mitigation: Only copy AGENTS.md or TOOLS.md routing snippets when persistent tool-finder behavior is intentionally desired, and review those rules separately before adoption.

Risk: The security review flags unconfirmed package installation through mutable remote CLIs.

Mitigation: Require separate confirmation before installation, review the target source and version, and prefer pinned or inspected packages for higher-risk environments.

Risk: Search results can be incomplete or misleading when APIs fail, rate limit, or return low-relevance matches.

Mitigation: Use verbose or exact searches for important selections, verify results on the source marketplace, and avoid treating scores as a security or quality guarantee.

## Reference(s):

- [Tool Finder ClawHub release](https://clawhub.ai/lironghai/skills/tool-finder)
- [Publisher profile](https://clawhub.ai/user/lironghai)
- [ClawHub](https://clawhub.ai)
- [Smithery API](https://api.smithery.ai)
- [Brave Search API](https://brave.com/search/api/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output may include ranked tool names, source labels, relevance scores, recommendation levels, warnings, and installation guidance.]

## Skill Version(s):

1.7.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
