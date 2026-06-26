## Description: <br>
短视频一键生成技能 v2.2。调用video-director进行画面规划，然后生成AI素材、TTS配音、视频渲染，输出完整MP4。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a1024708231](https://clawhub.ai/user/a1024708231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to coordinate storyboard planning, AI image generation, text-to-speech narration, Remotion rendering, and audio-video merging for short vertical videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded shared MiniMax API keys may expose credentials or route usage through keys the operator does not control. <br>
Mitigation: Remove and rotate embedded keys before installation, and require MINIMAX_API_KEY and MINIMAX_IMAGE_API_KEY to be supplied through the operator's environment. <br>
Risk: User-derived text is passed through shell-string execSync calls. <br>
Mitigation: Run only in an isolated workspace and replace shell-string command construction with argument-based process execution before processing untrusted or sensitive text. <br>
Risk: The workflow creates media assets, generated code, and final video files from AI services and local tooling. <br>
Mitigation: Review generated storyboard, assets, source code, and final MP4 before publishing or using the output commercially. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a1024708231/video-producer) <br>
- [Publisher profile](https://clawhub.ai/user/a1024708231) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown storyboards, JSON storyboard data, generated JavaScript/Remotion project files, image/audio assets, and MP4 video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces storyboard.md, storyboard.json, generated materials, audio files, Remotion source code, and out/final.mp4 under the configured project output directory.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
