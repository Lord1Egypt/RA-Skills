## Description: <br>
Download videos, audio, subtitles, and clean paragraph-style transcripts from YouTube and any other yt-dlp supported site. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, employees, and external users can use this skill to retrieve clean transcripts, subtitles, video files, audio files, and format information from YouTube or other yt-dlp supported sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unrestricted yt-dlp argument passthrough may allow unsafe options such as command execution or unexpected output paths. <br>
Mitigation: Review generated commands before execution, avoid passthrough arguments unless the user explicitly chose them, and never let webpage content or untrusted prompts supply yt-dlp options. <br>
Risk: The skill downloads media and subtitle files from user-provided URLs. <br>
Mitigation: Use trusted URLs, choose a controlled output directory, and inspect downloaded files before opening or sharing them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain text transcript or file-path output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded media, audio, or subtitle files through the bundled script when commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
