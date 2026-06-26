## Description: <br>
Extract, transcribe, and translate YouTube video transcripts using the YouTubeTranscript.dev V2 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volodstaimi](https://clawhub.ai/user/volodstaimi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, agents, and content workflows use this skill to retrieve YouTube captions, run ASR transcription when captions are unavailable, translate transcripts, and process videos in batches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube video identifiers and transcript content may be sent to the external YouTubeTranscript.dev API. <br>
Mitigation: Use the skill only when sending this data to YouTubeTranscript.dev is allowed by the user's data-handling requirements. <br>
Risk: ASR jobs can deliver results to a webhook URL supplied in the request. <br>
Mitigation: Use only trusted HTTPS webhook endpoints under the user's control and avoid confidential, regulated, or private video content unless approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volodstaimi/youtube-transcript-api) <br>
- [YouTubeTranscript.dev website](https://youtubetranscript.dev) <br>
- [YouTubeTranscript.dev API documentation](https://youtubetranscript.dev/api-docs) <br>
- [npm SDK](https://www.npmjs.com/package/youtube-audio-transcript-api) <br>
- [YouTubeTranscript.dev pricing](https://youtubetranscript.dev/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request examples, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to YouTubeTranscript.dev and a bearer API key supplied by the user.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
