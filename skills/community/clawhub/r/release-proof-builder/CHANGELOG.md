# Changelog

## 1.0.3

- 收紧 E2：仅目标发布 workflow 完成且成功时成立
- 收紧 E3：registry 元数据正确且 `moderation.verdict` 为 `clean` 时成立
- E4 新增主动安装污染记录与自然观察起点重建要求
- 同步更新证据等级、核验命令、冲突示例和报告模板

## 1.0.2

- 将 frontmatter `name` 统一为人类可读展示名 `Release Proof Builder`
- 新增稳定 `slug: release-proof-builder`，避免展示名变化影响 registry 标识
- 同步更新页面主标题，强化系列产品的一致性

## 1.0.0

- 创建 `release-proof-builder` 的首个可发布版本
- 用 `E0-E4` 区分本地、GitHub、流水线、registry 和安装证据
- 增加证据冲突示例、核验命令参考和发布证据报告模板
