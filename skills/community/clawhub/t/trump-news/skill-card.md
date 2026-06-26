## Description: <br>
每日拉取特朗普相关新闻（来自官方与主流通讯社信息源），经 AI 翻译成中文、编辑后推送给用户 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wall-nut417](https://clawhub.ai/user/Wall-nut417) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to fetch public Trump-related news, translate the gathered summaries into Chinese, and receive a concise news digest through chat or an optional configured delivery channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Truth Social fetching requires account credentials or a token. <br>
Mitigation: Enable the Truth Social option only when the user is comfortable providing those credentials, and store them as environment variables rather than embedding them in prompts or files. <br>
Risk: The optional truthbrush dependency changes the runtime dependency surface. <br>
Mitigation: Pin and review the truthbrush package before enabling optional Truth Social support. <br>
Risk: Scheduled or Telegram delivery can send news digests to the wrong recipient or at the wrong cadence if misconfigured. <br>
Mitigation: Confirm the recipient and schedule before enabling Telegram or cron delivery. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Wall-nut417/trump-news) <br>
- [Publisher profile](https://clawhub.ai/user/Wall-nut417) <br>
- [White House Briefing Room feed](https://www.whitehouse.gov/briefing-room/feed/) <br>
- [Federal Register documents API](https://www.federalregister.gov/api/v1/documents.json) <br>
- [SCOTUSblog feed](https://www.scotusblog.com/feed/) <br>
- [truthbrush package](https://pypi.org/project/truthbrush/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown news digest with source links and optional shell commands for fetching or delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Chinese summaries from fetched public-source English news; optional Truth Social support requires user-provided credentials or token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
