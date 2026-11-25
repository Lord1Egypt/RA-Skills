## Description:

WorkBuddy 换电脑/迁移/备份/恢复场景的总入口。当用户说"换电脑了""迁移 WorkBuddy""把 WorkBuddy 搬到新电脑""备份我的技能和会话""新电脑怎么恢复""migration""迁移包"等任何涉及把本机 WorkBuddy 全部内容搬到另一台电脑的请求时使用。覆盖打包（旧电脑）与还原（新电脑）两个方向，含自动探测、一键生成、一键恢复、断点重跑与覆盖度对账。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要更换电脑或备份、恢复 WorkBuddy 的个人用户，指导其先试运行并核对收集范围，再生成迁移包并在新电脑恢复配置、项目与本地数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 完整迁移范围可能收集无关或含凭据的文件，且静态分析覆盖不完整。

Mitigation: 先查看 DryRun 清单和恢复内容，仅选所需范围并保留现有备份；迁移包通过移动硬盘直拷，勿上传公有网盘、微信或邮件。

Risk: 恢复可能与新电脑现有数据冲突；以管理员权限运行或绕过执行策略会扩大影响。

Mitigation: 先备份目标数据并确认脚本内容和目标路径；除非已理解原因，否则不要使用管理员权限或绕过执行策略。

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oracis/skills/workbuddy-migration)
- [WorkBuddy 数据落盘全景图](artifact/references/migration-layout.md)
- [迁移排障手册](artifact/references/troubleshooting.md)
- [WorkBuddy 一键迁移使用说明](artifact/references/user-guide.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions]

**Output Format:** [迁移包文件夹、Markdown 操作指引与 PowerShell/CMD 命令]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows 迁移包；文件内容取决于所选范围。]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
