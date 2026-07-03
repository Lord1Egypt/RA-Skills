---
name: tencentcloud-sms
description: 腾讯云短信（SMS）服务 Skill。当用户需要发送短信（验证码/通知/营销，单发或批量群发），管理短信签名与模板（查询、申请、跟踪审核状态），查询套餐包用量，统计发送量与回执送达率，或按手机号追踪短信下发/回复状态时使用。覆盖国内短信与国际/港澳台短信，基于腾讯云 SMS API。
---

# 腾讯云短信服务 Skill

基于腾讯云短信（SMS）API，帮助用户完成短信发送（验证码/通知/营销，单发或批量群发）、签名与模板管理（查询、申请、跟踪审核状态）、套餐包用量查询、发送量与回执送达率统计，以及按手机号追踪短信下发/回复状态。覆盖国内短信与国际/港澳台短信。

官方文档：https://cloud.tencent.com/document/product/382

## 能力总览

### 核心能力

| 能力 | 脚本 | 说明 |
|------|------|------|
| **发送短信** | `scripts/send_sms.py` | 发送验证码/通知/营销短信，支持从群发模板批量发送 |
| **签名管理** | `scripts/describe_sign.py`<br>`scripts/add_sign.py` | 查询签名列表/状态、新增签名并提交审核 |
| **模板管理** | `scripts/describe_template.py`<br>`scripts/add_template.py` | 查询模板列表/状态、新增模板并提交审核 |
| **套餐包监控统计** | `scripts/packages_statistics.py` | 查询套餐包用量、剩余条数、到期时间等 |
| **发送短信统计** | `scripts/send_status_statistics.py` | 统计指定时间段内提交侧数据（提交量、提交成功量、计费条数） |
| **发送回执统计** | `scripts/callback_status_statistics.py` | 统计指定时间段运营商回执侧结果分布（成功/失败/无效号码/停机/免打扰/频率限制等） |
| **状态拉取** | `scripts/pull_send_status_by_phone.py`<br>`scripts/pull_reply_status_by_phone.py` | 按手机号拉取下发状态/回复状态，用于追踪单个号码的送达情况与上行回复 |

### 群发短信支持

当用户需要**批量群发短信**时，使用 Skill 内置的群发 Excel 模板。

**模板文件**

| 模板文件 | 适用场景 | 手机号格式 |
|----------|----------|------------|
| `assets/国内短信群发模板.xlsx` | 国内短信群发 | 11 位手机号（如 `15122261234`），自动补 `+86` 前缀 |
| `assets/国际港澳台短信群发模板.xlsx` | 国际/港澳台短信群发 | 国家码+手机号（如 `8521414xxxx`），自动补 `+` 前缀 |

**模板格式说明**

| 列 | 内容 | 说明 |
|----|------|------|
| A 列 | 客户手机号 | 必填，每行一个号码 |
| B 列 | 短信内容变量1 | 对应模板中的 `{1}`，无变量时留空 |
| C 列 | 短信内容变量2 | 对应模板中的 `{2}`，无变量时留空 |
| D 列 | 短信内容变量3 | 对应模板中的 `{3}`，无变量时留空 |

> **注意**：如果短信模板中没有变量，只需填写 A 列（客户手机号）即可。变量列可根据实际模板变量数量扩展。

**配套脚本（分发 / 解析）**

| 能力 | 脚本 | 说明 |
|------|------|------|
| 分发群发模板 | `scripts/prepare_bulk_template.py` | 复制空白群发模板到工作区（带时间戳）并作为附件下发，避免使用 Skill 内置原始文件残留旧数据；桌面端可选 `--open` 自动打开 |
| 解析群发模板 | `scripts/parse_bulk_template.py` | 解析群发 Excel 模板，提取手机号和模板变量，自动校验变量列数（可选调用 DescribeSmsTemplateList） |

## 使用时机

当用户提出以下需求时触发此技能：

### 短信发送场景
- 需要发送短信（验证码、通知、营销）
- 需要批量群发短信、导入号码群发
- 涉及腾讯云 SMS 服务的调用场景

### 签名管理场景
- 查询已有签名列表、签名审核状态
- 新增短信签名并提交审核
- **国内短信实名报备场景**：查询新签名的报备状态，通过 `StatusCode=0` 标识签名报备完成可用

### 模板管理场景
- 查询已有模板列表、模板审核状态
- 新增短信模板并提交审核
- 确认模板变量数量（用于群发校验）

### 套餐包监控场景
- 查询套餐包剩余条数、用量统计
- 监控套餐包到期时间，提前预警
- 评估是否需要购买新套餐包

### 状态查询场景
- 按手机号查询短信下发状态（是否送达）
- 按手机号查询用户回复状态
- 统计指定时间段的发送回执数据（运营商回执侧）
- 统计指定时间段的发送短信数据（提交侧）

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（脚本会自动检测并安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云 API 密钥 SecretId
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云 API 密钥 SecretKey

检查环境变量：
```bash
python3 scripts/check_env.py
```

### 前提条件

