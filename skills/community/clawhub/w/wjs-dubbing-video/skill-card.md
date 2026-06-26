## Description: <br>
Generates a time-aligned TTS voice dub from a video and target-language SRT, with optional multi-speaker voice routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianshuo](https://clawhub.ai/user/jianshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Video creators and localization engineers use this skill to turn an existing video and target-language SRT into a dubbed MP4. It also supports speaker-specific voice assignment when the user explicitly requests multi-speaker handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subtitle text may be sent to an external TTS provider during dubbing. <br>
Mitigation: Review subtitles for sensitive content before synthesis and confirm the chosen TTS provider before running dubbing commands. <br>
Risk: The skill may access local TTS credentials. <br>
Mitigation: Use a dedicated minimal environment file containing only the required TTS keys instead of loading broad local credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jianshuo/wjs-dubbing-video) <br>
- [Volcano TTS speaker catalog](https://www.volcengine.com/docs/6561/1257544) <br>
- [MediaPipe Face Landmarker model](https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce dubbed MP4 files and per-cue MP3 work files when its scripts are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
