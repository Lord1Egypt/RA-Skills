## Description: <br>
Set up WeCom (企业微信) as a chat channel for OpenClaw using the official Tencent plugin with WebSocket long-polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengtruman922-dotcom](https://clawhub.ai/user/pengtruman922-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure WeCom as an OpenClaw chat channel, including plugin installation, channel settings, gateway restart, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trusting and installing the external WeCom OpenClaw plugin may expose the deployment to package or integration risk. <br>
Mitigation: Install only when the @wecom/wecom-openclaw-plugin package is intended and trusted for the deployment. <br>
Risk: The WeCom bot secret is required for the WebSocket connection and could be mishandled during setup. <br>
Mitigation: Keep the bot secret protected and store it only in the intended OpenClaw configuration. <br>
Risk: The open sample access policy can allow broad direct-message or group access. <br>
Mitigation: Prefer allowlist or pairing policies when the bot should be limited to specific users or groups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengtruman922-dotcom/wecom-setup) <br>
- [WeCom Open Platform](https://open.work.weixin.qq.com) <br>
- [WeCom AI Bot documentation](https://open.work.weixin.qq.com/help?doc_id=21657) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and troubleshooting instructions; it does not directly modify user configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
