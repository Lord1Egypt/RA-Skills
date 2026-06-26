---
name: skill-a-create-meeting
description: "【会议创建总入口，必须优先触发】当用户提出任何新建会议、开会、约会、安排会议、预约会议、组会、周会、例会、讨论会、紧急会议、跨项目会议、循环会议相关需求时，必须优先使用此技能，而不要直接调用 tencent-meeting-skill。OpenClaw 负责意图分析和参数补全；本技能作为会议创建总控入口，负责协调后续流程：先由 OpenClaw 调用 tencent-meeting-skill 创建腾讯会议，再调用本技能完成 Gitea 会议目录、meta.yaml、agenda.md、仓库成员/邮箱查询、日志写入和邮件内容编排，最后由 OpenClaw 调用 imap-smtp-email 发送邀请邮件。只有当用户是在查询、修改、取消已有会议，或查看会议录制、转写、纪要时，才直接使用 tencent-meeting-skill。"
author: mayidan
---

# Skill-A: create_meeting — 会议创建总控入口技能

## 核心路由规则（非常重要）

**凡是用户要“新建一场会议”，都必须优先调用本技能。**

包括但不限于这些表达：
- 开个会
- 新建会议
- 约个会
- 安排一个会
- 预约会议
- 开组会 / 周会 / 例会
- 开紧急会议
- 开讨论会
- 今晚 11 点 40 建个会
- 晚上 11 点 30 开组会
- 从下周开始每周一开会
- 建一个跨项目会议

**不要在用户首次提出“新建会议”需求时直接调用 `tencent-meeting-skill`。**

### 只有以下场景，才直接调用 `tencent-meeting-skill`
- 查询已有会议详情
- 通过会议号查会议信息
- 修改已有会议
- 取消已有会议
- 查询参会人 / 邀请人 / 等候室
- 查询录制、转写、AI纪要

---

## 定位

本技能是 **会议创建总入口 / 总控技能**。

它 **不负责 LLM 分析**，也 **不直接操作腾讯会议或 SMTP**。

职责分工如下：

- **OpenClaw**
  - 理解用户自然语言
  - 补问缺失参数
  - 判断项目归属
  - 决定何时调用下游 skill

- **Skill-A（本技能）**
  - 作为“新建会议”场景的统一入口
  - 约束正确调用顺序
  - 在 Gitea 中创建会议目录与文件
  - 查询仓库成员与邮箱
  - 生成邀请邮件 HTML
  - 写日志
  - 把后续发信所需参数整理返回给 OpenClaw

- **tencent-meeting-skill**
  - 仅作为本技能下游依赖
  - 负责实际创建腾讯会议
  - 返回 `meeting_id / meeting_code / join_url`

- **imap-smtp-email**
  - 仅作为本技能下游依赖
  - 负责实际发送邀请邮件

---

## 配置要求

配置文件路径：`~/.config/skill-a-create-meeting/.env`

首次使用前运行：

```bash
bash setup.sh
```

---

## 调用前提

在调用本技能前，OpenClaw 必须先完成以下工作：

### 1. 解析用户意图
必须先从用户输入中确认这些信息：

- `time`：会议开始时间（ISO8601，带时区，默认 +08:00）
- `topic`：会议主题
- `repo`：目标仓库，如 `owner/repo`
- `category`：`single` 或 `cross-project`
- `organizer`：组织者 Gitea 用户名

### 2. 如有缺失，必须先追问用户
特别是以下情况必须先问清楚，不能直接跳过：

- 用户没说项目归属
- 用户没说会议主题
- 用户时间表达不清楚
- 用户是临时会议还是循环会议不明确

### 3. 先调用 tencent-meeting-skill 创建腾讯会议
拿到以下字段后，才能调用本技能：

- `meeting_id`
- `meeting_code`
- `join_url`

---

## 输入参数

必填参数：

- `time`
- `topic`
- `repo`
- `category`
- `organizer`
- `meeting_id`
- `meeting_code`
- `join_url`

可选参数：

- `duration`：默认 60 分钟
- `attendees`：逗号分隔的 Gitea 用户名列表；若不传，则自动取该仓库成员
- `meeting_type`：`ad-hoc` 或 `recurring`
- `series_id`：循环会议系列 ID

---

## 严格工作流（必须按顺序执行）

### 第一步：OpenClaw 先处理用户对话

