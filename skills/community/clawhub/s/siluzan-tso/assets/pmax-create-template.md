# `ad pmax-create` JSON 配置说明

`siluzan-tso ad pmax-create` / `ad pmax-validate` **仅**接受 `--config-file` 指向的 JSON 文件。

**与 Search 智投隔离**：勿使用 `campaign-create-template.json` 或 `ad campaign-create`。PMax 使用 `ad pmax-create`，同步返回 `campaignId`。

模板 JSON：同目录 [`pmax-create-template.json`](pmax-create-template.json)。

---

## Agent 常见坑

| 场景          | 正确做法                                                                                                                                                            |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 创建 PMax     | `pmax-validate` → 用户确认 → `pmax-create`                                                                                                                          |
| 文案超长      | `pmax-validate --json-out` 读 `lengthViolations`（含完整 `text`）；**勿自动截断**，列改写方案给用户确认后再改 JSON 并重跑 validate（同 Search `campaign-validate`） |
| 金额          | JSON 填**主币种「元」**；CLI 提交前 `budget`、`targetCpa_BidingAmount` ×100                                                                                         |
| 图片          | **只填 `imagePaths`** 指向本地 PNG/JPEG；`pmax-create` 会自动 multipart 上传并用 assetId 创建（勿把 Base64 提交进 Git）                                             |
| 视频          | JSON 填 **`videoPath`**（别名 `video` 亦可）；`pmax-create` 成功后 **必定**经 PyAPI 上传并链接（含 `--json-out`）。已有 YouTube 用 `youtubeUrlOrId`                 |
| 附加资产      | **必填** `campaignExtensions`：宣传信息 ≥20、结构化摘要 ≥20、站内链接 ≥6、leadForm、WhatsApp |
| 文案数量      | 短标题 15、长 nga 5（Google API 上限，须填满）、描述 5 |
| Lead Gen 方案 | **默认**在 `campaignExtensions` 含 **`leadForm`**（B2B/询盘/留资）；仅 callouts/snippets 不算完整方案；用户明确不要才省略                                        |
| 存量补表单    | 活动已创建时用 `ad extension lead-form`（见 `pmax-lead-form-template.md` 方式 B）                                                                                   |
| 改已上线 PMax | 先 `ad pmax-get` 看 `_brandGuidelinesActive`；改品牌见 `pmax-api.md` § Brand Guidelines                                                                             |
| 列表复核      | `ad campaigns -a <id> --json-out ./snap`，`channelTypeV2` 应为 `PERFORMANCE_MAX`                                                                                    |

---

## 方案生成（Agent 出投放方案时）

出 PMax **投放方案**（Markdown + JSON）时，除标题/描述/图片外，**Lead Gen / B2B 场景默认包含潜在客户表单**：

1. JSON：`campaignExtensions.leadForm` 字段结构与 `pmax-lead-form-template.json` 的 `leadForm` 相同（`businessName`、`headline`、`description`、`privacyPolicyUrl`、`finalUrl`、`fields`）。
2. Markdown：单独一节 **「潜在客户表单」**，列出表单标题、描述、收集字段、隐私政策 URL；**不得**只在 JSON 里写而方案正文遗漏。
3. `privacyPolicyUrl`：从落地页站点找 `/privacy`、`/terms` 等；找不到时向用户确认，**禁止**编造 URL。
4. 用户说「不要表单 / 仅品牌曝光 / 纯电商 Shopping」→ 可省略 `leadForm` 并在方案中说明原因。
5. `pmax-validate` 会校验 `leadForm`；创建后 `--json-out` 的 `campaignExtensions.leadForm` 段含 `ok` / `error`。

---

## 推荐命令顺序

```bash
siluzan-tso ad geo search -a <accountId> -q "United States"
siluzan-tso ad pmax-validate --config-file ./pmax.json --json-out ./snap-pmax
# 用户确认方案后：
siluzan-tso ad pmax-create --config-file ./pmax.json --json-out ./snap-pmax
siluzan-tso ad campaigns -a <accountId> --json-out ./snap
```

---

## 字段说明（camelCase）

