# WHEN 时钟 HTTP 接口说明

适用对象：通过 HTTP 读取/设置 WHEN 时钟参数的用户与平台对接方。

产品页面：https://iottimer.com/products/when/

---

## 1. 产品与接口定位

- 产品名称：WHEN
- 常见型号：由设备实时返回（建议通过 `GET /get?type=10` 的 `model` 字段获取）
- 固件版本：由设备实时返回（`ver_now`）
- 通信方式：局域网 HTTP（设备内置 Web 页面同样调用本协议）

说明：本协议既可给浏览器页面使用，也可给你自己的上位机/服务脚本使用。

---

## 2. 基础访问规则

### 2.1 路由

- `GET /`
- `GET /html?id=<页面ID>`
- `GET /style.css`
- `GET /clock.js`
- `GET /Language`
- `GET /get?type=<int>`
- `POST /set`

### 2.2 请求与响应

- `GET /get`：按 `type` 返回 JSON 数据
- `POST /set`：请求体必须是 JSON，必须包含 `type`
- `POST /set` 通用响应：

```json
{"status":0,"msg":"succ"}
```

`status` 语义：

- `0`：成功
- `1`：业务失败
- `101`：无数据
- `102`：数据过长

---

## 3. 登录与会话

### 3.1 登录流程

请求：

`POST /set`

```json
{
  "type": 86,
  "pass": "<SHA256(明文密码)后的64位十六进制字符串>"
}
```

成功后：

- 响应体：`{"status":0,"msg":"succ"}`
- 响应头：`Set-Cookie: Session-Key=...`

后续请求建议带 Cookie。

### 3.2 登录开关配置

请求：`type=16`

```json
{
  "type": 16,
  "loginSW": true,
  "newPwd": "<64位十六进制sha256>"
}
```

字段说明：

- `loginSW`：是否开启登录保护
- `newPwd`：新密码的 SHA256（仅在开启时必填）

---

## 4. 前端业务流程（结合页面逻辑）

以下是页面的实际调用顺序，便于第三方按同样逻辑接入：

1. 页面初始化：先 `GET /get?type=85`
   - 若返回 `Login=true`：先登录
   - 若 `firstSet=true`：进入语言/时区首次设置
2. 网络页：
   - 读取当前配置：`GET /get?type=2`
   - 刷新Wi-Fi列表：`POST /set {"type":22}` 后轮询 `GET /get?type=22`
   - 尝试联网：`POST /set {"type":23,...}` 后轮询 `GET /get?type=23`
   - 仅保存网络参数：`POST /set {"type":2,...}`
3. 各功能页进入时均先 `GET /get?type=...` 拉取，再 `POST /set` 保存
4. 设备控制（重启/授时/恢复出厂）通过动作型 type 触发

---

## 5. GET 查询接口详细说明（表格版）

入口：`GET /get?type=<int>`

### 5.1 通用网络状态字段（type=2/22/23 会出现）

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `netSET` | int | `0/1` | `1` | 是否已保存网络参数 |
| `netCON` | int | `0未开始/1进行中/2失败/3成功` | `3` | 路由器连接状态 |
| `netNTP` | int | `0未开始/1进行中/2失败/3成功` | `3` | NTP 同步状态 |
| `netSer` | int | `0未开始/1进行中/2失败/3成功` | `3` | 服务器连接状态 |
| `netWea` | int | 当前通常为 `0` | `0` | 天气获取状态 |

返回示例：

```json
{
  "netSET": 1,
  "netCON": 3,
  "netNTP": 3,
  "netSer": 3,
  "netWea": 0
}
```

### 5.2 type=2 网络信息

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `isAP` | bool | `true/false` | `true` | 是否处于 AP 配网模式 |
| `ssid` | string | 0~32 字符（常见） | `"MyWiFi"` | 当前保存的 Wi-Fi 名称 |
| `password` | string | 0~64 字符（常见） | `"12345678"` | 当前保存的 Wi-Fi 密码 |
| `bindBssid` | bool | `true/false` | `false` | 是否绑定指定热点 MAC |
| `list` | string[] | SSID 数组 | `["MyWiFi","Office"]` | 扫描得到的热点名 |
| `listDetail[].ssid` | string | 热点名 | `"Office"` | 扫描详情中的 SSID |
| `listDetail[].rssi` | int | 常见 `-100~-20` dBm | `-58` | 信号强度 |
| `listDetail[].authmode` | int | 平台认证枚举值 | `3` | 加密方式编号 |
| `listDetail[].primary` | int | `1~13`（常见） | `6` | Wi-Fi 信道 |
| `listDetail[].bssid` | int[6] | 每段 `0~255` | `[44,112,79,66,154,229]` | 热点 MAC |
| `isDHCP` | bool | `true/false` | `true` | 是否自动获取 IP |
| `ip` | int[4] | 每段 `0~255` | `[192,168,1,33]` | 设备 IP |
| `mask` | int[4] | 每段 `0~255` | `[255,255,255,0]` | 子网掩码 |
| `gateway` | int[4] | 每段 `0~255` | `[192,168,1,1]` | 网关 |
| `DNS` | int[4] | 每段 `0~255` | `[223,5,5,5]` | 主 DNS |
| `subDNS` | int[] | `[]` 或 `int[4]` | `[]` | 备用 DNS |
| `MAC` | int[6] | 每段 `0~255` | `[140,37,5,154,63,19]` | 设备 MAC |
| `netSET` | int | `0/1` | `1` | 见 5.1 |
| `netCON` | int | `0~3` | `3` | 见 5.1 |
| `netNTP` | int | `0~3` | `3` | 见 5.1 |
| `netSer` | int | `0~3` | `3` | 见 5.1 |
| `netWea` | int | 通常 `0` | `0` | 见 5.1 |

