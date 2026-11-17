## Description:

Baidu Agent Sandbox management skill for creating, connecting to, inspecting, executing commands in, and destroying sandbox instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igogo888](https://clawhub.ai/user/igogo888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Baidu Agent Sandbox credentials, create sandbox instances from supported templates, connect to existing sandboxes, inspect sandbox files and metadata, run commands, and end sandbox sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful sandbox credentials and may store API keys in a user-level environment file.

Mitigation: Install only after trusting the publisher and service; prefer a safer secret manager or tightly permissioned skill-specific file for secrets.

Risk: The skill can pass sensitive API keys or COMATE tokens through command-line arguments or sandbox environment variables.

Mitigation: Avoid passing real API keys or COMATE tokens on the command line; scope credentials narrowly and rotate them after testing.

Risk: The skill depends on the Baidu sandbox service and a custom Baidu pip index.

Mitigation: Review the configured E2B_DOMAIN and dependency source before use, and install only if those services are trusted.

Risk: Sandbox kill operations destroy sandbox state.

Mitigation: Confirm destructive lifecycle commands and preserve important sandbox data before ending a sandbox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/igogo888/skills/sandbox-manager)
- [Baidu Agent Sandbox console](https://console.cloud.baidu-int.com/aitools/sandbox-square)
- [Baidu sandbox usage documentation](https://ku.baidu-int.com/knowledge/HFVrC7hq1Q/_SKPgSwp2G/B8wSneaLSC/xBjsa6yz-ZsV4-)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python snippets, sandbox identifiers, and service URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credential setup steps, sandbox template choices, timeout values, command results, and sandbox lifecycle status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
