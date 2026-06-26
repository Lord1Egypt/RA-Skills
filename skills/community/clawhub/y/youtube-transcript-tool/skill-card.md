## Description: <br>
Fetches YouTube video transcript or subtitle information from a provided video URL, with support claims for timestamps and multiple languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loverun321](https://clawhub.ai/user/loverun321) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to request YouTube transcript or subtitle data by supplying a YouTube URL. The published artifact currently returns a structured readiness response for matched YouTube video IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence flags a published API key in the artifact. <br>
Mitigation: Do not install or use this version until the publisher removes the credential and rotates any exposed secret. <br>
Risk: The release evidence flags broad paid-service activation wording. <br>
Mitigation: Review and narrow invocation wording so the skill only runs when a user clearly requests YouTube transcript retrieval. <br>
Risk: The artifact handler reports service readiness instead of fetching an actual transcript. <br>
Mitigation: Verify runtime behavior against expected transcript retrieval before relying on the skill for transcript output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loverun321/youtube-transcript-tool) <br>
- [Publisher profile](https://clawhub.ai/user/loverun321) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON response with status, video ID, transcript fields, language metadata, or error text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a YouTube video URL containing a recognizable 11-character video ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
