## Description: <br>
Vision lets agents without native image understanding analyze, describe, compare, and extract content from local or remote images through a configured OpenAI-compatible vision service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guorui999](https://clawhub.ai/user/guorui999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when a base model lacks vision support and needs to interpret screenshots, photos, image files, or image URLs. It is suited to image description, comparison, OCR-like extraction, and visual issue analysis after the user configures a compatible provider and API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive images, URLs, and prompts may be sent to the configured third-party vision provider. <br>
Mitigation: Use only providers approved for the data being analyzed, avoid IDs, secrets, medical or financial documents, and internal materials without explicit approval. <br>
Risk: API credentials are entered during setup and stored in the skill configuration. <br>
Mitigation: Protect the skill directory from sharing, backups, or commits, and rotate the API key if exposure is possible. <br>
Risk: Installation can fetch files from a supplied remote source. <br>
Mitigation: Review the install source before running it and prefer a pinned trusted URL or checksum-verified package. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guorui999/vision-2) <br>
- [Server-resolved GitHub source](https://github.com/guorui999/vision) <br>
- [Aliyun Bailian console](https://bailian.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text returned on stdout, with setup and usage instructions documented as Markdown and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports one or more local image paths or image URLs; requires a configured API key, base URL, and model; default request cap is 1024 output tokens.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
