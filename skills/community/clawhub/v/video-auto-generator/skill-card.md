## Description: <br>
Generates AI-assisted video workflows for scripts, voiceovers, subtitles, covers, and ffmpeg-based editing from a topic or source material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nh5gntnf78-oss](https://clawhub.ai/user/nh5gntnf78-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketing teams, educators, and developers use this skill to turn video topics or source material into scripts, voiceover text, generated assets, shell commands, and local video pipeline outputs for short-form or promotional videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious because the runnable video pipeline may perform materially different work than a user expects from the description. <br>
Mitigation: Review the bundled scripts, generated commands, and planned output directory before installing or running the skill. <br>
Risk: The skill can create local files and invoke ffmpeg, edge-tts, package installation commands, and optional external API calls. <br>
Mitigation: Run it in a controlled workspace, approve dependencies explicitly, and avoid using private source material with third-party providers unless sharing is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nh5gntnf78-oss/skills/video-auto-generator) <br>
- [Kling AI developer site](https://klingai.com/) <br>
- [Kling AI image generation API endpoint](https://api.klingai.com/v3/images/generations) <br>
- [HeyGen video generation API endpoint](https://api.heygen.com/v2/video/generate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python/PowerShell code, JSON reports, text scripts, and generated local media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local script, voice, image, report, and video files; may invoke ffmpeg, edge-tts, package installation commands, and optional external video or avatar APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