使用前请确保：
1. 已开通 [腾讯云短信服务](https://console.cloud.tencent.com/smsv2)
2. 已在 [访问管理 > API 密钥管理](https://console.cloud.tencent.com/cam/capi) 获取 SecretId 和 SecretKey
3. 如需发送国内短信，需先购买国内短信套餐包
4. 签名和模板需通过审核后方可用于发送短信
5. **企业认证要求**：签名、模板的增查 API 仅支持企业认证用户，个人认证用户请在控制台操作

## 必须遵守的规则

### 密钥安全

- 禁止将 SecretId、SecretKey 硬编码到代码或工作区文件中
- 群聊场景：禁止让用户直接发送密钥
- 私聊场景：提醒"密钥会经过 LLM，存在泄漏风险"
- **密钥轮换建议**：定期轮换 API 密钥，避免长期使用同一密钥
- **最小权限原则**：建议使用 CAM 子账号并配置自定义策略，仅授予本 Skill 所需的最小 API 权限，而非 `QcloudSMSFullAccess` 全量权限。详见下方「推荐权限配置」

### 推荐权限配置

#### 方案 1：自定义策略 — 仅授权本 Skill 涉及的 API

前往 [CAM 策略管理](https://console.cloud.tencent.com/cam/policy) → 新建自定义策略 → 按策略语法创建，使用以下 JSON：

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "sms:SendSms",
        "sms:DescribeSmsSignList",
        "sms:DescribeSmsTemplateList",
        "sms:AddSmsSign",
        "sms:AddSmsTemplate",
        "sms:SmsPackagesStatistics",
        "sms:SendStatusStatistics",
        "sms:CallbackStatusStatistics",
        "sms:PullSmsSendStatusByPhoneNumber",
        "sms:PullSmsReplyStatusByPhoneNumber"
      ],
      "resource": "*"
    }
  ]
}
```

> 上述 10 个 action 与本 Skill 的核心能力对应：
> | API Action | 对应能力 |
> |-----------|---------|
> | `sms:SendSms` | 发送短信 |
> | `sms:DescribeSmsSignList` | 签名管理 - 查询 |
> | `sms:AddSmsSign` | 签名管理 - 新增 |
> | `sms:DescribeSmsTemplateList` | 模板管理 - 查询 |
> | `sms:AddSmsTemplate` | 模板管理 - 新增 |
> | `sms:SmsPackagesStatistics` | 套餐包监控统计 |
> | `sms:SendStatusStatistics` | 发送短信统计（提交侧） |
> | `sms:CallbackStatusStatistics` | 发送回执统计（运营商回执侧） |
> | `sms:PullSmsSendStatusByPhoneNumber` | 状态拉取 - 下发状态 |
> | `sms:PullSmsReplyStatusByPhoneNumber` | 状态拉取 - 回复状态 |

如果只需要发送短信（不需要管理签名/模板），可进一步缩小为：

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "sms:SendSms",
        "sms:DescribeSmsTemplateList"
      ],
      "resource": "*"
    }
  ]
}
```

#### 方案 2：叠加 IP 白名单限制（推荐）

