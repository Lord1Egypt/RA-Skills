## Description:

TCM Clinic helps solo Traditional Chinese Medicine practitioners manage patient records, medical charts, herbal inventory, appointments, and financial bookkeeping in local Excel files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slamw](https://clawhub.ai/user/slamw)

### License/Terms of Use:

MIT-0

## Use Case:

External solo Traditional Chinese Medicine practitioners use this skill to manage daily clinic records, appointment queues, herbal inventory, and fee summaries through agent-guided CLI operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive patient, medical, and payment records in ordinary local Excel files.

Mitigation: Use a private, access-controlled, backed-up location and avoid shared or synced folders.

Risk: Terminal output can expose patient, medical, inventory, appointment, or financial details.

Mitigation: Treat terminal output as sensitive and restrict access to logs, transcripts, and shared screens.

Risk: Production PHI use requires controls beyond the artifact's local file workflow.

Mitigation: Add appropriate privacy, security, retention, and compliance controls before using it for production PHI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/slamw/skills/tcm-clinic)
- [Data schema reference](references/data-schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown summaries with shell command execution and local Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local .xlsx files under clinic_data/; command output may include patient, medical, inventory, appointment, and financial records.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
