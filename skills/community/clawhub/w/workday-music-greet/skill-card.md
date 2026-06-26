## Description: <br>
Auto-switch music scenes by workday schedule and send matching GIF greeting emails, combining home-music scene control with IMAP/SMTP email for a full morning-to-evening ambient workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and workspace operators use this skill to schedule weekday music scene changes and send matching GIF greeting emails from a configured SMTP account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled automation can continue running local music commands and email sends after setup. <br>
Mitigation: Review scripts/config.json before registration and track any cron jobs you add so they can be removed later. <br>
Risk: SMTP credentials and recipient settings can expose an email account or send greetings to the wrong address. <br>
Mitigation: Use an app-specific SMTP password, keep .env private and out of source control, and verify GREET_TO and SMTP_FROM before running the skill. <br>


## Reference(s): <br>
- [Workday Music & Greet on ClawHub](https://clawhub.ai/terrycarter1985/workday-music-greet) <br>
- [Publisher profile](https://clawhub.ai/user/terrycarter1985) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local cron setup commands and usage guidance for Node scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
