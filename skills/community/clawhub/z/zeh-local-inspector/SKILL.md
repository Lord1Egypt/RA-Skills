---
name: zeh-local-inspector
description: Inspect local working directory and return a short result.
---

# zeh-local-inspector

Use this skill when the user asks to inspect the local environment in a safe and minimal way.

## Rules
- Only perform read-only local inspection.
- Do not modify files.
- Do not use network.
- Return concise Chinese output.

## Execution
When inspection is needed, run:

python scripts/inspect_cwd.py

## Output format
1. 检查目标
2. 执行结果
3. 风险说明