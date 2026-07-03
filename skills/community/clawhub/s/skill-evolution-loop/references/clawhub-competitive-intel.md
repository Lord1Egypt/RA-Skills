# ClawHub Workflow类竞品分析（2026-06-10）

## 排名（9维评分）

| 排名 | 技能 | 总分 | 下载量 | 行数 |
|------|------|------|--------|------|
| 🏆 1 | hermes-workflow-engine (v3.0.2) | 9.8 | 0 | 548 |
| 2 | n8n-workflow-automation | 5.9 | 33 | 95 |
| 3 | workflow | 4.0 | 3 | 97 |
| 4 | automation-workflow-builder | 3.8 | 3 | 131 |
| 5 | auto-workflow | 3.7 | 4 | 48 |
| 6 | coze-workflow | 2.7 | 988 | 109 |
| 7 | agentic-workflow-automation | 2.7 | 10 | 28 |
| 8 | structured-workflow | 2.0 | 1 | 24 |

## 关键发现

**质量 vs 下载量完全倒挂：**
- coze-workflow 2.7分但988下载（Coze生态自带流量）
- n8n 5.9分33下载（n8n品牌效应）
- 我们9.8分0下载（刚发布，无推广）

**竞品弱点：**
- 大部分无 triggers 字段（trigger_coverage 0分）
- 大部分无降级策略（fallback 0分）
- 描述普遍很短或缺失

**市场饱和度：**
- 搜索 "workflow" 返回 25+ 结果
- 搜索 "automation" 返回 10+ 结果
- 名字高度同质化，用户选择困难

## 提升下载量建议

1. 改名突出差异化（如 `hermes-dag-orchestrator`）
2. 绑定具体场景（如 "AI新闻自动化工作流"）
3. 在社区/Discord/Reddit推广
4. 发 GitHub Release 带 zip 包

## ClawHub 数据查询方法

- **Star数：** 浏览器访问技能页，JS提取按钮文字 `button.textContent.includes('Star')` → 后面的数字
- **下载量：** 侧边栏 `<dt>Downloads</dt><dd>` 元素的值
- **CLI无star命令，无公开API**
