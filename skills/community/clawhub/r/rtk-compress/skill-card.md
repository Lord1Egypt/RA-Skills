## Description:

Save 60-90% of LLM tokens on shell commands, file reads, and test outputs. Wraps rtk CLI for compressed output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erscoder](https://clawhub.ai/user/erscoder)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to route common shell, file-reading, test, build, lint, git, container, and analytics commands through rtk so command output is compressed before it reaches the agent context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer guidance includes a curl-to-shell fallback path.

Mitigation: Prefer package-manager installation; if using the installer script, pin and verify it before execution.

Risk: Broad command wrapping can hide important details for git mutations, pushes, GitHub actions, container or Kubernetes operations, environment inspection, and network commands.

Mitigation: Require normal user approval and review full uncompressed output for sensitive or state-changing commands.

Risk: Compressed command output can omit details needed by scripts, parsers, or exact-output reviews.

Mitigation: Use bare commands when output is piped, parsed, or needed exactly, and fall back to the bare command if rtk fails.

## Reference(s):

- [rtk](https://github.com/rtk-ai/rtk)
- [OpenClaw feature request](https://github.com/openclaw/openclaw/issues/35053)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output may be compressed or filtered by rtk; exact full output requires using the underlying command directly.]

## Skill Version(s):

1.15.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
