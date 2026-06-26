## Description: <br>
小红书作品爬取工具，根据关键词爬取小红书热门作品数据，支持日期范围和排序筛选，并以结构化表格展示结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, brand and e-commerce teams, MCN planners, and content operators use this skill to search Xiaohongshu posts by keyword, date range, and ranking mode for topic research, competitive analysis, trend exploration, and report export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Xiaohongshu search terms and a RedFox API key to redfox.hk. <br>
Mitigation: Use only search terms appropriate for third-party processing, verify the API key source and revocation options, and keep REDFOX_API_KEY out of committed files, prompts, logs, and output. <br>
Risk: Generated CSV and HTML reports can contain sensitive content research or competitive intelligence. <br>
Mitigation: Store generated reports in controlled locations, review contents before sharing, and delete reports that are no longer needed. <br>
Risk: The security summary flags local active HTML reports with limited scoping safeguards. <br>
Mitigation: Open only reports generated from trusted crawler output and avoid redistributing HTML reports without review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/xiaohongshu-crawler-redfox) <br>
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox](https://redfox.hk) <br>
- [RedFox Xiaohongshu Crawl API Endpoint](https://redfox.hk/story/api/xhs/crawl/work) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown tables and guidance, JSON from crawler scripts, and optional CSV or HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; generated reports are written locally and may contain sensitive search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
