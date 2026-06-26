## Description: <br>
Translate .txt files into Chinese or another target language using configurable OpenAI-compatible APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litousteven](https://clawhub.ai/user/litousteven) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and document-processing users use this skill to configure a translation provider and translate text files while preserving formatting, chunking large files, and reporting the translated output path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text files are sent to the configured external translation provider. <br>
Mitigation: Use only providers approved for the data being translated, and avoid confidential, regulated, or proprietary documents unless that provider is approved for them. <br>
Risk: The translation API key may be stored in a skill-local .env file. <br>
Mitigation: Protect or remove the .env file after setup, use revocable credentials, and rotate the key if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litousteven/smart-translate-txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text files with terminal status lines and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a translated .txt file, prints OUTPUT:<path> on success, and uses configurable target language, source language, chunk size, concurrency, and context-window settings.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
