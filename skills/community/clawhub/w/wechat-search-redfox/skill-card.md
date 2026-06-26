## Description: <br>
Searches WeChat Official Account hot articles by keyword, ranks results by relevance, heat, and timeliness, and returns recommendations for content trend research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, WeChat operators, self-media teams, and brand teams use this skill to find recent high-read WeChat articles, compare trend signals, and plan content topics or scheduled tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation reportedly includes a live-looking API key. <br>
Mitigation: Install only after the publisher removes the exposed key, rotates it, replaces it with a placeholder, and documents secure credential supply. <br>
Risk: Recurring push or subscription behavior may create ongoing tracking or unexpected notifications. <br>
Mitigation: Require explicit opt-in, visible schedules, rate limits, and easy cancellation before use. <br>
Risk: Debug mode may expose real or sensitive API responses. <br>
Mitigation: Avoid debug mode with real data unless output is redacted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/wechat-search-redfox) <br>
- [RedFoxHub API key setup](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [WeChat trend data format reference](references/gzh_trend_data_format.md) <br>
- [RedFox hot article API endpoint](https://redfox.hk/story/api/gzh/search/hotArticle) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown tables and prompts, JSON stdout, optional HTML report files, and shell commands for running the Python script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; article data is limited to the provider's recent indexed WeChat articles and may not be real-time.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
