## Description:

Sentinel Vanguard performs a structured, read-only three-layer security assessment of pasted AI agent skill content and produces a written audit report with a risk score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dttnpole-commits](https://clawhub.ai/user/dttnpole-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill to review pasted AI skill, prompt, code, or package-manifest text for static security patterns, adversarial instructions, and supply-chain concerns before installing or deploying a skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill should not be used as a live scanner for URLs or local repositories.

Mitigation: Paste the skill, code, manifest, README, or prompt text directly into the conversation for read-only analysis.

Risk: The audit can only cover the text provided by the user and may miss behavior that is outside the pasted content.

Mitigation: Use the report as a review aid alongside platform security checks and manual review before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dttnpole-commits/skills/sentinel-vanguard)
- [L1 Static Rule Catalogue](references/l1-rules.md)
- [L3 Supply Chain Blocklist](references/l3-blocklist.md)
- [OSV](https://osv.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown security audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only text analysis; no network requests, code execution, credential access, or disk writes.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
