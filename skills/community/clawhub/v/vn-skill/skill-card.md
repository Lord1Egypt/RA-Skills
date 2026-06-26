## Description: <br>
VN Skill helps agents process local video, audio, and image files on macOS with VN Video Editor, including captions, subtitles, denoising, extraction, compression, merging, and background removal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cawcut](https://clawhub.ai/user/cawcut) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents on macOS use this skill to run local VN Video Editor media workflows for local files, including subtitle generation, SRT burn-in, compression, denoising, extraction, merging, and portrait cutout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download, persist, and run a native helper executable on the user's Mac. <br>
Mitigation: Review the helper source or release provenance, confirm the SHA-256 checksum from a trusted source, and approve the install before execution. <br>
Risk: Caption engines or helper commands may trigger additional downloads before processing. <br>
Mitigation: Ask for explicit approval before CLI or model downloads run, especially on first use. <br>
Risk: Previews sent through chat platforms are uploads of derived media. <br>
Mitigation: Confirm with the user before sending previews and keep sensitive media local when upload is not intended. <br>


## Reference(s): <br>
- [vnapp-cli Reference](references/cli-reference.md) <br>
- [VN Video Editor App Store Page](https://apps.apple.com/us/app/vn-video-editor/id1494451650) <br>
- [vnapp-cli Helper Download](https://github.com/cawcut/skill-vn/releases/download/0.1.0/vnapp-cli-darwin-universal-v0.1.0.5.zip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-lines CLI status interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on local files and may create edited media files, captions, images, previews, or VN drafts.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
