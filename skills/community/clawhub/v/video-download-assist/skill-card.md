## Description:

Downloads videos from Bilibili, Douyin, TikTok, YouTube, and other supported video sites when a user provides a link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxiangyu8516](https://clawhub.ai/user/zhangxiangyu8516)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent download videos from user-provided Bilibili, Douyin, TikTok, YouTube, or other yt-dlp-supported links into local storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads remote videos to local storage, which can consume disk space or bring untrusted media files into the workspace.

Mitigation: Run it in an isolated workspace, set an explicit output directory, and review downloaded files before sharing or reusing them.

Risk: The documentation includes a privileged sudo curl install path for yt-dlp.

Mitigation: Prefer package-manager installation or an isolated Python environment, and verify binaries before granting executable permissions.

Risk: Browser-cookie download options can expose sensitive login sessions.

Mitigation: Avoid browser-cookie options unless necessary, use least-privilege accounts, and remove exported cookies after use.

Risk: Downloading videos may violate copyright or platform terms if used without permission.

Mitigation: Download only user-authorized content and follow the applicable platform rules and rights restrictions.

## Reference(s):

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API)
- [ClawHub skill page](https://clawhub.ai/zhangxiangyu8516/skills/video-download-assist)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON status output from the bundled downloader script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create downloaded media files and yt-dlp metadata JSON in local storage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
