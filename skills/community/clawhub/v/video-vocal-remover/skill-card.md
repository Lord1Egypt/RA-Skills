## Description: <br>
Helps agents reduce human speech frequencies in video audio with ffmpeg while preserving mechanical and environmental sounds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyanbo2007](https://clawhub.ai/user/zhangyanbo2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-processing agents use this skill to produce ffmpeg commands and tuning guidance that attenuate speech in local video files while retaining non-speech machine or environmental audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch commands can process every matching video in a selected folder. <br>
Mitigation: Review the folder path and file pattern before running batch processing, and test on a small copied subset first. <br>
Risk: Incorrect input or output paths can overwrite or replace local media files. <br>
Mitigation: Write to the documented _novoice output first and only replace originals after reviewing the result. <br>
Risk: Frequency filtering may leave some speech audible or reduce desired non-speech audio when frequency ranges overlap. <br>
Mitigation: Listen to the output before use and tune equalizer gain, bandwidth, or added frequency bands for the specific recording. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyanbo2007/video-vocal-remover) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ffmpeg command examples and parameter tuning guidance; resulting media files are created by the user's local ffmpeg run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
