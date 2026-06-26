---
name: sharpinput-output-renderer
description: Use when SharpInput needs to render the final user-facing response after prompt compilation, pressure, scoring, or Judge review.
---

# Output Renderer

Render the final response. Do not do new reasoning here except formatting and clarity cleanup.

## Required Output

```text
[SharpInput 识别结果]
Level:
主意图:
场景:
上下文状态:

[原问题诊断]
1. ...
2. ...
3. ...

[升级版问题]
> ...

[这版升级加入了什么]
1. 角色:
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

## Rules

- Always include a complete copy-ready prompt.
- Do not output only diagnosis, scoring, or advice.
- Keep the user's language.
- If information is missing, show placeholders rather than blocking unless output quality would collapse.
- If user requested quick mode, compress diagnosis and additions.
