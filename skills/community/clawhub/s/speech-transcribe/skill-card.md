## Description: <br>
Transcribes local audio and video files into plain-text transcripts and SRT subtitles with sentence-level timestamps using a remote Modal L4 GPU Whisper pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[speech2srt](https://clawhub.ai/user/speech2srt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and other ClawHub users use this skill to send selected audio or video files to Modal for GPU-backed transcription and retrieve .txt and .srt outputs in the original file locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected recordings are uploaded to Modal for remote GPU processing. <br>
Mitigation: Use only media that is acceptable to process with Modal, and avoid sensitive or regulated recordings unless that service is approved for the data. <br>
Risk: The workflow includes a recursive cleanup command for the selected remote volume slug. <br>
Mitigation: Confirm the slug and selected files before cleanup, and download expected transcript and subtitle outputs before removing the remote volume path. <br>


## Reference(s): <br>
- [Error Handling](references/error-handling.md) <br>
- [ClawHub skill page](https://clawhub.ai/speech2srt/speech-transcribe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated .txt/.srt transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one plain-text transcript and one SRT subtitle file per processed media file; streams Modal progress and reports processed count and real-time factor.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata; artifact frontmatter says v1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
