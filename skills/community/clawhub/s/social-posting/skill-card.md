## Description: <br>
Multi-platform social media posting service with automatic provider failover for Twitter/X, LinkedIn, Instagram, Facebook, TikTok, Threads, Bluesky, YouTube, and Pinterest, including per-user credential management, OAuth flow, media upload, scheduling, and post history tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to help agents configure and use social posting workflows across multiple social platforms. It supports connecting user social accounts, uploading media, publishing immediately, scheduling posts, and reviewing post history through PostForMe or LATE. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent publish or schedule posts to external social platforms. <br>
Mitigation: Confirm the exact account, platforms, content, media, and schedule before each posting action. <br>
Risk: Provider credentials and global fallback credentials could be mis-scoped or used unintentionally. <br>
Mitigation: Use per-user credentials where possible, avoid global fallback credentials unless intentionally scoped and audited, and ensure credentials can be reviewed, revoked, and deleted. <br>
Risk: Post history and uploaded media can contain sensitive campaign or account information. <br>
Mitigation: Review storage, access control, retention, and deletion behavior for encrypted credentials, media references, and post history. <br>


## Reference(s): <br>
- [Canlah AI](https://canlah.ai) <br>
- [Social Posting on ClawHub](https://clawhub.ai/PHY041/social-posting) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples, environment variable names, database schema examples, and posting workflow guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
