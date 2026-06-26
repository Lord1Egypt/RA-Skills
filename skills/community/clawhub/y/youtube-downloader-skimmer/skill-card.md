## Description: <br>
Downloads YouTube videos and clips key segments based on chapters or custom time ranges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bg1avd](https://clawhub.ai/user/bg1avd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and content operators use this skill to download public YouTube media, split it into chapter-based or manually defined clips, and save MP4 or MP3 outputs for downstream handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and processes media from YouTube URLs and writes the resulting files locally. <br>
Mitigation: Use a dedicated output directory and review downloaded or clipped files before relying on or sharing them. <br>
Risk: Raw downloaded videos may be deleted after clipping when cleanup is enabled. <br>
Mitigation: Disable raw-file deletion or preserve a separate copy when the original download must be retained. <br>
Risk: The release advertises QQ or Telegram delivery, but the reviewed behavior only prepares and lists clip paths for downstream handling. <br>
Mitigation: Treat messaging-platform delivery as a manual or separately integrated step and verify files before sending them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bg1avd/youtube-downloader-skimmer) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Local media files with console status text and command-line options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces clipped MP4 or MP3 files in a local output directory; raw downloads may be deleted when cleanup is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
