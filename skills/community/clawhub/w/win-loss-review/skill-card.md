## Description:

Runs a monthly review of closed CRM deals and proposes evidence-backed ICP checks, insights, objections, and client context in a pull request with a Slack digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

RevOps teams and sales leaders use it to compare closed-won and closed-lost CRM deals, document evidence-backed patterns, and propose context updates for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with high confidence because the CLI fallback may download an unpinned version and contact data may be collected beyond the stated need.

Mitigation: Consider avoiding installation until the CLI fallback is pinned to a reviewed version and contact data collection is limited to necessary fields.

Risk: The security evidence is incomplete: one executable file was only partially inspected.

Mitigation: Have the remaining executable fully inspected before relying on the security assessment.

## Reference(s):

- [CRM audit reference](artifact/references/crm-audit.md)
- [ClawHub release page](https://clawhub.ai/cargo-ai/skills/win-loss-review)

## Skill Output:

**Output Type(s):** [Markdown files, Text]

**Output Format:** [Markdown context files and run record, pull request content, and a five-line Slack digest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include counts and denominators; proposals are submitted for human review.]

## Skill Version(s):

0.2.0 (source: SKILL.md frontmatter; release evidence agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
