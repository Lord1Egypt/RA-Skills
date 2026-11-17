---
name: jielong-cli
description: |
  接龙活动管理工具（CLI版）。通过 jielong 命令行工具管理接龙活动。
  支持创建、查看、修改、删除接龙活动、收费报名活动、打卡接龙活动，
  以及查看报名列表、查看活动详情、管理填表项、控制活动状态（开始/结束/重启）、
  删除报名记录、清空报名等操作。
  触发场景：
  - 用户提到"创建接龙/报名/打卡"、"帮我发一个活动"、"查看报名"、"看看我的活动"
  - "帮我报名"、"代报名"、"我要参加"、"报名一下"
  - "删除活动"、"修改活动时间/名称/描述"、"添加填表项"、"删除报名"
  - "清空报名"、"结束活动"、"开始活动"、"重启活动"等
  NOT for: 与接龙活动无关的请求。
compatibility:
  tools: []
metadata:
  openclaw:
    requires:
      bins:
        - jielong
    install:
      - id: install-jielong-cli
        kind: command
        command: npm install -g jielong-cli
---

# 接龙活动管理（jielong CLI）

> **前提条件**：机器上必须已安装 `jielong` 命令行工具。
> 所有操作通过终端执行 `jielong` 命令完成。
> 排查工具问题先执行 `jielong version` 确认版本（v1.1.6+ 创建活动会自动生成带活动名称的海报；若只弹出裸二维码说明版本过旧，升级即可：`npm i -g jielong-cli@latest`）。

---

## ⚠️ 全局最高优先级规则：禁止向用户暴露活动ID

**在与用户的任何对话中，绝对不要出现活动ID、活动Key、订单ID等内部数字标识！包括操作前的叙述文字！**

- ❌ 禁止说："正在删除活动45480"、"找到活动45480"、"活动45480已删除"、"活动ID：45480"
- ✅ 用活动名称代替："「周末聚餐」已删除"、"正在删除「周末聚餐」"
- ✅ `jielong` 命令本身需要活动ID作为参数（如 `jielong delete 45480`），这是 AI 内部使用的，用户看不到命令行参数；但 AI 在文字回复中绝对不要重复这些数字
- ✅ 接口/命令返回的活动ID、活动Key，AI 自己记住用于后续操作即可，**不要展示给用户**
- ✅ 用户如果说"活动45480"，AI 理解后操作即可，回复时用活动名称
- ⚠️ 不要直接把 `jielong` 命令的原始输出（含活动ID/活动Key）粘贴给用户，应先翻译成只含活动名称的表述

---

## ⚠️ 强制前置流程：每次对话必须先执行！

**【禁止跳过以下步骤】在回复用户任何关于接龙活动的请求之前，你必须先用终端执行下面的命令来检查接龙工具的登录状态。这不是在检查 OpenClaw 的登录状态！**

### ⚠️ 关键区分（请仔细阅读）

这里检查的是 **接龙小程序（jielong CLI 命令行工具）的登录状态**，跟 OpenClaw 本身的登录状态完全无关。

- OpenClaw 已经登录了 ≠ jielong 接龙工具已经登录
- 这是两个完全独立的系统，互不相干
- 即使 OpenClaw 显示已登录，也必须单独检查 jielong 是否登录

### 第一步：立即执行（不要问用户，直接执行命令）

先确保工具是最新版本，在终端执行：
```
npm install -g jielong-cli@latest
```
（如果已是最新版会秒过，有新版才会下载更新）

然后验证工具可用：
```
jielong --help
```

- 如果成功返回帮助信息 → 继续第二步
- 如果报错"找不到命令" → 检查 npm 是否已安装，确认 node_modules 全局路径在系统 PATH 中

**版本核对（防止 npm 源缓存导致静默停留在旧版）**：执行 `jielong version` 和 `npm view jielong-cli version`，两者版本号应一致。若 `jielong version` 落后，说明 npm 源未同步，改用指定版本号安装：`npm i -g jielong-cli@<线上版本号>`。

### 第二步：立即执行（不要问用户，直接执行命令）

在终端中执行：
```
jielong whoami
```

根据**命令的实际输出**判断（不是根据 OpenClaw 的登录状态判断）：

- **如果输出包含"昵称"和"手机号"**（成功时完整输出4行）→ ✅ jielong 已登录
  成功时的完整输出示例：
  ```
  昵称: L
  用户ID: 12345
  手机号: 131xxxxxxx
  OpenID: oXXXXXXXXXXXX
  ```
  **请把这4行信息都展示给用户看**，让用户确认是自己的账号，然后继续处理用户的请求。
- **如果输出"未登录"、"请先登录"、"token"、"error"等** → ❌ jielong 未登录，必须先引导用户登录

### 第三步：如果 jielong 未登录，直接执行登录

> **⚠️ 这一步是 AI 必须自己执行的命令，绝对不能让用户自己去终端操作！**
> **`jielong login` 不是交互式命令，它会自动弹出浏览器窗口显示二维码，AI 可以直接执行。**
> **禁止回复"我无法代替你完成"、"请你自己去终端执行"之类的话！**

**发现 token 过期或未登录时，立即执行以下命令（不要问用户，直接执行）：**
```
jielong login
```

这个命令会：
1. 自动在浏览器中弹出二维码图片
2. 等待用户用微信扫码（最长2分钟）
3. 扫码成功后输出 "✅ 登录成功!"

