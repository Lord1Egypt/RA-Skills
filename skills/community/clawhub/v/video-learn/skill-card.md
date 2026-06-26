## Description: <br>
Enables an agent to analyze video links, collect available metadata, and summarize key points from supported platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jackeven02](https://clawhub.ai/user/Jackeven02) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to have an agent recognize video URLs, gather metadata from supported video platforms, and produce concise summaries, highlights, and viewing focus points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video metadata, subtitles, or downloaded media may expose private or sensitive content when agents process user-supplied links. <br>
Mitigation: Use trusted video URLs and avoid private videos unless the user intends to share them with the selected platform or API tooling. <br>
Risk: Adapting the yt-dlp command examples with unsafe string interpolation could introduce command execution risk. <br>
Mitigation: Prefer safe argument-based command execution when adapting downloader examples. <br>


## Reference(s): <br>
- [Video Understanding Reference Resources](references/resources.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Jackeven02/video-learn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with optional command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs video metadata, summaries, key points, timestamps when available, and viewing recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
