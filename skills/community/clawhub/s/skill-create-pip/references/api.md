# Ecovacs Robot Control API Reference

## Auth & Device Discovery

### Step 1: Login (ITLogin)
```
POST https://api-app.dc-cn.cn.ecouser.net/api/users/user.do
```
```json
{
  "todo": "ITLogin",
  "me": "<phone_or_email>",
  "password": "<md5(password)>",
  "resource": "<resource>",
  "last": "",
  "country": "CN",
  "org": "ECOCN",
  "edition": "ECOGLOBLE"
}
```
Returns: `token`, `userId`, `resource`

**Resource generation (Android domestic):**
```python
import hashlib, uuid
def gen_resource():
    uid = str(uuid.uuid4())
    r = hashlib.md5(uid.encode()).hexdigest()[:7]
    ck = hashlib.md5(r[-3:].encode()).hexdigest()[-1]
    return f"ANDROID{r}E{ck}"
```

**Password:** MD5 hex of plaintext password.

---

### Step 2: Get Device List
```
POST https://api-app.dc-cn.cn.ecouser.net/api/appsvr/app.do
```
```json
{
  "userid": "<userid>",
  "todo": "GetGlobalDeviceList",
  "defaultLang": "zh", "lang": "en",
  "appVer": "1.5.0", "platform": "Android",
  "channel": "c_test", "vendor": "",
  "auth": { "token": "<token>", "resource": "<resource>",
            "userid": "<userid>", "with": "users", "realm": "ecouser.net" },
  "aliliving": true, "app_robotconfig": false
}
```
Returns: `devices[]` — each device has:
- `did` → **toId**
- `resource` → **toRes**
- `class` → **toType**
- `deviceName`, `nick`, `status` (1=online, 0=offline)
- `service.mqs` → devmanager host

---

### Step 3: Send Command (devmanager)
```
POST https://<device.service.mqs>/api/iot/devmanager.do
```
```json
{
  "rn": "<cmdName>",
  "payloadType": "j",
  "payload": {
    "header": { "pri": 1, "ts": "<ms_timestamp>", "tzm": 480, "ver": "0.0.1" },
    "body": { "data": { "<cmd_params>" } }
  },
  "auth": { "token": "<token>", "resource": "<resource>",
            "userid": "<userid>", "with": "users", "realm": "ecouser.net" },
  "toType": "<device.class>",
  "toRes": "<device.resource>",
  "toId": "<device.did>",
  "td": "q",
  "cmdName": "<cmdName>"
}
```
**Critical:** `toType` = device's `class` field (e.g. `o0lqjm`), NOT `"device"` or `"USER"`.

---

## Core Protocol Reference

### Battery
| cmd | body.data |
|-----|-----------|
| `getBattery` | `{}` |
| `onBattery` (report) | `{ value: 0-100, isLow: 0/1 }` |

---

### Clean Control (clean_V2)
| act | description |
|-----|-------------|
| `start` | 开始清扫 |
| `pause` | 暂停 |
| `resume` | 继续 |
| `stop` | 停止 |

```json
// 全屋自动清扫
{ "act": "start", "content": { "type": "auto", "count": 1 } }

// 区域清扫
{ "act": "start", "content": { "type": "spotArea", "value": "mssid1,mssid2", "count": 1 } }

// 自定义框清扫
{ "act": "start", "content": { "type": "customArea", "value": "x1,y1,x2,y2;x1,y1,x2,y2" } }

// 定点清扫
{ "act": "start", "content": { "type": "spot", "value": "x,y" } }

// 暂停/继续/停止
{ "act": "pause" }
{ "act": "resume" }
{ "act": "stop" }
```

**content.cleanset** (可选，覆盖全局设置):
`"cleanCount,speed,waterAmount,workMode"` e.g. `"1,1,2,0"`

---

### Charge (回充)
```json
// 回充
{ "act": "go" }
// 停止回充
{ "act": "stop" }
```

---

### Clean State (getCleanInfo_V2 / onCleanInfo_V2)
Response `data`:
```json
{
  "state": "clean|idle|goCharging|washing|move",
  "trigger": "app|button|sched|batteryLow|workComplete|workInterrupt",
  "cleanState": {
    "cid": "<clean_session_id>",
    "router": "random|plan",
    "motionState": "working|pause",
    "category": 0,
    "content": { "type": "auto", "count": 1, "value": "..." }
  }
}
```

---

### Stats (getStats / onStats)
Response `data`:
```json
{ "cid": "...", "area": 10, "time": 600, "type": "auto", "avoidCount": 3, "aiopen": 1 }
```
- `area`: 平方米
- `time`: 秒

---

### Speed (吸力)
```json
// get: {}
// set: { "speed": 0 }
```
Values: `1000`=静音, `0`=标准, `1`=强劲, `2`=超强

---

### WaterInfo (水量)
```json
// get: {}
// set: { "amount": 2 }
```
Values: `1`=低, `2`=中, `3`=高, `4`=超高
`enable`: 1=拖地模式, 0=普通清扫

---

### WorkMode (扫拖模式)
```json
// get: {}
// set: { "mode": 0 }
```
Values: `0`=边扫边拖, `1`=仅扫地, `2`=仅拖地, `3`=先扫后拖

---

### LifeSpan (耗材)
```json
// get: { "type": "brush,sideBrush,heap,filter" }
```
Returns array: `[ { "type": "brush", "left": 80, "total": 100 } ]`
Types: `brush`滚刷, `sideBrush`边刷, `heap`尘盒滤网, `filter`空气滤芯, `roundMop`拖布, `wbHeap`水箱滤芯

---

### AutoEmpty (3D集尘)
```json
// get: {}
// start: { "act": "start" }
// set auto: { "enable": 1, "frequency": "auto|standard|smart|10|15|25" }
```
Status: `0`=关, `1`=集尘中, `2`=完成, `3`=尘盖开启, `4`=尘袋未装, `5`=尘袋已满

---

### CachedMapInfo (地图列表)
```json
// get: {}
```
Returns: `[ { "mid": "...", "index": 0, "name": "...", "status": 0, "using": 1 } ]`

---

### MapSet / MapSet_V2 (区域信息)
```json
// get: { "mid": "<map_id>", "type": "ar" }
```
Returns subsets (房间区域): `[ { "mssid": "...", "name": "客厅", "subtype": 1 } ]`

subtype: `0`默认, `1`客厅, `2`餐厅, `3`卧室, `4`书房, `5`厨房, `6`卫浴

---

### Sched_V2 (预约)
```json
// get: { "type": 1 }
// add:
{
  "act": "add", "enable": 1,
  "sid": "1", "repeat": "0000000",
  "hour": 8, "minute": 0,
  "mid": "<map_id>",
  "content": {
    "name": "clean",
    "jsonStr": "{\"router\":\"plan\",\"content\":{\"type\":\"auto\",\"value\":\"\"}}"
  }
}
// delete: { "act": "del", "sid": "1", "mid": "<map_id>" }
```
`repeat`: 7位，周日到周六，`1`=有预约，`0000000`=仅一次

---

### Error Codes (onError)
常见: `0`=清扫完成, `102`=卡住, `103`=悬崖检测, `104`=电量不足, `110`=尘盒未装

---

### Evt Codes (onEvt)
常见: `1`=清扫开始, `2`=清扫暂停, `3`=清扫停止, `1025`=低电回充充电, `1099`=集尘完成
