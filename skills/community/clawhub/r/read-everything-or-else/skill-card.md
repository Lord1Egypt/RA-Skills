## Description:

Creates a manifest and quote-checked audit trail to help an agent track exhaustive reading and report coverage gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT-0

## Use Case:

For users who ask an agent to review a whole repository, document set, or other defined collection. The agent tracks items in a manifest and quote-checked ledger, then reports uncovered material before claiming completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning a broad target can include files beyond the intended review scope.

Mitigation: Limit targets to the files the user intends to review, then inspect the generated manifest and exclusions.

Risk: A passing coverage audit and matching excerpts do not by themselves establish that an agent interpreted material correctly; the supplied security review also notes partial scan coverage.

Mitigation: Review conclusions against the source material and account for uncovered or unsupported file types before relying on a completion claim.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/catsmansion/skills/read-everything-or-else)

## Skill Output:

**Output Type(s):** [Markdown, Text files, Shell commands, Guidance]

**Output Format:** [Markdown guidance and commands, with TSV manifests and ledgers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tracks coverage using source excerpts and reports gaps for review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
