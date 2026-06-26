## Description: <br>
Enables agents to upload media, create and manage drafts, publish articles, and query publishing status for WeChat Official Accounts through the WeChat MP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan32382](https://clawhub.ai/user/ryan32382) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent prepare WeChat Official Account content workflows, including media upload, draft creation, article publishing, draft deletion, and status checks. It is intended for accounts with valid WeChat MP API credentials and the required Official Account permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish articles to a WeChat Official Account. <br>
Mitigation: Configure the agent to save drafts first and require explicit human approval before publishing. <br>
Risk: The skill can delete WeChat Official Account drafts. <br>
Mitigation: Require explicit confirmation for draft deletion and use dedicated credentials with the minimum permissions needed. <br>
Risk: WeChat MP credentials and cached access tokens grant account access if exposed. <br>
Mitigation: Protect config and token files, prefer dedicated credentials, and restrict file permissions to the account owner. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryan32382/wechat-mp-publisher-zhizi) <br>
- [README](README.md) <br>
- [Technical Specification](TECH_SPEC.md) <br>
- [Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Text and JSON responses from OpenClaw tools, with Markdown and shell command guidance in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeChat MP AppID/AppSecret credentials and local configuration or environment variables.] <br>

## Skill Version(s): <br>
2.0.3 (source: ClawHub server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
