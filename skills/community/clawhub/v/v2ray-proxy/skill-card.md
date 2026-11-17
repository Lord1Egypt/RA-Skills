## Description:

Manages a local V2Ray/Xray proxy by starting or stopping the proxy process, setting proxy environment variables, testing connectivity, and optionally wrapping shell commands with temporary proxy access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felixqian4160](https://clawhub.ai/user/felixqian4160)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to manage local proxy access when external network connectivity is needed, including enabling, disabling, testing, and wrapping commands through a V2Ray/Xray proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command wrapper uses eval and can execute unsafe input if untrusted URLs, filenames, branch names, or user-provided command text are passed to it.

Mitigation: Use the wrapper only with trusted, fully reviewed command arguments, or replace it with argument-preserving execution that avoids eval.

Risk: The script may leave a persistent marker in ~/.bashrc when enabling system proxy behavior.

Mitigation: Require explicit opt-in for shell profile changes and document a reversible cleanup path before deployment.

Risk: The script stops processes with pattern-based pkill matching for V2Ray/Xray-related process names.

Mitigation: Track and stop the specific V2Ray process ID launched by the skill instead of relying on broad process-name matching.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/felixqian4160/skills/v2ray-proxy)
- [ClawHub publisher profile](https://clawhub.ai/user/felixqian4160)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill delegates proxy actions to a Bash script and reports connection status and command results.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
