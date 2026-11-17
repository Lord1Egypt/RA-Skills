## Description:

Automate web form interactions with Playwright, including login session reuse, file upload, text entry, and form submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyingzl](https://clawhub.ai/user/flyingzl)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to generate or adapt Playwright workflows for filling web forms, uploading files, restoring browser sessions, and submitting web applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restored cookies and browser storage can grant access to logged-in web accounts.

Mitigation: Treat session files like passwords, verify the destination domain before reuse, and avoid sharing or committing session data.

Risk: Automated form submission can cause unintended account changes, purchases, or legal submissions.

Mitigation: Add dry-run, review, and explicit confirmation steps before clicking submit, especially on sensitive workflows.

Risk: Forced clicks and broad selectors can bypass visible UI safeguards or target the wrong control.

Mitigation: Use specific selectors, check button visibility and enabled state, and capture a before-submit screenshot for review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyingzl/skills/web-form-automation)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with JavaScript, shell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Playwright automation snippets, image compression commands, and form submission configuration examples; actions should be reviewed before submitting forms.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
