## Description: <br>
Local LRC Editor is a local Flask web tool for creating, importing, calibrating, and exporting LRC lyric files with waveform visualization, millisecond timestamp editing, realtime highlighting, and browser local autosave. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiyunnet](https://clawhub.ai/user/xiyunnet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Lyric creators and music workflow users use this skill to run a local browser editor for timing lyrics to audio, importing existing LRC files, adjusting timestamps, and exporting standard LRC output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Flask server binds broadly and exposes unauthenticated upload and shutdown actions. <br>
Mitigation: Bind the server to 127.0.0.1, use it only in a trusted local environment, and stop the service when editing is complete. <br>
Risk: The startup script installs Python packages at runtime. <br>
Mitigation: Run the skill in a virtual environment and review the dependency list before installation. <br>
Risk: Uploaded filenames are written to the temporary directory during waveform processing. <br>
Mitigation: Use trusted local files and sanitize upload filenames before adapting this service for shared environments. <br>
Risk: Lyrics and the current file name are saved in browser localStorage. <br>
Mitigation: Clear browser storage after editing sensitive or unpublished lyrics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiyunnet/xi-lrc-editor) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Local web UI and downloadable LRC text files, with Markdown setup guidance for the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Flask service on port 698 and stores working lyric data in browser localStorage.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
