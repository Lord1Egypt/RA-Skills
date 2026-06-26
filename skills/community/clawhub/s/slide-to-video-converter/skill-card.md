## Description: <br>
End-to-end pipeline for converting PPT/PPTX/PDF slides with speaker notes into narrated MP4 videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzsunzixiang](https://clawhub.ai/user/hzsunzixiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and content teams use this skill to turn slide decks and per-slide narration into narrated MP4 training, lecture, or presentation videos with subtitles and quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional HTTP TTS service is reported as too open and may expose or overwrite local files if reachable by others. <br>
Mitigation: Run the service only when needed, bind it to localhost, add access control, and restrict accepted input and output paths before exposing it beyond a local trusted environment. <br>
Risk: Confidential presentation text may be sent to an online TTS service when using the default Edge TTS mode. <br>
Mitigation: Use local TTS for sensitive content and run the skill in a constrained project directory or virtual environment. <br>


## Reference(s): <br>
- [Speaker Notes Script Format](references/script-format.md) <br>
- [ClawHub release page](https://clawhub.ai/hzsunzixiang/slide-to-video-converter) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the bundled scripts can generate slide images, TTS audio, per-slide videos, and a final MP4 in the project output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
