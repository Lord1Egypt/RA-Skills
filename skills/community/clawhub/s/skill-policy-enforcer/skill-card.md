## Description:

Use when checking an agent Skill against a local or enterprise policy before installation, publication, CI approval, marketplace review, or repository merge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[debtvc2022](https://clawhub.ai/user/debtvc2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and review teams use this skill to check agent Skill folders against local or enterprise policy before installation, publication, CI approval, marketplace review, or repository merge. It turns policy violations into repeatable pass, warning, or fail outcomes with rule identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports scanner bypass and unsafe file-reading weaknesses that make it unsuitable as the sole approval gate for untrusted skill packages.

Mitigation: Use it in a constrained workspace and pair results with independent review until symlink handling, pre-read size enforcement, policy regex validation, and broad line-skipping behavior are addressed.

Risk: The skill reads candidate skill folders and evaluates policy-controlled patterns, so weak or overly broad policy settings can miss relevant issues.

Mitigation: Keep policies explicit, review deny and warning rule IDs, and require policy changes instead of prose exceptions when findings are inconvenient.

## Reference(s):

- [Default Conservative Skill Policy](references/default-policy.yaml)
- [Policy Schema](references/policy-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON policy results with pass, warning, or fail status and rule-specific findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit CI-friendly JSON when invoked with --json; deny findings block release or installation decisions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
