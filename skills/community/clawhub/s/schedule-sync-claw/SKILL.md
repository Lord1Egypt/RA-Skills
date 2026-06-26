---
name: schedule-sync-claw
description: "飞书日历智能协作 Skill。核心能力：(1) 智能约会——查询多人空闲时间、自动创建会议并发送邀请，(2) 日程同步——监听/查询日历变更并同步，(3) 会议背景预置——会前自动拉取相关飞书文档和会议纪要。激活场景：用户提到安排会议、约人开会、查空闲时间、日程协调、会议邀请、预置背景资料、会前准备、查日历、创建日程、发日历邀请等。也适用于自然语言如帮我约张三开会、查一下这周谁有空、下午3点有个会帮我准备资料等请求。通用 Skill，任何 agent 均可调用。依赖飞书日历 v4 API 和飞书文档 API。"
---

# 日程协办虾 — 飞书日历智能协作

## 执行策略（按优先级）

### 🥇 优先级 1：飞书插件工具（openclaw-lark）

检查环境是否安装了 `openclaw-lark` 插件。该插件提供以下原生工具：

| 工具名 | 核心能力 |
|--------|---------|
| `feishu_calendar_event` | 创建/查询/修改/删除日程、搜索日程、回复邀请 |
| `feishu_calendar_freebusy` | 查询 1-10 个用户的空闲忙状态 |
| `feishu_calendar_event_attendee` | 添加参会人、查看参会人列表 |
| `feishu_calendar_calendar` | 查询/管理日历列表 |

**判断条件**：当前环境中可用 `feishu_calendar_event` 工具时，直接使用插件工具完成所有日历操作，跳过优先级 2。

> ⚠️ 插件工具使用**用户身份**（user_access_token），需用户完成 OAuth 授权。如授权未完成，工具会自动引导用户授权。

**插件工具使用要点**（详见 [feishu-calendar SKILL](~/.openclaw/extensions/openclaw-lark/skills/feishu-calendar/SKILL.md)）：
- 时间格式：ISO 8601（带时区），如 `2026-03-27T14:00:00+08:00`
- `user_open_id` 必填：值取消息上下文的 SenderId（`ou_xxx`），确保发起人出现在参会人列表
- 参会人 ID 统一用 `open_id`（`ou_xxx` 格式）
- 创建日程时可直接传 `attendees`（无需分两步）
- `list` 操作自动展开重复日程，时间区间不超过 40 天

### 🥈 优先级 2：API 脚本方式

当飞书插件未安装或不可用时，退化为使用 API 脚本。

**前置要求**：
- 环境变量 `FEISHU_APP_ID`、`FEISHU_APP_SECRET`
- 应用后台已开启 `calendar:calendar` 权限
- 详见 [references/feishu-calendar-api.md](references/feishu-calendar-api.md)
- 脚本：[scripts/feishu-calendar.sh](scripts/feishu-calendar.sh)

> ⚠️ API 脚本方式使用 `tenant_access_token`（应用身份），只能操作应用日历，无法查询用户 freebusy 或读取用户个人日历。

---

## 工作流

### 工作流 1：创建会议并邀请成员

触发：用户要创建会议、安排日程、约人开会

**步骤：**

1. **解析请求** — 提取：参与者（姓名/open_id）、会议主题、开始时间、结束时间、会议描述
2. **查询参与者 open_id** — 如只有姓名，通过 `feishu_search_user` 查找
3. **查空闲（可选但推荐）** — 创建前查询参会人是否有时间冲突
4. **创建日程** — 按优先级选择：
   - **插件方式**：调用 `feishu_calendar_event` with action=create
   - **脚本方式**：先获取 token + 日历 ID → 创建 event → 单独添加 attendees
5. **输出摘要** — 会议时间、主题、参会者、日程链接

**关键注意（仅脚本方式）**：
- `visibility` 必须是字符串 `"default"`，不能是数字 `0`
- `timestamp` 必须是秒级时间戳字符串（如 `"1774596600"`）
- 创建 event 不接受 `attendees`，必须先创建再单独添加
- 插件方式无此限制，可直接传 attendees

### 工作流 2：查询空闲时间

触发：用户要找时间开会、查某人有空没

**步骤：**

1. **确认参与者** — 收集需要查询的用户的 open_id
2. **确定时间范围** — 默认查询未来 5 个工作日
3. **查询忙闲** — 按优先级选择：
   - **插件方式**：调用 `feishu_calendar_freebusy`（支持 1-10 人批量查询）
   - **脚本方式**：告知用户需要 OAuth 授权，引导安装飞书插件
