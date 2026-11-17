## Description:

Relay logic and wiring diagram helper. Use when json relay tasks, csv relay tasks, checking relay status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run Relay CLI commands for local entry status, storage, search, removal, export, statistics, and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill is presented as an electrical relay helper, but behaves as a persistent local record manager with deletion, export, and config-writing features.

Mitigation: Review the behavior before installing, test with disposable data, and confirm the local record-management behavior is acceptable for the intended use.

Risk: The script stores arbitrary local entries under ~/.relay by default and can write export files in the current directory.

Mitigation: Avoid storing sensitive data, set RELAY_DIR to a dedicated private directory, and review generated relay-export files before sharing or retaining them.

Risk: Using shared, untrusted, or symlink-prone RELAY_DIR paths can increase local data exposure or file-handling risk.

Mitigation: Use a trusted directory with appropriate permissions and avoid RELAY_DIR values controlled by other users or processes.

## Reference(s):

- [Relay skill page](https://clawhub.ai/ckchzh/skills/relay)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration]

**Output Format:** [CLI text output with JSONL records and optional JSON or CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists entries under RELAY_DIR, defaulting to ~/.relay, and can write relay-export.json or relay-export.csv in the current directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
