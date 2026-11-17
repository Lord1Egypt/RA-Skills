## Description:

把一个 agent skill 发布到公开渠道并尽可能被人发现。覆盖 repo 布局改造、frontmatter 要件、clawhub 提交、skills.sh 遥测触发、索引验证、搜索曝光优化。用户要说「发布这个 skill」「上架」「让人能搜到」「publish to clawhub/skills.sh」时用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapleleo-hub](https://clawhub.ai/user/mapleleo-hub)

### License/Terms of Use:

MIT

## Use Case:

面向开发者：整理并发布 agent skill 到 ClawHub、skills.sh 等公开渠道，并验证目录索引、搜索曝光和下载状态。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 安装步骤建议清空 DISABLE_TELEMETRY/DO_NOT_TRACK，可能覆盖用户的遥测退出设置。

Mitigation: 保留已有退出设置；只有用户明确同意后，才运行会产生遥测的安装操作。

Risk: 排障段落建议使用 Remove-Item -Recurse -Force，可能绕过删除安全拦截。

Mitigation: 先核对目标路径并采用可恢复的清理方式，不要绕过安全拦截。

Risk: 发布指令使用未固定版本的 npx 工具，且扫描器指出一个脚本的分析不完整。

Mitigation: 运行前审阅脚本并核验工具版本；对行为尚未确认的脚本先不执行。

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mapleleo-hub/skills/ship-skill)
- [Distribution channels](references/channels.md)
- [Pitfalls](references/pitfalls.md)
- [Release status check script](scripts/check.mjs)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline shell and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
