# SharpInput Output Templates

Use these templates only after intent, scenario, context, and prompt compilation are complete.

The final answer must help the user copy the upgraded input immediately. Do not make the user reconstruct the prompt from analysis.

## Standard Template

```text
[SharpInput 识别结果]
Level: Level X
主意图: ...
场景: ...
上下文状态: complete | partial | insufficient

[原输入诊断]
1. ...
2. ...
3. ...

[升级版输入]
> ...

[这版升级加入了什么]
1. 角色/视角:
2. 目标:
3. 约束:
4. 判断标准:
5. 输出格式:
6. 默认答案压力测试:

[取舍提醒]
...

[最小补充项]
...
```

## Quick Template

Use when the user asks for quick rewrite, simple polish, or Level 0/1 output.

```text
[SharpInput Level X]

诊断: ...

升级版:
> ...

补充: 加入了 ...；保留了 ...
```

## Clarify-First Template

Use when one field would materially improve the prompt and asking is better than guessing.

```text
[SharpInput 需要补一刀]

我能先给出可用版本，但下面这个信息会明显影响质量:
- ...

先给你一个带占位符的版本:
> ...

你只要补充: ...
```

## Level 3 Multi-Path Template

Use when the task is high-risk, strategic, or naturally has multiple valid paths.

```text
[SharpInput Level 3]

诊断: ...

路径 A - 稳妥推进:
> ...
Judge: pass | minor_fix | rewrite_required
风险: ...

路径 B - 强约束决策:
> ...
Judge: pass | minor_fix | rewrite_required
风险: ...

路径 C - 探索式拆解:
> ...
Judge: pass | minor_fix | rewrite_required
风险: ...

建议默认选: ...
```

If interactive option selection is available, ask the user to pick one or more paths using `AskUserQuestion`. If not, recommend the lowest-risk path first and still include all paths in text.

## Output Rules

- Keep the user's language unless the user asks for another language.
- Always include one complete upgraded prompt.
- If context is missing but not blocking, use explicit placeholders like `[预算范围]`.
- Do not include hidden chain-of-thought, internal scores, or module handoff JSON in the final response.
- Do not output only critique, rating, or "建议你这样问"; the copy-ready prompt is mandatory.
- Use "默认答案压力测试" rather than "反共识" unless quoting old material.
