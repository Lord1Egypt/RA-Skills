# Step Definition Template

Use this format to summarize each completed step.

```
## Step N: <step-name>

**Input:**
- <what enters this step>

**Output:**
- <what this step produces>

**Responsibilities:**
- <what this step does / who owns it>

**Risks:**
- <what can go wrong>

**Validation:**
- <how to verify correctness>

**Rules:**
- <hard constraints / thresholds>
```

## Section Definitions

| Section | Definition |
|--------|-----------|
| Responsibilities | What the step does (action, owner) |
| Risks | What can go wrong (failure modes) |
| Validation | How to verify the step output is correct |
| Rules | Hard constraints, thresholds, or non-negotiables |

## Common Mistakes

- Do NOT mix Validation and Rules — validation tests correctness; rules are constraints
- Do NOT assume missing details — ask before filling in
- Do NOT generate Rules before Risks are identified
- A step is incomplete if ANY section is missing
