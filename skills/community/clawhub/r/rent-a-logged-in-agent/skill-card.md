## Description:

Lend or rent out a logged-in Claude Code or Codex agent through SettleMesh for allowlisted or trusted callers with metered billing and sandboxed execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[structureintelligence](https://clawhub.ai/user/structureintelligence)

### License/Terms of Use:

MIT

## Use Case:

External developers and trusted collaborators use this skill to lend or invoke a logged-in coding agent for paid, per-minute work through SettleMesh. It is intended for allowlisted accounts or accepted friends, not public offers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote callers receive prompt-level access to a credential-bearing logged-in coding agent.

Mitigation: Install only when SettleMesh and every allowed caller are fully trusted, and run from a dedicated disposable account or VM with no unrelated SSH, cloud, repository, or personal credentials.

Risk: The skill depends on an unpinned external SettleMesh CLI.

Mitigation: Pin and verify the CLI version where possible before lending access.

Risk: Disabling sandbox enforcement can expose host credentials and the injected agent login.

Mitigation: Avoid the no-sandbox override; use a filesystem-confining sandbox backend such as sandbox-exec on macOS or bwrap on Linux.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the settlemesh CLI and SETTLE_API_KEY; produces setup, lending, invocation, and safety guidance for a local agent session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
