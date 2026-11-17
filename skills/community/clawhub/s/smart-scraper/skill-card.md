## Description:

AI-powered web scraper with intelligent structure recognition that extracts lists, articles, and tables from websites with automatic type detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yadanzheng68-cmyk](https://clawhub.ai/user/yadanzheng68-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scrape user-selected web pages and extract lists, article content, or table data into reusable structured formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-based scraping can fetch untrusted, private-network, or otherwise sensitive target URLs.

Mitigation: Use only permitted target URLs, avoid internal or private-network hosts, and keep target selection under user control.

Risk: Scraped CSV or text output contains untrusted website data.

Mitigation: Review and sanitize exported data before opening it in spreadsheet software or feeding it into downstream systems.

Risk: Scraping a site without authorization can violate site rules or legal obligations.

Mitigation: Confirm permission to scrape the target site and follow applicable site terms before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yadanzheng68-cmyk/skills/smart-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [JSON, CSV, or Markdown emitted as CLI text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npm, installs Playwright, and accepts a target URL, extraction type, output format, maximum item count, and scroll option.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
