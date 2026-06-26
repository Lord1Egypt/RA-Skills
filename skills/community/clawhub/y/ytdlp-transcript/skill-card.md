## Description: <br>
Fetches cleaned transcript text from a YouTube URL or video ID using yt-dlp captions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nerikko](https://clawhub.ai/user/Nerikko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn YouTube videos into transcript text that an agent can summarize, translate, or analyze. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs the local yt-dlp executable found on PATH. <br>
Mitigation: Install yt-dlp from a trusted source and confirm the PATH entry points to the intended executable before use. <br>
Risk: Using the skill contacts YouTube for the video URL or ID supplied by the user. <br>
Mitigation: Only submit video identifiers that are appropriate to disclose to YouTube under the user's policy and environment. <br>
Risk: The skill briefly creates temporary caption files while processing transcripts. <br>
Mitigation: Run it in an environment where temporary file creation is acceptable and review cleanup behavior for sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Nerikko/ytdlp-transcript) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transcript with a language header] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and a trusted yt-dlp executable available on PATH.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
