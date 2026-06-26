## Description: <br>
WordPal is a personalized English vocabulary learning assistant that selects words from recent memory context, runs varied practice questions, reports progress, schedules FSRS-based review, and can register optional study reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lymon-srad](https://clawhub.ai/user/lymon-srad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use WordPal inside an agent chat to set an English-learning goal, practice new and due vocabulary, receive hints and feedback, and view progress reports. The skill is aimed at learners who want personalized word selection from recent memory summaries and local progress tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WordPal personalizes vocabulary from recent OpenClaw memory summaries, which may reflect sensitive user context. <br>
Mitigation: Use it only when memory-based personalization is appropriate, and avoid adding sensitive details to learning goals or study prompts. <br>
Risk: The skill stores vocabulary progress and learning profile data in a local database. <br>
Mitigation: Keep the workspace on a trusted device or directory and review local data handling expectations before use. <br>
Risk: Study reminders are registered when the user chooses push times. <br>
Mitigation: Enable reminders only after the user explicitly opts in, and review the scheduled times before registering them. <br>


## Reference(s): <br>
- [WordPal ClawHub page](https://clawhub.ai/lymon-srad/wordpal) <br>
- [Learn workflow](references/learn.md) <br>
- [Onboarding workflow](references/onboarding.md) <br>
- [Report workflow](references/report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style Chinese learning prompts and reports with inline shell commands and JSON-backed script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Node.js scripts, a local SQLite vocabulary database, recent OpenClaw memory summaries, and optional cron reminder registrations.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
