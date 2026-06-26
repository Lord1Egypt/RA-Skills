# Progress Tracking

## Required Files

Maintain these project-level records:

- `records/learning-progress.md`: current weak points and practice history.
- `records/YYYY-MM-DD-<source>-diagnosis.md`: one diagnosis per paper/photo batch/wrong-question batch.
- `weak-points/<topic-slug>.md`: one long-lived record per weak point.
- `knowledge-points/<topic-slug>.md`: reusable parent explanation and mastery evidence.
- `curriculum/progress.md`: learned scope, current unit, and exam range.
- `mistakes/school-mistakes.md`: school paper and official homework mistakes.
- `mistakes/system-mistakes.md`: mistakes from generated worksheets.

Use the local current date unless the user provides a date. Infer grade, semester, and phase from `memory/long-term.md`, `curriculum/school-calendar.md`, and `mistakes/index.md`.

## Status Values

- `观察中`: one possible issue, not enough evidence.
- `薄弱项`: repeated errors or high-confidence diagnosis.
- `补齐理解`: immediate explanation and validation passed; spaced review not proven.
- `待巩固`: mostly correct, needs spaced review.
- `已掌握`: two recent checks at 90% or above without major support.
- `复发`: repaired or mastered item clearly failed again.
- `复发待确认`: suspicious recurrence but evidence is not enough.

## Diagnosis Record Template

```markdown
# 批改诊断：<source>

- 日期：YYYY-MM-DD
- 学年：<school year>
- 年级：<grade>
- 学期：<grade semester>
- 学期时间段：YYYY-MM-DD 至 YYYY-MM-DD
- 学期阶段：<in_semester / midterm_window / final_window / semester_ended / winter_break / summer_break>
- 来源：<completed worksheet / photo / direct wrong questions / oral report>
- 范围：<items or topic>
- 总题数：<known/unknown>
- 正确数：<known/unknown>
- 总体判断：<one sentence>

## 错题明细

| 题号 | 题目 | 孩子答案 | 正确答案 | 结果 | 错题类型 | 可能原因 | 历史状态 | 复发判断 | 证据 | 置信度 | 补救动作 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 归因汇总

- <cause>: <count / representative item / judgment>

## 讲解与验证练习

### <priority cause>

讲解：

验证题：

## 下一步

- 更新薄弱项：
- 更新错题集：
- 下次练习：
- 复测标准：
- 是否复发：
```

## Weak Point Template

Each weak-point file should include:

- 当前状态
- 首次发现日期
- 最近证据日期
- 复发次数
- 关联知识点
- 下次复练日期
- 复练优先级
- 典型表现
- 可能原因
- 讲解策略
- 验证练习策略
- 复发处理策略
- 历史记录
- 下次动作

Update weak points only with evidence from actual mistakes or practice results.
