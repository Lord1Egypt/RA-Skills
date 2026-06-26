## Description: <br>
Download videos from Twitter/X posts. Just give it a tweet URL and it will download the video to your specified location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lemonpek66](https://clawhub.ai/user/Lemonpek66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to download Twitter/X videos or GIFs to local storage, with optional output folder, filename, quality, and proxy settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes yt-dlp and writes downloaded media to a local directory. <br>
Mitigation: Install yt-dlp from a trusted source, download only media you intend to save, and choose the output directory deliberately. <br>
Risk: Proxy configuration may be printed in logs when PROXY_URL is set. <br>
Mitigation: Do not include usernames, passwords, tokens, or other secrets in PROXY_URL. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lemonpek66/twitter-video-download) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime output is terminal text and downloaded media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python, pip, and yt-dlp. PROXY_URL is optional for users who need a proxy. Downloads are saved locally, typically as MP4 files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and release notes, released 2026-03-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
