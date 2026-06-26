## Description: <br>
下载微信公众号文章（mp.weixin.qq.com）中的视频、音频和音乐卡片，适配微信验证拦截场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ewanwu](https://clawhub.ai/user/ewanwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to capture and download video, audio, and music cards from WeChat public-account articles when the user is authorized to access and save the media. It is especially suited to Chinese WeChat article workflows that require visible Chrome verification, media URL capture, title extraction, and organized local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill attaches to a verified local Chrome session through the debugging port. <br>
Mitigation: Use a fresh temporary Chrome profile, keep the debugging port bound locally, and close Chrome when capture is finished. <br>
Risk: Captured page HTML, text, JSON, and downloaded media may contain sensitive or copyrighted content. <br>
Mitigation: Use the skill only when authorized to save the target media, store outputs in a controlled directory, and delete intermediate capture files after review. <br>
Risk: Audio URLs may only appear after a user plays each audio item in the browser. <br>
Mitigation: Have the user manually play missing audio items and rerun capture before downloading or packaging final outputs. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/ewanwu/wechat-media-downloader-weixin) <br>
- [GitHub README reference](references/github-readme-zh.md) <br>
- [Publish notes](references/publish-notes-zh.md) <br>
- [Reusable workflow](references/reusable-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce temporary HTML, text, JSON capture files, a download manifest, and organized local media files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
