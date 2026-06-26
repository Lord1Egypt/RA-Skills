---
name: sufn-smart-home
version: 1.0.2
tags: ["smart-home", "智能家居", "sufn", "三峰", "灯光", "场景控制"]
description: 三峰智能家居控制技能。适用场景：(1) 用户说"三峰登录 账号 密码"；(2) 用户说打开/关闭/调节灯/空调/窗帘/插座等设备；(3) 用户说同步设备、设备列表、场景列表、执行场景、家庭列表、进入家庭、帮助、三峰帮助；(4) 用户说任何模式/场景名称（如观影模式、阅读模式、回家等）。所有操作真实调用 API，不返回模拟结果。
---

> **技能激活说明**：
> - 用户发送「三峰登录 [账号] [密码]」时，调用本技能处理登录。
> - 用户发送设备控制指令（打开/关闭 + 设备名）时，调用本技能。
> - 用户说任何模式或场景名称时，调用本技能。

# 智能家居控制技能

## 外部服务声明

本技能调用以下外部 API：

- **https://open.aibasis.cc** —— 三峰智能家居（SUFN）官方开放平台 API，用于设备控制、场景执行、家庭数据同步、用户登录鉴权。

本技能不访问任何其他外部域名，不读写授权范围外的本地文件，不执行与智能家居控制无关的系统操作。

## 平台支持

- **Windows**：完全支持，使用 PowerShell + Invoke-RestMethod 调用 API。
- **macOS / Linux**：完全支持，使用 bash + curl 调用 API。

Agent 在执行前应先判断操作系统，选择下方对应章节的脚本。若检测失败，默认按 Windows 处理；非 Windows 环境下若未提供 bash 支持，回复用户「本技能在当前系统尚未完全适配，请在 Windows 环境使用」。

## 响应规则

- 所有操作真实调用 API，不返回模拟或伪造结果。
- 回复保持简洁，仅包含操作结果，不附加额外建议或多余提示。
- 每次操作只发一条消息。

---

## 状态文件

登录状态和设备数据持久化存储在 `{baseDir}/state.json`。

**读取**：使用标准 `read` 工具，path 填 `{baseDir}/state.json`。文件不存在时视为未登录。

**写入**：使用标准 `write` 工具，path 填 `{baseDir}/state.json`，content 为脚本输出的 JSON 字符串。

exec 工具仅用于调用 HTTP API，不用于文件读写。

**数据流约定**：下方所有脚本会在最后用 `Write-Output "STATE_JSON:<json>"`（PowerShell）或 `echo "STATE_JSON:<json>"`（bash）输出待持久化的 JSON。Agent 捕获该行后，提取 `STATE_JSON:` 之后的内容，用 `write` 工具写入 state.json。若脚本还输出了 `OK ...` 或 `FAIL ...` 行，则按该行决定回复文案。

---

## API 说明

Base URL：`https://open.aibasis.cc`
认证：所有接口 Header 加 `Authorization: Bearer <token>`

### 1. 登录
```
POST /api/user/login
Body: { "user": "xxx", "psw": "xxx" }
返回: { "code": 0, "data": { "token": "xxx", "home": { "id": "xxx", "name": "xxx" } } }
```

### 2. 获取家庭列表
```
GET /api/getHomeList
Headers: Authorization: Bearer <token>
返回: { "code": 0, "data": [{ "ID": "xxx", "NAME": "xxx" }] }
注意：字段名是大写 ID 和 NAME
```

### 3. 进入指定家庭
```
POST /api/inHome
Body: { "homeId": "xxx" }
返回: { "code": 0, "data": { "token": "xxx", "home": { "id": "xxx", "name": "xxx" } } }
注意：进入后 token 会更新，必须保存新 token
```

### 4. 同步家庭数据
```
POST /api/syncHomeData
Body: { "requestId": "sync_001", "timestamp": <毫秒时间戳>, "version": "1.0", "data": {} }
返回 data 包含: devices[]（含 id、name、model、roomId）、rooms[]（含 id、name）、scenes[]（含 id、name）
```

### 5. 控制设备或执行场景
```
POST /api/control
Body: {
  "requestId": "cmd_001",
  "timestamp": <毫秒时间戳>,
  "version": "1.0",
  "commands": [{ "id": "<设备id或场景id>", "model": "<设备model，场景为scene>", "properties": { <参数> } }]
}
```

