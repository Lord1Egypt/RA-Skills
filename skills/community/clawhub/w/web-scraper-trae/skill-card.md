## Description:

Opens browser and scrapes webpage content using Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengjia626](https://clawhub.ai/user/zhengjia626)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create and run a Playwright-based scraper for a user-provided URL, returning the page title, visible text, full HTML, and original URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can render arbitrary user-provided URLs and return full page contents.

Mitigation: Run only against trusted, intended public URLs and avoid private, authenticated, localhost, intranet, cloud metadata, or unknown hostile pages unless destination controls and output limits are added.

Risk: The Playwright launch configuration disables Chromium sandbox protections.

Mitigation: Execute scraping in an isolated environment with constrained network access and no sensitive credentials.

Risk: Scraped HTML and page text may include large, sensitive, or untrusted content.

Mitigation: Review outputs before reuse, limit captured content when possible, and avoid scraping pages that may expose secrets or personal data.

## Reference(s):


## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with JavaScript and bash snippets; scraped page data is returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns page title, visible body text, full HTML source, and the original URL.]

## Skill Version(s):

1.0.1 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
