---
when: 想理解论文依据，或某步骤拿不准（尤其 Gate 0 退休判定 / 五类 taxonomy 边界 / 和 skill-creator 的差异）
topics: skillreducer, less-is-more, day-zero, taxonomy, routing-signal, retirement, bookend
---

# 为什么要 day-0 前置结构约束

## skill-creator 的局限

官方 `skill-creator` 走 **create → test → eval → iterate**，优化"写得对不对"。但论文 [SkillReducer](https://arxiv.org/abs/2603.29919)（55,315 skill 实证）显示**三类问题 eval 指标抓不到**：

- **26.4% description 缺失/过短** → router 永远匹不上，测试查询全 miss，eval 给不了信号
- **body 仅 38.5% 是 actionable core rule**，60%+ 是 background / example / template；eval pass 不等于结构健康
- **10.7% skill 本该退休**（router 匹不上任何典型查询），但 skill-creator 默认"skill 应该存在"

**结论**：结构问题必须在创作**之前**用硬约束锁死，事后 eval 补救成本高且有盲点。

## Less-is-more

论文 600-skill 对照：压缩版比原版质量**反升 2.8%**——非必要内容会分散 agent 注意力，让它在不相关的 example / background 里"找答案"。

day-0 前置 = 让 skill 出生就精简 = 未来压缩空间有限。**理论保证**：skill-scaffolder 产出的 skill，过 skill-compressor 应该压不了多少。这是对 scaffolder 自身的验证指标。

## 五类 Taxonomy 速览

| 类型 | 定义 | 去向 |
|------|------|------|
| `core_rule` | actionable 指令（when / must / 步骤 / 禁止项 / 数字阈值） | `SKILL.md`（always loaded） |
| `background` | 动机、原理、why 解释 | `background.md` |
| `example` | I/O 对、示范、few-shot | `examples.md` |
| `template` | 可粘贴的 boilerplate、固定格式、配置片段 | `templates.md` |
| `redundant` | 重复、与引用文件重合 | 丢弃 |

**day-0 vs day-N 的分类差异**：
- skill-compressor 是**事后分类**——从已有 body 逆向识别类型
- skill-scaffolder 是**事前分类**——作者每想一条规则，当场就打标签，从源头避免混淆

## Gate 0 退休判定

给 skill idea 提出 3 个"典型触发场景"后，反问：

1. 场景 A 裸模型能做吗？（无 skill 时 Claude 的答案够用吗）
2. 场景 B 有现成 skill / MCP / tool 吗？（是否重复造轮子）
3. 场景 C 只需 1–2 条规则吗？（能否放 `CLAUDE.md` 或短 prompt 搞定）

**3 个全为 yes → 建议退休**。论文里 10.7% skill 属此类，作者在不自觉造不必要的 skill。

## Routing signal 三要素

好的 description 应包含，各 10–40 tok：

1. **primary capability**：这个 skill 做什么（能力名词 / 动作）
2. **trigger condition**：什么时候调用（when 从句）
3. **unique identifier**：具体工具 / 产品 / API / 领域关键词，避免与同类 skill 冲突

**常见错误**：
- 只有 primary capability（太泛，和一堆 skill 撞）
- 堆一长串触发词枚举（router 能从关键词推断，枚举反而增加 noise）

## 为什么"一次性生产"而非引导式

skill-creator 走引导式，每步问用户，适合新手但高摩擦。skill-scaffolder 面向**已读过本文档的 builder**——一把产出完整骨架，builder 自己 diff 迭代。

理由：有经验的 skill 作者不需要被反复问"primary capability 是什么"，他们更想一次拿到骨架然后快速 polish。

## 和 skill-compressor 的 Bookend

```
      ┌─ skill-scaffolder ─┐                        ┌─ skill-compressor ─┐
idea →│  day-0 出生精简     │ → SKILL.md → (时间) → │  day-N 老 skill 压缩 │
      └────────────────────┘                        └────────────────────┘
```

前者产出的 skill 一开始就是"已压缩"形态。后者处理社区历史遗留的臃肿 skill 或自己长胖了的老 skill。

## 论文实证参考

- 平均 description 压 48%
- 平均 body 压 39%
- 86% 压缩版通过 task eval，2.8% 质量反升
- 14% 回归里只有 33% 是真压缩损失，50% 是 skill 本就该退休，17% 是评估噪声

**推论**：激进的结构约束 + Faithfulness gate 在论文里被验证安全——day-0 前置等于把这个安全网从事后移到事前。
