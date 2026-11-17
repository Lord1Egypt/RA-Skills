## Description:

Download videos, torrents, magnet links, and Quark share links to 115, Quark, or rclone-compatible cloud storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[graysonzeng](https://clawhub.ai/user/graysonzeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search for media links, submit cloud-side offline download tasks, or download video and torrent content locally before uploading it to configured cloud storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill as suspicious because setup includes high-impact, under-scoped risks around installation and dependency handling.

Mitigation: Review scripts/install.sh before running it, prefer manual dependency installation or a sandboxed environment, and avoid the documented curl-to-sudo rclone installation pattern.

Risk: The skill stores cloud credentials and Quark cookies locally for access to 115, Quark, and rclone-compatible storage.

Mitigation: Use the skill only in an account or environment where those credentials are acceptable, keep rclone and Quark credential files private, and restrict file permissions.

Risk: Torrent searches, cloud-side transfer tasks, and local staging-directory cleanup may create policy, legal, or data-retention risks depending on the environment.

Mitigation: Use only approved content sources and destinations, confirm torrent-search usage is permitted, and configure the staging directory so cleanup cannot remove unrelated files.

## Reference(s):

- [rclone 115 setup guide](references/rclone-setup.md)
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp)
- [rclone 115 fork](https://github.com/gaoyb7/rclone-release)
- [ClawHub skill page](https://clawhub.ai/graysonzeng/skills/video-fetch-download)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local scripts, environment variables, cloud remotes, credential file paths, and download task status commands.]

## Skill Version(s):

1.1.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