在方案 1 基础上增加 `condition` 限制来源 IP，仅允许从指定 IP 地址调用 API。参考 [CAM 限制 IP 访问文档](https://cloud.tencent.com/document/product/598/38037)：

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "sms:SendSms",
        "sms:DescribeSmsSignList",
        "sms:DescribeSmsTemplateList",
        "sms:AddSmsSign",
        "sms:AddSmsTemplate",
        "sms:SmsPackagesStatistics",
        "sms:SendStatusStatistics",
        "sms:CallbackStatusStatistics",
        "sms:PullSmsSendStatusByPhoneNumber",
        "sms:PullSmsReplyStatusByPhoneNumber"
      ],
      "resource": "*",
      "condition": {
        "ip_equal": {
          "qcs:ip": [
            "YOUR_IP_ADDRESS"
          ]
        }
      }
    }
  ]
}
```

> 将 `YOUR_IP_ADDRESS` 替换为实际的公网 IP 或 CIDR 网段（如 `203.0.113.0/24`），支持填写多个。

#### 配置步骤

1. 前往 [CAM 用户列表](https://console.cloud.tencent.com/cam) → 新建子用户 → 选择「自定义创建」→ 可编程访问
2. 前往 [CAM 策略管理](https://console.cloud.tencent.com/cam/policy) → 新建自定义策略 → 按策略语法创建 → 粘贴上述 JSON
3. 将自定义策略关联到子用户
4. 使用子用户的 SecretId / SecretKey 配置环境变量

### 交互方式约定

- **选项交互优先**：当需要用户从**固定枚举值**中选择时（如短信类型、发送方式、签名类型、证明类型、签名用途、确认/取消等），**必须**使用 `AskUserQuestion` 工具提供交互式选择，而非纯文本编号列表。这样用户在 IDE / 桌面 Agent 中可以直接点选，避免来回打字。
- **选项格式约定**：每个选项使用 `label` + `description` 两字段：
  - `label`：简短中文名称（≤ 8 字），用作按钮文本
  - `description`：解释说明，告诉用户该选项的实际含义或对应的接口取值
- **示例**（短信类型选择）：
  ```json
  {
    "question": "请选择需要发送的短信类型",
    "options": [
      {"label": "国内短信", "description": "面向中国大陆 +86 手机号；--international 0"},
      {"label": "国际/港澳台短信", "description": "面向中国港澳台与海外手机号；--international 1"}
    ]
  }
  ```
- **不要用选项的场景**：自由输入（手机号、签名内容、模板内容、应用 ID 等）仍然使用文本输入；多步骤的逐步引导本身不是选项。
- **回退机制**：当宿主不支持或调用 `AskUserQuestion` 失败时，按以下规则降级：
  1. **格式**：输出编号纯文本列表，每行 `编号) label —— description`，末行提示"请回复编号或选项名称"。
  2. **写操作（发送短信 / 添加签名 / 添加模板 / 群发）的最终确认**：回退到文本时，**必须要求用户回复明确文字**（如 `确认发送`），**禁止接受单字符 `y`**，以避免误确认。
  3. **重试策略**：同一询问连续失败 2 次后，停止重试，向用户返回结构化错误（含具体卡点的字段名），由用户决定下一步。

### AI 行为约束

- **只调用本 Skill 封装的脚本**：禁止直接用 Python SDK 或 curl 调用未封装的腾讯云 API。如需调用本 Skill 未封装的接口，必须先告知用户"该接口暂未封装"，并建议前往 [控制台](https://console.cloud.tencent.com/smsv2) 操作
- **签名/模板 ID 必须来自真实查询**：禁止编造或猜测签名 ID / 模板 ID。查询签名/模板列表时，应先用 `describe_sign.py` 分页查询获取真实 ID，不得随意填写 1~10 等序号
- **先预览后执行**：对写入类操作（发送短信、添加签名/模板），**必须**先用 `--dry-run` 预览请求参数，展示给用户确认后再执行
- **定时/批量任务必须确认**：设置定时发送或批量群发时，即使已做 dry-run 预览，仍需明确告知用户发送签名、接收人数、发送内容，并等待用户确认后再执行（确认动作使用 `AskUserQuestion` 选项交互）
- **先审核后发送**：签名和模板必须审核通过后才能用于发送短信，审核状态通过 `describe_sign.py` / `describe_template.py` 查询确认
- **群发模板必须复制后再发**：分发群发 Excel 模板时，**禁止直接把 `assets/` 下原始模板路径告知用户**，必须调用 `prepare_bulk_template.py` 生成一份带时间戳的新副本（**默认生成到当前工作区，作为附件下发**；不要默认放桌面，桌面端如需可加 `--open`），确保用户每次拿到的是空白模板

### 输出规范

- **结构化输出**：所有脚本以 JSON 格式输出结果到 stdout，日志信息输出到 stderr
- **错误如实返回**：脚本失败时必须返回错误 JSON，不得猜测或伪造结果

## 发送短信工作流

当用户需要发送短信时，按以下步骤引导：

> **逐步引导原则（必须遵守）**：
> - **每次只展示当前步骤**，等用户完成并回复后，再引导下一步
> - **禁止在一条消息中同时展示多个步骤**的内容或参数收集表
> - 如果当前步骤包含子步骤（如 2.1、2.2），也要逐个引导，不要合并
> - 用户主动提供了后续步骤所需的信息时，可以跳过对应步骤，但仍然只展示下一个待完成的步骤

### 步骤 1：检查密钥配置

首先运行环境变量检测脚本，自动检查密钥是否已配置：

```bash
python3 <SKILL_DIR>/scripts/check_env.py
```

- **如果检测结果为 `"configured": true`**：说明已检测到环境变量已配置，直接进入步骤 2
- **如果检测结果为 `"configured": false`**：使用 `AskUserQuestion` 工具询问用户当前状态，提供以下选项（不要再用纯文本数字列表）：

  ```json
  {
    "question": "未检测到腾讯云密钥，请告诉我您当前的情况",
    "options": [
      {"label": "已有密钥，未配置", "description": "已经在控制台拿到 SecretId/SecretKey，但还没写入 shell 环境变量"},
      {"label": "没有密钥，待创建", "description": "还没创建过腾讯云 API 密钥，需要前往访问管理新建"},
      {"label": "无法获取密钥", "description": "受限环境/无主账号权限，希望直接用控制台手动操作"}
    ]
  }
  ```

用户选择后的引导：

- **选择「已有密钥，未配置」** → 引导用户将以下命令添加到 `~/.profile`、`~/.bashrc` 或 `~/.zshrc` 中：
  ```bash
  export TENCENTCLOUD_SECRET_ID="你的SecretId"
  export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
  ```
- **选择「没有密钥，待创建」** → 引导用户前往 [访问管理](https://console.cloud.tencent.com/cam/capi) 新建密钥
- **选择「无法获取密钥」** → 引导用户直接使用 [短信控制台](https://console.cloud.tencent.com/smsv2) 进行操作

> 等待用户确认密钥已配置后，再进入步骤 2。

### 步骤 2：收集短信发送参数

提醒用户需要先开通短信服务，可参考：
- [国内短信快速入门](https://cloud.tencent.com/document/product/382/37745)
- [国际/港澳台短信快速入门](https://cloud.tencent.com/document/product/382/37797)

#### 2.1 确认短信类型

使用 `AskUserQuestion` 工具询问用户需要发送的短信类型：

```json
{
  "question": "请选择需要发送的短信类型",
  "options": [
    {"label": "国内短信", "description": "面向中国大陆 +86 手机号；--international 0"},
    {"label": "国际/港澳台短信", "description": "面向中国港澳台或海外手机号；--international 1"}
  ]
}
```

> 等待用户选择短信类型后，再进入 2.2。

#### 2.2 收集基本参数

根据用户选择的短信类型，引导用户提供对应参数：

**国内短信参数：**

| 参数 | 格式示例 | 说明 |
|------|----------|------|
| 应用 ID | `1400006666` | 前往 [应用管理](https://console.cloud.tencent.com/smsv2/app-manage) 获取 |
| 签名内容 | `腾讯云` | 已审核通过的签名内容 |
| 模板 ID | `1110` | 已审核通过的模板 ID |

**国际/港澳台短信参数：**

| 参数 | 格式示例 | 说明 |
|------|----------|------|
| 应用 ID | `1400006666` | 前往 [应用管理](https://console.cloud.tencent.com/smsv2/app-manage) 获取 |
| 签名内容（可选） | `腾讯云` | 已审核通过的签名内容，国际/港澳台短信可不提供 |
| 模板 ID | `1110` | 已审核通过的模板 ID |
| SenderId | `Qsms` | 国际/港澳台短信已申请独立 SenderId 时需填写 |

> **注意**：应用 ID 可查询 [应用列表](https://console.cloud.tencent.com/smsv2/app-manage)。

> 等待用户提供基本参数后，再进入 2.3。

#### 2.3 确认发送方式

用户提供基本参数后，使用 `AskUserQuestion` 询问发送方式：

```json
{
  "question": "请选择发送方式",
  "options": [
    {"label": "单发", "description": "只给 1 个或少量手机号发送，直接在对话中提供号码"},
    {"label": "群发/批量发送", "description": "通过 Excel 模板批量导入号码与变量，自动按 200 条/批分发"}
  ]
}
```

- **选择「单发」**：引导用户提供接收手机号

  | 参数 | 格式示例 | 说明 |
  |------|----------|------|
  | 手机号 | `+8618501234444` | E.164 格式，国内手机号前加 +86 |

- **选择「群发/批量发送」**：跳转至 [步骤 5：批量/群发特殊处理](#步骤-5批量群发特殊处理)

> 等待用户确认发送方式并提供手机号后，再进入步骤 3。

### 步骤 3：辅助查询签名和模板（仅在用户无法提供时）

如果用户无法提供签名内容或模板 ID，主动为用户查询可用列表。根据步骤 2.1 确认的短信类型，使用对应的 `--international` 参数：

- **国内短信**：`--international 0`
- **国际/港澳台短信**：`--international 1`

1. **同时查询签名和模板**：并行执行以下两个命令，一次性获取签名和模板列表：
   - `describe_sign.py --international <0|1> --limit 10 --offset 0`
   - `describe_template.py --international <0|1> --limit 10 --offset 0`
2. **展示结果**：将查询到的签名列表和模板列表一并展示给用户，引导用户分别选择签名和模板
3. **处理非企业认证**：如果查询返回错误码 `FailedOperation.NotEnterpriseCertification`，告知用户：
   - "您的账号为个人认证，签名/模板增查 API 仅支持企业认证用户"
   - "请前往 [控制台](https://console.cloud.tencent.com/smsv2) 手动查看签名和模板"
   - "或前往 [实名认证](https://console.cloud.tencent.com/developer/auth) 升级为企业认证"

> 等待用户确认签名和模板选择后，再进入步骤 4。

### 步骤 4：dry-run 预览

发送前**必须**先执行 `--dry-run` 预览，并将预览结果格式化展示给用户。

其中「发送内容」需要根据**步骤 3 查询到的模板内容**，将用户提供的模板参数按顺序替换模板中的变量（变量格式为 `{1}`、`{2}`、`{3}`……）生成实际发送文本。例如：
- 模板内容：`{1}为您的登录验证码，请于{2}分钟内填写，如非本人操作，请忽略本短信。`
- 模板参数：`128719` `5`
- 发送内容：`128719为您的登录验证码，请于5分钟内填写，如非本人操作，请忽略本短信。`

根据步骤 2.1 确认的短信类型，使用对应的预览格式：

**国内短信预览：**

```
📋 短信发送预览（国内短信）
━━━━━━━━━━━━━━━━━━━━━━
📱 接收人: +8618501234444（共 1 个号码）
🔑 应用ID: 1400006666
📝 签名: 腾讯云
📄 模板ID: 1110
🔢 模板参数: ["128719", "5"]
📨 下发内容: 【腾讯云】128719为您的登录验证码，请于5分钟内填写，如非本人操作，请忽略本短信。
━━━━━━━━━━━━━━━━━━━━━━
```

**国际/港澳台短信预览（有签名）：**

```
📋 短信发送预览（国际/港澳台短信）
━━━━━━━━━━━━━━━━━━━━━━
📱 接收人: +8521414xxxx（共 1 个号码）
🔑 应用ID: 1400006666
📝 签名: 腾讯云
📄 模板ID: 1110
🆔 SenderId: Qsms
🔢 模板参数: ["128719", "5"]
📨 下发内容: [腾讯云]128719为您的登录验证码，请于5分钟内填写，如非本人操作，请忽略本短信。
━━━━━━━━━━━━━━━━━━━━━━
```

**国际/港澳台短信预览（无签名）：**

```
📋 短信发送预览（国际/港澳台短信）
━━━━━━━━━━━━━━━━━━━━━━
📱 接收人: +8521414xxxx（共 1 个号码）
🔑 应用ID: 1400006666
📄 模板ID: 1110
🆔 SenderId: Qsms
🔢 模板参数: ["128719", "5"]
📨 下发内容: 128719为您的登录验证码，请于5分钟内填写，如非本人操作，请忽略本短信。
━━━━━━━━━━━━━━━━━━━━━━
```

> **注意**：
> - 国际/港澳台短信的签名为可选项，如用户提供了签名，下发内容中使用英文中括号包裹签名（如 `[腾讯云]`）；如未提供签名，则不展示签名相关行。
> - 如用户在步骤 2.2 提供了 SenderId，预览中需展示该字段；如未提供则不展示。

**两步走，严禁合并**：

1. **第一步**：将上述预览代码块**正常输出**给用户（作为 markdown 内容展示），不要询问、不要带 `y/n`。
2. **第二步**：**单独**调用 `AskUserQuestion` 发起确认，`question` 字段保持简短（如 `"是否确认发送？"`），**禁止**把整段预览塞进 `question`：

   ```json
   {
     "question": "是否确认发送？",
     "options": [
       {"label": "确认发送", "description": "立即调用 SendSms 接口发送短信"},
       {"label": "取消", "description": "终止本次发送，不调用接口"},
       {"label": "修改参数", "description": "回到上一步重新调整签名/模板/接收人/参数"}
     ]
   }
   ```

用户选择「确认发送」后才实际执行发送。

> 等待用户确认后，执行发送。如需群发，进入步骤 5。

### 步骤 5：批量/群发特殊处理

当用户需要批量群发时，优先推荐使用群发 Excel 模板。以下子步骤也需逐步引导，每次只展示当前子步骤：

1. **生成并下发空白模板**：根据用户的短信类型，调用 `prepare_bulk_template.py` 生成一份**带时间戳的全新空白模板**到**当前工作区**（默认 cwd，**不要**默认放桌面），随后**作为附件下发给用户**。

   ```bash
   # 国内短信（生成到当前工作区，默认不自动打开）
   python3 <SKILL_DIR>/scripts/prepare_bulk_template.py --international 0

   # 国际/港澳台短信
   python3 <SKILL_DIR>/scripts/prepare_bulk_template.py --international 1
   ```

   脚本输出 JSON 包含 `destination`（生成文件的**绝对路径**）和 `opened`（是否自动打开成功）字段。展示给用户时**必须**：
   - **明确告知绝对路径**（直接读 `destination` 字段，不要再说"在 Skill 目录下"）。
   - **默认行为（适配多 channel）**：用户可能通过各类聊天 channel 使用本 Skill，这类环境**没有「桌面」概念、也不能在服务端「打开」文件**。因此：
     - **统一用支持文件附件的宿主能力，将 `destination` 作为附件直接发送给用户下载**——这是默认且首选的下发方式。
     - **不要默认自动打开文件**，脚本默认 `opened=false`。
   - **仅当确定是本地桌面端**（用户在本机桌面 Agent / IDE 中操作）时，才可追加 `--open` 让脚本自动打开 Excel；此时根据 `opened` 字段提示：
     - `opened=true`：告知"已为您打开模板，请在弹出的 Excel 中填写"。
     - `opened=false`：告知"请打开附件中的模板 `<destination>` 填写"。
   - **若用户显式指定了目录**，使用 `--dest-dir <用户指定路径>`；否则保持默认工作区。

   > **禁止**：不要直接使用 `<SKILL_DIR>/assets/...` 下的原始模板路径下发或解析（那份模板可能残留之前会话填的旧数据）。每次群发都必须**新建一份**。

> 等待用户确认收到模板后，再引导填写。

2. **引导用户填写**：告知用户模板的填写规则（A 列填手机号，B~D 列填模板变量；只填 A 列即可适用于无变量模板）。

> 等待用户上传填好的 Excel 后，再进行解析。

3. **解析与变量校验**：用户上传填好的 Excel 后，使用 `parse_bulk_template.py --template-id <模板ID> --international <0|1>` 解析验证。脚本会自动完成以下流程：
   - **自动查询模板变量数**：通过模板 ID 调用 API 获取模板内容，解析出实际需要的变量个数
   - **校验 Excel 变量列数**：
     - ✅ Excel 变量列数 **≥** 模板实际变量数 → 自动兼容解析，忽略多余列
     - ❌ Excel 变量列数 **<** 模板实际变量数 → 报错提示用户缺少几个变量，需要重新上传
   - 如果校验不通过，将用户报错信息展示给用户，引导用户补充缺失的变量列后重新上传

> 解析完成后，展示解析结果（含变量校验信息），等待用户确认再进行预览。

4. **dry-run 预览**：使用 `send_sms.py --from-file` 并加 `--dry-run` 预览群发参数

> 展示预览结果，等待用户确认后再执行发送。

5. **确认后发送**：**两步走**——先把接收人总数/前 5 号码预览/分批情况作为 markdown 输出给用户；然后**单独**调用 `AskUserQuestion` 发起确认，`question` 字段保持简短，**禁止**把预览内容塞进 `question`：

   ```json
   {
     "question": "是否开始群发？",
     "options": [
       {"label": "确认群发", "description": "立即发送，脚本将自动按每批 200 个号码分批发送"},
       {"label": "取消", "description": "终止本次群发，不调用接口"}
     ]
   }
   ```

群发（>10 个号码）时额外展示：
- 接收人总数及前 5 个号码预览
- 如号码超过 200 个，脚本会自动分批发送（每批最多 200 个）

## 脚本说明

### 通用参数

所有脚本均支持以下通用参数：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --region | str | 否 | 腾讯云地域，默认 `ap-guangzhou`（国内站）。国际站账号请使用 `ap-singapore` |
| --dry-run | flag | 否 | 预览模式：仅验证参数并输出请求体，不实际调用 API |

> **关于 `--region`**：默认 `ap-guangzhou` 适用于**国内站**账号。若接口返回错误码 `UnsupportedRegion`（或错误信息提示当前地域不支持），通常意味着用户使用的是**国际站账号**，此时应通过 `AskUserQuestion` 询问用户是否改用 `ap-singapore`（国际站标准地域）后重试；用户确认后所有后续调用都应带上 `--region ap-singapore`。

### 1. 发送短信 — `scripts/send_sms.py`

发送验证码、通知类或营销短信。

```bash
python3 <SKILL_DIR>/scripts/send_sms.py \
  --phone-number-set "+8618501234444" "+8618501234445" \
  --sdk-app-id "1400006666" \
  --template-id "1110" \
  --sign-name "腾讯云" \
  --template-param-set "4370"

