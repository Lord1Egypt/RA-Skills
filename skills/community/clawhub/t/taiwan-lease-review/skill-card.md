## Description:

Professional lease contract review for Taiwan rental agreements covering residential, commercial/storefront, and parking space leases, with clause analysis for illegality, unfairness, and risk under Taiwan lease rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External renters, landlords, property managers, and real estate professionals use this skill to review Taiwan residential, commercial/storefront, and parking leases before signing or revising agreements. It helps identify illegal or high-risk clauses, missing mandatory terms, tenant-landlord rights issues, and fairer clause wording.

### Deployment Geography for Use:

Taiwan

## Known Risks and Mitigations:

Risk: The artifact tells agents to run an unbundled relative-path analytics script after use, creating code-execution and privacy review concerns.

Mitigation: Disable or ignore the post-use skills/analytics.py commands unless the publisher provides a bundled, reviewed, consent-based analytics implementation with clear privacy terms.

Risk: The skill is tailored to Taiwan lease workflows and may be inappropriate for other jurisdictions.

Mitigation: Use the review output only for Taiwan rental agreements and have jurisdiction-specific legal advice reviewed by a qualified professional before relying on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tsaitepiao-alt/skills/taiwan-lease-review)
- [Review Report Template](assets/review-report.md)
- [Commercial Lease Special Topics](references/commercial-lease.md)
- [Illegal Clauses](references/illegal-clauses.md)
- [Mandatory Items](references/mandatory-items.md)
- [Parking Lease Special Topics](references/parking-lease.md)
- [Rental Law Summary](references/rental-law.md)
- [Risk Levels](references/risk-levels.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text guidance and Markdown review reports, with optional JSON input for script-generated reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 only when running scripts/analyze-contract.py; review content is Taiwan-specific.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
