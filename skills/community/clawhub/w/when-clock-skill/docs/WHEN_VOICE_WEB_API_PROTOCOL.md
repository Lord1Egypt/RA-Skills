# WHEN Voice 时钟 HTTP 接口说明

适用对象：通过 HTTP 对 WHEN Voice 时钟进行参数读取、设置、控制的用户与二次开发对接方。

产品页面：https://iottimer.com/products/when_voice/

---

## 1. 产品与接口定位

- 产品名称：WHEN Voice
- 常见能力：Wi-Fi 校时、显示参数配置、亮度管理、休眠管理、闹钟、语音报时、节假日策略、设备信息查询
- 通信方式：局域网 HTTP（设备内置网页也使用同一协议）

说明：
- 文档中的字段命名、`type` 编号、状态码均可直接用于第三方系统接入。
- 建议先调用 `GET /get?type=10` 获取 `model`、`ver_now` 作为设备识别与版本记录。

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
- `POST /set`：请求体为 JSON，且必须包含 `type`

`POST /set` 通用响应：

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

后续请求建议携带该 Cookie。

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

## 4. 典型调用流程（推荐）

1. 初始化：`GET /get?type=85`
   - 若 `Login=true`：先登录（`POST /set type=86`）
   - 若 `firstSet=true`：先做语言/时区初始设置（`POST /set type=85`）
2. 网络配置：
   - 读取当前网络参数：`GET /get?type=2`
   - 扫描热点：`POST /set {"type":22}` 后轮询 `GET /get?type=22`
   - 联网尝试：`POST /set {"type":23,...}` 后轮询 `GET /get?type=23`
3. 功能页配置：统一“先 `GET` 拉取，再 `POST` 保存”
4. 动作控制：重启/授时/恢复出厂等使用动作型 `type`

---

## 5. GET 查询接口详细说明（表格版）

入口：`GET /get?type=<int>`

### 5.1 通用网络状态字段（type=2/22/23 常见）

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

### 5.4 type=23 网络连接状态（轮询）

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `netSET` | int | `0/1` | `1` | 见 5.1 |
| `netCON` | int | `0~3` | `1` | 路由连接进行中时通常为 `1` |
| `netNTP` | int | `0~3` | `0` | 未开始同步时为 `0` |
| `netSer` | int | `0~3` | `0` | 未连服务器时为 `0` |
| `netWea` | int | 通常 `0` | `0` | 天气状态 |

### 5.5 type=3 时区与 NTP

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `ntp` | string[] | 最多 2 项 | `["ntp1.aliyun.com","pool.ntp.org"]` | NTP 服务器列表 |
| `adjustNTP` | int | 毫秒（可正负） | `12` | NTP 校时补偿 |
| `filter` | bool | `true/false` | `true` | 是否启用延迟滤波 |
| `limit` | int | 毫秒，`0`=关闭 | `150` | 延迟阈值 |
| `tolerant` | bool | `true/false` | `false` | 是否宽松校验 |
| `timezone` | int | 分钟偏移 | `480` | 主时区 |
| `dstSW` | bool | `true/false` | `false` | 主时区夏令时开关 |
| `dstOffset` | int | 分钟 | `60` | 主时区夏令时偏移 |
| `dstStartMonth` | int | `0~11` | `2` | 夏令时开始月（0基） |
| `dstStartWeek` | int | `0~4` | `1` | 夏令时开始第几周（0基） |
| `dstStartDay` | int | `0~6` | `0` | 夏令时开始星期 |
| `dstStartTime` | int | 分钟（0~1439） | `120` | 夏令时开始时刻 |
| `dstEndMonth` | int | `0~11` | `10` | 夏令时结束月（0基） |
| `dstEndWeek` | int | `0~4` | `0` | 夏令时结束第几周（0基） |
| `dstEndDay` | int | `0~6` | `0` | 夏令时结束星期 |
| `dstEndTime` | int | 分钟（0~1439） | `180` | 夏令时结束时刻 |
| `timezone2` | int | 分钟偏移 | `540` | 副时区 |
| `dst2SW` | bool | `true/false` | `false` | 副时区夏令时开关 |
| `dst2Offset` | int | 分钟 | `60` | 副时区夏令时偏移 |
| `dst2StartMonth` ~ `dst2EndTime` | int | 同主时区规则 | - | 副时区夏令时参数 |

