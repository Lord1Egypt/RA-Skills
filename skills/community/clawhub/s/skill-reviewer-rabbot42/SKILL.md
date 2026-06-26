---
name: skill-reviewer
description: "审查和评估 OpenClaw Skill 的质量，提供改进建议"
metadata: { "openclaw": { "emoji": "🔍" } }
---

# Skill 质量审查器

审查一个 Skill 的质量，判断其是否是个好 Skill。

## When to Use

✅ **USE this skill when:**

- 用户想审查某个 Skill 的质量
- 评估一个 Skill 是否需要改进
- 检查 Skill 是否符合最佳实践
- 给 Skill 打分或提出改进建议

❌ **DON'T use this skill when:**

- 用户只是询问某个 Skill 的使用方法
- 需要直接修改某个 Skill（只负责审查，不负责修改）
- 与 Skill 开发无关的一般性问题

---

## 什么是好的 Skill

### 1. 描述精准
- ✅ 清晰说明能做什么
- ❌ 避免太宽泛（如"查东西"、"GitHub 相关"）

### 2. 场景边界清晰
- 有 **When to Use**（什么时候用）
- 有 **When NOT to Use**（什么时候不用）

### 3. 命令具体可执行
- 有可直接运行的命令示例
- ❌ 不能只有概念，没有具体实现

### 4. 专注一件事
- 一次只做一件事，窄而深
- ❌ 避免瑞士军刀式的大杂烩

---

## 审查清单

给目标 Skill 逐项检查：

| 检查项 | 权重 | 说明 |
|--------|------|------|
| Header 完整 | ⭐⭐⭐ | 包含 name, description, metadata |
| description 精准 | ⭐⭐⭐⭐⭐ | 不模糊，不宽泛 |
| 有明确 Use Cases | ⭐⭐⭐⭐ | 有 When to Use 说明 |
| 有具体命令示例 | ⭐⭐⭐⭐⭐ | 可直接复制运行 |
| 有注意事项 | ⭐⭐⭐ | 包含 limitations, requirements |
| 专注一件事 | ⭐⭐⭐⭐ | 不做"大杂烩" |

---

## 评分标准

| 等级 | 分数 | 评价 |
|------|------|------|
| 优秀 | 90-100 | 可直接使用，无需修改 |
| 良好 | 70-89 | 不错，稍作优化更佳 |
| 一般 | 50-69 | 需要较大改进 |
| 较差 | <50 | 建议重新设计 |

---

## 注意事项

- ⚠️ 审查结果仅供参考，最终判断需人工决定
- ⚠️ 只负责审查，不自动修改目标 Skill
- ⚠️ 需要先读取目标 SKILL.md 才能审查（无法审查不存在的文件）
- 💡 建议结合具体使用场景灵活应用

---

## 实际示例

### 审查步骤

1. **读取目标 Skill 的 SKILL.md**
   ```bash
   # 假设要审查 weather skill
   cat ~/.openclaw/skills/weather/SKILL.md
   # 或
   cat /opt/homebrew/lib/node_modules/openclaw/skills/weather/SKILL.md
   ```

2. **逐项对照审查清单检查**

3. **输出审查结果**（见下方模板）

### 示例输出

```
## 审查结果：weather skill

### 得分：95/100 (优秀)

### 优点
- Header 完整，包含 emoji
- description 精准，不模糊
- 有完整的 When to Use / When NOT to Use
- 命令示例丰富且可直接运行
- 包含注意事项（rate limit）

### 问题
- 无明显问题

### 改进建议
- 可考虑添加更多城市的格式示例
```

---

## 输出格式

审查完成后，输出：

```
## 审查结果：[Skill 名称]

### 得分：X/100 (等级)

### 优点
- ...

### 问题
- ...

### 改进建议
1. ...
2. ...
```

---

## 使用方法

当需要审查某个 Skill 的质量时：
1. 读取该 Skill 的 SKILL.md 文件
2. 根据上述清单逐项检查
3. 输出审查结果和改进建议
