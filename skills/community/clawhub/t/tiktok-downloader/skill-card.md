## Description: <br>
Download TikTok videos by URL or hashtag with support for browser cookies, user-agent rotation, batch downloads, and guidance for 403 errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kgc-yj](https://clawhub.ai/user/kgc-yj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to download individual TikTok videos or batches of TikTok URLs for offline review or archiving when they are authorized to access the content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a local Chromium browser profile that may contain a logged-in TikTok session. <br>
Mitigation: Use a dedicated browser profile or exported cookie file, and confirm consent before using browser cookies. <br>
Risk: The downloader accepts user-provided URLs and writes media files to disk. <br>
Mitigation: Verify each URL is a TikTok URL and choose an explicit output folder before running downloads. <br>
Risk: The workflow depends on yt-dlp and scripted downloads that may fail or trigger rate limits. <br>
Mitigation: Install yt-dlp from a trusted source, review commands before execution, and use pacing for large batches. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kgc-yj/tiktok-downloader) <br>
- [TikTok](https://www.tiktok.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands and a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create downloaded video files in a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
