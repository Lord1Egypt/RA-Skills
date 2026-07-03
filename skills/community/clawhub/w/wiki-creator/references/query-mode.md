# 查询模式 + 两级索引使用

> 本文档在 LLM 处理用户查询时必读。**不走向量检索。**

## 1. 查询标准流程

```
用户提问
  ↓
读 wiki/index.md              ← 主题层（主题清单 + 摘要）
  ↓
判断属于哪个 / 哪些主题
  ↓
读 topics/<topic>.md          ← 页面层（该主题所有页面 + 摘要）
  ↓
按摘要自主判断相关页
  ↓
读 pages/<topic>/<slug>.md    ← 页面全文
  ↓
沿 [[wikilink]] 多跳推理     ← 按需读关联页（可跨主题）
  ↓
作答，引用 [[页面]] + 源文件
```

## 2. 两级索引天然限流

| 层级 | 文件 | 用途 |
|---|---|---|
| 主题层 | `wiki/index.md` | 列出所有主题 + 主题摘要 + 页面数 |
| 页面层 | `wiki/topics/<topic>.md` | 该主题所有页面，按 entity_type 分组，每页带摘要 |
| 页面 | `wiki/pages/<topic>/<slug>.md` | 单页全文 |

LLM 每层只读必要部分：
1. 读 `index.md` → 判断主题（一次读全文，主题数有限）。
2. 只读相关主题的 `topics/<topic>.md`，不读全部主题。
3. 只读相关页的全文，不读整个主题目录。

**禁止**整库加载所有页面到 context。

## 3. 多跳推理

页面正文中的 `[[wikilink]]` 是前向链接。读到 A 页时看到 `[[B]]`：

1. 如果 B 与当前问题相关，按需读 B 页全文。
2. 如果 B 不相关，跳过。
3. 可跨主题——`pages/deep-learning/transformer.md` 可链接到 `[[distributed-systems/parameter-server]]`。
4. 多跳深度建议 ≤ 3 跳，避免上下文膨胀。

反链（`.backlinks.json`）不在页面正文中，但 LLM 可在查询时主动查反链做"反向追溯"——例如查"哪些页引用了 attention"。脚本已计算好，LLM 直接读 json。

## 4. 作答规范

回答必须包含：
1. **答案正文**：客观陈述，不超过 3 段。
2. **引用**：每条结论后注 `[[页面-slug]]`；如有具体出处再注 `raw/<file> §<section>`。

示例：

> Transformer 是基于自注意力的序列模型架构，通过并行计算注意力权重替代 RNN 的递归结构 [[transformer]]。其核心是 Scaled Dot-Product Attention，通过 Q/K/V 三个矩阵计算注意力分布 [[attention]]；原文见 raw/paper-a.pdf §page-3。
>
> 相关：[[positional-encoding]]（位置编码）、[[bert]] / [[gpt]]（应用）。

## 5. 查询失败的处理

- 主题层无相关主题 → 报告"Wiki 中无相关主题"，建议补充资料。
- 主题层命中但页面层无相关页 → 报告"主题 X 下暂无相关页"，列出该主题现有页供参考。
- 页面命中但内容不足 → 沿 wikilink 多跳，仍不足则报告数据缺口，建议补料。
- 出现 `[[dangling-link]]` → 报告"引用了未建页实体 X，建议建页或补充资料"。

## 6. 与"语义搜索"的区分

**本技能不走向量检索。** 用户说"语义搜索 / 相似度 / embedding"类需求，**不触发本技能**，转交其他工具。

本技能的"查询"是基于两级索引 + 摘要 + wikilink 的**符号式推理**：
- 主题判断靠 LLM 读 index.md 摘要。
- 页面选择靠 LLM 读 topics/*.md 摘要。
- 多跳靠 LLM 沿 wikilink 主动读关联页。

## 7. 查询示例

### 例 1：单主题单页

> 用户："Transformer 是什么？"
>
> 1. 读 index.md → 命中主题 `deep-learning`。
> 2. 读 topics/deep-learning.md → 命中 `[[transformer]]`。
> 3. 读 pages/deep-learning/transformer.md 全文。
> 4. 作答。

### 例 2：跨主题多跳

> 用户："Raft 算法和 Paxos 算法有什么区别？"
>
> 1. 读 index.md → 命中主题 `distributed-systems`。
> 2. 读 topics/distributed-systems.md → 命中 `[[raft]]` 和 `[[paxos]]`。
> 3. 读 pages/distributed-systems/raft.md 全文，看到 `## 关联` 中 `对比：[[paxos]]`。
> 4. 读 pages/distributed-systems/paxos.md 全文。
> 5. 对比作答。

### 例 3：反向追溯

> 用户："Wiki 里有哪些页提到了 attention？"
>
> 1. 读 `.backlinks.json`，查 `attention` 的反链列表。
> 2. 报告所有引用 attention 的页面。
