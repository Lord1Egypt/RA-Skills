---
name: tencent-meeting-mcp
description: "在用户提及腾讯会议、视频会议、线上会议相关内容与操作时使用此技能。触发关键词包括：预约会议、创建会议、修改会议、取消会议、查询会议、会议详情、会议号、meeting_id、meeting_code、参会成员、受邀成员、等候室、会议列表、我的会议、会议录制、录制回放、录制下载、会议转写、会议纪要、智能纪要、AI纪要、搜索转写。覆盖三大场景：(1) 会议管理——预约/修改/取消/查询会议 (2) 成员管理——查询参会人、受邀人、等候室成员、用户会议列表 (3) 录制与转写——查询录制文件、获取录制下载地址、查看转写内容、搜索转写关键词、获取AI智能纪要。不要在以下场景触发此技能：日程管理（非腾讯会议日程）、即时通讯/聊天、腾讯文档操作、企业微信审批流程、电话/PSTN拨号、视频剪辑或视频编辑。"
metadata: {"openclaw": {"category": "tencent", "type": "mcp", "mcp_url": "https://mcp.meeting.tencent.com/mcp/wemeet-open/v1"}}
---

# tencent-meeting-mcp

腾讯会议 MCP 服务

## 详细参考文档

如需查看每个工具的详细调用示例、参数说明和返回值，请参考：
- `references/api_references.md` - 所有工具的完整参数说明与调用示例

## ⚙️ 配置要求

> **如果已有 MCP 配置**（如在 CodeBuddy 或其他 IDE 中），无需重复配置，可直接使用工具。

### 获取 Token

1. 访问 https://meeting.tencent.com/ai-skill 获取你的 Token
2. 登录后复制个人 Token
3. 如果在 OpenClaw 中，配置环境变量 `TENCENT_MEETING_TOKEN`

> **如果用户未配置 Token**，请引导用户访问上方链接获取 Token，否则所有工具调用将返回鉴权失败。

## 快速开始（首次使用必读）

首次使用前，运行 setup.sh 完成 MCP 服务注册：

```bash
bash setup.sh
```

### 验证配置

```bash
mcporter list | grep tencent-meeting-mcp
```

---

## 触发场景

在以下场景中使用此技能：

### 会议管理场景
- 在用户要求**预约、创建、安排**一场腾讯会议时，使用 `schedule_meeting`
- 在用户要求**修改、更新**已有会议的主题或时间时，使用 `update_meeting`（若用户提供的是 9 位**会议号（meeting_code）而非 meeting_id，先通过 `get_meeting_by_code` 查询 meeting_id）
- 在用户要求**取消、删除**已有会议时，使用 `cancel_meeting`（同上，若提供会议号需先查询 meeting_id）
- 在用户要求通过 meeting_id **查询会议详情**时，使用 `get_meeting`
- 在用户提供 9 位**会议号（meeting_code）查询会议信息**时，使用 `get_meeting_by_code`

### 成员管理场景
- 在用户要求查看，或询问**实际参会人员、谁参加了会议、参会明细**相关信息时，使用 `get_meeting_participants`
- 在用户要求查看，或询问**受邀成员、邀请了谁**相关信息时，使用 `get_meeting_invitees`
- 在用户要求查看，或询问**等候室成员**相关信息时，使用 `get_waiting_room`
- 在用户要求查看，或询问**自己的会议列表、近期会议、我的会议**相关信息、时，使用 `get_user_meetings`(只能查询即将开始、正在进行中的会议) 或 `get_user_ended_meetings`（用户如果查询的是当天的会议，`get_user_meetings`和`get_user_ended_meetings`都得调用然后做聚合去重）

