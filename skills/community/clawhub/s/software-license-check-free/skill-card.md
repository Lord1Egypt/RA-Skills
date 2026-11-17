## Description:

A free deterministic check for software license and cloud resource ledgers, covering annual cost, monthly average, subscription term months, over-installation, duplicate rows, totals, blanks, and inverted dates with source-line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

IT asset managers and finance teams use this skill to check software license and cloud resource ledgers before budget reviews, renewals, or audits. It recalculates table relationships, flags missing or inconsistent rows, and reports when input is insufficient rather than inventing a clean result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ledger inputs may contain sensitive software, account, vendor, or cloud-cost information.

Mitigation: Run the checker locally on copied or redacted ledger data and avoid sharing input or output files that contain confidential values.

Risk: The skill checks arithmetic and table consistency, but does not determine vendor license terms or replace legal review.

Mitigation: Use findings as triage for data quality and cost checks, then confirm licensing obligations against contracts with legal or procurement reviewers.

Risk: Outputs and operational guidance are mainly Chinese.

Mitigation: Use a Chinese-reading reviewer, or translate and verify output, before relying on results in non-Chinese workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/software-license-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable Chinese text or JSON containing check results, missing-input guidance, executed checks, and withheld checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers. The skill reports insufficient input without producing a no-issues conclusion.]

## Skill Version(s):

1.0.46 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
