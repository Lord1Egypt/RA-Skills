## Description:

ZeroToken guides agents toward concise, token-efficient task execution and includes optional utilities for environment detection, UTF-8-safe file handling, encoding conversion, and Windows PowerShell workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phoenixlucky](https://clawhub.ai/user/phoenixlucky)

### License/Terms of Use:

GPL-3.0

## Use Case:

Developers and agent users use ZeroToken to make assistants choose the right task mode, limit unnecessary context, produce concise answers, and apply platform-aware file and shell workflows when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File and encoding utilities can modify project files or overwrite conversion targets.

Mitigation: Review generated commands before execution, use preview or backup modes for conversion and repair workflows, and run the bundled checks after changes.

Risk: Local helper scripts and environment detection can create workspace state or adjust current-repository Git display settings on Windows.

Mitigation: Install only when the concise-output and encoding workflow is desired, run utilities in trusted workspaces, and inspect repository-local configuration changes.

Risk: External search tasks may send query terms to third-party search or browser services.

Mitigation: Avoid external search for sensitive or non-public project details unless the user has confirmed the disclosure.

## Reference(s):

- [ZeroToken Skill](SKILL.md)
- [README](README.md)
- [Unicode Safety Encoding Specification](docs/unicode-encoding-spec.md)
- [Windows / PowerShell Environment Adaptation](references/windows-powershell.md)
- [Major Refactor / Architecture Adjustment Playbook](references/refactor-playbook.md)
- [External Search Guidelines](references/search.md)
- [Tool Mapping and Host-Specific Behavior](references/tool-mapping.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline commands, code snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise, task-mode-driven output; language follows the user's interaction language.]

## Skill Version(s):

1.17.0 (source: frontmatter, package.json, CHANGELOG, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
