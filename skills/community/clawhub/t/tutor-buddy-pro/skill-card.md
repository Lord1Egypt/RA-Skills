## Description:

Tutor Buddy Pro helps students work through homework with Socratic, step-by-step tutoring, personalized study plans, adaptive quizzes, and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Students, parents, and education-focused agent users use this skill for homework tutoring, study planning, adaptive quizzes, and progress tracking across core school subjects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Learner profile, quiz history, session log, and study plan files may contain sensitive student data.

Mitigation: Use a private local workspace, keep restrictive file permissions, and avoid collecting personal information beyond what is needed for tutoring.

Risk: Rerunning setup can overwrite or reset existing learner progress files.

Mitigation: Back up existing data files and confirm the target workspace before initializing learner profile, quiz history, session log, or study plan files.

Risk: The setup prompt includes recursive permission changes based on path discovery that may mis-handle multiple or empty matches.

Mitigation: Resolve a single skill directory deterministically, validate it exists, and avoid broad recursive chmod commands on ambiguous paths.

Risk: Dashboard sync would move learner data from local JSON files to a web service if implemented or enabled.

Mitigation: Keep sync disabled unless the user intentionally opts in and the deployment uses authentication, transport security, schema validation, and data minimization.

Risk: Product-promotion text could be inappropriate or unclear in a student-facing tutoring flow.

Mitigation: Remove promotions or clearly disclose them before using the skill with students or children.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/tutor-buddy-pro)
- [README](README.md)
- [Setup instructions](SETUP-PROMPT.md)
- [Security policy](SECURITY.md)
- [Security audit](CODEX-SECURITY-AUDIT.md)
- [Tutor configuration](config/tutor-config.json)
- [Dashboard companion spec](dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tutoring responses with JSON data schemas, configuration examples, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learner profile, quiz history, session log, study plan, and progress report files when the user directs the agent to do so.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