返回示例：

```json
{
  "isAP": true,
  "ssid": "MyWiFi",
  "password": "12345678",
  "bindBssid": false,
  "list": ["MyWiFi", "Office"],
  "listDetail": [
    {"ssid": "MyWiFi", "rssi": -58, "authmode": 3, "primary": 6, "bssid": [44,112,79,66,154,229]}
  ],
  "isDHCP": true,
  "ip": [192,168,1,33],
  "mask": [255,255,255,0],
  "gateway": [192,168,1,1],
  "DNS": [223,5,5,5],
  "subDNS": [],
  "MAC": [140,37,5,154,63,19],
  "netSET": 1,
  "netCON": 3,
  "netNTP": 3,
  "netSer": 3,
  "netWea": 0
}
```

### 5.3 type=22 Wi-Fi 扫描结果

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `bindBssid` | bool | `true/false` | `true` | 当前绑定策略 |
| `list` | string[] | SSID 数组 | `["MyWiFi","Cafe"]` | 扫描到的热点名 |
| `listDetail[].ssid` | string | 热点名 | `"Cafe"` | 明细 SSID |
| `listDetail[].rssi` | int | 常见 `-100~-20` | `-70` | 明细信号强度 |
| `listDetail[].authmode` | int | 平台认证枚举值 | `4` | 明细加密模式 |
| `listDetail[].primary` | int | `1~13`（常见） | `11` | 明细信道 |
| `listDetail[].bssid` | int[6] | 每段 `0~255` | `[120,45,12,88,77,66]` | 明细 MAC |
| `getOK` | bool | `true/false` | `true` | 扫描是否完成 |
| `netSET` | int | `0/1` | `1` | 见 5.1 |
| `netCON` | int | `0~3` | `1` | 见 5.1 |
| `netNTP` | int | `0~3` | `0` | 见 5.1 |
| `netSer` | int | `0~3` | `0` | 见 5.1 |
| `netWea` | int | 通常 `0` | `0` | 见 5.1 |

返回示例：

```json
{
  "bindBssid": true,
  "list": ["MyWiFi", "Cafe"],
  "listDetail": [
    {"ssid": "Cafe", "rssi": -70, "authmode": 4, "primary": 11, "bssid": [120,45,12,88,77,66]}
  ],
  "getOK": true,
  "netSET": 1,
  "netCON": 1,
  "netNTP": 0,
  "netSer": 0,
  "netWea": 0
}
```

### 5.4 type=23 网络连接状态（轮询）

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `netSET` | int | `0/1` | `1` | 见 5.1 |
| `netCON` | int | `0~3` | `1` | 路由连接进行中时通常为 `1` |
| `netNTP` | int | `0~3` | `0` | 未开始同步时为 `0` |
| `netSer` | int | `0~3` | `0` | 未连服务器时为 `0` |
| `netWea` | int | 通常 `0` | `0` | 天气状态 |

返回示例：

```json
{
  "netSET": 1,
  "netCON": 1,
  "netNTP": 0,
  "netSer": 0,
  "netWea": 0
}
```

### 5.5 type=3 时区与 NTP

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `ntp` | string[] | 最多 2 项 | `["ntp1.aliyun.com","pool.ntp.org"]` | NTP 服务器列表 |
| `adjustNTP` | int | 毫秒，正负均可 | `12` | NTP 校时补偿 |
| `filter` | bool | `true/false` | `true` | 是否启用延迟滤波 |
| `limit` | int | 毫秒，`0`=关闭 | `150` | 延迟阈值 |
| `tolerant` | bool | `true/false` | `false` | 是否宽松校验 |
| `timezone` | int | 分钟偏移 | `480` | 主时区（北京时间） |
| `dstSW` | bool | `true/false` | `false` | 主时区夏令时开关 |
| `dstOffset` | int | 分钟 | `60` | 主时区夏令时偏移 |
| `dstStartMonth` | int | `1~12` | `3` | 夏令时开始月 |
| `dstStartWeek` | int | `1~5`（常见） | `2` | 夏令时开始第几周 |
| `dstStartDay` | int | `0~6`（周日~周六） | `0` | 夏令时开始星期 |
| `dstStartTime` | int | 分钟（0~1439） | `120` | 夏令时开始时刻 |
| `dstEndMonth` | int | `1~12` | `11` | 夏令时结束月 |
| `dstEndWeek` | int | `1~5`（常见） | `1` | 夏令时结束第几周 |
| `dstEndDay` | int | `0~6` | `0` | 夏令时结束星期 |
| `dstEndTime` | int | 分钟（0~1439） | `180` | 夏令时结束时刻 |
| `timezone2` | int | 分钟偏移 | `540` | 副时区 |
| `dst2SW` | bool | `true/false` | `false` | 副时区夏令时开关 |
| `dst2Offset` | int | 分钟 | `60` | 副时区夏令时偏移 |
| `dst2StartMonth` | int | `1~12` | `3` | 副时区开始月 |
| `dst2StartWeek` | int | `1~5`（常见） | `2` | 副时区开始周 |
| `dst2StartDay` | int | `0~6` | `0` | 副时区开始星期 |
| `dst2StartTime` | int | 分钟（0~1439） | `120` | 副时区开始时刻 |
| `dst2EndMonth` | int | `1~12` | `11` | 副时区结束月 |
| `dst2EndWeek` | int | `1~5`（常见） | `1` | 副时区结束周 |
| `dst2EndDay` | int | `0~6` | `0` | 副时区结束星期 |
| `dst2EndTime` | int | 分钟（0~1439） | `180` | 副时区结束时刻 |

