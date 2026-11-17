## Description:

Guides agents through user-assisted browser capture and download of segmented streaming video, followed by MP4 merging and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sedey999](https://clawhub.ai/user/sedey999)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users download streaming videos they are authorized to save, including videos requiring the user to complete login or verification in a visible browser. The skill guides stream capture, segmented downloads, MP4 merging, playback checks, and cleanup after user acceptance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser login state can persist and expose streaming-site sessions.

Mitigation: Use a dedicated browser profile; do not point CHROME_PROFILE at an everyday browser profile.

Risk: Plaintext cookies and password diagnostic files can remain in the work directory.

Mitigation: Delete work-directory cookie and password diagnostic files after use.

Risk: Downloading restricted videos may exceed the user's authorization.

Mitigation: Download only content the user is authorized to save.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sedey999/skills/video-downloader-by-browser)
- [Youku platform guide](references/youku.md)
- [Tencent Video platform guide](references/tencent.md)
- [iQIYI platform guide](references/iqiyi.md)
- [Bilibili platform guide](references/bilibili.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflow produces an MP4 file and temporary segments; cleanup follows user acceptance.]

## Skill Version(s):

1.3.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
