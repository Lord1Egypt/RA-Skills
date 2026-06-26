## Description: <br>
Local speech-to-text with OpenAI Whisper CLI. Supports Chinese, English, 100+ languages with translation and summarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gykdly](https://clawhub.ai/user/gykdly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe local audio files with Whisper, optionally translating speech to English or producing a short text summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio transcripts are saved as .txt files beside the source audio. <br>
Mitigation: Run the skill only on audio you are comfortable storing locally, and delete or protect generated transcript files according to your data-handling requirements. <br>
Risk: The quick-command setup adds a persistent shell alias to ~/.zshrc. <br>
Mitigation: Add the alias only after confirming the script path is trusted and appropriate for the local environment. <br>
Risk: Whisper models may be downloaded and cached under the user's account. <br>
Mitigation: Install Whisper from a trusted source and account for local model cache storage when handling sensitive environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcripts are written as .txt files beside the source audio when the Whisper CLI runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
