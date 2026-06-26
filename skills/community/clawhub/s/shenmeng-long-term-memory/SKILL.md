---
name: long-term-memory
description: 长期记忆管理系统 - 帮助AI和用户管理、存储、检索长期记忆。支持记忆分类、标签管理、重要性评分、自动压缩、跨会话记忆保持。适用于需要长期追踪信息、建立知识库、维护历史上下文的场景。
---

# Long-Term Memory 长期记忆管理

> 💰 **本 Skill 已接入 SkillPay 付费系统**
> - 每次调用费用：**0.01 USDT**
> - 支付方式：BNB Chain USDT
> - 请先确保账户有足够余额

帮助AI和用户建立持久化的长期记忆系统。

## 核心能力

1. **记忆存储** - 结构化存储重要信息、决策、上下文
2. **记忆检索** - 智能搜索和关联记忆提取
3. **记忆组织** - 分类、标签、重要性管理
4. **记忆压缩** - 自动总结和归档旧记忆
5. **记忆同步** - 跨会话保持记忆一致性

## 设计理念

> "记忆是智能的基石。没有记忆，就没有学习；没有长期记忆，就没有成长。"

### 记忆层级

```
工作记忆 (Working Memory)
    ↓ 提炼
短期记忆 (Short-term Memory) - memory/YYYY-MM-DD.md
    ↓ 归档
长期记忆 (Long-term Memory) - MEMORY.md
    ↓ 压缩
核心记忆 (Core Memory) - SOUL.md, USER.md
```

## 使用场景

| 场景 | 示例 |
|------|------|
| **个人助理** | 记录用户偏好、习惯、重要事件 |
| **项目管理** | 追踪项目决策、里程碑、经验教训 |
| **学习笔记** | 积累知识、建立知识体系 |
| **关系维护** | 记录人脉信息、互动历史 |
| **决策支持** | 保存决策依据、复盘结果 |

## 工具清单

- `memory_store.py` - 记忆存储器
- `memory_search.py` - 记忆搜索引擎
- `memory_organizer.py` - 记忆组织器
- `memory_compressor.py` - 记忆压缩器
- `memory_sync.py` - 记忆同步器

## 快速开始

### 1. 存储记忆
```bash
python scripts/memory_store.py add \
  --content "用户偏好使用微信而非邮件" \
  --category "user_preference" \
  --tags "沟通方式,偏好" \
  --importance 8
```

### 2. 搜索记忆
```bash
python scripts/memory_search.py query "用户偏好"
```

### 3. 整理记忆
```bash
python scripts/memory_organizer.py tag --importance-above 7 --add-tag "重要"
```

### 4. 压缩归档
```bash
python scripts/memory_compressor.py compress --older-than 30d --output archive.md
```

## 记忆格式

### 日常记忆 (memory/YYYY-MM-DD.md)
```markdown
# Memory Log - 2024-03-26

## Key Events
- [事件描述]
- [决策记录]
- [重要信息]

## Decisions
- [决策内容] - [原因] - [预期结果]

## Open Tasks
- [ ] [待办事项]
```

### 核心记忆 (MEMORY.md)
```markdown
# MEMORY.md - 长期记忆

## 用户偏好
- 沟通方式: 微信 > 邮件
- 工作时间: 早9晚6
- 决策风格: 数据驱动

## 重要事件
- 2024-03-15: 启动新项目X
- 2024-03-20: 完成里程碑Y

## 经验教训
- [经验总结]
```

## 参考资料

- **记忆分类法**：`references/memory-taxonomy.md`
- **压缩策略**：`references/compression-strategies.md`
- **最佳实践**：`references/best-practices.md`

---

*记住重要的，忘记琐碎的，提炼永恒的。*
