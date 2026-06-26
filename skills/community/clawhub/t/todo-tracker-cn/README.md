# Todo Tracker - 待办事项管理技能

## 📋 技能简介

**待办事项管理神器！专为 AI 助手设计的任务追踪系统，让复杂任务的执行过程可视化。**

当你需要 AI 执行复杂任务时，是否经常遇到这些问题：
- ❌ AI 说"正在处理"，但不知道进展如何
- ❌ 等了很久问"怎么样了"，才得到回复
- ❌ AI 说"已完成"，但实际没有执行
- ❌ 多个步骤的任务，不知道完成了哪些

**Todo Tracker 就是为了解决这些问题而生！**

---

## ✨ 核心功能

### 1️⃣ 生成待办列表 (`generate-todo-list`)

根据任务描述自动生成结构化的待办清单，支持：
- ✅ 智能拆解任务为可执行的子步骤
- ✅ 为每个步骤分配唯一 ID
- ✅ 自动记录创建时间
- ✅ **立即展示完整待办列表**，让用户看到计划

**使用场景**：
- 配置复杂系统（如 Self-Improving）
- 排查和解决问题
- 开发和部署技能
- 任何包含 3 个以上步骤的任务

### 2️⃣ 标记完成 (`mark-completed`)

每完成一个步骤，立即标记为已完成：
- ✅ 记录完成时间
- ✅ 自动计算进度百分比
- ✅ **立即展示更新后的进度**
- ✅ 防止重复标记

**使用场景**：
- 执行任何实质性操作后
- 完成一个可验证的步骤后
- 需要向用户汇报进展时

### 3️⃣ 查看进度 (`show-progress`)

实时查看当前任务的执行进度：
- ✅ 清晰展示已完成项（✅）
- ✅ 清晰展示待完成项（⏳）
- ✅ 进度统计（X/Y 已完成）
- ✅ 支持随时查询

**使用场景**：
- 用户询问"怎么样了"
- 定期主动汇报进展
- 长任务（>2 分钟）的进度更新

### 4️⃣ 验证完成 (`verify-completion`)

任务结束前的最终验证：
- ✅ 检查是否所有步骤都已完成
- ✅ 如果有未完成项，列出清单
- ✅ 如果全部完成，输出总结
- ✅ 防止口头说"完成"但实际未执行

**使用场景**：
- 任务即将结束时
- 用户要求验证完成情况
- 需要输出执行总结时

---

## 🚀 使用示例

### 示例 1：配置 Self-Improving 系统

**用户**：帮我配置 Self-Improving 系统

**AI 执行流程**：

```bash
# 1. 创建待办列表
python3 todo_tracker.py generate-todo-list "配置 Self-Improving 系统"
```

**输出**：
```
📋 **待办列表：配置 Self-Improving 系统**
进度：0/5

⏳ 待完成：
  - [step1] 创建 corrections.md
  - [step2] 创建 memory.md
  - [step3] 创建 heartbeat-state.md
  - [step4] 配置每日自省定时任务
  - [step5] 配置每周反思定时任务
```

```bash
# 2. 执行步骤 1 后标记
python3 todo_tracker.py mark-completed "step1"
```

**输出**：
```
✅ 已完成：创建 corrections.md

📋 **待办列表：配置 Self-Improving 系统**
进度：1/5

✅ 已完成：
  - 创建 corrections.md

⏳ 待完成：
  - [step2] 创建 memory.md
  - [step3] 创建 heartbeat-state.md
  - [step4] 配置每日自省定时任务
  - [step5] 配置每周反思定时任务
```

```bash
# 3. 所有步骤完成后验证
python3 todo_tracker.py verify-completion
```

**输出**：
```
🎉 所有待办项已完成！任务执行完毕。

总结：
- 创建了 3 个文件（corrections.md, memory.md, heartbeat-state.md）
- 配置了 2 个定时任务（每日自省 22:00，每周反思 周六 20:00）
- Git 提交：62f5161
```

---

### 示例 2：排查小红书发布失败

**用户**：排查小红书中午自动发布失败

**AI 执行流程**：

```bash
# 1. 创建待办列表
python3 todo_tracker.py generate-todo-list "排查小红书中午自动发布失败"
```