lamp_5 设备 properties：{"open":1} 开、{"open":0} 关、{"brightness":80} 亮度、{"colorTemperature":4000} 色温、{"h":120,"s":100,"l":50} 颜色
执行场景：model="scene"，properties={}

---

## 操作流程

### 一、登录

触发词：`三峰登录 账号 密码`

**Windows (PowerShell)：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$body = @{ user = "账号"; psw = "密码" } | ConvertTo-Json
$res = Invoke-RestMethod -Method POST -Uri "https://open.aibasis.cc/api/user/login" -ContentType "application/json" -Body $body
if ($res.code -eq 0) {
  $token = $res.data.token
  $syncBody = @{ requestId = "sync_001"; timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds(); version = "1.0"; data = @{} } | ConvertTo-Json
  $syncRes = Invoke-RestMethod -Method POST -Uri "https://open.aibasis.cc/api/syncHomeData" -ContentType "application/json" -Headers @{ Authorization = "Bearer $token" } -Body $syncBody
  $devices = $syncRes.data.devices | ForEach-Object { @{ id = $_.id; name = $_.name; model = $_.model; roomId = $_.roomId } }
  $rooms = $syncRes.data.rooms | ForEach-Object { @{ id = [string]$_.id; name = $_.name } }
  $scenes = $syncRes.data.scenes | ForEach-Object { @{ id = $_.id; name = $_.name } }
  $state = @{ token = $token; home = @{ id = $res.data.home.id; name = $res.data.home.name }; devices = $devices; rooms = $rooms; scenes = $scenes }
  $json = $state | ConvertTo-Json -Depth 5 -Compress
  Write-Output "STATE_JSON:$json"
  Write-Output "OK home:$($res.data.home.name) devices:$($devices.Count) scenes:$($scenes.Count)"
} else {
  Write-Output "FAIL $($res.msg)"
}
```

**macOS / Linux (bash)：**

```bash
USER_NAME="账号"
USER_PSW="密码"
LOGIN_RES=$(curl -s -X POST "https://open.aibasis.cc/api/user/login" \
  -H "Content-Type: application/json" \
  -d "{\"user\":\"$USER_NAME\",\"psw\":\"$USER_PSW\"}")
CODE=$(echo "$LOGIN_RES" | jq -r '.code')
if [ "$CODE" = "0" ]; then
  TOKEN=$(echo "$LOGIN_RES" | jq -r '.data.token')
  HOME_ID=$(echo "$LOGIN_RES" | jq -r '.data.home.id')
  HOME_NAME=$(echo "$LOGIN_RES" | jq -r '.data.home.name')
  TS=$(($(date +%s)*1000))
  SYNC_BODY=$(jq -n --argjson ts "$TS" '{requestId:"sync_001",timestamp:$ts,version:"1.0",data:{}}')
  SYNC_RES=$(curl -s -X POST "https://open.aibasis.cc/api/syncHomeData" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "$SYNC_BODY")
  STATE=$(echo "$SYNC_RES" | jq --arg token "$TOKEN" --arg hid "$HOME_ID" --arg hname "$HOME_NAME" \
    '{token:$token, home:{id:$hid,name:$hname}, devices:[.data.devices[]|{id,name,model,roomId}], rooms:[.data.rooms[]|{id:(.id|tostring),name}], scenes:[.data.scenes[]|{id,name}]}')
  DEV_COUNT=$(echo "$STATE" | jq '.devices | length')
  SCENE_COUNT=$(echo "$STATE" | jq '.scenes | length')
  echo "STATE_JSON:$(echo "$STATE" | jq -c .)"
  echo "OK home:$HOME_NAME devices:$DEV_COUNT scenes:$SCENE_COUNT"
else
  MSG=$(echo "$LOGIN_RES" | jq -r '.msg')
  echo "FAIL $MSG"
fi
```

**Agent 处理**：
- 捕获 `STATE_JSON:` 行，用 `write` 工具写入 `{baseDir}/state.json`。
- 输出 `OK home:xxx devices:N scenes:M` 时回复：`✅ 登录成功，家庭：xxx，已同步设备 N 个、场景 M 个`。
- 输出 `FAIL xxx` 时回复：`❌ 登录失败：xxx`。
- 未提供账号密码时回复：`请用格式登录：三峰登录 账号 密码`。

---

### 二、家庭列表

触发词：`家庭列表`、`我的家庭`、`有哪些家庭`

先用 `read` 工具读取 state.json，获取 token，再执行：

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$token = "从 state.json 读取的 token"
$res = Invoke-RestMethod -Method GET -Uri "https://open.aibasis.cc/api/getHomeList" -Headers @{ Authorization = "Bearer $token" }
$total = $res.data.Count
$names = ($res.data | Select-Object -First 10 | ForEach-Object { $_.NAME }) -join "、"
Write-Output "OK total:$total names:$names"
```

