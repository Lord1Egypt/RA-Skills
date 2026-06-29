## Description: <br>
Automates daily remote job search, matching, and email reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aliceyuruchan](https://clawhub.ai/user/aliceyuruchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search remote job listings, match opportunities against a user profile, verify links, and deliver results in the console or by email report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send outbound job-search reports using configured SMTP credentials. <br>
Mitigation: Confirm before the first outbound email and use a dedicated email account or app password where possible. <br>
Risk: Scheduled runs can continue sending recurring reports after setup. <br>
Mitigation: Review any cron, TRAE, or daily-run configuration and keep the schedule visible to the user. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aliceyuruchan/skills/remotejobhunter) <br>
- [Server-resolved GitHub source](https://github.com/aliceyuruchan/remotejobhunter) <br>
- [Gmail App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce console job-match summaries, setup guidance, configuration edits, and email-report instructions.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
