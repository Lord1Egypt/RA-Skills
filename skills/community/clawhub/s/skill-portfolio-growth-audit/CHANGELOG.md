# Changelog

## 1.0.2

- 新增 `evidenceQuality.decisionReady`、同采集方法、两次 `activeInstall: false`、至少 7 天观察窗口的决策闸门
- 要求搜索 query 文本、`limit` 和完整 query set 一致后才能比较可见性
- 更新作品集报告模板，逐项记录闸门结果；未就绪时只允许继续观察或修复数据质量

## 1.0.1

- 将 frontmatter `name` 统一为人类可读展示名 `Skill Portfolio Growth Audit`
- 新增稳定 `slug: skill-portfolio-growth-audit`，避免展示名变化影响 registry 标识
- 同步更新页面主标题，强化系列产品的一致性

## 1.0.0

- 创建 `skill-portfolio-growth-audit` 的首个可发布版本
- 强制使用 ClawHub registry 指标、搜索结果和仓库证据
- 用 `加码 / 修复 / 合并 / 观察 / 停更 / 新建` 管理作品集决策
- 增加观察窗口、竞争审查和证据边界规则
