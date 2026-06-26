## Description: <br>
Manages vitamin and supplement reminders across configurable daily time slots by syncing OpenClaw cron jobs from a workspace VITAMINS.md schedule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdmichaelb](https://clawhub.ai/user/cdmichaelb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain a personal supplement schedule and create or refresh reminder cron jobs that post to a configured OpenClaw channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The update script removes matching vitamin reminder cron jobs before recreating them. <br>
Mitigation: Review existing OpenClaw cron jobs with vitamin reminder names and run the script only when replacement is intended. <br>
Risk: Reminder delivery depends on the configured channel ID and timezone. <br>
Mitigation: Confirm VITAMIN_CHANNEL_ID and VITAMIN_TIMEZONE before creating or refreshing the schedule. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cdmichaelb/vitamin-tracker-channel) <br>
- [README](artifact/README.md) <br>
- [Update script](artifact/scripts/update_vitamin_crons.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates OpenClaw cron job definitions from a user-maintained VITAMINS.md schedule; does not write data files.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
