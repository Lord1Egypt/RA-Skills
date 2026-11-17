## Description:

Locate the full path of executable commands in the system PATH. Find command locations, verify installation, and resolve command conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent to locate executable command paths in PATH, verify that tools are installed, and diagnose command resolution issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation claims options such as --all, --json, and multi-command support that the bundled script does not implement.

Mitigation: Before relying on advanced options, test the installed skill behavior and treat unsupported options as documentation/implementation mismatches.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/which-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and command-path text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report a resolved executable path or that a command was not found.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
