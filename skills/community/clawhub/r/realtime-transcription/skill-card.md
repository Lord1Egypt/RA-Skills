## Description: <br>
Real-time audio transcription for system or microphone audio with automatic summarization and dated Markdown archival after manual stop or idle timeout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeleoo](https://clawhub.ai/user/leeleoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture local system or microphone audio, produce live transcripts, summarize sessions, and archive meeting or recording notes as dated Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Microphone or system audio may contain sensitive personal, business, or third-party information that is transcribed and saved locally. <br>
Mitigation: Use the skill only with appropriate consent, store archives in protected locations, and delete transcripts that are no longer needed. <br>
Risk: Transcript text may be sent to the configured LLM during summarization. <br>
Mitigation: Use an approved LLM configuration for the data being processed, and avoid summarizing sensitive recordings unless policy allows it. <br>
Risk: The skill installs and runs local Python dependencies and an ASR model. <br>
Mitigation: Run it in a virtual environment, pin or review dependencies and the SenseVoice model, and keep permissions limited to the commands and triggers required for transcription. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leeleoo/realtime-transcription) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Transcript text, Markdown archive files, and command-oriented agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Archives include generated title, summary, source, duration, and full transcript; summary prompts truncate transcript input at 4000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
