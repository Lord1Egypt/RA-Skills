## Description:

Extract structured data from any web page. Supports CSS selectors, auto-detection of tables and lists, JSON/CSV output formats. Use when asked to scrape a website, extract data from a page, pull product info, gather contact details, or collect listings from a URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agents use this skill to extract structured data from static web pages, including selected elements, tables, links, page structure, and multi-page listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scraper can fetch arbitrary URLs from the agent machine's network position, including local or internal resources if a user or untrusted prompt supplies those targets.

Mitigation: Use explicit public http or https URLs and do not allow untrusted pages or prompts to choose crawl targets.

Risk: The scraper can save output to a user-specified path, which could overwrite files if misused.

Mitigation: Review output paths before execution and write results only to intended working directories.

Risk: Contact-data scraping can create privacy, authorization, or anti-spam concerns.

Mitigation: Scrape contact data only with authorization and in compliance with applicable privacy and anti-spam rules.

## Reference(s):

- [Smart Web Scraper ClawHub listing](https://clawhub.ai/mariusfit/skills/smart-web-scraper)
- [Publisher profile](https://clawhub.ai/user/mariusfit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus extracted data emitted as text, JSON, CSV, or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write extracted results to a user-specified output file.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
