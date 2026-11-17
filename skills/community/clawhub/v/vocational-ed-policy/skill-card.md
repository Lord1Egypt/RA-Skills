## Description:

Automatically scrapes vocational education policy documents and project announcements from Chinese Ministry of Education, Ministry of Human Resources, and provincial education department websites, with keyword filtering and periodic summaries.

This skill is for research and development only.

## Publisher:

[erich1566](https://clawhub.ai/user/erich1566)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, policy analysts, and education staff use this skill to collect and summarize China-focused vocational education policy notices, project announcements, and related government documents for review and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags the release as suspicious because it includes unrelated high-impact publishing and deletion instructions.

Mitigation: Review those sections as documentation only and do not execute publishing, deletion, or account-management examples as agent instructions.

Risk: Security evidence says the skill overstates its scraping capabilities and includes an unsafe helper script.

Mitigation: Run the scraper manually in an isolated environment, validate numeric arguments before shell helper use, and pin dependencies before installation.

Risk: Scraped government websites may change structure, block automated access, or return irrelevant links.

Mitigation: Verify result accuracy against source pages, use conservative request rates, prefer HTTPS sources where available, and respect site terms and robots guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erich1566/skills/vocational-ed-policy)
- [Publisher profile](https://clawhub.ai/user/erich1566)
- [Education department website list](references/edu_websites.md)
- [Web scraping implementation notes](references/implementation-notes.md)
- [Testing results and limitations](references/testing-results-and-limitations.md)
- [Framework status note](references/framework_status.md)
- [Ministry of Education source site](https://www.moe.gov.cn)
- [Ministry of Human Resources and Social Security source site](http://www.mohrss.gov.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; scraper runs produce JSON result files and terminal summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English usage text; generated scraping results may need manual validation against source sites.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
