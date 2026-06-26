## Description: <br>
Monitors a detached WeChat Mac window via OCR and automatically replies using a customizable AI persona with safety locks to prevent interference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarryxin](https://clawhub.ai/user/jarryxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced end users run this skill on a trusted macOS machine to monitor selected WeChat contacts through screenshots/OCR, generate AI replies, and send those replies through UI automation. It is intended for local, user-controlled operation where the operator can manage chat privacy, API keys, and messaging behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private chat content, screenshots, and history can be exposed through the dashboard or stored local files. <br>
Mitigation: Run only on a trusted Mac, bind the dashboard to localhost or add authentication, avoid sensitive chats, and clear screenshots and history regularly. <br>
Risk: The skill can send real WeChat messages automatically without per-message confirmation. <br>
Mitigation: Use a narrow contact list, review persona settings before starting, supervise early runs, and stop the daemon when unattended sending is not acceptable. <br>
Risk: API keys and model access are required for screenshot analysis and reply generation. <br>
Mitigation: Use a limited API key, avoid sharing the dashboard over the network, and rotate the key if dashboard access or local files may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jarryxin/wechat-auto-reply-ai) <br>
- [Publisher profile](https://clawhub.ai/user/jarryxin) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local setup steps, contact targets, dashboard controls, persona settings, and safety guidance for supervised operation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