执行后，告诉用户：

> 🔒 接龙工具登录已过期，已为你打开登录二维码，请在浏览器中用微信扫码完成登录。扫码成功后告诉我"登录好了"。

**注意事项：**
- **必须自己执行 `jielong login`，不能让用户自己去终端执行**
- `jielong login` 会自动弹出浏览器显示二维码，AI 直接执行即可
- 等用户回复"登录好了"后，**再次执行 `jielong whoami` 确认**
- 确认看到昵称和手机号后，才能继续处理用户的接龙请求
- 在用户完成 jielong 登录之前，**不要执行任何 create/list/get/update/delete 命令**
- 如果登录超时（2分钟内未扫码），自动重新执行 `jielong login`

---

## ⚠️ 创建活动强制流程：先展示确认，再执行创建

**【禁止跳过以下步骤】创建活动时，不允许直接执行 `jielong create` 命令！必须按以下流程操作：**

### 第一步：整理信息并展示给用户

根据用户的需求，整理出以下信息并**以清晰的格式展示给用户**：

```
📋 即将创建以下活动，请确认信息是否正确：

活动名称：周末聚餐
活动类型：接龙报名(106)
开始时间：2026-06-01 00:00:00
结束时间：2026-06-07 23:59:59
活动描述：请大家准时参加
填表项：姓名、手机号

请回复"确认创建"或"创建"来创建活动，或者告诉我需要修改的地方。
```

### 第二步：等待用户确认

- 用户回复"确认"、"确认创建"、"创建"、"好的"、"没问题"、"OK"等肯定回复 → 执行创建命令
- 用户指出需要修改的地方 → 修改信息后重新展示，再次等待确认
- 用户说"取消"、"不要了" → 停止创建

### 第三步：执行创建命令

用户确认后才执行 `jielong create` 命令。

---

## 一、简单创建活动

适用于：只需要文本、手机号、日期等简单填表项的活动。

### 命令格式

