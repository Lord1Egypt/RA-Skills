## Description: <br>
企业微信整合服务技能 - 包含普通回调和会话内容存档功能 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyl2835](https://clawhub.ai/user/cyl2835) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and enterprise operations teams use this skill to deploy and configure an Enterprise WeChat archive service with callback handling, message storage, query endpoints, and Cloudflare Tunnel deployment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the artifact ships with hardcoded Enterprise WeChat credentials. <br>
Mitigation: Remove embedded credentials, rotate any exposed Enterprise WeChat secrets, and load secrets only from an operator-controlled secret store or configuration file before deployment. <br>
Risk: The security summary says sensitive chat-archive APIs are exposed without adequate built-in access controls. <br>
Mitigation: Add strong authentication, authorization, and network restrictions before exposing callback, query, debug, or management endpoints through a tunnel or public domain. <br>
Risk: The security guidance calls out fixed third-party domain constants and public exposure risk. <br>
Mitigation: Replace fixed domain constants with verified operator-owned domains and review Cloudflare Tunnel, firewall, IP allowlist, and rate-limit settings before production use. <br>
Risk: The security guidance requires verification of encryption, retention, logging, and legal or employee-notice obligations for archived chats. <br>
Mitigation: Complete a compliance review covering chat archival consent, retention, encryption, access logging, backup handling, and data deletion before processing real employee communications. <br>


## Reference(s): <br>
- [企业微信API接口文档](references/企业微信API接口文档.md) <br>
- [企业微信后台配置步骤](references/企业微信后台配置步骤.md) <br>
- [企业微信存档服务合规要求](references/合规要求.md) <br>
- [Cloudflare Tunnel 完整配置文档](references/Cloudflare Tunnel完整配置文档.md) <br>
- [ClawHub release page](https://clawhub.ai/cyl2835/wework-archive-service) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, configuration JSON, Python scripts, and SQL assets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment and configuration guidance for a local service that handles Enterprise WeChat callbacks and archived message data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
