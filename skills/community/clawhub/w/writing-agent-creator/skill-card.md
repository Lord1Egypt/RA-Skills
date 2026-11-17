## Description:

Generates OpenClaw writing-agent configurations, reusable custom templates, and sub-agent spawn instructions for specialized writing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balingsisi](https://clawhub.ai/user/balingsisi)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to create reusable writing-agent templates, generate SOUL.md configuration snippets, and produce sub-agent spawn instructions for writing, development, review, testing, and database tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent, auto-loaded custom templates can override built-in templates when they reuse the same ID.

Mitigation: Use only trusted custom templates and review same-ID templates before allowing them to replace built-in behavior.

Risk: Generated content may change agent behavior if saved into SOUL.md or the user template directory.

Mitigation: Confirm and review generated configuration before copying it into SOUL.md or saving it under ~/.openclaw/workspace/agent-templates/.

Risk: The skill's file-write behavior is described inconsistently across the evidence.

Mitigation: Treat generated outputs as proposals until the user explicitly approves any persistent save location.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/balingsisi/skills/writing-agent-creator)
- [Agent Template Registry](references/agent-registry.md)
- [Output Templates](references/output-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown snippets with inline command examples and YAML-style template configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable user template content and sub-agent spawn instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
