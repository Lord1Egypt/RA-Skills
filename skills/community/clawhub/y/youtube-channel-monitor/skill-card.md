## Description: <br>
Monitors subscribed YouTube channels, extracts available subtitles, creates Chinese summaries, publishes them to Telegraph, and sends Telegram notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subwukong](https://clawhub.ai/user/subwukong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to automate monitoring of selected YouTube channels, turn new video transcripts into readable Chinese summaries, and publish updates through Telegraph and Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic publishing can send generated summaries to external Telegraph and Telegram destinations. <br>
Mitigation: Review the script, destination channel, and publishing behavior before installing or scheduling it. <br>
Risk: The security evidence reports an embedded Telegram bot token and fixed destination. <br>
Mitigation: Replace embedded credentials and channel identifiers with user-controlled configuration before running the script. <br>
Risk: Hourly cron execution can repeatedly access YouTube and publish updates without manual review. <br>
Mitigation: Test manually first and enable the cron job only after confirming channels, proxy settings, and notification destinations. <br>


## Reference(s): <br>
- [Cron setup reference](references/cron.md) <br>
- [ClawHub skill page](https://clawhub.ai/subwukong/youtube-channel-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled script emits text status and published article links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish externally to Telegraph and Telegram when configured and run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
