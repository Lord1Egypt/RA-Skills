# skill-upgrade-checker

## 中文介绍

`skill-upgrade-checker` 是一个技能升级检查与执行技能，通过 **ClawHub** 比对已安装技能与注册表最新版本，解读变更日志，评估升级风险，并在用户确认后执行一键升级。

**ClawHub 常用命令：**

| 操作 | 命令 |
|---|---|
| 查看已安装 | `clawhub list` |
| 搜索技能 | `clawhub search <关键词>` |
| 更新技能 | `clawhub update <技能>` |

核心能力：

- 清点所有已安装技能及其本地版本
- 与 ClawHub 注册表进行语义版本比较
- 解读变更日志，识别新增/变更/修复/破坏性变更
- 多维风险评估（版本跳跃、破坏性关键词、依赖影响、版本滞后、采用度）
- 用户确认后执行升级，Major 升级强制逐个确认

适用场景：

- "我的技能有没有新版本？"
- "升级这个技能安全吗？有什么变化？"
- "一键升级所有低风险技能"
- "哪些技能版本落后了？"

---

## English Overview

`skill-upgrade-checker` is an upgrade detection and execution skill — it compares installed skills against the latest **ClawHub** registry versions, interprets changelogs, assesses upgrade risk, and executes one-click upgrades after explicit user confirmation.

**ClawHub CLI commands:**

| Action | Command |
|---|---|
| List installed | `clawhub list` |
| Search skills | `clawhub search <keywords>` |
| Update a skill | `clawhub update <skill>` |

Key capabilities:

- Inventory all installed skills with their local versions
- Semver comparison against ClawHub registry
- Changelog interpretation — identify additions, changes, fixes, and breaking changes
- Multi-dimensional risk assessment (version jump, breaking keywords, dependency impact, staleness, adoption)
- Execute upgrades after user confirmation; major upgrades require individual approval

Typical use cases:

- "Do any of my skills have updates available?"
- "Is it safe to upgrade this skill? What changed?"
- "Upgrade all low-risk skills at once"
- "Which skills are falling behind on versions?"

---

## Author

VinceZ.辉 (<https://x.com/zhaowh3613>)
