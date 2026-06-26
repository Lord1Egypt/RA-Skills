## Description: <br>
自动发布视频到中国三大平台（B站、抖音、小红书） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huanghonggit](https://clawhub.ai/user/huanghonggit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators can use this skill to automate uploading a selected or latest local video to Bilibili, Douyin, and Xiaohongshu with title, description, tags, platform selection, and browser-based posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use saved session cookies to access creator accounts and perform live posts. <br>
Mitigation: Run it only for accounts prepared for publishing, review the video metadata and selected platforms before execution, and protect or delete the cookies directory after use. <br>
Risk: Browser automation and anti-detection behavior may violate platform rules or fail when platform pages change. <br>
Mitigation: Confirm platform terms before use, test with non-critical accounts or drafts where possible, and review logs and resulting platform pages after each run. <br>
Risk: Automatically generated title, description, and tags may be unsuitable for a specific video. <br>
Mitigation: Pass explicit title, description, and tags for each run when accuracy or brand fit matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huanghonggit/video-auto-publisher-cn) <br>
- [Publisher profile](https://clawhub.ai/user/huanghonggit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Command-line arguments plus log and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create cookie JSON files, timestamped logs, and diagnostic screenshots during browser automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
