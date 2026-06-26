## Description: <br>
Complete the creation, editing, and publishing of WeChat Official Account articles through browser automation simulating manual operation. No API key required; operates directly on the Official Account platform backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators who manage WeChat Official Accounts use this skill to create, preview, schedule, and publish articles through browser automation while preserving user confirmation for QR-code steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a live WeChat Official Account and can publish or schedule public content. <br>
Mitigation: Review the article, target account, mass-notification setting, and schedule before scanning any publishing confirmation QR code. <br>
Risk: Login, preview, and publishing verification depend on admin WeChat QR-code scans. <br>
Mitigation: Only scan QR codes after confirming the displayed account, page state, and intended operation. <br>
Risk: Mass notification quotas and post-publish edit limits can make accidental publication difficult to correct. <br>
Mitigation: Keep mass notification disabled unless explicitly requested, preview the article first, and confirm publishing options before final approval. <br>


## Reference(s): <br>
- [WeChat Official Account Platform](https://mp.weixin.qq.com) <br>
- [ClawHub skill page](https://clawhub.ai/openlark/wechat-mp-article-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with browser automation command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user QR-code confirmation for login, preview, and publishing actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