# 预览模式（不实际发送）
python3 <SKILL_DIR>/scripts/send_sms.py \
  --phone-number-set "+8618501234444" \
  --sdk-app-id "1400006666" --template-id "1110" \
  --sign-name "腾讯云" --template-param-set "4370" \
  --dry-run

# 从群发 Excel 模板批量发送（每个号码可有独立模板变量）
python3 <SKILL_DIR>/scripts/send_sms.py \
  --from-file "/path/to/群发模板.xlsx" \
  --sdk-app-id "1400006666" --template-id "1110" \
  --sign-name "腾讯云" --international 0 --dry-run
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --phone-number-set | str[] | 二选一 | 手机号列表（E.164 格式，如 +8618501234444），单次最多 200 个 |
| --from-file | str | 二选一 | 群发 Excel 模板文件路径（.xlsx），与 --phone-number-set 互斥 |
| --sdk-app-id | str | 是 | 短信 SdkAppId |
| --template-id | str | 是 | 已审核通过的模板 ID |
| --sign-name | str | 否 | 已审核通过的签名（国内短信必填） |
| --template-param-set | str[] | 否 | 模板参数列表（使用 --from-file 时忽略，从 Excel 读取） |
| --international | int | 否 | 0=国内短信（默认），1=国际/港澳台短信（仅 --from-file 模式使用） |
| --extend-code | str | 否 | 短信码号扩展号 |
| --session-context | str | 否 | 用户 session 上下文，会原样返回 |
| --sender-id | str | 否 | 国际/港澳台短信 Sender ID |

