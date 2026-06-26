# `ad extension whatsapp` JSON 配置说明

为**已创建的 PMax 活动**挂载 WhatsApp 私信（`BUSINESS_MESSAGE`）。也可写入 `pmax-create` JSON 的 `campaignExtensions.businessMessage` 由 CLI 自动编排。

模板：`pmax-whatsapp-template.json`。

---

## 命令

```bash
# 单独挂载
siluzan-tso ad extension whatsapp -a <accountId> --config-file ./whatsapp.json --json-out ./snap

# 更新（PUT 后 id 会变，用响应新 id）
siluzan-tso ad extension update -a <accountId> --id <extensionId> --config-file ./whatsapp.json

# 或在 pmax-create 一并挂载
# campaignExtensions.businessMessage 见 pmax-create-template.md
```

---

## 字段

| 字段                                      | 必填 | 说明                                                 |
| ----------------------------------------- | :--: | ---------------------------------------------------- |
| `account`                                 |  ✅  | Google 媒体客户 ID                                   |
| `campaignId`                              |  ✅  | PMax 活动 ID                                         |
| `businessMessage.starterMessage`          |  ✅  | 欢迎语                                               |
| `businessMessage.callToActionDescription` |      | 默认 `Message us on WhatsApp`                        |
| `businessMessage.callToActionSelection`   |      | 默认 `CONTACT_US`；可选 `LEARN_MORE`、`GET_QUOTE` 等 |
| `businessMessage.messageProvider`         |      | 默认 `WHATSAPP`                                      |
| `businessMessage.whatsapp.countryCode`    |  ✅  | 两位国家码（如 `US`）                                |
| `businessMessage.whatsapp.phoneNumber`    |  ✅  | WhatsApp Business 注册号码                           |

---

## 前置条件

1. **Google API 白名单**（阻塞项）：未开通返回 `CUSTOMER_NOT_ON_ALLOWLIST_FOR_MESSAGE_ASSETS`；须 MCC 运营联系 Google AM 申请。
2. 号码已在 **WhatsApp Business** 注册。
3. 同 Campaign **仅 1 个** ENABLED WhatsApp；已有则 POST 400，须 DELETE 或 PUT。

详见 Sammamish `pmax-frontend-api.md` §3.2.4。
