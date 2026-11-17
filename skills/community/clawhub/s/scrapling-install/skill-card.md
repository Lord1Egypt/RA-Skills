## Description:

Scrapling Install helps agents configure and use Scrapling through MCP guidance for extraction, crawling, and permissioned anti-bot handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frisky1985](https://clawhub.ai/user/frisky1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to choose Scrapling fetch modes, configure MCP access, and apply practical scraping recipes for authorized extraction and crawling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad web fetching, stealth fetching, proxy use, and login-based scraping.

Mitigation: Use it only for authorized targets, keep outbound network access restricted, and avoid stealth, Cloudflare-solving, or proxy modes unless explicitly permitted.

Risk: Examples and helper scripts may write exports, downloads, checkpoints, or crawl data to local storage.

Mitigation: Review file-writing recipes and run the skill in an isolated workspace with only the necessary filesystem permissions.

Risk: Proxy and login workflows can expose credentials if copied into commands or configuration.

Mitigation: Do not hardcode proxy, session, or login secrets; provide credentials through approved secret-management mechanisms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frisky1985/skills/scrapling-install)
- [Scrapling documentation](https://scrapling.readthedocs.io)
- [Fetcher selection documentation](https://scrapling.readthedocs.io/en/latest/fetching/choosing/)
- [Selection methods documentation](https://scrapling.readthedocs.io/en/latest/parsing/selection/)
- [Spiders architecture documentation](https://scrapling.readthedocs.io/en/latest/spiders/architecture.html)
- [Proxy and blocking documentation](https://scrapling.readthedocs.io/en/latest/spiders/proxy-blocking.html)
- [MCP server documentation](https://scrapling.readthedocs.io/en/latest/ai/mcp-server/)
- [Anti-bot handling](artifact/references/anti-bot.md)
- [MCP Server Setup](artifact/references/mcp-setup.md)
- [Spider Recipes](artifact/references/spider-recipes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe MCP calls, Scrapling CLI usage, and helper script commands; helper scripts may emit JSON or console text.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
