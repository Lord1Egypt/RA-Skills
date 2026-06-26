## Description: <br>
Automates Xiaohongshu account workflows for login, publishing, search and discovery, social interactions, and multi-step content operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Angiin](https://clawhub.ai/user/Angiin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a logged-in Xiaohongshu browser session for content publishing, search, account checks, interaction management, and content operations. Public posting and commenting workflows should be reviewed by the user before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a logged-in Xiaohongshu browser session and can publish, comment, like, favorite, and manage account state. <br>
Mitigation: Use staged flows for posting and commenting; manually verify the selected account, content, and target before approving any public action. <br>
Risk: QR-login handling sends login QR material to a third-party QR service. <br>
Mitigation: Review the QR-login path before use and avoid it where sharing login QR material with a third-party service is unacceptable. <br>
Risk: The release includes anti-detection automation behavior that may conflict with platform rules or account safety expectations. <br>
Mitigation: Avoid stealth features where platform compliance or account safety matters, and operate within platform rules and rate limits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Angiin/xiaohongshu-skills) <br>
- [Project Homepage](https://github.com/xpzouying/xiaohongshu-skills) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>
- [OpenClaw](https://github.com/anthropics/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may describe or trigger browser-session actions, including account checks, search results, drafts, posts, comments, likes, and favorites.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