返回示例：

```json
{
  "ntp": ["ntp1.aliyun.com", "pool.ntp.org"],
  "adjustNTP": 12,
  "filter": true,
  "limit": 150,
  "tolerant": false,
  "timezone": 480,
  "dstSW": false,
  "dstOffset": 60,
  "dstStartMonth": 3,
  "dstStartWeek": 2,
  "dstStartDay": 0,
  "dstStartTime": 120,
  "dstEndMonth": 11,
  "dstEndWeek": 1,
  "dstEndDay": 0,
  "dstEndTime": 180,
  "timezone2": 540,
  "dst2SW": false,
  "dst2Offset": 60,
  "dst2StartMonth": 3,
  "dst2StartWeek": 2,
  "dst2StartDay": 0,
  "dst2StartTime": 120,
  "dst2EndMonth": 11,
  "dst2EndWeek": 1,
  "dst2EndDay": 0,
  "dst2EndTime": 180
}
```

### 5.6 type=4 / type=5 显示参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `page1_1`~`page3_3` | int | 页面内容枚举 | `1` | 3页×3区内容配置 |
| `page1_3_1`~`page3_3_3` | int | 子项内容枚举 | `2` | 第3区的细分内容 |
| `page1Time/page2Time/page3Time` | int | 秒，常见 `1~255` | `5` | 各页停留时长 |
| `page2SW/page3SW` | bool | `true/false` | `true` | 第2/3页开关 |
| `timeZero` | bool | `true/false` | `true` | 时间前导零 |
| `dateZero` | bool | `true/false` | `false` | 日期前导零 |
| `is12H` | bool | `true/false` | `false` | 12 小时制 |
| `secFlash` | bool | `true/false` | `true` | 秒闪烁 |
| `dateFormat` | int | 日期格式枚举 | `0` | 日期显示格式 |
| `sundayType` | int | 周日起始/结束枚举 | `1` | 星期显示风格 |
| `countMode` | int | 计时模式枚举 | `0` | 倒计时/正计时策略 |
| `countTime` | int | Unix 秒 | `1735707600` | 计时目标时间 |
| `offset` | int | 分钟偏移 | `0` | 页面显示时间偏移 |
| `isTempF` | bool | `true/false` | `false` | 温度单位（摄氏/华氏） |

type=4 返回示例：

```json
{
  "page1_1": 1,
  "page1_2": 2,
  "page1_3": 3,
  "page1_3_1": 2,
  "page1Time": 5,
  "page2SW": true,
  "page3SW": true,
  "timeZero": true,
  "dateZero": false,
  "is12H": false,
  "secFlash": true,
  "dateFormat": 0,
  "sundayType": 1,
  "countMode": 0,
  "countTime": 1735707600,
  "offset": 0,
  "isTempF": false
}
```

type=5 返回示例：

```json
{
  "page2_1": 1,
  "page2_2": 4,
  "page2_3": 3,
  "page2_3_1": 1,
  "page2Time": 8,
  "page3_1": 2,
  "page3_2": 5,
  "page3_3": 3,
  "page3_3_1": 2,
  "page3Time": 6
}
```

### 5.7 type=6 休眠参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `pwSwitch` | bool | `true/false` | `true` | 休眠总开关 |
| `pwMode` | int | `0定时/1感光/2定时+感光` | `2` | 休眠模式 |
| `pwOn` | int | 分钟（0~1439） | `420` | 每日开机时间（07:00） |
| `pwOff` | int | 分钟（0~1439） | `1380` | 每日关机时间（23:00） |
| `pwSen` | int | 感光灵敏度枚举 | `1` | 感光触发灵敏度 |
| `pwOffTime` | int | `0~5` | `2` | 关机延迟档位 |
| `week` | int | 星期位图 | `31` | 生效星期（示例：周一到周五） |

返回示例：

```json
{
  "pwSwitch": true,
  "pwMode": 2,
  "pwOn": 420,
  "pwOff": 1380,
  "pwSen": 1,
  "pwOffTime": 2,
  "week": 31
}
```

