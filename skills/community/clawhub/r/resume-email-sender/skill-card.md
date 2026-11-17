## Description:

Send resume and cover letter to companies via Gmail. Activate when user wants to send, deliver, or submit a resume by email, apply to a job, or email a company about a position. Uses gog Gmail tool to compose and send professional job application emails with resume attached.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxty](https://clawhub.ai/user/xiaoxty)

### License/Terms of Use:

MIT-0

## Use Case:

Job applicants and agents assisting them use this skill to draft, preview, personalize, send, and log professional job application emails through Gmail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send email from the user's Gmail account.

Mitigation: Require explicit user review and confirmation of recipient, subject, sender account, and email body before sending.

Risk: The skill may state that a resume is attached when it is not actually attached.

Mitigation: Correct the email wording or add a real attachment workflow before using it for applications.

Risk: The skill handles resume text through unsafe temporary-file and shell-command patterns.

Mitigation: Use safer temporary-file handling and quote or escape shell inputs before execution.

Risk: The Gmail integration depends on the gog tool and account permissions.

Mitigation: Verify the gog installation source and Gmail authorization scope before installing or running the skill.

## Reference(s):

- [Skill source](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/xiaoxty/skills/resume-email-sender)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with email previews and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Gmail send or draft commands and job application log entries after user confirmation.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
