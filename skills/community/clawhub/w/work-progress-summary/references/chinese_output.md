# 中文输出模板

仅在用户使用中文时参考这些模板。
保持简洁，优先复述事实，不要补写未记录的内容。

## 记录成功

适用于 `record` 成功后。

模板：

```text
已记录 {date} 的工作，共 {recorded} 项：
1. {task_1}
2. {task_2}
```

如果存在非 `done` 状态，补充状态说明：

```text
其中：
- 进行中：{in_progress_tasks}
- 阻塞：{blocked_tasks}
```

## 修改成功

适用于 `replace-day` 成功后。

模板：

```text
已更新 {date} 的日报，当前共 {recorded} 项：
1. {task_1}
2. {task_2}
```

如果用户把当天日报清空，则回答：

```text
已清空 {date} 的日报记录。
```

## 单条任务更新成功

适用于 `update-entry` 成功后。

模板：

```text
已更新任务 #{entry_id}：
- 日期：{date}
- 事项：{task}
- 状态：{status}
```

如果 `details` 非空，再补一行：

```text
- 备注：{details}
```

## 单条任务删除成功

适用于 `delete-entry` 成功后。

模板：

```text
已删除任务 #{entry_id}：
- 日期：{date}
- 事项：{task}
```

## 历史版本查询

适用于 `entry-history`。

模板：

```text
任务 #{entry_id} 共记录了 {version_count} 个版本：
1. v{version} {action} {date} {task}
2. v{version} {action} {date} {task}
```

如果该任务已经被删除，可以补一句：

```text
该任务当前已不在日报中。
```

## 日期历史查询

适用于 `day-history`。

模板：

```text
{date} 的日报历史共涉及 {entry_count} 条任务、{version_count} 次变更：
1. 任务 #{entry_id}
- v{version} {action} {task}
- v{version} {action} {task}
```

如果某条任务当前已被删除，可以补一句：

```text
该任务当前已不在这天的日报中。
```

如果某条任务已被移到别的日期，可以补一句：

```text
该任务当前已移动到 {current_date}。
```

## 单日查询

适用于 `day-report`。

有记录时：

```text
{date} 的工作记录如下：
1. {task}（已完成）
2. {task}（进行中）
3. {task}（阻塞：{details}）
```

无记录时：

```text
{date} 还没有记录任何工作项。
```

## 周报汇总

适用于 `week-report`。

模板：

```text
本周工作进度（{week_start} 到 {week_end}）：

{date_1}
- {task}
- {task}

{date_2}
- {task}

本周统计：
- 已完成：{done_count}
- 进行中：{in_progress_count}
- 阻塞：{blocked_count}
```

如果一周内某天没有记录，不必强行列出；只有在用户明确要求“按天全列”时再保留空天。

## 多天混合请求

如果用户一条消息里同时要求“记录今天工作”和“顺便总结本周”，先执行 `record`，再执行
`week-report`，最后按下面顺序回答：

1. 先确认已记录成功
2. 再给出本周汇总
