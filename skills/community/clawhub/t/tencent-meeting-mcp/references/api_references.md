# 腾讯会议 MCP 工具完整参考

本文件包含所有工具的详细参数说明、调用示例与返回值说明。

---

## 会议管理

### 1. `schedule_meeting` — 创建/预订会议

**功能**：创建一个新的腾讯会议。

**参数**：

| 参数                                         | 类型 | 必填 | 默认值 | 取值范围/说明 |
|--------------------------------------------|------|------|--------|--------------|
| `subject`                                  | string | ✅ | - | 会议主题 |
| `start_time`                               | string | ✅ | - | 会议开始时间，秒级时间戳 |
| `end_time`                                 | string | ✅ | - | 会议结束时间，秒级时间戳 |
| `password`                                 | string | ❌ | - | 会议密码（4~6位数字） |
| `time_zone`                                 | string | ❌ | - | 时区，遵循 Oracle-TimeZone 标准，例如：Asia/Shanghai |
| `meeting_type`                             | number | ❌ | 0 | 0：普通会议；1：周期性会议 |
| `only_user_join_type`                      | number | ❌ | - | 1：所有成员可入会；2：仅受邀成员可入会；3：仅企业内部成员可入会 |
| `auto_in_waiting_room`                     | boolean | ❌ | false | true：开启等候室；false：不开启等候室 |
| `recurring_rule`                           | object | ❌ | - | 周期性会议配置，当 meeting_type=1 时使用（见下方子字段） |
| `recurring_rule.recurring_type`            | number | ❌ | - | 周期类型：0-每天、1-周一至周五、2-每周、3-每两周、4-每月 |
| `recurring_rule.until_type`                | number | ❌ | - | 结束类型：0-按日期结束、1-按次数结束 |
| `recurring_rule.until_count`               | number | ❌ | - | 重复次数（1-50次），当 until_type=1 时必填 |
| `recurring_rule.until_date`                | number | ❌ | - | 结束日期时间戳（秒级），当 until_type=0 时必填 |
| `recurring_rule.customized_recurring_type` | number | ❌ | - | 自定义周期类型（保留字段） |
| `recurring_rule.customized_recurring_step` | number | ❌ | - | 自定义周期步长（保留字段） |
| `recurring_rule.customized_recurring_days` | number | ❌ | - | 自定义周期天数（保留字段） |

**调用示例**：
```bash
# 普通会议
mcporter call tencent-meeting-mcp schedule_meeting --args '{"subject": "产品周会", "start_time": "1773280800", "end_time": "1773284400"}'

# 周期性会议（每周开会，共重复5次）
mcporter call tencent-meeting-mcp schedule_meeting --args '{
  "subject": "每周例会",
  "start_time": "1773280800",
  "end_time": "1773284400",
  "meeting_type": 1,
  "recurring_rule": {
    "recurring_type": 2,
    "until_type": 1,
    "until_count": 5
  }
}'

# 周期性会议（每两周开会，共重复50次）
mcporter call tencent-meeting-mcp schedule_meeting --args '{
  "subject": "每双周例会",
  "start_time": "1773280800",
  "end_time": "1773284400",
  "meeting_type": 1,
  "recurring_rule": {
    "recurring_type": 3,
    "until_type": 1,
    "until_count": 50
  }
}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `meeting_number` | int64 | 会议数量 |
| `meeting_info_list` | array | 会议列表 |
| `meeting_info_list[].subject` | string | 会议主题 |
| `meeting_info_list[].meeting_code` | string | 会议 App 的呼入号码 |
| `meeting_info_list[].password` | string | 会议密码 |
| `meeting_info_list[].start_time` | string | 会议开始时间戳（秒） |
| `meeting_info_list[].end_time` | string | 会议结束时间戳（秒） |
| `meeting_info_list[].join_url` | string | 加入会议 URL |
| `meeting_info_list[].participants` | array | 邀请的参会人列表 |
| `meeting_info_list[].participants[].userid` | string | 参会人用户 ID |
| `meeting_info_list[].participants[].nick_name` | string | 参会人匿名昵称 |
| `meeting_info_list[].participants[].is_anonymous` | bool | 是否匿名入会 |

---

### 2. `update_meeting` — 修改会议

**功能**：修改已创建的会议信息（主题、时间、密码、时区、会议类型、入会限制、等候室、周期性规则等）。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `meeting_id` | string | ✅ | 会议ID |
| `subject` | string | ❌ | 新会议主题 |
| `start_time` | string | ❌ | 新开始时间，秒级时间戳 |
| `end_time` | string | ❌ | 新结束时间，秒级时间戳 |
| `password` | string | ❌ | 会议密码（4~6位数字），可不填。如果将字段值改为空字符串""，则表示取消会议密码 |
| `time_zone` | string | ❌ | 时区，遵循 Oracle-TimeZone 标准，例如：Asia/Shanghai |
| `meeting_type` | number | ❌ | 会议类型，默认值为0。0：普通会议 1：周期性会议 |
| `only_user_join_type` | number | ❌ | 成员入会限制。1：所有成员可入会 2：仅受邀成员可入会 3：仅企业内部成员可入会 |
| `auto_in_waiting_room` | boolean | ❌ | 是否开启等候室，默认值为 false。true：开启 false：不开启 |
| `recurring_rule` | object | ❌ | 周期性会议配置，当 meeting_type=1 时使用（见下方子字段） |
| `recurring_rule.recurring_type` | number | ❌ | 周期类型：0-每天 1-周一至周五 2-每周 3-每两周 4-每月 5-自定义 |
| `recurring_rule.until_type` | number | ❌ | 结束类型：0-按日期结束 1-按次数结束 |
| `recurring_rule.until_count` | number | ❌ | 重复次数（1-50次），当 until_type=1 时必填 |
| `recurring_rule.until_date` | number | ❌ | 结束日期时间戳（秒级），当 until_type=0 时必填 |
| `recurring_rule.customized_recurring_type` | number | ❌ | 自定义周期类型：0-按天 1-按周 2-按月（以周为粒度） 3-按月（以日期为粒度） |
| `recurring_rule.customized_recurring_step` | number | ❌ | 自定义周期步长，例如：每5天重复一次 |
| `recurring_rule.customized_recurring_days` | number | ❌ | 自定义周期天数，根据 customized_recurring_type 和 customized_recurring_step 的不同，该字段可取值与表达含义不同 |
| `recurring_rule.sub_meeting_id` | string | ❌ | 子会议 ID，表示修改该子会议时间，不可与周期性会议规则同时修改 |

**调用示例**：
```bash
# 修改非周期性会议
mcporter call tencent-meeting-mcp update_meeting --args '{"meeting_id": "xxx", "subject": "新主题", "start_time": "1773284400", "end_time": "1773288000"}'

