## Description: <br>
检测小红书笔记限流状态。通过创作者后台 API 获取所有笔记的 level 字段，判断限流等级、敏感词命中、标签风险。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swaylq](https://clawhub.ai/user/swaylq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to inspect Xiaohongshu creator notes for distribution level, sensitive-word hits, excessive tag counts, and throttling indicators. It can summarize results as a human-readable report or structured JSON for further agent processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to exported Xiaohongshu creator-session cookies. <br>
Mitigation: Use a cookie file scoped to creator.xiaohongshu.com, store it privately, and do not commit or share it. <br>
Risk: Generated JSON or Markdown reports may contain sensitive account and content-performance data. <br>
Mitigation: Treat reports as private account data and avoid writing them to shared locations. <br>
Risk: The reported note health levels depend on Xiaohongshu creator API fields and may change if the service changes its response shape. <br>
Mitigation: Review output for unexpected empty results or authentication errors and refresh cookies only from the official creator site when needed. <br>


## Reference(s): <br>
- [xhs-note-health ClawHub listing](https://clawhub.ai/swaylq/xhs-note-health) <br>
- [Xiaohongshu creator note manager](https://creator.xiaohongshu.com/new/note-manager) <br>
- [xhs-note-health-checker reference](https://github.com/jzOcb/xhs-note-health-checker) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown report or JSON from a Python CLI, with agent-facing summary guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a report file when an output path is provided.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
