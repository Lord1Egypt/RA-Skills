## Description: <br>
推特视频下载器 downloads Twitter/X videos, GIFs, and audio as MP4 or MP3, supports multiple quality levels, batch download, media info lookup, and proxy use for restricted networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harbour015](https://clawhub.ai/user/harbour015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to save public Twitter/X media, extract audio, inspect media metadata, or batch download multiple public post URLs through yt-dlp and ffmpeg. Users in network-restricted regions can provide a local proxy when permitted by local rules and platform terms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads public internet media and writes files to local directories. <br>
Mitigation: Use it only for public content you are allowed to save, and choose an output directory you are comfortable writing to. <br>
Risk: The skill accepts proxy URLs for network access, which may expose credentials if usernames or passwords are embedded in command-line arguments. <br>
Mitigation: Avoid putting proxy usernames or passwords in command-line proxy URLs and prefer trusted local proxy configurations. <br>
Risk: The skill depends on yt-dlp and ffmpeg to fetch and process media. <br>
Mitigation: Install yt-dlp and ffmpeg only from trusted package managers or official sources before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harbour015/twitter-video-downloader) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local file output from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads media files to local output directories and can emit video metadata as terminal text.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
