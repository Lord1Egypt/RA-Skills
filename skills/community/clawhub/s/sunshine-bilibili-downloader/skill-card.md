## Description:

Download videos, audio, subtitles, covers, and playlists from Bilibili with bilibili-api-python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate commands, code snippets, and configuration for downloading Bilibili media, choosing quality levels, exporting subtitles, and using authenticated downloads when required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles BILIBILI_SESSDATA session cookies for authenticated content.

Mitigation: Treat session cookies like passwords, keep them out of source code and tracked config files, and prefer environment variables or secret storage.

Risk: Downloaded filenames can be influenced by remote Bilibili video titles.

Mitigation: Download into a dedicated directory and review generated filenames, especially on Windows or shared systems.

Risk: The skill depends on bilibili-api-python and writes downloaded media to disk.

Mitigation: Use a virtual environment, pin and review dependencies, and ensure the output directory has enough disk space before large downloads.

## Reference(s):

- [Quick Guide](references/quick_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/sunshine-del-ux/skills/sunshine-bilibili-downloader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Python, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require bilibili-api-python, ffmpeg, Bilibili content identifiers, and optional BILIBILI_SESSDATA for authenticated content.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
