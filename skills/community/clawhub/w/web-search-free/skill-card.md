## Description:

Provides web, code, company, people, crawl, and deep research search guidance through Exa MCP without requiring API keys, with fallback guidance for Multi Search Engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciding](https://clawhub.ai/user/deciding)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to perform public web research, code-context lookup, company and people research, webpage crawling, and longer-form research reports through configured search tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, URLs, company or person names, and code-search text may be sent to Exa and fallback search providers.

Mitigation: Use the skill for public web research and avoid private source code, internal URLs, credentials, personal data, or confidential business context unless the user explicitly approves that sharing.

Risk: The skill broadly directs agents to prefer this third-party search path before built-in search or fetch tools.

Mitigation: Require deliberate use for tasks where third-party search is appropriate, and review the remote MCP configuration before installation.

## Reference(s):

- [Exa MCP Server GitHub](https://github.com/exa-labs/exa-mcp-server)
- [Exa MCP Server npm Package](https://www.npmjs.com/package/exa-mcp-server)
- [Exa Documentation](https://exa.ai/docs)
- [Exa Search Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search behavior depends on mcporter, Exa MCP tools, and optional fallback to Multi Search Engine; result volume is controlled by tool parameters such as numResults, tokensNum, and maxCharacters.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact _meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
