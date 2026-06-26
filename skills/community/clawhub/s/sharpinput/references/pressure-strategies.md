# Pressure Strategies

Pressure makes the upgraded prompt harder to answer with vague default advice. It must not change user intent.

## Name

Use "默认答案压力测试" as the default phrase.

Avoid older framing like "反共识" as the main concept. The goal is not contrarian performance; the goal is better fit to the user's real constraints.

## Pressure Levels

| Level | Use When | Injection |
|---|---|---|
| none | factual explanation, light rewrite, translation | no pressure |
| light | simple improvement with minor ambiguity | ask for concrete examples and avoid generic advice |
| medium | optimization, comparison, product/technical analysis | require trade-offs, criteria, and failure conditions |
| strong | decision, validation, strategy, high stakes | require recommendation, counterexample, flip condition, and first action |

## Default-Answer Stress Test

Add only when the default answer is likely to be weak:

- "不要只给通用建议；请指出在什么条件下主流建议会失效。"
- "如果你给出推荐，必须同时说明你放弃了什么。"
- "先列出最可能误导我的默认答案，再给出更适合我场景的版本。"
- "给出可以推翻你建议的信号。"

## Pressure Selection

| Intent | Default Pressure |
|---|---|
| 理解 | light |
| 决策 | strong |
| 生成 | light or medium |
| 分析 | medium |
| 探索 | light |
| 诊断 | medium |
| 说服 | medium |
| 验证 | strong |
| 规划 | medium |
| 学习 | light |
| 优化 | medium |
| 对比 | strong |
| 梳理 | none or light |
| 求助 | light |

## Overpressure Warning Signs

Reduce pressure when:

- the prompt becomes longer than the task deserves
- the user asked only for wording polish
- pressure introduces a stance the user did not choose
- the output sounds adversarial where collaboration is needed
- the prompt asks the next AI to do too many unrelated jobs

## Required Handoff Fields

```json
{
  "pressure_requirements": [
    {
      "type": "default_answer_stress_test",
      "text": "",
      "reason": "",
      "strength": "light | medium | strong"
    }
  ],
  "overpressure_risk": "low | medium | high"
}
```
