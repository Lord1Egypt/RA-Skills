# Self-Improving Agent v2.0 - 自我进化智能体

## 🎯 技能描述

**自我反思 + 自我学习 + 自我改进** 的 AI 代理系统。

基于 Anthropic 的自我进化理念，结合记忆管理系统，实现：
- 🔄 每日自动反思（3 次/天）
- 💾 对话记录全量保存
- 📚 长期记忆自动整理
- 🚀 持续学习和改进

---

## ✨ 核心功能

### 1️⃣ 每日自动反思（3 次）

| 时间 | 内容 | 说明 |
|------|------|------|
| **09:00** | 早晨反思 | 回顾昨天，规划今天 |
| **14:00** | 下午反思 | 上午复盘，调整下午 |
| **21:00** | 晚上反思 | 全天总结，整理记忆 |

**反思模板：**
```markdown
## 🤔 反思 - [时间]

### 1. 做得好的
- [具体事项]

### 2. 可以改进的
- [错误/不足]

### 3. 学到的新东西
- [新知识/认知]

### 4. 用户偏好更新
- [新偏好/需求变化]

### 5. 后续行动
- [待办事项]
```

---

### 2️⃣ 对话记录保存

**保存策略：**

| 内容类型 | 保存方式 | 清理策略 |
|---------|---------|---------|
| **文字对话** | 全量保存 | ✅ 永久保存 |
| **图片** | 保存 | ✅ 永久保存 |
| **重要决策** | 提取到 MEMORY.md | ✅ 永久保存 |
| **代码/脚本** | 全量保存 | ✅ 永久保存 |
| **视频** | 临时保存 | 🔄 月清理 |
| **大型文件** | 临时保存 | 🔄 月清理 |

**保存位置：**
```
📂 workspace/
├── MEMORY.md              # 长期记忆（精华，永久）
├── memory/
│   ├── YYYY-MM-DD.md      # 每日记忆（永久）
│   └── ...
└── media/
    ├── images/            # 图片（永久）
    └── videos/            # 视频（月清理）
```

---

### 3️⃣ MEMORY.md 整理

**整理频率：**
- 📅 每天小整理（21:00 反思时）
- 📅 每周大整理（周日晚）
- 📅 每月深度整理（月末）

**整理内容：**
```
✅ 应该存入的：
- 重要决策
- 用户偏好
- 长期目标
- 关键人脉/资源
- 核心技能/能力

❌ 不应存入的：
- 临时待办
- 日常闲聊
- 已完成的琐事
- 过时的信息
```

---

## 🔧 技术实现

### 系统架构：

```
self-improving/
├── SKILL.md               # 技能说明
├── scripts/
│   ├── memory_manager.py  # 记忆管理主脚本
│   ├── daily_reflection.py # 每日反思
│   ├── save_conversation.py # 对话保存
│   └── organize_memory.py  # 记忆整理
├── cron/
│   └── reflection_jobs.json # 定时任务配置
└── tests/
    └── test_memory.py     # 测试脚本
```

### Cron 定时任务：

```json
{
  "jobs": [
    {
      "name": "记忆反思 - 早晨 09:00",
      "schedule": "0 9 * * *",
      "action": "daily_reflection morning"
    },
    {
      "name": "记忆反思 - 下午 14:00",
      "schedule": "0 14 * * *",
      "action": "daily_reflection afternoon"
    },
    {
      "name": "记忆反思 - 晚上 21:00",
      "schedule": "0 21 * * *",
      "action": "daily_reflection evening + organize"
    }
  ]
}
```

---

## 📋 使用方法

### 安装：
```bash
clawhub install self-improving
```

### 配置：
```bash
# 启用定时任务
openclaw cron add self-improving-reflection

# 查看任务状态
openclaw cron list
```

### 手动使用：
```bash
# 保存对话
python scripts/memory_manager.py save "主题" "要点 1" "要点 2"

# 手动反思
python scripts/memory_manager.py reflect [morning|afternoon|evening]

# 整理记忆
python scripts/memory_manager.py organize
```

---

## 🆚 v1.0 vs v2.0 更新说明

### v1.0 功能：
- ❌ 仅基础反思功能
- ❌ 手动触发
- ❌ 无记忆管理
- ❌ 无定时任务

### v2.0 新增：
- ✅ 每日自动反思 3 次（Cron 定时）
- ✅ 对话记录全量保存
- ✅ 图片和文字永久保存
- ✅ 视频等大型文件月清理
- ✅ MEMORY.md 自动整理
- ✅ 完整的记忆管理系统
- ✅ 自动提取关键信息
- ✅ 用户偏好追踪

### 核心改动：

| 模块 | v1.0 | v2.0 | 改进 |
|------|------|------|------|
| **反思频率** | 手动 | 自动 3 次/天 | ⬆️ 自动化 |
| **对话保存** | ❌ | ✅ 全量 | ⬆️ 完整性 |
| **图片保存** | ❌ | ✅ 永久 | ⬆️ 新能力 |
| **视频清理** | ❌ | ✅ 月清理 | ⬆️ 空间管理 |
| **记忆整理** | ❌ | ✅ 自动 | ⬆️ 智能化 |
| **Cron 任务** | ❌ | ✅ 3 个定时 | ⬆️ 自动化 |

---

## 📊 记忆存储策略

### 永久保存（不清理）：
```
✅ 所有文字对话
✅ 所有图片
✅ 重要决策
✅ 用户偏好
✅ 代码/脚本
✅ MEMORY.md
✅ memory/YYYY-MM-DD.md
```

### 月度清理：
```
🔄 视频文件（>30 天）
🔄 大型附件（>30 天）
🔄 临时文件（>30 天）
```

### 清理脚本：
```python
# 每月 1 号自动执行
def monthly_cleanup():
    # 清理>30 天的视频
    cleanup_videos(older_than=30)
    # 清理>30 天的大型文件
    cleanup_large_files(older_than=30)
    # 保留所有文字和图片
    preserve_text_and_images()
```

---

## 🎯 最佳实践

### 1. 每日反思
- 定时任务触发时认真填写
- 具体记录做得好和不好的
- 更新用户偏好和需求

### 2. 对话保存
- 重要对话后自动保存
- 提取 3-5 个关键要点
- 记录决策和待办

### 3. 记忆整理
- 每周日回顾本周记忆
- 提取精华到 MEMORY.md
- 删除过时信息

---

## 🚀 发布说明

### 发布到 ClawHub：
```bash
clawhub publish self-improving --version 2.0.0
```

### 发布到 GitHub：
```bash
git add .
git commit -m "feat: v2.0 - 完整的自我进化系统"
git tag v2.0.0
git push origin main --tags
```

### 更新日志：
```markdown
## [2.0.0] - 2026-03-20

### Added
- 每日自动反思 3 次（09:00/14:00/21:00）
- 对话记录全量保存
- 图片永久保存
- 视频月清理机制
- MEMORY.md 自动整理
- Cron 定时任务系统

### Changed
- 反思从手动改为自动
- 记忆从临时改为永久（文字/图片）
- 清理策略优化

### Improved
- 自动化程度提升
- 记忆管理更智能
- 空间管理更合理
```

---

## 📄 许可证

MIT License

---

## 👥 贡献

欢迎提交 Issue 和 PR！

---

*版本：2.0.0*
*最后更新：2026-03-20*
*作者：Jarvis*
