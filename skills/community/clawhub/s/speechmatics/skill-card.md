## Description: <br>
Transcribes audio files such as voice notes, recordings, and podcasts to text using the Speechmatics batch transcription API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coreyh](https://clawhub.ai/user/coreyh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users with Speechmatics configured use this skill to submit audio files for batch transcription, poll job status, and receive transcripts for review or downstream use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are sent to Speechmatics or the configured base URL for transcription. <br>
Mitigation: Use the skill only with recordings appropriate for that service and avoid sensitive recordings unless the service's data handling fits the user's requirements. <br>
Risk: The Speechmatics API key is sensitive and could be exposed through shared files, logs, or command history if mishandled. <br>
Mitigation: Keep the API key out of shared files and logs, and prefer environment or local configuration storage over passing keys in visible commands. <br>
Risk: The default transcript path may overwrite an existing output file. <br>
Mitigation: Set --out explicitly when preserving existing transcript files matters. <br>


## Reference(s): <br>
- [Speechmatics Batch Transcription documentation](https://docs.speechmatics.com/introduction/batch-transcription) <br>
- [ClawHub Speechmatics listing](https://clawhub.ai/coreyh/speechmatics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text transcript, Speechmatics json-v2, or SRT subtitle file; agent guidance is Markdown with shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a Speechmatics API key; default output is written beside the input unless --out is set.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