# 修改周期性会议其中一场子会议
mcporter call tencent-meeting-mcp update_meeting --args '{"meeting_id": "xxx", "start_time": "1773842400", "end_time": "1773846000", "meeting_type": 1, "recurring_rule": {"sub_meeting_id": "yyy"}}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `meeting_number` | int64 | 会议数量 |
| `meeting_info_list` | array | 会议列表 |
| `meeting_info_list[].meeting_id` | string | 会议唯一 ID |
| `meeting_info_list[].meeting_code` | string | 会议号码 |
| `meeting_info_list[].host_key` | string | 主持人密钥 |
| `meeting_info_list[].enable_live` | bool | 是否开启直播 |
| `meeting_info_list[].live_config` | object | 直播配置（内部只返回直播观看地址） （含子字段，见下方各行） |
| `meeting_info_list[].live_config.live_addr` | string | 直播观看地址 |
| `meeting_info_list[].settings` | object | 会议设置 （含子字段，见下方各行） |
| `meeting_info_list[].settings.change_nickname` | int64 | 是否允许用户自己改名（1:允许 2:不允许） |
| `meeting_info_list[].settings.only_user_join_type` | int64 | 成员入会限制（1:所有成员 2:仅受邀成员 3:仅企业内部成员） |

---

### 3. `cancel_meeting` — 取消会议

**功能**：取消已创建的会议。支持取消普通会议或周期性会议的某个子会议。

**参数**：

| 参数               | 类型 | 必填 | 说明 |
|------------------|------|------|------|
| `meeting_id`     | string | ✅ | 会议ID |
| `sub_meeting_id` | string | ❌ | 周期性会议子会议ID，取消周期性会议的某个子会议时传入 |
| `meeting_type`   | number | ❌ | 如果需要取消整场周期性会议, 传1, 其他情况下不传 |

**调用示例**：
```bash
# 取消普通会议
mcporter call tencent-meeting-mcp cancel_meeting --args '{"meeting_id": "xxx"}'

# 取消周期性会议的某个子会议
mcporter call tencent-meeting-mcp cancel_meeting --args '{"meeting_id": "xxx", "sub_meeting_id": "yyy"}'
```

**返回值**：

取消成功返回 HTTP 200 空响应（无 body 字段）。请求失败时返回错误信息。

---

### 4. `get_meeting` — 查询会议详情

