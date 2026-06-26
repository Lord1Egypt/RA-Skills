## Description: <br>
Convert bookmarked videos from YouTube, X, and other supported sites into a podcast RSS feed hosted on Cloudflare R2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryandeathridge](https://clawhub.ai/user/ryandeathridge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn saved or bookmarked video URLs into podcast episodes, maintain a local episode list, and publish the generated audio files and RSS feed to Cloudflare R2. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use browser login cookies when downloading protected videos. <br>
Mitigation: Set VIDPOD_COOKIE_BROWSER=none unless cookie-backed downloads are intentional, and review each add or sync action before it runs. <br>
Risk: Cloud storage credentials are stored in a plaintext local env file. <br>
Mitigation: Scope the R2 token to one bucket, grant only required permissions, and restrict file permissions on ~/.openclaw/.env. <br>
Risk: The skill publishes generated podcast audio and feed data to a public R2 endpoint. <br>
Mitigation: Install only when public podcast publishing is intended and review source URLs before adding or syncing episodes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryandeathridge/video2podcast) <br>
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp) <br>
- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) <br>
- [Cloudflare](https://cloudflare.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown or plain text with command output, feed URLs, and generated podcast artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local state, MP3 audio objects, and feed.xml when configured with Cloudflare R2 credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
