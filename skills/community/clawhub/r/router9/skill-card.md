## Description: <br>
Router9 provides agent-accessible AI tools for speech recognition, text-to-speech, image description, OCR, image generation, and file storage through the Router9 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shushuo-dev](https://clawhub.ai/user/shushuo-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use Router9 to run Router9 API tasks from an agent session, including transcribing audio, generating speech, analyzing images, extracting text from images, generating images, and managing stored files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-selected media, prompts, and files to Router9 services. <br>
Mitigation: Use it only for data that is appropriate to share with Router9, and avoid sending secrets or regulated data unless approved for that environment. <br>
Risk: The skill requires a Router9 API key. <br>
Mitigation: Store ROUTER9_API_KEY securely, avoid committing it to files or logs, and rotate it if exposure is suspected. <br>
Risk: Upload, download, and delete commands can affect remote storage records or local output paths without extra confirmation safeguards. <br>
Mitigation: Review file IDs, selected files, and output paths before running storage commands. <br>


## Reference(s): <br>
- [Router9 Skill on ClawHub](https://clawhub.ai/shushuo-dev/router9) <br>
- [Router9 Publisher Profile](https://clawhub.ai/user/shushuo-dev) <br>
- [Router9 Homepage](https://router9.com) <br>
- [Router9 API Key Settings](https://router9.com/settings/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI responses are JSON, text, or generated files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ROUTER9_API_KEY and may write audio, image, or downloaded files to user-selected output paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
