## Description:

Legacy compatibility alias for Ziwei + Bazi consultation workflows that forwards older `ziwei-bazi-consulting` prompts to `destiny-fusion-pro` for dual-system consultation reports with unified calculation rules and optional chart output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyfree](https://clawhub.ai/user/spyfree)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation maintainers use this skill when older workflows still call `ziwei-bazi-consulting` and need those requests forwarded to the newer Ziwei and Bazi consultation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The alias runs Python code from a sibling destiny-fusion-pro package that is outside the reviewed artifact.

Mitigation: Install only when the sibling package is trusted, reviewed, and pinned or otherwise controlled at the expected path.

Risk: Forwarded execution inherits the agent's normal local permissions.

Mitigation: Review the forwarded package before deployment and run it only in environments appropriate for its permissions and data access.

## Reference(s):

- [Market Positioning](references/positioning.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or structured JSON consultation output produced by the forwarded destiny-fusion-pro workflow, with shell command guidance for compatibility execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on the separately installed sibling destiny-fusion-pro package for the executable payload.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
