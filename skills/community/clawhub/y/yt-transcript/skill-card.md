## Description: <br>
Extracts clean, plain-text transcripts from YouTube links or video IDs for research, summarization, and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alti-Systems](https://clawhub.ai/user/Alti-Systems) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers, researchers, and content analysts use this skill to fetch YouTube transcripts so agents can summarize videos, extract quotes, and support content analysis without manual viewing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive private or internal video URLs may disclose the video ID and request metadata to YouTube or a configured transcript provider. <br>
Mitigation: Use only video links that are appropriate to share with external transcript services, and avoid sensitive URLs unless that exposure is acceptable. <br>
Risk: Documentation mentions Supadata and yt-dlp, while the artifact includes bundled YouTube scripts and package dependencies. <br>
Mitigation: Verify the command path and provider configuration before relying on a specific extraction or fallback method. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Alti-Systems/yt-transcript) <br>
- [Publisher profile](https://clawhub.ai/user/Alti-Systems) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transcript, optionally with timestamped lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a YouTube URL or video ID; bundled scripts also support an optional language parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
