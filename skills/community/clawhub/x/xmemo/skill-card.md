## Description:

Persistent, user-owned memory for agents. Use the standalone runtime to remember, recall, search, preserve restart continuity, manage TODOs and expenses, inspect account overview, activity and stats diagnostics, read user Cloud Skills (read-only) and Dream-run digests (read-only), configure agent instructions, check for updates or upgrade runtime, or diagnose XMemo when MCP tools are unavailable. Not for codebase search, web search, or short-lived in-session notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmemo](https://clawhub.ai/user/xmemo)

### License/Terms of Use:

MIT-0

## Use Case:

People using AI agents can use XMemo to save and retrieve durable project context across sessions, preserve task continuity, manage action items and expenses, and inspect account or runtime status. Developers can use the standalone Node.js runtime when XMemo MCP tools are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious with medium confidence because it could not fully inspect many executable files.

Mitigation: Consider postponing installation until the executable files have been fully inspected and the required tool scope is clear.

Risk: The first-run login flow can save an authentication token unencrypted on the local computer.

Mitigation: Prefer XMEMO_KEY from a managed secret store, or proceed with local sign-in only after accepting that local processes may read the credential file.

## Reference(s):

- [XMemo website](https://xmemo.dev)
- [Memory operations](references/memory-operations.md)
- [Authentication setup](references/auth-setup.md)
- [Command details](references/command-details.md)
- [Ledger operations](references/ledger-operations.md)
- [Runtime operations](references/runtime-operations.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance and command examples; memory results and diagnostics are returned as text or structured data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retrieved memories, task continuity notes, action items, ledger information, or runtime diagnostics.]

## Skill Version(s):

1.1.53 (source: release evidence and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
