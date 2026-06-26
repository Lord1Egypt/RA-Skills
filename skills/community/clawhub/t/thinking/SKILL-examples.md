# Thinking Protocol 范例与模板

## 范例 1: 技术问题分析

```thinking
Hmm, 这是一个关于 Transformer 架构的问题。让我先理清核心概念...

首先，Transformer 最大的特点是什么？哦对，是 self-attention 机制和并行处理能力。不像 RNN 需要逐个处理 token，Transformer 可以一次性处理整个序列。

让我从输入开始推演：
1. Input embeddings 将 token 转换为向量
2. 加上 positional encoding 注入顺序信息
3. 进入 encoder stack 的 multi-head attention

等等，这里有个关键点：为什么需要 positional encoding？因为 self-attention 本身是排列不变的，必须显式注入位置信息...

(继续深入分析)
```

## 范例 2: 复杂推理问题

```thinking
Wait, 这个问题看起来简单，但需要多步推理。让我把问题分解：

首先问题问的是：XXX。表面意思是...，但深层可能是...

让我考虑几个可能的解释：
1. 解释 A: 如果用户是这个意思...
2. 解释 B: 或者用户想问的是...
3. 解释 C: 还可能是更抽象的...

Hmm, 哪个解释更合理？考虑到用户之前的对话历史，应该是解释 B。因为...（展开论证）

Actually, 我是不是忽略了什么？让我检查...
- 上下文：用户之前提到过 XXX
- 时间因素：如果是近期的问题，应该优先考虑...
- 技术成熟度：XXX 技术目前是否可行？

让我重新组织思路...
```

## 范例 3: 错误识别与修正

```thinking
我现在得出结论：XXX。但是，让我验证一下...

等一下，我刚才的推理有个漏洞。我说 "因为 A 所以 B"，但 A 和 B 之间其实没有必然联系。

让我重新审视：
- 前提 A 是对的
- 但结论 B 需要额外的假设 C
- 而 C 并没有被证实

所以正确的结论应该是...（修正后的推理）

嗯，这样就合理多了。感谢我自己及时发现了这个逻辑漏洞！
```

## 范例 4: 响应准备

```thinking
Okay, 我已经完成了完整的思考过程...

现在快速检查：
✅ 完整回答了原始问题
✅ 提供了适当的 detail level（技术细节 + 简洁总结）
✅ 使用了清晰的语言
✅ 预判了可能的问题：XXX, YYY, ZZZ

准备输出最终回复...
```

## 使用建议

1. **不要照搬** - 这些是模板，不是必须遵守的公式
2. **保持自然** - 思考应该像真实人类的思维流程
3. **动态调整** - 根据问题复杂度调整思考深度
4. **自我修正** - 随时准备修改之前的思考

## 与 Thinking-Claude 的对应

| Thinking-Claude | 本技能 | 说明 |
|----------------|--------|------|
| Inner Monolog | Stream-of-consciousness | 内心独白式思考 |
| Natural Language | Hmm..., Wait..., Actually... | 自然思考短语 |
| Error Recognition | "Wait, I made a mistake..." | 错误识别显式化 |
| Progressive Understanding | 从简到深的推理 | 渐进式理解 |