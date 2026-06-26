## Description: <br>
同程特价机票查询与价格监控技能。通过第三方旅行平台API查询机票价格，支持自然语言解析、价格监控、降价推送（飞书）。当用户需要查询机票价格、监控特定航班价格波动、设置价格提醒时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qi812560784](https://clawhub.ai/user/qi812560784) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and EasyClaw/OpenClaw agents use this skill to parse Chinese natural-language flight queries, retrieve route or flight price results, create price-monitoring subscriptions, and send Feishu price-drop notifications when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route and date queries are sent to third-party travel services, and Feishu notifications may receive query and price details when configured. <br>
Mitigation: Use the skill only when sharing those travel details with the travel provider and Feishu webhook destination is acceptable. <br>
Risk: The security review reports mock flight fallbacks and potentially misleading alert behavior, including monitor creation claims that may not reflect durable setup. <br>
Mitigation: Treat returned prices and subscription confirmations as advisory until verified against the travel provider and local subscription files. <br>
Risk: The installer can make broad changes under ~/.easyclaw/skills. <br>
Mitigation: Review installation changes before running the installer and keep a backup of existing EasyClaw skill files. <br>
Risk: The bundled API exploration script may perform probing behavior against third-party endpoints. <br>
Mitigation: Avoid running scripts/test_api_exploration.py unless the operator has reviewed it and has permission to perform the requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qi812560784/tc-cheapflights) <br>
- [API documentation](references/api_documentation.md) <br>
- [City and airport codes](references/city_airport_codes.md) <br>
- [Natural language examples](references/natural_language_examples.md) <br>
- [Feishu webhook endpoint template](https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx) <br>
- [Tongcheng cheap flights API endpoint](https://wx.17u.cn/cheapflights/newcomparepriceV2/single) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text responses with optional Python and shell snippets, JSON configuration, and notification payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local subscription, history, configuration, and log files when installed and used.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
