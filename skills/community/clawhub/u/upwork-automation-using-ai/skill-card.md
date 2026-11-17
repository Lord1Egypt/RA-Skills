## Description:

Automate Upwork login, search, filter, and proposal drafting in one browser session, stopping before submission unless explicitly instructed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adeel-powerhouse](https://clawhub.ai/user/adeel-powerhouse)

### License/Terms of Use:


## Use Case:

Freelancers and agencies use this skill to keep one active Upwork browser session, find jobs matching explicit criteria, filter disqualifiers, and draft proposal fields for human review before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent operates an active Upwork browser session and could affect a real user account.

Mitigation: Keep the session visible to the user, verify page state before risky clicks, and stop before submission unless the user explicitly says to submit now.

Risk: Proposal text or job choice may be inaccurate, misleading, or mismatched to the user's intent.

Mitigation: Have the user review the selected job, rationale, and completed proposal fields before any submission decision.

Risk: Credentials may be exposed if reused outside the active login flow.

Mitigation: Accept credentials only when explicitly provided for the current run, do not echo passwords, and do not persist credentials in files or notes.

## Reference(s):

- [Proposal Template](references/proposal-template.md)
- [Session Checklist](references/session-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status summary and proposal-field guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports selected job, selection rationale, fields filled, submission status, and the next user action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
