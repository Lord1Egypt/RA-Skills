---
name: work-schedule-assistant
description: 自动保存工作安排、会议、待办和相关附件，维护带附件链接的固定日程台账，并生成每日工作提醒。
version: 1.1.0
---

# 工作日程助手

## 目标

把用户在聊天中发送的工作消息持续整理到固定位置，并在用户查询或定时任务触发时生成当天工作提醒。

默认数据目录：

```text
~/.openclaw/workspace/work-schedule/
```

其中：

- `schedule.json`：结构化日程数据
- `工作日程.md`：方便用户随时查看的日程台账
- `history.jsonl`：新增、修改、完成和取消的操作记录
- `attachments/`：与日程事项关联的稳定附件副本

可通过环境变量 `WORK_SCHEDULE_HOME` 修改保存目录，通过 `WORK_SCHEDULE_TZ` 修改工作时区；默认时区为 `Asia/Shanghai`。

## 触发规则

以下消息必须使用本 Skill：

- 以“工作：”“日程：”“待办：”“会议：”“提醒：”开头
- 包含明确工作任务和日期、时间、截止日期或会议安排
- 用户要求添加、修改、完成、取消或查询工作日程
- 用户询问今天、明天、本周或逾期工作
- 定时任务要求生成当天工作提醒

对于明显的工作安排，即使没有前缀，也应识别并保存，例如：

- “明天下午三点开项目推进会”
- “周五前提交教学大纲”
- “下周联系合作医院确认数据”

不要把闲聊、新闻、知识问答、他人的日程或没有行动含义的信息自动保存。不能确定是否属于用户工作任务时，先询问一句。

## 消息处理流程

### 1. 提取字段

从消息中提取：

- `title`：简洁、动词开头的工作事项
- `date`：`YYYY-MM-DD`；无明确日期时留空
- `time`：`HH:MM`；无明确时间时留空
- `end_time`：可选
- `deadline`：可选，ISO 日期或日期时间
- `priority`：高、中、低；默认中
- `category`：会议、教学、科研、行政、沟通、材料、出差或其他
- `notes`：地点、参与人、材料、前置事项等
- `source`：尽量保存用户原始消息

解析“今天、明天、后天、周五、下周一”等相对日期时，以当前会话时区为准，并在写入前转成绝对日期。

如果缺少日期但任务本身明确，不要丢弃，保存到“待安排日期”。如果日期存在歧义且会影响执行，先向用户确认。

### 2. 保存事项

定位本 Skill 的安装目录，然后运行：

```bash
python3 scripts/work_schedule.py add \
  --title "提交教学大纲" \
  --date "2026-07-31" \
  --time "17:00" \
  --priority "高" \
  --category "教学" \
  --source "周五下午五点前提交教学大纲"
```

根据实际字段增减参数。不要用 shell 拼接未转义的用户输入；使用参数数组或安全工具调用。

脚本会自动去重、分配编号，并同步更新 JSON、Markdown 和历史记录。

### 3. 回复确认

保存成功后简洁回复：

```text
已加入工作日程：
7月31日 17:00｜提交教学大纲｜高优先级
```

如果任务没有日期：

```text
已加入“待安排日期”：联系合作医院确认数据。
```

不要在每次写入后输出整个日程表。

## 关联附件

当工作消息附带会议材料、通知、表格、Word、PDF、图片或其他相关文件时，读取 [references/attachment-handling.md](references/attachment-handling.md)。

先保存日程并取得事项编号，再关联附件：

```bash
python3 scripts/work_schedule.py attach \
  --id WS-20260731-001 \
  --file "/机器人下载的临时文件/会议通知.pdf" \
  --label "会议通知"
```

网络附件使用：

```bash
python3 scripts/work_schedule.py attach \
  --id WS-20260731-001 \
  --url "https://example.com/material.pdf" \
  --label "会议材料"
```

本地附件会复制到固定日程目录，网络附件保存为链接。`工作日程.md` 会在对应事项下生成可点击链接。

只有与工作事项直接相关且后续确有查看价值时才保存附件。普通聊天图片、表情、头像和无关文件不要关联。

## 查询和管理

### 查看今天

```bash
python3 scripts/work_schedule.py list --date today
```

### 查看明天

```bash
python3 scripts/work_schedule.py list --date tomorrow
```

### 查看本周

```bash
python3 scripts/work_schedule.py list --date week
```

### 查看全部未完成事项

```bash
python3 scripts/work_schedule.py list --date all
```

### 标记完成

先通过查询确认事项编号，再运行：

```bash
python3 scripts/work_schedule.py done --id WS-20260731-001
```

### 修改事项

```bash
python3 scripts/work_schedule.py update \
  --id WS-20260731-001 \
  --date "2026-08-01" \
  --time "09:00"
```

### 取消事项

取消前确认编号：

```bash
python3 scripts/work_schedule.py cancel --id WS-20260731-001
```

取消采用状态标记，不物理删除记录。

## 每日提醒

定时任务调用：

```bash
python3 scripts/work_schedule.py brief --date today
```

提醒内容包括：

1. 当天按时间排序的工作
2. 高优先级任务
3. 已逾期但未完成事项
4. 尚未安排日期的工作

如果当天没有事项、逾期事项和待安排事项，输出：

```text
今日暂无已登记工作安排。
```

首次安装后，读取 [references/setup-reminder.md](references/setup-reminder.md) 配置每天提醒。Cron 修改需要用户授权和 OpenClaw `operator.admin` 权限。

## 数据安全

- 不把工作日程发送到未指定的外部服务。
- 不存储密码、验证码、API Key 或身份证件信息。
- 用户消息包含敏感凭证时，保存任务描述但删除凭证内容。
- 不执行、解压或自动打开附件。
- 不下载用户只提供 URL 的网络附件，只保存明确的 HTTP/HTTPS 链接。
- 不覆盖整个台账来完成单项修改。
- 使用脚本管理数据，避免并发写入损坏。
- 对“删除全部日程”“清空历史”等请求必须再次确认；本 Skill 默认不提供物理删除。

## 时区

默认采用系统本地时区。用户明确指定时区时，按其要求解析；当前用户的常用工作时区可配置为 `Asia/Shanghai`。