### 2. 查询签名 — `scripts/describe_sign.py`

查询短信签名列表，辅助用户获取可用签名信息。

```bash
# 按 ID 精确查询
python3 <SKILL_DIR>/scripts/describe_sign.py \
  --sign-id-set 1110 1111 \
  --international 0

# 分页查询全部签名
python3 <SKILL_DIR>/scripts/describe_sign.py \
  --international 0 --limit 10 --offset 0
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --sign-id-set | int[] | 否 | 签名 ID 列表（空格分隔），不填则分页查询全部，最多 100 个 |
| --international | int | 是 | 0=国内短信，1=国际/港澳台短信 |
| --limit | int | 否 | 返回数量上限，默认 10，最大 100（仅分页模式） |
| --offset | int | 否 | 偏移量，默认 0（仅分页模式） |

#### 签名状态码说明（StatusCode）

| 状态码 | 含义 | 说明 |
|--------|------|------|
| **0** | **已审核通过** | 签名报备完成，可用于发送短信 |
| 1 | 审核中 | 签名正在审核，通常 2 小时内完成 |
| 2 | 审核未通过 | 查看 ReviewReply 字段获取拒绝原因 |
| -1 | 已删除/无效 | 签名已被删除或失效 |

> **国内短信实名报备场景**：新签名提交后，需等待审核通过（`StatusCode=0`）才能用于发送短信。可通过定期调用此脚本查询签名状态，确认报备是否完成。

### 3. 查询模板 — `scripts/describe_template.py`

查询短信模板列表，辅助用户获取可用模板信息。

```bash
# 按 ID 精确查询
python3 <SKILL_DIR>/scripts/describe_template.py \
  --international 0 \
  --template-id-set 1110 1111

