## Description:

Provides an OpenClaw session memory workflow that stores, restores, and archives conversation summaries to reduce context loss after session restarts without extra API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winter1102](https://clawhub.ai/user/winter1102)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to preserve useful conversation context across restarted sessions by reading, appending, and archiving local session summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation summaries may be saved locally and reused in later sessions without clear user controls.

Mitigation: Require explicit opt-in, retention, review, deletion, and secret-redaction controls before enabling automatic persistence.

Risk: The referenced AGENTS.md.patch is missing from the artifact, so installation behavior cannot be fully reviewed from the release files.

Mitigation: Inspect or supply the missing patch before deployment and verify that restored summaries are treated as untrusted notes rather than instructions.

Risk: Workspace-relative memory paths can place persisted summaries somewhere the operator did not intend.

Mitigation: Configure storage under a trusted absolute directory with appropriate access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/winter1102/skills/session-persistence)
- [Publisher profile](https://clawhub.ai/user/winter1102)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Files]

**Output Format:** [Markdown guidance and Bash-managed local Markdown session summary files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads local session memory under a workspace-relative memory directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