```
jielong create -n "活动名称" -t 类型 -b "开始时间" -e "结束时间" -f "填表项" -c "活动描述"
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `-n` | 活动名称（必填） | `"周末聚餐报名"` |
| `-t` | 活动类型（默认106） | `106`接龙报名 / `101`收费报名 / `109`打卡接龙 |
| `-b` | 开始时间（必填） | `"2026-06-01 00:00:00"` |
| `-e` | 结束时间（必填） | `"2026-06-07 23:59:59"` |
| `-f` | 填表项，逗号分隔 | `"姓名,手机号,备注"` |
| `-C` | 收费项（仅 `101`） | `"成人票:50:100,儿童票:30:50"` |
| `-c` | 活动描述（选填） | `"请大家准时参加"` |

### 活动类型对照

| 用户说法 | 对应类型值 | 说明 |
|----------|-----------|------|
| 接龙、报名、通用接龙、普通报名 | `106` | 默认类型 |
| 收费、收费报名、付费、购票 | `101` | **必须**用 `-C` 设置收费项（名称:单价:库存），如 `-C "成人票:50:100"`；不设置会报错 |
| 打卡、打卡接龙、签到 | `109` | 需要设置打卡配置 |

> **收费项 `-C` 语法**：`名称:单价:库存`，多个用逗号分隔；可选追加 `:最少购买:最多购买`。
> 例如：`-C "成人票:50:100:1:10,儿童票:30:50:1:5"`（成人票50元/库存100/限购1~10，儿童票30元/库存50/限购1~5）。
> 使用 `-C` 时 CLI 会自动设置 `paymentSwitch=1` 并把收费项写入 `fmActivityChargeItemVOS`。

### 填表项对照

**方式1：字段名自动映射**（逗号分隔）：
`-f "姓名,手机号,备注"`

| 用户说 | 字段名 | 类型 |
|--------|--------|------|
| 姓名/名字/名称 | 姓名 | 文本(1) |
| 手机/电话/手机号 | 手机号 | 手机号(11) |
| 日期/时间 | 日期 | 日期(3) |
| 备注/说明/留言 | 备注 | 多行文本(9) |
| 身份证 | 身份证 | 身份证(10) |
| 图片/照片 | 图片 | 图片(5) |
| 数量/人数/份数 | 数量 | 数量(13) |

**方式2：显式指定类型**（支持全部 16 种类型，见下方字段类型对照表）：
`-f "录像:视频,录音:音频,邮箱:邮箱"` —— `字段名:类型名` 或 `字段名:类型数字` 均可。

**必填/选填**：字段后加 `(选填)` / `(可选)` 设为选填，默认必填：
`-f "姓名,手机号(选填),录像:视频(选填)"`

### 时间处理规则

- 用户说"今天"→ 用当前日期，开始时间 `00:00:00`，结束时间 `23:59:59`
- 用户说"明天"→ 当前日期+1天
- 用户说"X天后"/"一周后"→ 当前日期+X天
- 格式固定为 `"yyyy-MM-dd HH:mm:ss"`

### 简单创建示例

**用户说"帮我创建一个周末聚餐接龙，要填姓名和手机号"：**
```
jielong create -n "周末聚餐" -t 106 -b "2026-05-30 00:00:00" -e "2026-06-01 23:59:59" -f "姓名,手机号"
```

**用户说"建一个每天打卡的接龙"：**
```
jielong create -n "每日打卡" -t 109 -b "2026-05-30 00:00:00" -e "2026-06-30 23:59:59" -f "姓名"
```

---

## 二、复杂创建活动（JSON文件模式）

当用户的请求包含以下**任意一个**时，必须使用 JSON 文件模式：
- 单选/多选字段（如"是否携带凭证 是/否"）
- 收费项（如"成人票50元"）
- 打卡详细配置（如"每天9点到18点打卡"）
- 图片、数量等特殊字段类型
- 多个填表分组

### 创建流程

**第一步**：用 `write_file` 工具生成 JSON 配置文件到 `%TEMP%\jielong_activity.json`

**第二步**：执行命令
```
jielong create --file "%TEMP%\jielong_activity.json"
```

### JSON 文件格式

以下是**完整的 JSON 模板**，所有字段都必须包含，不要省略任何字段：

```json
{
  "name": "活动名称",
  "content": "活动描述",
  "activityType": 106,
  "activityMode": 1,
  "activityBigType": 1,
  "beginTime": "2026-06-01 00:00:00",
  "endTime": "2026-06-07 23:59:59",
  "generalCheckTimes": 0,
  "confirmWord": "立即报名",
  "createSource": 4,
  "paymentSwitch": 0,
  "rebateSwitch": 0,
  "verificationSwitch": 1,
  "is_it_over": 1,
  "signStatus": 1,
  "signInfoStatus": 1,
  "copyStatus": 1,
  "shareStatus": 1,
  "multipleActivitiesStatus": 1,
  "removeSignStatus": 4,
  "updateSignInfo": 1,
  "userIfDel": 2,
  "adminIfDel": 2,
  "isTemplate": 2,
  "commentStatus": 2,
  "giftStatus": 2,
  "projectVos": [],
  "goods": [],
  "modular": [],
  "fmActivityChargeItemVOS": [],

  "signList": [
    {
      "signListName": "报名信息",
      "signField": [
        {
          "fieldName": "姓名",
          "type": 1,
          "isRequired": 1,
          "sort": 0
        },
        {
          "fieldName": "是否参加",
          "type": 2,
          "isRequired": 1,
          "sort": 1,
          "content": "[{\"value\":\"是\",\"maxNum\":-1},{\"value\":\"否\",\"maxNum\":-1}]"
        }
      ]
    }
  ],

  "fmClockIn": {
    "clockFrequencyType": 3,
    "clockFrequencyName": "每天",
    "clockFrequency": "0,1,2,3,4,5,6",
    "beginTime": "00:00",
    "endTime": "23:59",
    "checkSwitch": 1,
    "checkTimes": 0,
    "clockMaxSwitch": 2,
    "clockMaxNum": 1,
    "multiPeriodSwitch": 2,
    "clockLocationStatus": 2,
    "clockLocationInfo": "",
    "clockRange": "",
    "clockRemindStatus": 1,
    "remindTime": "10:00",
    "clockSupplyStatus": 1,
    "clockSupplyType": -1,
    "supplyTimes": "-1",
    "customDate": "",
    "dayOfDate": "",
    "timeOfDay": "",
    "clockInTimeSlot": [
      {
        "startTime": "00:00",
        "endTime": "23:59",
        "ifDel": 2,
        "randomDecimal": 1234567890
      }
    ]
  }
}
```

**关键说明：**
- 非收费活动：`paymentSwitch` 设为 `0`，`fmActivityChargeItemVOS` 设为空数组 `[]`
- 收费活动(101)：`paymentSwitch` 设为 `1`，`fmActivityChargeItemVOS` 填充收费项数组
- 非打卡活动：不传 `fmClockIn` 字段
- 打卡活动(109)：必须传完整的 `fmClockIn` 对象，不能省略任何字段
- `projectVos`、`goods`、`modular` 固定为空数组 `[]`
- `activityBigType` 固定为 `1`
- `verificationSwitch` 固定为 `1`

### 字段类型对照表

| type值 | 含义 | 是否需要 content | 说明 |
|--------|------|-----------------|------|
| 1 | 文本 | 否 | 普通输入框 |
| 2 | 单选 | **是** | content 为选项JSON数组 |
| 3 | 日期 | 否 | 日期选择器 |
| 4 | 多选 | **是** | content 为选项JSON数组 |
| 5 | 图片 | 否 | 图片上传 |
| 6 | 视频 | 否 | 视频上传 |
| 7 | 音频 | 否 | 音频上传 |
| 8 | 省市区 | 否 | 省市区选择器 |
| 9 | 多行文本 | 否 | 多行输入框 |
| 10 | 身份证 | 否 | 身份证号输入 |
| 11 | 手机号 | 否 | 手机号输入 |
| 12 | 位置 | 否 | 地理位置 |
| 13 | 数量 | 否 | 数字输入 |
| 15 | 时间 | 否 | 时间选择器 |
| 19 | 邮箱 | 否 | 邮箱输入 |
| 35 | 拍照 | 否 | 拍照上传 |

**必填/选填**：每个 signField 通过 `isRequired` 设置，`1`=必填（默认）、`0`=选填，例如：
```json
{"fieldName": "手机号", "type": 11, "isRequired": 0, "sort": 1}
```

### 单选/多选 content 格式

`content` 是一个 **JSON字符串**（注意：是字符串里嵌套JSON），格式：
```
"[{\"value\":\"选项A\",\"maxNum\":10},{\"value\":\"选项B\",\"maxNum\":-1}]"
```
- `value`：选项名称
- `maxNum`：名额限制，-1 表示不限
- 非单选/多选字段 **不要传 content**

### 收费项格式（仅 activityType=101）

`fmActivityChargeItemVOS` 数组，最多20项。**同时必须设置 `paymentSwitch: 1`**。

```json
{
  "itemName": "成人票",
  "unitPrice": 50.0,
  "stock": 100,
  "remainingStock": 100,
  "minBuyNum": 1,
  "maxBuyNum": 10
}
```

### 打卡配置格式（仅 activityType=109）

fmClockIn 完整字段如下，根据 `clockFrequencyType` 不同，部分字段有特殊要求：

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `clockFrequencyType` | 1=每月 2=每周 3=每天 4=法定工作日 5=法定节假日 6=自定义周几 7=自定义日期 8=一次性 | 3 |
| `clockFrequencyName` | 频率中文名，如 "每天"/"每周"/"自定义周几打卡" | "每天" |
| `clockFrequency` | 周几选择，"0,1,2,3,4,5,6" 表示全周 | "0,1,2,3,4,5,6" |
| `beginTime` | 打卡开始时间 | "00:00" |
| `endTime` | 打卡结束时间 | "23:59" |
| `checkSwitch` | 1=开启审核 2=不审核 | 1（Go默认开启） |
| `checkTimes` | 打卡次数（一次性打卡时由 generalCheckTimes 控制） | 0 |
| `clockLocationStatus` | 1=开启定位 2=不定位 | 2 |
| `clockLocationInfo` | 定位信息 | "" |
| `clockRange` | 定位范围 | "" |
| `clockRemindStatus` | 1=开启提醒 2=不提醒 | 1（Go默认开启） |
| `remindTime` | 提醒时间，如 "10:00"（clockRemindStatus=1时必填） | "10:00"（Go默认） |
| `clockSupplyStatus` | 1=允许补卡 2=不允许（一次性打卡固定=2） | 1（Go默认允许） |
| `clockSupplyType` | 补卡类型 | -1 |
| `supplyTimes` | 补卡次数（字符串） | "-1" |
| `clockMaxSwitch` | 1=限制打卡人数 2=不限制 | 2 |
| `clockMaxNum` | 最大打卡人数 | 1 |
| `multiPeriodSwitch` | 1=多时段 2=单时段 | 2 |
| `customDate` | 自定义日期，逗号分隔（仅 clockFrequencyType=7） | "" |
| `dayOfDate` | 日期值：每月=当月最后一天日期数字，每周=6(周日) | "" |
| `timeOfDay` | 截止时间（仅每月/每周有效），如 "20:00" | "" |
| `clockInTimeSlot` | 打卡时间段数组 | 见下方 |

**clockFrequencyType 对应的特殊字段：**

| clockFrequencyType | 必须额外设置的字段 | 示例 |
|--------------------|-------------------|------|
| 1=每月 | `dayOfDate`=月末日(如"31"), `timeOfDay`="20:00" | 每月最后一天20:00截止 |
| 2=每周 | `dayOfDate`="6"(周日), `timeOfDay`="20:00" | 每周日20:00截止 |
| 3=每天 | 无额外字段 | |
| 6=自定义周几 | `clockFrequency`="0,2,4" | 周一三五打卡 |
| 7=自定义日期 | `customDate`="2026-06-01,2026-06-15" | 指定日期打卡 |
| 8=一次性 | `clockSupplyStatus`=2, `supplyTimes`="-1" | 不可补卡 |

**clockInTimeSlot 格式：**
```json
"clockInTimeSlot": [
  {
    "startTime": "08:00",
    "endTime": "22:00",
    "ifDel": 2,
    "randomDecimal": 1234567890
  }
]
```

**打卡 JSON 完整示例（每天打卡 8:00-22:00，允许补卡）：**
```json
"fmClockIn": {
  "clockFrequencyType": 3,
  "clockFrequencyName": "每天",
  "clockFrequency": "0,1,2,3,4,5,6",
  "beginTime": "08:00",
  "endTime": "22:00",
  "checkSwitch": 1,
  "checkTimes": 0,
  "clockMaxSwitch": 2,
  "clockMaxNum": 1,
  "multiPeriodSwitch": 2,
  "clockLocationStatus": 2,
  "clockLocationInfo": "",
  "clockRange": "",
  "clockRemindStatus": 1,
  "remindTime": "10:00",
  "clockSupplyStatus": 1,
  "clockSupplyType": -1,
  "supplyTimes": "-1",
  "customDate": "",
  "dayOfDate": "",
  "timeOfDay": "",
  "clockInTimeSlot": [
    {
      "startTime": "08:00",
      "endTime": "22:00",
      "ifDel": 2,
      "randomDecimal": 1234567890
    }
  ]
}
```

**打卡 JSON 示例（自定义周几打卡，周一三五）：**
```json
"fmClockIn": {
  "clockFrequencyType": 6,
  "clockFrequencyName": "自定义周几打卡",
  "clockFrequency": "0,2,4",
  "beginTime": "09:00",
  "endTime": "18:00",
  "checkSwitch": 1,
  "checkTimes": 0,
  "clockMaxSwitch": 2,
  "clockMaxNum": 1,
  "multiPeriodSwitch": 2,
  "clockLocationStatus": 2,
  "clockLocationInfo": "",
  "clockRange": "",
  "clockRemindStatus": 1,
  "remindTime": "10:00",
  "clockSupplyStatus": 1,
  "clockSupplyType": -1,
  "supplyTimes": "-1",
  "customDate": "",
  "dayOfDate": "",
  "timeOfDay": "",
  "clockInTimeSlot": [
    {
      "startTime": "09:00",
      "endTime": "18:00",
      "ifDel": 2,
      "randomDecimal": 1234567890
    }
  ]
}
```

**打卡 JSON 示例（每月最后一天打卡）：**
```json
"fmClockIn": {
  "clockFrequencyType": 1,
  "clockFrequencyName": "每月",
  "clockFrequency": "0,1,2,3,4,5,6",
  "beginTime": "00:00",
  "endTime": "23:59",
  "checkSwitch": 1,
  "checkTimes": 0,
  "clockMaxSwitch": 2,
  "clockMaxNum": 1,
  "multiPeriodSwitch": 2,
  "clockLocationStatus": 2,
  "clockLocationInfo": "",
  "clockRange": "",
  "clockRemindStatus": 1,
  "remindTime": "10:00",
  "clockSupplyStatus": 1,
  "clockSupplyType": -1,
  "supplyTimes": "-1",
  "customDate": "",
  "dayOfDate": "31",
  "timeOfDay": "20:00",
  "clockInTimeSlot": [
    {
      "startTime": "00:00",
      "endTime": "23:59",
      "ifDel": 2,
      "randomDecimal": 1234567890
    }
  ]
}
```

**打卡 JSON 示例（自定义日期打卡，指定某几天）：**
```json
"fmClockIn": {
  "clockFrequencyType": 7,
  "clockFrequencyName": "自定义日期",
  "clockFrequency": "0,1,2,3,4,5,6",
  "beginTime": "00:00",
  "endTime": "23:59",
  "checkSwitch": 1,
  "checkTimes": 0,
  "clockMaxSwitch": 2,
  "clockMaxNum": 1,
  "multiPeriodSwitch": 2,
  "clockLocationStatus": 2,
  "clockLocationInfo": "",
  "clockRange": "",
  "clockRemindStatus": 1,
  "remindTime": "10:00",
  "clockSupplyStatus": 1,
  "clockSupplyType": -1,
  "supplyTimes": "-1",
  "customDate": "2026-06-01,2026-06-15,2026-06-30",
  "dayOfDate": "",
  "timeOfDay": "",
  "clockInTimeSlot": [
    {
      "startTime": "00:00",
      "endTime": "23:59",
      "ifDel": 2,
      "randomDecimal": 1234567890
    }
  ]
}
```

**打卡 JSON 示例（一次性打卡）：**
```json
"fmClockIn": {
  "clockFrequencyType": 8,
  "clockFrequencyName": "一次性",
  "clockFrequency": "0,1,2,3,4,5,6",
  "beginTime": "00:00",
  "endTime": "23:59",
  "checkSwitch": 1,
  "checkTimes": 0,
  "clockMaxSwitch": 2,
  "clockMaxNum": 1,
  "multiPeriodSwitch": 2,
  "clockLocationStatus": 2,
  "clockLocationInfo": "",
  "clockRange": "",
  "clockRemindStatus": 1,
  "remindTime": "10:00",
  "clockSupplyStatus": 2,
  "clockSupplyType": -1,
  "supplyTimes": "-1",
  "customDate": "",
  "dayOfDate": "",
  "timeOfDay": "",
  "clockInTimeSlot": [
    {
      "startTime": "00:00",
      "endTime": "23:59",
      "ifDel": 2,
      "randomDecimal": 1234567890
    }
  ]
}
```

### 复杂创建示例

**用户说"创建签售会报名，需要填姓名、是否携带购书凭证（是/否），成人票50元库存100，一周时间"：**

1. 先写入 `%TEMP%\jielong_activity.json`：
```json
{
  "name": "签售会报名",
  "activityType": 101,
  "activityMode": 1,
  "activityBigType": 1,
  "beginTime": "2026-05-30 00:00:00",
  "endTime": "2026-06-06 23:59:59",
  "generalCheckTimes": 0,
  "confirmWord": "立即报名",
  "createSource": 4,
  "paymentSwitch": 1,
  "rebateSwitch": 0,
  "verificationSwitch": 1,
  "is_it_over": 1, "signStatus": 1, "signInfoStatus": 1, "copyStatus": 1,
  "shareStatus": 1, "multipleActivitiesStatus": 1, "removeSignStatus": 4,
  "updateSignInfo": 1, "userIfDel": 2, "adminIfDel": 2, "isTemplate": 2,
  "commentStatus": 2, "giftStatus": 2,
  "projectVos": [],
  "goods": [],
  "modular": [],
  "signList": [
    {
      "signListName": "报名信息",
      "signField": [
        {"fieldName": "姓名", "type": 1, "isRequired": 1, "sort": 0},
        {"fieldName": "是否携带购书凭证", "type": 2, "isRequired": 1, "sort": 1,
         "content": "[{\"value\":\"是\",\"maxNum\":-1},{\"value\":\"否\",\"maxNum\":-1}]"}
      ]
    }
  ],
  "fmActivityChargeItemVOS": [
    {"itemName": "成人票", "unitPrice": 50.0, "stock": 100, "remainingStock": 100, "minBuyNum": 1, "maxBuyNum": 10}
  ]
}
```

2. 然后执行：
```
jielong create --file "%TEMP%\jielong_activity.json"
```

---

## 三、查看活动详情

```
jielong get 活动ID
```

---

## 四、查看活动列表

```
jielong list
jielong list -t 2          # 我参加的
jielong list --status 1    # 进行中
jielong list -p 2 -s 20    # 第2页，每页20条
```

| 参数 | 说明 |
|------|------|
| `-t 1` | 我创建的（默认） |
| `-t 2` | 我参加的 |
| `--status 1` | 进行中 |
| `--status 2` | 已结束 |
| `--status 3` | 未开始 |

---

## 五、查看报名列表

```
jielong signups 活动ID
jielong signups 活动ID -p 2 -s 20
```

---

## 六、修改活动

> **⚠️ 关键流程：确定要操作哪个活动**
>
> 用户说"修改活动"、"改一下时间"、"加个填表项"时，**必须先确定要修改哪个活动**。按以下顺序判断：
>
> 1. **用户直接说了活动ID**（如"修改活动45480"）→ AI 内部记住这个ID用于执行命令
> 2. **用户说了活动名称但没有ID**（如"把周末聚餐的活动改一下"）→ 执行 `jielong list` 查看活动列表，找到名称匹配的活动，用「活动名称」向用户确认（**不要告诉用户活动ID**）
> 3. **用户什么都没说**（如"帮我改一下活动"）→ 执行 `jielong list` 显示活动列表（含名称），让用户用名称选择
> 4. **同一次对话中之前已经创建/查看过某个活动** → 可以直接用那个活动，但最好跟用户用名称确认一下
>
> **绝对不能凭猜测使用活动ID！必须从 `jielong list` 的输出中获取（AI内部使用，不要展示给用户）。**

```
jielong update 活动ID -n "新名称"
jielong update 活动ID -b "2026-06-01 00:00:00" -e "2026-06-30 23:59:59"
jielong update 活动ID -c "新的活动描述"
jielong update 活动ID -n "新名称" -b "2026-06-01 00:00:00" -e "2026-06-30 23:59:59" -c "新描述"
```

| 参数 | 说明 |
|------|------|
| `-n` | 修改活动名称 |
| `-b` | 修改开始时间 |
| `-e` | 修改结束时间 |
| `-c` | 修改活动描述 |

可以同时修改多个属性，也可以只修改其中一个。

**示例**：
```
# 只改名称
jielong update 45480 -n "周末聚餐（第二期）"

