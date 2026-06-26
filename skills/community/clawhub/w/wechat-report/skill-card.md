## Description: <br>
Generate a structured comparison report for multiple WeChat Official Account articles under one topic, including article metadata, engagement status, content-structure tables, writing-pattern tags, and an optional later Feishu sync step. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content researchers, editors, and marketing teams use this skill to collect several WeChat Official Account articles for one topic and compare their metadata, engagement availability, structure, titles, openings, endings, and reusable writing hooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches search results and WeChat article pages, runs browser automation, and stores scraped article content and metadata locally. <br>
Mitigation: Use it only in workspaces where local retention of scraped content is acceptable, review generated files before sharing, and set collect_engagement to false when browser-based engagement collection is not needed. <br>
Risk: A WeChat login or verification flow may expose browser session state to the skill's Playwright profile. <br>
Mitigation: Use a dedicated browser profile for WeChat access and avoid reusing a personal or broadly privileged browser profile. <br>
Risk: The article extractor dependency influences what content is collected and parsed. <br>
Mitigation: Review and pin the external extractor dependency before relying on the outputs in production workflows. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/abigale-cyber/wechat-report) <br>
- [Publisher Profile](https://clawhub.ai/user/abigale-cyber) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Text] <br>
**Output Format:** [Local Markdown report plus structured raw JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a comparison report under content-production/inbox/ and raw article data under content-production/inbox/raw/wechat-report/.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
