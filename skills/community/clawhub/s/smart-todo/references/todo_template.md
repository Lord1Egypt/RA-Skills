# 代办模板

## 活动代办 (active.md)

```markdown
# 活动代办列表

## 统计
- 总计: {total_count}
- P0: {p0_count}
- P1: {p1_count}
- 进行中: {in_progress_count}
- 未开始: {not_started_count}
- 暂停: {paused_count}

## 代办列表

{todo_list}

---
最后更新: {last_updated}
```

## 单个代办条目格式

```markdown
### [{id}] {priority} {name}
**状态**: {status}
**创建时间**: {created_at}
**更新时间**: {updated_at}
**预估时间**: {estimated_time}分钟

**原始描述**:
{original_description}

**确认理解**:
{confirmed_understanding}

**上下文**:
{context}

**标签**: {tags}

---
```

## 归档代办 (archive.md)

```markdown
# 归档代办列表

## 统计
- 总计: {total_count}
- 已完成: {completed_count}
- 已终止: {terminated_count}

## 归档列表

{archive_list}

---
最后更新: {last_updated}
```

## 归档条目格式

```markdown
### [{id}] {priority} {name}
**原状态**: {original_status}
**创建时间**: {created_at}
**完成/终止时间**: {completed_at}
**归档原因**: {archive_reason}

**原始描述**:
{original_description}

**确认理解**:
{confirmed_understanding}

**上下文**:
{context}

---
```
