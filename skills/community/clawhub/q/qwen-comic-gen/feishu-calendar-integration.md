# 📅 飞书日历集成脚本

**创建时间：** 2026-03-15 08:55  
**作者：** 阿香 🦞

---

## 功能说明

检查飞书日历事件，生成今日日程提醒。

---

## API 调用示例

### 1. 获取日历列表

```powershell
# 需要 Access Token
$accessToken = "your_access_token"

# 获取日历列表
$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}

$response = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/calendar/v4/calendars" -Method GET -Headers $headers
```

### 2. 获取日历事件

```powershell
# 获取今日事件
$calendarId = "primary"
$timeMin = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
$timeMax = (Get-Date).AddDays(1).ToString("yyyy-MM-ddTHH:mm:ssZ")

$uri = "https://open.feishu.cn/open-apis/calendar/v4/calendars/$calendarId/events"
$queryParams = "?time_min=$timeMin&time_max=$timeMax"

$response = Invoke-RestMethod -Uri ($uri + $queryParams) -Method GET -Headers $headers
```

### 3. 解析事件数据

```powershell
# 解析事件
$events = $response.data.events

foreach ($event in $events) {
    $title = $event.summary
    $startTime = $event.start_time
    $endTime = $event.end_time
    
    Write-Host "事件：$title"
    Write-Host "时间：$startTime - $endTime"
}
```

---

## 集成到优先级提醒

### 步骤 1：获取 Access Token

需要配置飞书应用的 App ID 和 App Secret。

### 步骤 2：调用日历 API

使用 tenant_access_token 调用日历 API。

### 步骤 3：生成提醒文案

```
📅 今日日程（飞书）：
- 10:00 团队站会
- 14:00 项目评审
- 16:30 1 对 1 会议
```

---

## 注意事项

1. 需要飞书应用的 API 权限
2. 需要处理 API 限流
3. 需要缓存 Token 避免频繁刷新

---

_实施中，持续更新..._
