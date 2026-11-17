## Description:

Use when addressing computer configuration failures, software or package installation errors, command line exceptions, network connectivity bugs, or system runtime crashes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hermes186](https://clawhub.ai/user/hermes186)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT staff, and support agents use this skill to classify, diagnose, and resolve software, package installation, command-line, network, runtime, and configuration issues. It guides evidence collection, verification, and troubleshooting memory updates for repeated problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create persistent .troubleshooting-memory/ files that could capture sensitive logs, paths, or environment details.

Mitigation: Review memory entries before keeping or sharing them, and avoid persisting secrets, credentials, private logs, or unnecessary personal data.

Risk: Troubleshooting suggestions can include privileged or global system changes, including Docker permission changes, process termination, and package or path updates.

Mitigation: Review each command before execution, prefer scoped project-level fixes, and confirm the target OS, path, service, and process before applying changes.

Risk: Some common fixes may weaken security, such as disabling TLS verification for Git.

Mitigation: Use insecure bypasses only as temporary diagnostics, document the reason, and restore secure settings after testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hermes186/skills/troubleshooting-computer-issues)
- [Diagnostic Templates](references/diagnostic-templates.md)
- [Memory Format Specification](references/memory-format.md)
- [Common Solutions Index](references/common-solutions.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown troubleshooting guidance with command snippets and memory-entry updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .troubleshooting-memory/ Markdown files in the active workspace.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