**功能**：根据会议ID查询会议的详细信息。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `meeting_id` | string | ✅ | 会议ID |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp get_meeting --args '{"meeting_id": "xxx"}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `meeting_number` | int64 | 会议数量 |
| `meeting_info_list` | array | 会议列表 |
| `meeting_info_list[].meeting_id` | string | 会议唯一 ID |
| `meeting_info_list[].meeting_code` | string | 会议号码 |
| `meeting_info_list[].subject` | string | 会议主题 |
| `meeting_info_list[].start_time` | string | 会议开始时间戳（秒） |
| `meeting_info_list[].end_time` | string | 会议结束时间戳（秒） |
| `meeting_info_list[].status` | string | 会议状态（MEETING_STATE_INIT/MEETING_STATE_STARTED/MEETING_STATE_ENDED 等） |
| `meeting_info_list[].join_url` | string | 加入会议 URL |
| `meeting_info_list[].password` | string | 会议密码 |
| `meeting_info_list[].need_password` | bool | 是否需要密码 |
| `meeting_info_list[].host_key` | string | 主持人密钥 |
| `meeting_info_list[].enable_live` | bool | 是否开启直播 |
| `meeting_info_list[].enable_host_key` | bool | 是否开启主持人密钥 |
| `meeting_info_list[].enable_enroll` | bool | 是否开启报名 |
| `meeting_info_list[].enable_doc_upload_permission` | bool | 是否允许成员上传文档 |
| `meeting_info_list[].allow_enterprise_intranet_only` | bool | 是否仅允许企业内网（混合云企业返回） |
| `meeting_info_list[].has_vote` | bool | 是否有投票 |
| `meeting_info_list[].sync_to_wework` | bool | 是否同步到企业微信 |
| `meeting_info_list[].meeting_type` | int64 | 会议类型（0:一次性 1:周期性 2:微信专属 等） |
| `meeting_info_list[].type` | int64 | 会议类型（0:预约 1:快速） |
| `meeting_info_list[].location` | string | 会议地点 |
| `meeting_info_list[].time_zone` | string | 时区 |
| `meeting_info_list[].media_set_type` | int64 | 0:公网会议 1:专网会议（混合云企业返回） |
| `meeting_info_list[].current_sub_meeting_id` | string | 当前子会议 ID（进行中/即将开始） |
| `meeting_info_list[].remain_sub_meetings` | int64 | 剩余子会议场数 |
| `meeting_info_list[].has_more_sub_meeting` | int64 | 0:无更多 1:有更多子会议特例 |
| `meeting_info_list[].hosts` | array | 主持人列表 |
| `meeting_info_list[].hosts[].userid` | string | 主持人用户 ID |
| `meeting_info_list[].hosts[].operator_id` | string | 操作者 ID |
| `meeting_info_list[].hosts[].operator_id_type` | int64 | 操作者 ID 类型 |
| `meeting_info_list[].current_hosts` | array | 当前主持人列表 |
| `meeting_info_list[].current_hosts[].userid` | string | 当前主持人用户 ID |
| `meeting_info_list[].current_hosts[].operator_id` | string | 操作者 ID |
| `meeting_info_list[].current_hosts[].operator_id_type` | int64 | 操作者 ID 类型（1:userid 2:openid） |
| `meeting_info_list[].current_co_hosts` | array | 当前联席主持人列表 |
| `meeting_info_list[].current_co_hosts[].userid` | string | 联席主持人用户 ID |
| `meeting_info_list[].current_co_hosts[].operator_id` | string | 操作者 ID |
| `meeting_info_list[].current_co_hosts[].operator_id_type` | int64 | 操作者 ID 类型（1:userid 2:openid） |
| `meeting_info_list[].participants` | array | 受邀参会人列表 |
| `meeting_info_list[].participants[].userid` | string | 受邀参会人用户 ID |
| `meeting_info_list[].participants[].operator_id` | string | 操作者 ID |
| `meeting_info_list[].participants[].operator_id_type` | int64 | 操作者 ID 类型（1:userid 2:openid） |
| `meeting_info_list[].guests` | array | 外部嘉宾列表 |
| `meeting_info_list[].guests[].guest_name` | string | 嘉宾名称 |
| `meeting_info_list[].guests[].area` | string | 区域码 |
| `meeting_info_list[].guests[].phone_number` | string | 手机号 |
| `meeting_info_list[].sub_meetings` | array | 周期性子会议列表 |
| `meeting_info_list[].sub_meetings[].sub_meeting_id` | string | 子会议 ID |
| `meeting_info_list[].sub_meetings[].start_time` | string | 子会议开始时间 |
| `meeting_info_list[].sub_meetings[].end_time` | string | 子会议结束时间 |
| `meeting_info_list[].sub_meetings[].status` | int64 | 0:存在 1:已删除 |
| `meeting_info_list[].recurring_rule` | object | 周期性会议规则 （含子字段，见下方各行） |
| `meeting_info_list[].recurring_rule.recurring_type` | int64 | 频率（0:每天 1:周一至周五 2:每周 3:每两周 4:每月） |
| `meeting_info_list[].recurring_rule.until_type` | int64 | 结束类型（0:按日期 1:按次数） |
| `meeting_info_list[].recurring_rule.until_count` | int64 | 限定次数（1-50） |
| `meeting_info_list[].recurring_rule.until_date` | int64 | 结束日期时间戳 |
| `meeting_info_list[].recurring_rule.customized_recurring_type` | int64 | 自定义周期类型 |
| `meeting_info_list[].recurring_rule.customized_recurring_step` | int64 | 自定义周期步长 |
| `meeting_info_list[].recurring_rule.customized_recurring_days` | int64 | 自定义周期天数 |
| `meeting_info_list[].settings` | object | 会议设置 （含子字段，见下方各行） |
| `meeting_info_list[].settings.allow_in_before_host` | bool | 允许成员在主持人进会前加入 |
| `meeting_info_list[].settings.allow_multi_device` | bool | 允许多端入会 |
| `meeting_info_list[].settings.allow_screen_shared_watermark` | bool | 屏幕共享水印 |
| `meeting_info_list[].settings.allow_unmute_self` | bool | 静音自解除 |
| `meeting_info_list[].settings.auto_asr` | bool | 自动转写 |
| `meeting_info_list[].settings.auto_in_waiting_room` | bool | 开启等候室 |
| `meeting_info_list[].settings.auto_record_type` | string | 自动录制类型（none:禁用 local:本地录制 cloud:云录制） |
| `meeting_info_list[].settings.enable_host_pause_auto_record` | bool | 允许主持人暂停/停止云录制 |
| `meeting_info_list[].settings.mute_enable_join` | bool | 加入静音 |
| `meeting_info_list[].settings.mute_enable_type_join` | int64 | 加入静音类型 |
| `meeting_info_list[].settings.only_allow_enterprise_user_join` | bool | 仅企业内部成员可入会 |
| `meeting_info_list[].settings.only_user_join_type` | int64 | 成员入会限制（1:所有成员 2:仅受邀成员 3:仅企业内部成员） |
| `meeting_info_list[].settings.open_asr_view` | int64 | 主持人入会是否自动打开转写侧边栏（auto_asr 为 true 时生效） |
| `meeting_info_list[].settings.participant_join_auto_record` | bool | 成员入会自动录制 |
| `meeting_info_list[].settings.water_mark_type` | int64 | 水印类型 |
| `meeting_info_list[].live_config` | object | 直播配置 （含子字段，见下方各行） |
| `meeting_info_list[].live_config.enable_live_im` | bool | 开启直播互动 |
| `meeting_info_list[].live_config.enable_live_replay` | bool | 开启直播回放 |
| `meeting_info_list[].live_config.live_addr` | string | 直播观看地址 |
| `meeting_info_list[].live_config.live_password` | string | 直播密码 |
| `meeting_info_list[].live_config.live_subject` | string | 直播主题 |
| `meeting_info_list[].live_config.live_summary` | string | 直播简介 |
| `meeting_info_list[].live_config.live_watermark` | object | 直播水印对象 （含子字段，见下方各行） |
| `meeting_info_list[].live_config.live_watermark.watermark_opt` | int64 | 水印选项（0:默认水印 1:无水印） |

