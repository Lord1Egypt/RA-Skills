## Description: <br>
Helps an agent burn SRT subtitles into video, soft-mux togglable subtitles, or combine burned subtitles with dubbed audio and an original-audio bed in one ffmpeg encode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianshuo](https://clawhub.ai/user/jianshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media localization agents use this skill to produce upload-ready MP4 files with burned or soft-muxed subtitles, optionally mixing dubbed audio with the original audio as a low-volume bed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script may automatically download and run an unverified ffmpeg executable from evermeet.cx. <br>
Mitigation: Install a trusted libass-enabled ffmpeg yourself, or review and trust the executable in /tmp/ff_bin/ffmpeg before using the fallback. <br>
Risk: Subtitle burn-in re-encodes the video and permanently changes the rendered pixels. <br>
Mitigation: Render a short preview and inspect a frame at a long subtitle cue before running a full render. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianshuo/wjs-burning-subtitles) <br>
- [evermeet ffmpeg static build](https://evermeet.cx/ffmpeg/getrelease/zip) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with shell commands and MP4 file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports burned subtitles, soft-muxed subtitles, dub-only audio replacement or mixing, and full localized cuts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
