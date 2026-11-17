## Description:

Helps agents use the Seongnam Library CLI to search books, check account and loan details, and prepare interlibrary loan or book requests for submission after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruseel](https://clawhub.ai/user/ruseel)

### License/Terms of Use:

MIT-0

## Use Case:

Library patrons and their agents can search Seongnam Library holdings, check loans and reservations, and prepare interlibrary loan or book purchase requests for explicit approval before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and executes a native binary.

Mitigation: Use the pinned release and verify its SHA-256 checksum before execution.

Risk: Login and account information can be exposed through files or logs.

Mitigation: Keep login JSON in a private file, protect locally stored sessions, and avoid shared logs for account output.

Risk: Submitting a library request may have unintended or duplicate effects.

Mitigation: Review the prepared payload and obtain explicit user confirmation before submitting; check request status before retrying after an error.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ruseel/skills/snlib-cli)
- [Command patterns](references/commands.md)
- [Library codes](references/lib-code.md)
- [Management codes](references/manage-code.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with shell examples and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results include an outcome and code; request submissions require user confirmation.]

## Skill Version(s):

2026.9.30-rc3 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
