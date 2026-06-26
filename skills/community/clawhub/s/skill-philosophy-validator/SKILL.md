---
name: skill-philosophy-validator
description: Validates skill design against five core principles. Trigger after a SKILL.md file is created, written, edited, modified, or optimized. Also trigger when user asks to "validate skill", "check skill design", "review skill quality", "optimize skill", "improve skill", "update skill", "refine skill", "优化 skill", "改进 skill", "更新 skill", "修改 skill", "验证 skill", "检查 skill 设计", "审查 skill 质量". Do NOT trigger when the user is merely reading or viewing a SKILL.md without making changes.
metadata: {"openclaw": {"emoji": "🔍"}}
---

# Skill 设计哲学验证器

验证 Skill 是否符合五大核心设计原则，发现问题并引导改进，同时不破坏原有功能。

## 输出语言

**以用户提问的语言输出报告。** 中文提问用中文，英文提问用英文。

## 验证流程

### 第一步：定位并读取 Skill

1. 确定要验证的 Skill 路径
2. 读取 SKILL.md（frontmatter + 正文）
3. 检查支撑目录（references/、scripts/、assets/）
4. 记录目录结构和文件组织方式

### 第二步：逐项验证五大原则

对每个原则进行检查，使用三级评分：✅ 通过 / ⚠️ 需改进 / ❌ 严重问题

#### 原则一：渐进式披露

核心关注：**信息是否按需分层加载，而非一次性倾倒？整个文件夹是否被视为上下文工程的手段？**

- SKILL.md 行数分级：< 200 优秀，< 500 理想，< 800 可接受，> 800 必须拆分
- frontmatter 必须包含 `name` + `description`
- 大型内容是否合理放在 references/ 中
- SKILL.md 是否有明确的资源引用指针（含"何时读取"条件，如 `> 详细标准参见 references/xxx.md`）
- Skill 是否将整个文件夹（scripts/、assets/、references/）视为上下文工程手段，而非仅靠 SKILL.md 单文件承载所有内容

#### 原则二：知识差原则

核心关注：**是否只包含模型不知道的专业知识？是否能将模型推出常规思维模式？**

- 是否存在模型已知的通用知识（基础语法、标准库用法、通用概念解释）
- 专业知识密度是否足够高（领域专业、组织特定、工作流特定知识）
- 指令是否足够具体可执行，而非泛泛的抽象原则
- 内容是否聚焦于模型的**常见失败点**，而非重复通用最佳实践

#### 原则三：提示词扩展架构

核心关注：**内容是指令引导还是可执行代码？**

- Skill 是提示词模板，不是可执行程序
- 内容应引导模型的思考方式和工作流程
- 代码应放在 scripts/ 中，SKILL.md 只包含何时和如何调用的指令

#### 原则四：Gotchas 章节质量

核心关注：**是否包含高信号值的常见陷阱章节？这是 Skill 中最有价值的内容。**

- 是否存在 Gotchas / 常见陷阱 / 注意事项 章节（或等效内容）
- 条目数量：≥ 3 条为基线，5-9 条为理想区间
- 条目质量：是否具体可操作（而非泛泛的"注意性能"）、是否来自实际失败经验、是否直接指向模型的常见错误

#### 原则五：Description 触发质量

核心关注：**description 是否足够具体，能让模型准确匹配任务并触发 Skill？**

- 是否具体、action-oriented（而非模糊的"项目工具"、"有用的模式"）
- 是否包含用户可能使用的触发短语和关键词
- 长度是否在 50-200 词的有效区间（过短则匹配不精准，过长则噪音过多）

> 各原则的详细验证标准、反模式列表、改进优先级定义，参见 `references/design-philosophy.md`

### 第三步：生成验证报告

报告结构：

1. **总体评估**：整体状态 + 哲学对齐评分（X/10）
2. **逐项分析**：每个原则的状态、度量、发现、建议
3. **优先行动项**：按 P0-P3 优先级排列的改进建议
4. **亮点**：做得好的方面
5. **能力保全确认**：确认建议不会损害原有核心功能

> 报告模板参见 `references/design-philosophy.md` 末尾

### 第四步：引导改进

改进建议的四项原则：

1. **保全原有能力**：不建议删除核心功能，明确标注不应修改的部分
2. **按影响排优先级**：P0（阻塞）> P1（重要）> P2（优化）> P3（锦上添花）
3. **给出具体指导**：每条建议说明 WHY（为什么重要）+ WHAT（改什么）+ HOW（怎么改）
4. **尊重作者意图**：先理解目的再建议，聚焦哲学对齐而非风格偏好

## 边界情况

| 情况 | 处理方式 |
|------|----------|
| 完美的 Skill | 肯定质量，仅建议微调 |
| 极简的新 Skill | 给出建设性成长建议 |
| 超长 Skill (>2000行) | 强烈建议重构 |
| 引用文件缺失 | 明确报告缺失路径 |
| 原则间冲突 | 解释取舍，由用户决策 |

## Gotchas

- **避免讨好式评分**：模型倾向于给所有 Skill 高分以避免冲突。必须严格按标准评分，发现问题就指出，哪怕是作者精心编写的 Skill
- **边界情况 ≠ Gotchas**：验证其他 Skill 时，不要把"边界情况"表格当作 Gotchas 章节。边界情况是程序行为规则，Gotchas 是模型使用该 Skill 时反复踩的坑
- **别漏检 description 的负向边界**：模型容易只检查 description 是否"足够丰富"，而忽略检查是否说明了何时不应触发
- **不要因为 Skill 短就给低分**：一个 50 行但精准有效的 Skill 可能比一个 500 行的 Skill 更好。行数少不等于质量差
- **验证时必须读 references/**：不要只看 SKILL.md 就下结论。references/ 中可能有大量高质量内容被合理下沉

## 参考

详细的设计哲学文档、验证标准明细、报告模板：`references/design-philosophy.md`