4. **计算共同空闲时段** — 取各参与者空闲时段交集，按会议时长筛选
5. **推荐时间** — 展示 2-3 个可用时段，工作日上午优先

> ⚠️ 查询用户空闲忙状态**必须使用用户身份**（插件方式）。脚本方式（tenant_access_token）无法查询用户 freebusy。

### 工作流 3：日程查询与同步

触发：用户查日历 / "今天有什么会" / "这周安排"

**步骤：**

1. **确定时间范围** — 按请求解析（今天/本周/指定日期）
2. **查询日程** — 按优先级选择：
   - **插件方式**：调用 `feishu_calendar_event` with action=list（自动展开重复日程）
   - **脚本方式**：用 `scripts/feishu-calendar.sh list` 或直接 curl
3. **格式化输出** — 按时间排序，简洁展示（北京时间）

### 工作流 4：修改/删除日程

触发：用户要改时间、取消会议、更新会议信息

**步骤：**

1. **定位日程** — 通过 search 或 list 找到目标 event_id
2. **执行操作** — 按优先级选择：
   - **插件方式**：`feishu_calendar_event` with action=patch/delete
   - **脚本方式**：直接 curl 对应 API 端点
3. **确认结果** — 反馈操作是否成功

### 工作流 5：回复日程邀请

触发：用户要接受/拒绝/暂定某个会议邀请

**步骤：**

1. **获取 event_id** — 从日程列表中找到目标日程
2. **回复** — 调用 `feishu_calendar_event` with action=reply，传 `rsvp_status`（accept/decline/tentative）

> ⚠️ 回复邀请仅插件方式支持（需要用户身份）。

### 工作流 6：会议背景预置

触发：会议即将开始 / 用户要求准备会议资料 / "帮我看看XX会议的相关文档"

**步骤：**

1. **识别会议** — 从用户消息或日历中获取会议信息
2. **关键字提取** — 从会议主题提取核心关键词
3. **搜索相关文档** — 搜索飞书云文档、知识库、云空间文件
4. **整理背景摘要** — 文档标题、链接、摘要，按相关性排序
5. **输出** — 结构化背景资料清单

---

## 关键规则

- **时间格式统一**：内部处理用 `Asia/Shanghai` (UTC+8)，展示用北京时间（"下午3点"），不展示 UTC
- **插件优先**：有飞书插件时必须优先使用插件工具，退化为 API 脚本时明确告知用户限制
- **先查空闲再创建**：创建会议前尽量查 freebusy 避免时间冲突
- **去重优先**：创建前检查是否已有相同时间/主题的会议
- **对外操作先确认**：创建日程、邀请参会人等操作需先与用户确认细节

## 插件工具速查

| 用户意图 | 工具 | action | 必填参数 | 强烈建议 |
|---------|------|--------|---------|---------|
| 创建会议 | feishu_calendar_event | create | summary, start_time, end_time | user_open_id, attendees |
| 查日程 | feishu_calendar_event | list | start_time, end_time | - |
| 改日程 | feishu_calendar_event | patch | event_id | start_time/end_time |
| 搜日程 | feishu_calendar_event | search | query | - |
| 回复邀请 | feishu_calendar_event | reply | event_id, rsvp_status | - |
| 删日程 | feishu_calendar_event | delete | event_id | - |
| 查空闲 | feishu_calendar_freebusy | list | time_min, time_max, user_ids[] | - |
| 邀请参会人 | feishu_calendar_event_attendee | create | calendar_id, event_id, attendees[] | - |
| 查日历列表 | feishu_calendar_calendar | list | - | - |

## API 脚本速查（备选方案）

| 操作 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 获取 tenant token | POST | `/auth/v3/tenant_access_token/internal` | 应用身份认证 |
| 获取主日历 | GET | `/calendar/v4/calendars/primary` | tenant 下返回应用日历 |
| 创建日程 | POST | `/calendar/v4/calendars/{cal_id}/events` | 不含 attendees |
| 添加参会人 | POST | `/calendar/v4/calendars/{cal_id}/events/{evt_id}/attendees` | 创建后单独调用 |
| 查询日程 | GET | `/calendar/v4/calendars/{cal_id}/events?start_time=&end_time=` | 秒级时间戳 query 参数 |
| 更新日程 | PATCH | `/calendar/v4/calendars/{cal_id}/events/{evt_id}` | |
| 删除日程 | DELETE | `/calendar/v4/calendars/{cal_id}/events/{evt_id}` | |

Base URL: `https://open.feishu.cn/open-apis`

> 详细 API 参考见 [references/feishu-calendar-api.md](references/feishu-calendar-api.md)
