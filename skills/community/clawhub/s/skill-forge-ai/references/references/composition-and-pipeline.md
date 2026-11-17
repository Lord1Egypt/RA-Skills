# Composition & Pipeline Orchestration (元技能组合与管线编排)

Complete methodology for Step 0.4 meta-skill composition suggestions in skill-forge v5.1.

**When to read**: When Step 0.4 pre-check finds that the user's need can be decomposed into multiple existing Skills, or when a multi-step pipeline is more efficient than creating a new monolithic Skill.

---

## Core Principle

**Before creating a new Skill, check if the need can be met by combining existing high-quality Skills.**

Many "I want a Skill that does X" requests are actually multi-step workflows:
- "把会议录音转成行动项" = 音频转文字 + 纪要提取 + 行动项生成
- "把网页文章转成公众号排版" = 网页提取 + 内容增强 + 排版
- "把PDF转成知识卡片" = PDF提取 + 内容归纳 + 卡片生成

If each step already has a high-quality Skill, composing them is better than building a monolithic new one.

---

## Decomposition Method

### Step 1: Break down the user's need into atomic operations

```
用户需求: "把会议录音转成结构化行动项"

分解:
  ① 音频 → 文字 (转写)
  ② 文字 → 会议纪要 (提取要点)
  ③ 纪要 → 行动项 (提取行动项+负责人+截止)
```

### Step 2: Search each atomic operation on SkillHub

For each step, use TRAE built-in tools (Grep/WebSearch) to search SkillHub for matching skills

### Step 3: Evaluate each step's coverage

| Step | SkillHub Top Skill | Quality Score | Coverage |
|------|-------------------|---------------|----------|
| ① | audio-to-text-pro | 8.5/10 | 完全覆盖 |
| ② | meeting-summary-extractor | 7.2/10 | 完全覆盖 |
| ③ | action-item-generator | 4.1/10 | 质量一般，有差距 |

### Step 4: Composition Decision

| Pattern | Condition | Recommendation |
|---------|-----------|----------------|
| **全组合** | 所有步骤都有高质量Skill(≥7) | "你的需求已有现成Skill组合，建议安装+编排管线，无需新建" |
| **部分组合+部分新建** | 部分步骤高质量，部分质量一般或缺失 | "建议安装已有的N个Skill + 只新建缺失的1个" |
| **全新建** | 没有高质量同类 | 直接进入Phase 1创建 |
| **单步即可** | 需求不需要分解 | 不适用组合，直接创建 |

---

## Pipeline Orchestration Suggestions

### Pattern 1: Sequential Pipeline (顺序管线)

```
Skill A → Skill B → Skill C
  输出       输出       最终输出
```

When: 前一步的输出是后一步的输入。

Example:
```
audio-to-text → meeting-summary → action-item
  (音频转文字)    (提取纪要)        (提取行动项)
```

Suggestion: "安装这3个Skill，使用时依次调用：先说'转写这段录音'，再说'提取会议纪要'，最后说'提取行动项'"

### Pattern 2: Branch Pipeline (分支管线)

```
         ┌→ Skill B (格式A)
Skill A ─┤
         └→ Skill C (格式B)
```

When: 同一输入需要多种输出格式。

Example:
```
pdf-extractor ─┬→ markdown-converter (输出MD)
               └→ html-converter (输出HTML)
```

### Pattern 3: Conditional Pipeline (条件管线)

```
Skill A → [判断条件] → Skill B (条件满足)
                    → Skill C (条件不满足)
```

When: 根据中间结果选择不同路径。

Example:
```
content-analyzer → [有无敏感信息?]
                   ├→ yes → redact-sensitive → publish
                   └→ no  → publish directly
```

---

## Composition Recommendation Template

When suggesting composition, present:

```
🔍 同类预检结果

你的需求可以分解为 N 个步骤：

  ① [步骤1描述] → 已有高质量Skill: [名称] (评分: X/10)
  ② [步骤2描述] → 已有高质量Skill: [名称] (评分: X/10)
  ③ [步骤3描述] → 质量一般/无同类，建议新建

建议方案：[全组合 / 部分组合+部分新建 / 全新建]

如果选择组合方案：
  安装命令：clawhub install [slug1] [slug2]
  使用顺序：先说"[触发词1]"，再说"[触发词2]"

如果选择新建[步骤3]：
  你的差异化优势：[具体差异点]
  我会基于这个差异点创建一个聚焦的新Skill。
```

---

## When NOT to Suggest Composition

| Situation | Why |
|-----------|-----|
| 用户需求是单一原子操作 | 无法分解，直接创建 |
| 所有步骤的Skill质量都<5 | 组合低质量Skill不如新建一个完整的 |
| 用户明确要求一体化 | 尊重用户选择 |
| 步骤间有强耦合状态 | 管线编排无法传递中间状态，需一体化 |
| 延迟敏感场景 | 多Skill调用比单Skill慢 |

---

## Integration with Phase 0.4

```
确认门通过
  ↓
Step 0.4: SkillHub 同类预检
  ├─ 搜索完整需求 → 有更好的同类 → 建议安装，结束
  ├─ 搜索完整需求 → 有但不够好 → 提取差异点 → Phase 1 设计输入
  ├─ 搜索完整需求 → 无同类 → 直接 Phase 1
  └─ 分解为原子操作 → 逐个搜索 → 组合分析
      ├─ 全组合 → 建议安装+管线编排，结束
      ├─ 部分组合 → 建议安装已有的+新建缺失的
      └─ 全新建 → 直接 Phase 1
```