---

### 5. `get_meeting_by_code` — 通过会议Code查询

**功能**：通过9位会议号查询会议信息。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `meeting_code` | string | ✅ | 9位会议号 |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp get_meeting_by_code --args '{"meeting_code": "904854736"}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `meeting_number` | int64 | 会议数量 |
| `remaining` | int64 | 是否还剩下会议（非0表示需继续查询） |
| `next_pos` | int64 | 下次查询的 pos 参数 |
| `next_cursory` | int64 | 下次查询的 cursory 参数 |
| `meeting_info_list` | array | 会议列表 |
| `meeting_info_list[].meeting_id` | string | 会议唯一 ID |
| `meeting_info_list[].meeting_code` | string | 会议号码 |
| `meeting_info_list[].subject` | string | 会议主题 |
| `meeting_info_list[].start_time` | string | 开始时间 |
| `meeting_info_list[].end_time` | string | 结束时间 |
| `meeting_info_list[].status` | string | 会议状态（MEETING_STATE_INIT/MEETING_STATE_STARTED/MEETING_STATE_ENDED/MEETING_STATE_CANCELLED/MEETING_STATE_NULL/MEETING_STATE_RECYCLED 等） |
| `meeting_info_list[].join_url` | string | 加入会议 URL |
| `meeting_info_list[].password` | string | 会议密码 |
| `meeting_info_list[].need_password` | bool | 是否需要密码 |
| `meeting_info_list[].meeting_type` | int64 | 会议类型（0:一次性 1:周期性 2:微信专属 5:个人会议号 6:网络研讨会） |
| `meeting_info_list[].type` | int64 | 0:预约 1:快速 |
| `meeting_info_list[].location` | string | 会议地点 |
| `meeting_info_list[].time_zone` | string | 时区 |
| `meeting_info_list[].media_set_type` | int64 | 0:公网会议 1:专网会议（混合云企业返回） |
| `meeting_info_list[].current_sub_meeting_id` | string | 当前子会议 ID（进行中/即将开始） |
| `meeting_info_list[].remain_sub_meetings` | int64 | 剩余子会议场数 |
| `meeting_info_list[].has_more_sub_meeting` | int64 | 0:无更多 1:有更多子会议特例 |
| `meeting_info_list[].enable_live` | bool | 是否开启直播 |
| `meeting_info_list[].enable_host_key` | bool | 是否开启主持人密钥 |
| `meeting_info_list[].enable_enroll` | bool | 是否开启报名 |
| `meeting_info_list[].enable_doc_upload_permission` | bool | 是否允许成员上传文档 |
| `meeting_info_list[].has_vote` | bool | 是否有投票 |
| `meeting_info_list[].sync_to_wework` | bool | 是否同步到企业微信 |
| `meeting_info_list[].host_key` | string | 主持人密钥 |
| `meeting_info_list[].join_meeting_role` | string | 查询者角色（creator/hoster/invitee） |
| `meeting_info_list[].hosts` | array | 主持人列表 |
| `meeting_info_list[].hosts[].userid` | string | 主持人用户 ID |
| `meeting_info_list[].current_hosts` | array | 当前主持人列表 |
| `meeting_info_list[].current_hosts[].userid` | string | 当前主持人用户 ID |
| `meeting_info_list[].current_co_hosts` | array | 当前联席主持人列表 |
| `meeting_info_list[].current_co_hosts[].userid` | string | 联席主持人用户 ID |
| `meeting_info_list[].participants` | array | 受邀参会人列表 |
| `meeting_info_list[].participants[].userid` | string | 受邀参会人用户 ID |
| `meeting_info_list[].guests` | array | 外部嘉宾列表 |
| `meeting_info_list[].guests[].guest_name` | string | 嘉宾名称 |
| `meeting_info_list[].guests[].area` | string | 区域码 |
| `meeting_info_list[].guests[].phone_number` | string | 手机号 |
| `meeting_info_list[].sub_meetings` | array | 周期性子会议列表 |
| `meeting_info_list[].sub_meetings[].sub_meeting_id` | string | 子会议 ID |
| `meeting_info_list[].sub_meetings[].start_time` | string | 子会议开始时间 |
| `meeting_info_list[].sub_meetings[].end_time` | string | 子会议结束时间 |
| `meeting_info_list[].sub_meetings[].status` | int64 | 子会议状态（0:存在 1:已删除） |
| `meeting_info_list[].recurring_rule` | object | 周期性会议规则 （含子字段，见下方各行） |
| `meeting_info_list[].recurring_rule.recurring_type` | int64 | 频率（0:每天 1:周一至周五 2:每周 3:每两周 4:每月） |
| `meeting_info_list[].recurring_rule.until_type` | int64 | 结束类型（0:按日期 1:按次数） |
| `meeting_info_list[].recurring_rule.until_count` | int64 | 限定次数（1-50） |
| `meeting_info_list[].recurring_rule.until_date` | int64 | 结束日期时间戳 |
| `meeting_info_list[].recurring_rule.customized_recurring_type` | int64 | 自定义周期类型 |
| `meeting_info_list[].recurring_rule.customized_recurring_step` | int64 | 自定义周期步长 |
| `meeting_info_list[].recurring_rule.customized_recurring_days` | int64 | 自定义周期天数 |
| `meeting_info_list[].settings` | object | 会议设置 （含子字段，见下方各行） |
| `meeting_info_list[].settings.allow_in_before_host` | bool | 允许成员在主持人进会前加入 |
| `meeting_info_list[].settings.allow_multi_device` | bool | 允许多端入会 |
| `meeting_info_list[].settings.allow_screen_shared_watermark` | bool | 屏幕共享水印 |
| `meeting_info_list[].settings.allow_unmute_self` | bool | 静音自解除 |
| `meeting_info_list[].settings.auto_asr` | bool | 自动转写 |
| `meeting_info_list[].settings.auto_in_waiting_room` | bool | 开启等候室 |
| `meeting_info_list[].settings.auto_record_type` | string | 自动录制类型（none:禁用 local:本地录制 cloud:云录制） |
| `meeting_info_list[].settings.change_nickname` | int64 | 是否允许用户改名（1:允许 2:不允许） |
| `meeting_info_list[].settings.enable_host_pause_auto_record` | bool | 允许主持人暂停/停止云录制 |
| `meeting_info_list[].settings.mute_enable_join` | bool | 加入静音 |
| `meeting_info_list[].settings.mute_enable_type_join` | int64 | 加入静音类型 |
| `meeting_info_list[].settings.only_allow_enterprise_user_join` | bool | 仅企业内部成员可入会 |
| `meeting_info_list[].settings.only_user_join_type` | int64 | 成员入会限制（1:所有成员 2:仅受邀成员 3:仅企业内部成员） |
| `meeting_info_list[].settings.participant_join_auto_record` | bool | 成员入会自动录制 |
| `meeting_info_list[].settings.water_mark_type` | int64 | 水印类型 |
| `meeting_info_list[].live_config` | object | 直播配置 （含子字段，见下方各行） |
| `meeting_info_list[].live_config.enable_live_im` | bool | 开启直播互动 |
| `meeting_info_list[].live_config.enable_live_password` | bool | 是否开启直播密码 |
| `meeting_info_list[].live_config.enable_live_replay` | bool | 开启直播回放 |
| `meeting_info_list[].live_config.live_addr` | string | 直播观看地址 |
| `meeting_info_list[].live_config.live_password` | string | 直播密码 |
| `meeting_info_list[].live_config.live_subject` | string | 直播主题 |
| `meeting_info_list[].live_config.live_summary` | string | 直播简介 |
| `meeting_info_list[].live_config.live_watermark` | object | 直播水印对象 （含子字段，见下方各行） |
| `meeting_info_list[].live_config.live_watermark.watermark_opt` | int64 | 水印选项（0:默认水印 1:无水印） |

