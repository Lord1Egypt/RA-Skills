## Description: <br>
Automatically downloads user-provided videos from Bilibili, Douyin, TikTok, YouTube, and other yt-dlp-supported sites to local storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangxiangyu8516](https://clawhub.ai/user/zhangxiangyu8516) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent download videos they explicitly provide from supported platforms and return saved file details for local use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Supported video links can trigger local downloads and consume disk space, especially for large videos or playlists. <br>
Mitigation: Install only where automatic local downloads are desired, monitor the downloads directory, and avoid bulk or playlist downloads unless intended. <br>
Risk: The skill relies on yt-dlp and may inherit risk from an untrusted or outdated local installation. <br>
Mitigation: Install yt-dlp from a trusted source and keep it updated through the selected package manager. <br>
Risk: Browser-cookie based downloads may use authenticated account access when enabled by the user. <br>
Mitigation: Use cookie options only for accounts and content the user is authorized to access, and avoid sharing exported cookie files. <br>


## Reference(s): <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance, shell commands, and JSON status from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save video files and metadata JSON to a local downloads directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
