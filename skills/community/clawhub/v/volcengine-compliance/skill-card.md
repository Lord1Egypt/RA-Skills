## Description:

This skill helps agents recommend Volcengine Config compliance baselines, summarize account compliance posture, and guide custom Rego rule creation or confirmed conformance pack deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators, developers, and security or compliance engineers use this skill to evaluate Volcengine accounts, choose built-in compliance baselines, and produce compliance posture reports. It can also guide custom Rego rule authoring when built-in templates do not cover a requested check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment path can create or modify cloud compliance resources, including conformance packs, configuration recorders, and custom rules.

Mitigation: Use read-only recommendation and overview flows by default; review dry-run output and require explicit confirmation before any write path.

Risk: The security review notes that resource-modifying rules may be created even though the workflow is presented as audit-focused.

Mitigation: Before confirmed deployment, verify that every planned rule effect is visible and set to Audit unless the user separately approves a modifying effect.

Risk: Cloud recorders, conformance packs, and custom rules can persist after the skill run.

Mitigation: Confirm target account, permissions, names, scope, and cleanup expectations before enabling recorders or registering rules.

Risk: Generated CSV reports may contain account or resource data and should be treated as untrusted spreadsheet input.

Mitigation: Handle reports as sensitive operational output, avoid exposing credentials or tokens, and sanitize CSVs before opening them in spreadsheet tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volc-sdk-team/skills/volcengine-compliance)
- [Compliance recommendation reference](references/recommend.md)
- [Compliance overview reference](references/overview.md)
- [Conformance pack deployment reference](references/apply.md)
- [Authentication and prerequisites reference](references/auth.md)
- [Custom Config rule writing reference](references/writing-config-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, CSV, Rego policy snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write compliance overview artifacts as Markdown, CSV, and JSON when the overview command is run.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
