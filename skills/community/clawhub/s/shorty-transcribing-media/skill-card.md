## Description:

Transcribes publicly accessible audio or video links or creates video subtitle tracks through Shorty after the user confirms a quota-consuming job.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

People with public media links use this skill to retrieve transcripts or request subtitle tracks for videos through their Shorty account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Starting a transcription or subtitle job consumes the user's Shorty quota.

Mitigation: Confirm the exact media URL and requested job with the user before starting it; check quota and limits for long media.

Risk: Submitting private or login-walled media links may expose media to the Shorty service or fail processing.

Mitigation: Use publicly accessible media links and avoid private or login-walled URLs unless the user intends Shorty to process them.

## Reference(s):

- [Transcribing Media on ClawHub](https://clawhub.ai/devino/skills/shorty-transcribing-media)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Transcript text or Markdown status and instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Subtitle files are accessed through Shorty; the chat returns job status and a tracking link, not the files.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
