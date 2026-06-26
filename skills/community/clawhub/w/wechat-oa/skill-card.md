## Description: <br>
WeChat Official Account draft management toolkit for managing drafts, publishing workflows, images, materials, and account-audience lookups through official WeChat APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy8663](https://clawhub.ai/user/andy8663) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to manage WeChat Official Account drafts, media uploads, generated cover or inline images, published article lists, and material cleanup through guided agent commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access WeChat publication account user or subscriber information. <br>
Mitigation: Use lookup commands only for specific user-requested tasks and avoid pasting or exporting subscriber lists unnecessarily. <br>
Risk: Publishing and material-management commands can affect live WeChat Official Account drafts, materials, or published-content workflows. <br>
Mitigation: Confirm the target account, permissions, media IDs, and requested action before creating, updating, deleting, or uploading content. <br>
Risk: The connected publishing tool may rely on account credentials or permissions. <br>
Mitigation: Confirm which credentials and account permissions are in use before installation or execution. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/andy8663/wechat-oa) <br>
- [ClawHub skill page](https://clawhub.ai/andy8663/wechat-oa) <br>
- [WeChat Official Account Platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code, Files] <br>
**Output Format:** [Markdown guidance with command examples, configuration steps, and generated or updated article/media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce draft logs, cover images, inline infographics, uploaded media references, and WeChat draft or material management actions.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
