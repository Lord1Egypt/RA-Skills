## Description: <br>
Creates AI-narrated short videos from existing clips and a script through a two-phase workflow that generates review materials before assembling the final FFmpeg-rendered video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessy-huang](https://clawhub.ai/user/jessy-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users can use this skill to turn source video clips and narration text into social-media-ready explainer videos with AI voiceover, subtitles, transitions, and a required human review checkpoint before final rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local scripts can run broader code and shell commands than the video-creation task strictly requires. <br>
Mitigation: Run the skill only in a dedicated project folder after reviewing the scripts and generated commands. <br>
Risk: A config.py file and media paths from an untrusted source could affect what local files or commands the workflow touches. <br>
Mitigation: Use only trusted configuration files and verify all source media paths before running either phase. <br>
Risk: Narration text is sent to edge-tts for voice generation. <br>
Mitigation: Avoid sensitive narration content unless sending it to edge-tts is acceptable for the project. <br>
Risk: The xfade path uses a shell-command execution pattern that deserves review before processing third-party files. <br>
Mitigation: Patch that path to subprocess-style argument execution or review the generated inputs before use. <br>


## Reference(s): <br>
- [FFmpeg on Windows: Pitfalls & Solutions](references/ffmpeg-pitfalls.md) <br>
- [Configuration example](references/config-example.py) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>
- [ClawHub skill page](https://clawhub.ai/jessy-huang/video-short-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python configuration and shell commands; generated artifacts include subtitle review Markdown, narration audio, SRT subtitles, intermediate media files, and a final MP4 video.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses FFmpeg/ffprobe for local media processing and edge-tts for narration; the workflow requires user approval before final video assembly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
