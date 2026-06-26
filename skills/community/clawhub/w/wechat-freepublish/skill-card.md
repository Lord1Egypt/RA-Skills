## Description: <br>
Submits WeChat Official Account draft media IDs for formal publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need an agent to submit a WeChat Official Account draft for formal publication from a known media_id after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A successful publish action may immediately push the article to followers. <br>
Mitigation: Require explicit final user confirmation and verify the media_id before running the publish command. <br>
Risk: The skill requires a WeChat access token to submit publication requests. <br>
Mitigation: Use the narrowest practical WeChat token and provide it only through the WECHAT_ACCESS_TOKEN environment variable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell command execution and JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WECHAT_ACCESS_TOKEN and a user-confirmed media_id before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
