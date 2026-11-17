## Description:

This skill helps agents use the Unkey CLI to manage API namespaces, keys, identities, permissions, roles, rate limits, analytics queries, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyriswu](https://clawhub.ai/user/kyriswu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate, check, and troubleshoot Unkey CLI commands for API key management, RBAC, identities, rate limiting, and verification analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Root keys may be exposed in prompts, command examples, terminal output, or logs.

Mitigation: Avoid exposing root keys, redact credentials in displayed commands, and prefer configured authentication through environment variables or Unkey login.

Risk: An unpinned global Unkey CLI installation can change command behavior as the CLI evolves.

Mitigation: Install only from Unkey's official package or release channel and prefer a pinned, verified version where operational stability matters.

Risk: Mutating Unkey resources such as keys, permissions, roles, rate limits, or deletes can affect production access.

Mitigation: Review mutations carefully, confirm destructive operations before execution, and use built-in help or official docs to verify flags.

## Reference(s):

- [Unkey Documentation Index](https://unkey.com/docs/llms.txt)
- [ClawHub Skill Page](https://clawhub.ai/kyriswu/skills/unkey-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and optional JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should redact root keys and prefer JSON output for scripting workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
