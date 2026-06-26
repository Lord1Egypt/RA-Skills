## Description: <br>
B站视频弹幕提取工具，输入B站视频链接或BV号后提取弹幕并导出为JSON和Markdown文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unclecheng-li](https://clawhub.ai/user/unclecheng-li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract danmaku from a Bilibili video for local review, archiving, or downstream analysis. It accepts a Bilibili URL or BV identifier and saves time-ordered exports with video metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Bilibili public APIs for each provided video. <br>
Mitigation: Use it only when network access to Bilibili is acceptable for the video being processed. <br>
Risk: Extracted danmaku is stored locally and may include user-generated content. <br>
Mitigation: Write exports to a dedicated output folder and review sharing decisions against platform rules and privacy expectations. <br>
Risk: Aggressive bulk extraction may trigger platform rate limits or risk controls. <br>
Mitigation: Run extraction at a controlled pace and retry later if Bilibili returns access or rate-limit errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unclecheng-li/unclecheng-bilibili-danmaku-extractor) <br>
- [Publisher profile](https://clawhub.ai/user/unclecheng-li) <br>
- [Bilibili video info API](https://api.bilibili.com/x/web-interface/view?bvid={bvid}) <br>
- [Bilibili danmaku API](https://api.bilibili.com/x/v1/dm/list.so?oid={cid}) <br>
- [Bilibili](https://www.bilibili.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files, Markdown files] <br>
**Output Format:** [JSON and Markdown files, with conversational guidance and shell command examples when used by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes extracted danmaku, timestamps, display type, color, send timestamp, and video metadata to a user-selected local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _skillhub_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