### 5.8 type=7 闹钟参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `offMode` | int | `0按键/1感光/2按键+感光/3自动` | `0` | 闹钟关闭方式 |
| `sensitivity` | int | `0高/1中/2低` | `1` | 感光关闭灵敏度 |
| `holidaysStatus` | int | `0未获取/1已获取/2手动` | `1` | 节假日数据状态 |
| `updateTime` | int | Unix 秒 | `1735603200` | 节假日更新时间 |
| `alarmNum` | int | `0~10` | `3` | 闹钟数量 |
| `alarmInfo[].mode` | int | `0关/1单次/2每周/3节假日` | `2` | 单个闹钟模式 |
| `alarmInfo[].week` | int | 星期位图 | `31` | 每周模式下生效日 |
| `alarmInfo[].ring` | int | 铃音编号（0基） | `4` | 闹钟铃音 |
| `alarmInfo[].time` | int | 秒（0~86399） | `27000` | 触发时刻（07:30） |
| `alarmInfo[].delay` | int | 持续时长档位 | `2` | 响铃持续档位 |

返回示例：

```json
{
  "offMode": 0,
  "sensitivity": 1,
  "holidaysStatus": 1,
  "updateTime": 1735603200,
  "alarmNum": 2,
  "alarmInfo": [
    {"mode": 2, "week": 31, "ring": 4, "time": 27000, "delay": 2},
    {"mode": 1, "week": 0, "ring": 3, "time": 75600, "delay": 1}
  ]
}
```

### 5.9 type=8 系统参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `language` | int | `0中文/1繁中/2英文/3日文` | `0` | 界面语言 |
| `offset` | int | RTC 补偿（整数） | `0` | 硬件时钟校准值 |
| `ctpe` | int | 自动校时周期档位 | `2` | 自动授时间隔 |
| `ledState` | bool | `true/false` | `true` | 网络指示灯开关 |
| `link` | int | 连接策略枚举 | `1` | 断网重连策略 |
| `resetSW` | bool | `true/false` | `false` | 定时重启开关 |
| `resetTime` | int | 分钟（0~1439） | `240` | 定时重启时刻（04:00） |
| `timerBeep` | int | 铃音编号（0基） | `3` | 计时器铃音 |
| `timerDelay` | int | 延迟档位 | `1` | 计时器延迟 |
| `locMode` | int | `1自动(IP)/2自定义` | `1` | 定位模式 |
| `locCountry` | int | 地区编号 | `0` | 国家/地区 |
| `locCode` | string | 地区编码字符串 | `"101010100"` | 城市编码 |
| `locName` | string | 文本 | `"北京"` | 城市名称 |
| `locTime1` | string | 文本（可空） | `"08:30"` | 定位/天气展示字段1 |
| `locTime2` | string | 文本（可空） | `"18:45"` | 定位/天气展示字段2 |

返回示例：

```json
{
  "language": 0,
  "offset": 0,
  "ctpe": 2,
  "ledState": true,
  "link": 1,
  "resetSW": false,
  "resetTime": 240,
  "timerBeep": 3,
  "timerDelay": 1,
  "locMode": 1,
  "locCountry": 0,
  "locCode": "101010100",
  "locName": "北京",
  "locTime1": "08:30",
  "locTime2": "18:45"
}
```

### 5.10 type=9 报时参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `ring_hour` | int | 铃音编号（0基） | `1` | 整点铃音 |
| `ring_30min` | int | 铃音编号（0基） | `0` | 半点铃音 |
| `ring_15min` | int | 铃音编号（0基） | `0` | 15 分钟铃音 |
| `TK_time` | int | 24小时位图 | `16777215` | 报时生效时段 |
| `week` | int | 星期位图 | `127` | 报时生效星期 |

返回示例：

```json
{
  "ring_hour": 1,
  "ring_30min": 0,
  "ring_15min": 0,
  "TK_time": 16777215,
  "week": 127
}
```

### 5.11 type=10 设备信息

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `id` | string | 设备唯一ID | `"61b4c0756c5a49a296004c23"` | 设备身份标识 |
| `model` | string | 型号字符串 | `"CWT9S19"` | 设备型号 |
| `name` | string | 产品名称 | `"WHEN"` | 产品名 |
| `ver_now` | string | 版本号文本 | `"2.4.7"` | 当前固件版本 |
| `ver_new` | string | 版本号或 `None` | `"None"` | 可升级版本 |
| `ver_note` | string | 文本（可空） | `""` | 升级说明 |
| `auth` | bool | `true/false` | `true` | 设备认证状态 |
| `rtc` | int | RTC 型号编号 | `81` | RTC 芯片类型 |
| `factoryTime` | int | Unix 秒 | `1680316800` | 出厂时间 |

返回示例：

```json
{
  "id": "61b4c0756c5a49a296004c23",
  "model": "CWT9S19",
  "name": "WHEN",
  "ver_now": "2.4.7",
  "ver_new": "None",
  "ver_note": "",
  "auth": true,
  "rtc": 81,
  "factoryTime": 1756961043
}
```

### 5.12 type=11 / 14 / 15 节假日参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `holidaysStatus` | int | `0未获取/1已获取/2手动` | `2` | 节假日数据状态 |
| `updateTime` | int | Unix 秒 | `1735603200` | 节假日更新时间 |
| `dataSources` | int | `0自动/1手动` | `1` | 数据来源模式 |
| `regions` | int | `0内地/1日本` | `0` | 地区规则 |
| `week` | int | 星期位图 | `31` | 工作周模板 |
| `offDayLen` | int | `0~50` | `11` | 休息日数量 |
| `offDayList` | int[] | 年内天序号数组 | `[1,2,3,35,36]` | 法定休息日 |
| `workDayLen` | int | `0~30` | `2` | 调休工作日数量 |
| `workDayList` | int[] | 年内天序号数组 | `[40,41]` | 法定工作日 |

