## Description: <br>
拾遗 is a general exam-prep tracking skill that records wrong-question screenshots or text, classifies them with reusable tags, schedules review reminders, and exports an Excel error notebook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KaguraNanaga](https://clawhub.ai/user/KaguraNanaga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners preparing for exams use this skill to turn screenshots and short text notes into organized wrong-question records, review prompts, and filtered Excel exports. It supports general exam workflows across standardized tests, school exams, and professional qualification exams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exam screenshots and extracted study details may contain personal or sensitive information and are stored locally, backed up, reused in prompts, and included in reminders or exports. <br>
Mitigation: Avoid submitting screenshots with personal information, review local data retention expectations before use, and limit exports or reminders to contexts where that study data is appropriate to share. <br>
Risk: Export filenames and spreadsheet output can be influenced by user-provided filter text. <br>
Mitigation: Sanitize export filters and filenames before broad use, and keep generated exports constrained to the intended local export directory. <br>
Risk: Scheduled cron jobs can proactively send study summaries and review prompts through Feishu. <br>
Mitigation: Enable scheduled jobs only when proactive reminders are desired and the configured channel is acceptable for the study data being sent. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/KaguraNanaga/shiyi-study-tracker) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, configuration, shell commands, guidance] <br>
**Output Format:** [Conversational text, JSON-backed local records, scheduled reminder messages, and Excel exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local study records, screenshot-derived details, Feishu reminder text, and .xlsx attachments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; package.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
