## Description:

Manages WeChat Official Account workflows, including access token retrieval, permanent material management, draft publishing, publication status checks, published article listing, and deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enihsago](https://clawhub.ai/user/enihsago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage WeChat Official Account content workflows from an agent, including token retrieval, material upload and retrieval, draft publishing, status checks, and published article deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat AppID, AppSecret, and access tokens.

Mitigation: Use a restricted config file or secret store, avoid passing AppSecret on the command line, and avoid logging get-token output.

Risk: The skill can publish and delete WeChat Official Account content.

Mitigation: Require explicit confirmation before publishing or deleting WeChat content.

## Reference(s):

- [WeChat Stable Access Token API](https://developers.weixin.qq.com/doc/subscription/api/base/api_getstableaccesstoken.html)
- [WeChat Permanent Material API](https://developers.weixin.qq.com/doc/subscription/api/material/permanent/api_getmaterial.html)
- [WeChat Publishing API](https://developers.weixin.qq.com/doc/subscription/api/public/api_freepublish_batchget.html)
- [WeChat API Error Codes](https://developers.weixin.qq.com/doc/oplatform/developers/errCode/errCode.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API Calls, Files]

**Output Format:** [Markdown guidance with Python snippets, shell commands, JSON API results, and saved media files for binary material retrieval.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WeChat AppID and AppSecret configuration; operations call api.weixin.qq.com and may create, publish, retrieve, or delete official account content.]

## Skill Version(s):

1.0.0 (source: release evidence, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
