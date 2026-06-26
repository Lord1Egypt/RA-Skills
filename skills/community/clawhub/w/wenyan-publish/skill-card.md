## Description: <br>
AI-ready skill to format and publish Markdown articles to WeChat Official Accounts using Wenyan CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caol64](https://clawhub.ai/user/caol64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to guide agents through formatting Markdown articles and publishing them to WeChat Official Accounts with Wenyan CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent using this skill can publish externally through a delegated WeChat Official Account. <br>
Mitigation: Require manual final approval before any preview or publish submission. <br>
Risk: WeChat AppID and secret values may be exposed if credential checks print them into logs or chat. <br>
Mitigation: Store credentials in protected environment configuration and avoid commands that echo secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caol64/wenyan-publish) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML frontmatter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WECHAT_APP_ID and WECHAT_APP_SECRET environment variables and an installed wenyan-cli.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
