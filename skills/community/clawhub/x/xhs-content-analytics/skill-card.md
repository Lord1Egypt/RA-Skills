## Description: <br>
小红书自动化运营工具，支持搜索笔记、查看笔记详情及评论，用于小红书、Xiaohongshu 或 RedNote 内容调研。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[um-why](https://clawhub.ai/user/um-why) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, marketers, and analysts use this skill to search public Xiaohongshu notes, inspect note details and comments, compare engagement metrics, and export results for content planning or marketing reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Keywords, note URLs, and GUAIKEI_API_TOKEN are sent to the guaikei.com API. <br>
Mitigation: Use the skill only when that third-party API use is acceptable, and keep the token in a protected environment variable. <br>
Risk: Generated log files may contain sensitive content research records. <br>
Mitigation: Review, protect, and delete local logs when they are no longer needed, especially on shared or backed-up machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/um-why/xhs-content-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text with JSON or Markdown result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; writes local JSON logs under the skill logs directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