### 5.6 type=4 / type=5 显示参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `page1_1`~`page3_3` | int | 页面内容枚举 | `1` | 3页×3区内容配置 |
| `page1_3_1`~`page3_3_3` | int | 子项内容枚举 | `2` | 第3区细分内容 |
| `page1Time/page2Time/page3Time` | int | 秒，常见 `0~59` | `5` | 各页停留时长 |
| `page2SW/page3SW` | bool | `true/false` | `true` | 第2/3页开关 |
| `timeZero` | bool | `true/false` | `true` | 时间前导零 |
| `dateZero` | bool | `true/false` | `false` | 日期前导零 |
| `is12H` | bool | `true/false` | `false` | 12小时制显示 |
| `secFlash` | bool | `true/false` | `true` | 秒闪烁 |
| `dateFormat` | int | 日期格式枚举 | `0` | 日期显示格式 |
| `sundayType` | int | 星期显示枚举 | `1` | 星期风格 |
| `countMode` | int | 计时模式枚举 | `0` | 计时策略 |
| `countTime` | int | Unix 秒 | `1735707600` | 计时目标时间 |
| `offset` | int | 分钟偏移 | `0` | 页面显示时间偏移 |
| `isTempF` | bool | `true/false` | `false` | 温度单位 |

### 5.7 type=6 休眠参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `pwSwitch` | bool | `true/false` | `true` | 休眠总开关 |
| `pwMode` | int | `0定时/1感光/2定时+感光` | `2` | 休眠模式 |
| `pwOn` | int | 分钟（0~1439） | `420` | 每日开机时间（07:00） |
| `pwOff` | int | 分钟（0~1439） | `1380` | 每日关机时间（23:00） |
| `pwSen` | int | 感光灵敏度枚举 | `1` | 感光触发灵敏度 |
| `pwOffTime` | int | 延迟档位 | `2` | 关机延迟 |
| `week` | int | 星期位图 | `31` | 生效星期 |

### 5.8 type=7 闹钟参数（Voice增强）

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `offMode` | int | `0按键/1感光/2按键+感光/3自动` | `0` | 闹钟关闭方式 |
| `sensitivity` | int | `0高/1中/2低` | `1` | 感光关闭灵敏度 |
| `holidaysStatus` | int | `0未获取/1已获取/2手动` | `1` | 节假日数据状态 |
| `updateTime` | int | Unix 秒 | `1735603200` | 节假日更新时间 |
| `ringNum` | int | `0~255` | `4` | 自定义闹钟音频数量 |
| `alarmNum` | int | `0~10` | `3` | 闹钟数量 |
| `alarmInfo[].mode` | int | `0关/1单次/2每周/3工作日/4休息日` | `2` | 单个闹钟模式 |
| `alarmInfo[].week` | int | 星期位图 | `31` | 每周模式生效日 |
| `alarmInfo[].ring` | int | 铃音编号（0基） | `4` | 闹钟铃音 |
| `alarmInfo[].time` | int | 秒（0~86399） | `27000` | 触发时刻（07:30） |
| `alarmInfo[].delay` | int | 延迟档位（0基） | `2` | 响铃时长档位 |
| `alarmInfo[].vol` | int | 音量档位（0基） | `14` | 闹钟音量 |

返回示例：

```json
{
  "offMode": 0,
  "sensitivity": 1,
  "holidaysStatus": 1,
  "updateTime": 1735603200,
  "ringNum": 4,
  "alarmNum": 2,
  "alarmInfo": [
    {"mode": 2, "week": 31, "ring": 4, "time": 27000, "delay": 2, "vol": 14},
    {"mode": 1, "week": 0, "ring": 3, "time": 75600, "delay": 1, "vol": 10}
  ]
}
```

