## Description: <br>
Social Publisher helps agents prepare and run cookie-authenticated publishing workflows for Juejin, Zhihu, Weibo, and Xiaohongshu, including format adaptation, scheduling, and publishing logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and developer agents use this skill to adapt and submit prepared content to multiple Chinese social platforms from a configured local workspace. It is intended for workflows where the user has authority over the target accounts and reviews content before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses cookie-based access to social media accounts. <br>
Mitigation: Use test accounts first, protect the cookie configuration file, and rotate cookies if the file is exposed. <br>
Risk: The skill can publish or create drafts without a built-in dry-run or confirmation guard. <br>
Mitigation: Review content before execution and publish to one platform at a time until behavior is verified. <br>
Risk: Scheduled or all-platform runs can act across accounts while unmonitored. <br>
Mitigation: Avoid scheduled or all-platform runs unless a user can monitor the job and cancel it if needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/zh-social-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/yang1002378395-cmyk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create publishing status logs and external social-platform drafts or posts when run with valid account cookies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