---

## 成员管理

### 6. `get_meeting_participants` — 获取参会成员明细

**功能**：查询会议的实际参会成员信息。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `meeting_id` | string | ✅ | 会议ID |
| `sub_meeting_id` | string | ❌ | 周期性会议子会议 ID。说明：可通过查询用户的会议列表、查询会议接口获取返回的子会议 ID，即 current_sub_meeting_id；如果是周期性会议，此参数必传。 |
| `pos` | string | ❌ | 分页获取参会成员列表的查询起始位置值。当参会成员较多时，建议使用此参数进行分页查询，避免查询超时。此参数为非必选参数，默认值为0，从头开始查询。设置每页返回的数量，请参考参数"size"的说明。查询返回输出参数"has_remaining"为 true，表示该会议人数较多，还有一定数量的参会成员需要继续查询。返回参数"next_pos"的值即为下一次查询的 pos 的值。多次调用该查询接口直到输出参数"has_remaining"值为 false。 |
| `size` | string | ❌ | 拉取参会成员条数，目前每页支持最大100条。 |
| `start_time` | string | ❌ | 参会时间过滤起始时间（单位秒）。说明：时间区间不允许超过31天，如果为空默认当前时间前推31天；start_time 和 end_time 都没传时最大查询时间跨度90天；对于周期性会议查询暂时不生效，请使用分页参数查询。 |
| `end_time` | string | ❌ | 参会时间过滤终止时间（单位秒）。说明：时间区间不允许超过31天，如果为空默认取当前时间；start_time 和 end_time 都没传时最大查询时间跨度90天；对于周期性会议查询暂时不生效，请使用分页参数查询。 |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp get_meeting_participants --args '{"meeting_id": "xxx", "size": "20", "pos": "0"}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `meeting_id` | string | 会议唯一 ID |
| `meeting_code` | string | 会议号码 |
| `subject` | string | 会议主题 |
| `schedule_start_time` | string | 预定开始时间戳（秒） |
| `schedule_end_time` | string | 预定结束时间戳（秒） |
| `total_count` | int64 | 当前参会总人次 |
| `has_remaining` | bool | 是否还有未拉取的数据（上限5w条） |
| `next_pos` | int64 | 下次查询的 pos 值（has_remaining 为 true 时使用） |
| `participants` | array | 参会人员对象数组 |
| `participants[].userid` | string | 参会者用户 ID |
| `participants[].open_id` | string | OAuth2.0 用户 openId |
| `participants[].ms_open_id` | string | 当场会议用户临时 ID（可用于会控） |
| `participants[].user_name` | string | 入会用户名（base64编码） |
| `participants[].is_enterprise_user` | bool | 是否企业用户 |
| `participants[].join_time` | string | 加入会议时间戳（秒） |
| `participants[].left_time` | string | 离开会议时间戳（秒） |
| `participants[].user_role` | int64 | 用户角色（0:普通 1:创建者 2:主持人 3:创建者+主持人 4:游客 6:联席主持人 等） |

