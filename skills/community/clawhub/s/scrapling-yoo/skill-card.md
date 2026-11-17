## Description:

Advanced web scraping with Scrapling - MCP-native guidance for extraction, crawling, and anti-bot handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cccccqqqqq](https://clawhub.ai/user/cccccqqqqq)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to choose Scrapling fetchers, configure MCP-based scraping workflows, and apply extraction, crawling, proxy, and anti-bot handling patterns for authorized web data collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad web fetching, browser automation, proxy use, and anti-bot handling that may be unsafe without clear scope.

Mitigation: Run it in a constrained agent environment, restrict egress to approved public domains, and use anti-bot or proxy features only with authorization.

Risk: Scraping workflows may expose credentials or sensitive traffic through untrusted proxies.

Mitigation: Avoid sending credentials through untrusted proxies and block loopback, private, link-local, and metadata addresses.

Risk: Dependency and browser automation behavior may vary across environments.

Mitigation: Pin dependencies where possible and review the skill before installing it in an autonomous agent.

## Reference(s):

- [Scrapling Yoo ClawHub Page](https://clawhub.ai/cccccqqqqq/skills/scrapling-yoo)
- [MCP Server Setup](references/mcp-setup.md)
- [Anti-bot handling (permissioned)](references/anti-bot.md)
- [Scrapling quick reference](references/api_reference.md)
- [Proxy Rotation](references/proxy-rotation.md)
- [Spider Recipes](references/spider-recipes.md)
- [Scrapling documentation](https://scrapling.readthedocs.io)
- [Scrapling MCP server documentation](https://scrapling.readthedocs.io/en/latest/ai/mcp-server/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline Python, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Scrapling MCP calls, local helper scripts, and authorization guardrails for scraping workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
