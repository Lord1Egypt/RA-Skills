## Description:

Uses Playwright with stealth browser behavior to retrieve protected or JavaScript-rendered web pages when standard fetch tools cannot access the content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdt328606](https://clawhub.ai/user/sdt328606)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect web pages that block lightweight fetch requests, require JavaScript rendering, or need browser-style page interaction. It can provide scraping guidance, setup commands, JavaScript examples, and text returned from a Playwright-based MCP tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell-based URL handling can allow unintended command execution.

Mitigation: Replace shell interpolation with safe argument passing and strict URL validation before exposing the MCP tool.

Risk: Browser automation may have broad access to a live browser session.

Mitigation: Run only in an isolated environment with a dedicated browser profile, and do not connect it to a normal logged-in browser.

Risk: Scraping protected, high-friction, or login-gated sites can violate site rules or collect sensitive content.

Mitigation: Confirm permission to scrape, respect robots.txt and rate limits, and avoid automated credential entry or sensitive-account sessions.

Risk: Unpinned or unaudited browser automation dependencies can change behavior across installs.

Mitigation: Pin and audit dependencies before deployment, and reinstall Chromium only from trusted package sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdt328606/skills/stitch-playwright-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples; the MCP tool returns text content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Playwright, Chromium, and related Node.js dependencies when executing browser automation.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
