## Description: <br>
Transcribe audio or video files using the TextOps/Modal API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanelrotem](https://clawhub.ai/user/netanelrotem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to convert local or URL-hosted audio and video files into text transcripts, with optional speaker separation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recordings, links, filenames, job IDs, and transcript content are sent to TextOps for processing. <br>
Mitigation: Use the skill only for media that may be shared with TextOps, and avoid private or tokenized URLs unless necessary. <br>
Risk: Generated transcript files may contain sensitive audio content and are saved locally. <br>
Mitigation: Delete or secure generated transcript files when the audio is sensitive. <br>
Risk: The TEXTOPS_API_KEY credential is required to run the transcription workflow. <br>
Mitigation: Keep TEXTOPS_API_KEY in an environment variable rather than chat or files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/netanelrotem/transcribe-he) <br>
- [Publisher profile](https://clawhub.ai/user/netanelrotem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcripts, JSON transcript files, and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill saves both .json and .txt transcript files and reports the generated file paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