**输出**：
```
📋 **待办列表：排查小红书中午自动发布失败**
进度：0/3

⏳ 待完成：
  - [step1] 查看日志文件
  - [step2] 分析问题原因
  - [step3] 修复并测试
```

```bash
# 2. 查看日志后标记
python3 todo_tracker.py mark-completed "step1"
```

**输出**：
```
✅ 已完成：查看日志文件

📋 **待办列表：排查小红书中午自动发布失败**
进度：1/3

✅ 已完成：
  - 查看日志文件

⏳ 待完成：
  - [step2] 分析问题原因
  - [step3] 修复并测试
```

```bash
# 3. 分析原因后标记
python3 todo_tracker.py mark-completed "step2"
```

**输出**：
```
✅ 已完成：分析问题原因

📋 **待办列表：排查小红书中午自动发布失败**
进度：2/3

✅ 已完成：
  - 查看日志文件
  - 分析问题原因

⏳ 待完成：
  - [step3] 修复并测试
```

**根因**：`ModuleNotFoundError: No module named 'requests'`

```bash
# 4. 修复后验证
python3 todo_tracker.py mark-completed "step3"
python3 todo_tracker.py verify-completion
```

**输出**：
```
🎉 所有待办项已完成！任务执行完毕。

总结：
- 问题根因：缺少 requests 模块
- 解决方案：pip3 install requests
- 补发成功：Post ID 已生成
```

---

## 📊 技术细节

### 数据存储

**存储位置**：`~/.openclaw/workspace/todo-current.json`

**数据结构**：
```json
{
  "id": "todo_20260326141113",
  "title": "排查小红书中午自动发布失败",
  "createdAt": "2026-03-26T14:11:13.780226",
  "items": [
    {
      "id": "feed1f00",
      "description": "步骤 1: 查看日志文件",
      "status": "completed",
      "createdAt": "2026-03-26T14:11:13.780211",
      "completedAt": "2026-03-26T14:11:29.901937"
    }
  ]
}
```

### 记忆集成

任务完成后自动归档到 `MEMORY.md`：
```markdown
## 待办任务 [todo_20260326141113]
- 创建时间：2026-03-26T14:11:13
- 任务：排查小红书中午自动发布失败
- 状态：3/3 已完成
```

---

## 🎯 最佳实践

### ✅ 推荐做法

1. **复杂任务必用**
   - 3 个以上步骤的任务
   - 预计执行时间 >5 分钟
   - 配置修改、文件创建、技能开发

2. **立即展示进度**
   - 创建待办后立即展示
   - 每完成一步立即展示
   - 主动汇报，不要等用户问

3. **定期汇报**
   - 短任务（<2 分钟）：完成后汇报
   - 中任务（2-5 分钟）：每 50% 汇报
   - 长任务（>5 分钟）：每 1 分钟汇报

4. **结束前验证**
   - 必须调用 `verify-completion`
   - 有未完成项要说明
   - 输出执行总结

### ❌ 禁止行为

1. **不要**等用户问"怎么样了"才汇报
2. **不要**说"已完成"但实际没有执行
3. **不要**跳过 `verify-completion` 直接说完成
4. **不要**为每个步骤创建独立的待办列表

---

## 🔧 命令行用法

```bash
# 生成待办列表
python3 todo_tracker.py generate-todo-list "任务描述"

# 标记完成
python3 todo_tracker.py mark-completed "todo_id"

# 查看进度
python3 todo_tracker.py show-progress

# 验证完成
python3 todo_tracker.py verify-completion
```

---

## 📝 更新日志

### v1.0.0 (2026-03-26)
- ✅ 初始版本发布
- ✅ 支持生成待办列表
- ✅ 支持标记完成
- ✅ 支持查看进度
- ✅ 支持验证完成
- ✅ 自动展示进度（无需手动查询）
- ✅ 集成 Self-Improving 系统

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**项目地址**：https://github.com/openclaw/openclaw

---

## 📄 许可证

MIT License

---

## 💡 设计灵感

这个技能的设计灵感来自于 AI 助手执行任务时的常见问题：
- 用户看不到执行过程，只能等待结果
- AI 容易"口头承诺"但实际未执行
- 复杂任务缺乏结构化管理

Todo Tracker 通过**可视化的待办列表**和**强制的进度展示**，让 AI 的执行过程透明化，建立用户对 AI 的信任。

---

*最后更新：2026-03-26*