type=11 返回示例：

```json
{
  "holidaysStatus": 1,
  "updateTime": 1735603200,
  "dataSources": 0,
  "regions": 0,
  "week": 31,
  "offDayLen": 5,
  "offDayList": [1,2,3,35,36],
  "workDayLen": 2,
  "workDayList": [40,41]
}
```

type=14 返回示例：

```json
{
  "holidaysStatus": 2,
  "offDayLen": 4,
  "offDayList": [1,2,3,35]
}
```

type=15 返回示例：

```json
{
  "holidaysStatus": 2,
  "workDayLen": 2,
  "workDayList": [40,41]
}
```

### 5.13 type=12 感光参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `nowLT` | int | ADC 原始值 | `812` | 当前环境光强 |
| `nowLeve` | int | 亮度档位（1基） | `4` | 当前亮度档 |
| `minLT` | int | 阈值整数 | `150` | 低区最小阈值 |
| `maxLT` | int | 阈值整数 | `500` | 低区最大阈值 |
| `minLT_H` | int | 阈值整数 | `501` | 高区最小阈值 |
| `maxLT_H` | int | 阈值整数 | `1023` | 高区最大阈值 |

返回示例：

```json
{
  "nowLT": 812,
  "nowLeve": 4,
  "minLT": 150,
  "maxLT": 500,
  "minLT_H": 501,
  "maxLT_H": 1023
}
```

### 5.14 type=13 亮度参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `lightMode` | int | 模式枚举（固定/感光/定时） | `2` | 亮度策略 |
| `lightMin` | int | 亮度档位整数 | `2` | 最小亮度 |
| `lightMax` | int | 亮度档位整数 | `8` | 最大亮度 |
| `lightTime1` | int | 分钟（0~1439） | `420` | 时段1开始（07:00） |
| `lightTime2` | int | 分钟（0~1439） | `1320` | 时段2开始（22:00） |

返回示例：

```json
{
  "lightMode": 2,
  "lightMin": 2,
  "lightMax": 8,
  "lightTime1": 420,
  "lightTime2": 1320
}
```

### 5.15 type=16 登录设置

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `typeID` | int | 固定 `16` | `16` | 数据类型标识 |
| `loginSW` | bool | `true/false` | `true` | 是否开启登录校验 |

返回示例：

```json
{
  "typeID": 16,
  "loginSW": true
}
```

### 5.16 type=17 温度设置

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `typeID` | int | 固定 `17` | `17` | 数据类型标识 |
| `sensorType` | int | `0=M1601B/1=18B20` | `1` | 温度传感器类型 |
| `powerDelay` | int | `0~9` | `2` | 上电延时档位 |
| `brightnessDelay` | int | `0~4` | `1` | 亮度切换延时档位 |
| `offset` | int[] | 最多 11 项 | `[0,0,1,1,0,0,0,0,0,0,0]` | 分段温度补偿 |

返回示例：

```json
{
  "typeID": 17,
  "sensorType": 1,
  "powerDelay": 2,
  "brightnessDelay": 1,
  "offset": [0,0,1,1,0,0,0,0,0,0,0]
}
```

### 5.17 type=85 首次设置信息

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `typeID` | int | 固定 `85` | `85` | 数据类型标识 |
| `Login` | bool | `true/false` | `true` | 当前是否要求登录 |
| `firstSet` | bool | `true/false` | `false` | 是否首次配置流程 |
| `language` | int | `0中文/1繁中/2英文/3日文` | `0` | 当前语言 |
| `timezone` | int | 分钟偏移 | `480` | 当前主时区 |

返回示例：

```json
{
  "typeID": 85,
  "Login": true,
  "firstSet": false,
  "language": 0,
  "timezone": 480
}
```

---

## 6. POST 设置接口详细说明

入口：`POST /set`

请求头建议：`Content-Type: application/json`

### 6.1 参数保存类 type

### type=2 网络参数保存

字段：

- `ssid`：Wi-Fi 名称
- `password`：Wi-Fi 密码
- `bindBssid`：是否绑定BSSID（可选）
- `bssid`：目标热点MAC（int[6]，可选）
- `isDHCP`：是否DHCP
- `ip/mask/gateway/DNS/subDNS`：静态网络参数（非DHCP时生效）
- `MAC`：设备MAC（int[6]）

示例：

```json
{
  "type": 2,
  "ssid": "OfficeWiFi",
  "password": "12345678",
  "bindBssid": true,
  "bssid": [44,112,79,66,154,229],
  "isDHCP": true,
  "ip": [192,168,1,99],
  "mask": [255,255,255,0],
  "gateway": [192,168,1,1],
  "DNS": [223,5,5,5],
  "subDNS": [119,29,29,29],
  "MAC": [140,37,5,154,63,19]
}
```

### type=23 网络保存并立即重连

字段与 `type=2` 相同。

效果：保存后立即触发 Wi-Fi 重连与时间同步。

请求示例：

