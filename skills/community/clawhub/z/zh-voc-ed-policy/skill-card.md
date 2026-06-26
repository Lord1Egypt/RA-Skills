## Description: <br>
Scrapes vocational education policy documents and project application announcements from Chinese national and provincial education websites, with keyword filtering and periodic summary support. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[erich1566](https://clawhub.ai/user/erich1566) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, education policy analysts, and developers use this skill to collect public vocational education policy notices, project announcements, and related government documents for review and summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated scraping can fail or produce incomplete results when government site structures change or when sites block automated requests. <br>
Mitigation: Verify important results against the original government pages and adjust selectors, target URLs, or request cadence when failures appear. <br>
Risk: The skill can write local result files and includes optional examples for cron scheduling and ClawHub publishing workflows. <br>
Mitigation: Review output paths and optional shell commands before execution, especially commands that publish, rename, delete, or schedule repeated runs. <br>
Risk: Frequent requests to public websites may violate site expectations or trigger anti-scraping controls. <br>
Mitigation: Use conservative run frequency, keep request delays enabled, and follow applicable robots.txt, copyright, and terms-of-use requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/erich1566/zh-voc-ed-policy) <br>
- [Education Department Website List](references/edu_websites.md) <br>
- [Web Scraping Implementation Notes](references/implementation-notes.md) <br>
- [Framework Status](references/framework_status.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON scraping results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local result files when an output path is supplied; supports Chinese and English user-facing output.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
