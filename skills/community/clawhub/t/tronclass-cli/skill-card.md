## Description:

This skill helps an agent use the tronclass CLI to check TronClass courses, assignments, deadlines, grades, announcements, course materials, downloads, and homework submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujun-bo2](https://clawhub.ai/user/yujun-bo2)

### License/Terms of Use:

MIT

## Use Case:

Students and authorized TronClass users use this skill to let an agent inspect LMS course information, retrieve materials, track due work, and prepare or submit homework through the tronclass CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to use real TronClass sessions and account data.

Mitigation: Use it only with TronClass or FJU accounts the agent is intended to access, and confirm session status before acting on account data.

Risk: Passwords can be exposed if supplied in chat or command-line arguments.

Mitigation: Prefer interactive login where possible, avoid sharing passwords in chat, and use the deferred CAPTCHA flow so passwords are supplied only at the resume step.

Risk: Downloads or homework submissions may target the wrong course, activity, or local file path.

Mitigation: Verify course IDs, activity IDs, and file paths before downloads or submissions; inspect homework details and use draft mode before final submission when appropriate.

Risk: Installing the underlying tronclass-cli package introduces package supply-chain risk.

Mitigation: Pin or independently review the tronclass-cli package version before installation.

## Reference(s):

- [TronClass CLI skill homepage](https://github.com/YuJun-BO2/tronclass-cli-skill)
- [TronClass CLI tool repository](https://github.com/YuJun-BO2/tronclass-cli-ts)
- [ClawHub skill page](https://clawhub.ai/yujun-bo2/skills/tronclass-cli)
- [TronClass](https://tronclass.com/)
- [Auth command reference](references/auth.md)
- [Todo command reference](references/todo.md)
- [Courses command reference](references/courses.md)
- [Activities command reference](references/activities.md)
- [Homework command reference](references/homework.md)
- [Announcements command reference](references/announcements.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and terminal-output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to download files or submit user-provided files when the user authorizes those CLI actions.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