# 分页查询全部模板
python3 <SKILL_DIR>/scripts/describe_template.py \
  --international 0 --limit 20 --offset 0
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --international | int | 是 | 0=国内短信，1=国际/港澳台短信 |
| --template-id-set | int[] | 否 | 模板 ID 列表，空则查询全部 |
| --limit | int | 否 | 返回数量上限，默认 10，最大 100 |
| --offset | int | 否 | 偏移量，默认 0 |

#### 模板状态码说明（StatusCode）

| 状态码 | 含义 | 说明 |
|--------|------|------|
| **0** | **已审核通过** | 模板可用于发送短信 |
| 1 | 审核中 | 模板正在审核，通常 2 小时内完成 |
| 2 | 审核未通过 | 查看 ReviewReply 字段获取拒绝原因 |
| -1 | 已删除/无效 | 模板已被删除或失效 |

### 4. 添加签名 — `scripts/add_sign.py`

创建短信签名并提交审核（企业认证用户）。

```bash
# 国内短信签名（需提供资质 ID）
python3 <SKILL_DIR>/scripts/add_sign.py \
  --sign-name "腾讯云" \
  --sign-type 0 \
  --document-type 1 \
  --international 0 \
  --sign-purpose 0 \
  --proof-image "/path/to/proof.jpg" \
  --qualification-id 1000001

# 国际/港澳台短信签名（无需资质 ID）
python3 <SKILL_DIR>/scripts/add_sign.py \
  --sign-name "腾讯云" \
  --sign-type 0 \
  --document-type 1 \
  --international 1 \
  --sign-purpose 0 \
  --proof-image "/path/to/proof.jpg"

# 预览模式（不实际调用 API）
python3 <SKILL_DIR>/scripts/add_sign.py \
  --sign-name "腾讯云" --sign-type 0 --document-type 1 \
  --international 0 --sign-purpose 0 --proof-image "/path/to/proof.jpg" \
  --qualification-id 1000001 --dry-run
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --sign-name | str | 是 | 签名名称 |
| --sign-type | int | 是 | 签名类型：0=公司，4=商标，5=政府/机关事业单位/其他机构 |
| --document-type | int | 是 | 证明类型：0=三证合一，1=企业营业执照，2=组织机构代码证书，3=社会信用代码证书，7=商标注册书 |
| --international | int | 是 | 0=国内短信，1=国际/港澳台短信 |
| --sign-purpose | int | 是 | 签名用途：0=自用，1=他用 |
| --proof-image | str | 是 | 资质证明图片文件路径（自动 Base64 编码） |
| --commission-image | str | 否 | 委托授权证明图片路径（他用时需要） |
| --remark | str | 否 | 申请备注 |
| --qualification-id | int | 条件必填 | 已审核通过的国内短信资质 ID（国内短信需填写，国际短信无需填写）。前往 [实名资质管理](https://console.cloud.tencent.com/smsv2/enterprise) 查看 |

#### add_sign.py 参数收集时的选项交互

收集 `--sign-type` / `--document-type` / `--sign-purpose` 这三个枚举字段时，**必须**用 `AskUserQuestion` 工具，不要让用户打字数字：

```json
{
  "question": "请选择签名类型（对应 --sign-type）",
  "options": [
    {"label": "公司",   "description": "企业、机构主体；--sign-type 0"},
    {"label": "商标",   "description": "已注册商标；--sign-type 4"},
    {"label": "政府/事业单位", "description": "政府、机关事业单位、其他机构；--sign-type 5"}
  ]
}
```

```json
{
  "question": "请选择资质证明类型（对应 --document-type）",
  "options": [
    {"label": "三证合一",   "description": "--document-type 0"},
    {"label": "企业营业执照", "description": "--document-type 1"},
    {"label": "组织机构代码证书", "description": "--document-type 2"},
    {"label": "社会信用代码证书", "description": "--document-type 3"},
    {"label": "商标注册书",  "description": "--document-type 7"}
  ]
}
```

```json
{
  "question": "请选择签名用途（对应 --sign-purpose）",
  "options": [
    {"label": "自用", "description": "用于自有业务发送；--sign-purpose 0"},
    {"label": "他用", "description": "代第三方发送，需额外提交委托授权证明；--sign-purpose 1"}
  ]
}
```

### 5. 添加模板 — `scripts/add_template.py`

创建短信正文模板并提交审核。

```bash
python3 <SKILL_DIR>/scripts/add_template.py \
  --template-name "验证码" \
  --template-content "您的验证码是{1}，{2}分钟内有效。" \
  --sms-type 3 \
  --international 0 \
  --remark "登录验证码"
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --template-name | str | 是 | 模板名称 |
| --template-content | str | 是 | 模板内容，变量使用 {1}、{2} 等 |
| --sms-type | int | 是 | 短信类型：1=营销，2=通知，3=验证码 |
| --international | int | 是 | 0=国内短信，1=国际/港澳台短信 |
| --remark | str | 是 | 模板备注（申请原因、使用场景） |

