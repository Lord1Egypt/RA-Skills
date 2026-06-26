## Description: <br>
Downloads public social-media videos from supported URLs via yt-dlp when the user clearly asks to save or grab the video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elony-7](https://clawhub.ai/user/elony-7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill when a user has clear intent to download a public video from a supported social-media link. The skill checks metadata, downloads the video to temporary local storage, and returns the file path for delivery to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download media from public social platforms, which may be inappropriate if the user lacks rights to save or share the content. <br>
Mitigation: Use it only for public videos the user clearly intends to download and has rights to save or share. <br>
Risk: The skill depends on local yt-dlp and optionally ffmpeg, so installation source and runtime environment affect trust. <br>
Mitigation: Install dependencies from a trusted package manager or in an isolated Python environment before use. <br>
Risk: Network downloads can expose the agent host to unsafe URLs or internal-network targeting. <br>
Mitigation: Keep the artifact's URL allowlist, private-IP blocking, shell metacharacter validation, and subprocess argument isolation in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elony-7/social-video-downloader) <br>
- [Setup instructions](artifact/SETUP.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Console status text and local video file path for agent delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local yt-dlp; ffmpeg is recommended; private or restricted content is expected to fail.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
