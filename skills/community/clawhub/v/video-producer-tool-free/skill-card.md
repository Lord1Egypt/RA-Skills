## Description: <br>
短视频生成-免费版 helps an agent turn a topic and spoken script into a short MP4 video through storyboard planning, AI image generation, Chinese TTS narration, Remotion rendering, and audio-video assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent users use this skill to generate lightweight short videos for social media, educational explainers, and simple promotional clips from a topic and scene-level script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends video scripts, prompts, or narration text to third-party image and TTS providers. <br>
Mitigation: Use trusted providers, review API key configuration, and avoid sending sensitive or proprietary content unless the provider terms are acceptable. <br>
Risk: The workflow runs local Node, Remotion, and FFmpeg commands and writes generated media files. <br>
Mitigation: Run it in a scoped workspace, review output paths and generated files, and keep dependencies current. <br>
Risk: Generated visual or voice assets can raise copyright, consent, or suitability concerns for public release. <br>
Mitigation: Review generated media before publishing and avoid using the skill for copyrighted media processing, live streaming, or professional film post-production workflows outside its documented scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/video-producer-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown instructions with JSON examples, bash commands, and generated video project files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces storyboard and material plans, Remotion video code, audio and image assets, and an MP4 output; the free edition is documented for one video, up to 10 scenes, and Chinese TTS.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
