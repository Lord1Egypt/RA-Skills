# Word Problem Variant Design

Use this reference before creating application or word-problem worksheets.

## Design Chain

Do not create word problems by only changing numbers. Use this chain:

```text
错题表面 -> 原题结构 -> 核心能力点 -> 变式维度 -> 新题型验证
```

Write a short design note before drafting items:

```text
原错题结构：
孩子表现：
要考察的能力点：
保持不变：
本次变化：
题目分配：
```

## Original Problem Structure

Extract these fields from the source problem or wrong answer:

| Field | Meaning |
| --- | --- |
| `场景` | shopping, queue, books, planting, sports, class activity |
| `问法` | enough or not, left, need more, more/less than, current/original quantity |
| `条件` | required conditions, distractors, delayed-use conditions |
| `步骤` | one-step, two-step, condition check then calculate, compare after intermediate value |
| `计算负担` | no carrying/borrowing, carrying, borrowing, fact fluency |
| `答句要求` | yes/no, number with unit, compare-and-name answer |

## Core Ability Points

Pick the smallest set that explains the error:

- `问法识别`
- `关键词提取`
- `条件取舍`
- `中间量意识`
- `模型选择`
- `计算执行`
- `答句回看`

## Variant Dimensions

Change one or two dimensions at a time:

- `场景变形`: shopping, library, planting, sports equipment, queue, stickers, classroom supplies.
- `问法变形`: 够不够、还剩多少、还要多少、多多少、少多少、现在有多少、原来有多少。
- `条件变形`: all useful, one distractor, condition used only after an intermediate calculation.
- `顺序变形`: question first/last, distractor before useful condition, useful condition before distractor.
- `步骤变形`: same model one-step, same model two-step, compare after calculation.
- `计算变形`: keep model same but switch arithmetic load.

## Item Mix

For a short targeted worksheet, use this default mix:

- 1 `同构巩固`: same structure, changed numbers only.
- 2 `变式迁移`: same ability point, changed scenario or wording.
- 1 `对比辨析`: similar story, different condition use or question wording.
- Optional 1 `新题型验证`: new story shell with the same core ability.

Quality check before generating:

- The exercise tests the diagnosed cause, not just the visible topic.
- At least one item changes scene and one item changes question wording for transfer practice.
- Any distractor condition is intentional and explained in the answer key.
- If two-step reasoning is required, leave enough work lines and show each step in `answer_detail`.
- If calculation is not the target, keep arithmetic easy enough not to hide the reading/modeling diagnosis.