#### add_template.py 参数收集时的选项交互

收集 `--sms-type` 时，**必须**用 `AskUserQuestion` 工具：

```json
{
  "question": "请选择模板类型（对应 --sms-type）",
  "options": [
    {"label": "验证码", "description": "登录、注册、找回密码等场景；--sms-type 3"},
    {"label": "通知",   "description": "订单、状态、活动通知等服务类短信；--sms-type 2"},
    {"label": "营销",   "description": "促销、活动推广类短信，需用户授权；--sms-type 1"}
  ]
}
```

### 6. 解析群发模板 — `scripts/parse_bulk_template.py`

解析群发 Excel 模板文件，提取手机号和模板变量列表。支持通过 `--template-id` 自动查询模板实际变量数并校验。

```bash
# 解析国内短信群发模板（带变量校验）
python3 <SKILL_DIR>/scripts/parse_bulk_template.py \
  --file "/path/to/国内短信群发模板.xlsx" --international 0 --template-id 1110

# 解析国际/港澳台短信群发模板（带变量校验）
python3 <SKILL_DIR>/scripts/parse_bulk_template.py \
  --file "/path/to/国际港澳台短信群发模板.xlsx" --international 1 --template-id 1111
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --file | str | 是 | 群发 Excel 模板文件路径 |
| --international | int | 否 | 0=国内短信（默认），1=国际/港澳台短信 |
| --template-id | str | 是 | 模板 ID，脚本会自动查询模板变量数并校验 Excel 变量列数（Excel 变量列 ≥ 模板变量数则兼容，< 则报错） |

### 7. 套餐包查询 — `scripts/packages_statistics.py`

查询短信套餐包用量统计。

```bash
python3 <SKILL_DIR>/scripts/packages_statistics.py \
  --sdk-app-id "1400006666" \
  --begin-time "2026010100" \
  --end-time "2026033123"
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --sdk-app-id | str | 是 | 短信 SdkAppId |
| --begin-time | str | 是 | 套餐包起始创建时间，格式 yyyymmddhh |
| --end-time | str | 是 | 套餐包结束创建时间，格式 yyyymmddhh |
| --limit | int | 否 | 返回数量上限，默认 100 |
| --offset | int | 否 | 偏移量，默认 0 |

### 8. 发送短信统计 — `scripts/send_status_statistics.py`

统计指定时间段提交侧数据（提交量 / 提交成功量 / 计费条数）。

```bash
python3 <SKILL_DIR>/scripts/send_status_statistics.py \
  --sdk-app-id "1400006666" \
  --begin-time "2026010100" \
  --end-time "2026013123"

# 预览模式
python3 <SKILL_DIR>/scripts/send_status_statistics.py \
  --sdk-app-id "1400006666" \
  --begin-time "2026010100" --end-time "2026013123" --dry-run
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --sdk-app-id | str | 是 | 短信 SdkAppId |
| --begin-time | str | 是 | 起始时间，格式 yyyymmddhh |
| --end-time | str | 是 | 结束时间，格式 yyyymmddhh，需 ≥ BeginTime（无 32 天上限） |

### 9. 发送回执统计 — `scripts/callback_status_statistics.py`

统计指定时间段运营商回执侧数据（回执成功/失败、无效号码、停机、免打扰、频率限制等）。

```bash
python3 <SKILL_DIR>/scripts/callback_status_statistics.py \
  --sdk-app-id "1400006666" \
  --begin-time "2026010100" \
  --end-time "2026013123"

# 预览模式
python3 <SKILL_DIR>/scripts/callback_status_statistics.py \
  --sdk-app-id "1400006666" \
  --begin-time "2026010100" --end-time "2026013123" --dry-run
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --sdk-app-id | str | 是 | 短信 SdkAppId |
| --begin-time | str | 是 | 起始时间，格式 yyyymmddhh |
| --end-time | str | 是 | 结束时间，格式 yyyymmddhh，需 ≥ BeginTime 且区间 ≤ 32 天 |

### 10. 按手机号拉取下发状态 — `scripts/pull_send_status_by_phone.py`

按单个 E.164 手机号 + 时间区间拉取下发状态明细（SerialNo、ReportStatus、用户接收时间等）。

