## Description:

Detect which of your contacts have changed jobs and where they went, powered by Cargo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and account teams use this skill to check existing CRM contacts for job changes, identify where movers went, and prioritize follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact records may contain information that cannot be shared with Cargo.

Mitigation: Use only contacts you are permitted to share with Cargo.

Risk: Credit use grows with the number of contacts processed and can recur on scheduled runs.

Mitigation: Start with a small sample and review the credit estimate before approving larger batches or recurring runs.

Risk: The CLI and optional full skill pack are outside the reviewed artifact.

Mitigation: Review and pin the CLI and any optional full pack separately.

## Reference(s):

- [Cargo GTM Skills project homepage](https://github.com/getcargohq/gtm-skills)
- [Job change monitoring recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/job-change-monitoring.md)

## Skill Output:

**Output Type(s):** [Structured data, Analysis]

**Output Format:** [Structured contact records with job-change status and person details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One result per contact; status is moved, left, no_change, or unknown.]

## Skill Version(s):

1.1.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
