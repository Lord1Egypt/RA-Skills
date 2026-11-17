## Description:

Extract structured data from websites with browser automation for single pages and paginated flows, saving results as CSV, JSON, or XLSX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinanping-cpu](https://clawhub.ai/user/yinanping-cpu)

### License/Terms of Use:


## Use Case:

Developers, data analysts, and operations teams use this skill to extract structured fields from authorized web pages, product listings, articles, job postings, and directories for downstream analysis or monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can target broad web content and may be used on sites or data the user is not authorized to scrape.

Mitigation: Use it only for authorized sites and data, and review site terms, robots.txt, and applicable law before running a scrape.

Risk: Anti-blocking guidance mentions proxies, IP rotation, and CAPTCHA services.

Mitigation: Do not use those techniques to bypass access controls, rate limits, or explicit site restrictions.

Risk: CSV and XLSX outputs can contain formula-like values from scraped pages.

Mitigation: Treat generated spreadsheets as untrusted and sanitize formula-like values before opening or sharing them.

Risk: Scraping may collect personal data that is unnecessary for the task.

Mitigation: Minimize personal data collection and confirm privacy obligations before storing or using extracted data.

## Reference(s):

- [CSS Selector Reference](references/css-selectors.md)
- [ClawHub Skill Page](https://clawhub.ai/yinanping-cpu/skills/yinan-web-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; scraper runs can produce CSV, JSON, or XLSX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local scripts with CSS selector field definitions and writes extracted data to user-selected output files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