OpenClaw 必须先完成：

- 识别这是“新建会议”需求
- 决定项目归属
- 补齐缺失参数
- 明确会议时间、主题、仓库、组织者

**不要在本技能内再次做自然语言分析。**

---

### 第二步：OpenClaw 调用 tencent-meeting-skill 创建腾讯会议

OpenClaw 应先调用腾讯会议 skill，拿到：

- `meeting_id`
- `meeting_code`
- `join_url`

---

### 第三步：调用本技能，完成 Gitea 侧落库与邮件内容准备

```bash
node main.js prepare \
  --time "2026-04-22T15:00:00+08:00" \
  --topic "v2 设计评审" \
  --repo "mayidan/project-test" \
  --category "single" \
  --organizer "mayidan" \
  --meeting-id "xxx" \
  --meeting-code "123456789" \
  --join-url "https://meeting.tencent.com/..." \
  --duration 60
```

本技能会完成以下动作：

1. 解析时间并确定会议目录名 `meetings/YYYY-MM-DD-HHMM/`
2. 自动获取仓库成员（如果 `--attendees` 未传）
3. 获取成员邮箱与仓库 owner 邮箱
4. 查找上次同类会议并生成 agenda 回顾（若无摘要能力则降级为“暂无参考记录”）
5. 创建 `meta.yaml` 和 `agenda.md`
6. 生成邀请邮件 HTML 与邮件主题
7. 写运行日志到 `aifusion-meta/logs/YYYY-MM-DD.jsonl`
8. 返回后续发信所需 JSON

---

### 第四步：OpenClaw 调用 imap-smtp-email 发送邀请邮件

收到本技能输出后，OpenClaw 必须使用 `imap-smtp-email` 发送：

- 收件人：`invite_email.to`
- 主题：`invite_email.subject`
- HTML 正文：`invite_email.html`

---

## 输出 JSON 说明

本技能返回 JSON，关键字段包括：

- `user_message`：展示给用户的话术
- `invite_email`：邀请邮件发件参数
- `repo_member_usernames`：仓库成员列表
- `repo_member_emails`：仓库成员邮箱列表
- `repo_owner_email`：仓库 owner 邮箱（供后续 Skill-B 发会前简报使用）
- `agenda_gitea_url`：议程文件链接
- `meeting_dir`：会议目录名

---

## 错误处理规则

| 错误场景 | 处理方式 |
|----------|----------|
| 参数缺失 | 直接报错，不执行任何写入 |
| 腾讯会议信息缺失 | 直接报错，不创建 Gitea 目录 |
| Gitea 写入失败 | 报错，由 OpenClaw 决定是否回滚会议 |
| 仓库成员邮箱部分缺失 | 不阻塞主流程，返回能拿到的邮箱 |
| 上次会议摘要不可用 | agenda 中写“暂无参考记录” |

---

## 典型触发示例

以下用户表达，**都应该优先触发本技能**：

| 用户说 | OpenClaw 应做什么 |
|--------|-------------------|
| "周三下午 3 点开个组会" | 解析时间 → 追问项目 → 调 tencent-meeting-skill → 调本技能 → 调邮件 skill |
| "晚上 11 点 30 开组会" | 解析时间 → 追问项目 → 调 tencent-meeting-skill → 调本技能 |
| "新建一个晚上 11 点 40 的会议" | 解析时间 → 追问主题/项目 → 调 tencent-meeting-skill → 调本技能 |
| "帮我约个今晚的会" | 解析时间 → 追问主题/项目 → 调 tencent-meeting-skill → 调本技能 |
| "从下周一起每周一下午 3 点开例会连续 10 周" | 解析循环规则 → 追问项目 → 调 tencent-meeting-skill → 调本技能 |
| "帮灵巧手项目约个会，后天上午 10 点" | 识别仓库 → 调 tencent-meeting-skill → 调本技能 |
| "开个跨项目全员会议，明天下午 2 点" | 识别 cross-project → 调 tencent-meeting-skill → 调本技能 |

---

## 非本技能直接处理的场景

以下场景不要优先调用本技能，而应直接使用 `tencent-meeting-skill`：

- “帮我查一下这个会议号对应的会议”
- “把明天下午那个会改到 4 点”
- “取消今晚那个会议”
- “帮我看看这场会议谁参加了”
- “导出这场会议的转写”
- “获取这场会议的 AI 纪要”