```json
{
  "type": 23,
  "ssid": "OfficeWiFi",
  "password": "12345678",
  "bindBssid": false,
  "isDHCP": true,
  "ip": [192,168,1,99],
  "mask": [255,255,255,0],
  "gateway": [192,168,1,1],
  "DNS": [223,5,5,5],
  "subDNS": [119,29,29,29],
  "MAC": [140,37,5,154,63,19]
}
```

### type=3 时区/NTP保存

字段：

- 主时区：`zone,dstSW,dstOffset,dstStartMonth,dstStartWeek,dstStartDay,dstStartTime,dstEndMonth,dstEndWeek,dstEndDay,dstEndTime`
- 副时区：`zone2,dst2SW,dst2Offset,dst2StartMonth,dst2StartWeek,dst2StartDay,dst2StartTime,dst2EndMonth,dst2EndWeek,dst2EndDay,dst2EndTime`
- NTP：`ntp`(string[]), `adjustNTP`, `filter`, `limit`, `tolerant`

说明：

- `zone/zone2` 单位为分钟（例如北京时间 `480`）
- `dstStartTime/dstEndTime` 单位为分钟（当天0点起）
- 保存后会重新初始化NTP流程

请求示例：

```json
{
  "type": 3,
  "zone": 480,
  "dstSW": false,
  "dstOffset": 60,
  "dstStartMonth": 3,
  "dstStartWeek": 2,
  "dstStartDay": 0,
  "dstStartTime": 120,
  "dstEndMonth": 11,
  "dstEndWeek": 1,
  "dstEndDay": 0,
  "dstEndTime": 180,
  "zone2": 540,
  "dst2SW": false,
  "dst2Offset": 60,
  "dst2StartMonth": 3,
  "dst2StartWeek": 2,
  "dst2StartDay": 0,
  "dst2StartTime": 120,
  "dst2EndMonth": 11,
  "dst2EndWeek": 1,
  "dst2EndDay": 0,
  "dst2EndTime": 180,
  "ntp": ["ntp1.aliyun.com", "pool.ntp.org"],
  "adjustNTP": 12,
  "filter": true,
  "limit": 150,
  "tolerant": false
}
```

### type=4 / type=5 显示保存

字段同 `GET type=4/5`。

说明：

- `type=4` 常用于基础显示参数页
- `type=5` 常用于扩展显示页

type=4 请求示例：

```json
{
  "type": 4,
  "page1_1": 1,
  "page1_2": 2,
  "page1_3": 3,
  "page1_3_1": 2,
  "page1Time": 5,
  "page2SW": true,
  "page3SW": true,
  "timeZero": true,
  "dateZero": false,
  "is12H": false,
  "secFlash": true,
  "dateFormat": 0,
  "sundayType": 1,
  "countMode": 0,
  "countTime": 1735707600,
  "offset": 0,
  "isTempF": false
}
```

type=5 请求示例：

```json
{
  "type": 5,
  "page2_1": 1,
  "page2_2": 4,
  "page2_3": 3,
  "page2_3_1": 1,
  "page2Time": 8,
  "page3_1": 2,
  "page3_2": 5,
  "page3_3": 3,
  "page3_3_1": 2,
  "page3Time": 6
}
```

### type=6 休眠保存

字段：`pwSwitch,pwOn,pwOff,pwMode,pwSen,pwOffTime,week`

说明：

- `pwOn/pwOff` 单位：分钟
- `week`：星期位图（建议沿用页面生成逻辑）

请求示例：

```json
{
  "type": 6,
  "pwSwitch": true,
  "pwOn": 420,
  "pwOff": 1380,
  "pwMode": 2,
  "pwSen": 1,
  "pwOffTime": 2,
  "week": 31
}
```

### type=7 闹钟保存

字段：

- `alarmNum,offMode,sensitivity,holidaysStatus,alarmInfo[]`
- `alarmInfo[]` 子项：`time,mode,ring,delay,week`

说明：

- `alarmNum` 最大 10
- `time` 单位秒
- `ring` 为0基编号（前端会做减1）

请求示例：

```json
{
  "type": 7,
  "alarmNum": 2,
  "offMode": 0,
  "sensitivity": 1,
  "holidaysStatus": 1,
  "alarmInfo": [
    {"time": 27000, "mode": 2, "ring": 4, "delay": 2, "week": 31},
    {"time": 75600, "mode": 1, "ring": 3, "delay": 1, "week": 0}
  ]
}
```

### type=8 系统保存

字段：`ctpe,ledState,language,offset,resetSW,resetTime,timerBeep,timerDelay,link,locMode,locCountry,locCode`

说明：

- 保存后设备会触发天气/定位刷新

请求示例：

```json
{
  "type": 8,
  "ctpe": 2,
  "ledState": true,
  "language": 0,
  "offset": 0,
  "resetSW": false,
  "resetTime": 240,
  "timerBeep": 3,
  "timerDelay": 1,
  "link": 1,
  "locMode": 1,
  "locCountry": 0,
  "locCode": "101010100"
}
```

### type=9 报时保存

字段：`ring_hour,ring_30min,ring_15min,TK_time,week`

请求示例：

```json
{
  "type": 9,
  "ring_hour": 1,
  "ring_30min": 0,
  "ring_15min": 0,
  "TK_time": 16777215,
  "week": 127
}
```

### type=11 节假日策略保存

字段：`dataSources,regions,week`

说明：

