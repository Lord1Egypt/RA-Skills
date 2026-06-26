## Description: <br>
微信公众号管理 skill。支持获取 Access Token、永久素材管理、发布能力（发布草稿、查询发布状态、获取已发布列表、删除发布文章）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enihsago](https://clawhub.ai/user/enihsago) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage a WeChat Official Account from an agent workflow, including access-token retrieval, permanent media management, draft publishing, publish-status checks, published-content listing, and article deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live WeChat Official Account credentials and can expose access tokens through command output. <br>
Mitigation: Store credentials in a restricted local config file, avoid passing secrets on the command line, and avoid running token commands in logged sessions. <br>
Risk: Publish and delete commands operate on a real WeChat Official Account with limited built-in safeguards. <br>
Mitigation: Review intended account, media IDs, article IDs, and command arguments before execution; require operator approval for publish and delete workflows. <br>


## Reference(s): <br>
- [WeChat Stable Access Token API](https://developers.weixin.qq.com/doc/subscription/api/base/api_getstableaccesstoken.html) <br>
- [WeChat Permanent Material API](https://developers.weixin.qq.com/doc/subscription/api/material/permanent/api_getmaterial.html) <br>
- [WeChat Publish API](https://developers.weixin.qq.com/doc/subscription/api/public/api_freepublish_batchget.html) <br>
- [WeChat Official Account Error Codes](https://developers.weixin.qq.com/doc/oplatform/developers/errCode/errCode.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/enihsago/wechat-gzh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with Python and shell command examples plus JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local configuration, call WeChat Official Account APIs, upload files, and perform live publish or delete actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
