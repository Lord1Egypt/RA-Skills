## Description: <br>
微信搜一搜实时搜索工具，支持获取微信生态中的文章、视频和图片搜索数据；当前 artifact 实现了关键词视频搜索。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[um-why](https://clawhub.ai/user/um-why) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to search WeChat content by keyword, especially for real-time video results, market monitoring, competitor analysis, and content planning. It requires a GUAIKEI_API_TOKEN and Node.js runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords are sent to guaikei.com using the configured GUAIKEI_API_TOKEN. <br>
Mitigation: Use only with keywords appropriate to share with the service, protect the token, and rotate it if exposed. <br>
Risk: Successful search results are saved locally under the skill's logs directory. <br>
Mitigation: Review generated log files and manage retention according to the user's data-handling requirements. <br>
Risk: The release description mentions article, video, and image search, while the current artifact implements video search. <br>
Mitigation: Treat this version as a video-search tool unless additional article or image modes are separately verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/um-why/wechat-sou) <br>
- [Guaikei service site](https://www.guaikei.com) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files] <br>
**Output Format:** [JSON object printed to stdout and saved as a local JSON log file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include status, keyword, limit, total count, timestamp, runtime metadata, and result records when the upstream service returns matches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
