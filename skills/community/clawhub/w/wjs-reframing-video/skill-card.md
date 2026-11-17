## Description:

Converts videos between landscape and portrait formats by cropping to the inverted aspect ratio and tracking the visually active speaker with face landmarks and mouth-motion variance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianshuo](https://clawhub.ai/user/jianshuo)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and developers use this skill to repurpose interviews, podcasts, talks, and phone-recorded videos between portrait and landscape formats while keeping the active speaker in frame.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes local videos with ffmpeg and Python media libraries, and the chosen output file can be overwritten during rendering.

Mitigation: Use it only in an environment suitable for local media processing, review output paths before execution, and keep separate copies of original inputs.

Risk: First-run model download can fail in offline environments and introduces a model-provenance dependency.

Mitigation: Pin dependency versions, prefetch the MediaPipe face landmarker model for controlled deployments, and verify the downloaded model hash.

Risk: Visual active-speaker tracking can be wrong with profile faces, overlapping speech, small or wide shots, heavy camera motion, long silence, or mouth gestures that are not speech.

Mitigation: Inspect the generated .crop.json sidecar and sample output; adjust face-picking or mouth-motion thresholds, pre-segment footage, or stabilize input video when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jianshuo/skills/wjs-reframing-video)
- [MediaPipe FaceLandmarker model](https://storage.googleapis.com/mediapipe-models/face_landmarker/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and descriptions of generated media files and JSON sidecars]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the bundled crop workflow is executed, it can create a cropped MP4 and a .crop.json sidecar without modifying the original input.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
