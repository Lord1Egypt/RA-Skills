## Description: <br>
Web Search Free helps agents use Exa MCP through mcporter for web, code, company, people, crawling, and deep research queries without API keys, with fallback to Multi Search Engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciding](https://clawhub.ai/user/deciding) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to route current-information lookups, code searches, company and people research, webpage crawling, and longer research tasks through Exa MCP. It is intended for workflows where external web information is useful and no Exa API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, people or company lookups, and research prompts may be sent to Exa or a fallback search provider. <br>
Mitigation: Do not include secrets, private or internal URLs, confidential business material, or sensitive personal data in queries. <br>
Risk: The skill broadly prefers web-search-free before built-in web tools, which can be inappropriate when no lookup is needed or a built-in tool is better suited. <br>
Mitigation: Override the preference when built-in tools, local evidence, or no web lookup better fits the task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/deciding/web-search-free) <br>
- [Exa MCP Server GitHub Repository](https://github.com/exa-labs/exa-mcp-server) <br>
- [Exa MCP Server npm Package](https://www.npmjs.com/package/exa-mcp-server) <br>
- [Exa Documentation](https://exa.ai/docs) <br>
- [Exa Search Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP call examples; tool results return text, links, summaries, code context, or research reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter with Exa MCP configured; falls back to Multi Search Engine when Exa tools are unsuitable or fail.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
