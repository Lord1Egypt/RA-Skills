## Description: <br>
Parses Douyin share links or video-page URLs into downloadable video links, titles, and descriptions, with options to download locally or upload the video to Feishu Drive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuaner](https://clawhub.ai/user/kuaner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to turn Douyin share links or video-page URLs into downloadable metadata and either save video locally or upload it to an authorized Feishu Drive folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu Drive upload authority can expose workspace data or allow unwanted uploads if credentials or folder permissions are too broad. <br>
Mitigation: Provide app secrets and access tokens only through a secure runtime secret mechanism, grant the minimum Feishu Drive scopes and folder permissions needed for upload, and do not store secrets in TOOLS.md, chat, shell history, or source-controlled files. <br>
Risk: Downloading and uploading Douyin content can create policy or rights issues if the user is not authorized to move that content into Feishu. <br>
Mitigation: Confirm that the user is allowed to download the source video and upload it into the target Feishu workspace before running the workflow. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/kuaner/save-douyin-video-to-feishu-drive/tree/main/skills/save-douyin-video-to-feishu-drive) <br>
- [ClawHub skill page](https://clawhub.ai/kuaner/skills/save-douyin-video-to-feishu-drive) <br>
- [Feishu folder permission documentation](https://open.feishu.cn/document/faq/trouble-shooting/how-to-add-permissions-to-app) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe expected fields such as feishu_url, title, desc, video_urls, or download_path depending on the chosen workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
