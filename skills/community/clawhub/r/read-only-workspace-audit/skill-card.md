## Description:

Audit whether one imported workspace snapshot is rich enough for export, cited AI, or MCP consumption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local-first academic tooling reviewers use this skill to audit imported Campus Copilot workspace snapshots for open items, evidence location, and readiness for export, cited AI, or MCP consumption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Snapshot-only evidence may be mistaken for live browser or session state.

Mitigation: Limit claims to imported snapshots or exported artifacts and state when evidence is insufficient for live-state conclusions.

Risk: Suggested MCP or server commands could start unexpected local tools if run in the wrong repository.

Mitigation: Run commands only in the intended Campus Copilot repository and verify the package names before starting local services.

Risk: Incomplete snapshot evidence may be treated as ready for export, cited AI, or MCP consumption.

Mitigation: Report which site carries each piece of evidence and call out missing or insufficient evidence before approving downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaojiou176/skills/read-only-workspace-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text audit guidance with optional shell commands and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only posture; conclusions are limited to imported snapshot or exported artifact evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
