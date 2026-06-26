## Description: <br>
Generates YouTube video assets from a prompt, including a script, voiceover, stock footage, captions, thumbnail, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mayank8290](https://clawhub.ai/user/Mayank8290) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, marketers, and developers use this skill to automate draft YouTube video production from a topic prompt, including narration, stock media assembly, captions, thumbnails, and upload metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video topics, search phrases, and generated narration may be sent to external Pexels and Microsoft Edge TTS services. <br>
Mitigation: Avoid confidential or regulated prompts, and review generated scripts and metadata before publishing. <br>
Risk: The skill requires a Pexels API key plus local tools such as ffmpeg, edge-tts, and Python packages. <br>
Mitigation: Use a dedicated Pexels key, install dependencies from trusted sources, and keep local media generation in an environment appropriate for the content. <br>
Risk: The documentation overstates that the skill is self-contained. <br>
Mitigation: Confirm the required external services, command-line tools, and environment variables are available before relying on the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mayank8290/youtube-factory) <br>
- [Project homepage](https://github.com/Mayank8290/openclaw-video-skills) <br>
- [Pexels API](https://pexels.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and generated local media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local script.md, voiceover.mp3, video files, thumbnail.jpg, and metadata.json under the configured output directory.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
