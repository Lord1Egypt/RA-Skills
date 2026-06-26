# 回复格式模板

所有回复使用纯文本格式，不使用 Markdown 语法。脚本输出即回复内容，直接发送。

## 安排日程 / 新增日程完成

```
[直接粘贴 schedule_crud.py add 的输出]

[直接粘贴 schedule_crud.py list 的输出]

是否需要为任务设置定时提醒？
```

## 查看完整日程

```
[直接粘贴 schedule_crud.py list 的输出]
```

脚本输出格式如下（自动生成，不要手写）：

```
━━━━━━━━━━━━━━━━
  日程表  |  2026-03-24 14:30 更新
━━━━━━━━━━━━━━━━

P0 — 重要且紧急
────────────────
  #1. CVPR Camera Ready [已设提醒]
     DDL: 3/28(周六) 19:59
     备注: 原始DDL为3/27 AOE
  #4. 毕业中期材料提交
     DDL: 3/30(周一)

P1 — 紧急不重要
────────────────
  (暂无)

P2 — 重要不紧急
────────────────
  #3. 学习Rust基础
     DDL: 4/30(周四)
     备注: 每周末2h

P3 — 不重要不紧急
────────────────
  (暂无)

━━━━━━━━━━━━━━━━
  共 3 项  P0:2  P1:0  P2:1  P3:0
━━━━━━━━━━━━━━━━
```

## 查看今日任务

```
[直接粘贴 schedule_crud.py list --today 的输出]
```

## 查看明日任务

```
[直接粘贴 schedule_crud.py list --tomorrow 的输出]
```

## 查看本周日程

```
[直接粘贴 schedule_crud.py list --week 的输出]
```

## 查看下周日程

```
[直接粘贴 schedule_crud.py list --next-week 的输出]
```

## 查看本月日程

```
[直接粘贴 schedule_crud.py list --month 的输出]
```

## 查看下月日程

```
[直接粘贴 schedule_crud.py list --next-month 的输出]
```

## 修改日程完成

```
[直接粘贴 schedule_crud.py update 的输出]

是否需要为任务设置定时提醒？
```

## 删除日程完成

```
[直接粘贴 schedule_crud.py delete 的输出]
```

## 设置提醒完成

```
已为「任务名」设置 YYYY-MM-DD HH:mm 的定时提醒。
```
