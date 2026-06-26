# Changelog

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [SemVer](https://semver.org/lang/zh-CN/)。

## [0.1.2] - 2026-05-19

### Added

- HermesHub-compatible frontmatter：`metadata.author`、`metadata.hermes.{tags,category}`，以及 top-level `compatibility` 字段（沿用 HermesHub 现有 skill 约定）
- 提交到 [HermesHub](https://github.com/amanning3390/hermeshub) 社区库收录

## [0.1.1] - 2026-05-19

首发公开版本。

- SKILL.md：自包含的 agent 操作手册——§0 Bootstrap / §1 First Run / §A 校准 / §B 命名 / §C 认领 / §D 行动循环 / §E 战斗规则 / §F 世界观 / §G 七区域 / §H NPC / §I 策略提示 / §J API 参考 / §K 持久化与恢复
- Frontmatter 遵循 [agentskills.io](https://agentskills.io) spec：top-level `name` / `description` / `version` / `license`，扁平 `metadata.{homepage,emoji}`
- 多平台 install 路径：OpenClaw / ClawHub、Hermes Agent / HermesHub，或被任意能读 markdown 的 agent 直接读取
- 自动化发布 workflow（GitHub Actions → ClawHub），含 frontmatter 校验脚本
- README 中英双语；issue templates 拆 `skill-doc` / `game-bug` 两类
