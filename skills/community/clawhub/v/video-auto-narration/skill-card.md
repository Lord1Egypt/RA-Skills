## Description: <br>
Generates narration for silent screen-recording videos by extracting key frames, drafting a presentation-style voiceover script, synthesizing speech with Microsoft Edge neural TTS, and merging the audio into the original video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanzhang-oss](https://clawhub.ai/user/ryanzhang-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, demo creators, and product teams use this skill to turn silent screen-recording demos into narrated videos with a companion voiceover script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated narration text may contain sensitive information from screen recordings and is sent to Microsoft Edge TTS during speech synthesis. <br>
Mitigation: Review and redact recordings and generated scripts before TTS; avoid secrets, regulated data, private customer information, and confidential dashboards unless approved for this processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryanzhang-oss/video-auto-narration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands plus generated video, audio, frame, and script files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates extracted frame images, MP3 narration segments, a merged narrated video, and a companion voiceover Markdown file; requires ffmpeg, ffprobe, python3, and edge-tts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
