## Description: <br>
Run comprehensive SEO audits on websites and generate scored, prioritized Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and site operators use this skill to crawl authorized websites, check technical, on-page, content, and link SEO signals, and produce prioritized fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit makes live web requests to the target site and discovered internal pages. <br>
Mitigation: Use it only on domains the user owns or is authorized to assess, and keep crawl depth and maximum pages modest. <br>
Risk: Targets can include localhost or private-network URLs if a user supplies them. <br>
Mitigation: Avoid localhost and private-network targets unless that access is intentional and authorized. <br>
Risk: A user-specified report path can overwrite an existing file. <br>
Mitigation: Choose a new report filename or confirm overwrite intent before using the output path. <br>


## Reference(s): <br>
- [SEO Audit Report on ClawHub](https://clawhub.ai/Johnnywang2001/seo-audit-report) <br>
- [Complete SEO Audit Checklist](references/seo-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with scores, issue lists, and recommendations; optional command-line status text during crawling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can be printed to standard output or written to a user-specified Markdown file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
