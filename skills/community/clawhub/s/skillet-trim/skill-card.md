## Description:

Guides agents to improve test quality and audit or prune low-value coverage without losing important behavioral guarantees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to assess test quality, verify candidate removals against stronger proofs, and plan evidence-backed test cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Test cleanup could remove useful coverage or obscure an existing product defect.

Mitigation: Record evidence and remaining proof before removals, and review coverage changes and baseline failures before accepting the cleanup.

## Reference(s):

- [Campaign mode guide](references/campaign.md)
- [OpenClaw license attribution](references/openclaw-LICENSE)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Code]

**Output Format:** [Markdown audit report with actionable test and code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-led; preserves baseline failures for separate investigation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
