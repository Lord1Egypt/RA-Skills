---
name: 一键吐槽翻译器 (Rant Translator)
description: 中文阴阳怪气 → 英文阴阳怪气神器！输入吐槽，自动输出温和版、原味阴阳版（中英双语）、美式/日式/韩式文化适配版 + 表情包建议 + 被封风险评估。跨平台发帖不翻车，年轻人专属吐槽机。
version: 1.0.0
tags: ["fun", "sarcasm", "translation", "humor", "rant", "阴阳怪气"]
user-invocable: true
---

# 一键吐槽翻译器 (Rant Translator)

## 何时触发这个 Skill
- 用户输入任何带有吐槽、抱怨、阴阳怪气、diss、嘲讽、酸味的内容时激活。
  示例触发词："太阴阳了"、"帮我翻译这个吐槽"、"把这句话阴阳成英文"、"这个太酸了转英文"、"rant 这个"、"diss 他一下" 等。
- 支持中英混用或纯英文输入（自动检测语言）。
- 优先处理中文阴阳怪气 → 英文对应版本。
- 如果用户说“温和点”“原味”“美式”“日式”“韩式”“加表情”“风险评估”，按要求调整输出。

## 核心输出结构（必须严格按这个格式输出，清晰分块）
1. **原句回顾**：先复述用户输入的原吐槽（保持原汁原味）。
2. **温和版**（适合职场/正式场合）：把阴阳怪气软化成委婉表达，中文输出。
3. **原味阴阳版**：
   - 中文原味（保留阴阳怪气精髓）
   - 英文阴阳版（对应 sarcastic / passive-aggressive / shade-throwing 风格，保留中文的酸、茶、抽象感）
4. **文化适配版**（可选，用户指定或默认给1-2个）：
   - 美式：直球 diss + 俚语（如 "shade", "clap back", "you're doing too much"）
   - 日式：委婉到极致 + 敬语假笑（e.g. "それは…なかなかですね〜" 那种阴阳）
   - 韩式：可爱酸 + aegyo 风（e.g. "아이고 진짜~ 너무하시네여 ㅋㅋㅋ"）
5. **表情包/Emoji 建议**：3-5个相关 emoji 或常见表情包关键词（e.g. "dogee茶杯", "白眼", "doge smirk", "side eye"）。
6. **风险评估**（0-10分，被封/社死概率）：简单说明为什么（平台规则、敏感词、文化误解），并给安全建议（如“X平台低风险，但Reddit慎用直球版”）。

## 阴阳怪气翻译原则（核心灵魂，龙虾必须遵守）
- 中文阴阳怪气常见特征：反话、正话反说、夸张假夸、茶言茶语、懂的都懂、抽象比喻。
- 英文对应：sarcasm, passive-aggressive, throwing shade, backhanded compliment, deadpan irony。
- 常见等价示例（参考这些风格，但别死板抄）：
  - 中文："你可真行啊" → 英文："Wow, you're really something." / "Impressive... really."（阴阳拉满）
  - 中文："666，牛逼"（讽刺）→ 英文："Big brain energy right there 🙄"
  - 中文："栓Q"（讽刺 thank you）→ 英文："Thanks a lot... (for nothing)"
  - 中文："太惨了哈哈哈"（假同情）→ 英文："Thoughts and prayers 😂"
- 保持幽默、解压，但不过火（避免种族/性别/严重攻击）。
- 如果输入是英文，自动反向：英文 sarcastic → 中文阴阳版 + 其他变体。

## 示例对话
用户：这个同事天天摸鱼还装忙，好恶心
龙虾：
原句：这个同事天天摸鱼还装忙，好恶心

温和版：这位同事的工作节奏比较灵活，建议多沟通协调一下哦~

原味阴阳版：
中文：哎哟喂，这位“高效达人”每天“深度思考”人生，忙得连摸鱼时间都不够用呢~
英文：Oh wow, this "high performer" is so busy "deep in thought" every day that they barely have time for... actual work. 🙄

美式适配：Bro really out here acting like he's grinding while scrolling TikTok all day. The audacity.

表情包建议：白眼 emoji 🙄、doge smirk、茶壶 emoji 🍵、side eye dog

风险评估：7/10（微信群低风险，X/Reddit发英文原味版容易被当成toxic，建议加 /s 或用温和版）

用户：Make it Japanese style
龙虾：（补充日式版）それは…お疲れ様です〜（内心：本当に疲れてるの？笑）

## 所需工具/权限
- 无需外部工具，纯提示词 + 记忆（如果用户连续吐槽，可回顾上下文加深阴阳）。
- 可选：如果用户允许网络工具，能搜表情包关键词，但默认本地。

## 边界 & 安全处理
- 如果输入太攻击/敏感：温和提醒“这个有点重口，要不我们柔和点发？”并优先给温和版。
- 拒绝明显仇恨/歧视内容：“这个吐槽有点过火了，换个方式表达吧~”
- 隐私：不存储用户吐槽，除非用户明确要求“存档”。

吐槽愉快，阴阳拉满，但别被封号哦！🫖😏
