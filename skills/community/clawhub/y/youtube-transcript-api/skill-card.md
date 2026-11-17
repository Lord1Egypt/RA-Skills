## Description:

Extract, transcribe, and translate YouTube video transcripts using the YouTubeTranscript.dev V2 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volodstaimi](https://clawhub.ai/user/volodstaimi)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to retrieve YouTube captions, request ASR transcription when captions are unavailable, translate transcripts, and process multiple videos for AI or content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends YouTube video URLs or IDs, transcript options, webhook URLs, and an API key to the third-party youtubetranscript.dev service.

Mitigation: Use direct HTTPS requests when possible, keep API keys secret, and only send webhook URLs for trusted HTTPS endpoints under the user's control.

Risk: Using the optional npm SDK adds dependency exposure beyond the direct API examples.

Mitigation: Pin and review the npm SDK before use, or prefer the direct HTTP examples for minimal dependency exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volodstaimi/skills/youtube-transcript-api)
- [YouTubeTranscript.dev](https://youtubetranscript.dev)
- [YouTubeTranscript.dev API documentation](https://youtubetranscript.dev/api-docs)
- [youtube-audio-transcript-api npm package](https://www.npmjs.com/package/youtube-audio-transcript-api)
- [YouTubeTranscript.dev pricing](https://youtubetranscript.dev/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python, JavaScript, and cURL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a YouTubeTranscript.dev API key and network access to the third-party API.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
