---
when: 分类某段内容拿不准,或想理解为什么按这种方式拆
topics: taxonomy, less-is-more, bipartite, routing-signal, faithfulness
---

# 为什么这样压 skill

来源:SkillReducer(arXiv 2603.29919v1, 2026)对 55,315 个公开 skill 的实证。

## 三类系统性浪费

- 26.4% description 缺失或过短 → router 永远匹不上,token 在候选池里白烧
- body 仅 38.5% 是 actionable core rule,60%+ 是 background / example / template
- 14.8% skill 带 reference 文件,单次调用可注入数万 token(100 个 SkillHub skill 共 1.67M)

## 二分结构

Skill = 路由层(description) + 执行层(body + references)。两层问题不同,必须分别优化:
- 路由层:delta debugging,1-minimal(刚好够 router 唯一匹中)
- 执行层:taxonomy 分类 + progressive disclosure(只把 core_rule 常驻,其余拆出按需 read_file)

## Less-is-more

600 skill 评估中,压缩版比原版质量**反升 2.8%**。原因:非必要内容会分散 agent 注意力,让它在不相关的 example / background 里"找答案"。

**推论**:只要 faithfulness 通过,激进压缩是安全的;保留"可能有用"的内容反而是风险。

## 五类 Taxonomy

| 类型 | 定义 | 去向 |
|------|------|------|
| `core_rule` | actionable 指令(when / must / 步骤 / 禁止项 / 数字阈值) | SKILL.md(always loaded) |
| `background` | 动机、原理、why 解释 | background.md |
| `example` | I/O 对、示范、案例、few-shot | examples.md |
| `template` | 可粘贴的 boilerplate、固定格式、配置片段 | templates.md |
| `redundant` | 重复、与引用文件重合 | 丢弃 |

## 边界判断

- "为什么"→ background;"怎么做"→ core_rule
- Few-shot 示范 → example,**即使它暗含规则**。这是最常见的分类失败:examples-as-specification(作者把规则藏在示例里)。Gate 1 faithfulness 就是为了抓这种
- 纯格式约束(JSON schema / markdown 模板 / 配置文件片段)→ template
- 同一规则重复出现 → 一次留 core_rule,其余 redundant

## Routing signal 三要素

好的 description 应包含,各 20–40 tok:
1. **primary capability**:这个 skill 做什么(能力名词)
2. **trigger condition**:什么时候调用(when 从句)
3. **unique identifier**:具体工具 / 产品 / API 名,避免与同类 skill 冲突

压缩时保留这三项,其余删。触发词枚举通常可删——router 从关键词就能推断。

## Faithfulness 的必要性

结构通过 ≠ 可用。LLM 分类器会漏判 example 中的隐式规则,所以必须逐条对照原 body 的 operational concept(actionable 动词、阈值、API 名、路径、env 变量)。

回滚粒度是"类型"而非"整体":若丢失出现在被归为 example 的段里,把那段改归 core_rule 重压,而非放弃整次压缩。

## 论文实证基准

- Stage 1 平均 description 压 48%
- Stage 2 平均 body 压 39%
- 端到端 26.8% input 节省
- 86% 通过 task eval,2.8% 质量反升
- 14% 回归里只有 33% 是真压缩损失,50% 是 skill 本就该退休(obsolescence),17% 评估噪声

## 退休信号(非压缩)

若压缩版不触发 **且** 原版也不触发(router 都匹不上任何测试查询),该 skill 可能已无用。论文中 10.7% 属此类。在报告里标"候选退休",让用户判断。
