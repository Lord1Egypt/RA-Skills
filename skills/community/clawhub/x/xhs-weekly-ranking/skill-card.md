## Description: <br>
专注于小红书平台的内容趋势分析，基于近7天热门笔记TOP50深度洞察，支持25个垂直领域分类查询、冷门爆款挖掘及每日订阅推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brand marketers, MCN operators, and growth analysts use this skill to query Xiaohongshu seven-day hot-note rankings, analyze viral content patterns, and generate shareable trend reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFoxHub API key and includes guidance for persistent credential handling. <br>
Mitigation: Use a skill-scoped secret store or explicit environment variable, avoid writing keys into shell profiles, and never expose the key in prompts, logs, or generated files. <br>
Risk: Recurring daily push behavior can create ongoing automation after a user query. <br>
Mitigation: Require clear user confirmation before creating any recurring daily push and make the schedule and content scope explicit. <br>
Risk: Generated HTML previews and report files may expose queried trend data and outbound links. <br>
Mitigation: Ask for confirmation before generating or previewing reports when the query or destination is sensitive, and review generated files before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/xhs-weekly-ranking) <br>
- [Core workflow](references/core_workflow.md) <br>
- [RedFoxHub](https://redfox.hk) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown ranking tables and analysis, with optional standalone HTML report files and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses REDFOX_API_KEY for RedFoxHub access; default ranking output shows TOP20 with optional expansion to TOP50.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