| 字段                          | 类型       | 必填 | 说明                                                                                                                                                |
| ----------------------------- | ---------- | :--: | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `account`                     | string     |  ✅  | Google 媒体客户 ID（`list-accounts` → `mediaCustomerId`）                                                                                           |
| `name`                        | string     |  ✅  | 广告系列名称                                                                                                                                        |
| `budget`                      | number     |  ✅  | 日预算（**元**），如 `50` = 主币种 50.00/天                                                                                                         |
| `budgetName`                  | string     |      | 预算资源名称                                                                                                                                        |
| `assetGroupName`              | string     |      | 首个资产组名称；缺省由服务端生成                                                                                                                    |
| `finalUrls`                   | string[]   |  ✅  | 至少 1 个 `https://` 落地页                                                                                                                         |
| `businessName`                | string     |  ✅  | BUSINESS_NAME：1 条，≤25 字符                                                                                                                       |
| `headlines`                   | string[]   |  ✅  | HEADLINE：3–15 条，每条 ≤30 字符（CJK×2）                                                                                                           |
| `longHeadlines`               | string[]   |  ✅  | LONG_HEADLINE：1–5 条，每条 ≤90 字符                                                                                                                |
| `descriptions`                | string[]   |  ✅  | DESCRIPTION：2–5 条，每条 ≤90 字符                                                                                                                  |
| `imagePaths.marketing`        | string     | ✅\* | MARKETING_IMAGE 横图 1.91:1，≤5MB（创建 JSON 1 张；资产组 API 最多 20）                                                                             |
| `imagePaths.square`           | string     | ✅\* | SQUARE_MARKETING_IMAGE 方图 1:1，≤5MB（创建 1 张；最多 20）                                                                                         |
| `imagePaths.logo`             | string     | ✅\* | LOGO 方图 1:1，≤5MB（创建 1 张；最多 5）                                                                                                            |
| `marketingImageAssetId`       | string     | ✅\* | 已上传横图 asset.id（与 path/base64 三选一）                                                                                                        |
| `squareMarketingImageAssetId` | string     | ✅\* | 已上传方图 asset.id                                                                                                                                 |
| `logoImageAssetId`            | string     | ✅\* | 已上传 Logo asset.id                                                                                                                                |
| `marketingImageBase64`        | string     | ✅\* | 内联 Base64（不推荐；无 path 时用）                                                                                                                 |
| `squareMarketingImageBase64`  | string     | ✅\* | 内联方图 Base64                                                                                                                                     |
| `logoImageBase64`             | string     | ✅\* | 内联 Logo Base64                                                                                                                                    |
| `targetedLocations`           | `{ id }[]` |      | 地理 criterion ID，如 `{ "id": "2840" }`（美国）                                                                                                    |
| `targetedLanguages`           | `{ id }[]` |      | 语言 ID，如 `{ "id": 1000 }`（英语）                                                                                                                |
| `biddingStrategyTypeV2`       | string     |      | 默认 `MAXIMIZE_CONVERSIONS`                                                                                                                         |
| `targetCpa_BidingAmount`      | number     |      | `TARGET_CPA` 或带目标 CPA 的 `MAXIMIZE_CONVERSIONS` 时必填（**元**）                                                                                |
| `targetRoas`                  | number     |      | `TARGET_ROAS` 时必填（如 `2.5` = 250%）                                                                                                             |
| `brandGuidelinesEnabled`      | boolean    |      | 省略 = 网关默认 `true`（Campaign 级 BG）；`false` = 品牌在 AssetGroup（旧路径）                                                                     |
| `videoPath`                   | string     |      | YOUTUBE_VIDEO（可选）：本地视频 ≥10s；与 `youtubeUrlOrId` 二选一，创建时最多 1 条；更多视频创建后用 `pmax-youtube-link` / `pmax-assets-update` 追加 |
| `videoTitle`                  | string     |      | PyAPI 上传标题（默认文件名）                                                                                                                        |
| `videoDescription`            | string     |      | PyAPI 上传描述（可选）                                                                                                                              |
| `youtubeUrlOrId`              | string     |      | 已有 YouTube URL 或 11 位 ID；`pmax-create` 后自动链接                                                                                              |
| `youtubeAssetName`            | string     |      | 链接 YouTube 时的资产显示名                                                                                                                         |
| `campaignExtensions`          | object     |      | 创建成功后自动挂载的 Campaign 级扩展（见下表）                                                                                                      |

\* 三张图各须有一种来源（路径或 Base64）。

### `campaignExtensions`（可选，CLI 编排）

**不**随 `POST .../campaign/pmax` 提交；活动创建成功后 CLI 自动调用 `extensionmanagement`。

| 子字段               | 类型     | 说明                                                                     |
| -------------------- | -------- | ------------------------------------------------------------------------ |
| `callouts`           | string[] | 宣传信息（CALLOUT），每条 ≤25 字符，各创建 1 个扩展                      |
| `structuredSnippets` | object[] | `{ header, values }`；`values` 至少 3 项                                 |
| `leadForm`           | object   | 潜在客户表单；字段同 `pmax-lead-form-template.json` 的 `leadForm`        |
| `businessMessage`    | object   | WhatsApp 私信；字段同 `pmax-whatsapp-template.json` 的 `businessMessage` |

标头可选值：`ad extension snippet-headers`。WhatsApp 需 Google API 白名单（见 `pmax-whatsapp-template.md`）。

若挂载失败，活动仍已创建；`--json-out` 的 `campaignExtensions` 段含各条 `ok` / `error`，可手动 `ad extension *` 补挂。

### 出价策略（PMax 支持子集）

| 值                          | 说明                                    |
| --------------------------- | --------------------------------------- |
| `MAXIMIZE_CONVERSIONS`      | 默认                                    |
| `MAXIMIZE_CONVERSION_VALUE` | 最大化转化价值                          |
| `TARGET_CPA`                | 目标 CPA（须 `targetCpa_BidingAmount`） |
| `TARGET_ROAS`               | 目标 ROAS（须 `targetRoas`）            |

---

## 成功响应（create）

网关同步返回（camelCase）：

| 字段           | 说明                                               |
| -------------- | -------------------------------------------------- |
| `campaignId`   | 活动 ID                                            |
| `assetGroupId` | 首个资产组 ID                                      |
| `budgetId`     | 日预算 ID（后续 PATCH 改预算时需与 `budget` 成对） |

---

## 范围说明

- **支持**：Lead Gen / 非 Shopping 的 Performance Max
- **不含**：Shopping PMax、Listing groups；信号与其它编辑见 `ad pmax-signals-*` 等（`references/google-ads/pmax-api.md`）

命令与流程见 `references/google-ads/pmax-api.md`。