# 只改时间
jielong update 45480 -b "2026-06-10 00:00:00" -e "2026-06-15 23:59:59"

# 改名称+时间+描述
jielong update 45480 -n "周末聚餐" -b "2026-06-10 00:00:00" -e "2026-06-15 23:59:59" -c "请大家准时参加"
```

---

## 七、删除活动

```
jielong delete 活动ID
```

**注意**：删除操作不可恢复，执行前必须向用户确认（用活动名称，如"确认删除「周末聚餐」吗？"，不要暴露活动ID）！

---

## 八、重复创建

```
jielong redo
jielong redo -n "新的活动名称"
```

---

## 九、查看登录状态

```
jielong whoami
```

---

## 十、填表项管理（fields）

查看、添加、删除、修改活动的填表项。

> **确定要操作的活动**：如果用户没有提供活动（名称或ID），先执行 `jielong list` 查看活动列表，找到对应的活动（用活动名称与用户确认，不要暴露活动ID）。

### 10.1 查看填表项

```
jielong fields 活动ID
```

会列出所有填表项的序号、名称、类型、是否必填，以及单选/多选的选项。

### 10.2 添加填表项

```
jielong fields 活动ID --add "字段名:类型"
jielong fields 活动ID --add "字段名:类型:选项1,选项2"
jielong fields 活动ID --add "备注:多行文本" --optional
```

**格式**：`"字段名:类型"` 或 `"字段名:类型:选项1,选项2"`

**类型对照**：

| 类型名 | 类型值 | 说明 | 是否需要选项 |
|--------|--------|------|:----------:|
| 文本 | 1 | 普通输入框 | 否 |
| 单选 | 2 | 单选按钮 | **是** |
| 日期 | 3 | 日期选择器 | 否 |
| 多选 | 4 | 多选按钮 | **是** |
| 图片 | 5 | 图片上传 | 否 |
| 视频 | 6 | 视频上传 | 否 |
| 音频 | 7 | 音频上传 | 否 |
| 省市区 | 8 | 省市区选择器 | 否 |
| 多行文本 | 9 | 多行输入框 | 否 |
| 身份证 | 10 | 身份证号 | 否 |
| 手机号 | 11 | 手机号输入 | 否 |
| 位置 | 12 | 地理位置 | 否 |
| 数量 | 13 | 数字输入 | 否 |
| 时间 | 15 | 时间选择器 | 否 |
| 邮箱 | 19 | 邮箱输入 | 否 |
| 拍照 | 35 | 拍照上传 | 否 |

**参数**：
- `--optional`：设为选填（默认是必填）；不加此参数则为必填

**示例**：
```
# 添加文本字段（必填）
jielong fields 45480 --add "姓名:文本"

