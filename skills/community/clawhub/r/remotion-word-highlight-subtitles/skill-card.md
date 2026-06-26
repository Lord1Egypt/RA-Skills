## Description: <br>
Add word-level highlighted subtitles to local short videos using Whisper word timestamps and Remotion rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x00000003](https://clawhub.ai/user/0x00000003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to transcribe local short videos, convert Whisper word timestamps into Remotion caption data, render current-word highlighted subtitles, and verify the final video output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local video or audio may contain sensitive content. <br>
Mitigation: Use the skill only on media the user explicitly provides, and avoid sensitive media unless local processing is intended. <br>
Risk: The workflow may create or reuse Remotion/npm project files and modify the working folder. <br>
Mitigation: Run it in a working folder that can be modified, and review generated or reused Remotion and npm dependencies before rendering. <br>
Risk: Automatic speech recognition can produce incorrect names, numbers, or homophones in subtitles. <br>
Mitigation: Perform the required transcript QA pass, apply a correction map before rendering, and inspect still frames before accepting the final video. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0x00000003/remotion-word-highlight-subtitles) <br>
- [Remotion Word Highlight Subtitles Usage Guide](https://github.com/0x00000003/remotion-word-highlight-subtitles) <br>
- [Word Highlight Subtitle Example](https://raw.githubusercontent.com/0x00000003/remotion-word-highlight-subtitles/main/assets/effect-word-highlight.jpg) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON/code snippets; generated artifacts include Remotion caption JSON and rendered video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes user-provided local media, writes outputs next to the source video by default, and requires visual and ffprobe verification of the rendered result.] <br>

## Skill Version(s): <br>
0.1.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
