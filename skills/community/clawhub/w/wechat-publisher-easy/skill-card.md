## Description: <br>
Automatically collects AI news, formats it as WeChat-ready HTML, and creates WeChat public account drafts with scheduling, deduplication, and publishing status output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[403914291](https://clawhub.ai/user/403914291) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to prepare scheduled AI news posts for a WeChat public account draft box. It helps configure account credentials, generate HTML article content, call the WeChat draft API, and report draft IDs for review before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires powerful WeChat public account credentials and the security evidence flags unsafe AppSecret storage and display patterns. <br>
Mitigation: Use a dedicated low-risk WeChat account where possible, prefer environment variables or a secret manager over CLI arguments and config files, restrict local file permissions, and rotate any exposed AppSecret. <br>
Risk: The skill caches access tokens and writes local memory, status, result, and log files during publishing. <br>
Mitigation: Clear token cache and local memory files when uninstalling, changing credentials, or moving the skill between machines. <br>
Risk: The skill can create drafts on a WeChat public account, so incorrect configuration or unreviewed generated news content may affect a real publishing workflow. <br>
Mitigation: Run tests on a low-risk account first, verify IP whitelist and account permissions, and review generated drafts in WeChat before publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/403914291/wechat-publisher-easy) <br>
- [User guide](artifact/docs/user_guide.md) <br>
- [Install guide](artifact/docs/install-guide.md) <br>
- [Publishing rules](artifact/docs/publish-rules.md) <br>
- [WeChat public platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, HTML article templates, and WeChat draft status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces WeChat draft IDs, local status JSON, logs, cached token data, and generated article/result files when executed.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
