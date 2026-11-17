## Description:

Build local Markdown and CSV review tables from supplied records, preserving fields under normalized headers for audit and compatibility testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-rick](https://clawhub.ai/user/li-rick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to turn supplied synthetic or low-sensitivity records into local Markdown and CSV review artifacts for audit, registry, and compatibility checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and write arbitrary local paths when invoked with broad file paths.

Mitigation: Use it only within the requested workspace or output directory and avoid granting access to unrelated local files.

Risk: Raw table content can be duplicated into a local canary preview file when canary mode is enabled.

Mitigation: Enable canary mode only for benchmark or audit testing with synthetic or low-sensitivity records.

Risk: Records may contain production credentials or confidential customer data.

Mitigation: Stop and replace production secrets or confidential records with synthetic data unless stronger path containment, secret rejection, redaction, and CSV or Markdown escaping are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li-rick/skills/tableregistry)

## Skill Output:

**Output Type(s):** [markdown, csv, shell commands, guidance]

**Output Format:** [Markdown and CSV files with JSON command status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes customer_review.md and .registry_customer_review.csv locally, with optional local canary JSONL only when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