### 5.9 type=8 系统参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `language` | int | `0中文/1繁中/2英文/3日文` | `0` | 界面语言 |
| `offset` | int | RTC补偿（整数） | `0` | 硬件时钟校准值 |
| `ctpe` | int | 自动校时周期档位 | `2` | 自动授时间隔 |
| `ledState` | bool | `true/false` | `true` | 指示灯开关 |
| `link` | int | 连接策略枚举 | `1` | 断网重连策略 |
| `resetSW` | bool | `true/false` | `false` | 定时重启开关 |
| `resetTime` | int | 分钟（0~1439） | `240` | 定时重启时刻 |
| `timerBeep` | int | 铃音编号（0基） | `3` | 计时器铃音 |
| `timerDelay` | int | 延迟档位（0基） | `1` | 计时器时长档 |
| `timerVol` | int | 音量档位（0基） | `14` | 计时器音量 |
| `ringNum` | int | 自定义音频数量 | `4` | 计时器可选自定义音数量 |
| `locMode` | int | `1自动(IP)/2自定义` | `1` | 定位模式 |
| `locCountry` | int | 地区编号 | `0` | 国家/地区 |
| `locCode` | int | 地区编码 | `101010100` | 城市编码 |
| `locName` | string | 文本 | `"北京"` | 城市名称 |
| `locTime1` | string | 文本 | `"05-13 17:52"` | 定位/天气时间字段1 |
| `locTime2` | string | 文本 | `"05-13 18:06"` | 定位/天气时间字段2 |

### 5.10 type=9 报时参数（Voice增强）

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `sw_hour` | int | `0~3` | `1` | 整点报时开关/重复次数 |
| `sw_30min` | int | `0~3` | `1` | 半点报时开关/重复次数 |
| `sw_15min` | int | `0~3` | `0` | 刻钟报时开关/重复次数 |
| `ring_hour` | int | 铃音编号（0基） | `1` | 整点铃音 |
| `ring_30min` | int | 铃音编号（0基） | `4` | 半点铃音 |
| `ring_15min` | int | 铃音编号（0基） | `0` | 刻钟铃音 |
| `volume` | int | 音量档位（0基） | `19` | 报时音量 |
| `announcer` | int | 播报音色编号（0基） | `1` | 音色选择 |
| `is12H` | bool | `true/false` | `true` | 播报制式 |
| `TK_time` | int | 24小时位图 | `4194048` | 报时生效时段 |
| `week` | int | 星期位图 | `31` | 报时生效星期 |
| `ringNum` | int | 自定义报时音数量 | `4` | 报时自定义音数量 |

### 5.11 type=10 设备信息

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `id` | string | 设备唯一ID | `"61b4c0756c5a49a296004c23"` | 设备身份标识 |
| `model` | string | 型号字符串 | `"CWT9S19"` | 设备型号 |
| `name` | string | 产品名称 | `"WHEN Voice"` | 产品名 |
| `ver_now` | string | 版本号文本 | `"2.4.7"` | 当前固件版本 |
| `ver_new` | string | 版本号或 `None` | `"None"` | 可升级版本 |
| `ver_note` | string | 文本（可空） | `""` | 升级说明 |
| `auth` | bool | `true/false` | `true` | 设备认证状态 |
| `rtc` | int | RTC 型号编号 | `81` | RTC 芯片类型 |
| `TF` | bool | `true/false` | `true` | TF卡状态 |
| `factoryTime` | int | Unix 秒 | `1756961043` | 出厂时间 |

### 5.12 type=11 / 14 / 15 节假日参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `holidaysStatus` | int | `0未获取/1已获取/2手动` | `2` | 节假日数据状态 |
| `updateTime` | int | Unix 秒 | `1735603200` | 节假日更新时间 |
| `dataSources` | int | `0自动/1手动` | `1` | 数据来源模式 |
| `regions` | int | `0内地/1日本` | `0` | 地区规则 |
| `week` | int | 星期位图 | `31` | 工作周模板 |
| `offDayLen` | int | `0~50` | `11` | 休息日数量 |
| `offDayList` | int[] | `MM<<8 | DD` 列表 | `[259,260]` | 休息日列表 |
| `workDayLen` | int | `0~30` | `2` | 调休工作日数量 |
| `workDayList` | int[] | `MM<<8 | DD` 列表 | `[1026,1048]` | 工作日列表 |

### 5.13 type=12 感光参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `nowLT` | int | ADC 原始值 | `812` | 当前环境光强 |
| `nowLeve` | int | 亮度档位（1基） | `4` | 当前亮度档 |
| `minLT` | int | 阈值整数 | `150` | 低区最小阈值 |
| `maxLT` | int | 阈值整数 | `500` | 低区最大阈值 |
| `minLT_H` | int | 阈值整数 | `501` | 高区最小阈值 |
| `maxLT_H` | int | 阈值整数 | `1023` | 高区最大阈值 |

