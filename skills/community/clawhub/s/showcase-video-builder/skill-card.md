## Description:

Build polished showcase and demo videos from screenshots, avatars, and text overlays using ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, hackathon teams, and OSS project maintainers use this skill to turn static screenshots, avatars, and written captions into showcase videos, demo reels, product walkthroughs, and social media clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted image filenames may change the ffmpeg command that the bundled script runs.

Mitigation: Use only trusted local image directories, or update the script to use shell arrays and quoted path arguments before processing files from other people.

Risk: Screenshots and images may contain sensitive information.

Mitigation: Review and sanitize local media before processing or sharing generated showcase videos.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/showcase-video-builder)
- [Publisher profile](https://clawhub.ai/user/nissan)
- [Skill source documentation](artifact/SKILL.md)
- [Showcase builder script](artifact/scripts/build_showcase.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with ffmpeg command examples and shell script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local ffmpeg; no outbound network requirement is declared in metadata.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
