# 技能减法检查报告

**检查时间**：2026-08-12
**技能总数**：8 个（用户级 8 个，项目级 0 个）
**扫描平台**：WorkBuddy（6 个）+ 工作区 Github（2 个）
**报告模式**：详细检查报告

## 建议保留（3 个）

| 技能 | 所在 Agent | 类型 | 细分领域 | 保留理由 | 使用频率 | 综合评分 |
|------|-----------|------|---------|---------|---------|---------|
| skill-subtraction | WorkBuddy | 元技能类 | 技能检查与管理 | 不可替代的技能检查能力，今天刚完成双语升级，当前正在使用 | 高（每天） | 100 |
| generate-html-ppt | WorkBuddy / Github 项目级 | 内容与多媒体类 | HTML/PPT 演示文稿生成 | HTML 演示文稿生成，今天有修改记录，与当前工作方向直接匹配 | 高（每天） | 88 |
| follow-builders | WorkBuddy | 数据与集成类 | SaaS 与 API 连接器 | AI builder 内容聚合，今天有修改记录，与用户 AI 关注方向匹配 | 高（每周） | 88 |

## 建议归档（4 个）

| 技能 | 所在 Agent | 类型 | 细分领域 | 归档理由 | 重新激活条件 | 综合评分 |
|------|-----------|------|---------|---------|------------|---------|
| aihot | WorkBuddy | 数据与集成类 | 知识检索与 RAG | 使用频率低，WebSearch 可部分替代 AI 新闻获取；通过 API 获取精选资讯有一定独特性但不常用 | 需要批量获取精选 AI 资讯时 | 63 |
| competitor-analysis | WorkBuddy | 专业业务类 | 营销与竞品 | 使用频率低，当前无活跃竞品分析项目；标准化框架有保留价值 | 启动竞品分析项目时 | 63 |
| github-ai-trends | WorkBuddy | 数据与集成类 | SaaS 与 API 连接器 | 使用频率低，与 follow-builders 功能部分重叠；GitHub trending 可通过 WebSearch 替代 | 需要系统化 GitHub 趋势报告时 | 63 |
| weekly-report | WorkBuddy | 生产力类 | 周报与会议纪要 | 已禁用（`disable_model_invocation=true`），但 8 月 11 日有修改记录，可能偶尔手动调用；归档优于卸载 | 恢复每周写周报习惯时 | 57 |

## 已归档技能库（0 个）

本次详细检查已扫描归档库，当前无已归档技能。归档记录不计入已安装技能总数，也不参与建议评分。

## 卸载（1 个）

| 技能 | 所在 Agent | 类型 | 细分领域 | 卸载理由 | 风险评估 | 综合评分 |
|------|-----------|------|---------|---------|---------|---------|
| ecom-customer-service | WorkBuddy | 专业业务类 | 客服与运营 | 已禁用且从未手动调用（特殊规则：禁用+从未调用→直接卸载）；当前无电商客服业务；`disable_model_invocation=true` | 低风险：技能由 Agent 创建（`agent_created=true`），可随时重新创建；归档 SKILL.md 后卸载更安全 | 31 |

## 评分明细

| 技能 | 所在 Agent | 使用频率(25) | 必要性(20) | 相关性(20) | 启用状态(15) | 维护(10) | 独特价值(10) | 总分 |
|------|-----------|-------------|-----------|-----------|-------------|---------|-------------|------|
| skill-subtraction | WorkBuddy | 25 高 | 20 不可替代 | 20 匹配 | 15 已启用 | 10 活跃 | 10 独有 | **100** |
| generate-html-ppt | WorkBuddy / Github 项目级 | 25 高 | 12 有替代 | 20 匹配 | 15 已启用 | 10 活跃 | 6 部分独有 | **88** |
| follow-builders | WorkBuddy | 25 高 | 12 有替代 | 20 匹配 | 15 已启用 | 10 活跃 | 6 部分独有 | **88** |
| aihot | WorkBuddy | 8 低 | 12 有替代 | 12 部分匹配 | 15 已启用 | 10 活跃 | 6 部分独有 | **63** |
| competitor-analysis | WorkBuddy | 8 低 | 12 有替代 | 12 部分匹配 | 15 已启用 | 10 活跃 | 6 部分独有 | **63** |
| github-ai-trends | WorkBuddy | 8 低 | 12 有替代 | 12 部分匹配 | 15 已启用 | 10 活跃 | 6 部分独有 | **63** |
| weekly-report | WorkBuddy | 8 低 | 12 有替代 | 12 部分匹配 | 9 禁用但近期修改 | 10 活跃 | 6 部分独有 | **57** |
| ecom-customer-service | WorkBuddy | 4 零 | 4 可有可无 | 4 不相关 | 3 禁用从未调用 | 10 活跃 | 6 部分独有 | **31** |

## 汇总建议

- **当前技能集健康度**：中
- **主要问题**：8 个技能中有 2 个已禁用（ecom-customer-service、weekly-report），其中 ecom-customer-service 完全闲置建议卸载；aihot 和 github-ai-trends 功能部分重叠且使用频率低，建议至少归档其中一个
- **去重建议**：aihot（AI 资讯）与 github-ai-trends（GitHub AI 趋势）功能有重叠，follow-builders 也可覆盖部分 AI 动态。三个资讯类技能建议只保留 follow-builders，其余归档
- **下次检查建议时间**：2026 年 11 月（每季度）

---

*本报告由 skill-subtraction v1.2.0 自动生成*