# 添加单选字段（带选项）
jielong fields 45480 --add "是否参加:单选:是,否"

# 添加多选字段
jielong fields 45480 --add "兴趣爱好:多选:篮球,足球,游泳,跑步"

# 添加选填字段
jielong fields 45480 --add "备注:多行文本" --optional

# 添加手机号字段
jielong fields 45480 --add "联系电话:手机号"
```

### 10.3 删除填表项

```
jielong fields 活动ID --remove 序号
```

先用 `jielong fields 活动ID` 查看当前填表项获取序号，然后删除。

**示例**：
```
# 先查看
jielong fields 45480
# 输出: 1. 姓名 [文本]  2. 手机号 [手机号]  3. 备注 [多行文本]

# 删除第2个（手机号）
jielong fields 45480 --remove 2
```

### 10.4 修改填表项名称

```
jielong fields 活动ID --remove 序号 --rename "新名称"
```

**注意**：用 `--remove` 指定要修改的序号，用 `--rename` 指定新名称。两个参数必须同时使用。

**示例**：
```
# 把第1个字段从"姓名"改为"参与者姓名"
jielong fields 45480 --remove 1 --rename "参与者姓名"
```

### 10.5 从JSON文件替换全部填表项

```
jielong fields 活动ID --file signlist.json
jielong fields 活动ID -F signlist.json
```

先用 `write_file` 生成 JSON 文件，然后用 `-F` 参数替换。

**JSON 文件格式**（是一个数组，包含分组）：
```json
[
  {
    "signListName": "报名信息",
    "signField": [
      {"fieldName": "姓名", "type": 1, "isRequired": 1, "sort": 0},
      {"fieldName": "是否参加", "type": 2, "isRequired": 1, "sort": 1, "content": "[{\"value\":\"是\",\"maxNum\":-1},{\"value\":\"否\",\"maxNum\":-1}]"},
      {"fieldName": "备注", "type": 9, "isRequired": 0, "sort": 2}
    ]
  }
]
```

---

## 十一、活动状态控制

> **确定要操作的活动**：如果用户没有提供活动（名称或ID），先执行 `jielong list` 查看活动列表，找到对应的活动（用活动名称与用户确认，不要暴露活动ID）。

### 11.1 提前结束活动（stop）

```
jielong stop 活动ID
jielong stop 活动ID --confirm
```

将正在进行中的活动提前结束。会显示活动名称和当前状态，需要确认后才执行。

- 活动已经是"已结束"状态 → 提示无需操作
- `--confirm` 可跳过确认提示

### 11.2 立即开始活动（start）

```
jielong start 活动ID
jielong start 活动ID --confirm
```

将"未开始"的活动立即改为"进行中"。

- 活动已经在"进行中" → 提示无需操作
- 活动已结束 → 提示使用 `restart` 命令
- `--confirm` 可跳过确认提示

### 11.3 重启已结束的活动（restart）

```
jielong restart 活动ID
jielong restart 活动ID -b "2026-06-01 00:00:00" -e "2026-06-30 23:59:59"
jielong restart 活动ID -b "2026-06-01 00:00:00" -e "2026-06-30 23:59:59" --confirm
```

重启一个已结束的活动，可以指定新的时间范围。

| 参数 | 说明 |
|------|------|
| `-b` | 新的开始时间（不指定则使用原时间） |
| `-e` | 新的结束时间（不指定则使用原时间） |
| `--confirm` | 跳过确认提示 |

**示例**：
```
# 用原来的时间重启
jielong restart 45480

