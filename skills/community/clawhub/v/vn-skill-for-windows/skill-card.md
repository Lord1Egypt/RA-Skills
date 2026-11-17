## Description:

Local video, image, and audio processing skill for Windows that helps an agent run VN Tools CLI workflows for captions, subtitles, denoising, extraction, compression, merging, and cutout tasks on local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cawcut](https://clawhub.ai/user/cawcut)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process local media files on Windows through guided VN Tools CLI commands. It is intended for practical video, image, and audio transformations such as auto-captioning, subtitle burn-in, compression, denoising, extraction, clip merging, and foreground cutout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically download and silently install an unverified Windows MSI.

Mitigation: Review before installing, and prefer a release that asks before installation and verifies the MSI hash and publisher signature.

Risk: Some caption models may download on first use.

Mitigation: Use the skill only when first-use model downloads are acceptable, or choose the built-in caption model path when avoiding additional downloads is required.

## Reference(s):

- [VN Tools CLI reference](references/cli-reference.md)
- [VN Skill homepage](https://www.vlognow.me/skill/)
- [ClawHub skill page](https://clawhub.ai/cawcut/skills/vn-skill-for-windows)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown status messages with PowerShell command invocations and local media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI prints generated output paths on success; filenames include timestamps, and large video outputs may be represented by lower-resolution previews when chat upload limits apply.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
