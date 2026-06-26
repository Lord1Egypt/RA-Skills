## Description: <br>
Download videos, audio, subtitles, and covers from Bilibili using bilibili-api. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate guidance, commands, configuration, and Python examples for downloading Bilibili videos, playlists, audio, subtitles, covers, and related metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bilibili SESSDATA cookies can expose account access if pasted into shared chats, committed, logged, or stored in shell history. <br>
Mitigation: Treat SESSDATA like a password, keep it out of shared prompts and repositories, and prefer short-lived local environment variables or private configuration. <br>
Risk: The skill depends on bilibili-api-python and uses it to fetch Bilibili content. <br>
Mitigation: Install the dependency only from a trusted package source and use the skill only when you intend to download Bilibili content. <br>
Risk: Video and playlist downloads can write large files or overwrite expected output locations. <br>
Mitigation: Use a dedicated output directory and check existing files and available storage before running video or playlist downloads. <br>


## Reference(s): <br>
- [Bilibili API Reference Guide](references/quick_guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Sunshine-del-ux/sunshine-bilibili-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local helper scripts and configuration templates for Bilibili download workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
