## Description:

Channel and thread memory for Slack: decisions, context, and open loops from across the workspace, requiring a BlueColumn API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Slack workspace agents use this skill to capture decisions, promises, summaries, and context from approved channels and threads, then recall that history before answering questions or following up on open loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slack channel and thread content may be sent to and stored in BlueColumn/Supabase without clear scoping, consent, or retention controls.

Mitigation: Use only approved channels and data, avoid private messages and regulated or sensitive content, and confirm retention, deletion, and access-control terms before broad monitoring.

Risk: The skill requires a BlueColumn API key and provides live API call examples.

Mitigation: Store BLUECOLUMN_API_KEY in approved secret storage, restrict access to it, and review commands before execution.

## Reference(s):

- [BlueColumn API Docs](https://bluecolumn.ai/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLUECOLUMN_API_KEY for BlueColumn API calls.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