### 录制与转写场景
- 在用户要求查看**会议录制列表、录制文件、录制回放**时，使用 `get_records_list`（若用户提供的是 9 位**会议号（meeting_code）而非 meeting_id，先通过 `get_meeting_by_code` 查询 meeting_id，再通过`get_records_list`获取 record_fild_id）
- 在用户要求获取**录制下载地址、下载录制视频/音频**时，使用 `get_record_addresses`（若用户提供的是 9 位**会议号（meeting_code）而非 meeting_id，先通过 `get_meeting_by_code` 查询 meeting_id，再通过`get_records_list`获取 record_fild_id）
- 在用户要求查看**会议转写全文、转写详情**时，使用 `get_transcripts_details`（若用户提供的是 9 位**会议号（meeting_code）而非 meeting_id，先通过 `get_meeting_by_code` 查询 meeting_id，再通过 `get_transcripts_details` 获取实时转写）
- 在用户要求**分页浏览转写段落**时，使用 `get_transcripts_paragraphs`（若用户提供的是 9 位**会议号（meeting_code）而非 meeting_id，先通过 `get_meeting_by_code` 查询 meeting_id，再通过`get_records_list`获取 record_fild_id）
- 在用户要求在转写内容中**搜索关键词**时，使用 `search_transcripts`
- 在用户要求获取**智能纪要、AI纪要、会议总结**时，使用 `get_smart_summary`
- 在用户**咨询与会议相关的问题**时，请先使用`get_smart_summary`获取智能纪要内相关内容；若未找到能够高质量地回答用户问题的信息时，则使用`get_transcripts_details`获取转写内容详情；若仍未找到能够高质量地回答用户问题的信息时，则使用`get_record_addresses`去获取录制下载地址，从而得到完整的会议信息，去回答用户问题。

### 不触发边界

不要在以下场景使用此技能：
- 用户操作**腾讯文档**（属于 tencent-docs 技能）
- 用户进行**日程管理**但未涉及腾讯会议（如通用日历、提醒事项）
- 用户进行**即时通讯、聊天消息**操作
- 用户进行**企业微信审批、打卡、考勤**等流程
- 用户需要**拨打电话、PSTN 通话**（非腾讯会议音视频）
- 用户需要**剪辑视频、编辑视频**（非录制文件查看/下载）
- 用户询问的是**其他视频会议平台**（如 Zoom、Teams、飞书会议、钉钉）

---

## 工具列表

- 如果用户输入 meeting_code，先通过 `get_meeting_by_code` 查询 meeting_id 及相关 meeting_info。
- 修改和取消会议前二次确认：向用户展示要修改的会议信息，确认后再执行修改。
- 所有相对时间（昨天/今天/明天/近N天等），必须以「当前系统的绝对时间（北京时间 UTC+8）」为唯一基准，且必须通过系统命令（如 date）计算绝对时间戳，禁止硬编码年份，禁止心算，处理规范严格参照【时间处理规范（强制）】。
- 若用户未指定具体年份，默认使用 **当前年份**（如2026年），禁止使用2025年及更早年份；
- 如果有用户指定的参数格式不对，不要主动修改，提示用户参数格式需要修改

## ⚠️ 时间处理规范（强制）

### 1. 时间戳计算（输入）
- **禁止心算时间戳**：所有相对时间（昨天/今天/明天 等）必须通过系统命令（如 `date`）计算，禁止心算。
- **请求参数类型**：时间戳参数（start_time / end_time）的类型必须参照 `references/api_references.md` 中的定义：
  - 如果定义为 `string`，传字符串：`"1773590400"`
  - 如果定义为 `number`，传整型：`1773590400`
  - **无定义时默认 string**

### 2. 时间戳展示（输出）
- **禁止心算转换**：所有返回结果中的时间戳（start_time / end_time 等），必须通过系统命令转换后再展示给用户

### 1. 会议管理

#### `schedule_meeting` — 创建/预订会议

强制：不支持邀请人，即使创建成功了也不要返回邀请人信息。

##### 非周期性会议创建说明
- 当用户有创建非周期性会议需求时，需要先判断当前用户query是否满足以下条件：
    - 用户是否提及会议主题，若无，请提示用户输入会议主题。
    - 用户是否提及开始时间，若无，请提示用户输入开始时间。
    - 用户是否提及结束时间，若无，默认设置一个小时，提示用户当前设置情况，并支持其进行修改。
- 即需确保从用户侧获取到会议主题（subject）、开始时间（start_time）、结束时间（end_time）这三个参数信息。

