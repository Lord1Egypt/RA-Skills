## Description:

Zero-bot-detection web scraping for OpenClaw that supports basic HTTP scraping, stealth anti-bot bypass flows, and dynamic browser automation for JavaScript-heavy sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengxinjipai](https://clawhub.ai/user/zhengxinjipai)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to scrape web pages, extract content with CSS selectors, return machine-readable JSON, and handle dynamic pages or anti-bot-protected targets when they have authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks this release suspicious because it is openly designed for stealth scraping and Cloudflare or anti-bot bypass.

Mitigation: Use only on sites where scraping is authorized, follow applicable terms and laws, and require review before using stealth or Cloudflare-solving modes.

Risk: The skill installs and runs browser-enabled scraping dependencies that may interact with untrusted web pages.

Mitigation: Run in an isolated virtual environment or container under an unprivileged account and pin reviewed Scrapling and browser component versions before operational use.

Risk: Scraping authenticated or sensitive URLs can expose private page content in command output or JSON results.

Mitigation: Avoid sensitive targets unless necessary, minimize captured content, and review outputs before sharing or storing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhengxinjipai/skills/scrapling-web-scraper-openclaw)
- [Publisher profile](https://clawhub.ai/user/zhengxinjipai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, and optional JSON scraping results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI can print extracted page data as formatted text or JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
