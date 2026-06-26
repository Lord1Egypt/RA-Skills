## Description: <br>
Advanced web scraping guidance for Scrapling with MCP setup, extraction patterns, crawling recipes, and anti-bot handling strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frisky1985](https://clawhub.ai/user/frisky1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and configure Scrapling MCP, choose fetcher strategies, build web extraction flows, and plan permissioned crawls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes anti-bot, stealth fetching, and proxy guidance that could be misused against sites without authorization. <br>
Mitigation: Install and use it only for sites you own, administer, or are explicitly authorized to access; follow robots.txt, site terms, rate limits, and the bundled guardrails. <br>
Risk: Proxy, API, account, and session examples may involve sensitive credentials. <br>
Mitigation: Do not hardcode credentials in scripts or shared configuration; use environment-specific secret storage and review configs before committing or sharing them. <br>
Risk: Cloudflare-solving and stealth examples can bypass access friction if applied outside approved workflows. <br>
Mitigation: Require explicit approval before enabling stealth or Cloudflare-solving options, and keep usage limited to legitimate reliability testing or permitted automation. <br>
Risk: Checkpoint reset or cleanup snippets can delete crawl state or local artifacts. <br>
Mitigation: Review deletion commands before execution, scope them to disposable crawl directories, and keep backups for data that must be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frisky1985/scrapling-install) <br>
- [Scrapling repository](https://github.com/D4Vinci/Scrapling) <br>
- [Scrapling documentation](https://scrapling.readthedocs.io) <br>
- [Fetcher selection documentation](https://scrapling.readthedocs.io/en/latest/fetching/choosing/) <br>
- [Selection methods documentation](https://scrapling.readthedocs.io/en/latest/parsing/selection/) <br>
- [Spider architecture documentation](https://scrapling.readthedocs.io/en/latest/spiders/architecture.html) <br>
- [Proxy and blocking documentation](https://scrapling.readthedocs.io/en/latest/spiders/proxy-blocking.html) <br>
- [MCP server documentation](https://scrapling.readthedocs.io/en/latest/ai/mcp-server/) <br>
- [MCP Server Setup](references/mcp-setup.md) <br>
- [Anti-bot handling](references/anti-bot.md) <br>
- [Proxy Rotation](references/proxy-rotation.md) <br>
- [Spider Recipes](references/spider-recipes.md) <br>
- [Scrapling quick reference](references/api_reference.md) <br>
- [Scrapling recipes](references/recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP configuration snippets, Scrapling command examples, selector recipes, and Python helper script usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
