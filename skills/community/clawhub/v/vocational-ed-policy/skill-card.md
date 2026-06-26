## Description: <br>
Automatically scrapes vocational education policy documents and project announcements from the Ministry of Education, Ministry of Human Resources, and provincial education department websites, with keyword filtering and periodic summaries. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[erich1566](https://clawhub.ai/user/erich1566) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, education policy analysts, and developers use this skill to collect and summarize Chinese vocational education policy announcements from public government websites. It supports local command-line scraping workflows with filters for keywords, date ranges, categories, sources, and output files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the scripts sends automated requests to public government websites and stores results locally. <br>
Mitigation: Install dependencies from trusted package sources, keep request rates modest, respect site terms and robots.txt, and review generated local files before sharing or using them. <br>
Risk: Optional scheduled scraping can repeatedly contact external sites without further review. <br>
Mitigation: Review cron examples before use, set conservative schedules, and confirm that the configured output paths and request cadence are appropriate. <br>
Risk: Documented testing found date extraction, filtering, and keyword matching limitations that can produce stale, irrelevant, or incomplete results. <br>
Mitigation: Validate scraped records against source websites, use narrow filters where possible, and treat generated summaries as aids rather than authoritative policy records. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/erich1566/vocational-ed-policy) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Education Website Reference List](artifact/references/edu_websites.md) <br>
- [Web Scraping Implementation Notes](artifact/references/implementation-notes.md) <br>
- [Testing Results and Limitations](artifact/references/testing-results-and-limitations.md) <br>
- [Ministry of Education](https://www.moe.gov.cn) <br>
- [Ministry of Human Resources and Social Security](http://www.mohrss.gov.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scraper outputs local JSON result files containing source counts, document records, errors, timestamps, and applied filters.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
