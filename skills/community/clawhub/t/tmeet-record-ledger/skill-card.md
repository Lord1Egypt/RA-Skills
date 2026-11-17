## Description:

Use the complete official Tencent Meeting record command family to locate recordings, retrieve native smart-minutes summaries and Todos, verify evidence in transcripts, handle recording-access requests, and produce a source-labeled meeting Todo ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metaphor279](https://clawhub.ai/user/metaphor279)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external collaborators use this skill to locate Tencent Meeting recordings, retrieve native smart-minutes summaries and transcript evidence, and assemble a source-labeled meeting summary and Todo ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Tencent Meeting recordings, transcripts, and smart-minutes content.

Mitigation: Install only when the agent should work with meeting content available through the user's tmeet login, and review outputs for sensitive details before sharing.

Risk: Playback or download links may contain temporary credentials.

Mitigation: Show those links only when the user explicitly requests them, note expiry, and keep them out of Todo ledgers.

Risk: Permission requests can initiate a real access approval workflow.

Mitigation: Require explicit confirmation in a separate user turn before committing a permission request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metaphor279/skills/tmeet-record-ledger)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown meeting summary and Todo ledger with source labels; may include Tencent Meeting CLI commands when relevant.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Markdown, CSV, or JSON files only when the user asks to save results to a specified location.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