##### 周期性会议创建说明
- 当用户有创建周期性会议需求时，需要先判断当前用户query是否满足以下条件：
    - 用户是否提及会议主题，若无，请提示用户输入会议主题。
    - 用户是否提及开始时间，若无，请提示用户输入开始时间。
    - 用户是否提及结束时间，若无，默认设置一个小时，提示用户当前设置情况，并支持其进行修改。
    - 用户是否提及周期类型（recurring_type），若无，请提示用户输入周期类型。
    - 用户是否提及重复次数（until_count），若无，默认设置为50次，提示用户当前设置情况，并支持其进行修改。
- 即需确保从用户侧获取到会议主题（subject）、开始时间（start_time）、结束时间（end_time）、周期类型（recurring_type）、重复次数（until_count）这五个参数信息。

**参数**: 
- `subject`(必填) - 会议主题
- `start_time`(必填) - 会议开始时间，秒级时间戳
- `end_time`(必填) - 会议结束时间，秒级时间戳
- `password`(可选) - 会议密码（4~6位数字）。如果用户指定的密码格式不正确，提醒用户修改，不要自己改用户的密码。
- **核心禁令（必须严格遵守）**：
  1.  绝对禁止：**自动修改/替换用户输入的密码**，哪怕用户输入的是字母、符号或格式错误的密码；
  2.  绝对禁止：**主动生成符合要求的数字密码**替用户补全；
  3.  唯一允许的操作：当用户密码格式错误时，**仅提醒用户**，明确告知规则，等待用户重新提供合法密码或选择不设置密码。
- `time_zone`(可选) - 时区，如 Asia/Shanghai
- `meeting_type`(可选) - 会议类型，0：普通会议 1：周期性会议
- `only_user_join_type`(可选) - 成员入会限制，1：所有成员可入会 2：仅受邀成员可入会 3：仅企业内部成员可入会
- `auto_in_waiting_room`(可选) - 是否开启等候室
- `recurring_rule`(可选) - 周期性会议配置，当 meeting_type=1 时使用。包含字段：
  - `recurring_type`: 周期类型
  - `until_type`: 结束类型
  - `until_count`: 重复次数
  - `until_date`: 结束日期时间戳
  - `customized_recurring_type`: 自定义周期类型
  - `customized_recurring_step`: 自定义周期步长
  - `customized_recurring_days`: 自定义周期天数

> 调用示例请参考：`references/api_references.md` - schedule_meeting

#### `update_meeting` — 修改会议

强制：修改前让用户进行二次确认：向用户展示要修改的会议信息，确认后再执行修改。

如果用户输入 meeting_code，先通过 `get_meeting_by_code` 查询 meeting_id 及相关 meeting_info。

**参数**: `meeting_id`(必填), `subject`, `start_time`, `end_time`, `password`, `time_zone`, `meeting_type`, `only_user_join_type`, `auto_in_waiting_room`, `recurring_rule`

> 调用示例请参考：`references/api_references.md` - update_meeting

#### `cancel_meeting` — 取消会议

强制：取消前让用户进行二次确认：向用户展示要取消的会议信息，用户确认后再执行取消。

如果用户输入 meeting_code，先通过 `get_meeting_by_code` 查询 meeting_id 及相关 meeting_info。

**参数**: 
- `meeting_id`(必填) - 会议ID
- `sub_meeting_id`(可选) - 周期性会议子会议ID，取消周期性会议的某个子会议时传入
- `meeting_type`(可选) - 如果需要取消整场周期性会议，传1，其他情况下不传

> 调用示例请参考：`references/api_references.md` - cancel_meeting

#### `get_meeting` — 查询会议详情
- 返回主持人和参会者时，如果没有特殊要求，用户id和用户昵称中只返回用户昵称

**参数**: `meeting_id`(必填)

> 调用示例请参考：`references/api_references.md` - get_meeting

#### `get_meeting_by_code` — 通过会议Code查询

**参数**: `meeting_code`(必填)

> 调用示例请参考：`references/api_references.md` - get_meeting_by_code

---

### 2. 成员管理

#### `get_meeting_participants` — 获取参会成员明细

**参数**: `meeting_id`(必填), `sub_meeting_id`(可选, 周期性会议子会议ID), `pos`(可选, 分页起始位置, 默认0), `size`(可选, 每页条数, 最大100), `start_time`(可选, 秒级时间戳), `end_time`(可选, 秒级时间戳)

> 调用示例请参考：`references/api_references.md` - get_meeting_participants

