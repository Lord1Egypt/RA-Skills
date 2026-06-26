# `ad extension lead-form` JSON 配置说明

PMax **潜在客户表单**（`LEAD_FORM`）有两种挂载方式：

| 方式 | 何时用 | 入口 |
| ---- | ------ | ---- |
| **A（推荐·新建活动）** | `pmax-create` 一次性创建系列 + 扩展 | `pmax-create` JSON 的 `campaignExtensions.leadForm`（见 `pmax-create-template.json`） |
| **B（存量补挂）** | 活动已存在、需单独加/改表单 | 本文件 + `ad extension lead-form` |

**Lead Gen / B2B 询盘类 PMax 方案**：默认在 `campaignExtensions` 中包含 `leadForm`；用户明确不要表单时才省略。

模板 JSON：同目录 [`pmax-lead-form-template.json`](pmax-lead-form-template.json)（方式 B 用；方式 A 只取其中的 `leadForm` 对象嵌入 `pmax-create` JSON）。

---

## 推荐命令顺序

```bash
# 1. 确认 PMax 活动 ID
siluzan-tso ad campaigns -a <accountId> --json-out ./snap

# 2. 查看 PMax 支持的扩展类型
siluzan-tso ad extension pmax-types --json-out ./snap

# 3. 检查活动上是否已有 Lead Form
siluzan-tso ad extension list -a <accountId> --type LEAD_FORM --campaign-id <campaignId> --json-out ./snap

# 4. 创建
siluzan-tso ad extension lead-form -a <accountId> --config-file ./lead-form.json --json-out ./snap

# 5. 更新（须带完整 leadForm 对象）
siluzan-tso ad extension update -a <accountId> --id <extensionId> --config-file ./lead-form.json
```

---

## 字段说明

| 字段                               | 类型     | 必填 | 说明                                                           |
| ---------------------------------- | -------- | :--: | -------------------------------------------------------------- |
| `account`                          | string   |  ✅  | Google 媒体客户 ID                                             |
| `campaignId`                       | string   |  ✅  | PMax 活动 ID（`channelTypeV2=PERFORMANCE_MAX`）                |
| `leadForm.businessName`            | string   |  ✅  | 商家名称                                                       |
| `leadForm.headline`                | string   |  ✅  | 表单标题                                                       |
| `leadForm.description`             | string   |  ✅  | 表单描述                                                       |
| `leadForm.privacyPolicyUrl`        | string   |  ✅  | 隐私政策 URL                                                   |
| `leadForm.finalUrl`                | string   |  ✅  | 落地页 URL                                                     |
| `leadForm.callToActionType`        | string   |      | 默认 `LEARN_MORE`                                              |
| `leadForm.callToActionDescription` | string   |      | 默认 `Contact us`                                              |
| `leadForm.fields`                  | object[] |  ✅  | 至少 1 项；`inputType` 如 `FULL_NAME`、`EMAIL`、`PHONE_NUMBER` |
| `leadForm.webhook`                 | object   |      | 写入 Google 的 Webhook（非平台接收端）                         |

---

## PMax 附加资产对照

| 中文          | 类型                 | CLI 命令                                                        |
| ------------- | -------------------- | --------------------------------------------------------------- |
| 宣传信息      | `CALLOUT`            | `ad extension callout`                                          |
| 结构化摘要    | `STRUCTURED_SNIPPET` | `ad extension snippet`                                          |
| 潜在客户表单  | `LEAD_FORM`          | `ad extension lead-form`                                        |
| 附加链接      | `SITELINK`           | `ad extension sitelink`                                         |
| 附加电话      | `CALL`               | `ad extension call`                                             |
| 私信 WhatsApp | `BUSINESS_MESSAGE`   | `ad extension whatsapp` 或 `campaignExtensions.businessMessage` |

**层级**：PMax 仅 `Account` / `Campaign`；`Ad Group` 会 **400**。

**副作用**：创建 Lead Form 后，后端会自动尝试将 `SUBMIT_LEAD_FORM` + `GOOGLE_HOSTED` 转化目标设为 `biddable=true`。

详见 `references/google-ads/pmax-api.md` § 附加资产。
