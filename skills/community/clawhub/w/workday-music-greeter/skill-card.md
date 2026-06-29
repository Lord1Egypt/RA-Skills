## Description: <br>
On weekdays, this skill switches the current home-music scene, fetches a matching GIF, and sends a themed greeting email with optional weekday cron scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and home automation operators use this skill to automate weekday music scene changes and send scene-matched greeting emails. It is useful when a recurring workday routine should coordinate music, GIF selection, and email notification from one agent skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the cron helper can create recurring weekday actions that send email and change music without further prompts. <br>
Mitigation: Inspect the fixed schedule, confirm the recipient and SMTP credentials, and test run.sh with --dry-run before running install-cron.sh. <br>
Risk: Missing or incorrect dependencies and credentials can prevent music switching, GIF retrieval, or email delivery. <br>
Mitigation: Verify bash, node, WMG_MAIL_TO, SMTP settings, and optional home-music, gifgrep, and imap-smtp-email integrations before relying on the automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/workday-music-greeter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Bash/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead to external side effects when run or scheduled, including weekday cron entries, music scene changes, GIF lookup, and greeting email delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
