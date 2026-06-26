## Description: <br>
Convert video files or clips into animated GIFs or WebP using ffmpeg, with resizing, fps control, trimming, palette generation, and file-size optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiwei26](https://clawhub.ai/user/xiwei26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to convert local video files or selected clips into shareable animated GIF or WebP outputs with trimming, frame-rate, size, palette, and quality controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite the chosen output path during conversion. <br>
Mitigation: Choose an output path that is safe to create or overwrite and review it before running conversion. <br>
Risk: Video processing depends on local ffmpeg and ffprobe binaries and local input files. <br>
Mitigation: Install ffmpeg and ffprobe only from trusted sources and use videos you intend to process locally. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Animated GIF/WebP files with concise Markdown status and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and ffprobe on PATH; output size depends on source duration, resolution, fps, colors, and format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