# 重启并设置新的时间范围
jielong restart 45480 -b "2026-06-01 00:00:00" -e "2026-06-30 23:59:59"
```

---

## 十二、复制活动（copy）

```
jielong copy 源活动ID
jielong copy 源活动ID -n "新活动名称"
jielong copy 源活动ID -n "新名称" --with-signlist=false
```

从已有活动复制配置（类型、时间、填表项）创建一个新的活动。

| 参数 | 说明 |
|------|------|
| `-n` | 新活动名称（不指定则默认用源活动名称） |
| `--with-signlist` | 是否复制填表项（默认 `true`） |
| `--with-clockin` | 是否复制打卡配置（默认 `true`，仅打卡活动） |

**注意**：copy 命令需要交互式确认。AI 环境中使用时无法交互确认，请用以下替代方案：
先用 `jielong get 源活动ID` 获取配置，再用 `jielong create` 创建新活动。

---

## 十三、报名/代报名（sign）

> **确定要操作的活动**：如果用户没有提供活动（名称或ID），先执行 `jielong list` 查看活动列表，找到对应的活动（用活动名称与用户确认，不要暴露活动ID）。

### 13.1 查看活动的填表项（不报名，只看）

```bash
jielong sign 活动ID
```

不传 `--field` 参数时，会列出活动的所有填表项及其类型、是否必填、选项列表，方便确认后报名。

### 13.2 报名

```bash
jielong sign 活动ID --field "姓名:张三" --field "常用电话:13800138000"
jielong sign 活动ID --field "姓名:李四" --field "今晚吃什么:火锅"
jielong sign 活动ID --field "姓名:王五" --field "喜欢什么花:牡丹,茉莉"
```

| 用法 | 说明 |
|------|------|
| `--field "字段名=值"` | 填写一个字段，Windows 下用 `=` 分隔 |
| `--field "字段名:值"` | 填写一个字段，兼容冒号分隔 |
| 多选用逗号分隔 | `--field "喜欢什么花:牡丹,茉莉"` |
| 不提供图片字段 | 图片字段会自动留空（CLI 无法上传图片） |

**字段名必须与活动的填表项名称完全匹配**。如果不确定字段名，先执行 `jielong sign 活动ID` 查看。

### 13.3 报名示例

```bash
# 查看活动45522的填表项
jielong sign 45522

