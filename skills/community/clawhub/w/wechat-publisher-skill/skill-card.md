## Description: <br>
Automatically collects AI news, generates HTML content, and creates draft posts in WeChat official accounts with configurable templates and scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[403914291](https://clawhub.ai/user/403914291) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators of WeChat official accounts use this skill to prepare recurring AI news drafts, manage template-based HTML layouts, and schedule publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat AppSecrets and access tokens can expose a high-impact publishing integration if stored in plaintext, command histories, logs, or screenshots. <br>
Mitigation: Use environment variables or protected config files, avoid command-line secret flags and shared terminals, restrict local file permissions, and rotate any exposed secret. <br>
Risk: Scheduled or unattended runs may create drafts without the account operator's intended approval. <br>
Mitigation: Test with a low-risk account first, review scheduled-job settings, and confirm draft creation is expected before relying on automation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/403914291/wechat-publisher-skill) <br>
- [User guide](artifact/docs/user-guide.md) <br>
- [Install guide](artifact/docs/install-guide.md) <br>
- [Publishing rules](artifact/docs/publish-rules.md) <br>
- [Template documentation](artifact/docs/templates.md) <br>
- [Troubleshooting guide](artifact/docs/troubleshooting.md) <br>
- [WeChat Official Accounts platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, Python behavior, and generated WeChat HTML draft content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call WeChat APIs, read local configuration, cache tokens and status in local memory files, and create drafts in a configured official account.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
