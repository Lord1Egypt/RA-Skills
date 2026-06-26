---
name: wecom-meeting
description: 企业微信会议管理工具。用于创建、查询、取消和管理企业微信预约会议。支持创建预约会议、获取会议详情、取消会议、获取成员会议列表等操作。使用企业微信会议API需要配置CorpID、Secret和AgentID。当用户需要创建企业微信会议、查询会议信息、取消会议或管理会议时使用此Skill。
---

# 企业微信会议管理

此Skill提供企业微信预约会议的管理功能，基于企业微信官方API（文档：https://developer.work.weixin.qq.com/document/path/99104）。

## 核心功能

- **创建预约会议**：创建指定主题、时间、参会人的会议
- **获取会议详情**：查询会议的详细信息
- **取消会议**：取消已创建的会议
- **获取成员会议列表**：查询指定成员的所有会议

## 前置要求

### 企业微信API配置

使用此Skill需要企业微信API凭证：

- **CorpID**（企业ID）：从企业微信管理后台「我的企业」获取
- **Secret**（应用Secret）：从企业微信管理后台「应用管理」→ 选择应用 → 查看 Secret 获取
- **AgentID**（应用ID）：从企业微信管理后台「应用管理」→ 选择应用 → 查看 AgentId 获取

### 安装依赖

```bash
pip3 install requests
```

### 配置文件（推荐）

将企业微信凭证保存在 `~/.wecom/config.json` 中：

```json
{
  "corpid": "wwxxxxxxxxxxxxxxxx",
  "secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "agentid": "1000002"
}
```

## 工作流程

### 1. 创建预约会议

**关键点**：企业微信会议API使用特定的参数格式，必须严格按照官方文档格式。

#### 基本格式

```python
{
  "admin_userid": "发起人UserID",
  "title": "会议主题",
  "meeting_start": 开始时间戳（秒）,
  "meeting_duration": 会议时长（秒）,
  "description": "会议描述（可选）",
  "invitees": {
    "userid": ["参会人UserID1", "参会人UserID2"]
  },
  "reminders": {
    "is_repeat": 0,  # 0=非周期性会议
    "remind_before": [120]  # 提前2分钟（单位：秒）
  }
}
```

#### 重要参数说明

- `meeting_start`：Unix时间戳（秒），必须大于当前时间
- `meeting_duration`：会议时长（秒），最小300秒（5分钟），最大86399秒（约24小时）
- `remind_before`：会议提醒时间，支持：0（会议开始时）、300（5分钟前）、900（15分钟前）、3600（1小时前）、86400（1天前）
- `invitees.userid`：参会人的企业微信UserID（注意：不是中文姓名）

#### 使用脚本创建

```bash
cd ~/.openclaw/workspace/skills/wecom-meeting
python3 scripts/create_meeting.py \
  --userid "WanHuiYi" \
  --title "openclaw应用" \
  --time "17:40" \
  --duration 60 \
  --attendees "WanHuiYi,WanLang"
```

#### 参数说明

- `--userid`：发起人UserID（必填）
- `--title`：会议主题（必填）
- `--time`：开始时间，格式：HH:MM（必填）
- `--duration`：会议时长（分钟），默认60（可选）
- `--attendees`：参会人列表，逗号分隔（可选）
- `--date`：日期，格式：YYYY-MM-DD，默认今天（可选）
- `--description`：会议描述（可选）
- `--remind`：提前提醒（分钟），默认2（可选）

### 2. 取消会议

```bash
cd ~/.openclaw/workspace/skills/wecom-meeting
python3 scripts/cancel_meeting.py \
  --userid "WanHuiYi" \
  --meetingid "hyBsrsUwAAZ6jYVW5GX73PHdS927OrCA"
```

#### 参数说明

- `--userid`：发起人UserID（必填）
- `--meetingid`：会议ID（必填）

### 3. 获取会议详情

```bash
cd ~/.openclaw/workspace/skills/wecom-meeting
python3 scripts/get_meeting.py \
  --meetingid "hyBsrsUwAAZ6jYVW5GX73PHdS927OrCA"
```