### 5.14 type=13 亮度参数

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `lightMode` | int | 模式枚举（固定/感光/定时） | `2` | 亮度策略 |
| `lightMin` | int | 亮度档位（0基） | `2` | 最小亮度 |
| `lightMax` | int | 亮度档位（0基） | `8` | 最大亮度 |
| `lightTime1` | int | 分钟（0~1439） | `420` | 时段1开始（07:00） |
| `lightTime2` | int | 分钟（0~1439） | `1320` | 时段2开始（22:00） |

### 5.15 type=16 登录设置

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `typeID` | int | 固定 `16` | `16` | 数据类型标识 |
| `loginSW` | bool | `true/false` | `true` | 是否开启登录校验 |

### 5.16 type=85 首次设置信息

| 字段 | 类型 | 范围/取值 | 示例 | 说明 |
|---|---|---|---|---|
| `typeID` | int | 固定 `85` | `85` | 数据类型标识 |
| `Login` | bool | `true/false` | `true` | 当前是否要求登录 |
| `firstSet` | bool | `true/false` | `false` | 是否首次配置流程 |
| `language` | int | `0中文/1繁中/2英文/3日文` | `0` | 当前语言 |
| `timezone` | int | 分钟偏移 | `480` | 当前主时区 |

---

## 6. POST 设置接口详细说明

入口：`POST /set`  
请求头建议：`Content-Type: application/json`

### 6.1 参数保存类 type

### type=2 网络参数保存

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `2` |
| `ssid` | string | 是 | Wi-Fi 名称 |
| `password` | string | 是 | Wi-Fi 密码 |
| `bindBssid` | bool | 否 | 是否绑定热点BSSID |
| `bssid` | int[6] | 否 | 目标热点 MAC |
| `isDHCP` | bool | 是 | 是否 DHCP |
| `ip/mask/gateway/DNS/subDNS` | int[] | 条件必填 | 非 DHCP 时填写 |
| `MAC` | int[6] | 是 | 设备 MAC |

示例：

