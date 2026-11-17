## Description:

Tracks email threads, promised actions, and follow-ups so agents managing correspondence can recall commitments and deadlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help agents managing email correspondence log commitments, recall overdue or due-soon follow-ups, and draft replies with thread context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email-thread summaries may include confidential, regulated, or personal information that is sent to and persisted by an external BlueColumn/Supabase service.

Mitigation: Use only for approved correspondence; exclude customer, legal, HR, financial, regulated, or confidential content unless retention, deletion, access controls, and data-processing terms are approved.

Risk: The skill requires a live BlueColumn API key for all operations.

Mitigation: Store BLUECOLUMN_API_KEY in approved secret management, scope access to authorized agents, and rotate or remove it if exposure is suspected.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/remember-emails)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown guidance with inline bash code blocks and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLUECOLUMN_API_KEY and sends email-thread summaries to BlueColumn/Supabase endpoints.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
