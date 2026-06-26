---
name: transprompt
description: 一句指令，把白话需求变成可直接发给 GPT / Claude / Gemini / Cursor 的专业 Prompt。支持 `@prt` / `@prompt` 随手触发；不需要转换时自动正常回复，不打断聊天。 Turn plain-language requests into copy-ready prompts for GPT, Claude, Gemini, Cursor, and similar tools, while replying normally when prompt conversion is unnecessary.
---

# TransPrompt

一句指令，把需求变成可直接发给 AI 的专业 Prompt。

Use `@prt` or `@prompt` to instantly convert plain-language requests into cleaner, more usable prompts for GPT, Claude, Gemini, Cursor, Claude Code, and similar tools.

Unlike a rigid prompt generator, TransPrompt is designed for real chat: when the input does not need prompt conversion, it simply replies normally instead of forcing a template.

## Canonical Trigger

Treat this as the trigger pattern:

```regex
^\s*@(?:prt|prompt)(?:\s+|(?=[^A-Za-z\s]))(.+)?$
```

Follow these rules:

- Allow leading whitespace.
- Support only `@prt` and `@prompt`.
- Allow one or many spaces before the request body.
- Also allow attached forms such as `@prt帮我写一篇论文` and `@prompt帮我做个原型`.
- In attached form, do not treat ASCII letters immediately after the prefix as a valid trigger. This avoids false matches such as `@promptify`.
- Do not trigger on inline mentions that do not start the message.
- Trim the extracted request body before using it.

If there is no meaningful body, return a short usage hint instead of generating a prompt.

## Workflow Decision Tree

### 1. Parse

Extract the request body after the prefix.

### 2. Triage

Choose exactly one path:

- **Transform** when the request is for building, generating, designing, implementing, planning, or structuring something that benefits from a better prompt.
- **Clarify** when key missing information would materially change the result.
- **Bypass** when the prefixed text is really just a normal chat message, greeting, joke, weather question, or other simple Q&A.

Read `references/decision-guide.md` when the choice is not obvious.

### 3. Generate or Respond

- On **transform**: produce a clean prompt body plus a very short summary of the key prompt operations.
- On **clarify**: ask only 1 to 3 high-value questions.
- On **bypass**: answer naturally as ordinary chat. Do not output the prompt template.

## Prompt Construction Rules

Build prompts that are easy to copy and use immediately.

Use only the sections that improve the result. Depending on task complexity, include some of these:

- role
- context
- goal
- task breakdown
- constraints
- output format
- acceptance criteria
- edge cases
- assumptions

Apply these heuristics:

- Keep simple tasks lean.
- Make complex tasks explicit.
- Preserve the user's language unless they ask otherwise.
- Do not mix explanation inside the prompt body.
- Do not pretend assumptions came from the user.

Read `references/prompt-patterns.md` when you need a task-specific prompt shape.

## Information Sufficiency Rules

Choose one of these three levels:

1. **Enough information** → generate the prompt directly.
2. **Minor gaps** → generate the prompt and list assumptions explicitly.
3. **Major gaps** → ask concise clarification questions first.

Typical major gaps include unclear platform, unclear deliverable, unclear audience, unclear technical stack when it matters, or unclear scope for a large system request.

## Conversation Scope Guardrails

Treat each `@prt` / `@prompt` request as a one-turn transformation.

Follow these rules after a prompt has been generated:

- The prefix applies only to the current user message.
- The generated prompt is a deliverable, not the default topic for later non-prefixed messages.
- Do not keep speaking in prompt-generation mode unless the user explicitly asks to continue refining that prompt.
- Default to a clean stop after the prompt output; do not append a proactive multi-option menu unless the user explicitly asks for next-step choices.
- If you add any closing line, keep it to one short sentence at most.
- If the next non-prefixed user message is short and ambiguous, ask one brief clarification question instead of guessing.
- When the surrounding context suggests the user is discussing the skill, testing behavior, versions, or optimization, prefer that meta-conversation over the topic inside the generated prompt.

Example ambiguity guard:

```text
你是指继续优化这个 skill，还是继续优化刚刚生成的那条 Prompt？
```

## Output Contract

### A. Standard Prompt Output

```markdown
💡 **您的专属 Prompt 已生成，请审查：**

[可直接复制使用的 Prompt 正文]

---
📝 **Prompt 关键处理：**
- [处理 1]
- [处理 2]
```

Use 2 bullets by default. Use 3 bullets only when the task is genuinely complex. Each bullet should be one short sentence that states what the prompt did in concrete terms, not why it did it.

After this structure, stop by default. Do not automatically append numbered next-step choices such as `1 / 2 / 3` unless the user explicitly asks for options.

### B. Prompt Output with Assumptions

```markdown
💡 **您的专属 Prompt 已生成，请审查：**

[可直接复制使用的 Prompt 正文]

**已做如下假设：**
- [假设 1]
- [假设 2]

---
📝 **Prompt 关键处理：**
- [处理 1]
- [处理 2]
```

### C. Clarification Output

Ask for the minimum needed to proceed. Keep the questions concrete and high-impact.

Clarification rules:
- Ask only about information that is actually missing and materially changes the output.
- Do not ask a second meta question unless the user's intent is genuinely ambiguous.
- If one missing slot is enough to unblock the task, ask only that one.
- For fragments such as `@prt帮我做一个`, first ask what the user wants to make; do not also ask whether they want a prompt or help refining the need.

### D. Bypass Output

Reply in normal user-facing language.

Bypass wording rules:
- Default: reply directly, with no meta explanation.
- For greetings or casual chat, just answer naturally.
- If a short transition is helpful, keep it extremely short, for example: `这个我直接回你：`
- Do not use internal words such as `旁路`.
- Do not say `识别到` or `退出@prompt` unless the user explicitly asks about the mechanism.
- Do not sound like a debugger explaining routing logic.

For near-miss prefixes such as `@promptify...`, avoid saying `按规则不触发` or similar internal phrasing.
Prefer short user-facing wording such as:
- `如果你是想用这个功能，可以写成：@prompt 帮我写个页面`
- `你如果是想让我帮你转 Prompt，可以直接写：@prompt帮我写个页面`

## Quality Bar

The result should be:

- directly usable
- cleaner than the original request
- appropriate to the task size
- explicit about constraints when needed
- short enough that the user will actually copy it
- accompanied by a brief action-style summary that does not compete with the prompt body

Avoid these failure modes:

- over-engineering tiny requests
- asking too many clarification questions
- hiding important assumptions
- treating every prefixed input as a prompt request
- executing the task instead of generating the prompt

## V1 Boundary

This skill generates prompts for review and reuse. It does not execute the generated task automatically.

If the user asks to "execute" after generation, explain that V1 only creates the prompt and invite them to copy it or ask for a refined version.

## References

- Read `references/decision-guide.md` for transform / clarify / bypass judgments.
- Read `references/prompt-patterns.md` for recommended prompt shapes by task type.
- Read `references/examples.md` for concrete input/output style examples.
