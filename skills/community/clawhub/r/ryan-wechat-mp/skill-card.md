## Description: <br>
Automates WeChat Official Account article publishing with media upload, draft management, publishing, status checks, and draft deletion through the WeChat MP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan32382](https://clawhub.ai/user/ryan32382) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams managing a WeChat Official Account can use this skill to upload media, create drafts, publish articles, inspect publish status, and remove drafts from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public WeChat articles and delete drafts. <br>
Mitigation: Use draft mode by default, require explicit human approval before publishing or deletion, and verify article title, content, cover media, and target account before action. <br>
Risk: The skill requires WeChat App ID, App Secret, and access-token handling. <br>
Mitigation: Store credentials outside source control with restrictive permissions, use environment variables or a protected config file, and rotate credentials if they are exposed. <br>
Risk: Media upload accepts local file paths. <br>
Mitigation: Upload only intended files, confirm path and media type before execution, and avoid granting the agent broad filesystem access. <br>
Risk: The artifact documentation references npm install and build steps, but the release evidence includes only the skill document. <br>
Mitigation: Review the actual implementation source and dependencies before running install, build, or publishing workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryan32382/ryan-wechat-mp) <br>
- [WeChat Official Account API Overview](https://developers.weixin.qq.com/doc/offiaccount/en/Getting_Started/Overview.html) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Configuration Guidance] <br>
**Output Format:** [JSON responses with success, message, and optional data fields; guidance may include Markdown, code examples, shell commands, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operations may create or delete remote WeChat drafts, upload media, publish public articles, and cache access tokens.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
