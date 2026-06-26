## Description: <br>
Analyze local or linked video files and convert them into structured summaries of features, functions, workflows, or topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mrgoodgreen](https://clawhub.ai/user/Mrgoodgreen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and analysts use this skill to turn long, noisy, or hard-to-access videos into tracked transcripts and readable structured summaries while preserving honest progress reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local video, transcript, and summary files can contain private content. <br>
Mitigation: Use the workflow only for videos intended for local analysis and clear tmp/video_analysis after the work is complete. <br>
Risk: Workspace-local media dependencies may be installed without pinned versions. <br>
Mitigation: Review the dependency install plan and pin versions before using the skill in controlled or repeatable environments. <br>
Risk: Noisy automatic transcription can produce incomplete or incorrect summaries. <br>
Mitigation: Keep confidence caveats, preserve intermediate transcript files, and verify important details against the source video. <br>


## Reference(s): <br>
- [Tracked Video Analysis Pipeline](references/pipeline.md) <br>
- [ClawHub release page](https://clawhub.ai/Mrgoodgreen/tracked-video-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands, status JSON, progress logs, and transcript JSONL files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces tracked local extraction and structuring artifacts under tmp/video_analysis when the workflow is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
