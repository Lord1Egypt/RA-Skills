## Description: <br>
Automates rough cuts for single-person talking-to-camera video by detecting silence, scoring candidate segments, removing duplicate content, clipping the best takes, and generating reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gilbertwuu](https://clawhub.ai/user/gilbertwuu) <br>

### License/Terms of Use: <br>
GPL v3 <br>


## Use Case: <br>
Content creators and video engineers use this skill to automate first-pass editing of single-person A'Roll footage, including candidate segment selection, cross-take deduplication, final clip or batch concatenation, and Markdown reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local media processing can expose private speech in Whisper transcripts and generated Markdown reports. <br>
Mitigation: Process videos in a dedicated local work directory and review or delete generated reports when source videos contain private speech. <br>
Risk: The workflow invokes FFmpeg and openai-whisper on user-provided file paths, with path-handling cautions noted by the security evidence. <br>
Mitigation: Use trusted FFmpeg and openai-whisper installations, keep videos in a dedicated folder, and avoid filenames containing quotes or newlines. <br>
Risk: Batch mode removes intermediate clips and temporary audio after concatenation, which can discard review artifacts. <br>
Mitigation: Run on copied source media and use a disposable work directory when intermediate files may need later inspection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gilbertwuu/video-aroll-auto-editor) <br>
- [README.md](artifact/README.md) <br>
- [CODE_DOCUMENTATION.md](artifact/CODE_DOCUMENTATION.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; the skill runtime produces MP4 video files and Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python 3.8+, FFmpeg with ffprobe, and openai-whisper; intended for .MTS, .mp4, and .mov inputs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata); artifact documentation describes Video Auto Editor v4.7 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
