## Description: <br>
全网持续收录每日超过1000+公众号10w+文章内容，向用户推送公众号达到10w+阅读的热门文章；当用户需要获取全领域的公众号热门文章、或订阅每日10w+文章推送、特定领域爆款文章时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators, creators, editors, marketing teams, and researchers use this skill to retrieve WeChat Official Account 10w+ article rankings by date and category, analyze viral content patterns, and generate shareable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Redfox API key and evidence.security reports unsafe credential-handling guidance that could lead an agent to read shell profile files for secrets. <br>
Mitigation: Configure REDFOX_API_KEY through a scoped environment variable or OpenClaw secret configuration, do not store it in prompts, logs, or generated files, and do not allow the agent to inspect shell profile files to retrieve credentials. <br>
Risk: Generated JSON, HTML, or PDF-exportable reports may contain user query results and article data. <br>
Mitigation: Treat generated reports as local files, review contents before sharing, and delete temporary files that are no longer needed. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/redfox-data/wechat-10w-hot) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox article data API](https://redfox.hk/story/api/cozeSkill/getWxDataByCategoryAndTime) <br>
- [API specification](references/api-spec.md) <br>
- [Category mapping](references/category-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown responses with shell command examples, JSON intermediate files, and optional HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may produce local JSON, HTML, or PDF-exportable report files containing article query results.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
