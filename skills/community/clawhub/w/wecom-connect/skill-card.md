## Description: <br>
Helps an agent connect Enterprise WeChat to OpenClaw by generating an authorization link, waiting for user confirmation, polling for the bot credentials, writing local OpenClaw configuration, and restarting the gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EaseLearnAI](https://clawhub.ai/user/EaseLearnAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need an agent to bind an Enterprise WeChat bot to OpenClaw. The skill guides the authorization-link flow, waits for the user to complete authorization in WeCom, then configures OpenClaw with the returned bot credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Enterprise WeChat bot credentials in the local OpenClaw configuration file. <br>
Mitigation: Treat ~/.openclaw/openclaw.json as sensitive, restrict access to it, and install the skill only when binding Enterprise WeChat to OpenClaw is intended. <br>
Risk: The setup flow restarts the OpenClaw gateway after credentials are written. <br>
Mitigation: Run the skill in an environment where a gateway restart is acceptable and expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EaseLearnAI/wecom-connect) <br>
- [Enterprise WeChat authorization endpoint](https://work.weixin.qq.com/ai/qc/generate?source=wecom-cli&plat=3) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an authorization link for the user, may poll the WeCom result endpoint after user confirmation, and writes OpenClaw channel configuration when credentials are returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
