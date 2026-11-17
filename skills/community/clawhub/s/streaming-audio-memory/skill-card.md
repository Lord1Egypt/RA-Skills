## Description:

Ingests live edge-device audio into per-device streaming memory so an agent can monitor audio streams and answer questions about a device's audio history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to stream authorized audio chunks from edge devices into BlueColumn memory and ask questions about retained per-device audio history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent ambient audio memory can expose highly sensitive audio and derived transcripts across a broad device scope.

Mitigation: Use only with clear authorization, notice, and consent for the specific devices and environments being monitored.

Risk: Uploaded audio and derived transcripts may have unclear storage, protection, retention, or deletion handling.

Mitigation: Confirm BlueColumn data handling controls before sending real streams, and avoid production or regulated audio until those controls are approved.

Risk: Access to the BlueColumn API key enables audio ingestion and recall actions.

Mitigation: Store the key in the platform secret store, restrict access to authorized agents, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/streaming-audio-memory)
- [BlueColumn streaming audio API base URL](https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and authorized audio sources; supports streaming recall responses via SSE.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