---

### 7. `get_meeting_invitees` — 获取受邀成员列表

**功能**：查询会议邀请的成员列表。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `meeting_id` | string | ✅ | 会议ID |
| `page_size` | number | ❌ | 每页数量，默认20 |
| `page_number` | number | ❌ | 页码，从1开始 |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp get_meeting_invitees --args '{"meeting_id": "xxx"}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `has_remaining` | bool | 是否还存在受邀成员需要继续查询 |
| `next_pos` | int64 | 下次查询时 pos 参数值（has_remaining 为 true 时使用） |
| `invitees` | array | 受邀成员列表 |
| `invitees[].userid` | string | 用户唯一 ID |
| `invitees[].nick_name` | string | 用户昵称 |

---

### 8. `get_waiting_room` — 查询等候室成员记录

**功能**：查询会议等候室的成员记录。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `meeting_id` | string | ✅ | 会议ID |
| `page_size` | number | ❌ | 每页数量，默认20 |
| `page` | number | ❌ | 页码，从1开始 |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp get_waiting_room --args '{"meeting_id": "xxx"}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `meeting_id` | string | 会议唯一 ID |
| `meeting_code` | string | 会议 CODE |
| `subject` | string | 会议主题 |
| `schedule_start_time` | int64 | 预定开始时间（毫秒） |
| `schedule_end_time` | int64 | 预定结束时间（毫秒） |
| `total_page` | int64 | 总页数 |
| `current_page` | int64 | 当前页码 |
| `current_size` | int64 | 当前页数据条数 |
| `participants` | array | 等候室人员对象数组 |
| `participants[].userid` | string | 成员用户 ID |
| `participants[].open_id` | string | OAuth2.0 用户 openId |
| `participants[].ms_open_id` | string | 当场会议用户临时 ID |
| `participants[].user_name` | string | 入会用户名（base64编码） |
| `participants[].join_time` | int64 | 加入时间（毫秒） |
| `participants[].left_time` | int64 | 离开时间（毫秒） |

---

### 9. `get_user_meetings` — 查询用户会议列表

**功能**：查询当前用户的会议列表。

**参数**：

| 参数 | 类型 | 必填 | 说明                                        |
|------|------|------|-------------------------------------------|
| `pos` | number | ❌ | 查询起始位置，默认为0。分页获取用户会议列表的查询起始时间值，unix 秒级时间戳 |
| `cursory` | number | ❌ | 分页游标，默认为20                                |
| `is_show_all_sub_meetings` | number | ❌ | 是否展示全部子会议，0-不展示，1-展示，默认为0                 |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp get_user_meetings --args '{"pos": 0, "cursory": 20, "is_show_all_sub_meetings": 0}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `meeting_number` | int64 | 会议数量 |
| `next_cursory` | int64 | 分页获取用户会议列表，查询的会议的最后一次修改时间值，UNIX 毫秒级时间戳，分页游标。 因目前一次查询返回会议数量最多为20，当用户会议较多时，如果会议总数量超过20，则需要再次查询。此参数为非必选参数，默认值为0，表示第一次查询利用会议开始时间北京时间当日零点进行查询。 查询返回输出参数“remaining”不为0时，表示还有会议需要继续查询。返回参数“next_cursory”的值即为下一次查询的 cursory 的值。 多次调用该查询接口直到输出参数“remaining”值为0。 当只使用 pos 作为分页条件时,可能会出现查询不到第二页,数据排序出现重复数据等情况与 pos 配合使用。 |
| `next_pos` | int64 | 下次查询时请求里需要携带的 pos 参数。 |
| `remaining` | int64 | 是否还剩下会议；因目前一次查询返回会议数量最多为20，如果会议总数量超过20则此字段被置为非0，表示需要再次查询，且下次查询的“pos”参数需从本次响应的“next_pos”字段取值 |
| `meeting_info_list` | array | 会议信息列表 |
| `meeting_info_list[].meeting_id` | string | 会议 ID |
| `meeting_info_list[].meeting_code` | string | 会议 App 的呼入号码 |
| `meeting_info_list[].subject` | string | 会议主题 |
| `meeting_info_list[].meeting_type` | int64 | 会议类型（0:一次性 1:周期性 2:微信专属 5:个人会议号 6:网络研讨会） |
| `meeting_info_list[].start_time` | int64 | 开始时间戳（秒） |
| `meeting_info_list[].end_time` | int64 | 结束时间戳（秒） |
| `meeting_info_list[].sub_meeting_id` | string | 子会议 ID |

