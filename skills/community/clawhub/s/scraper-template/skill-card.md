## Description:

Helps developers adapt a Playwright-based template for scraping open-platform API documentation and exporting standardized JSON interface records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woai36d](https://clawhub.ai/user/woai36d)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create platform-specific API documentation scrapers by subclassing a reusable Playwright scraper base and exporting interface metadata to standardized JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated output file paths can be influenced by scraped module identifiers and module names.

Mitigation: Sanitize module ids and names, resolve output paths, and verify generated files stay under the selected output directory before scraping untrusted or externally controlled documentation sites.

Risk: The skill operates against external documentation pages with Playwright.

Mitigation: Review target sites and scraper subclasses before execution, and run scraping in a controlled environment with only required access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/woai36d/skills/scraper-template)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, JSON files]

**Output Format:** [Markdown guidance with shell commands, Python code patterns, and standardized JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scraper subclasses must implement menu expansion, API navigation, and API detail extraction for the target platform.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
