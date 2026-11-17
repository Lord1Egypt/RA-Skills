## Description:

Audit an unfamiliar codebase and map architecture, user-facing features, maturity, and risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nalendrax8](https://clawhub.ai/user/nalendrax8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to inspect unfamiliar repositories, map architecture and user-facing features, assess maturity, surface risks, and prepare practical implementation handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prompt an agent to inspect repository files during broad repository-analysis tasks.

Mitigation: Use it only in repositories whose files you are comfortable having the agent read.

Risk: Static repository audits can produce misleading conclusions if claims are not tied to inspected files or verified behavior.

Mitigation: Require claims to cite inspected files or patterns, and label static-code inferences instead of presenting them as verified runtime behavior.

## Reference(s):

- [Repo Discovery Auditor README](artifact/README.md)
- [Repo Discovery Auditor Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-based findings tied to inspected files and patterns; no fixed token cap is specified.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