---

### 10. `get_user_ended_meetings` — 查询用户已结束会议列表

**功能**：查询当前用户在指定时间范围内已结束的会议列表。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `start_time` | string | ✅ | 查询开始时间，秒级时间戳 |
| `end_time` | string | ✅ | 查询结束时间，秒级时间戳 |
| `page_size` | number | ❌ | 每页数量，默认20 |
| `page_number` | number | ❌ | 页码，从1开始 |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp get_user_ended_meetings --args '{"start_time": "1773280800", "end_time": "1773367200"}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `total_count` | int64 | 数据总条数 |
| `total_page` | int64 | 数据总页数 |
| `current_page` | int64 | 当前页 |
| `current_size` | int64 | 当前实际页大小 |
| `meeting_info_list` | array | 会议信息列表 |
| `meeting_info_list[].meeting_id` | string | 会议 ID |
| `meeting_info_list[].meeting_code` | string | 会议 App 的呼入号码 |
| `meeting_info_list[].subject` | string | 会议主题 |
| `meeting_info_list[].meeting_type` | int64 | 会议类型（0:一次性 1:周期性 2:微信专属 5:个人会议号 6:网络研讨会） |
| `meeting_info_list[].start_time` | int64 | 开始时间戳（秒） |
| `meeting_info_list[].end_time` | int64 | 结束时间戳（秒） |
| `meeting_info_list[].sub_meeting_id` | string | 子会议 ID |

---

## 录制与转写

---

### 11. `get_record_addresses` — 获取录制下载地址

**功能**：获取录制文件的下载链接。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `meeting_record_id` | string | ✅ | 会议录制ID |
| `page_number` | number | ❌ | 页码，从1开始 |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp get_record_addresses --args '{"meeting_record_id": "xxx"}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `meeting_id` | string | 会议唯一 ID |
| `meeting_code` | string | 会议 code |
| `meeting_record_id` | string | 会议录制 ID |
| `subject` | string | 会议主题 |
| `total_count` | int64 | 录制总数 |
| `total_page` | int64 | 总页数 |
| `current_page` | int64 | 当前页 |
| `current_size` | int64 | 当前 size |
| `record_files` | array | 录制文件列表 |
| `record_files[].record_file_id` | string | 录制文件 ID |
| `record_files[].view_address` | string | 播放地址 |
| `record_files[].meeting_summary` | array | 会议纪要文件列表 |
| `record_files[].meeting_summary[].download_address` | string | 纪要下载地址 |
| `record_files[].meeting_summary[].file_type` | string | 文件类型（txt/pdf/docs） |

---

### 12. `get_transcripts_details` — 查询转写详情

**功能**：获取录制文件的完整转写内容。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `record_file_id` | string | ✅ | 录制文件ID |
| `meeting_id` | string | ❌ | 会议ID（可选，传入可加速定位） |
| `pid` | string | ❌ | 查询的起始段落 ID。获取 pid 后（含）的段落，默认从0开始 |
| `limit` | string | ❌ | 查询的段落数，默认查询全量数据 |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp get_transcripts_details --args '{"record_file_id": "xxx"}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `more` | bool | 是否还有更多内容 |
| `minutes` | object | 会议纪要对象 （含子字段，见下方各行） |
| `minutes.audio_detect` | int64 | 声纹识别状态（0:未完成 1:已完成） |
| `minutes.keywords` | array\<string\> | 关键词列表 |
| `minutes.paragraphs` | array | 段落对象列表 |
| `minutes.paragraphs[].pid` | string | 段落 ID |
| `minutes.paragraphs[].start_time` | int64 | 段落开始时间（毫秒） |
| `minutes.paragraphs[].end_time` | int64 | 段落结束时间（毫秒） |
| `minutes.paragraphs[].speaker_info` | object | 发言人信息 （含子字段，见下方各行） |
| `minutes.paragraphs[].speaker_info.userid` | string | 企业用户 userid |
| `minutes.paragraphs[].speaker_info.ms_open_id` | string | 会议临时 ID |
| `minutes.paragraphs[].speaker_info.username` | string | 昵称 |
| `minutes.paragraphs[].sentences` | array | 句子列表 |
| `minutes.paragraphs[].sentences[].sid` | string | 句子 ID |
| `minutes.paragraphs[].sentences[].start_time` | int64 | 句子开始时间（毫秒） |
| `minutes.paragraphs[].sentences[].end_time` | int64 | 句子结束时间（毫秒） |
| `minutes.paragraphs[].sentences[].words` | array | 词对象列表 |
| `minutes.paragraphs[].sentences[].words[].wid` | string | 词 ID |
| `minutes.paragraphs[].sentences[].words[].text` | string | 文本内容 |
| `minutes.paragraphs[].sentences[].words[].start_time` | int64 | 词开始时间（毫秒） |
| `minutes.paragraphs[].sentences[].words[].end_time` | int64 | 词结束时间（毫秒） |

