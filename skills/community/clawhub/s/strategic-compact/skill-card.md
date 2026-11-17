## Description:

Guides agents to save important context and compact conversations at logical workflow boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to preserve key findings before switching phases or unrelated tasks, then resume with a concise continuation note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional hooks or scheduled runs may use an outdated script path or an untested host integration.

Mitigation: Enable recurring integrations only when wanted, correct the script path, and check the setup in the target environment.

Risk: The reference guide describes a /tmp counter location that differs from the script's current user-state directory.

Mitigation: Follow the script's current user-state behavior and disregard the outdated counter-path instructions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/djc00p/skills/strategic-compact)
- [Strategic Compaction Guide](references/compaction-guide.md)
- [Tool Integration Guide](references/tool-integration.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflow guidance and optional reminder-script integration instructions.]

## Skill Version(s):

1.0.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
