## Description: <br>
Converts video between horizontal and vertical orientations by cropping to the inverted aspect ratio and tracking the active speaker with MediaPipe face landmarks and mouth-motion variance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianshuo](https://clawhub.ai/user/jianshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, editors, and developers use this skill to repurpose talking-head, interview, podcast, and mobile video between landscape and portrait formats while keeping the likely active speaker in frame. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First run downloads the MediaPipe face model before processing can complete. <br>
Mitigation: Pre-stage and verify the model in offline or stricter environments, or run the skill only where this download is acceptable. <br>
Risk: The workflow depends on ffmpeg, ffprobe, and Python media packages to process local video files. <br>
Mitigation: Use current, trusted media tooling and run the skill only on videos you intentionally choose. <br>
Risk: The generated MP4 and .crop.json sidecar may reflect imperfect face or speaker tracking. <br>
Mitigation: Review the rendered video and crop-plan sidecar before publishing or relying on the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianshuo/wjs-reframing-video) <br>
- [MediaPipe Face Landmarker model](https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output is a cropped MP4 and JSON crop-plan sidecar.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The original input video is not modified; generated sidecars record crop settings, speaker segments, and face-tracking counts.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
