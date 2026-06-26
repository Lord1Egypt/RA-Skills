## Description: <br>
Advanced web scraping guidance for using Scrapling via MCP, including extraction, crawling, anti-bot handling, and practical recipes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DevBD1](https://clawhub.ai/user/DevBD1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute permissioned web scraping workflows with Scrapling, including MCP setup, selector-based extraction, browser-backed fetching, proxy-aware crawling, and spider recipes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Advanced scraping, anti-bot, stealth fetching, and proxy guidance can be misused against sites where the user lacks authorization. <br>
Mitigation: Use only on owned or explicitly authorized sites, respect robots.txt and terms of service, avoid paywalls or access controls, and apply rate limits. <br>
Risk: Local scripts and Scrapling dependencies execute code in the user's Python environment. <br>
Mitigation: Install in a pinned virtual environment, review examples before running them, and verify any file-writing or deletion behavior before use. <br>
Risk: Browser-backed fetching and proxy rotation can increase request volume or bypass ordinary blocking signals if configured carelessly. <br>
Mitigation: Start with the HTTP fetcher, lower concurrency, add delays, use proxies only for permissioned reliability needs, and monitor target-site responses. <br>


## Reference(s): <br>
- [MCP Server Setup](references/mcp-setup.md) <br>
- [Anti-bot Handling](references/anti-bot.md) <br>
- [Proxy Rotation](references/proxy-rotation.md) <br>
- [Spider Recipes](references/spider-recipes.md) <br>
- [Scrapling Quick Reference](references/api_reference.md) <br>
- [Scrapling Recipes](references/recipes.md) <br>
- [Scrapling References](references/links.md) <br>
- [Scrapling Repository](https://github.com/D4Vinci/Scrapling) <br>
- [Scrapling Documentation](https://scrapling.readthedocs.io) <br>
- [Scrapling MCP Server Documentation](https://scrapling.readthedocs.io/en/latest/ai/mcp-server/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, JSON configuration examples, and optional script output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Scrapling MCP calls, Python examples, scraping strategy, and safety guidance for authorized targets.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
