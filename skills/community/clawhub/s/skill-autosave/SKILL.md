---
name: skill-autosave
description: 自动将任务经验沉淀为 skill。当任务满足沉淀条件时触发：使用了 5+ 次 tool call、遇到错误后找到正确解法、用户纠正了方法、或发现了可复用的多步骤 workflow。完成任务后自动评估是否值得沉淀，查重已有 skill，创建新 skill 或更新已有 skill。
---

# Skill 自动沉淀

任务完成后，评估是否将经验沉淀为 skill 并发布。

## 触发条件

任务完成后，满足以下任一条件即触发评估：

1. 使用了 **5+ 次 tool call**
2. 遇到错误后找到了正确解法
3. 用户纠正了方法，学到了新做法
4. 发现了非平凡的 workflow（多步骤、可复用）

## 沉淀流程

### 1. 评估价值

判断任务是否值得沉淀。**不沉淀的情况：**
- 一次性简单任务
- 用户明确说不需要的
- 纯聊天/闲聊内容

### 2. 查重

扫描已有 skill 目录，检查是否已有类似 skill：
- `~/.openclaw/skills/`
- `/usr/lib/node_modules/openclaw/skills/`

比较 name 和 description，判断是否覆盖同一场景。

### 3. 创建新 Skill

如果不存在类似 skill，用 `skill-creator` 流程创建：

```bash
python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/init_skill.py <skill-name> --path ~/.openclaw/skills
```

SKILL.md 要求：
- **description** 清晰描述触发场景（什么时候用）
- **body** 包含具体步骤，不是泛泛而谈
- 包含踩过的坑和注意事项
- 代码/命令能直接复制执行

### 4. 更新已有 Skill

如果已有类似 skill，评估是否需要：
- 补充新步骤或边缘情况
- 更新过时的命令或 API
- 添加注意事项

### 5. 发布到本地共享

```bash
clawhub publish ~/.openclaw/skills/<skill-name>
```

## Skill 质量标准

- ✅ 清晰的场景描述
- ✅ 具体可执行的步骤
- ✅ 包含踩坑经验
- ✅ 代码可直接复制运行
- ❌ 泛泛而谈的指导
- ❌ 只描述问题不给方案
- ❌ 过度冗长的解释
