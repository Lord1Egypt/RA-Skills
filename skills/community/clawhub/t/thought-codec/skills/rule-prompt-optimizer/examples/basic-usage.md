# Rule And Prompt Optimizer Example / 规则与提示词迭代示例

## Scenario

A user repeatedly corrects an assistant to avoid vague praise and produce direct engineering prose.

用户反复纠正助手，要求避免空泛称赞，并输出直接的工程表达。

## Prompt

```text
Use the Rule And Prompt Optimizer Skill.

Source material:
- The assistant repeatedly says "great idea" before doing the work.
- The user prefers direct execution and concise progress updates.
- The final accepted responses lead with concrete actions and verification.

Observed problem:
The assistant spends too much space praising or summarizing instead of moving the task forward.

Reuse target:
Update the assistant collaboration rules.

Output:
Draft rule patch with layer, evidence, limits, and regression checks.
```

## Expected Output Shape

```json
{
  "rule_id": "direct-progress-updates",
  "layer": "L1_Presentation",
  "instruction": "When work is requested, lead with the action being taken and keep praise out of progress updates.",
  "evidence": ["Repeated user corrections against vague praise"],
  "limits": ["Does not ban warm tone in casual conversation"],
  "regression_checks": ["Progress updates name the concrete action and stay concise"],
  "patch_target": "collaboration style rules"
}
```

## Review Checks

- The rule is not overgeneralized.
- The evidence is summarized without exposing private transcripts.
- The rule has limits and regression checks.
- The patch target is clear.
