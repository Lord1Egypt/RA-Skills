## Description: <br>
Automates a WeChat Official Account article workflow from topic planning through drafting, humanized editing, formatting, cover handling, and draft creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenjiahui11](https://clawhub.ai/user/chenjiahui11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and WeChat Official Account operators use this skill to turn a topic into a planned, polished article draft that can be saved to the WeChat backend. It requires WeChat app credentials, IP allowlisting, Python dependencies, and the included license-check flow before automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included license flow sends a paid card key and stable device fingerprint to a plain-HTTP licensing server. <br>
Mitigation: Install only if the publisher is trusted; prefer HTTPS licensing or a trusted override via TMO_LICENSE_SERVER before entering a card key. <br>
Risk: The workflow requires WeChat App ID and App Secret configuration, which can enable account access if mishandled. <br>
Mitigation: Protect WECHAT_APPID and WECHAT_APPSECRET, restrict execution to approved environments, and verify WeChat IP allowlisting before use. <br>
Risk: Automated draft and media creation can publish or prepare account content that has not been reviewed. <br>
Mitigation: Require explicit operator approval and review generated article, cover, and draft details before creating or using WeChat drafts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenjiahui11/weixin-wechat-channel) <br>
- [Publisher profile](https://clawhub.ai/user/chenjiahui11) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or prepare WeChat draft content after credentials, network access, and license checks are configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
