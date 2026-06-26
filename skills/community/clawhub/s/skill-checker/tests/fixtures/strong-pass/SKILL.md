---
name: strong-pass
description: Build polished audit feedback for creative coding skills and explain when each workflow applies. Use when an agent needs to evaluate a skill with staged instructions, clear constraints, and a shareable review summary.
description_en: Build polished audit feedback for creative coding skills. Use when an agent needs staged review guidance and clear output expectations.
description_zh: 为创意编程技能生成高质量审计反馈。适用于需要分阶段评审流程与明确产出标准的场景。
license: Apache-2.0
metadata:
  author: skill-team
  version: "1.2.0"
  category: review
compatibility: generic-agent
allowed-tools: shell_command apply_patch
---

# Strong Pass

## Principle

Work in visible phases so another agent can follow the review without guessing.

## Workflow

1. Inspect the target skill and confirm the requested audience.
2. Evaluate the frontmatter, body structure, and output expectations.
3. Record the exact problems, explain the impact, and provide repair steps.

## Output

Return a concise result, then list the highest-priority fixes and any remaining warnings.
