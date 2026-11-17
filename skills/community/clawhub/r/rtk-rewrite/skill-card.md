## Description:

RTK Rewrite intercepts OpenClaw exec tool calls and delegates command rewrites to rtk rewrite to reduce token usage while preserving command intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luw2007](https://clawhub.ai/user/luw2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this OpenClaw plugin to automatically rewrite eligible shell commands through RTK before execution, with the goal of reducing agent token usage while keeping the intended command behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin can automatically alter exec commands across OpenClaw agents when enabled.

Mitigation: Review the plugin before installation, enable it only for intended environments, and test representative rewrites before relying on it in routine workflows.

Risk: Command rewriting depends on the external rtk binary resolved from the OpenClaw gateway PATH.

Mitigation: Use only a trusted rtk installation and verify the resolved binary path and version in the gateway environment.

Risk: The artifact documentation includes a curl-to-sh installer path.

Mitigation: Avoid the curl-to-sh installer and prefer a trusted package manager or reviewed installation method.

Risk: Audit logs can include original and rewritten commands, which may contain secrets.

Mitigation: Keep audit logging disabled unless logs are protected and the deployment accepts that command text may contain sensitive data.

## Reference(s):

- [RTK repository](https://github.com/rtk-ai/rtk)
- [OpenRTKlaw plugin homepage](https://github.com/aimagist/openrtklaw)
- [ClawHub skill page](https://clawhub.ai/luw2007/skills/rtk-rewrite)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Configuration]

**Output Format:** [Rewritten shell command text with optional plain-text audit log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Automatically rewrites only exec tool calls when enabled; unsupported commands are left unchanged by rtk rewrite.]

## Skill Version(s):

0.15.3 (source: server release metadata, artifact frontmatter, and plugin manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
