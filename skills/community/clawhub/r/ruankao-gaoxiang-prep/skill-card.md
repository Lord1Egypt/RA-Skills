## Description:

Ruankao Gaoxiang Prep helps users prepare for the advanced Information System Project Manager exam by generating daily chapter review points, English vocabulary, exam questions, and on-demand study lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artwebs](https://clawhub.ai/user/artwebs)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and exam candidates use this skill to schedule recurring Ruankao Gaoxiang study reminders and request chapter highlights, English terms, terminology, and practice questions on demand.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent QQ delivery jobs for daily study reminders.

Mitigation: Create the job only after explicit user intent, verify the QQ recipient and schedule first, and check the cron list afterward so unwanted jobs can be deleted.

Risk: A README cron command contains a fixed QQ recipient value.

Mitigation: Prefer the setup script because it prompts for the user's openid, or replace the README recipient with the intended openid before creating the job.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/artwebs/skills/ruankao-gaoxiang-prep)
- [README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)
- [Study plan](artifact/study-plan.md)
- [Terminology reference](artifact/references/terminology.md)
- [English words reference](artifact/references/english-words.md)
- [Exam questions reference](artifact/references/exam-questions.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown study responses, JSON daily-push payloads, and inline shell or cron configuration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or describe recurring QQ bot delivery jobs when the user requests daily push reminders.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
