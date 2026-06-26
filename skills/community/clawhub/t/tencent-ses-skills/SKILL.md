---
name: tencent-ses
description: >-
  腾讯云邮件推送(SES)服务技能，用于通过腾讯云 API 发送邮件。当用户提到"发送邮件"、"邮件推送"、"发邮件给"、
  "用某个地址给某人发送模板/邮件内容"时触发。支持完整的邮件发送工作流：
  (0) 检查 API 密钥配置并按安全配置指南引导用户完成子账号创建和密钥获取，
  (1) 解析用户指令并在信息缺失时引导用户查询已有资源或创建新资源，
  (2) 查询和验证发信域名，(3) 管理发信地址，
  (4) 使用模板或自定义内容发送邮件（自定义内容需先确认权限），
  (5) 自动查询邮件发送状态。
  当域名验证不通过或创建新域名时，自动启动"邮件域名认证向导"，引导用户完成 SPF/DKIM/DMARC/MX 配置，
  并通过全球 DNS 传播检测确认生效状态。
  当邮件发送出现认证失败时，自动执行"DNS 问题诊断器"，定位 DNS 配置问题并给出修复方案。
  也适用于用户询问"邮件发送状态"、"邮件是否送达"、"域名验证"、"DNS 配置"、"SPF/DKIM/DMARC"等场景。
  依赖环境变量 TENCENTCLOUD_SECRET_ID、TENCENTCLOUD_SECRET_KEY 和可选的 SES_REGION、SES_ENDPOINT。
---

# 腾讯云邮件推送（SES）Skill 使用指南

## 目录

