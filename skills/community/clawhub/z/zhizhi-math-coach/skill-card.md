## Description: <br>
Primary-school math coaching skill created to help my first-grade daughter Zhizhi: grade worksheet photos or wrong questions, track weak points and learning progress, explain concepts for parents and students, and generate printable PDF/HTML practice aligned with grade, semester, textbook, exam, and holiday plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linzi007](https://clawhub.ai/user/linzi007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents and tutors use this skill to grade primary-school math work, diagnose weak points, explain concepts, track progress, and generate printable practice for a child. It can also help manage local learning records, optional GitHub sync, public worksheet publishing, and scheduled reminders when the user enables those features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage a child's learning records through GitHub sync, public worksheet links, SSH deploy keys, and scheduled reminders. <br>
Mitigation: Install only for a local-first math coaching workspace, review `.zhizhi-math-coach/config.json`, and enable cloud sync, Pages, deploy keys, or cron settings only when the repository privacy and exposure are acceptable. <br>
Risk: Public publishing can expose worksheet metadata or learning files if the user configures a public repository or Pages workflow too broadly. <br>
Mitigation: Publish only child-facing worksheet HTML/PDF files and keep answer keys, diagnosis records, memories, weak-point histories, student photos, and textbook files out of public output. <br>
Risk: Automatic pull, commit, push, publish, or reminder registration can change local or remote learning-workspace state after configuration is enabled. <br>
Mitigation: Treat `.zhizhi-math-coach/config.json` as the consent boundary, verify auto-pull, auto-commit, auto-push, auto-publish, and cron settings before use, and keep automation limited to reminders unless explicit record writes or worksheet generation are requested. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linzi007/skills/zhizhi-math-coach) <br>
- [Daily Grading Workflow](references/daily-grading-workflow.md) <br>
- [Grading And Diagnosis Rubric](references/grading-diagnosis-rubric.md) <br>
- [Worksheet Generation](references/worksheet-generation.md) <br>
- [Worksheet Standards](references/worksheet-standards.md) <br>
- [Curriculum Alignment](references/curriculum-alignment.md) <br>
- [GitHub Sync Authorization](references/github-sync-authorization.md) <br>
- [GitHub Pages Publishing](references/github-pages-publishing.md) <br>
- [OpenClaw Automation](references/automation-openclaw.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON worksheet specs, local files, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local learning records, worksheet HTML/PDF files, answer keys, configuration files, GitHub sync state, Pages output, and scheduled reminder settings when enabled by the user.] <br>

## Skill Version(s): <br>
0.2.14 (source: server release evidence, created 2026-06-29T05:36:17Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
