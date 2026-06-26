# Example: Interactive Routing

## User request

`帮我优化一下这个文档。`

## Why interactive routing is required

- `优化` is ambiguous
- output style is unclear
- file permission is unclear
- token depth is unclear

## Sample full prompt

```markdown
## 任务路由确认

为了避免误判需求和浪费 token，我先确认 3 件事。你可以直接回复选项编号。

### 1. 这个任务的复杂度是？

A. 简单任务：一次回答即可完成，不涉及重要文件修改  
B. 中等任务：需要 2—3 步处理，可能涉及少量文件或较长文本  
C. 复杂任务：涉及多个文件、知识库、批量处理、项目重构或完整报告  

### 2. 你希望我以哪种模式处理？

A. Ask Mode：只诊断、解释、给建议，不直接修改  
B. Plan Mode：先给计划，等你确认后再执行  
C. Craft Mode：直接生成结果或执行低风险任务  
D. Expert Mode：按某类专家视角处理复杂问题  

### 3. 你希望输出多详细？

A. Micro：只给结论和下一步  
B. Standard：给关键理由和可执行步骤  
C. Deep：系统分析，适合复杂任务  
D. Artifact：生成文件、模板或完整文档
```

## Sample quick reply

`MPS`

## Meaning

- medium complexity
- Plan Mode
- Standard depth

## Unsafe-choice interception example

If the user chooses `CCD` for a batch file task, reply with:

```markdown
这个组合风险较高。复杂任务且涉及文件修改时，我建议改用 Plan Mode，先确认执行范围。
```
