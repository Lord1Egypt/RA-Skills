## Description:

Pre-scans a SKILL.md file before ClawHub publishing by simulating the ClawScan security review and reporting whether the skill is likely to pass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanningwang](https://clawhub.ai/user/hanningwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to run a local ClawScan-style pre-check on a SKILL.md file before publishing to ClawHub or after addressing review feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The target SKILL.md and a nearby file manifest are sent to the configured remote LLM provider.

Mitigation: Use only an approved provider, avoid scanning secrets or proprietary material, review the confirmation prompt, and reserve --yes for controlled CI use.

Risk: The local pre-scan does not analyze the contents of other skill files and may differ from ClawHub's production review.

Mitigation: Review companion files separately and treat the local result as pre-publication guidance rather than a final security decision.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hanningwang/skills/skill-prescan)
- [ClawHub Repository](https://github.com/openclaw/clawhub)
- [ClawHub Security Prompt Source](https://github.com/openclaw/clawhub/blob/main/convex/lib/securityPrompt.ts)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Terminal text report or raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured remote LLM provider and can run multiple scans to compare verdict consistency.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
