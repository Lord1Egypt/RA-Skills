# Changelog

## 2.0.0

- 展示名从 Skill Publish Readiness 更新为 ClawHub Skill Launch Review，保留 `skill-publish-readiness` slug
- 合并 `skill-launch-checklist` 的快速上线检查能力，统一由 `skill-publish-readiness` 提供
- 新增 `auto` 选择器与 `quick` / `deep` 双模式；定义自动升级条件与输出契约
- 整版重写报告模板，加入模式信息、quick 闸门、deep 证据矩阵、P0/P1/P2 与验收项
- 重写成熟候选与问题候选示例，演示模式选择、升级和证据边界
- 明确与 `skill-positioning-audit` 的 Storefront Copy Brief 及 `skill-summary-rewriter` 的交接关系

## 1.0.9

- 安全审查补充真实发布事故教训：Python 字节码/缓存（`*.pyc`、`__pycache__`）进包会被 A.I.G 扫描器拒收（CVE-2026-84809），发布前需删除并加 `.clawhubignore`
- 安全审查补充敏感配置脱敏（代理/URL 剥 userinfo 再打印或落盘）与外部输入路径白名单校验（防路径穿越）
- `security_review_guide.md` 风险分级与「审查时要回答的问题」同步扩展

## 1.0.8

- 所有 Skill 发布命令显式传递稳定 `--slug` 与人类可读 `--name`
- 发布审查报告按 Skill / Plugin 分支输出下一步命令
- Plugin 分支使用 `package validate` 与 `package publish --dry-run`，不再套用 Skill 参数

## 1.0.7

- 新增基于真实 GitHub Actions → ClawHub 发布事故整理的复合失败审查案例
- 覆盖受保护 slug、`pending-publication` 误判和上传票据瞬时失效
- 将发布报告模板升级为证据矩阵，补充问题优先级、修复后验收和证据边界
- 在主文档加入 `Built from real publish failures`，强化产品可信度与差异化

## 1.0.6

- 将 frontmatter `name` 统一为人类可读展示名 `Skill Publish Readiness`
- 新增稳定 `slug: skill-publish-readiness`，避免展示名变化影响 registry 标识
- 同步更新页面主标题，强化系列产品的一致性

## 1.0.1

- 将商店页摘要改为中英混合短描述，首屏更快说明它解决什么问题
- 补充 `emoji`，提高在目录和安装页里的识别度
- 为 `skill-publish-readiness` 增加目录级 catalog metadata
- 自动发布时同步写入 `categories` 和 `topics`，避免技能继续落在 `Other`
- 为后续 skill 预留 `.clawhub/skill-catalog.json` 作为统一元数据入口

## 1.0.0

- 创建 `clawhub-publish-assistant-pro` 的首个可发布版本
- 增加面向 ClawHub 发布前的五类检查：
  - 文件完整性
  - 版本与一致性
  - 代码与环境
  - 安全与审核风险
  - 同类 skill 差异化
- 增加真实使用示例与典型失败案例
- 增加差异化评分规则
- 增加配套参考文件、示例文件与输出模板