# 报名（填写文本和手机号）
jielong sign 45522 --field "姓名=张三" --field "常用电话=13800138000"

# 报名（含单选：今晚吃什么=火锅）
jielong sign 45522 --field "姓名=张三" --field "今晚吃什么=火锅"

# 报名（含多选：喜欢什么花=牡丹和茉莉）
jielong sign 45522 --field "姓名=张三" --field "喜欢什么花=牡丹,茉莉"

# 报名（含数量字段）
jielong sign 45522 --field "姓名=张三" --field "购买数量=3"
```

### 13.4 注意事项

1. **图片字段无法通过 CLI 上传**，图片字段会自动留空
2. **只填写提供的字段**，未通过 `--field` 提供的字段值为空字符串
3. **报名成功后返回订单ID**
4. **同一个用户对同一活动重复报名**可能被服务端拒绝，取决于活动设置

---

## 十四、报名记录管理

> **确定要操作的活动**：如果用户没有提供活动（名称或ID），先执行 `jielong list` 查看活动列表，找到对应的活动（用活动名称与用户确认，不要暴露活动ID）。

### 14.1 删除单条报名记录（sign-del）

```
jielong sign-del 活动ID 订单ID
jielong sign-del 活动ID 订单ID --confirm
```

先用 `jielong signups 活动ID` 查看报名列表，每条记录前会显示 `[订单ID]`，获取订单ID后再删除。

- 会自动查找该订单的报名人昵称并显示
- 需要确认后才执行删除
- `--confirm` 可跳过确认提示

**示例**：
```
# 第一步：查看报名列表，获取订单ID
jielong signups 45480
# 输出: [订单1001] 张三  姓名:张三  手机号:131xxxx
#       [订单1002] 李四  姓名:李四  手机号:132xxxx

