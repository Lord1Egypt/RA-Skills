## Description:

Professional web scraping for OpenClaw with stealth Playwright automation, anti-bot bypass, JavaScript rendering, and structured data extraction from modern websites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[showmemercy19-rgb](https://clawhub.ai/user/showmemercy19-rgb)

### License/Terms of Use:

Commercial

## Use Case:

Developers and agents use this skill to scrape JavaScript-heavy public web pages, render browser content, and extract structured data using automatic extraction or caller-provided CSS selectors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can browse arbitrary target URLs with weakened browser protections.

Mitigation: Run it only for authorized scraping tasks in an isolated container or VM with restricted outbound network access.

Risk: The SCRAPELESS_LICENSE_KEY secret can be exposed in output.

Mitigation: Treat the license key as a secret, avoid sharing command output from license validation, and keep it out of logs and shared shells.

Risk: Scraping authenticated, internal, or unauthorized sites can create data-handling and policy risk.

Mitigation: Avoid authenticated or internal URLs and confirm permission, robots guidance, and data-use constraints before scraping.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/showmemercy19-rgb/skills/scrapeless-pro-skill)
- [Scrapeless Pro homepage](https://cosmic-lollipop-a61cc5.netlify.app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI examples and generated JSON, CSV, or Markdown scrape results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npx, Playwright Chromium, and SCRAPELESS_LICENSE_KEY.]

## Skill Version(s):

1.0.3 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
