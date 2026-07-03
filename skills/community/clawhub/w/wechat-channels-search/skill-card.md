## Description: <br>
Searches WeChat Channels content by keyword and returns structured result tables with likes, author, duration, publish time, pagination, and optional daily keyword updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brand operators, marketing teams, and individual users use this skill to research WeChat Channels content trends, monitor keyword performance, browse paginated results, and subscribe to daily keyword updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords and pagination state are sent to Redfox using REDFOX_API_KEY. <br>
Mitigation: Use a key with an understood scope and validity period, keep it out of code and logs, and confirm it can be rotated or revoked. <br>
Risk: Daily subscriptions create recurring external API calls. <br>
Mitigation: Before enabling a subscription, confirm where the scheduled task is stored and how to list, cancel, or disable it. <br>


## Reference(s): <br>
- [API Data Field Mapping](references/api-mapping.md) <br>
- [RedFoxHub API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/wechat-channels-search) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tables and guidance, with JSON returned by the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; visible result tables omit direct work links and can include pagination prompts and subscription guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
