## Description:

智能网页数据采集器。自动识别网页结构，批量抓取列表/表格/详情页数据，支持导出JSON/CSV/Excel。内置反爬策略适配。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjstate](https://clawhub.ai/user/cjstate)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and data engineers use this skill to configure and run authorized web data collection from list, table, and detail pages, then export results as JSON, CSV, or Excel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill drives an unsandboxed browser to arbitrary user-supplied URLs without network or local-resource limits.

Mitigation: Run it in an isolated environment and avoid internal, local, or otherwise sensitive URLs.

Risk: Scraping unauthorized websites or ignoring robots.txt can create legal, compliance, or operational risk.

Mitigation: Use it only on sites you are authorized to scrape and configure conservative request delays.

Risk: Scraped exports may contain sensitive or regulated data.

Mitigation: Review exports before sharing or storing them and apply the same controls used for other sensitive datasets.

Risk: Runtime dependencies execute in the local Node.js environment.

Mitigation: Review or pin dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjstate/skills/xh-smart-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with command examples, JSON configuration examples, and generated export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports may contain scraped data and should be handled as potentially sensitive.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