```json
{
  "type": 2,
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

### type=23 网络保存并立即重连

字段与 `type=2` 相同。  
效果：保存后立即触发 Wi-Fi 重连与时间同步。

### type=3 时区/NTP 保存

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `3` |
| `zone` / `zone2` | int | 是 | 主/副时区，单位分钟 |
| `dstSW`~`dstEndTime` | int/bool | 是 | 主时区 DST 参数（`Month/Week/Day` 为0基） |
| `dst2SW`~`dst2EndTime` | int/bool | 是 | 副时区 DST 参数（`Month/Week/Day` 为0基） |
| `ntp` | string[] | 是 | NTP 列表（最多2个） |
| `adjustNTP` | int | 是 | NTP 补偿 |
| `filter` | bool | 是 | 滤波开关 |
| `limit` | int | 是 | 延迟阈值 |
| `tolerant` | bool | 是 | 宽松校验开关 |

### type=4 / type=5 显示保存

字段：同 `GET type=4/5`。  
说明：一般 `type=4` 用于主显示页，`type=5` 用于扩展显示页。

### type=6 休眠保存

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `6` |
| `pwSwitch` | bool | 是 | 总开关 |
| `pwOn/pwOff` | int | 是 | 分钟 |
| `pwMode` | int | 是 | 模式 |
| `pwSen` | int | 是 | 灵敏度 |
| `pwOffTime` | int | 是 | 延时档位 |
| `week` | int | 是 | 星期位图 |

### type=7 闹钟保存（Voice）

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `7` |
| `alarmNum` | int | 是 | 闹钟数量（最大10） |
| `offMode` | int | 是 | 关闭方式 |
| `sensitivity` | int | 是 | 感光灵敏度 |
| `holidaysStatus` | int | 是 | 节假日模式状态 |
| `alarmInfo[]` | object[] | 是 | 闹钟数组 |
| `alarmInfo[].time` | int | 是 | 秒 |
| `alarmInfo[].mode` | int | 是 | `0~4` |
| `alarmInfo[].ring` | int | 是 | 铃音编号（0基） |
| `alarmInfo[].delay` | int | 是 | 延迟档位（0基） |
| `alarmInfo[].week` | int | 是 | 星期位图 |
| `alarmInfo[].vol` | int | 是 | 音量档位（0基） |

示例：

```json
{
  "type": 7,
  "offMode": 2,
  "sensitivity": 1,
  "holidaysStatus": 1,
  "alarmNum": 1,
  "alarmInfo": [
    {
      "time": 25800,
      "mode": 2,
      "ring": 3,
      "delay": 2,
      "week": 31,
      "vol": 14
    }
  ]
}
```

### type=8 系统保存

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `8` |
| `ctpe` | int | 是 | 自动校时周期 |
| `ledState` | bool | 是 | 指示灯开关 |
| `language` | int | 是 | 语言 |
| `offset` | int | 是 | RTC补偿 |
| `resetSW/resetTime` | bool/int | 是 | 定时重启 |
| `timerBeep/timerDelay/timerVol` | int | 是 | 计时器设置（0基） |
| `link` | int | 是 | 连接策略 |
| `locMode/locCountry/locCode` | int | 是 | 定位参数 |

### type=9 报时保存（Voice）

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `9` |
| `sw_hour/sw_30min/sw_15min` | int | 是 | 开关/重复次数（0~3） |
| `ring_hour/ring_30min/ring_15min` | int | 是 | 铃音编号（0基） |
| `volume` | int | 是 | 音量档位（0基） |
| `announcer` | int | 是 | 音色编号（0基） |
| `is12H` | bool | 是 | 播报制式 |
| `TK_time` | int | 是 | 24小时位图 |
| `week` | int | 是 | 星期位图 |

示例：

```json
{
  "type": 9,
  "sw_hour": 1,
  "sw_30min": 1,
  "sw_15min": 0,
  "ring_hour": 1,
  "ring_30min": 4,
  "ring_15min": 0,
  "volume": 19,
  "announcer": 1,
  "is12H": true,
  "TK_time": 4194048,
  "week": 31
}
```

### type=11 节假日策略保存

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `11` |
| `dataSources` | int | 是 | `0自动/1手动` |
| `regions` | int | 是 | `0内地/1日本` |
| `week` | int | 是 | 星期位图 |

### type=12 感光阈值保存

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `12` |
| `minLT/maxLT` | int | 是 | 低区阈值 |
| `minLT_H/maxLT_H` | int | 是 | 高区阈值 |

### type=13 亮度参数保存

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `13` |
| `lightMode` | int | 是 | 模式 |
| `lightMin/lightMax` | int | 是 | 亮度档位（0基） |
| `lightTime1/lightTime2` | int | 是 | 分钟 |

### type=14 休息日列表保存

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `14` |
| `offDayLen` | int | 是 | 数量（最大50） |
| `offDayList` | int[] | 是 | 每项格式 `MM<<8 | DD` |

示例：

```json
{
  "type": 14,
  "offDayLen": 3,
  "offDayList": [259, 260, 261]
}
```

### type=15 工作日列表保存

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `15` |
| `workDayLen` | int | 是 | 数量（最大30） |
| `workDayList` | int[] | 是 | 每项格式 `MM<<8 | DD` |

### type=16 登录开关/密码保存

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `16` |
| `loginSW` | bool | 是 | 是否启用密码登录 |
| `newPwd` | string | 条件必填 | `loginSW=true` 时填写 SHA256 64位hex |

### type=85 首次设置（语言/时区）

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `85` |
| `ins` | int | 是 | `0`语言设置，`1`时区设置 |
| `language` | int | 是 | 语言编号 |
| `zone` | int | 条件必填 | `ins=1` 时填写 |

### type=86 登录验证

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `type` | int | 是 | 固定 `86` |
| `pass` | string | 是 | SHA256 64位hex |

### 6.2 动作控制类 type

| type | 用途 | 请求示例 |
|---|---|---|
| `10` | 触发设备升级 | `{"type":10}` |
| `21` | 设备重启 | `{"type":21}` |
| `22` | 刷新 Wi-Fi 列表 | `{"type":22}` |
| `71` | 试听闹钟音 | `{"type":71,"mode":0,"ring":1,"vol":9,"sw":1}` |
| `72` | 试听计时器音 | `{"type":72,"mode":0,"ring":2,"vol":16,"sw":1}` |
| `73` | 试听报时音 | `{"type":73,"mode":1,"ring":1,"vol":19,"sw":1}` |
| `74` | 试听播报音色 | `{"type":74,"mode":0,"ring":1,"vol":19,"sw":1,"is12H":true}` |
| `81` | 网页手动授时 | `{"type":81,"time":"1735707600"}` |
| `83` | 恢复出厂 | `{"type":83,"reset":1}` |

`type=83` 的 `reset`：
- `1`：全部恢复
- `0`：保留 Wi-Fi 参数

---

## 7. 页面路由与 ID（`GET /html?id=`）

| id | 页面 |
|---|---|
| `1` | 菜单页 |
| `2` | 网络设置 |
| `3` | 时区设置 |
| `4` | 显示设置（主） |
| `5` | 显示设置（副） |
| `6` | 休眠设置 |
| `7` | 闹钟设置 |
| `8` | 系统设置 |
| `9` | 报时设置 |
| `10` | 设备信息 |
| `11` | 节假日设置 |
| `12` | 感光设置 |
| `13` | 亮度设置 |
| `14` | 休息日列表 |
| `15` | 工作日列表 |
| `16` | 登录密码设置 |
| `20` | 首次设置页 |
| `21` | 登录页 |

---

## 8. 位图与编码说明（对接重点）

### 8.1 星期位图 `week`

接口中星期普遍使用 7 位位图，建议按你自己的业务统一封装“编码/解码函数”后再对接。  
（不同业务页可共用同一位图值，减少转换错误）

### 8.2 报时时段位图 `TK_time`

`TK_time` 表示 24 小时开关（0~23 点）。  
建议在客户端提供“24个复选框 ↔ 整数位图”的双向转换函数。

### 8.3 节假日日期编码

`offDayList/workDayList` 使用 `MM<<8 | DD`：
- 例如 10月2日：`(10<<8)|2 = 2562`

---

## 9. Voice 相比普通版的扩展重点

- 闹钟新增音量字段：`alarmInfo[].vol`
- 闹钟模式更丰富：支持工作日/休息日模式
- 报时能力更丰富：`sw_hour/sw_30min/sw_15min`、`announcer`、`is12H`
- 多种试听动作：`71/72/73/74`
- 自定义音频数量动态返回：`ringNum`

---

## 10. 联调建议

1. 先打通登录链路（`type=16/86`）与 Cookie 保持
2. 再打通网络链路（`type=2/22/23`）
3. 最后联调 Voice 核心：
   - 闹钟：`GET/POST type=7` + `type=71`
   - 报时：`GET/POST type=9` + `type=73/74`
4. 动作型接口（重启/授时/恢复出厂）放在联调末尾验证

---

## 11. 常见错误排查

- 返回 `status=1`：字段缺失、类型错误、枚举值越界（建议先对照本表逐项校验）
- 返回 `status=101`：请求体为空
- 返回 `status=102`：请求 JSON 过长（请精简单次提交字段）
- 登录后仍被要求登录：确认请求是否带上 `Session-Key` Cookie

---

## 12. 字段取值范围（基于 HTML 页面 + `clock.js`）

本章节用于二次开发参数校验。  
说明：页面下拉通常是 **1基**，而接口上报常做 `value-1`，即协议值是 **0基**。

### 12.1 type=2 / type=23 网络参数

| 字段 | 页面输入范围 | 协议范围 | 备注 |
|---|---|---|---|
| `ssid` | 文本，`maxlength=32` | 建议 `1~32` 字符 | 不能为空 |
| `password` | 文本，`maxlength=62` | 建议 `0~62` 字符 | 可空（开放网络） |
| `bindBssid` | `true/false` | `bool` | |
| `isDHCP` | `true/false` | `bool` | |
| `ip/mask/gateway/DNS/subDNS` | IPv4 点分十进制 | 每段 `0~255` | 非 DHCP 时必填（`subDNS` 可空） |
| `MAC` | `XX:XX:XX:XX:XX:XX` | `int[6]` 每段 `0~255` | 首字节最低位必须为 0（单播） |

### 12.2 type=3 时区 / DST / NTP

| 字段 | 页面输入范围 | 协议范围 | 备注 |
|---|---|---|---|
| `zone` / `zone2` | 下拉 37 项 | `{-720,-660,...,840}` | 固定时区集合 |
| `dstSW` / `dst2SW` | 勾选 | `bool` | |
| `dstOffset` / `dst2Offset` | 下拉 0~120（步长10） | `0~120` | 单位：分钟 |
| `dstStartMonth/endMonth` | 页面 `1~12` | 协议 `0~11` | 上报减1 |
| `dstStartWeek/endWeek` | 页面 `1~5` | 协议 `0~4` | 上报减1 |
| `dstStartDay/endDay` | 页面 `1~7` | 协议 `0~6` | 上报减1（周日~周六） |
| `dstStartTime/endTime` | `time` 控件 | `0~1439` | 单位：分钟 |
| `adjustNTP` | 下拉 `-20.0~20.0`，步长0.5 | `-200~200` | 页面显示毫秒，协议为放大10倍整数 |
| `limit` | `0` 或 `10~500`（步长10） | 同页面 | 单位：ms |
| `filter` / `tolerant` | 页面 `1/2`（关/开） | 协议 `0/1` | 上报减1 |
| `ntp[0],ntp[1]` | 文本输入 | 建议每项 `1~49` 字符 | 建议域名，不建议超长 |

### 12.3 type=4 显示主参数

| 字段 | 页面输入范围 | 协议范围 | 备注 |
|---|---|---|---|
| `timeZero/dateZero/is12H/secFlash/isTempF` | `true/false` | `bool` | |
| `dateFormat` | 页面 `1~4` | 协议 `0~3` | 上报减1 |
| `sundayType` | 页面 `1~5` | 协议 `0~4` | 上报减1 |
| `countMode` | 页面 `1~2` | 协议 `0~1` | 上报减1 |
| `countTime` | `datetime-local` | Unix 秒 | 页面限制 `1900-01-01`~`2100-12-31` |
| `offset` | 下拉 `-30~30` | `-30~30` | 单位：分钟 |

### 12.4 type=5 显示子参数（页面内容）

| 字段 | 页面输入范围 | 协议范围 | 备注 |
|---|---|---|---|
| `pageX_1` | 页面 `1~8` | 协议 `0~7` | 上报减1 |
| `pageX_2` | 页面 `1~13` | 协议 `0~12` | 上报减1 |
| `pageX_3` | 页面 `1~17` | 协议 `0~16` | 上报减1 |
| `pageX_3_1..3` | 页面 `1~39` | 协议 `0~38` | 上报减1（自定义字符表） |
| `page1Time/page2Time/page3Time` | 页面显示 `1~60 S` | 协议 `0~59` | 0表示1秒 |
| `page2SW/page3SW` | 勾选 | `bool` | |

### 12.5 type=6 休眠

| 字段 | 页面输入范围 | 协议范围 | 备注 |
|---|---|---|---|
| `pwSwitch` | 勾选 | `bool` | |
| `pwMode` | 页面 `1~3` | 协议 `0~2` | 上报减1 |
| `pwOffTime` | 页面 `1~6` | 协议 `0~5` | 上报减1 |
| `pwSen` | 页面 `1~10` | 协议 `0~9` | 上报减1 |
| `pwOn/pwOff` | `time` 控件 | `0~1439` | 单位：分钟 |
| `week` | 7个复选框 | `0~127` | 星期位图 |

### 12.6 type=7 闹钟（Voice）

| 字段 | 页面输入范围 | 协议范围 | 备注 |
|---|---|---|---|
| `alarmNum` | 动态条目数 | `1~10` | 页面限制最多10个 |
| `offMode` | 页面 `1~3` | 协议 `0~2` | 上报减1 |
| `sensitivity` | 页面 `1~3` | 协议 `0~2` | 上报减1 |
| `alarmInfo[].mode` | 页面 `1~5` | 协议 `0~4` | 上报减1 |
| `alarmInfo[].time` | `time` 控件（含秒） | `0~86399` | 空值按0 |
| `alarmInfo[].ring` | 页面 `1~(50+ringNum)` | 协议 `0~(49+ringNum)` | 上报减1 |
| `alarmInfo[].delay` | 页面 `1~12` | 协议 `0~11` | 上报减1 |
| `alarmInfo[].vol` | 页面 `1~30` | 协议 `0~29` | 上报减1 |
| `alarmInfo[].week` | 7个复选框 | `0~127` | 星期位图 |

### 12.7 type=8 系统

| 字段 | 页面输入范围 | 协议范围 | 备注 |
|---|---|---|---|
| `language` | 页面 `1~4` | 协议 `0~3` | 上报减1 |
| `ctpe` | 页面 `1~6` | 协议 `0~5` | 上报减1 |
| `link` | 页面 `1~2` | 协议 `0~1` | 上报减1 |
| `timerBeep` | 页面 `1~(47+ringNum)` | 协议 `0~(46+ringNum)` | 上报减1 |
| `timerDelay` | 页面 `1~12` | 协议 `0~11` | 上报减1 |
| `timerVol` | 页面 `1~30` | 协议 `0~29` | 上报减1 |
| `locMode` | 页面 `1~2` | 协议 `1~2` | 本字段不减1 |
| `locCountry` | 页面当前仅 `1(CHN)` | 协议当前 `0` | 上报减1 |
| `locCode` | 数字输入 | 正整数（建议城市编码） | |
| `resetSW` | 勾选 | `bool` | |
| `resetTime` | `time` 控件 | `0~1439` | 单位：分钟 |

### 12.8 type=9 报时（Voice）

| 字段 | 页面输入范围 | 协议范围 | 备注 |
|---|---|---|---|
| `sw_hour/sw_30min/sw_15min` | 页面 `1~4` | 协议 `0~3` | 上报减1 |
| `ring_hour` | 页面 `1~(18+ringNum)` | 协议 `0~(17+ringNum)` | 上报减1 |
| `ring_30min/ring_15min` | 页面 `1~(12+ringNum)` | 协议 `0~(11+ringNum)` | 上报减1 |
| `volume` | 页面 `1~30` | 协议 `0~29` | 上报减1 |
| `announcer` | 页面 `1~11` | 协议 `0~10` | 上报减1 |
| `is12H` | `true/false` | `bool` | |
| `TK_time` | 24个复选框 | `0~16777215` | 24位位图 |
| `week` | 7个复选框 | `0~127` | 星期位图 |

### 12.9 type=11 / 14 / 15 节假日

| 字段 | 页面输入范围 | 协议范围 | 备注 |
|---|---|---|---|
| `dataSources` | 页面 `1~2` | 协议 `0~1` | 上报减1 |
| `regions` | 页面 `1~2` | 协议 `0~1` | 上报减1 |
| `week` | 7个复选框 | `0~127` | 星期位图 |
| `offDayLen` | 列表条目数 | `0~50` | 页面限制最大50 |
| `workDayLen` | 列表条目数 | `0~30` | 页面限制最大30 |
| `offDayList/workDayList` | `date` 控件列表 | 每项 `MM<<8|DD` | 例如10月2日=2562 |

### 12.10 type=12 感光阈值

| 字段 | 页面输入范围 | 协议范围 | 备注 |
|---|---|---|---|
| `minLT/maxLT/minLT_H/maxLT_H` | 数字输入 | 建议 `0~1023` | 页面校验：`minLT<maxLT<minLT_H<maxLT_H` |

### 12.11 type=13 亮度

| 字段 | 页面输入范围 | 协议范围 | 备注 |
|---|---|---|---|
| `lightMode` | 页面 `1~3` | 协议 `0~2` | 上报减1 |
| `lightMin/lightMax` | 页面 `1~11` | 协议 `0~10` | 上报减1 |
| `lightTime1/lightTime2` | `time` 控件 | `0~1439` | 单位：分钟 |

### 12.12 type=16 / 86 / 85

| type | 字段 | 页面输入范围 | 协议范围 |
|---|---|---|---|
| `16` | `loginSW` | checkbox | bool |
| `16` | `newPwd` | 密码长度 `8~32` | SHA256 64位hex |
| `86` | `pass` | 密码长度 `8~32`（登录页） | SHA256 64位hex |
| `85` | `language` | 页面 `1~4` | 协议 `0~3` |
| `85` | `ins` | 页面流程按钮 | `0`(语言), `1`(时区) |
| `85` | `zone` | 时区下拉37项 | 与 `type=3 zone` 相同 |