- `dataSources=0` 时设备会自动拉取节假日
- `dataSources=1` 时通常配合 `type=14/15` 手动列表

请求示例：

```json
{
  "type": 11,
  "dataSources": 1,
  "regions": 0,
  "week": 31
}
```

### type=12 感光阈值保存

字段：`minLT,maxLT,minLT_H,maxLT_H`

请求示例：

```json
{
  "type": 12,
  "minLT": 150,
  "maxLT": 500,
  "minLT_H": 501,
  "maxLT_H": 1023
}
```

### type=13 亮度参数保存

字段：`lightMode,lightMin,lightMax,lightTime1,lightTime2`

请求示例：

```json
{
  "type": 13,
  "lightMode": 2,
  "lightMin": 2,
  "lightMax": 8,
  "lightTime1": 420,
  "lightTime2": 1320
}
```

### type=14 法定休息日列表保存

字段：`offDayLen,offDayList[]`

约束：`offDayLen <= 50`

请求示例：

```json
{
  "type": 14,
  "offDayLen": 4,
  "offDayList": [1,2,3,35]
}
```

### type=15 法定工作日列表保存

字段：`workDayLen,workDayList[]`

约束：`workDayLen <= 30`

请求示例：

```json
{
  "type": 15,
  "workDayLen": 2,
  "workDayList": [40,41]
}
```

### type=16 登录配置保存

字段：

- `loginSW`（bool）
- `newPwd`（64位hex，开启登录时必填）

请求示例：

```json
{
  "type": 16,
  "loginSW": true,
  "newPwd": "ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f"
}
```

### type=17 温度保存

字段：`sensorType,powerDelay,brightnessDelay,offset[]`

约束：`offset` 最多11项

请求示例：

```json
{
  "type": 17,
  "sensorType": 1,
  "powerDelay": 2,
  "brightnessDelay": 1,
  "offset": [0,0,1,1,0,0,0,0,0,0,0]
}
```

### 6.2 动作触发类 type

- `10`：触发OTA（通常随后重启）
- `21`：设备重启
- `22`：启动Wi-Fi扫描
- `71`：试听闹钟铃音（字段：`ring`，0基）
- `72`：试听计时器铃音（字段：`ring`，0基）
- `73`：试听报时铃音（字段：`ring`，0基）
- `81`：网页授时（字段：`time`，Unix秒字符串）
- `83`：恢复出厂（字段：`reset`；1=含Wi-Fi，其他=不含Wi-Fi）
- `85`：首次设置语言/时区（字段：`ins,language,zone`）
- `86`：登录认证（字段：`pass`）

`type=10` 请求示例：

```json
{
  "type": 10
}
```

`type=21` 请求示例：

```json
{
  "type": 21
}
```

`type=22` 请求示例：

```json
{
  "type": 22
}
```

`type=71` 请求示例：

```json
{
  "type": 71,
  "ring": 4
}
```

`type=72` 请求示例：

```json
{
  "type": 72,
  "ring": 3
}
```

`type=73` 请求示例：

```json
{
  "type": 73,
  "ring": 1
}
```

`type=81` 请求示例：

```json
{
  "type": 81,
  "time": "1760000000"
}
```

`type=83` 请求示例：

```json
{
  "type": 83,
  "reset": 1
}
```

`type=85` 请求示例：

```json
{
  "type": 85,
  "ins": true,
  "language": 0,
  "zone": 480
}
```

`type=86` 请求示例：

```json
{
  "type": 86,
  "pass": "ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f"
}
```

---

## 7. 换算说明

### 7.1 时区字段 `zone` / `timezone`

这类字段的单位都是“分钟”，表示相对 UTC 的偏移量。

| 显示时区 | 传值示例 | 说明 |
|---|---:|---|
| UTC-12:00 | `-720` | 西12区 |
| UTC-05:00 | `-300` | 美东标准时常见偏移 |
| UTC+00:00 | `0` | 零时区 |
| UTC+05:30 | `330` | 印度常见时区 |
| UTC+08:00 | `480` | 北京时间 |
| UTC+09:00 | `540` | 日本/韩国常见时区 |

换算公式：`时区值 = 小时 * 60 + 分钟`。

例如：

- `UTC+8` -> `8 * 60 = 480`
- `UTC+5:30` -> `5 * 60 + 30 = 330`
- `UTC-3:30` -> `-(3 * 60 + 30) = -210`

### 7.2 时间字段 `time`

协议里的时间字段并不都是同一种单位，主要分成下面 3 类：

| 类型 | 典型字段 | 单位 | 示例 | 说明 |
|---|---|---|---|---|
| 当天分钟数 | `pwOn` `pwOff` `resetTime` `lightTime1` `lightTime2` `dstStartTime` `dstEndTime` | 分钟 | `420` | 表示当天 `07:00` |
| 当天秒数 | `alarmInfo[].time` | 秒 | `27000` | 表示当天 `07:30:00` |
| Unix 时间戳 | `countTime` `updateTime` `factoryTime` `type=81.time` | 秒 | `1760000000` | 从 `1970-01-01 00:00:00 UTC` 起的秒数 |

常见换算：

| 人类可读时间 | 分钟值 | 秒值 |
|---|---:|---:|
| `00:00` | `0` | `0` |
| `07:00` | `420` | `25200` |
| `07:30` | `450` | `27000` |
| `08:00` | `480` | `28800` |
| `22:00` | `1320` | `79200` |
| `23:00` | `1380` | `82800` |
| `23:59:59` | `1439` | `86399` |