# 第二步：删除指定订单
jielong sign-del 45480 1001 --confirm
```

### 14.2 清空所有报名记录（sign-clear）

```
jielong sign-clear 活动ID
jielong sign-clear 活动ID --confirm
```

清空一个活动的所有报名记录。

- 会显示活动名称和当前报名人数
- 会显示"此操作不可恢复"警告
- 需要二次确认后才执行
- `--confirm` 可跳过确认提示

**示例**：
```
jielong sign-clear 45480 --confirm
```

---

## 十五、关于 edit 命令（交互式修改 — AI 环境不可用）

> **⚠️ 重要：`jielong edit` 是交互式命令，需要逐步输入修改内容，AI 环境无法使用交互式终端。**
>
> **AI 环境中如需修改活动，请用以下两个命令组合替代：**
>
> | 需求 | 使用的命令 |
> |------|-----------|
> | 修改活动名称/时间/描述 | `jielong update 活动ID -n/-b/-e/-c`（见第六节） |
> | 添加/删除/改名填表项 | `jielong fields 活动ID --add/--remove/--rename`（见第十节） |
> | 替换全部填表项 | `jielong fields 活动ID -F signlist.json`（见第十节） |
>
> **绝对不要执行 `jielong edit`，它会卡住等待输入！**

---

## 重要注意事项

1. **⚠️ 每次对话都必须先执行 `jielong whoami` 检查登录状态**（不是检查 OpenClaw 的登录，是检查 jielong CLI 的登录），确认看到昵称和手机号后才能继续。绝对不能跳过这一步。
2. **不要使用 `jielong new`**（交互式命令），始终使用 `jielong create`
3. **不要使用 `jielong edit`**（交互式命令），用 `jielong update` + `jielong fields` 替代
4. **不要使用 `jielong copy`**（需要交互确认），用 `jielong get` 获取配置 + `jielong create` 创建替代
5. **简单活动**（只有文本/手机号等普通字段）→ 用 `jielong create -n ... -f ...`
6. **复杂活动**（有单选/多选/收费项/打卡配置）→ 用 `write_file` 生成 JSON + `jielong create --file`
7. **修改活动基本信息**（名称/时间/描述）→ 用 `jielong update`
8. **修改活动填表项**（添加/删除/改名）→ 用 `jielong fields`
9. **时间格式固定为** `"yyyy-MM-dd HH:mm:ss"`
10. **删除操作前必须向用户确认**（delete / sign-del / sign-clear）
11. **如果命令返回错误**，翻译成中文告诉用户并给出建议
12. **如果 jielong 未登录**（whoami 返回错误），提示用户去终端执行 `jielong login` 扫码
13. **单选/多选的 content 字段**是字符串类型，值是 JSON 序列化后的字符串（双层转义）
14. **收费报名(101)必须同时设置 `paymentSwitch: 1` 和 `fmActivityChargeItemVOS` 数组**
15. **所有 `--confirm` 参数用于跳过交互确认**，在 AI 环境中建议加上此参数以避免命令卡住
16. **AI 环境中所有可能需要确认的命令都应加 `--confirm`**：`stop`、`start`、`restart`、`sign-del`、`sign-clear`
17. **⚠️ 最高优先级：任何场景下都不要向用户展示活动ID（activityId）、活动Key、订单ID**。AI 自己记住即可，后续操作使用。所有面向用户的文字都用活动名称代替，包括操作前的叙述（如"正在删除「周末聚餐」"而不是"正在删除活动45480"）。不要把 `jielong` 命令原始输出直接粘贴给用户。
