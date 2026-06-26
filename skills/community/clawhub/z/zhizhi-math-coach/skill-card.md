## Description: <br>
Primary-school math coaching skill that grades worksheet photos or wrong questions, tracks weak points and learning progress, explains concepts for parents and students, and generates printable PDF/HTML practice aligned with grade, semester, textbook, exam, and holiday plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linzi007](https://clawhub.ai/user/linzi007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, tutors, and learning agents use this skill to review primary-school math work, diagnose recurring weak points, maintain local learning records, and produce targeted printable practice. It also supports optional GitHub sync, public child-facing worksheet publishing, and scheduled reminder setup when the parent explicitly enables those features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional GitHub sync, Pages publishing, and scheduled reminders can change or expose student learning data if enabled without care. <br>
Mitigation: Leave these features disabled unless intentionally needed; before enabling sync or public links, confirm repository visibility, avoid committing student identifiers or answer keys, and know how to revoke the deploy key and remove cron jobs. <br>
Risk: Worksheet photo grading can be unreliable when handwriting, teacher marks, diagrams, or context are unclear. <br>
Mitigation: Grade only clear evidence, mark uncertain items as need-confirmation, and ask for a clearer photo or missing context before updating learning records. <br>
Risk: Scheduled automation could be mistaken for permission to write records or generate worksheets automatically. <br>
Mitigation: Use scheduled tasks for reminders and suggestions by default; allow record writes or automatic worksheet generation only when the parent explicitly enables those settings. <br>
Risk: Public worksheet publishing can accidentally reveal answers, diagnosis notes, or private learning history. <br>
Mitigation: Publish only child-facing HTML/PDF worksheet files and public-safe metadata; keep answer keys, diagnosis details, and sensitive learning records out of the public site. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linzi007/zhizhi-math-coach) <br>
- [OpenClaw Quickstart](references/openclaw-quickstart.md) <br>
- [Grading Diagnosis Rubric](references/grading-diagnosis-rubric.md) <br>
- [Worksheet Generation](references/worksheet-generation.md) <br>
- [GitHub Sync Authorization](references/github-sync-authorization.md) <br>
- [GitHub Pages Publishing](references/github-pages-publishing.md) <br>
- [OpenClaw Automation](references/automation-openclaw.md) <br>
- [Advanced GitHub Setup Guide](https://github.com/linzi007/zhizhi-math-coach-openclaw/blob/main/docs/github-advanced-setup.zh-CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance, JSON worksheet specs, HTML/PDF worksheet files, answer keys, shell commands, and local configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local learning records and worksheet artifacts; GitHub sync, Pages publishing, and scheduled reminders are optional and gated by explicit configuration.] <br>

## Skill Version(s): <br>
0.2.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
