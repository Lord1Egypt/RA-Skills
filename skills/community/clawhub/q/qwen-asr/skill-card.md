## Description: <br>
Transcribe audio files using Qwen ASR (千问STT). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[al-one](https://clawhub.ai/user/al-one) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users can use this skill to convert local audio files or piped audio data into transcript text through the Qwen ASR demo service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are sent to an external Qwen demo service. <br>
Mitigation: Avoid highly sensitive recordings and use the skill only when uploading the chosen audio to that service is acceptable. <br>
Risk: The script may print a remote audio file URL during processing. <br>
Mitigation: Treat logs and terminal output as potentially containing links to uploaded audio and avoid sharing them broadly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/al-one/qwen-asr) <br>
- [Qwen ASR demo service](https://qwen-qwen3-asr-demo.ms.show) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transcript with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required; selected audio is uploaded to an external Qwen demo endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
