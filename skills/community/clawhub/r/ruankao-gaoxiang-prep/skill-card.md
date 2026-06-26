## Description: <br>
Provides Ruankao advanced information systems project manager exam preparation with daily chapter highlights, English vocabulary, past exam questions, and on-demand study lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artwebs](https://clawhub.ai/user/artwebs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners and OpenClaw users use this skill to receive recurring Ruankao Gaoxiang study reminders through QQ and to query chapter summaries, vocabulary, terminology, and practice questions on demand. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent QQ scheduled agent messages from broad study-related triggers. <br>
Mitigation: Enable scheduled reminders only after explicit confirmation of the schedule and destination, and review existing OpenClaw cron jobs so the reminder can be removed. <br>
Risk: The skill handles QQ recipient openids and may expose them through temporary config files, logs, or screenshots. <br>
Mitigation: Verify the recipient openid before use and avoid storing configs in shared temporary locations or sharing logs and screenshots that contain the openid. <br>
Risk: One-time chapter or vocabulary lookup requests could unintentionally create a recurring reminder. <br>
Mitigation: For lookup-only use, do not create a scheduled job unless the user explicitly confirms a recurring reminder schedule and destination. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/artwebs/ruankao-gaoxiang-prep) <br>
- [README](artifact/README.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>
- [Study Plan](artifact/study-plan.md) <br>
- [Terminology Reference](artifact/references/terminology.md) <br>
- [English Vocabulary Reference](artifact/references/english-words.md) <br>
- [Exam Questions Reference](artifact/references/exam-questions.md) <br>
- [Ruankao Official Website](https://www.ruankao.org.cn/) <br>
- [Ruankao Gaoxiang Textbook Fourth Edition](https://item.jd.com/1000123456789.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown study responses, JSON daily-push payloads, and cron setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create a recurring OpenClaw cron job that delivers QQ bot messages to a configured recipient openid.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
