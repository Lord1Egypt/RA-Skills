## Description:

Resolve and download WeChat Channels / Weixin video share links directly using the online sph resolver and curl, without a local install or local proxy startup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imchao9](https://clawhub.ai/user/imchao9)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to resolve WeChat Channels share links and download accessible videos to a local Downloads folder. It is scoped to direct share-link or direct media URL downloads and excludes proxy, certificate, injection, sudo, and access-control bypass workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat share links are sent to a documented third-party resolver service before download.

Mitigation: Use the skill only for links you are comfortable disclosing to that resolver, and avoid sensitive or private share links.

Risk: The optional filename influences the path written under ~/Downloads.

Mitigation: Use a simple sanitized filename such as video.mp4 and review the output path before relying on the downloaded file.

Risk: Resolved media URLs and downloaded content may not match user expectations or usage rights.

Mitigation: Use only content the user is allowed to access and download, and review the resolved output before redistribution or reuse.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imchao9/skills/wx-channels-download)
- [Share Link Download Commands](artifact/references/commands.md)
- [Online sph resolver endpoint](https://sph.litao.workers.dev/api/fetch_video_profile)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown with inline bash commands and local downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads resolved media to ~/Downloads and may print author, title, quality, output path, and completion status.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
