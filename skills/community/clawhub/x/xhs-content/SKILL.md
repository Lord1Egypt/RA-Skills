---
name: xhs-content
description: Generate Xiaohongshu-style content for Chinese social posts focused on 职场成长、副业探索、AI工具应用. Use when the user provides a hot post, topic, angle, notes, or rough draft and wants: (1) 爆款逻辑拆解, (2) 小红书标题与正文改写, (3) 话题标签, (4) 配图建议, or (5) multiple post variants for A/B testing.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📝"
    homepage: "https://github.com/xiaonizhou-crypto/xhs-content-skill"
---

# 小红书内容生产 Skill

围绕「职场 / 副业 / AI 工具」赛道生成更像小红书原生风格的内容。

## 执行流程

1. 判断输入类型：热帖原文、主题关键词、草稿、产品卖点、案例素材。
2. 先提炼爆点：情绪钩子、痛点、人群、结果承诺、结构节奏。
3. 生成成品：标题、正文、标签、配图建议。
4. 如果用户提供的信息不足，仍然先给可用初稿，不先卡住流程。
5. 如果用户明确要求模仿热帖，只复用结构与节奏，不照抄原句。

## 输出默认结构

除非用户指定别的格式，否则按下面结构输出：

- 【爆款逻辑】100 字内
- 【标题】给 3-5 个备选，长度控制在 20 字内
- 【正文】1 个主版本，300-500 字，分段清楚
- 【标签】15 个，混合泛流量标签和精准标签
- 【配图建议】3 张，分别说明封面图 / 内容图 / 结尾图

## 风格要求

- 口语化，像真人分享，不像广告投放文案
- 先讲结果或情绪，再给过程和方法
- 每段尽量短，阅读阻力低
- 少用陈词滥调，不用“小编”“绝绝子”“闭眼冲”这类过时表达
- 强调实用价值，不写成纯技术说明书
- 标题避免硬夸张，优先“共鸣 + 结果 + 反差”

## 变体策略

按用户输入匹配下面的优先模式：

- **热帖拆解型**：先分析为什么火，再输出改写稿
- **干货教程型**：强调步骤、工具、收益、避坑
- **案例逆袭型**：强调前后对比、时间成本、可复制性
- **观点共鸣型**：强调打工人痛点、误区、认知反差

## 需要更多细节时再读的参考文件

- 标准输出模板：`references/prompt.md`
- 标题与钩子速查：`references/hooks.md`
- 示例输入输出：`references/examples.md`
- 案例场景库：`references/case-studies.md`