---

### 13. `get_transcripts_paragraphs` — 查询转写段落

**功能**：分页获取录制文件的转写段落信息。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `record_file_id` | string | ✅ | 录制文件ID |
| `meeting_id` | string | ❌ | 会议ID |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp get_transcripts_paragraphs --args '{"record_file_id": "xxx"}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | int64 | 段落总数 |
| `audio_detect` | int64 | 声纹识别状态（0:未完成 1:已完成） |
| `pids` | array | 段落对象列表 |
| `pids[].pid` | string | 段落 ID |
| `pids[].start_time` | int64 | 段落开始时间（毫秒） |
| `pids[].end_time` | int64 | 段落结束时间（毫秒） |

> **说明**：该接口返回段落 ID 列表，配合 `get_transcripts_details` 接口通过 pid 获取具体文本内容。

---

### 14. `search_transcripts` — 搜索转写内容

**功能**：在录制转写内容中搜索特定关键词。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `record_file_id` | string | ✅ | 录制文件ID |
| `text` | string | ✅ | 搜索的文本, 如果是中文, 需要urlencode一下 |
| `meeting_id` | string | ❌ | 会议ID |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp search_transcripts --args '{"record_file_id": "xxx", "text": "产品需求"}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `hits` | array | 搜索结果列表 |
| `hits[].pid` | string | 段落 ID |
| `hits[].sid` | string | 句子 ID |
| `hits[].offset` | int64 | text 相对词的偏移量 |
| `hits[].length` | int64 | 匹配长度 |
| `timelines` | array | 搜索结果时间戳对象列表 |
| `timelines[].pid` | string | 段落 ID |
| `timelines[].sid` | string | 句子 ID |
| `timelines[].start_time` | int64 | 词开始时间（毫秒） |

---

### 15. `get_smart_minutes` — 获取智能纪要

**功能**：获取会议录制的 AI 智能纪要总结。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `record_file_id` | string | ✅ | 录制文件ID |
| `lang` | string | ❌ | 翻译语言：`default`(原文，不翻译) / `zh`(简体中文) / `en`(英文) / `ja`(日语)，默认 default |
| `pwd` | string | ❌ | 录制文件访问密码（录制文件有密码时需传入） |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp get_smart_minutes --args '{"record_file_id": "xxx"}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `ai_summary` | string | 智能总结内容 |

---

### 16. `export_asr_details` — 导出会议实时转写记录

**功能**：导出指定条件下的会议实时转写记录，支持按会议ID、时间范围筛选，可配置双语展示和分页查询。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 取值范围/说明 |
|------|------|------|--------|--------------|
| `meeting_id` | string | ❌ | - | 会议ID，用于筛选指定会议的转写记录 |
| `start_time` | string | ❌ | - | 查询开始时间，秒级时间戳 |
| `end_time` | string | ❌ | - | 查询结束时间，秒级时间戳 |
| `show_bilingual` | number | ❌ | 0 | 0：不展示双语转写；1：展示双语转写 |
| `page` | number | ❌ | 1 | 页码，从1开始，用于分页查询转写记录 |

**调用示例**：
```bash
mcporter call tencent-meeting-mcp export_asr_details --args '{"meeting_id": "123456789", "start_time": "1773280800", "end_time": "1773284400"}'
```

---

### 17. `get_records_list` — 查询录制列表

**功能**：根据时间范围和会议ID查询用户的录制列表。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 取值范围/说明 |
|------|------|------|--------|--------------|
| `start_time` | string | ✅ | - | 查询开始时间，秒级时间戳 |
| `end_time` | string | ✅ | - | 查询结束时间，秒级时间戳 |
| `page_number` | number | ❌ | 1 | 页码，从1开始 |
| `meeting_id` | string | ❌ | - | 会议ID，不为空时优先根据会议ID查询 |

**调用示例**：
```bash
# 按时间范围查询
mcporter call tencent-meeting-mcp get_records_list --args '{"start_time": "1773280800", "end_time": "1773367200", "page_number": 1}'

# 按会议ID查询
mcporter call tencent-meeting-mcp get_records_list --args '{"start_time": "1773280800", "end_time": "1773367200", "meeting_id": "xxx"}'
```

**返回值**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `total_count` | int64 | 录制总数 |
| `total_page` | int64 | 总页数 |
| `current_page` | int64 | 当前页码 |
| `current_size` | int64 | 当前页数据条数 |
| `records` | array | 录制列表 |
| `records[].record_id` | string | 录制ID |
| `records[].meeting_id` | string | 会议ID |
| `records[].meeting_code` | string | 会议号 |
| `records[].subject` | string | 会议主题 |
| `records[].start_time` | string | 录制开始时间（秒级时间戳） |
| `records[].end_time` | string | 录制结束时间（秒级时间戳） |
| `records[].file_size` | int64 | 文件大小（字节） |
| `records[].status` | string | 录制状态 |
| `records[].download_url` | string | 下载地址 |