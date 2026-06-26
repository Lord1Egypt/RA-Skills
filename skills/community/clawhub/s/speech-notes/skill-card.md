## Description: <br>
Converts recordings, speech audio, or existing transcripts into structured Chinese meeting and speech notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqunabc](https://clawhub.ai/user/guoqunabc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external collaborators, and operators use this skill to transcribe Chinese meeting or speech recordings and turn either audio or existing transcripts into formal, structured notes suitable for Feishu-style documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recordings and transcripts may contain sensitive personal, business, or regulated information and may be sent to external transcription providers. <br>
Mitigation: Use only provider accounts and regions approved for the recording's data class, and avoid confidential or regulated recordings unless Feishu, Gemini, or Qwen/DashScope are approved for that use. <br>
Risk: Raw transcript files saved locally can retain sensitive meeting content after the notes are produced. <br>
Mitigation: Decide the storage location and retention period before processing, then delete or protect raw transcripts according to the user's data-handling policy. <br>
Risk: The workflow can run or create helper scripts for audio processing and transcription API calls. <br>
Mitigation: Review generated or referenced helper scripts before execution, especially commands that process local recordings or send audio to remote APIs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoqunabc/speech-notes) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/guoqunabc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown meeting notes with transcription text, optional shell commands, and optional helper code for audio processing or API calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local transcript files and may use Feishu STT, Gemini, or Qwen/DashScope transcription services when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
