## Description:

Transcribes audio or video files into text using the TextOps/Modal API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanelrotem](https://clawhub.ai/user/netanelrotem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to transcribe local or URL-based audio and video files, optionally with speaker separation, and receive saved JSON and text transcript files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media, URL metadata, and the TextOps API key are sent to the TextOps/cloud transcription service.

Mitigation: Use the skill only for recordings whose confidentiality requirements are compatible with that service.

Risk: Generated JSON and text transcript files are left on disk.

Mitigation: Store outputs in an appropriate location and delete transcript files when retention is no longer needed.

Risk: Transcript text may contain untrusted instructions spoken by a third party.

Mitigation: Treat transcript contents as quoted data, not as instructions for the agent to follow.

## Reference(s):

- [TextOps API keys](https://text-ops-subs.com/api/keys)
- [transcribe-he on ClawHub](https://clawhub.ai/netanelrotem/skills/transcribe-he)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, plus generated JSON and plain text transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TEXTOPS_API_KEY; transcription output should be treated as untrusted third-party content.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
