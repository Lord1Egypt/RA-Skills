## Description: <br>
Video To Notes turns local or linked videos into transcripts and structured study notes using ffmpeg and Whisper, with note styles for courses, lectures, tutorials, talks, documentaries, and meetings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yll-kb](https://clawhub.ai/user/yll-kb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, students, professionals, and knowledge workers use this skill to convert videos or video URLs into reviewable transcripts and structured notes. The agent checks required tools, optionally downloads supported video URLs after confirmation, transcribes audio, and produces notes tailored to the content type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video transcripts and notes may contain private or sensitive content. <br>
Mitigation: Review generated files after processing and delete transcripts or notes when the source video contains private information. <br>
Risk: URL downloads and local transcription require user-visible local processing and may involve platform or copyright restrictions. <br>
Mitigation: Only process videos the user is allowed to use, confirm any URL download and output directory before execution, and follow platform terms. <br>
Risk: Dependency installation can add local tools or Python packages. <br>
Mitigation: Detect missing dependencies first, show the exact tools or packages and installation commands, and proceed only after explicit user approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yll-kb/video-to-notes) <br>
- [Workflow Reference](artifact/references/workflow.md) <br>
- [Note Templates Reference](artifact/references/note-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown notes and timestamped text transcripts, with shell commands and setup guidance when dependencies or downloads are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcript files are written as .txt beside the source video or in the requested output directory; generated notes are derived from the transcript and the selected note style.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
