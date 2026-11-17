## Description:

Web scraping using the Scrapfly Scraper API with the Python SDK

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapfly](https://clawhub.ai/user/scrapfly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Scrapfly API scraping workflows for collecting web page data, rendering JavaScript-heavy pages, reusing sessions, and returning HTML, JSON, markdown, or text outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports anti-bot bypass, proxy use, and session reuse, which can be misapplied to scraping that is not authorized.

Mitigation: Use it only for websites and data collection workflows where you have authorization, and review the target site's rules before use.

Risk: The skill shows request forwarding patterns that may include cookies, headers, request bodies, or session identifiers.

Mitigation: Avoid sending private cookies, tokens, personal data, or confidential request bodies through the Scrapfly API.

Risk: The setup installs and uses an external SDK and paid API service.

Mitigation: Install the SDK in an isolated environment, pin the package version, and review the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scrapfly/skills/scrapfly-scraper)
- [Scrapfly Scraper API endpoint](https://api.scrapfly.io/scrape)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Scrapfly API key supplied through SCRAPFLY_API_KEY or directly to the client.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
