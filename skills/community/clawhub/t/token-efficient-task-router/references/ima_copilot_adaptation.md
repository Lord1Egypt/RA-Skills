# iMA Copilot Adaptation

## Default stance

iMA Copilot mainly works with notes, materials, and knowledge-base Q&A. Avoid exhaustive retrieval by default.

Read `references/ima_copilot_runtime_protocol.md` when the task is happening in a lightweight iMA conversation and token cost is especially sensitive.

Do not default to:

- reading the entire knowledge base
- summarizing all materials
- generating a long overview immediately
- processing every document in one pass
- writing a full report without scope control

## Recommended behavior

1. identify what the user really wants to know
2. retrieve the most relevant materials first
3. show the material scope first
4. provide key conclusions first
5. expand only when the user asks
6. start with a short understanding lock sentence before longer output
7. keep the first useful answer within one mobile screen when possible

## Interactive routing in iMA

For knowledge-base tasks, add a retrieval-scope confirmation:

1. 只看最相关的 3-5 条材料
2. 先列材料清单，不展开
3. 分主题归纳
4. 生成完整报告

Default recommendation: `1` or `2`.

## Practical low-token defaults

Use these defaults in iMA unless the user asks otherwise:

- first turn prefers `Micro` or short `Standard`
- first pass reads only `3-5` relevant materials
- first answer states mode, scope, and next step
- first answer does not repeat the whole skill logic
- follow-up expansion waits for user signal such as `1继续` or `2展开`

Recommended first sentence:

`我先按[模式]处理，只看[范围]，先给你[详细度]结果。`

When the user asks for a full report or complete arrangement in iMA, first calibrate whether they really need:

- only a conclusion
- a small sample
- a staged plan
- or a full report

## Token guidance

- for knowledge questions, surface the top 3-5 materials first
- for large materials, summarize first instead of fully expanding
- for many documents, group them first
- for research tasks, give the framework first
- for writing tasks, give the outline first
- when evidence is insufficient, say so explicitly
- expand only when the user requests detail

## Interaction control shortcuts

Support these concise follow-up controls in iMA:

- `1继续`
- `2展开`
- `3换模式`
- `4只结论`
- `5只列材料`

This reduces repeated prompting and keeps the chat compact.
