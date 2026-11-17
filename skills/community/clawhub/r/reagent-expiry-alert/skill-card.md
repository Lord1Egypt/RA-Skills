## Description:

Scan reagent barcodes or IDs, log expiration dates, and generate multi-level alerts before reagent expiry to support laboratory inventory management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Laboratory staff, inventory managers, and agents supporting lab operations use this skill to log reagent IDs with expiration dates, check alert windows, and produce expiry status and reorder guidance for ordinary non-regulated inventory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inventory details are persisted locally in plaintext at ~/.openclaw/reagent_inventory.json.

Mitigation: Use the skill only on appropriate accounts and avoid storing sensitive or regulated inventory details in the local file.

Risk: Expired-item output may display overdue items incorrectly until the known overdue display bug is fixed.

Mitigation: Manually verify expired-item reports against the stored expiration dates before acting on disposal or reorder decisions.

Risk: The skill is not intended for controlled substances, biological hazards requiring special disposal, or regulated chain-of-custody inventory.

Mitigation: Use it only for ordinary non-regulated reagent expiry tracking and route regulated inventory through approved lab systems.

Risk: Local inventory records may be operationally important but are stored outside a managed database.

Mitigation: Keep backups when the inventory matters for operations and review file access controls on shared systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/reagent-expiry-alert)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and structured alert reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local inventory data to ~/.openclaw/reagent_inventory.json when the packaged CLI is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