```bash
# 默认最近 24 小时
python3 <SKILL_DIR>/scripts/pull_send_status_by_phone.py \
  --sdk-app-id "1400006666" --phone-number "+8618501234444"

# 指定 UNIX 秒时间区间
python3 <SKILL_DIR>/scripts/pull_send_status_by_phone.py \
  --sdk-app-id "1400006666" --phone-number "+8618501234444" \
  --begin-time 1715000000 --end-time 1715086400

# 指定本地时间字符串
python3 <SKILL_DIR>/scripts/pull_send_status_by_phone.py \
  --sdk-app-id "1400006666" --phone-number "+8618501234444" \
  --begin-datetime "2026-05-01 00:00:00" \
  --end-datetime   "2026-05-02 00:00:00"
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --sdk-app-id | str | 是 | 短信 SdkAppId |
| --phone-number | str | 是 | E.164 格式手机号，必须以 `+` 开头（如 `+8618501234444`） |
| --begin-time / --end-time | int | 条件必填 | UNIX 秒时间区间；与 `--begin-datetime`/`--end-datetime` 互斥 |
| --begin-datetime / --end-datetime | str | 条件必填 | 本地时区字符串 `YYYY-MM-DD HH:MM:SS`；与上一组互斥。**未传任一组时默认最近 24 小时** |
| --limit | int | 否 | 返回数量上限，默认 100，最大 100 |
| --offset | int | 否 | 偏移量，默认 0 |

> 时间窗口限制：最多可拉取当前时间往前 7 天。

### 11. 按手机号拉取回复状态 — `scripts/pull_reply_status_by_phone.py`

按单个 E.164 手机号 + 时间区间拉取上行回复明细（SignName、ReplyContent、ReplyTime 等）。

```bash
# 默认最近 24 小时
python3 <SKILL_DIR>/scripts/pull_reply_status_by_phone.py \
  --sdk-app-id "1400006666" --phone-number "+8618501234444"

# 指定 UNIX 秒时间区间
python3 <SKILL_DIR>/scripts/pull_reply_status_by_phone.py \
  --sdk-app-id "1400006666" --phone-number "+8618501234444" \
  --begin-time 1715000000 --end-time 1715086400
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --sdk-app-id | str | 是 | 短信 SdkAppId |
| --phone-number | str | 是 | E.164 格式手机号，必须以 `+` 开头 |
| --begin-time / --end-time | int | 条件必填 | UNIX 秒时间区间；与 `--begin-datetime`/`--end-datetime` 互斥 |
| --begin-datetime / --end-datetime | str | 条件必填 | 本地时区字符串 `YYYY-MM-DD HH:MM:SS`；与上一组互斥。**未传任一组时默认最近 24 小时** |
| --limit | int | 否 | 返回数量上限，默认 100，最大 100 |
| --offset | int | 否 | 偏移量，默认 0 |

> 时间窗口限制：最多可拉取当前时间往前 7 天。

### 12. 分发群发模板 — `scripts/prepare_bulk_template.py`

把 Skill 内置的群发 Excel 模板**复制一份带时间戳的全新空白副本**到目标目录（**默认当前工作区 cwd，不是桌面**），生成后**作为附件下发给用户**。**每次群发都应调用此脚本**，避免直接使用 `assets/` 下原始模板（可能残留之前的填写数据）。

> **多 channel 设计**：用户可能通过各类聊天 channel 使用 Agent，这类环境没有「桌面」概念、也不能在服务端打开文件。因此脚本**默认生成到工作区且不自动打开**，由宿主以附件下发；**仅本地桌面端**才追加 `--open` 自动打开。

```bash
# 国内短信群发模板（默认生成到当前工作区，不自动打开 → 作为附件下发）
python3 <SKILL_DIR>/scripts/prepare_bulk_template.py --international 0

# 国际/港澳台短信群发模板
python3 <SKILL_DIR>/scripts/prepare_bulk_template.py --international 1

# 仅本地桌面端：复制后用系统默认程序打开 Excel
python3 <SKILL_DIR>/scripts/prepare_bulk_template.py --international 0 --open

# 用户显式指定目录（如桌面）
python3 <SKILL_DIR>/scripts/prepare_bulk_template.py \
  --international 0 --dest-dir "~/Desktop"
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --international | int | 否 | 0=国内短信（默认），1=国际/港澳台短信 |
| --dest-dir | str | 否 | 目标目录，**默认当前工作目录（工作区）**；仅在用户显式需要时指定（如 `~/Desktop`） |
| --open | flag | 否 | **仅本地桌面端使用**：复制后尝试用系统默认程序打开。默认不打开（聊天 channel 下应由宿主以附件下发） |

**输出 JSON 字段**：

| 字段 | 说明 |
|------|------|
| `source` | Skill 内置模板的绝对路径（仅用于审计） |
| `destination` | **复制后**新文件的绝对路径，**应作为附件直接发给用户** |
| `opened` | 是否成功调用系统命令打开（默认 false；仅在传 `--open` 且为桌面 GUI 环境时可能为 true） |
| `platform` | 当前系统：`darwin` / `linux` / `windows` |
| `international` | 模板对应的短信类型 |

## 输出格式 & 参考资料

### 输出格式

所有脚本成功时以 JSON 格式输出 API 返回结果，例如发送短信成功：

```json
{
  "SendStatusSet": [
    {
      "SerialNo": "5000:1045710669157053657849499619",
      "PhoneNumber": "+8618501234444",
      "Fee": 1,
      "Code": "Ok",
      "Message": "send success",
      "IsoCode": "CN",
      "SessionContext": ""
    }
  ],
  "RequestId": "a0aabda6-cf91-4f3e-a81f-9198114a2279"
}
```

预览模式输出（`--dry-run`）：

```json
{
  "dry_run": true,
  "api": "SendSms",
  "params": {
    "PhoneNumberSet": ["+8618501234444"],
    "SmsSdkAppId": "1400006666",
    "TemplateId": "1110",
    "SignName": "腾讯云",
    "TemplateParamSet": ["4370"]
  }
}
```

错误时输出结构化错误 JSON：

```json
{
  "error": "SMS_API_ERROR",
  "code": "AuthFailure.SecretIdNotFound",
  "message": "The SecretId is not found..."
}
```

### 何时继续读 references

- **遇到 API 错误，需要排查原因**：读 [error-codes.md](references/error-codes.md)
- **需要确认 API 频率限制、签名/模板/发送规格**：读 [api-limits.md](references/api-limits.md)
