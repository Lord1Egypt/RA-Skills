## Description:

Use study limitations drafter for academic writing workflows that need structured execution, explicit assumptions, and clear output boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Academic writers, researchers, and agents use this skill to draft professionally worded study limitation sections, grant proposal risk notes, and peer review responses from explicit study constraints and assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged script can overwrite any writable output path supplied with --output.

Mitigation: Use --output only with a deliberate workspace-local filename, avoid existing files, and run with sandbox-level write restrictions until output path validation is enforced.

Risk: Generated limitation language may understate uncertainty or overgeneralize beyond the supplied study constraints.

Mitigation: Review drafted statements against the source study design, required assumptions, and documented scope before using them in academic or grant materials.

## Reference(s):

- [Study Limitations Drafter](https://clawhub.ai/aipoch-ai/skills/study-limitations-drafter)
- [Publisher profile: aipoch-ai](https://clawhub.ai/user/aipoch-ai)
- [Audit Reference](references/audit-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown limitation statements with optional workspace file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify assumptions, scope limits, risks, and unresolved checks when relevant.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
