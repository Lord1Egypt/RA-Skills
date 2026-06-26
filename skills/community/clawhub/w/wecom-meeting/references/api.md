# 企业微信会议API参考

本文档基于企业微信官方API文档整理：https://developer.work.weixin.qq.com/document/path/99104

## 目录

- [创建预约会议](#创建预约会议)
- [获取会议详情](#获取会议详情)
- [取消预约会议](#取消预约会议)
- [获取成员会议ID列表](#获取成员会议id列表)
- [错误码说明](#错误码说明)

---

## 创建预约会议

**接口地址**：`POST https://qyapi.weixin.qq.com/cgi-bin/meeting/create?access_token=ACCESS_TOKEN`

**请求参数**：

| 参数 | 是否必填 | 类型 | 说明 |
|------|---------|------|------|
| admin_userid | 是 | string | 会议管理员userid |
| title | 是 | string | 会议标题，最多支持40个字节或20个utf8字符 |
| meeting_start | 是 | number | 会议开始时间的unix时间戳（秒），需大于当前时间 |
| meeting_duration | 是 | number | 会议持续时间（单位秒），最小300秒（5分钟），最大86399秒（约24小时） |
| description | 否 | string | 会议描述，最多支持500个字节 |
| invitees | 否 | object | 邀请参会的成员 |
| invitees.userid | 否 | array | 参与会议的企业成员userid |
| reminders | 否 | object | 重复会议相关配置 |
| reminders.is_repeat | 否 | number | 是否是周期性会议，1：周期性会议，0：非周期性会议，默认为0 |
| reminders.remind_before | 否 | array | 指定会议开始前多久提醒成员（相对于meeting_start前的秒数），默认不提醒。支持：0（会议开始时提醒）、300（5分钟前）、900（15分钟前）、3600（1小时前）、86400（1天前） |

**请求示例**：

```json
{
  "admin_userid": "WanHuiYi",
  "title": "openclaw应用",
  "meeting_start": 1772790000,
  "meeting_duration": 3600,
  "description": "openclaw应用讨论会议",
  "invitees": {
    "userid": ["WanHuiYi", "WanLang"]
  },
  "reminders": {
    "is_repeat": 0,
    "remind_before": [120]
  }
}
```

**返回参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| errcode | number | 返回码 |
| errmsg | string | 对返回码的文本描述 |
| meetingid | string | 会议ID |
| excess_users | array | 参会人中包含无效会议账号的userid |

**返回示例**：

```json
{
  "errcode": 0,
  "errmsg": "ok",
  "meetingid": "hyBsrsUwAAZ6jYVW5GX73PHdS927OrCA",
  "excess_users": []
}
```

---

## 获取会议详情

**接口地址**：`POST https://qyapi.weixin.qq.com/cgi-bin/meeting/get?access_token=ACCESS_TOKEN`

**请求参数**：

| 参数 | 是否必填 | 类型 | 说明 |
|------|---------|------|------|
| meetingid | 是 | string | 会议ID |

**请求示例**：

```json
{
  "meetingid": "hyBsrsUwAAZ6jYVW5GX73PHdS927OrCA"
}
```

**返回参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| errcode | number | 返回码 |
| errmsg | string | 对返回码的文本描述 |
| meeting_info | object | 会议信息 |
| meeting_info.meetingid | string | 会议ID |
| meeting_info.title | string | 会议标题 |
| meeting_info.meeting_start | number | 会议开始时间戳 |
| meeting_info.meeting_end | number | 会议结束时间戳 |
| meeting_info.status | number | 会议状态 |
| meeting_info.hosts | array | 主持人列表 |
| meeting_info.invitees | object | 参会人信息 |

---

## 取消预约会议

**接口地址**：`POST https://qyapi.weixin.qq.com/cgi-bin/meeting/cancel?access_token=ACCESS_TOKEN`

**请求参数**：

| 参数 | 是否必填 | 类型 | 说明 |
|------|---------|------|------|
| meetingid | 是 | string | 会议ID |
| admin_userid | 是 | string | 会议管理员userid |

**请求示例**：

```json
{
  "meetingid": "hyBsrsUwAAZ6jYVW5GX73PHdS927OrCA",
  "admin_userid": "WanHuiYi"
}
```

**返回参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| errcode | number | 返回码 |
| errmsg | string | 对返回码的文本描述 |

**返回示例**：

```json
{
  "errcode": 0,
  "errmsg": "ok"
}
```

---

## 获取成员会议ID列表

**接口地址**：`POST https://qyapi.weixin.qq.com/cgi-bin/meeting/get_user_meetings?access_token=ACCESS_TOKEN`

**请求参数**：

| 参数 | 是否必填 | 类型 | 说明 |
|------|---------|------|------|
| userid | 是 | string | 成员userid |

**请求示例**：

```json
{
  "userid": "WanHuiYi"
}
```

**返回参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| errcode | number | 返回码 |
| errmsg | string | 对返回码的文本描述 |
| meetingid_list | array | 会议ID列表 |

**返回示例**：

```json
{
  "errcode": 0,
  "errmsg": "ok",
  "meetingid_list": [
    "hyBsrsUwAAZ6jYVW5GX73PHdS927OrCA",
    "hyBsrsUwAA7OKk5fEqmRJuIdv61ixuEg"
  ]
}
```

---

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 0 | 请求成功 |
| 40058 | 缺少必填参数或参数格式错误 |
| 400034 | meeting_start 无效（已过去或格式错误） |
| 60111 | userid 不存在或无效 |
| 48002 | API权限不足 |
| 93000 | 会议ID不存在 |
| 93001 | 会议已取消 |

**常见错误处理**：

1. **错误 40058**: 检查参数格式，确保使用正确的参数名称（如 `title` 而不是 `meetingname`）
2. **错误 400034**: 确保 `meeting_start` 是未来的时间戳（秒）
3. **错误 60111**: 确保使用正确的企业微信UserID（不是中文姓名）
4. **错误 48002**: 检查应用是否有会议管理权限