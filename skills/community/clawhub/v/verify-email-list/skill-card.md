## Description:

Verifies email addresses through Cargo to help reduce bounces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, sales development, and revenue operations teams use the skill to check contact email lists before a campaign and decide which addresses may need to be excluded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact lists may contain personal data shared with Cargo and its verification providers.

Mitigation: Use only lists you are authorized to share, including the initial sample.

Risk: Batch verification costs increase with the number of records processed.

Mitigation: Start with a 10–20 address sample, report the observed cost and estimated full-run cost, and get approval before processing the full list.

Risk: The review covers the supplied instructions, not the external CLI implementation or future upstream changes.

Mitigation: Use reviewed package versions and assess the CLI and broader skill collection separately.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown summary and per-address status table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status and reason for each checked email address.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
