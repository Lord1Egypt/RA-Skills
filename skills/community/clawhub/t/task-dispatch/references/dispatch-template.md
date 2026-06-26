# Subagent Dispatch Template

派发任务给 subagent 时，使用以下模板确保上下文完整。

---

## Template

```markdown
# Task Dispatch

## Task Identity
- project: <projectName> (<projectId>)
- task_id: <taskId>
- title: <taskTitle>
- priority: <P0|P1|P2|P3>

## Goal
<一句话目标>

## Project Summary
<3-6行，必要背景，不展开>

## Task Context
<当前任务已知上下文，尽量精准>

## Hard Constraints
- 只处理当前任务，不修改无关内容
- 遵循现有代码结构/技术栈
- <其他硬约束>

## Source-of-truth Docs
- <doc path 1>
- <doc path 2>

## Source-of-truth Files
- <file path 1>
- <file path 2>

## Deliverables
- <交付物1>
- <交付物2>

## Acceptance Criteria
- <验收标准1>
- <验收标准2>

## Fallback Rule
- 若信息不足：先暂停并说明缺什么，不要自行猜测

## Output Format (Required)
在回复末尾必须包含：

```completion_signal
task_id: <taskId>
status: done | blocked
summary: <一句话总结>
deliverables: <逗号分隔结果或产物路径>
next_step: <done 写 N/A；blocked 写阻塞点与建议>
```
```

---

## Field Guidelines

| 字段 | 必填 | 说明 |
|------|------|------|
| Task Identity | ✅ | 任务标识，用于追踪 |
| Goal | ✅ | 一句话说明目标，帮助 subagent 聚焦 |
| Project Summary | ⚠️ | 复杂项目必填，简单项目可省略 |
| Task Context | ✅ | 当前任务相关的上下文，避免 subagent 瞎猜 |
| Hard Constraints | ✅ | 必须遵守的规则，防止越界操作 |
| Source-of-truth Docs | ⚠️ | 有则提供，帮助 subagent 理解项目 |
| Source-of-truth Files | ⚠️ | 有则提供，指明关键文件路径 |
| Deliverables | ✅ | 明确产出物，验收依据 |
| Acceptance Criteria | ✅ | 明确验收标准，避免理解偏差 |
| Fallback Rule | ✅ | 防止 subagent 自行猜测导致错误 |
| Output Format | ✅ | 标准化输出，便于主 Agent 解析 |

---

## Usage Example

```markdown
# Task Dispatch

## Task Identity
- project: 测试项目2 (test-project-2)
- task_id: TEST2-001
- title: 创建测试文档1
- priority: P2

## Goal
在 ClawBoard 的 docs 目录下创建测试文档 test-doc-1.md

## Project Summary
ClawBoard 是一个任务看板系统，用于管理项目和任务。
文档存放在 docs/ 目录下。

## Task Context
这是一个测试任务，用于验证任务调度流程是否正常工作。

## Hard Constraints
- 只创建指定文件，不修改其他文件
- 文件内容可以简单，但必须存在

## Source-of-truth Docs
- /root/ClawBoard/README.md

## Source-of-truth Files
- /root/ClawBoard/docs/

## Deliverables
- /root/ClawBoard/docs/test-doc-1.md

## Acceptance Criteria
- 文件已创建
- 文件为空白或包含标题

## Fallback Rule
- 若目录不存在，先创建目录再创建文件

## Output Format (Required)
在回复末尾必须包含：

```completion_signal
task_id: TEST2-001
status: done | blocked
summary: <一句话总结>
deliverables: <逗号分隔结果或产物路径>
next_step: <done 写 N/A；blocked 写阻塞点与建议>
```
```

---

## Parsing Completion Signal

主 Agent 收到 subagent 回复后，解析 `completion_signal` 块：

```python
def parse_completion_signal(response: str) -> dict:
    """Parse completion_signal block from subagent response."""
    import re
    
    pattern = r'```completion_signal\n(.*?)\n```'
    match = re.search(pattern, response, re.DOTALL)
    
    if not match:
        return {"status": "unknown", "error": "No completion_signal found"}
    
    signal_text = match.group(1)
    result = {}
    
    for line in signal_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip()
    
    return result
```

---

## Integration with task-dispatch

在 `SKILL.md` 的派发流程中：

1. 从任务数据提取字段
2. 填充模板
3. 调用 `sessions_spawn`，将模板内容作为 `task` 参数
4. 等待 subagent 完成
5. 解析 `completion_signal`
6. 根据状态更新任务