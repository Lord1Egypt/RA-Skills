## Description: <br>
Diagnoses and fixes OpenClaw WeCom channel configuration issues, including connection failures, missing bot credentials, plugin ID mismatches, and unsupported multi-account setups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fclwtt](https://clawhub.ai/user/fclwtt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect WeCom channel status, review OpenClaw configuration, apply plugin ID and single-account configuration fixes, and verify the gateway after changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to read or modify OpenClaw WeCom configuration that may contain bot secrets. <br>
Mitigation: Review proposed changes before applying them, keep a backup of openclaw.json, and avoid sharing real secrets in logs or chats. <br>
Risk: Gateway restart commands may interrupt the current WeCom channel session. <br>
Mitigation: Run restarts during an acceptable maintenance window and verify channel and gateway status after changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fclwtt/skills-5) <br>
- [WeCom OpenClaw plugin](https://github.com/openclaw/wecom-openclaw-plugin) <br>
- [Enterprise WeChat AI Bot documentation](https://open.work.weixin.qq.com/help?doc_id=21657) <br>
- [OpenClaw channel configuration documentation](https://docs.openclaw.ai/channels) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to local OpenClaw configuration and gateway restart commands for user review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