### 4. 获取成员会议列表

```bash
cd ~/.openclaw/workspace/skills/wecom-meeting
python3 scripts/list_meetings.py \
  --userid "WanHuiYi"
```

## 常见错误及解决方案

### 错误 40058: missing field `title` 或 `meeting_start`

**原因**：参数格式错误，使用了不兼容的API版本

**解决方案**：使用正确的参数格式
- 使用 `title` 而不是 `meetingname`
- 使用 `meeting_start` 而不是 `starttime`
- 使用 `admin_userid` 而不是 `userid`

### 错误 60111: userid not found

**原因**：UserID不存在或格式错误

**解决方案**：
- 使用企业微信系统生成的UserID（如 `WanHuiYi`），而不是中文姓名
- 在企业微信管理后台「通讯录」→ 成员详情中查看正确的UserID

### 错误 400034: invalid meeting_start

**原因**：会议开始时间无效（已过去或时间戳格式错误）

**解决方案**：
- 确保会议开始时间在未来
- 使用Unix时间戳（秒），而不是毫秒或其他格式

### 错误 48002: api forbidden

**原因**：应用没有创建会议的权限

**解决方案**：
- 在企业微信管理后台为应用分配"会议"权限
- 确认应用已启用

## API文档参考

详细的API文档请查看：
- [创建预约会议](https://developer.work.weixin.qq.com/document/path/99104)
- [取消预约会议](https://developer.work.weixin.qq.com/document/path/99048)
- [获取会议详情](https://developer.work.weixin.qq.com/document/path/99049)
- [获取成员会议ID列表](https://developer.work.weixin.qq.com/document/path/99050)

或查看本skill的 `references/api.md` 文件。

## 注意事项

1. **权限要求**：应用需要具有"会议"管理权限
2. **时间限制**：会议开始时间必须在未来，不能创建过去或当前时间的会议
3. **参会人限制**：参会人必须是企业微信成员，UserID必须正确
4. **时长限制**：会议时长最小5分钟（300秒），最大约24小时（86399秒）
5. **提醒时间**：仅支持特定的提醒时间点（0、300、900、3600、86400秒）

## 示例

### 示例1：创建简单会议

```bash
python3 scripts/create_meeting.py \
  --userid "WanHuiYi" \
  --title "项目讨论会" \
  --time "14:00" \
  --duration 30
```

### 示例2：创建多参会人会议

```bash
python3 scripts/create_meeting.py \
  --userid "WanHuiYi" \
  --title "周会" \
  --time "09:30" \
  --duration 60 \
  --attendees "WanHuiYi,WanLang,ZhangSan"
```

### 示例3：创建带提醒的会议

```bash
python3 scripts/create_meeting.py \
  --userid "WanHuiYi" \
  --title "重要会议" \
  --time "15:00" \
  --duration 90 \
  --remind 15
```

### 示例4：取消会议

```bash
python3 scripts/cancel_meeting.py \
  --userid "WanHuiYi" \
  --meetingid "hyBsrsUwAAZ6jYVW5GX73PHdS927OrCA"
```

### 示例5：查看今日会议

```bash
python3 scripts/list_meetings.py --userid "WanHuiYi"
```

## 直接调用（高级用法）

如果需要更灵活的控制，可以直接在Python代码中使用 `WeComMeeting` 类：

```python
import sys
sys.path.append('~/.openclaw/workspace/skills/wecom-meeting/scripts')
from wecom_meeting_api import WeComMeeting

# 初始化
meeting = WeComMeeting()

# 创建会议
result = meeting.create_meeting(
    admin_userid="WanHuiYi",
    title="openclaw应用",
    meeting_start=1772790000,  # Unix时间戳
    meeting_duration=3600,      # 60分钟
    invitees={"userid": ["WanHuiYi", "WanLang"]},
    reminders={"is_repeat": 0, "remind_before": [120]}
)

print(f"会议ID: {result['meetingid']}")
```

详细API参考见 `scripts/wecom_meeting_api.py`。