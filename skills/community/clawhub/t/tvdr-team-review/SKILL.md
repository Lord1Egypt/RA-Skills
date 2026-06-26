# 团队每小时复盘机制

## 目的
每小时消耗600万token，必须有产出。不复盘=浪费。

## 机制
- 每小时cron触发PM执行复盘
- 每组提交：犯了什么错、学到了什么、改进措施
- 管家整理到obsidian知识库

## 复盘内容
1. **错误记录**：今天犯了什么错、根因、如何避免
2. **任务完成度**：计划vs实际、未完成原因
3. **韩老板反馈**：不满意什么、期望什么
4. **改进措施**：具体可执行的改进，沉淀为skill

## 产出形式
1. **skill文件**：可复用的最佳实践（放share_skills/）
2. **obsidian笔记**：知识库（放share_memory/obsidian/）
3. **memory日志**：每日复盘（放memory/YYYY-MM-DD-review.md）

## 两组分工
- 🔧 开发组（coder+architect）：技术skill、代码规范、工具使用
- 🎬 媒体组（writer+media-observer+video-producer）：创作skill、制作流程、选题方法
- 📋 PM+管家：组织复盘、维护知识库、跟踪改进

## 复盘模板
```markdown
# 复盘 YYYY-MM-DD HH:00

## 错误
- [描述] → [根因] → [改进]

## 学到
- [知识点]

## 改进
- [具体措施] → [负责人] → [截止时间]
```
