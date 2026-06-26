## Description: <br>
Complete Venice AI API toolkit - image generation, video, audio, embeddings, transcription, characters, models, and admin functions. Privacy-focused inference with zero data retention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sabrinaaquino](https://clawhub.ai/user/sabrinaaquino) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to call Venice AI APIs for media generation and editing, speech, transcription, embeddings, model and character discovery, and account administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected prompts, media, audio, text files, and admin requests to Venice AI. <br>
Mitigation: Install and run it only when that data transfer is intended, and review local file paths before upload-style commands. <br>
Risk: Admin API keys can access billing, usage, and API-key management operations. <br>
Mitigation: Use an inference key for normal generation tasks and reserve admin keys for billing and API-key management. <br>
Risk: Generated media and reports can be written to local files. <br>
Mitigation: Choose output paths deliberately and inspect generated files before sharing or reusing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sabrinaaquino/venice-api-kit) <br>
- [Publisher Profile](https://clawhub.ai/user/sabrinaaquino) <br>
- [Venice AI](https://venice.ai) <br>
- [Venice API Documentation](https://docs.venice.ai) <br>
- [PEP 723 Inline Script Metadata](https://peps.python.org/pep-0723/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, API calls] <br>
**Output Format:** [Markdown guidance with shell commands; scripts print JSON, text, CSV, tables, or media file paths depending on the command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated images, audio, video, embeddings, transcripts, usage reports, and discovery results to local files when an output path is provided.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
