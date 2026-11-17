## Description:

A project memory that tracks status, milestones, owners, and blockers so nothing stalls silently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Agents managing ongoing work use this skill to open, update, recall, and summarize active project records, including owners, milestones, blockers, and outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send and store confidential project, roadmap, customer, personnel, security, or business details in an external BlueColumn/Supabase service.

Mitigation: Use only with an approved BlueColumn account, obtain user or organization consent before sending project details, and redact sensitive owner, blocker, milestone, and risk information unless external storage is explicitly allowed.

Risk: Broad automatic-use instructions can cause project information to be recalled or updated before a user has reviewed what will be shared.

Mitigation: Confirm the intended project scope before recall or update calls and review payloads before execution.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/remember-projects)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends project records to an external BlueColumn/Supabase service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
