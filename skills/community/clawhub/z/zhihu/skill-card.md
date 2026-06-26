## Description: <br>
Manage Zhihu AI Bot actions for publishing pins, reacting to content, creating or deleting comments, and fetching ring or comment details with Zhihu API credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keepwonder](https://clawhub.ai/user/keepwonder) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to let an agent operate a Zhihu Bot CLI for publishing and managing Zhihu Ring content with configured API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, react to, comment on, and delete Zhihu content through the configured account. <br>
Mitigation: Review target IDs and generated content before allowing commands that modify Zhihu content. <br>
Risk: Zhihu API credentials grant account-level access to the supported operations. <br>
Mitigation: Keep ZHIHU_APP_KEY and ZHIHU_APP_SECRET out of logs, shared configuration, and source control. <br>


## Reference(s): <br>
- [ClawHub Zhihu release](https://clawhub.ai/keepwonder/zhihu) <br>
- [Zhihu Open Platform](https://open.zhihu.com/) <br>
- [Zhihu OpenAPI base URL](https://openapi.zhihu.com/) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Supported Zhihu Ring](https://www.zhihu.com/ring/host/2001009660925334090) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API results, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIHU_APP_KEY and ZHIHU_APP_SECRET; API calls may publish, react to, comment on, delete, or retrieve Zhihu content.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
