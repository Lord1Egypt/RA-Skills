## Description: <br>
Automate X/Twitter brand account operations using OpenClaw native tools, xurl, browser fallback, and cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoqi](https://clawhub.ai/user/caoqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External brand operators and social media teams use this skill to configure scheduled X/Twitter posting, keyword engagement, weekly reporting, Telegram alerts, and Substack draft generation for a brand account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make unattended public X/Twitter posts, replies, likes, and follows. <br>
Mitigation: Require review before public posts or replies, use a dedicated xurl app and browser profile, and set strict per-run limits for likes, follows, and replies. <br>
Risk: Browser fallback may operate the wrong account if the active browser profile is not scoped to the intended brand. <br>
Mitigation: Verify the active account before enabling browser fallback and keep cron jobs visible, time-limited, and easy to disable. <br>
Risk: Telegram summaries or drafts may be sent to an unintended recipient. <br>
Mitigation: Confirm Telegram recipient IDs before enabling alerts or scheduled reports. <br>


## Reference(s): <br>
- [Content Strategy](references/content-strategy.md) <br>
- [Cron Job Configuration](references/cron-config.md) <br>
- [Engagement Playbook](references/engagement-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and cron configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose public social actions and recurring schedules that should be reviewed before activation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