换算公式：

- `分钟值 = 小时 * 60 + 分钟`
- `秒值 = 小时 * 3600 + 分钟 * 60 + 秒`

### 7.3 星期字段 `week`

`week` 使用 7 位位图编码，真实规则以网页前端为准：

- `bit0 = 周一 = 1`
- `bit1 = 周二 = 2`
- `bit2 = 周三 = 4`
- `bit3 = 周四 = 8`
- `bit4 = 周五 = 16`
- `bit5 = 周六 = 32`
- `bit6 = 周日 = 64`

也就是说：多个星期同时生效时，直接把对应值相加即可。

例如：

- 周一到周五：`1 + 2 + 4 + 8 + 16 = 31`
- 周末：`32 + 64 = 96`
- 全周：`1 + 2 + 4 + 8 + 16 + 32 + 64 = 127`

该规则适用于：

- `type=6` 的 `week`
- `type=7` 的 `alarmInfo[].week`
- `type=9` 的 `week`
- `type=11` 的 `week`

---

## 8. 位图字段常见取值对照表

### 8.1 `week` 常见取值

| 数值 | 二进制 | 含义 |
|---:|---|---|
| `0` | `0000000` | 全不选 |
| `1` | `0000001` | 仅周一 |
| `2` | `0000010` | 仅周二 |
| `4` | `0000100` | 仅周三 |
| `8` | `0001000` | 仅周四 |
| `16` | `0010000` | 仅周五 |
| `32` | `0100000` | 仅周六 |
| `64` | `1000000` | 仅周日 |
| `31` | `0011111` | 周一到周五 |
| `96` | `1100000` | 周六、周日 |
| `127` | `1111111` | 全周 |

### 8.2 `TK_time` 常见取值

`TK_time` 是 24 位位图，按小时控制报时有效时段：

- `bit0 = 00点`
- `bit1 = 01点`
- `bit2 = 02点`
- ...
- `bit23 = 23点`

也就是说，如果你希望某几个小时生效，就把这些小时对应的值相加。

| 数值 | 含义 |
|---:|---|
| `1` | 仅 `00:00` 这一小时有效 |
| `2` | 仅 `01:00` 这一小时有效 |
| `4` | 仅 `02:00` 这一小时有效 |
| `256` | 仅 `08:00` 这一小时有效 |
| `32768` | 仅 `15:00` 这一小时有效 |
| `8388608` | 仅 `23:00` 这一小时有效 |
| `255` | `00:00` 到 `07:59` 有效 |
| `65280` | `08:00` 到 `15:59` 有效 |
| `16711680` | `16:00` 到 `23:59` 有效 |
| `16777215` | 全部 24 小时有效 |

补充说明：

- `TK_time` 只决定“哪些小时允许报时”
- 具体是整点、半点还是 15 分钟报时，还要结合 `ring_hour`、`ring_30min`、`ring_15min` 一起看

---

## 9. 页面ID（/html?id=）

- `1` 菜单
- `2` 网络
- `3` 时区
- `4` 显示1
- `5` 显示2
- `6` 休眠
- `7` 闹钟
- `8` 系统
- `9` 报时
- `10` 设备信息
- `11` 假期设置
- `12` 感光设置
- `13` 亮度设置
- `14` 休息日列表
- `15` 工作日列表
- `16` 登录密码设置
- `17` 温度设置
- `20` 首次设置
- `21` 登录页

---

## 10. 实用示例

### 8.1 查询设备型号与版本

请求：`GET /get?type=10`

返回示例：

```json
{
  "id": "61b4c0756c5a49a296004c23",
  "model": "CWT9S19",
  "name": "WHEN",
  "ver_now": "2.4.7",
  "ver_new": "None",
  "ver_note": "",
  "auth": true,
  "rtc": 81,
  "factoryTime": 1756961043
}
```

### 8.2 登录

```json
{
  "type": 86,
  "pass": "ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f"
}
```

### 8.3 网络保存并立即重连

```json
{
  "type": 23,
  "ssid": "MyWiFi",
  "password": "12345678",
  "bindBssid": false,
  "isDHCP": true,
  "ip": [192,168,1,100],
  "mask": [255,255,255,0],
  "gateway": [192,168,1,1],
  "DNS": [223,5,5,5],
  "subDNS": [119,29,29,29],
  "MAC": [140,37,5,154,63,19]
}
```

### 8.4 网页授时

```json
{
  "type": 81,
  "time": "1760000000"
}
```

---

## 11. 注意事项

1. 建议仅在局域网可信环境使用本接口。
2. `/Language` 路径区分大小写。
3. 字段命名存在读写不对称：
   - 读取常见 `timezone`
   - 写入使用 `zone`
4. 列表长度建议提前校验：
   - `offDayLen <= 50`
   - `workDayLen <= 30`
5. 密码相关字段必须是 64 位十六进制 SHA256 字符串。
6. `week` 不是自然日序号，而是位图：`1=周一`，`31=周一到周五`，`96=周末`，`127=全周`。
7. `TK_time` 不是普通小时数字，而是 24 位位图；例如 `16777215` 表示全天都允许报时。

