## Description:

Maintain an explicit Markdown commitments ledger with a local cockpit for NOW, next actions, deadlines, waiting items, workstream states and inbox capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Questlog to maintain an explicit local commitments ledger, capture authorized task deltas, track current focus, next actions, deadlines, waiting items, and inspect the ledger through bundled localhost views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The localhost cockpit is single-user local software and is not a remotely authenticated multi-user service.

Mitigation: Bind and use it only on loopback, do not expose the port through a network or reverse proxy, and do not run it as root.

Risk: Commitment ledgers may contain private tasks, transcripts, account context, or local paths.

Mitigation: Set QUESTLOG_ROOT to a dedicated private directory, keep state outside public artifacts, and use synthetic examples for reports or tests.

Risk: Concurrent or stale edits can overwrite decisions made from an older visible ledger state.

Mitigation: Use the bundled CLI or localhost UI so writes share the lock, preserve If-Match revision checks, and reload/reconsider after conflicts.

Risk: Users may mistake saved instruction drafts for completed external actions.

Mitigation: Treat pending instructions as local drafts only; review and authorize any future scheduler, mail, calendar, or action-runner integration separately.

## Reference(s):

- [README](README.md)
- [Ledger format](references/ledger-format.md)
- [Security](SECURITY.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local ledger updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-user local state; no bundled external action runner, scheduler, mail, calendar, or semantic search integration.]

## Skill Version(s):

1.0.0 (source: release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
