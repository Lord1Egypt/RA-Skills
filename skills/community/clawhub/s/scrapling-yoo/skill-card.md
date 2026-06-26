## Description: <br>
Advanced web scraping with Scrapling, providing MCP-native guidance for extraction, crawling, and anti-bot handling through mcporter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cccccqqqqq](https://clawhub.ai/user/cccccqqqqq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan and run permissioned Scrapling-based web extraction, including MCP setup, selector guidance, crawling patterns, and troubleshooting for dynamic or protected pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anti-bot bypass, Cloudflare solving, proxy rotation, login sessions, and protected-page scraping can be misused or violate site rules when used without authorization. <br>
Mitigation: Use these modes only for sites where access is explicitly permitted, and prefer normal fetching before escalating to stealth, solving, proxy, or login-session workflows. <br>
Risk: Broad crawling can create excessive traffic or collect more content than intended. <br>
Mitigation: Set explicit domains, crawl depth, concurrency limits, and delays before running crawls. <br>
Risk: Scrape outputs, downloaded media, cookies, and crawl checkpoints may leave sensitive or stale data on disk. <br>
Mitigation: Run in an isolated environment and clean up generated files, cookies, and crawl checkpoints when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cccccqqqqq/scrapling-yoo) <br>
- [Scrapling repository](https://github.com/D4Vinci/Scrapling) <br>
- [Scrapling documentation](https://scrapling.readthedocs.io) <br>
- [MCP server setup](references/mcp-setup.md) <br>
- [Anti-bot handling](references/anti-bot.md) <br>
- [Proxy rotation](references/proxy-rotation.md) <br>
- [Spider recipes](references/spider-recipes.md) <br>
- [Scrapling quick reference](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also guide use of Scrapling MCP tool calls and helper scripts that produce JSON or JSONL scrape outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
