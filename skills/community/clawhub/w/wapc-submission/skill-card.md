## Description:

Automate WAPC award submissions on mulandxc.com when you need to collect real LoTW-confirmed evidence, fill the WAPC table, upload screenshots, save applicant info, and complete the final browser-based submission flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muningwang](https://clawhub.ai/user/muningwang)

### License/Terms of Use:

MIT-0

## Use Case:

External award applicants and supporting agents use this skill to prepare Mulan DX Club WAPC submissions with LoTW-confirmed QSOs, uploaded screenshots, saved row data, applicant information, and final browser submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has a hard-coded live WAPC application ID for remote updates and personal-data submission, which can update the wrong application record.

Mitigation: Confirm the authenticated account owns the target WAPC application and replace or verify application ID 806 from the live page before any update.

Risk: The workflow uploads evidence images and submits personal contact details.

Mitigation: Explicitly approve all LoTW evidence images and applicant contact details before upload or final submission.

## Reference(s):

- [WAPC Workflow Reference](references/workflow.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with commands, field names, API endpoints, and workflow checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before browser actions, evidence uploads, personal-data submission, or final award submission.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
