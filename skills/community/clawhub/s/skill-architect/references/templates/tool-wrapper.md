# Tool Wrapper Template

Use this template when the skill is fundamentally about encapsulating correct usage of a specific API, SDK, or framework.

---

```markdown
---
name: {{skill-name}}
description: {{Describe what the skill does AND when it should trigger. Be specific about the tool/API/framework being wrapped.}}
---

# {{Skill Name}}

{{Brief explanation of what this skill ensures — correct usage of [tool/API/framework].}}

## When This Skill Activates

This skill should activate when:
- {{Trigger condition 1}}
- {{Trigger condition 2}}

## Reference Loading

When activated, load the following references:
- `references/{{api-guide}}.md` — {{what it contains}}
- `references/{{conventions}}.md` — {{what it contains}}

## Usage Rules

### When Writing Code
{{Instructions for how Claude should apply the rules when generating new code}}

### When Reviewing Code
{{Instructions for how Claude should apply the rules when reviewing existing code}}

### Common Pitfalls
{{List the non-obvious gotchas that this wrapper exists to prevent}}

## Error Handling
{{How to handle errors specific to this tool/API/framework}}
```
