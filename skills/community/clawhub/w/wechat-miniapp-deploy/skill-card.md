## Description: <br>
Helps agents deploy and manage WeChat Mini Programs with the official miniprogram-ci CLI, including code upload, previews, versioning, review preparation, and CI/CD deployment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to prepare WeChat Mini Program deployments, upload versions, generate preview QR codes, configure CI/CD, and prepare submissions for WeChat review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat CI private keys, AppID values, and AppSecret may be exposed through prompts, repositories, or CI logs. <br>
Mitigation: Store secrets in a secret manager or CI secret store, avoid pasting them into prompts, redact logs, and remove temporary key files after use. <br>
Risk: Automated API review submission may publish incorrect metadata or submit before privacy requirements are complete. <br>
Mitigation: Prefer manual review submission unless automation is necessary, and verify privacy declarations, permissions, preview QR output, and review metadata before submitting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lm203688/wechat-miniapp-deploy) <br>
- [WeChat Mini Program admin console](https://mp.weixin.qq.com) <br>
- [WeChat access token API](https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=$APPID&secret=$APPSECRET) <br>
- [WeChat submit audit API](https://api.weixin.qq.com/wxa/submit_audit?access_token=$ACCESS_TOKEN) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, YAML, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deployment checklists, command examples, CI configuration snippets, API examples, and review-readiness guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
