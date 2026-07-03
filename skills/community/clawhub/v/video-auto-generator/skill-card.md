## Description: <br>
A video automation skill that helps agents generate scripts, narration, subtitles, cover images, and assembled videos from a topic using edge-tts and ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nh5gntnf78-oss](https://clawhub.ai/user/nh5gntnf78-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketing teams, educators, and developers use this skill to turn a topic into short-form video assets, including scripts, narration text, subtitles, covers, and assembled media. It is suited for batch content production and platform-specific video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local commands, process media with ffmpeg, and create files in the Desktop or a selected folder. <br>
Mitigation: Use a workspace where local command execution and media processing are acceptable, and pass an explicit output directory before running generation workflows. <br>
Risk: Narration text, prompts, or generated content may be sent to third-party TTS or video services. <br>
Mitigation: Do not process sensitive scripts or private business content unless the user accepts the relevant provider terms and data exposure. <br>
Risk: Generated output may include hardcoded promotional copy or other unwanted marketing text. <br>
Mitigation: Inspect generated scripts, narration, subtitles, and final videos before publishing or sharing them. <br>
Risk: The security evidence flags a risky rendering path and unusual output paths may behave unexpectedly. <br>
Mitigation: Avoid unusual characters in output paths until the rendering path is fixed, and review command behavior before batch runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nh5gntnf78-oss/skills/video-auto-generator) <br>
- [Kling AI developer site](https://klingai.com/) <br>
- [Kling image generation API endpoint](https://api.klingai.com/v3/images/generations) <br>
- [HeyGen video generation API endpoint](https://api.heygen.com/v2/video/generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with code blocks plus generated script, narration, image, audio, and video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on local ffmpeg, Python packages, edge-tts, and optional third-party video APIs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
