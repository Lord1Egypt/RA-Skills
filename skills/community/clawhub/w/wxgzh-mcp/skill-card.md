## Description: <br>
Manages WeChat Official Account drafts, image uploads, draft creation, publication, and access token caching for MCP clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[279458179](https://clawhub.ai/user/279458179) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent manage WeChat Official Account draft workflows, including credential-backed token retrieval, media uploads, draft listing, deletion, and publishing where the account permits it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents access to WeChat AppSecret-derived tokens and account actions. <br>
Mitigation: Treat AppSecret and access tokens like passwords, keep config.json out of source control, and restrict MCP server access to trusted clients. <br>
Risk: The skill can delete or publish drafts through credential-backed API calls. <br>
Mitigation: Require human confirmation before deletion or publication and review draft content before use. <br>
Risk: Publishing support depends on WeChat account type and certification status. <br>
Mitigation: Confirm account permissions and fall back to manual publishing for personal subscription accounts. <br>


## Reference(s): <br>
- [ClawHub wxgzh-mcp release page](https://clawhub.ai/279458179/wxgzh-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/279458179) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com) <br>
- [WeChat Official Account API endpoint](https://api.weixin.qq.com/cgi-bin) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Configuration, Guidance, JSON] <br>
**Output Format:** [JSON responses from MCP tools plus Markdown and code examples in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeChat AppID, AppSecret, configured IP allowlist, and account permissions for publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
