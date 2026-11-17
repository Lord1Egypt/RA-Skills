## Description:

Detect and redact PII from text files. Supports 15 categories including credit cards, SSNs, emails, API keys, addresses, and more -- with zero dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentward-ai](https://clawhub.ai/user/agentward-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers, security teams, and agent operators use this skill to detect and redact sensitive personal data in local text files before sharing or inspecting the content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JSON plus --output workflow can write raw sensitive values to a predictable *.entity-map.json sidecar file.

Mitigation: Use JSON plus --output only when the raw entity map is explicitly needed; treat the sidecar as highly sensitive and delete it after use.

Risk: Input, sanitized output, or entity-map files may be exposed through shared, synced, indexed, or backed-up directories.

Mitigation: Run the skill only on trusted local paths and write outputs to locations that are not shared, synced, indexed, or broadly backed up.

Risk: Reading raw input files or entity-map files can expose PII to an agent or reviewer.

Mitigation: Inspect only sanitized output or safe preview/JSON summaries; do not open raw inputs or *.entity-map.json files during agent workflows.

## Reference(s):

- [Supported PII Categories](references/SUPPORTED_PII.md)
- [AgentWard repository](https://github.com/agentward-ai/agentward)
- [AgentWard support](https://github.com/agentward-ai/agentward/issues)
- [AgentWard](https://agentward.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, files, guidance]

**Output Format:** [Markdown guidance with shell commands; sanitized text files, safe preview text, and JSON summaries when the script is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sanitized output replaces detected values with numbered placeholders; JSON and preview modes omit raw PII from stdout.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, clawhub.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
