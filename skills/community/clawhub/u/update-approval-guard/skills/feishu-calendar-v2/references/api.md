# 飞书日历 API 参考文档

## 目录

1. [OAuth 授权](#oauth-授权)
2. [日历 API](#日历-api)
3. [会议室 API](#会议室-api)
4. [错误码](#错误码)

---

## OAuth 授权

### 获取用户授权链接

```
GET https://open.feishu.cn/open-apis/authen/v1/authorize
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| app_id | string | 是 | 应用 ID |
| redirect_uri | string | 是 | 回调地址（需 URL 编码） |
| response_type | string | 是 | 固定值 `code` |
| state | string | 是 | 自定义状态值，用于防 CSRF |
| scope | string | 是 | 权限范围，**必须传递** |

**日历相关 Scope：**

```
contact:user.base:readonly calendar:calendar calendar:calendar.event calendar:room
```

### 用 Code 换取 Token

```
POST https://open.feishu.cn/open-apis/authen/v1/access_token
```

**请求头：**
```
Authorization: Bearer <tenant_access_token>
Content-Type: application/json
```

**请求体：**
```json
{
    "grant_type": "authorization_code",
    "code": "<authorization_code>"
}
```

**响应：**
```json
{
    "code": 0,
    "data": {
        "access_token": "u-xxx",
        "refresh_token": "ur-xxx",
        "expires_in": 7200,
        "name": "用户名",
        "open_id": "ou_xxx"
    }
}
```

### 刷新 Token

```
POST https://open.feishu.cn/open-apis/authen/v1/refresh_access_token
```

**请求体：**
```json
{
    "grant_type": "refresh_token",
    "refresh_token": "<refresh_token>"
}
```

---

## 日历 API

### 获取日历列表

```
GET https://open.feishu.cn/open-apis/calendar/v4/calendars
Authorization: Bearer <user_access_token>
```

**响应：**
```json
{
    "code": 0,
    "data": {
        "calendar_list": [
            {
                "calendar_id": "cal_xxx",
                "summary": "主日历",
                "type": "primary"
            }
        ]
    }
}
```

### 创建日程事件

```
POST https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events
Authorization: Bearer <user_access_token>
Content-Type: application/json
```

**请求体：**
```json
{
    "summary": "会议主题",
    "start_time": {
        "timestamp": "1772866800"
    },
    "end_time": {
        "timestamp": "1772870400"
    },
    "description": "会议描述（可选）",
    "location": {
        "name": "会议室名称（可选）"
    }
}
```

**响应：**
```json
{
    "code": 0,
    "data": {
        "event": {
            "event_id": "evt_xxx",
            "summary": "会议主题",
            "start_time": {
                "timestamp": "1772866800"
            },
            "end_time": {
                "timestamp": "1772870400"
            }
        }
    }
}
```

### 查询日程事件

```
GET https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events?start_time={start}&end_time={end}
Authorization: Bearer <user_access_token>
```

### 修改日程事件

```
PATCH https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}
Authorization: Bearer <user_access_token>
Content-Type: application/json
```

**请求体（部分更新）：**
```json
{
    "summary": "新主题",
    "start_time": {
        "timestamp": "1772866800"
    }
}
```

### 删除日程事件

```
DELETE https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}
Authorization: Bearer <user_access_token>
```

### 添加参会者

```
POST https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees
Authorization: Bearer <user_access_token>
Content-Type: application/json
```

**请求体：**
```json
{
    "attendees": [
        {
            "type": "user",
            "user_id": "ou_xxx"
        }
    ]
}
```

---

## 会议室 API

### 获取建筑物列表

```
GET https://open.feishu.cn/open-apis/meeting_room/building/list
Authorization: Bearer <tenant_access_token>
```

### 获取会议室列表

```
POST https://open.feishu.cn/open-apis/meeting_room/room/list
Authorization: Bearer <tenant_access_token>
Content-Type: application/json
```

**请求体：**
```json
{
    "building_id": "building_xxx"
}
```

**响应：**
```json
{
    "code": 0,
    "data": {
        "rooms": [
            {
                "room_id": "omm_xxx",
                "name": "1910尚志",
                "capacity": 10,
                "floor_name": "公共会议室"
            }
        ]
    }
}
```

### 预约会议室

```
POST https://open.feishu.cn/open-apis/meeting_room/room/reserve
Authorization: Bearer <user_access_token>
Content-Type: application/json
```

**请求体：**
```json
{
    "room_ids": ["omm_xxx"],
    "start_time": "1772866800",
    "end_time": "1772870400",
    "event_id": "evt_xxx"
}
```

### 查询会议室可用性

```
POST https://open.feishu.cn/open-apis/meeting_room/room/available_time
Authorization: Bearer <tenant_access_token>
Content-Type: application/json
```

---

## 错误码

### 通用错误

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 0 | 成功 | - |
| 99991663 | 请求频率超限 | 降低请求频率 |
| 99991668 | Token 无效 | 检查或刷新 Token |
| 99991679 | 权限不足 | 检查 scope，重新授权 |

### OAuth 错误

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 20003 | Code 过期或已使用 | 重新授权 |
| 20043 | Scope 参数有误 | 检查 scope 格式 |

### 日历错误

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 1901001 | 日历不存在 | 检查 calendar_id |
| 1901002 | 事件不存在 | 检查 event_id |
| 1901003 | 时间冲突 | 修改时间 |

### 会议室错误

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 1951001 | 会议室不存在 | 检查 room_id |
| 1951002 | 会议室已被预约 | 选择其他时间或会议室 |
| 1951003 | 不在预约时间范围内 | 检查预约时间 |

---

## 最佳实践

### 1. Token 管理

```bash
# 检查 token 是否过期
expires_at=$(cat token.json | jq -r '.expires_at')
now=$(date +%s)
if [ $now -gt $expires_at ]; then
    # 刷新 token
    refresh_token
fi
```

### 2. 时间处理

```bash
# 日期转时间戳
date -d "2026-03-07 15:00:00 Asia/Shanghai" +%s

# 时间戳转日期
date -d @1772866800 '+%Y-%m-%d %H:%M:%S %Z'

# 计算结束时间（1小时后）
start=$(date -d "tomorrow 15:00:00" +%s)
end=$((start + 3600))
```

### 3. 完整预约流程

```bash
# 1. 检查授权
oauth.sh check-auth

# 2. 查询会议室
calendar.sh list-rooms | grep "1910"

# 3. 计算时间
START=$(date -d "tomorrow 15:00:00" +%s)
END=$((START + 3600))

# 4. 完整预约
calendar.sh book-meeting "会议主题" $START $END "omm_xxx"
```

### 4. 错误处理

```bash
result=$(curl -s ...)
code=$(echo "$result" | jq -r '.code // -1')

case $code in
    0)
        echo "成功"
        ;;
    99991679)
        echo "权限不足，请重新授权"
        oauth.sh generate-auth
        ;;
    *)
        echo "错误: $(echo "$result" | jq -r '.msg')"
        ;;
esac
```
