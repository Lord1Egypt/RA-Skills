# Changelog

## v1.1.0 (2026-08-18) — checkbox 进展追踪工作流

### 🎯 核心功能
- **split_weekly.js `formatDailyPlan()` 输出 checkbox 格式**
  - 任务头：`1、` → `### 1.`（与周计划一致）
  - 子步骤：增加 `- [ ]` checkbox（用户手动勾选）
  - 标签格式保留：`  - [ ] 子步骤 \`#动作 #时间标签\``

- **copy_next_week_plan.js 新增 2 个工具函数 + 1 步集成**
  - `extractCompletedSubSteps(weekStart)`：从本周 5 个 daily plan 提取所有 `- [x]` 项
  - `mergeCompletedIntoProgress(weekContent, completed)`：合并到周计划"已推进"（fingerprint 去重）
  - `5-pre` 步骤：周五 15:00 cron 内集成（在复制到下周计划之前）

- **用户拍板：严格 action tag 匹配**
  - 提取时只匹配动作类型库（执行型/文档型/临时型）
  - 不在库的不算 action（用户之前手动加的 `#进展` 等会被忽略）
  - 合并时如果 action 不在库就不输出 `` `#xxx` ``

### 🐛 Bug 修复
- ✅ 任务标题格式 `1、` → `### 1.`（与周计划一致，方便 extractCompletedSubSteps 匹配）
- ✅ checkedRegex 允许行首空格 `- [x]` 匹配（修复 用户之前手动合并行不匹配的 bug）
- ✅ 全局正则漏掉任务 14 的 bug（任务块后跟 `## 约束段` 而非下一个 `### N.`，改用 `split(/(?=### )/)` 替代 lookahead）
- ✅ mergeCompletedIntoProgress 改用任务块隔离替换（避免 indexOf 漂移和跨任务污染）

### 📚 文档更新
- SKILL.md 加 "## ⚙️ checkbox 进展追踪工作流（v1.1.0 新增）" 章节
  - 完整工作流图
  - 4 个关键实现说明
  - 5 个已知 bug 修复记录
  - 隐私清理清单

### ✅ 验证
- 6 个场景封闭测试通过（正常提取 / 去重 / 空输入 / 跨任务 / 空任务 / 多格式）
- 真实 用户 4 项勾选场景验证通过（任务1 × 2 + 任务10 × 1 + 任务14 × 1）
- 修复后任务14 "大学科技园公司拟来访...` #沟通 `" 正确合并（之前全局正则漏掉）

