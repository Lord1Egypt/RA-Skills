## Description: <br>
Download videos from YouTube, Bilibili, Twitter, and thousands of other sites using yt-dlp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apollo1234](https://clawhub.ai/user/apollo1234) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent prepare or run yt-dlp commands for downloading videos, extracting MP3 audio, downloading subtitles, selecting quality, and troubleshooting common download errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use browser login cookies for video downloads, which can expose authenticated session access to the agent and external sites. <br>
Mitigation: Try downloads without cookies first; allow browser-cookie use only when explicitly intended, preferably with a dedicated browser profile or limited-scope cookie file. <br>
Risk: The skill proposes shell commands with network access and writes downloaded files locally. <br>
Mitigation: Review each command, destination path, and source URL before execution, and run downloads only in directories where created files are expected. <br>


## Reference(s): <br>
- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create downloaded media files in a local output directory when commands are executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
