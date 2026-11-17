## Description:

Transcribe user-supplied voice notes, interviews and recordings with PyAI Hear using the official CLI. Supports local audio and asynchronous HTTPS audio jobs, with available speaker/timestamp results. Requires a PyAI account and transcription permissions; does not record microphones or make calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atomsai](https://clawhub.ai/user/atomsai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn user-authorized voice notes, interviews, and recordings into transcripts through PyAI Hear. It supports local audio files and audio already available at an authorized HTTPS URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio is sent to PyAI for processing and consumes project usage; signed URLs and transcripts may contain sensitive information.

Mitigation: Confirm the intended project and permissions, submit only authorized recordings, and keep signed URLs and transcripts private.

## Reference(s):

- [PyAI CLI documentation](https://pyai.com/cli)
- [PyAI Hear streaming SDK documentation](https://docs.pyai.com)
- [PyAI homepage from skill metadata (this skill uses the CLI, not remote MCP)](https://pyai.com/mcp)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text transcript or JSON transcript with available segments, timestamps, and speaker labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Speaker labels and timestamps are included only when returned; speaker labels do not identify real people.]

## Skill Version(s):

1.0.0 (source: evidence.json release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