**macOS / Linux：**

```bash
TOKEN="从 state.json 读取的 token"
RES=$(curl -s -X GET "https://open.aibasis.cc/api/getHomeList" -H "Authorization: Bearer $TOKEN")
TOTAL=$(echo "$RES" | jq '.data | length')
NAMES=$(echo "$RES" | jq -r '.data[:10] | map(.NAME) | join("、")')
echo "OK total:$TOTAL names:$NAMES"
```

回复：`🏠 共 N 个家庭，前10个：名称1、名称2...，发送「进入家庭 名称」切换`

---

### 三、进入家庭

触发词：`进入家庭 <名称>`、`切换家庭 <名称>`

流程：先用 `read` 读取 state.json 获取 token，从用户消息提取家庭名称关键词。

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$token = "从 state.json 读取的 token"
$keyword = "用户输入的名称"
$listRes = Invoke-RestMethod -Method GET -Uri "https://open.aibasis.cc/api/getHomeList" -Headers @{ Authorization = "Bearer $token" }
$home = $listRes.data | Where-Object { $_.NAME -like "*$keyword*" -or $keyword -like "*$($_.NAME)*" } | Select-Object -First 1
if ($home) {
  $body = @{ homeId = $home.ID } | ConvertTo-Json
  $res = Invoke-RestMethod -Method POST -Uri "https://open.aibasis.cc/api/inHome" -ContentType "application/json" -Headers @{ Authorization = "Bearer $token" } -Body $body
  $newToken = $res.data.token
  $syncBody = @{ requestId = "sync_001"; timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds(); version = "1.0"; data = @{} } | ConvertTo-Json
  $syncRes = Invoke-RestMethod -Method POST -Uri "https://open.aibasis.cc/api/syncHomeData" -ContentType "application/json" -Headers @{ Authorization = "Bearer $newToken" } -Body $syncBody
  $devices = $syncRes.data.devices | ForEach-Object { @{ id = $_.id; name = $_.name; model = $_.model; roomId = $_.roomId } }
  $rooms = $syncRes.data.rooms | ForEach-Object { @{ id = [string]$_.id; name = $_.name } }
  $scenes = $syncRes.data.scenes | ForEach-Object { @{ id = $_.id; name = $_.name } }
  $newState = @{ token = $newToken; home = @{ id = $res.data.home.id; name = $res.data.home.name }; devices = $devices; rooms = $rooms; scenes = $scenes }
  $json = $newState | ConvertTo-Json -Depth 5 -Compress
  Write-Output "STATE_JSON:$json"
  Write-Output "OK home:$($res.data.home.name) devices:$($devices.Count) scenes:$($scenes.Count)"
} else {
  $available = ($listRes.data | Select-Object -First 5 | ForEach-Object { $_.NAME }) -join "、"
  Write-Output "FAIL 未找到「$keyword」，可用：$available..."
}
```

**macOS / Linux：**

```bash
TOKEN="从 state.json 读取的 token"
KEYWORD="用户输入的名称"
LIST=$(curl -s -X GET "https://open.aibasis.cc/api/getHomeList" -H "Authorization: Bearer $TOKEN")
HOME=$(echo "$LIST" | jq -c --arg k "$KEYWORD" '.data | map(select(.NAME|contains($k)) // select($k|contains(.NAME))) | .[0] // empty')
if [ -n "$HOME" ] && [ "$HOME" != "null" ]; then
  HID=$(echo "$HOME" | jq -r '.ID')
  RES=$(curl -s -X POST "https://open.aibasis.cc/api/inHome" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "{\"homeId\":\"$HID\"}")
  NEW_TOKEN=$(echo "$RES" | jq -r '.data.token')
  HOME_ID=$(echo "$RES" | jq -r '.data.home.id')
  HOME_NAME=$(echo "$RES" | jq -r '.data.home.name')
  TS=$(($(date +%s)*1000))
  SYNC_BODY=$(jq -n --argjson ts "$TS" '{requestId:"sync_001",timestamp:$ts,version:"1.0",data:{}}')
  SYNC_RES=$(curl -s -X POST "https://open.aibasis.cc/api/syncHomeData" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $NEW_TOKEN" \
    -d "$SYNC_BODY")
  STATE=$(echo "$SYNC_RES" | jq --arg token "$NEW_TOKEN" --arg hid "$HOME_ID" --arg hname "$HOME_NAME" \
    '{token:$token, home:{id:$hid,name:$hname}, devices:[.data.devices[]|{id,name,model,roomId}], rooms:[.data.rooms[]|{id:(.id|tostring),name}], scenes:[.data.scenes[]|{id,name}]}')
  DEV_COUNT=$(echo "$STATE" | jq '.devices | length')
  SCENE_COUNT=$(echo "$STATE" | jq '.scenes | length')
  echo "STATE_JSON:$(echo "$STATE" | jq -c .)"
  echo "OK home:$HOME_NAME devices:$DEV_COUNT scenes:$SCENE_COUNT"
else
  AVAILABLE=$(echo "$LIST" | jq -r '.data[:5] | map(.NAME) | join("、")')
  echo "FAIL 未找到「$KEYWORD」，可用：$AVAILABLE..."
fi
```

**Agent 处理**：
- 捕获 `STATE_JSON:` 行，用 `write` 工具写入 state.json。
- 输出 `OK home:xxx devices:N scenes:M` 时回复：`✅ 已进入家庭：xxx，已同步设备 N 个、场景 M 个`。
- 输出 `FAIL xxx` 时回复：`❌ 切换失败：xxx`。

---

### 四、同步设备

触发词：`同步设备`、`刷新设备`

流程：先用 `read` 读取 state.json 获取 token 和 home 信息。

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$token = "从 state.json 读取"
$homeId = "从 state.json 读取"
$homeName = "从 state.json 读取"
$body = @{ requestId = "sync_001"; timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds(); version = "1.0"; data = @{} } | ConvertTo-Json
$res = Invoke-RestMethod -Method POST -Uri "https://open.aibasis.cc/api/syncHomeData" -ContentType "application/json" -Headers @{ Authorization = "Bearer $token" } -Body $body
$devices = $res.data.devices | ForEach-Object { @{ id = $_.id; name = $_.name; model = $_.model; roomId = $_.roomId } }
$rooms = $res.data.rooms | ForEach-Object { @{ id = [string]$_.id; name = $_.name } }
$scenes = $res.data.scenes | ForEach-Object { @{ id = $_.id; name = $_.name } }
$newState = @{ token = $token; home = @{ id = $homeId; name = $homeName }; devices = $devices; rooms = $rooms; scenes = $scenes }
$json = $newState | ConvertTo-Json -Depth 5 -Compress
Write-Output "STATE_JSON:$json"
Write-Output "OK devices:$($devices.Count) scenes:$($scenes.Count)"
```

**macOS / Linux：**

```bash
TOKEN="从 state.json 读取"
HOME_ID="从 state.json 读取"
HOME_NAME="从 state.json 读取"
TS=$(($(date +%s)*1000))
SYNC_BODY=$(jq -n --argjson ts "$TS" '{requestId:"sync_001",timestamp:$ts,version:"1.0",data:{}}')
RES=$(curl -s -X POST "https://open.aibasis.cc/api/syncHomeData" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$SYNC_BODY")
STATE=$(echo "$RES" | jq --arg token "$TOKEN" --arg hid "$HOME_ID" --arg hname "$HOME_NAME" \
  '{token:$token, home:{id:$hid,name:$hname}, devices:[.data.devices[]|{id,name,model,roomId}], rooms:[.data.rooms[]|{id:(.id|tostring),name}], scenes:[.data.scenes[]|{id,name}]}')
DEV_COUNT=$(echo "$STATE" | jq '.devices | length')
SCENE_COUNT=$(echo "$STATE" | jq '.scenes | length')
echo "STATE_JSON:$(echo "$STATE" | jq -c .)"
echo "OK devices:$DEV_COUNT scenes:$SCENE_COUNT"
```

**Agent 处理**：捕获 STATE_JSON 行用 `write` 工具写入；回复 `✅ 同步完成，设备 N 个，场景 M 个`。

---

### 五、设备列表

触发词：`设备列表`、`有哪些设备`

用 `read` 工具读取 state.json，按房间分组，回复：`📋 设备列表（共N个）房间1：设备1、设备2 房间2：设备3`

---

### 六、场景列表

触发词：`场景列表`、`有哪些场景`

用 `read` 工具读取 state.json，回复：`🎬 场景列表（共N个）：场景1、场景2、场景3...`

---

### 七、控制设备

触发词：打开/关闭/开启/关掉/调节/设置 + 设备名

流程：
1. 用 `read` 工具读取 state.json，检查 token 和 devices。
2. 无 token 提示登录；无 devices 提示同步设备。
3. 从用户指令提取设备名，模糊匹配 devices，获取 id 和 model。
4. 构造 properties：开 `{"open":1}`、关 `{"open":0}`、亮度 `{"brightness":XX}`、色温 `{"colorTemperature":XXXX}`、HSL 颜色 `{"h":X,"s":X,"l":X}`。
5. 用 exec 调用 `/api/control`，commands 必须带 model。
6. 成功回复：`✅ 已执行：设备名 操作描述`。
7. 失败回复：`❌ 控制失败：错误信息`。
8. 找不到设备：`❌ 未找到「关键词」，当前设备：设备1、设备2...`。

---

### 八、场景模式（智能场景）

触发词：任何模式名称（观影模式、阅读模式、回家、离家、睡眠等）

**处理逻辑**：

1. 用 `read` 工具读取 state.json，提取用户说的场景关键词。
2. 在 scenes 列表中模糊匹配（场景名包含关键词，或关键词包含场景名）。
3. **若找到匹配场景**：调用 `/api/control` 执行场景，回复：`✅ 已执行场景：场景名`。
4. **若未找到场景**：根据关键词语义推断灯光参数，对所有设备批量控制。

常见模式推断规则（若未匹配，根据语义自行判断）：
- 观影：brightness:20, colorTemperature:2700
- 阅读：brightness:100, colorTemperature:6500
- 睡眠 / 休息：brightness:5, colorTemperature:2700
- 起床 / 早晨：brightness:70, colorTemperature:5500
- 浪漫：brightness:20, colorTemperature:2700
- 专注 / 工作：brightness:100, colorTemperature:5500
- 聚会 / 会客：brightness:80, colorTemperature:4000
- 全开：open:1
- 全关 / 离家：open:0

批量控制时在一次 control 请求里将所有设备放入 commands 数组，不要逐个发请求。

**PowerShell 序列化提示**：嵌套对象序列化时需避免 properties 变成 `System.Collections.Hashtable` 字符串，建议用字符串拼接构造 commands JSON。

**Windows：**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$token = "从 state.json 读取"
$ts = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$props = '{"brightness":20,"colorTemperature":2700}'  # 根据场景替换参数
$devicesJson = "从 state.json 读取的 devices 数组"
$cmds = ($devicesJson | ForEach-Object { '{"id":"' + $_.id + '","model":"' + $_.model + '","properties":' + $props + '}' }) -join ","
$bodyStr = '{"requestId":"cmd_001","timestamp":' + $ts + ',"version":"1.0","commands":[' + $cmds + ']}'
$res = Invoke-RestMethod -Method POST -Uri "https://open.aibasis.cc/api/control" -ContentType "application/json" -Headers @{ Authorization = "Bearer $token" } -Body $bodyStr
Write-Output "OK code:$($res.code)"
```

**macOS / Linux：**

```bash
TOKEN="从 state.json 读取"
TS=$(($(date +%s)*1000))
PROPS='{"brightness":20,"colorTemperature":2700}'  # 根据场景替换参数
# DEVICES_JSON 为 state.json 中 devices 数组的 JSON 字符串
CMDS=$(echo "$DEVICES_JSON" | jq --argjson props "$PROPS" 'map({id:.id, model:.model, properties:$props})')
BODY=$(jq -n --argjson ts "$TS" --argjson cmds "$CMDS" '{requestId:"cmd_001",timestamp:$ts,version:"1.0",commands:$cmds}')
RES=$(curl -s -X POST "https://open.aibasis.cc/api/control" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$BODY")
CODE=$(echo "$RES" | jq -r '.code')
echo "OK code:$CODE"
```

回复：`✅ 已执行「场景名」：亮度XX%，色温XXXXK`

---

### 九、未登录时收到控制指令

回复：`请先登录，发送：三峰登录 账号 密码`

---

### 十、帮助

触发词：`帮助`、`三峰帮助`、`怎么用`、`有什么功能`

直接回复（不调用 API）：

`🏠 三峰智能家居指令：三峰登录 账号 密码 | 家庭列表 | 进入家庭 名称 | 同步设备 | 设备列表 | 场景列表 | 打开/关闭 设备名 | 设备名 亮度XX% | 设备名 色温XXXX | 观影模式/阅读模式/回家 等场景名`