---
name: work-mail-notifier
description: QQ邮箱工作邮件监控与标注已读。当用户提到工作邮件通知、邮件日报、新邮件提醒、或需要标注邮件已读时触发。
---

# Work Mail Notifier

监控 QQ 邮箱「其他文件夹」下的所有子文件夹，新邮件实时推送，已读邮件支持序号标注。

## 核心脚本

- `scripts/work_mail_notifier.py` — 拉取自上次 anchor 至当前的所有新邮件，推送通知
- `scripts/mark_read.py` — 按序号将邮件标记为已读
- `scripts/show_body.py` — 按序号显示邮件正文

## 工作流程

### 推送新邮件通知

```
python3 scripts/work_mail_notifier.py
```

- **Anchor 机制**：上次通知的最晚邮件时间作为起点，避免邮件因QQ邮箱延迟收取而漏报
- 无新邮件时输出 `NO_REPLY`
- 有新邮件时按「告警/风险 → 失败/异常 → 普通」分组输出

### 按序号标已读

```
python3 scripts/mark_read.py <序号> [序号...]
```

示例：`python3 scripts/mark_read.py 01 03 05`

- 序号来自最近一次通知的显示顺序
- 支持单个或多个序号，以空格分隔
- 记录文件：`~/.openclaw/workspace/data/last_notification.json`

## 通知分组规则

- **告警/风险**：subject 含「告警、delay warning、warning、block」
- **失败/异常**：subject 含「Fail、FAIL、fail、失败、异常」
- **普通**：其余邮件

## 标注已读指令模式

用户可通过自然语言指令触发，如：

- "已读 07 08"
- "标记 09 10 为已读"
- "把第 3 封标已读"



## 按序号显示正文

```
python3 scripts/show_body.py <序号> [序号...]
```

示例：`python3 scripts/show_body.py 01 03`

显示对应序号邮件的正文内容，支持多封一并显示。

## 自然语言指令汇总

| 意图 | 示例 | 脚本 |
|------|------|------|
| 标已读 | "已读 01 03" | mark_read.py |
| 看正文 | "正文 01" / "01 03 正文" | show_body.py |
