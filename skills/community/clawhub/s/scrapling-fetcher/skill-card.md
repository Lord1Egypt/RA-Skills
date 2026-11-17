## Description:

Provides a Scrapling-based web scraping workflow for fetching pages, extracting structured data with CSS or XPath selectors, and using HTTP, stealth, or dynamic browser modes on sites the user is authorized to scrape.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeminay](https://clawhub.ai/user/jeminay)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation engineers use this skill to retrieve web page text or structured fields when ordinary fetch tools fail because of JavaScript rendering, rate limits, or anti-bot challenges. It is intended for authorized scraping workflows and selector-based extraction, not for bypassing restricted access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send requests through HTTP, stealth, and browser-based modes to external sites.

Mitigation: Use it only for sites the user is authorized to scrape, respect applicable terms and robots.txt, and avoid passing credentials or sensitive URLs unless the destination is trusted.

Risk: Installing full Scrapling dependencies and browser binaries expands the local runtime surface.

Mitigation: Install and run the skill in a virtual environment or disposable container without administrator privileges.

Risk: The optional MCP server starts a local HTTP service.

Mitigation: Start the server only when explicitly needed and only in a trusted local environment.

Risk: Adaptive scraping can persist element fingerprints or local state in the working directory.

Mitigation: Run adaptive workflows in a controlled directory and remove stored state when it is no longer needed.

## Reference(s):

- [Scrapling Patterns Reference](references/patterns.md)
- [Scrapling on PyPI](https://pypi.org/project/scrapling/)
- [ClawHub Skill Page](https://clawhub.ai/jeminay/skills/scrapling-fetcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python examples, plain text extraction, and optional JSON arrays]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit selector matches as text lines or JSON; stealth and dynamic modes may use headless Chromium.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