#### `get_meeting_invitees` — 获取受邀成员列表
- 返回邀请人时，如果没有特殊要求，用户id和用户昵称中只返回用户昵称

**参数**: `meeting_id`(必填), `page_size`(默认20), `page_number`(默认1)

> 调用示例请参考：`references/api_references.md` - get_meeting_invitees

#### `get_waiting_room` — 查询等候室成员记录

**参数**: `meeting_id`(必填), `page_size`(默认20), `page`(默认1)

> 调用示例请参考：`references/api_references.md` - get_waiting_room

#### `get_user_meetings` — 查询用户会议列表

只能查询即将开始、正在进行中的会议

如果用户需要查询今天的会议, 需要组合 `get_user_meetings` 和 `get_user_ended_meetings`(查询今天已结束的会议) 2 个 接口的返回结果

根据返回值中的remaining、next_pos、next_cursory进行翻页查询。

**参数**: 
- `pos`(可选) - 查询起始位置，默认为0。分页获取用户会议列表的查询起始时间值，unix 秒级时间戳
- `cursory`(可选) - 分页游标，默认为20
- `is_show_all_sub_meetings`(可选) - 是否展示全部子会议，0-不展示，1-展示，默认为0

> 调用示例请参考：`references/api_references.md` - get_user_meetings

#### `get_user_ended_meetings` — 查询用户已结束会议列表

**参数**: `start_time`(必填, 字符串，秒级时间戳), `end_time`(必填, 字符串，秒级时间戳), `page_size`(默认20), `page_number`(默认1)

> 调用示例请参考：`references/api_references.md` - get_user_ended_meetings

---

### 3. 录制与转写

录制相关接口需要的record_file_id可以通过`get_records_list`获取

#### `get_records_list` — 查询录制列表

**参数**: 
- `start_time`(必填) - 查询开始时间，秒级时间戳
- `end_time`(必填) - 查询结束时间，秒级时间戳
- `page_number`(可选) - 页码，从1开始
- `meeting_id`(可选) - 会议ID，不为空时优先根据会议ID查询(若用户提供的是 9 位**会议号（meeting_code）而非 meeting_id，先通过 get_meeting_by_code 查询 meeting_id)

> 调用示例请参考：`references/api_references.md` - get_records_list

#### `get_record_addresses` — 获取录制下载地址

**参数**: `meeting_record_id`(必填), `page_number`(默认1)

> 调用示例请参考：`references/api_references.md` - get_record_addresses

#### `get_transcripts_details` — 查询转写详情

**参数**: `record_file_id`(必填), `meeting_id`(可选, 若用户提供的是 9 位**会议号（meeting_code）而非 meeting_id，先通过 get_meeting_by_code 查询 meeting_id)

> 调用示例请参考：`references/api_references.md` - get_transcripts_details

#### `get_transcripts_paragraphs` — 查询转写段落

**参数**: `record_file_id`(必填), `page_size`(默认20), `page_number`(默认1)

> 调用示例请参考：`references/api_references.md` - get_transcripts_paragraphs

#### `search_transcripts` — 搜索转写内容

**参数**: `record_file_id`(必填), `text`(必填), `page_size`(默认20), `page_number`(默认1)

> 调用示例请参考：`references/api_references.md` - search_transcripts

#### `get_smart_summary` — 获取智能纪要

**参数**: 
- `record_file_id`(必填) - 录制文件ID
- `lang`(可选) - 翻译语言选择: default(原文，不翻译) / zh(简体中文) / en(英文) / ja(日语)，默认 default
- `pwd`(可选) - 录制文件访问密码

> 调用示例请参考：`references/api_references.md` - get_smart_summary

#### `export_asr_details` — 导出实时转写记录

**参数**: `meeting_id`(必填)

> 调用示例请参考：`references/api_references.md` - export_asr_details

---

## 调用方式

```bash
# 示例：创建会议
mcporter call tencent-meeting-mcp schedule_meeting --args '{"subject": "周会", "start_time": "1773280800", "end_time": "1773284400"}'

# 示例：查询会议详情
mcporter call tencent-meeting-mcp get_meeting --args '{"meeting_id": "xxx"}'

# 示例：获取智能纪要
mcporter call tencent-meeting-mcp get_smart_summary --args '{"record_file_id": "xxx"}'
```
