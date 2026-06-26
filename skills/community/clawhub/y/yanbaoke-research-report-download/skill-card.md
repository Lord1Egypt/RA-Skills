## Description: <br>
Searches Yanbaoke research reports across industry, brokerage, and institutional sources, returns report details and content, and can download source files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanbaoke](https://clawhub.ai/user/yanbaoke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to search Yanbaoke's research-report corpus, filter reports by topic, publisher, report type, stock, date, and page count, and retrieve downloadable PDF, DOC, or PPT report links when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloads require an API key, and the artifact shows examples that pass or persist credentials in shell-accessible locations. <br>
Mitigation: Use a low-privilege or free-tier key, avoid sharing keys in chat, and store credentials in a secret manager or restricted environment file instead of a shell startup file when possible. <br>
Risk: Report summaries and investment-oriented responses may be incomplete, outdated, or unsuitable for decision-making on their own. <br>
Mitigation: Treat output as informational, verify dates and source reports independently, and review important market or trading decisions with appropriate professional judgment. <br>
Risk: Generated download links expire quickly and may expose access to report files while valid. <br>
Mitigation: Use links promptly, avoid posting active links in shared channels, and re-run the authorized download flow when a fresh link is needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yanbaoke/yanbaoke-research-report-download) <br>
- [Yanbaoke Platform](https://pc.yanbaoke.cn) <br>
- [Yanbaoke API Key](https://pc.yanbaoke.cn/openclaw) <br>
- [Search API](https://api.yanbaoke.cn/skills/search_report) <br>
- [Download API](https://api.yanbaoke.cn/skills/report_download/{uuid}?format={format}) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with report summaries, metadata fields, downloadable links, and command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output can include report UUIDs, titles, publishers, dates, page counts, content excerpts, available formats, and links; download links expire after a short time.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