- [产品简介](#产品简介)
- [快速开始](#快速开始)
  - [前提条件](#前提条件)
  - [环境变量](#环境变量)
  - [验证配置](#验证配置)
- [必须遵守的规则](#必须遵守的规则)
  - [密钥安全](#密钥安全)
  - [AI 行为约束](#ai-行为约束)
  - [输出规范](#输出规范)
- [使用示例](#使用示例)
  - [发送邮件](#发送邮件)
  - [查看域名和地址](#查看域名和地址)
  - [域名与 DNS 配置](#域名与-dns-配置)
  - [创建发信地址](#创建发信地址)
  - [模板管理](#模板管理)
  - [查看发送状态](#查看发送状态)
  - [故障排查](#故障排查)
- [脚本说明](#脚本说明)
- [邮件发送工作流](#邮件发送工作流)
  - [第 0 步：检查 API 密钥配置](#第-0-步检查-api-密钥配置)
  - [第 1 步：解析用户指令](#第-1-步解析用户指令)
  - [第 2 步：检查发信域名](#第-2-步检查发信域名)
  - [第 3 步：检查发信地址](#第-3-步检查发信地址)
  - [第 4 步：发送邮件](#第-4-步发送邮件)
  - [第 5 步：查询发送状态](#第-5-步查询发送状态)
- [域名认证向导](#域名认证向导)
  - [触发条件](#触发条件)
  - [主域名与非主域名](#主域名与非主域名)
  - [操作步骤](#操作步骤)
- [DNS 问题诊断器](#dns-问题诊断器)
  - [触发条件](#触发条件)
  - [诊断命令](#诊断命令)
  - [自动识别的问题模式](#自动识别的问题模式)
- [命令参考](#命令参考与示例)
  - [SES API 命令](#ses-api-命令)
  - [DNS 诊断命令](#dns-诊断命令)
- [相关文档](#相关文档)

---

## 产品简介

腾讯云邮件推送（Simple Email Service，SES）是一款基于云端的平台化邮件推送服务，为企业和开发者提供安全稳定、简单快速、精准高效的营销邮件、通知邮件和事务邮件的推送能力。

本 Skill 封装了腾讯云 SES 的核心 API，提供以下能力：

| 能力模块 | 说明 |
|----------|------|
| **域名管理** | 查询、创建、验证发信域名 |
| **地址管理** | 查询、创建发信地址 |
| **邮件发送** | 支持模板发送与自定义内容发送，支持抄送、密送、附件、退订链接等高级选项 |
| **状态查询** | 查询邮件投递与送达状态 |
| **模板管理** | 创建、更新、删除邮件模板 |
| **DNS 诊断** | SPF / DKIM / DMARC / MX 记录检查、CNAME 冲突检测与全球传播检测 |

---

## 快速开始

### 前提条件

使用本 Skill 前，请确保已完成以下准备工作：

| 步骤 | 操作 | 说明 |
|:---:|------|------|
| 1 | **创建腾讯云子账号** | 建议创建专用子账号并关联预设策略 `QcloudSESFullAccess`，详见 [安全配置指南](references/security_setup_guide.md) |
| 2 | **获取 API 密钥** | 为子账号生成 SecretId 和 SecretKey，并妥善保存 |
| 3 | **安装 Python SDK** | 执行 `pip install tencentcloud-sdk-python` |
| 4 | **配置环境变量** | 设置必需的密钥和可选的地域参数（详见下表） |

> ⚠️ **安全提醒**：请勿使用主账号密钥。务必创建专用子账号，关联预设策略 `QcloudSESFullAccess`，并建议配置 IP 访问限制。详见 [安全配置指南](references/security_setup_guide.md)。

### 环境变量

| 变量名 | 是否必填 | 默认值 | 说明 |
|--------|:--------:|--------|------|
| `TENCENTCLOUD_SECRET_ID` | ✅ | — | 腾讯云 API SecretId |
| `TENCENTCLOUD_SECRET_KEY` | ✅ | — | 腾讯云 API SecretKey |
| `SES_REGION` | 否 | `ap-guangzhou` | 服务地域，可选值：`ap-hongkong`、`ap-singapore` |
| `SES_ENDPOINT` | 否 | `ses.tencentcloudapi.com` | API 接入点，可选值：`ses.intl.tencentcloudapi.com` |

### 验证配置

环境变量配置完成后，执行以下命令验证连通性：

```bash
python3 ${SKILL_DIR}/scripts/ses_tool.py list-domains
```

若返回域名列表，则表示配置正确。若用户尚未提供密钥或验证失败，**必须按照 [安全配置指南](references/security_setup_guide.md) 中的步骤，逐步引导用户完成子账号创建、策略关联和 API 密钥获取**，不可笼统地要求用户"去配置密钥"。引导内容应包括：

1. 告知用户需要提供 **SecretId** 和 **SecretKey** 两个值
2. 说明应创建**专用子账号**（而非使用主账号密钥），关联预设策略 `QcloudSESFullAccess`
3. 建议配置 **IP 访问限制**，参考 [限制 IP 访问](https://cloud.tencent.com/document/product/598/38037)
4. 提醒 SecretKey **仅在创建时显示一次**，需立即保存
5. 提供控制台链接：[用户列表](https://console.cloud.tencent.com/cam)

---


## 必须遵守的规则

### 密钥安全

- 禁止将 SecretId、SecretKey 硬编码到代码或工作区文件中
- 群聊场景：禁止让用户直接发送密钥
- 私聊场景：提醒"密钥会经过 LLM，存在泄漏风险"
- **最小权限原则**：建议使用 CAM 子账号，关联预设策略 `QcloudSESFullAccess`，并配置 IP 访问限制
- **密钥轮换建议**：定期轮换 API 密钥（建议每 90 天），避免长期使用同一密钥

### AI 行为约束

- **只调用本 Skill 封装的脚本**：禁止直接用 Python SDK 或 curl 调用未封装的腾讯云 API。如需调用本 Skill 未封装的接口，必须先告知用户"该接口暂未封装"，并建议前往 [SES 控制台](https://console.cloud.tencent.com/ses) 操作
- **域名/模板 ID 必须来自真实查询**：禁止编造或猜测域名名称、模板 ID 等标识符。查询域名/模板列表时，应先用 `ses_tool.py list-domains` 或 `ses_tool.py list-templates` 获取真实数据，不得随意填写
- **先预览后执行（`--dry-run`）**：对写入类操作（发送邮件、创建域名、创建发信地址、创建/删除模板），**必须**先使用 `--dry-run` 参数执行预览，将输出的请求参数展示给用户确认后，再去掉 `--dry-run` 正式执行。`--dry-run` 不会调用 API，仅验证参数并输出 JSON 格式的请求预览
- **定时/批量任务必须确认**：设置定时发送或批量邮件时，即使已做预览，仍需明确告知用户发件地址、收件人数、发送内容，并等待用户确认后再执行
- **域名须先验证后使用**：发信域名的 DNS 记录（SPF/DKIM/DMARC/MX）必须验证通过后才能用于发送邮件，验证状态通过 `ses_tool.py list-domains` 查询确认

### 输出规范

- **结构化输出**：所有脚本以 JSON 格式输出结果到 stdout，日志信息输出到 stderr
- **错误如实返回**：脚本失败时必须返回错误信息，不得猜测或伪造结果

---


## 使用示例

> 💡 以下示例展示了如何通过自然语言完成各类邮件操作，无需手动输入命令。

### 发送邮件

| 自然语言示例 | 说明 |
|-------------|------|
| "用 noreply@example.com 给 zhangsan@gmail.com 发一封欢迎邮件，用模板 251254620" | 使用指定模板发送邮件 |
| "用 noreply@example.com 给 a@qq.com、b@gmail.com、c@163.com 发送模板 251254620，主题是「活动邀请」" | 使用模板批量发送邮件 |
| "用 support@example.com 给 user@gmail.com 发一封邮件，内容是：您好，您的工单已处理完毕" | 使用自定义文本内容发送邮件 ⚠️ 须先确认权限 |
| "用 noreply@example.com 给 boss@company.com 发邮件，主题「月度报告」，内容是一段 HTML，抄送给 hr@company.com" | 发送 HTML 邮件并抄送 ⚠️ 须先确认权限 |
| "发邮件给 test@qq.com，附件是 /data/reports/report.pdf" | 发送带附件的邮件 |

> ⚠️ 自定义内容发送功能仅支持部分已申请特殊配置的客户使用。当用户请求使用自定义内容发送邮件时，**必须先向用户确认是否已开通该权限**，未确认前不得执行发送。如未开通，请引导用户联系腾讯云 SES 团队申请开通权限，或改为使用模板方式发送。

### 查看域名和地址

| 自然语言示例 | 说明 |
|-------------|------|
| "帮我看看现在有哪些发信域名" | 列出所有域名及其验证状态 |
| "example.com 这个域名的 DNS 配置情况怎么样？" | 查看域名的 SPF / DKIM / DMARC / MX 配置详情 |
| "列出所有发信地址" | 查看当前账号下的所有发信地址 |

### 域名与 DNS 配置

| 自然语言示例 | 说明 |
|-------------|------|
| "我想用 mail.example.com 来发邮件，帮我创建这个域名" | 创建发信域名并引导完成 DNS 配置 |
| "帮我检查一下 example.com 的 DNS 配置有没有问题" | 全面诊断 SPF / DKIM / DMARC / MX 记录 |
| "example.com 的 SPF 记录配对了吗？" | 单独检查 SPF 记录 |
| "我已经配好 DNS 了，帮我验证一下 mail.example.com" | 提交域名验证请求 |
| "帮我看看 example.com 的 DNS 在全球传播了没有" | 检测多节点 DNS 传播状态 |

### 创建发信地址

| 自然语言示例 | 说明 |
|-------------|------|
| "帮我创建一个发信地址 hello@example.com" | 创建不带别名的发信地址 |
| "创建发信地址 support@example.com，显示名称叫「客服中心」" | 收件人将看到"客服中心 \<support@example.com\>" |

### 模板管理

| 自然语言示例 | 说明 |
|-------------|------|
| "帮我看看有哪些邮件模板" | 列出模板列表（名称、ID、审核状态） |
| "查看模板 251254620 的详细内容" | 展示模板的 HTML 内容 |
| "帮我创建一个欢迎邮件模板，内容是：您好 \{\{name\}\}，欢迎注册！" | 创建支持变量替换的模板 |
| "把模板 251254620 的内容改成新版本" | 更新已有模板 |
| "删掉模板 251254620" | 删除指定模板 |

### 查看发送状态

| 自然语言示例 | 说明 |
|-------------|------|
| "刚才发的那封邮件送到了吗？" | 自动使用上次的 MessageId 查询投递状态 |
| "帮我查一下消息 ID 是 qcloudses-xxx 的邮件状态" | 查询指定邮件的送达情况 |

### 故障排查

| 自然语言示例 | 说明 |
|-------------|------|
| "域名验证失败了，帮我查查原因" | 自动诊断域名认证与 DNS 配置问题 |
| "SPF 验证一直不通过怎么办？" | 针对性诊断 SPF 记录问题并给出修复方案 |
| "DKIM 配置好了但还是报错" | 检查 DKIM 密钥是否匹配、格式是否正确 |

---

## 脚本说明

本 Skill 提供两个核心脚本工具：

| 脚本 | 路径 | 功能说明 | 是否依赖 AKSK |
|------|------|----------|:------------:|
| **SES 管理工具** | `${SKILL_DIR}/scripts/ses_tool.py` | 调用腾讯云 SES API，完成邮件发送全流程 | ✅ |
| **DNS 诊断工具** | `${SKILL_DIR}/scripts/dns_checker.py` | 检测 DNS 记录配置与全球传播状态 | 否 |

```bash
# SES API 操作
python3 ${SKILL_DIR}/scripts/ses_tool.py <command> [options]

# DNS 诊断（无需 AKSK，直接查询公共 DNS）
python3 ${SKILL_DIR}/scripts/dns_checker.py <command> [options]
```

> 💡 **全局选项 `--dry-run`**：所有写入类命令（`send-template`、`send-simple`、`create-domain`、`create-address`、`create-template`、`update-template`、`delete-template`）均支持 `--dry-run` 参数。启用后仅验证参数并输出 JSON 格式的请求预览，不实际调用 API。

---

## 邮件发送工作流

当用户请求发送邮件时（例如"用 xxx@domain.com 给 yyy@example.com 发送模板 12345"），系统按以下流程执行：

```
┌──────────────────────────────────────────────────────────────┐
│  第 0 步：检查 API 密钥配置                                    │
│  ├─ 环境变量已配置且验证通过 → 继续第 1 步                     │
│  └─ 未配置或验证失败 → 引导用户提供 SecretId 和 SecretKey      │
│      ├─ 引导用户参照安全配置指南完成子账号创建和密钥获取        │
│      └─ 用户提供密钥后，配置环境变量并验证连通性                │
└────────────────────────────┬─────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  第 1 步：解析用户指令（发信地址 / 收件人 / 内容 / 主题）       │
└────────────────────────────┬─────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  第 2 步：检查发信域名是否已通过验证                           │
│  ├─ 已验证 → 继续                                            │
│  ├─ 未验证 → 启动域名认证向导                                 │
│  └─ 不存在 → 创建域名 → 启动域名认证向导                      │
└────────────────────────────┬─────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  第 3 步：检查发信地址是否存在，不存在则自动创建                 │
└────────────────────────────┬─────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  第 3.5 步（仅自定义内容）：确认客户是否具有自定义内容发送权限  │
│  ├─ 使用模板发送 → 跳过此步，直接进入第 4 步                   │
│  ├─ 使用自定义内容 → 主动询问用户是否已开通权限                 │
│  │   ├─ 用户确认已开通 → 继续第 4 步                           │
│  │   └─ 用户未开通/不确定 → ❌ 终止发送                        │
│  │       ├─ 建议联系腾讯云 SES 团队申请开通权限                 │
│  │       └─ 或改用模板方式发送                                  │
└────────────────────────────┬─────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  第 4 步：发送邮件（模板发送 / 自定义内容发送）                 │
└────────────────────────────┬─────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  第 5 步：等待约 1 分钟后查询发送状态，向用户汇报结果           │
└──────────────────────────────────────────────────────────────┘
```

### 第 0 步：检查 API 密钥配置

在执行任何邮件发送操作之前，**必须先确认 API 密钥（SecretId / SecretKey）已正确配置**。这是调用腾讯云 SES API 的前提条件。

#### 检查方式

通过执行以下命令验证密钥是否已配置且可用：

```bash
python3 ${SKILL_DIR}/scripts/ses_tool.py list-domains
```

#### 密钥未配置时的处理流程

如果环境变量 `TENCENTCLOUD_SECRET_ID` 或 `TENCENTCLOUD_SECRET_KEY` 未设置，或命令执行返回认证错误，**必须引导用户提供密钥**，流程如下：

1. **告知用户需要提供 API 密钥**，向用户说明：
   > "使用邮件推送功能需要配置腾讯云 API 密钥（SecretId 和 SecretKey）。请提供您的 SecretId 和 SecretKey，我来帮您完成配置。"

2. **引导用户安全地获取密钥**，按照 [安全配置指南](references/security_setup_guide.md) 中的步骤，为用户提供清晰的指引：

   | 步骤 | 操作 | 说明 |
   |:---:|------|------|
   | 1 | **创建专用子账号** | 前往 [用户列表](https://console.cloud.tencent.com/cam) 创建子账号（如 `ses-skill-sender`），勾选 **编程访问**，关联预设策略 `QcloudSESFullAccess` |
   | 2 | **配置 IP 访问限制** | （推荐）新建自定义策略限制 IP 访问，详见 [安全配置指南](references/security_setup_guide.md) 及 [限制 IP 访问](https://cloud.tencent.com/document/product/598/38037) |
   | 3 | **生成 API 密钥** | 在子账号详情页的 **API 密钥** 页签创建密钥，**SecretKey 仅在创建时显示一次**，请务必立即保存 |

   > ⚠️ **安全提醒**：
   > - **请勿使用主账号密钥**。主账号拥有所有云资源的完整操作权限，一旦泄露可能导致严重安全风险和经济损失。
   > - 建议创建专用子账号，关联预设策略 `QcloudSESFullAccess`，并配置 **IP 访问限制**。
   > - 密钥应通过环境变量配置，**严禁明文存储**于代码、配置文件或版本控制系统中。
   > - 建议每 90 天轮换一次密钥，降低泄露风险。
   > - 详细的安全配置步骤请参考 [安全配置指南](references/security_setup_guide.md)。

3. **用户提供密钥后，配置环境变量**：

   ```bash
   export TENCENTCLOUD_SECRET_ID="<用户提供的 SecretId>"
   export TENCENTCLOUD_SECRET_KEY="<用户提供的 SecretKey>"
   ```

4. **验证连通性**：

   ```bash
   python3 ${SKILL_DIR}/scripts/ses_tool.py list-domains
   ```

   - 返回域名列表 → 配置成功，继续第 1 步。
   - 返回认证错误 → 提示用户检查密钥是否正确，或确认子账号权限是否包含 SES 相关操作。

**此步骤为强制前置条件。未完成密钥配置前，不得执行任何后续邮件发送操作。**

### 第 1 步：解析用户指令

从用户消息中提取以下关键信息：

| 字段 | 来源 | 示例 |
|------|------|------|
| 发信地址（From） | 用户说的"用 xxx" | `noreply@mail.example.com` |
| 收件人地址（To） | 用户说的"给 yyy" | `user@gmail.com` 或多人 `a@x.com,b@x.com` |
| 发送内容 | 模板 ID + 参数，或 HTML / 文本内容 | 模板 `12345`，或自定义 HTML |
| 邮件主题 | 用户指定，或根据内容自动生成 | `欢迎注册` |

#### 信息缺失时的引导

当用户首次表达发送邮件意图，但**未提供发信地址、收件人、发送内容等关键信息**时，不要直接报错或猜测，而是**主动引导用户补充信息**：

1. **提示用户可通过本 Skill 查询当前账号下的资源**，例如：
   - "帮我查看当前有哪些发信域名"
   - "帮我看一下账号下有哪些发信地址"
   - "帮我查一下现有的邮件模板"

2. **提供腾讯云 SES 控制台链接**，方便用户自行查看和管理：

   | 资源类型 | 控制台链接 |
   |----------|-----------|
   | 发信域名 | https://console.cloud.tencent.com/ses/domain |
   | 发信地址 | https://console.cloud.tencent.com/ses/address |
   | 发信模板 | https://console.cloud.tencent.com/ses/template |

3. **引导话术示例**：
   > "我可以帮您查看当前账号下已有的发信域名、发信地址和邮件模板，方便您选择使用。例如您可以说：
   > - '帮我查看当前有哪些发信域名'
   > - '帮我看一下账号下有哪些发信地址'
   > - '帮我查一下现有的邮件模板'
   >
   > 您也可以前往腾讯云 SES 控制台直接查看：
   > - 发信域名：https://console.cloud.tencent.com/ses/domain
   > - 发信地址：https://console.cloud.tencent.com/ses/address
   > - 发信模板：https://console.cloud.tencent.com/ses/template
   >
   > 请告诉我您要用哪个发信地址发送？发给谁？使用模板还是自定义内容？"

4. **资源不存在时的创建指引**：

   当查询后发现用户账号下**缺少所需资源**（无发信域名、无发信地址、无可用模板）时，需同时提供**腾讯云官方文档链接**和**本 Skill 的创建命令说明**，帮助用户快速创建：

   | 缺少的资源 | 官方创建指引文档 | Skill 创建方式 |
   |-----------|-----------------|---------------|
   | 发信域名 | [创建发信域名](https://cloud.tencent.com/document/product/1288/55191) | 告诉我要创建的域名，如"帮我创建发信域名 mail.example.com"，创建后会自动引导完成 DNS 验证配置 |
   | 发信地址 | [创建发信地址](https://cloud.tencent.com/document/product/1288/55192) | 告诉我要创建的地址，如"帮我创建发信地址 noreply@mail.example.com"，可选指定显示名称 |
   | 邮件模板 | [创建邮件模板](https://cloud.tencent.com/document/product/1288/55193) | 告诉我模板名称和内容，如"帮我创建一个欢迎邮件模板"，支持 HTML 和纯文本格式，支持 `{{变量名}}` 语法 |

   **引导话术示例**（以缺少发信域名为例）：
   > "当前账号下还没有已验证的发信域名。您可以：
   > 1. **通过本 Skill 创建**：告诉我您想使用的域名，例如"帮我创建发信域名 mail.example.com"，我会帮您创建并引导完成 DNS 验证配置。
   > 2. **在控制台手动创建**：前往 [SES 控制台 - 发信域名](https://console.cloud.tencent.com/ses/domain) 操作，详细步骤可参考 [创建发信域名文档](https://cloud.tencent.com/document/product/1288/55191)。"

从发信地址中提取**域名部分**（`@` 后的部分），用于后续域名检查。

### 第 2 步：检查发信域名

```bash
python3 ${SKILL_DIR}/scripts/ses_tool.py list-domains
```

根据域名状态执行对应操作：

| 域名状态 | 执行操作 |
|----------|----------|
| 存在且已验证（`SendingEnabled=true`） | 继续第 3 步 |
| 存在但未验证 | 启动 [域名认证向导](#域名认证向导) |
| 不存在 | 先创建域名，再启动 [域名认证向导](#域名认证向导) |

### 第 3 步：检查发信地址

```bash
python3 ${SKILL_DIR}/scripts/ses_tool.py list-addresses
```

- 地址已存在 → 继续第 4 步。
- 地址不存在 → 自动创建：

```bash
python3 ${SKILL_DIR}/scripts/ses_tool.py create-address <email> [别名]
```

### 第 4 步：发送邮件

根据用户提供的内容类型，选择对应的发送方式。

> ⚠️ **自定义内容发送权限确认（强制拦截）**
>
> 当用户请求使用**自定义内容**（即非模板方式）发送邮件时，**必须先向用户确认是否已开通自定义内容发送权限**，再执行发送操作。具体流程如下：
>
> 1. **识别发送方式**：如果用户提供的是自定义 HTML 或纯文本内容（而非模板 ID），则判定为自定义内容发送。
> 2. **主动询问权限**：向用户发出确认提示，例如：
>    > "自定义内容发送功能仅支持已申请特殊配置的客户使用。请确认您是否已开通该权限？如果未开通，建议您：
>    > - 联系腾讯云 SES 团队申请开通自定义内容发送权限
>    > - 或改为使用邮件模板进行发送（可通过 `list-templates` 查看可用模板）"
> 3. **根据用户回复决定后续操作**：
>    - 用户**确认已开通** → 继续执行 `send-simple` 发送流程。
>    - 用户**表示未开通或不确定** → **终止发送**，并引导用户联系开通权限或使用模板发送。
>
> **此确认步骤为强制要求，不可跳过。未经用户明确确认权限，禁止执行 `send-simple` 命令。**

#### 方式一：模板发送

> `<to>` 参数支持逗号分隔的多个收件人地址，单次最多 50 人。

```bash
python3 ${SKILL_DIR}/scripts/ses_tool.py send-template \
  "<from>" "<to1>,<to2>,..." "<subject>" <template_id> ['<template_data_json>'] \
  [--cc ...] [--bcc ...] [--reply-to ...] [--attachments ...] [--unsubscribe ...] [--trigger-type ...]
```

#### 方式二：自定义内容发送

> ⚠️ **限制说明**：自定义内容发送功能仅支持部分已申请特殊配置的客户使用。**在执行以下命令前，必须已完成上方的权限确认流程，且用户明确表示已开通权限。** 如用户未开通权限，请勿执行 `send-simple` 命令，应引导用户联系腾讯云 SES 团队申请开通或改用模板发送。

```bash
# HTML 内容
python3 ${SKILL_DIR}/scripts/ses_tool.py send-simple \
  "<from>" "<to1>,<to2>,..." "<subject>" "<html_content>" \
  [--cc ...] [--bcc ...] [--reply-to ...] [--attachments ...] [--unsubscribe ...] [--trigger-type ...]

# 纯文本内容
python3 ${SKILL_DIR}/scripts/ses_tool.py send-simple \
  "<from>" "<to1>,<to2>,..." "<subject>" "<text_content>" --text \
  [--cc ...] [--bcc ...] [--reply-to ...] [--attachments ...] [--unsubscribe ...] [--trigger-type ...]
```

#### 发送选项一览

`send-template` 和 `send-simple` 均支持以下可选参数：

| 选项 | 说明 | 取值 / 格式 |
|------|------|-------------|
| `--cc <emails>` | 抄送人地址（逗号分隔） | 最多 20 人 |
| `--bcc <emails>` | 密送人地址（逗号分隔） | 最多 20 人，不可与收件人重复 |
| `--reply-to <email>` | 回复地址 | 单个邮箱地址 |
| `--attachments <paths>` | 附件文件路径（逗号分隔） | 总大小 ≤ 4 MB |
| `--unsubscribe <0-11>` | 退订链接语言 | 0=不加 1=简中 2=英文 3=繁中 4=西班牙 5=法语 6=德语 7=日语 8=韩语 9=阿拉伯 10=泰语 11=马来语 |
| `--trigger-type <0\|1>` | 邮件触发类型 | 0=营销类 1=触发类（验证码等即时邮件） |
| `--dry-run` | 预览模式：仅验证参数并输出 JSON 请求预览，不调用 API | 无参数值，直接添加即可 |

#### 重要说明

- `FromEmailAddress` 支持别名格式：`别名 <email@domain.com>`，别名和 `<` 之间须有空格。
- `Destination`、`Cc`、`Bcc` 三个收件参数中**至少需填写一个**。
- 附件总大小须控制在 4 MB 以内（Base64 编码后请求包不超过 8 MB）。
- **频率限制**：同一发信地址在一小时内向同一收件地址发送邮件的封数超过上限时，将触发 `FailedOperation.FrequencyLimit` 错误。批量发送场景建议拉大发送间隔或使用 `BatchSendEmail` 接口。

### 第 5 步：查询发送状态

发送成功后，记录返回的 `MessageId`，等待约 1 分钟后查询状态：

```bash
python3 ${SKILL_DIR}/scripts/ses_tool.py get-status "<message_id>" "<YYYY-MM-DD>"
```

> 日期参数为邮件发送当天的日期，查询仅支持近 30 天内的记录。

向用户汇报腾讯云处理状态（SendStatus）和收件方处理状态（DeliverStatus）。

---

## 域名认证向导

当发信域名未通过验证或新创建域名时，系统将自动触发本向导，引导用户完成 SPF / DKIM / DMARC / MX 的 DNS 配置。

### 触发条件

满足以下任一条件即触发域名认证向导：

1. `verify-domain` 返回验证未通过。
2. `create-domain` 成功后需要配置 DNS。
3. 用户主动请求域名验证或 DNS 检查。
4. 邮件发送失败，错误码为 `3014`（发件域名未认证）。

### 主域名与非主域名

配置 DNS 记录前，需先判断发信域名是**主域名**还是**非主域名（子域名）**，两者在主机记录的填写方式上存在差异：

| 域名类型 | 示例 | 主机记录填写规则 |
|----------|------|------------------|
| **主域名** | `example.com` | 使用标准前缀：`@`、`qcloud._domainkey`、`_dmarc` |
| **非主域名** | `abc.example.com` | 在标准前缀后追加子域名前缀：`abc`、`qcloud._domainkey.abc`、`_dmarc.abc` |

### 操作步骤

#### 步骤一：获取所需 DNS 记录

```bash
python3 ${SKILL_DIR}/scripts/ses_tool.py get-domain <domain>
```

记录返回的 `Attributes` 中每条 DNS 配置的记录类型、域名、期望值和当前状态。

#### 步骤二：运行 DNS 综合诊断

```bash
python3 ${SKILL_DIR}/scripts/dns_checker.py check-all <domain>
```

该命令将执行以下检查项：

| 检查项 | 检查内容 |
|--------|----------|
| CNAME 冲突 | 检测域名及其子域名（DKIM / DMARC）是否存在 CNAME 记录冲突 |
| SPF | 记录是否存在、语法正确性、include 列表、DNS Lookup 次数（上限 10 次）、~all 策略 |
| DKIM | selector 对应记录是否存在、密钥长度、格式是否正确（仅支持 TXT 模式，不支持 CNAME 模式） |
| DMARC | 策略等级（none / quarantine / reject）、报告地址、对齐模式 |
| MX | 邮件交换记录指向是否正确 |

> ⚠️ **CNAME 冲突检测说明**：根据 DNS 协议（RFC1034 / RFC2181），CNAME 记录具有最高优先级，会与 TXT / MX 等记录类型冲突，导致腾讯云 SES 域名验证失败。如诊断工具检测到 CNAME 冲突，须先删除相关 CNAME 记录，再配置正确的 TXT / MX 记录。详见 [DNS 配置指南 - CNAME 记录冲突说明](references/dns_guide.md#9-cname-记录冲突说明)。

#### 步骤三：提供修复方案

根据步骤一和步骤二的检查结果，结合主域名 / 非主域名的区别，为每个未通过的检查项生成修复指引。

**主域名配置表（以 `example.com` 为例）**：

| 记录类型 | 主机记录 | 记录值 |
|----------|----------|--------|
| MX | `@` | `mxbiz1.qq.com.`（末尾须有 `.`） |
| TXT（SPF） | `@` | `v=spf1 include:qcloudmail.com ~all` |
| TXT（DKIM） | `qcloud._domainkey` | `v=DKIM1; k=rsa; p=MIGf...`（从腾讯云控制台获取） |
| TXT（DMARC） | `_dmarc` | `v=DMARC1; p=none` |

**非主域名配置表（以 `abc.example.com` 为例）**：

| 记录类型 | 主机记录 | 记录值 |
|----------|----------|--------|
| MX | `abc` | `mxbiz1.qq.com.`（末尾须有 `.`） |
| TXT（SPF） | `abc` | `v=spf1 include:qcloudmail.com ~all` |
| TXT（DKIM） | `qcloud._domainkey.abc` | `v=DKIM1; k=rsa; p=MIGf...`（从腾讯云控制台获取） |
| TXT（DMARC） | `_dmarc.abc` | `v=DMARC1; p=none` |

**常见问题修复指引**：

| 记录类型 | 常见问题 | 修复方式 |
|----------|----------|----------|
| CNAME 冲突 | 域名或子域名存在 CNAME 记录 | 删除 CNAME 记录后再添加 TXT / MX 记录，或使用其他子域名作为发信域名 |
| SPF | 完全缺失 | 新增完整的 SPF TXT 记录 |
| SPF | 存在但缺少 `include:qcloudmail.com` | 将 `include:qcloudmail.com` 合并到已有 SPF 记录中 |
| SPF | DNS Lookup 超过 10 次 | 使用 SPF Flattening 技术优化 |
| SPF | 存在多条 SPF 记录 | 合并为一条（RFC 规范要求每个域名仅保留一条 SPF 记录） |
| DKIM | 已配置为 CNAME 模式 | 腾讯云 SES 不支持 CNAME 模式验证 DKIM，须删除 CNAME 记录并改为 TXT 记录 |
| DKIM | 密钥不匹配 | 替换为腾讯云提供的 RSA 公钥 |
| DKIM | 密钥长度不足 | 建议升级至 2048 bit |
| DMARC | 缺失 | 新增 `v=DMARC1; p=none` |
| DMARC | 策略为 none | 建议按 none → quarantine → reject 路径渐进升级 |
| MX | 记录缺失 | 新增 MX 记录，指向 `mxbiz1.qq.com.` |

#### 步骤四：检测 DNS 传播状态

用户确认已完成 DNS 配置后，执行全球传播检测：

```bash
# SPF 传播检测
python3 ${SKILL_DIR}/scripts/dns_checker.py check-propagation <domain> TXT

# DKIM 传播检测
python3 ${SKILL_DIR}/scripts/dns_checker.py check-propagation <domain> TXT qcloud._domainkey

# DMARC 传播检测
python3 ${SKILL_DIR}/scripts/dns_checker.py check-propagation <domain> TXT _dmarc

# MX 传播检测
python3 ${SKILL_DIR}/scripts/dns_checker.py check-propagation <domain> MX
```

向用户展示各 DNS 节点（Google、Cloudflare、AliDNS、DNSPod）的传播状态。若部分节点尚未生效，建议等待 4 ~ 8 小时后重新检测。

也可使用 `dig` 命令快速验证（以 `example.com` 为例）：

```bash
dig mx +short example.com
dig txt +short example.com
dig txt +short _dmarc.example.com
dig txt +short qcloud._domainkey.example.com
```

> ⚠️ 若使用 DNSPod 注册域名但 `dig` 查询无结果，可能是域名实名认证未通过（注册局设置暂停解析）。

#### 步骤五：提交域名验证

DNS 记录全部传播生效后，向腾讯云提交验证请求：

```bash
python3 ${SKILL_DIR}/scripts/ses_tool.py verify-domain <domain>
```

- 验证通过 → 告知用户域名可用于发信。
- 验证未通过 → 返回步骤二重新诊断。

---

## DNS 问题诊断器

当邮件发送出现认证失败或用户主动请求 DNS 诊断时，系统将自动触发 DNS 问题诊断器。

### 触发条件

| 触发场景 | 说明 |
|----------|------|
| 用户主动请求 | "检查 DNS"、"诊断域名"、"SPF 验证失败"等 |
| 认证类错误 | 邮件发送返回状态码 `3014`（发件域名未认证） |
| 验证反复失败 | `verify-domain` 多次返回未通过 |

### 诊断命令

```bash
# 全面诊断（推荐）
python3 ${SKILL_DIR}/scripts/dns_checker.py diagnose <domain>

# 针对特定问题诊断
python3 ${SKILL_DIR}/scripts/dns_checker.py diagnose <domain> "SPF验证失败"

# 单项检查
python3 ${SKILL_DIR}/scripts/dns_checker.py check-spf <domain>
python3 ${SKILL_DIR}/scripts/dns_checker.py check-dkim <domain> [selector]
python3 ${SKILL_DIR}/scripts/dns_checker.py check-dmarc <domain>
python3 ${SKILL_DIR}/scripts/dns_checker.py check-mx <domain>
```

### 自动识别的问题模式

| 问题类型 | 自动建议 |
|----------|----------|
| CNAME 记录冲突 | 检测到 CNAME 与 TXT / MX 记录冲突，提示删除 CNAME 记录 |
| DKIM 配置为 CNAME 模式 | 腾讯云 SES 不支持 CNAME 模式验证 DKIM，提示改为 TXT 记录 |
| SPF DNS Lookup 超过 10 次 | 建议使用 SPF Flattening 展开 include |
| DKIM 密钥不匹配 | 对比期望值与当前值，提供正确的记录值 |
| DKIM 密钥长度不足 | 建议升级至 2048 bit |
| DMARC 策略为 none | 提供 none → quarantine → reject 渐进升级路径 |
| 多个 ESP 的 SPF include 冲突 | 提供合并后的 SPF 记录方案 |
| SPF 记录超过 255 字符 | 建议拆分为多个字符串或使用 Flattening |
| DNS 部分地区未生效 | 检查 TTL 设置，建议等待或更换 DNS 服务商 |
| 存在多条 SPF 记录 | 提示合并为单条（RFC 规范要求） |
| DMARC 缺少 rua 报告地址 | 建议添加聚合报告接收地址 |

---

## 命令参考与示例

### SES API 命令

以下命令均通过 `ses_tool.py` 执行，须提前配置 AKSK 环境变量。

#### 域名管理

| 命令 | 说明 |
|------|------|
| `list-domains` | 获取当前账号下所有发信域名列表 |
| `get-domain <domain>` | 获取指定域名的详细配置信息（含 DNS 记录要求） |
| `create-domain <domain>` | 创建新的发信域名 |
| `verify-domain <domain>` | 向腾讯云提交域名验证请求 |

**示例**：

```bash
# 列出所有发信域名及其验证状态
python3 ${SKILL_DIR}/scripts/ses_tool.py list-domains

# 查看 example.com 的 DNS 配置详情（SPF / DKIM / DMARC / MX 的期望值与当前状态）
python3 ${SKILL_DIR}/scripts/ses_tool.py get-domain example.com

# 创建新域名
python3 ${SKILL_DIR}/scripts/ses_tool.py create-domain mail.example.com

# DNS 配置完成后提交验证请求
python3 ${SKILL_DIR}/scripts/ses_tool.py verify-domain mail.example.com
```

#### 地址管理

| 命令 | 说明 |
|------|------|
| `list-addresses` | 获取所有发信地址列表 |
| `create-address <email> [name]` | 创建发信地址，可选指定显示名称 |

**示例**：

```bash
# 列出所有发信地址
python3 ${SKILL_DIR}/scripts/ses_tool.py list-addresses

# 创建发信地址（不带显示名称）
python3 ${SKILL_DIR}/scripts/ses_tool.py create-address noreply@example.com

# 创建发信地址（带显示名称，发出的邮件将显示为"客服中心 <support@example.com>"）
python3 ${SKILL_DIR}/scripts/ses_tool.py create-address support@example.com "客服中心"
```

#### 邮件发送

| 命令 | 说明 |
|------|------|
| `send-template <from> <to> <subject> <tid> [data] [options]` | 使用模板发送邮件（`to` 支持逗号分隔多收件人，最多 50 人） |
| `send-simple <from> <to> <subject> <content> [--text] [options]` | 使用自定义内容发送邮件 ⚠️ 须先确认用户已开通权限 |
| `get-status <msg_id> <date>` | 查询邮件发送状态（日期格式：`YYYY-MM-DD`） |

**示例 — 模板发送**：

```bash
# 基础模板发送（无模板参数）
python3 ${SKILL_DIR}/scripts/ses_tool.py send-template \
  "noreply@example.com" "user@gmail.com" "欢迎注册" 251254620

# 带模板参数的发送（模板中使用 {{name}} 等变量）
python3 ${SKILL_DIR}/scripts/ses_tool.py send-template \
  "noreply@example.com" "user@gmail.com" "订单确认" 251254620 \
  '{"name":"张三","order_id":"20260407001"}'

# 完整选项示例：抄送 + 密送 + 回复地址 + 附件 + 泰语退订链接 + 营销类邮件
python3 ${SKILL_DIR}/scripts/ses_tool.py send-template \
  "noreply@example.com" "user@gmail.com" "活动邀请" 251254620 \
  '{"event":"2026开发者大会"}' \
  --cc "manager@company.com,hr@company.com" \
  --bcc "archive@company.com" \
  --reply-to "reply@example.com" \
  --attachments "/path/to/invite.pdf,/path/to/agenda.docx" \
  --unsubscribe 10 \
  --trigger-type 0
```

**示例 — 预览模式（`--dry-run`）**：

```bash
# 预览模板邮件发送参数（不实际调用 API）
python3 ${SKILL_DIR}/scripts/ses_tool.py send-template \
  "noreply@example.com" "user@gmail.com" "欢迎注册" 251254620 \
  '{"name":"张三"}' --dry-run

# 预览创建域名（不实际调用 API）
python3 ${SKILL_DIR}/scripts/ses_tool.py create-domain mail.example.com --dry-run

# 预览删除模板（不实际调用 API）
python3 ${SKILL_DIR}/scripts/ses_tool.py delete-template 251254620 --dry-run
```

**示例 — 自定义内容发送**（⚠️ 仅支持已申请特殊配置的客户，执行前须确认用户已开通权限）：

```bash
# 发送 HTML 内容
python3 ${SKILL_DIR}/scripts/ses_tool.py send-simple \
  "noreply@example.com" "user@gmail.com" "系统通知" \
  "<h1>您好</h1><p>您的账户已激活。</p>"

# 发送纯文本内容
python3 ${SKILL_DIR}/scripts/ses_tool.py send-simple \
  "noreply@example.com" "user@gmail.com" "验证码" \
  "您的验证码是 123456，5 分钟内有效。" --text \
  --trigger-type 1

# 使用别名格式的发信地址
python3 ${SKILL_DIR}/scripts/ses_tool.py send-simple \
  "客服中心 <support@example.com>" "user@gmail.com" "工单回复" \
  "<p>您的工单 #1024 已处理完毕。</p>" \
  --reply-to "support@example.com"

# 带附件和英文退订链接
python3 ${SKILL_DIR}/scripts/ses_tool.py send-simple \
  "noreply@example.com" "user@gmail.com" "月度报告" \
  "<p>请查收附件中的月度报告。</p>" \
  --attachments "/data/reports/monthly_report.pdf" \
  --unsubscribe 2
```

**示例 — 查询发送状态**：

```bash
# 查询指定 MessageId 在 2026-04-07 的投递状态
python3 ${SKILL_DIR}/scripts/ses_tool.py get-status \
  "qcloudses-30-251200670-date-20260407150416-VYA4g7c2kPEq1" "2026-04-07"
```

#### 模板管理

| 命令 | 说明 |
|------|------|
| `list-templates [--offset N] [--limit N] [--status 0\|1\|2]` | 获取模板列表（支持分页与状态筛选：0=已通过 1=待审核 2=已拒绝） |
| `get-template <id>` | 获取模板详细内容 |
| `create-template <name> <html_or_text> [--text] [--file]` | 创建模板（`--file` 表示从文件读取内容） |
| `update-template <id> <name> <html_or_text> [--text] [--file]` | 更新已有模板 |
| `delete-template <id>` | 删除指定模板 |

**示例**：

```bash
# 获取前 20 个模板（默认分页）
python3 ${SKILL_DIR}/scripts/ses_tool.py list-templates

# 分页查询：从第 40 条起，每页 10 条，仅查看已审核通过的模板
python3 ${SKILL_DIR}/scripts/ses_tool.py list-templates --offset 40 --limit 10 --status 0

# 查看指定模板的详细内容
python3 ${SKILL_DIR}/scripts/ses_tool.py get-template 251254620

# 创建 HTML 模板（直接传入内容）
python3 ${SKILL_DIR}/scripts/ses_tool.py create-template "欢迎邮件模板" \
  "<h1>欢迎, {{name}}!</h1><p>感谢您的注册。</p>"

# 创建 HTML 模板（从文件读取，适合大模板）
python3 ${SKILL_DIR}/scripts/ses_tool.py create-template "促销模板" \
  "/data/templates/promo.html" --file

# 创建纯文本模板
python3 ${SKILL_DIR}/scripts/ses_tool.py create-template "验证码模板" \
  "您的验证码是 {{code}}，有效期 {{expire}} 分钟。" --text

# 更新模板
python3 ${SKILL_DIR}/scripts/ses_tool.py update-template 251254620 "欢迎邮件v2" \
  "<h1>Hi, {{name}}!</h1><p>Welcome aboard!</p>"

# 删除模板
python3 ${SKILL_DIR}/scripts/ses_tool.py delete-template 251254620
```

### DNS 诊断命令

以下命令均通过 `dns_checker.py` 执行，无需配置 AKSK，直接查询公共 DNS 服务。

| 命令 | 说明 |
|------|------|
| `check-all <domain>` | 综合检查 SPF / DKIM / DMARC / MX 所有记录及 CNAME 冲突 |
| `check-spf <domain>` | 检查 SPF 记录 |
| `check-dkim <domain> [selector]` | 检查 DKIM 记录（selector 默认为 `qcloud`） |
| `check-dmarc <domain>` | 检查 DMARC 记录 |
| `check-mx <domain>` | 检查 MX 记录 |
| `check-propagation <domain> <type> [name]` | 多节点 DNS 传播检测 |
| `diagnose <domain> [problem]` | 自动诊断并给出修复建议 |
| `guide <domain>` | 生成完整的 DNS 配置指南 |

**示例 — 综合检查**：

```bash
# 一键检查域名的所有邮件相关 DNS 记录
python3 ${SKILL_DIR}/scripts/dns_checker.py check-all example.com
```

**示例 — 单项检查**：

```bash
# 检查 SPF 记录（验证 include、DNS Lookup 次数、策略等）
python3 ${SKILL_DIR}/scripts/dns_checker.py check-spf example.com

# 检查 DKIM 记录（默认 selector 为 qcloud）
python3 ${SKILL_DIR}/scripts/dns_checker.py check-dkim example.com

# 检查 DKIM 记录（指定自定义 selector）
python3 ${SKILL_DIR}/scripts/dns_checker.py check-dkim example.com s1024

# 检查 DMARC 策略
python3 ${SKILL_DIR}/scripts/dns_checker.py check-dmarc example.com

# 检查 MX 记录
python3 ${SKILL_DIR}/scripts/dns_checker.py check-mx example.com
```

**示例 — DNS 传播检测**：

```bash
# 检测 SPF（TXT 记录）在各 DNS 节点的传播状态
python3 ${SKILL_DIR}/scripts/dns_checker.py check-propagation example.com TXT

# 检测 DKIM 记录的传播状态
python3 ${SKILL_DIR}/scripts/dns_checker.py check-propagation example.com TXT qcloud._domainkey

# 检测 DMARC 记录的传播状态
python3 ${SKILL_DIR}/scripts/dns_checker.py check-propagation example.com TXT _dmarc

# 检测 MX 记录的传播状态
python3 ${SKILL_DIR}/scripts/dns_checker.py check-propagation example.com MX
```

**示例 — 自动诊断**：

```bash
# 全面诊断域名的 DNS 配置问题并给出修复建议
python3 ${SKILL_DIR}/scripts/dns_checker.py diagnose example.com

# 针对特定问题进行诊断
python3 ${SKILL_DIR}/scripts/dns_checker.py diagnose example.com "SPF验证失败"
python3 ${SKILL_DIR}/scripts/dns_checker.py diagnose example.com "DKIM配置错误"
python3 ${SKILL_DIR}/scripts/dns_checker.py diagnose example.com "传播未生效"
```

**示例 — 生成配置指南**：

```bash
# 为指定域名生成完整的 DNS 配置指南
python3 ${SKILL_DIR}/scripts/dns_checker.py guide example.com
```

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [API 参考](references/api_reference.md) | SES API 参数说明、状态码映射、请求 / 响应示例 |
| [DNS 配置指南](references/dns_guide.md) | SPF / DKIM / DMARC / MX 配置详解、CNAME 冲突说明与常见问题 |
| [安全配置指南](references/security_setup_guide.md) | 子账号创建、策略关联、IP 访问限制、密钥安全管理 |
| [腾讯云 SES 产品文档](https://cloud.tencent.com/document/product/1288) | 官方产品文档（外部链接） |
| [SendEmail API 文档](https://cloud.tencent.com/document/product/1288/51034) | 官方 SendEmail 接口文档（外部链接） |
| [DNS 验证说明](https://cloud.tencent.com/document/product/1288/60652) | 官方发信域名 DNS 配置说明（外部链接） |