## Description:

Python web scraping toolkit for data extraction, pagination handling, anti-blocking techniques, Selenium-based JavaScript rendering, and structured JSON/CSV/text output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract data from authorized websites, including paginated and JavaScript-rendered pages, and convert scraped results into structured outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthorized or non-compliant scraping can violate site terms, robots.txt, privacy expectations, or copyright.

Mitigation: Use only on authorized public sources or official APIs, check robots.txt and site terms, avoid login-protected or personal data, and apply rate limits.

Risk: Cookie export, login-wall handling, CAPTCHA-solving, proxy rotation, and browser-detection bypass guidance can be misused to evade access controls.

Mitigation: Avoid those techniques unless explicit permission exists and testing is contained; do not use sensitive credentials in shared or untrusted environments.

Risk: The Selenium helper configures Chrome with no-sandbox behavior, which can increase risk on arbitrary sites.

Mitigation: Remove Chrome's no-sandbox option before running Selenium against arbitrary sites, pin dependencies, and run browsers in an isolated environment.

## Reference(s):

- [Anti-Blocking Strategies](references/anti-blocking.md)
- [Web Scraper ClawHub page](https://clawhub.ai/ericlooi504/skills/python-web-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python code; helper scripts output JSON, CSV, or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write JSON, CSV, or text files when an output path is provided.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
