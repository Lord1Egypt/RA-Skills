## Description: <br>
YouTube 批量视频发布工具，支持自动上传、元数据设置、缩略图上传等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fly3094](https://clawhub.ai/user/fly3094) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations teams use this skill to automate YouTube video uploads with titles, descriptions, tags, categories, privacy settings, thumbnails, progress reporting, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish videos to the selected YouTube account. <br>
Mitigation: Install and run it only for accounts where uploads are intended, and verify the target account, title, metadata, category, and privacy setting before each upload. <br>
Risk: The skill stores a reusable local OAuth token after authorization. <br>
Mitigation: Protect or delete credentials/token.pickle after use, and revoke Google app access when the tool is no longer needed. <br>
Risk: The bundled OAuth credentials file is a placeholder and must not be treated as production credentials. <br>
Mitigation: Replace it with a Google Cloud OAuth client controlled by the operator before use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/fly3094/youtube-bulk-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/fly3094) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, Python snippets, and JSON-style upload results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses YouTube OAuth credentials and can return video IDs, video URLs, upload status, and error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
