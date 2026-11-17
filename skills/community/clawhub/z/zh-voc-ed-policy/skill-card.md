## Description:

Automatically scrapes Chinese vocational education policy documents and project announcements from national and provincial government websites, with keyword filtering and periodic summaries.

This skill is for research and development only.

## Publisher:

[erich1566](https://clawhub.ai/user/erich1566)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, policy analysts, and education-program developers use this skill to collect Chinese vocational education policy links and project announcements, filter them by keyword, category, date, and source, and generate JSON results or summary reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell guidance and helper-script behavior could affect local files or a ClawHub account if copied or run without review.

Mitigation: Prefer the main Python scraper with simple arguments, avoid running quick_scrape.sh with untrusted input, and do not copy rm -rf, publish, delete, or account-impacting examples unless the target path and account impact are understood.

Risk: Scrape output can be incomplete or stale when government websites change structure, block automation, or return unexpected content.

Mitigation: Review generated JSON against source pages, keep site selectors current, and respect site terms, robots.txt, and rate limits.

Risk: JSON results may be written somewhere unintended if the output path is not reviewed.

Mitigation: Check the --output path before running the scraper and write results to an intended working directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/erich1566/skills/zh-voc-ed-policy)
- [Publisher Profile](https://clawhub.ai/user/erich1566)
- [Education Website Reference](references/edu_websites.md)
- [Web Scraping Implementation Notes](references/implementation-notes.md)
- [Implementation Notes](references/implementation_notes.md)
- [ClawHub Limitations and Workflow](references/clawhub-limitations-and-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with shell commands and JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English CLI output; generated scrape results include source, URL, date, category, keywords, filters, errors, and timestamp.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
