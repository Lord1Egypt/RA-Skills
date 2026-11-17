## Description:

Zaomeng Skill helps host-managed agents prepare Chinese novel character distillation, relationship extraction, relationship graph export, and in-character dialogue context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wkbin](https://clawhub.ai/user/wkbin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and host-managed agent users use this skill to turn Chinese novel text into structured character profiles, relationship artifacts, persona bundles, and dialogue-ready context for act, insert, and observe roleplay flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The self-card helper can delete or overwrite files outside its intended folder if given an unsafe card ID.

Mitigation: Install only in a sandboxed or backed-up workspace, do not pass untrusted values to --card-id or --cards-root, avoid self-card delete until path validation is fixed, and prefer pinned installer versions over @latest.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wkbin/skills/zaomeng-skill)
- [Capability Index](references/capability_index.md)
- [Output Schema](references/output_schema.md)
- [Chat Contract](references/chat_contract.md)
- [Validation Policy](references/validation_policy.md)
- [Safety Policy](references/safety_policy.md)
- [Host Workflow Example](examples/host_workflow_example.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON guidance with Python helper commands; generated artifacts may include persona Markdown, JSON status files, Mermaid, HTML, and SVG.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The host performs model calls; the skill prepares prompt payloads, validates workflow artifacts, and writes status sidecars.]

## Skill Version(s):

4.1.8 (source: SKILL.md frontmatter, .metadata.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
