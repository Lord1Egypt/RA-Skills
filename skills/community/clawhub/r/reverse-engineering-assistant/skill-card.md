## Description:

Authorized reverse engineering of shipped software, tracing feature implementations, recovering algorithms and formats, comparing versions, all evidence-backed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software engineers use this skill to investigate software they own or are authorized to analyze, trace behavior and data formats, compare versions, and document evidence-backed findings. When requested, it also guides reconstruction and validation of a feature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI fallback may download and execute third-party code without an additional npm prompt.

Mitigation: Use a restricted analysis directory, retain the version pin, and review updates and setup changes.

Risk: Running analyzed software is not sandboxed and may access files or the network.

Mitigation: Assess the target's file and network access before running it, explain the planned runtime action and permissions, and obtain user confirmation.

## Reference(s):

- [Reverse-Engineering Assistant on ClawHub](https://clawhub.ai/wangjiaocheng/skills/reverse-engineering-assistant)
- [Task catalog and workflow dependencies](references/reverse-engineering-assistant-catalog.md)
- [Task requirements and constraints](references/reverse-engineering-assistant-requirements.md)
- [Exemplar index and report formats](references/reverse-engineering-assistant-exemplars.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown investigation plans, evidence records, and reports; reconstructed code when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings distinguish facts, inferences, and unknowns and link conclusions to evidence. Code is produced only when reconstruction is requested.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
