## Description: <br>
Scrape web pages using Scrapling with anti-bot bypass, stealth headless browsing, spiders, adaptive scraping, and JavaScript rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d4vinci](https://clawhub.ai/user/d4vinci) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch, crawl, and extract website data when simple web fetches are insufficient, including dynamic pages, protected sites, and spider-based scraping workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables stealth anti-bot bypass, proxy use, cookie use, and persistent browser sessions. <br>
Mitigation: Use it only on sites the user is authorized to scrape, prefer non-stealth fetches first, and require explicit user direction before using protected sessions, proxies, or anti-bot bypass options. <br>
Risk: Cookies, browser profiles, proxy credentials, and persistent caches can expose sensitive session data. <br>
Mitigation: Avoid real session cookies or browser profiles unless necessary, prefer safe temporary paths, and close or clean persistent sessions and caches when finished. <br>
Risk: Fetched web content can contain prompt injection or hidden instructions. <br>
Mitigation: Use `--ai-targeted` for command-line scraping intended for agent consumption and keep extracted content scoped with selectors when possible. <br>


## Reference(s): <br>
- [Scrapling documentation](https://scrapling.readthedocs.io/en/latest/index.html) <br>
- [Scrapling Official Skill on ClawHub](https://clawhub.ai/d4vinci/scrapling-official) <br>
- [Fetching guide](references/fetching/choosing.md) <br>
- [Stealthy fetching guide](references/fetching/stealthy.md) <br>
- [Spider getting started guide](references/spiders/getting-started.md) <br>
- [MCP server reference](references/mcp-server.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary output files, crawler checkpoints, browser sessions, or cache directories when the user chooses those workflows.] <br>

## Skill Version(s): <br>
0.4.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
