## Description:

Local video, audio, and image processing skill for macOS that uses VN Video Editor to generate captions, burn subtitles, denoise media, extract audio or frames, compress media, merge video clips, and remove portrait backgrounds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cawcut](https://clawhub.ai/user/cawcut)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users on macOS use this skill to have an agent prepare local VN Video Editor commands for media processing tasks such as captions, compression, denoising, extraction, merging, and background removal. It is intended for local files and requires VN Video Editor and the vnapp-cli bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill installs and runs a downloaded third-party macOS bridge under ~/.openclaw/tools.

Mitigation: Review the publisher, pinned SHA-256, and install source before enabling the skill, and prefer releases that ask before installing or updating executables.

Risk: The release security guidance says media previews may be sent through remote chat platforms when used there.

Mitigation: Confirm before transmitting previews and avoid sending sensitive media through remote chat channels.

Risk: The release security guidance notes that removing quarantine can bypass normal Gatekeeper review.

Mitigation: Preserve platform security checks where possible and only run the bridge after local review.

## Reference(s):

- [vnapp-cli Reference](artifact/references/cli-reference.md)
- [VN Video Editor App Store Page](https://apps.apple.com/us/app/vn-video-editor/id1494451650)
- [vnapp-cli Release Download](https://github.com/cawcut/skill-vn/releases/download/0.1.0/vnapp-cli-darwin-universal-v0.1.0.5.zip)
- [ClawHub Skill Page](https://clawhub.ai/cawcut/skills/vn-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide local macOS media processing through VN Video Editor and may include command options, status checks, and result paths.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
