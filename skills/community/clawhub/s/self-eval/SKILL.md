---
name: self-eval
description: |
  自我评估 / rubric 评分器（元认知闭环核心）。让 agent 对自己的输出做结构化、可复现的评分，而非凭感觉"我觉得不错"。提供多维度评分表（相关性/完整性/结构/准确性/可执行性）、自动 rubric 生成、可选参考答案重叠比对，输出打分 JSON + 改进建议。当用户需要"评估一下这段输出""给自己的回答打分""做个 rubric 评分""self-evaluation""检查质量"时调用。
agent_created: true
visibility: "public"
---

# 自我评估（Self-Eval）· 元认知评分器

让 agent 对自己的输出做**结构化、可复现**的评分，把"质量"从主观感受变成可度量的维度分数。这是元认知闭环的核心一环：能评估自己，才能改进自己。

## 适用场景
- 任务完成后对最终输出做质量自检（发布/交付前门禁）
- 同一任务的多个候选答案横向对比、选优
- 把"用户反馈"沉淀为可复用的评分维度（rubric）
- 作为更上层「自我改进循环」的反馈信号（配合 prompt-optimizer / meta-evolver）

## 评分维度（默认 rubric，可覆盖）
1. **相关性** — 是否直接回应任务，没有跑题
2. **完整性** — 任务要求的要点是否都覆盖
3. **结构清晰度** — 是否层次分明、易读
4. **准确性** — 事实/逻辑是否成立（有参考答案时比对）
5. **可执行性** — 给出的内容能否直接落地（命令/步骤/代码可用）

## 标准工作流
用 `scripts/grade.py` 对一段输出做评分：
```bash
# 自带默认 5 维 rubric，直接评
python scripts/grade.py --task "写一封英文道歉邮件" --output answer.md --out report.json
# 指定自定义 rubric（JSON）
python scripts/grade.py --task "..." --output out.md --rubric rubric.json --out report.json
# 有参考答案时，加入重叠比对（更准确）
python scripts/grade.py --task "..." --output mine.md --reference gold.md --out report.json
```

`rubric.json` 结构：
```json
{
  "criteria": [
    {"name": "相关性", "weight": 0.25, "keywords": ["道歉", "原因"], "min_len": 80},
    {"name": "完整性", "weight": 0.25, "keywords": ["补偿", "联系方式"]}
  ]
}
```

## 质量门禁（agent 自评后据此决定是否返工）
- overall ≥ 0.75 → 通过，可直接交付
- 0.5 ≤ overall < 0.75 → 部分通过，针对 fail/partial 维度补强后复评
- overall < 0.5 → 不通过，回到原任务重做

## 自进化学习系统
```bash
python scripts/learner.py record . --capability "自我评估" [--fail --error <类型> --note <说明>]
python scripts/learner.py insight .
python scripts/learner.py reflect .
```
- 某维度反复 fail → 记录，reflect 建议把该维度关键词/阈值写进默认 rubric
- 用户的评分偏好（更看重准确性还是可执行性）→ `prefer` 记录，未来自动加权
