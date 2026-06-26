## Description: <br>
Download videos, torrents, magnet links, and Quark shares to 115 Pan, Quark Pan, or rclone-compatible cloud storage using bundled shell and Python tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[graysonzeng](https://clawhub.ai/user/graysonzeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search for video or torrent resources, submit supported offline-download tasks, and move downloaded media into cloud storage accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer and runtime commands can install packages, edit user shell PATH configuration, stage media under /tmp, and store cloud account credentials locally. <br>
Mitigation: Review the installer before execution, run it in a dedicated or isolated environment where practical, and verify cloud destinations before starting downloads. <br>
Risk: The skill stores powerful rclone tokens and a Quark browser cookie on disk for cloud account access. <br>
Mitigation: Protect the local configuration files, use dedicated cloud accounts where possible, and rotate or revoke exposed tokens or cookies promptly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/graysonzeng/video-fetch-download) <br>
- [rclone 115 setup guide](references/rclone-setup.md) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [rclone 115 fork](https://github.com/gaoyb7/rclone-release) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create local staging files, update user shell PATH configuration, and write local cloud-storage credentials.] <br>

## Skill Version(s): <br>
1.1.9 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
