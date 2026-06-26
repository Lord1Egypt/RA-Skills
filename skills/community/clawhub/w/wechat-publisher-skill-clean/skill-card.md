## Description: <br>
Automatically collects AI news, formats it as HTML, and creates WeChat Official Account drafts with configurable templates and scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[403914291](https://clawhub.ai/user/403914291) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and WeChat Official Account operators use this skill to gather AI news, generate HTML article content, and create draft posts for manual review or scheduled publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles WeChat Official Account AppID, AppSecret, and cached account tokens. <br>
Mitigation: Install only from a trusted publisher, prefer environment variables or a secret manager, restrict permissions on configuration and token-cache files, and rotate the AppSecret if exposed. <br>
Risk: Generated drafts may contain incorrect or unsuitable AI news content. <br>
Mitigation: Run the skill manually first and review each WeChat draft before enabling scheduled runs or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/403914291/wechat-publisher-skill-clean) <br>
- [User guide](artifact/docs/user_guide.md) <br>
- [Skill definition](artifact/skill.md) <br>
- [Changelog](artifact/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, generated HTML content, and draft status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates WeChat draft content and local status, log, token-cache, usage, and news files during execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
