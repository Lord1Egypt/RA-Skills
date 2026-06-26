# TESP Templates

## Layer 1

```text
✅ 已接收 | TESP v1.0.2 | 预计 X 分钟可完成
场景：[1-3句话概括问题总结或者前置场景]
目标：[1-3句话概括任务方向或者目标]
```

## Layer 2 — in progress

```text
⏳ 进行中(2/5)
[当前处于第2步] - [子任务目标] - [预计还需用时]
```

## Layer 2 — subtask finished

```text
⏳ 子任务2/5已完成
[第2步任务1句话总结]
[开始启动3/5] - [预计还需用时]
```

## Layer 2 — blocked

```text
🚨 阻塞(4/5)
原因：[X]
需要你决定：[选项A / 选项B]
```

## Layer 2 — final completion

```text
✅ 完成 | [结果摘要] - [与当初设计用时相差多少]
📁 产出位置：[路径或链接]
```

## Layer 3 — active board schema

```text
| ID | 任务 | 状态 | 阶段 | 启动时间 | 预计完成 | 产出 |
```

Allowed active statuses:
- `🔄进行中`
- `🚨阻塞`
- `⏸️等待确认`

## Layer 3 — archive board schema

```text
| ID | 任务 | 最终状态 | 最终阶段 | 启动时间 | 完成时间 | 产出 |
```

## Audit checklist
A TESP rollout or audit should check:
1. protocol file exists
2. registry entry exists
3. visible Layer 1 version matches current baseline
4. numeric progress is used
5. active board is clean
6. completed work is archived
7. low-token governance defaults are followed
