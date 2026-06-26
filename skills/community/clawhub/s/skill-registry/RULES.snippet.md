## Skill Discovery | 技能发现

**When user asks about skills, read `skills/REGISTRY.md` and respond accordingly:**

**当用户询问技能时，读取 `skills/REGISTRY.md` 并按需回复：**

| User Says | Action |
|-----------|--------|
| "what skills" / "有什么技能" / "/skills" | Read REGISTRY.md, list by category |
| "XX related skills" / "/skills XX" | Return related category only |
| "How to use XX skill" | Read `skills/XX/SKILL.md` |

**Trigger-word Routing Table | 触发词路由表：**

| Triggers | Skill | Description |
|----------|-------|-------------|
| example1, example2 | example-skill | Example description |

> Customize the table above for your skills
> 根据你的技能自定义上表

---

## Skill-Aware Execution | 技能感知执行

**When receiving a task request, follow this flow:**

**收到任务请求时，按以下流程执行：**

```
1. Scan request → Match triggers
2. If matched → Read skills/<name>/SKILL.md
3. Execute per SKILL.md workflow
4. If no match → Use general capability
```

**Examples | 示例：**

| User Says | Agent Thinks | Action |
|-----------|--------------|--------|
| "Help me do XX" | Trigger "XX" → skill-name | Read SKILL.md, execute |
| "Calculate something" | No match | Use general capability |

**Notes | 注意：**
- Skill matching is assistance, not restriction | 技能匹配是辅助，不是限制
- Complex tasks may need multiple skills | 复杂任务可能需要多技能协作
- When uncertain, ask user to confirm | 不确定时可询问用户确认
