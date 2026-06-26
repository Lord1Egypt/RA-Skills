## Description: <br>
Use when a user wants social media scheduling and publishing for AI agents on X, LinkedIn, Instagram, Facebook Pages, TikTok, Discord, Telegram, YouTube, Reddit, WordPress, and Pinterest through SocialClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndesv21](https://clawhub.ai/user/ndesv21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a SocialClaw workspace: connect social accounts, upload media, validate or preview schedules, apply campaigns, and inspect publishing status or analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real posting and scheduling actions across connected social accounts. <br>
Mitigation: Review target accounts, media, post content, timing, and campaign changes before running apply or publish commands. <br>
Risk: Workspace API keys, bot tokens, and webhook URLs may grant access to publishing surfaces. <br>
Mitigation: Use dedicated or least-privilege credentials where possible, avoid echoing secrets into chat or logs, and rotate credentials if exposed. <br>
Risk: The optional CLI can store credentials locally and install an agent command. <br>
Mitigation: Install and use the CLI only in trusted environments, and confirm local credential storage is acceptable before login. <br>


## Reference(s): <br>
- [SocialClaw homepage](https://getsocialclaw.com) <br>
- [ClawHub skill page](https://clawhub.ai/ndesv21/socialclaw) <br>
- [SocialClaw CLI](references/cli.md) <br>
- [SocialClaw Provider Notes](references/providers.md) <br>
- [SocialClaw Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands or request bodies that act on connected social accounts after user review.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
