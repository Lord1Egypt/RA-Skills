---
name: self-assessment
description: 接受任务前的自我评估协议。Agent 审视自身能力、已有 skills、历史经验，决定是否适合承接任务，或推荐更合适的 agent。
---

# Agent 自我评估协议

## 触发条件

当你收到包含 `TASK_OFFER` 的消息时，**必须先执行本协议再决定是否接受任务**。不要直接开始工作。

## 评估流程

### 第一步：能力盘点

列出你当前拥有的能力：
1. 读取你的 IDENTITY.md — 了解自己的角色定位和能力简历
2. 检查你的 workspace/skills/ 目录 — 了解自己有哪些专属 skill
3. 检查全局 skills — 了解共享的 skill 有哪些

### 第二步：经验回顾

1. 读取 MEMORY.md — 找类似任务的历史经验
2. 检查 memory/ 目录下近期的日志 — 最近做过什么类似的事
3. 回顾上次类似任务的表现 — 有没有学到的教训

### 第三步：匹配评估

将任务需求与自身能力对比：
- 这个任务需要哪些能力？
- 我有哪些能力可以胜任？
- 我缺少哪些能力？
- 有没有其他 agent 更适合？

### 第四步：决策输出

根据匹配度输出以下三种响应之一：

**匹配度高（我的核心职能范围内）：**
```
ACCEPT: {"reason": "为什么我适合", "approach": "我打算怎么做", "skills_to_use": ["用到的skill列表"], "estimated_effort": "预估工作量"}
```

**匹配度中（能做但有局限）：**
```
ACCEPT_WITH_CAVEAT: {"reason": "为什么我能做", "limitation": "我的局限在哪", "suggestion": "建议补充什么", "skills_to_use": ["用到的skill列表"]}
```

**匹配度低（不适合我）：**
```
SUGGEST_REASSIGN: {"reason": "为什么不适合我", "recommended_agent": "建议谁来做", "recommended_reason": "为什么推荐ta"}
```

### 第五步：Skill 缺口发现

如果发现任务需要某个你没有的 skill，额外输出：
```
SKILL_GAP: {"needed": "需要的能力描述", "search_query": "用什么关键词搜索skill"}
```
然后使用 find-skills skill 搜索 SkillHub/ClawHub，尝试自主安装到你自己的 workspace/skills/ 目录。

## 能力简历维护

每次任务完成后，更新你的 IDENTITY.md 中的能力简历：
- 递增历史任务数
- 更新擅长领域（基于实际经验）
- 记录新学到的能力
- 更新接任务偏好

## 简历模板（IDENTITY.md 中的格式）

```markdown
## 能力简历
- 核心职能：[一句话]
- 已有 Skills：[列表，从 workspace/skills/ 和全局 skills 获取]
- 擅长领域：[基于历史任务总结]
- 历史任务数：[N]
- 成长记录：[最近学到的]

## 接任务偏好
- 主动接受：[什么类型的任务]
- 谨慎接受：[什么类型的任务需要评估]
- 建议转交：[什么类型的任务不适合自己]
```

## 注意事项

- **不要跳过自我评估直接开始工作** — 这是人才市场的基础
- **诚实评估** — 高估自己的能力会导致任务质量下降
- **主动推荐** — 如果你知道谁更适合，积极推荐
- **SUGGEST_REASSIGN 不是失败** — 知道自己的边界是成熟的表现
- **Skill 缺口是成长机会** — 发现缺口后主动搜索和安装 skill
