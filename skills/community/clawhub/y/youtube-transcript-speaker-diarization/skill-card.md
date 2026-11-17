## Description:

Generate speaker-aware YouTube transcripts through diarize. Use when generic transcript skills are not enough and you need attributed speakers in TXT, JSON, SRT, or VTT format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patelnav](https://clawhub.ai/user/patelnav)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to submit YouTube URLs to diarize and retrieve speaker-attributed transcripts for reading, structured processing, or subtitle workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom diarize endpoint could receive the bearer token used for transcript requests.

Mitigation: Use the default https://diarize.io endpoint unless the custom endpoint is fully trusted.

Risk: API keys could be exposed through untrusted OpenClaw config or inherited environment variables.

Mitigation: Store API keys only in trusted local configuration or environment sources and review those sources before running the skill.

Risk: Crafted timeout or polling arguments could trigger command execution or unsafe runtime behavior.

Mitigation: Do not allow agents or external input to choose timeout or polling arguments until the script validates them as bounded positive integers.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/patelnav/skills/youtube-transcript-speaker-diarization)
- [diarize documentation](https://diarize.io/docs)
- [diarize API key settings](https://diarize.io/settings/api-keys)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [TXT, JSON, SRT, or VTT transcript content, with JSON job responses for submit and status commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, jq, and YOUTUBE_TRANSCRIPT_API_KEY; default endpoint is https://diarize.io.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
