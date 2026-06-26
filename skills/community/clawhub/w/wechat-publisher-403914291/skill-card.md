## Description: <br>
Automatically collects AI news, formats it as WeChat-ready HTML, and creates drafts in a WeChat official account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[403914291](https://clawhub.ai/user/403914291) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and WeChat official-account operators use this skill to automate daily AI-news draft creation, with configurable WeChat credentials, schedule, template, and draft-publishing settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat official-account AppSecrets and access tokens can grant draft-creation access. <br>
Mitigation: Use environment variables or a protected secret store, avoid screenshots or command history that expose secrets, and rotate credentials if they are copied into local files or logs. <br>
Risk: Scheduled publishing can create drafts against the wrong or a sensitive official account. <br>
Mitigation: Test first on a non-critical account, confirm the AppID and IP whitelist, and review generated drafts before enabling unattended scheduling. <br>
Risk: Artifact documentation includes sample AppSecrets and unsafe secret-handling examples. <br>
Mitigation: Treat the examples as placeholders only, replace them with non-secret dummy values in operational docs, and never hardcode real AppSecrets in scripts or shared configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/403914291/wechat-publisher-403914291) <br>
- [Publisher Profile](https://clawhub.ai/user/403914291) <br>
- [User Guide](artifact/docs/user-guide.md) <br>
- [Install Guide](artifact/docs/install-guide.md) <br>
- [Publish Rules](artifact/docs/publish-rules.md) <br>
- [Block Layout](artifact/docs/block-layout.md) <br>
- [Troubleshooting](artifact/docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and WeChat-ready HTML draft content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates WeChat drafts through the WeChat official-account API and writes local status and result files when the publishing script runs.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
