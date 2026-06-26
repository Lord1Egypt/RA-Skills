## Description: <br>
End-to-end short-video post-production from one raw talking-head video: transcribes speech, builds timed subtitles with highlights, adds SFX or BGM when available, and renders a final video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiepige8](https://clawhub.ai/user/tiepige8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to turn one spoken raw video into a short-form edit with readable subtitles, keyword highlights, sparse sound effects, optional background music, and a rendered MP4 output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local ffmpeg and Python commands and writes output files beside the source video. <br>
Mitigation: Use it only on videos intended for processing and review the generated working directory and final render before distribution. <br>
Risk: The workflow may prompt installation of faster-whisper if transcription support is missing. <br>
Mitigation: Review any dependency-install prompt and install packages only from trusted package sources in an appropriate environment. <br>
Risk: Default language, subtitle style, BGM, or SFX choices may be inappropriate for some videos. <br>
Mitigation: Specify language, output, subtitle style, BGM, and SFX preferences when defaults are not appropriate. <br>


## Reference(s): <br>
- [ASS Subtitle Effects Reference](references/ass_effects.md) <br>
- [Audio Resources & Douyin Ad Audio Design Guide](references/audio_resources.md) <br>
- [Skill page](https://clawhub.ai/tiepige8/video-post-production) <br>
- [Mixkit commercial music](https://mixkit.co/free-stock-music/tag/commercial/) <br>
- [Mixkit whoosh sound effects](https://mixkit.co/free-sound-effects/whoosh/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a working directory beside the input video with alignment.json, production_plan.json, subtitles.ass, and final.mp4.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
