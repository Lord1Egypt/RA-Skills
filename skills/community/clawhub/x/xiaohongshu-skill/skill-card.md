## Description: <br>
Xiaohongshu Skill is an agent toolkit for searching Xiaohongshu posts, reading post and profile details, browsing recommendation feeds, publishing posts, managing comments, likes and collections, generating writing templates, tracking strategy, and running SOP workflows. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[deliciousbuding](https://clawhub.ai/user/deliciousbuding) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to automate Xiaohongshu research, content drafting, publishing preparation, account interaction, and operating workflows through a Python Playwright CLI. It is best handled with explicit user approval for account-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a saved Xiaohongshu account session to publish, comment, reply, like, collect, and run engagement SOPs. <br>
Mitigation: Require explicit manual approval before any account-changing command and review the target content or post before execution. <br>
Risk: Saved login cookies, QR codes, and local session data can expose account access. <br>
Mitigation: Treat ~/.xiaohongshu and generated QR code files as credential material; do not share them and restrict local filesystem access. <br>
Risk: The artifact includes anti-detection and login-gate bypass behavior that may create platform terms or account-enforcement risk. <br>
Mitigation: Use only with an account the user is willing to risk, keep rate limits enabled, and stop if verification, captcha, or enforcement prompts appear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/deliciousbuding/xiaohongshu-skill) <br>
- [CLI Command Reference](docs/API.md) <br>
- [English README](README_EN.md) <br>
- [AgentSkills Specification](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime CLI commands output JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and Playwright; account-changing actions should require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.4.0 (source: ClawHub release metadata; artifact pyproject.toml reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
