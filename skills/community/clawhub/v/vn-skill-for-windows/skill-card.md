## Description: <br>
Helps agents run local Windows media-processing workflows with VN Tools CLI, including captions, subtitle burn-in, audio denoising, audio or frame extraction, compression, clip merging, and video cutout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cawcut](https://clawhub.ai/user/cawcut) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process local video, image, and audio files on Windows without cloud upload or API keys. It is intended for supported VN Tools CLI operations such as captioning, subtitle burn-in, compression, extraction, denoising, merging, and foreground cutout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or upgrade VN Tools CLI by downloading and running software on Windows. <br>
Mitigation: Require explicit user approval before any install or upgrade, and prefer manual CLI installation and verification on managed or privacy-sensitive systems. <br>
Risk: Some workflows can trigger network downloads, including the installer and larger Whisper model files. <br>
Mitigation: Disclose download size and source before starting downloads, and confirm with the user before downloading URLs, attachments, installers, or large model files. <br>
Risk: Media processing may involve private local audio, video, or images. <br>
Mitigation: Use local files only, avoid cloud uploads, and confirm source and output paths before processing sensitive media. <br>


## Reference(s): <br>
- [VN Tools CLI Reference](references/cli-reference.md) <br>
- [VN Skill Homepage](https://www.vlognow.me/skill/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, Text] <br>
**Output Format:** [Markdown with inline PowerShell commands and concise user-facing status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for local Windows processing and reports generated media file paths after CLI execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
