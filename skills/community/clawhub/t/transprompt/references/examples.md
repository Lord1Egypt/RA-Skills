# Prompt Transformer Examples

Use this file for concrete examples when choosing between transform, clarify, and bypass.

## 1. Transform Directly

### Example A: code generation

**Input**
```text
@prt 帮我写一个网页抓取的 Python 脚本，抓取新闻标题并保存成 CSV
```

**Also valid**
```text
@prt帮我写一个网页抓取的 Python 脚本，抓取新闻标题并保存成 CSV
```

**Not valid**
```text
@promptify帮我写一个网页抓取的 Python 脚本
```

**Preferred user-facing reply**
```text
如果你是想用这个功能，可以写成：@prompt帮我写一个网页抓取的 Python 脚本
```

**Preferred behavior**
- Transform directly
- Keep the prompt practical and not overly long
- Add 2 short `Prompt 关键处理` bullets by default

### Example B: prototype generation

**Input**
```text
@prompt 帮我设计一个面向独立开发者的 SaaS 登录页原型
```

**Preferred behavior**
- Transform directly
- Include role, goal, target audience, page sections, and expected output format


## 2. Transform with Assumptions

### Example C: moderate ambiguity

**Input**
```text
@prt 帮我做一个记账 App
```

**Preferred behavior**
- Generate a prompt only if the missing details can be reasonably defaulted
- State assumptions explicitly, for example:
  - 面向个人用户
  - 移动端优先
  - 核心功能包括记账、分类、统计

## 3. Clarify First

### Example D: critical ambiguity

**Input**
```text
@prompt 帮我做一个电商后台
```

**Preferred behavior**
- Ask 1 to 3 clarification questions first
- Focus on the details that most affect the output, such as platform, scope, and desired deliverable

### Example I: fragment only

**Input**
```text
@prt帮我做一个
```

**Preferred behavior**
- Ask only the single missing question that unblocks the task
- Good reply shape: `你想做一个什么？比如页面、App、脚本、方案、论文，还是原型？`
- Do not add an extra meta question about whether the user wants a prompt or wants help refining the need

## 4. Bypass

### Example E: ordinary question

**Input**
```text
@prt 今天天气怎么样？
```

**Preferred behavior**
- Do not output a transformed prompt
- Reply naturally as a normal question

### Example F: casual chat

**Input**
```text
@prt 哈哈
```

**Preferred behavior**
- Bypass naturally
- Do not explain prompt engineering unless necessary
- Prefer a direct human reply like `哈哈` or `哈哈，怎么啦？`

### Example H: greeting

**Input**
```text
@prt 哈喽
```

**Preferred behavior**
- Reply directly, for example: `哈喽`
- Do not say `这个例子应该走旁路`
- Do not expose internal routing language to the user

## 5. Empty Input

### Example G: prefix only

**Input**
```text
@prt
```

**Preferred behavior**
- Return short usage guidance
- Do not output an empty prompt

Suggested wording:

```markdown
请输入您要转化的需求，例如：

@prt 帮我写一个 Python 脚本，批量重命名文件
@prompt 帮我设计一个面向独立开发者的登录页原型
```

## 6. Output Tone

Prefer this tone:
- concise
- practical
- professional but not stiff
- educational in a lightweight way

Avoid:
- long lectures on prompt engineering
- excessive jargon
- overformatted templates for very small tasks
