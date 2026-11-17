## Description:

Use this skill when the user needs to create AI videos, manage canvases, nodes, files, or interact with the ZenVFX platform via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lenzli](https://clawhub.ai/user/lenzli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to guide agents through ZenVFX CLI setup, authentication, canvas management, node editing, task execution, and troubleshooting for AI video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on a global ZenVFX CLI package from the Tencent registry.

Mitigation: Install only from a trusted registry source and prefer a pinned CLI version for repeatable deployments.

Risk: The skill uses a ZenVFX token for authentication.

Mitigation: Use least-privilege, rotatable tokens and avoid entering tokens where shell history or logs may capture them.

Risk: The documented CLI workflows can modify or delete ZenVFX project files, canvases, nodes, and edges.

Mitigation: Review proposed commands before execution and require explicit confirmation before delete operations such as file or node removal.

Risk: Known CLI or daemon version mismatches can cause execution failures after upgrades.

Mitigation: Restart the daemon after CLI upgrades and verify the installed CLI version before running video generation workflows.

## Reference(s):

- [ZenVFX CLI ClawHub skill page](https://clawhub.ai/lenzli/skills/zenvfx-cli)
- [lenzli ClawHub publisher profile](https://clawhub.ai/user/lenzli)
- [Tencent npm registry](https://mirrors.tencent.com/npm/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is oriented around ZenVFX CLI commands that return JSON on stdout.]

## Skill Version(s):

1.0.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
