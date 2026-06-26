## Description: <br>
Combines two or more synced camera recordings into a single MP4 by generating audio-energy-based multicamera cuts with optional picture-in-picture rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianshuo](https://clawhub.ai/user/jianshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and video editors use this skill to turn synced recordings of the same event into an edited multicamera MP4. It helps choose camera cuts from per-camera audio energy and can render either hard cuts or hard cuts with a corner picture-in-picture inset. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendered outputs can overwrite existing files at the selected EDL or MP4 output paths. <br>
Mitigation: Confirm output filenames before running render scripts and use fresh paths for test renders. <br>
Risk: Local ffmpeg processing reads selected media and sidecar files and depends on valid local tooling. <br>
Mitigation: Run only on intended input videos and sidecars, and confirm ffmpeg and numpy are available before processing. <br>
Risk: Audio-energy-based camera selection can choose a loud but poorly framed or distorted source. <br>
Mitigation: Preview a short sample, listen to the selected audio source, and adjust mode, dwell settings, or manual overrides before a full render. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianshuo/wjs-editing-multicam) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Video files] <br>
**Output Format:** [Markdown guidance with shell commands, EDL JSON, and rendered MP4 outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local media files, sync sidecars, ffmpeg, and numpy; rendered output may overwrite existing files at selected output paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
