# Performance Max（PMax）

## 金额单位

| JSON / CLI                          | 提交到 API    |
| ----------------------------------- | ------------- |
| `budget: 5.5`（元）                 | `550`（×100） |
| `targetCpa_BidingAmount: 0.5`（元） | `50`          |

报表 `spend` 为美元浮点，勿与管理 API 混用。

---

## CLI 命令

| 命令                                                          | 说明                                                                                          |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `ad pmax-validate`                                            | 本地校验                                                                                      |
| `ad pmax-create`                                              | 创建系列（同步返回 `campaignId` 等）                                                          |
| `ad pmax-channel-types`                                       | 渠道类型列表                                                                                  |
| `ad pmax-get`                                                 | 系列详情（含 `brandAssets[]`；`--json-out` 附加 `_brandGuidelinesActive`、`_agentBrandHint`） |
| `ad pmax-edit`                                                | 编辑系列（预算/出价/状态；**不可**改 `brandGuidelinesEnabled`）                               |
| `ad pmax-brand-assets-edit`                                   | BG 已开启时改 Campaign 级品牌（商家名/Logo/样式）                                             |
| `ad pmax-brand-guidelines-enable`                             | 存量活动启用 BG（不可关闭）                                                                   |
| `ad pmax-asset-group-create`                                  | 新建资产组                                                                                    |
| `ad pmax-asset-group-edit`                                    | 编辑资产组                                                                                    |
| `ad pmax-assets-update`                                       | 更新资产                                                                                      |
| `ad pmax-youtube-link`                                        | **追加**单条 YouTube 视频（不替换已有视频）                                                   |
| `ad pmax-signals-get` / `ad pmax-signals-set`                 | 读/写信号（**全量** PUT）                                                                     |
| `ad pmax-audiences`                                           | 受众列表                                                                                      |
| `ad pmax-image-upload`                                        | 单张图片上传                                                                                  |
| `ad pmax-report-asset-groups` / `ad pmax-report-geo`          | 报表                                                                                          |
| `ad campaigns`                                                | 列表（筛 `PERFORMANCE_MAX`）                                                                  |
| `ad extension pmax-types`                                     | PMax 支持的附加资产类型与层级                                                                 |
| `ad extension callout` / `snippet` / `lead-form` / `whatsapp` | 宣传信息 / 结构化摘要 / 潜在客户表单 / WhatsApp                                               |
| `ad extension list`                                           | 查询已挂载扩展（`--type` / `--campaign-id`）                                                  |

模板：`assets/pmax-create-template.json`、`pmax-asset-group-template.json`、`pmax-assets-update-template.json`、`pmax-signals-template.json`、`pmax-patch-campaign-template.json`、`pmax-brand-assets-template.json`、`pmax-brand-guidelines-enable-template.json`、`pmax-lead-form-template.json`。

### 附加资产（Callout / Snippet / Lead Form）

网关 `POST .../campaign/pmax` **不**接受扩展字段；CLI 通过 **`campaignExtensions`** 在 `pmax-create` 成功后**自动编排** `extensionmanagement`（与手动 `ad extension *` 等价）。

**方式 A（推荐，一条命令）**：在 `pmax-create` JSON 中填 `campaignExtensions`。**Lead Gen / B2B 询盘方案须含 `leadForm`**（勿只写 callouts/snippets；用户明确不要表单才省略）：

```json
{
  "campaignExtensions": {
    "callouts": ["Free shipping"],
    "structuredSnippets": [{ "header": "Services", "values": ["A", "B", "C"] }],
    "leadForm": {
      "businessName": "...",
      "headline": "...",
      "description": "...",
      "privacyPolicyUrl": "...",
      "finalUrl": "...",
      "fields": [{ "inputType": "EMAIL" }]
    },
    "businessMessage": {
      "starterMessage": "Hi!",
      "whatsapp": { "countryCode": "US", "phoneNumber": "2125550100" }
    }
  }
}
```

`pmax-validate` 会一并校验；`pmax-create` 成功后在同一次调用内挂载（`--json-out` 含 `campaignExtensions` 结果）。

**方式 B（分步）**：活动创建后手动走 `extensionmanagement`（PMax 限制 Account/Campaign 层级）。

| 中文            | 类型                 | 命令                                                                                                 |
| --------------- | -------------------- | ---------------------------------------------------------------------------------------------------- |
| 宣传信息        | `CALLOUT`            | `ad extension callout -a <id> --text "..." --level Campaign --campaign-id <cid>`                     |
| 结构化摘要      | `STRUCTURED_SNIPPET` | `ad extension snippet -a <id> --header Brands --values "A,B,C" --level Campaign --campaign-id <cid>` |
| 潜在客户表单    | `LEAD_FORM`          | `ad extension lead-form -a <id> --config-file ./lead-form.json`                                      |
| 附加链接 / 电话 | `SITELINK` / `CALL`  | `ad extension sitelink` / `call`（同上 `--level Campaign`）                                          |
| 私信 WhatsApp   | `BUSINESS_MESSAGE`   | `ad extension whatsapp` 或 `campaignExtensions.businessMessage`                                      |

```bash
# 查 PMax 支持类型
siluzan-tso ad extension pmax-types --json-out ./snap

# 结构化摘要标头下拉
siluzan-tso ad extension snippet-headers --json-out ./snap

# Lead Form（模板见 assets/pmax-lead-form-template.md）
siluzan-tso ad extension lead-form -a <accountId> --config-file ./lead-form.json --json-out ./snap

# WhatsApp（模板见 assets/pmax-whatsapp-template.md；需 Google API 白名单）
siluzan-tso ad extension whatsapp -a <accountId> --config-file ./whatsapp.json --json-out ./snap

# 复核 / 更新 / 删除
siluzan-tso ad extension list -a <accountId> --type LEAD_FORM --campaign-id <cid> --json-out ./snap
siluzan-tso ad extension list -a <accountId> --type BUSINESS_MESSAGE --campaign-id <cid> --json-out ./snap
siluzan-tso ad extension update -a <accountId> --id <extId> --config-file ./lead-form.json
siluzan-tso ad extension update -a <accountId> --id <extId> --config-file ./whatsapp.json  # id 会变
siluzan-tso ad extension delete -a <accountId> --id <extId>
```

**约束**：

- PMax **不支持** `level: Ad Group`（会 400）
- `LEAD_FORM` **仅** `Campaign` 级；每活动通常 1 个
- `BUSINESS_MESSAGE`（WhatsApp）每 Campaign **仅 1 个** ENABLED；须 **Google API 白名单**
- WhatsApp **PUT 后 asset id 会变**；后续操作须用响应中的新 `id`
- 创建 Lead Form 后后端自动尝试开启 `SUBMIT_LEAD_FORM` + `GOOGLE_HOSTED` 转化目标

**网关**：`GET /extensionmanagement/pmaxSupportedTypeList`；`POST|PUT|DELETE /extensionmanagement/extension/{accountId}[/{id}]`（Sammamish `ExtensionManagementController.cs`）。

### 图片（推荐流程）

1. JSON 配置 `imagePaths`（三张本地图）。
2. `ad pmax-validate` → 用户确认 → `ad pmax-create`：CLI **自动上传**三张图并写入 `*ImageAssetId`（Body 不含 Base64）。
3. 可选预上传：`ad pmax-image-upload -a <id> --image-path ./x.png`，将返回 `id` 写入 JSON。

### 视频（YouTube）

**语义（与后端 `pmax-frontend-api.md` §5.3 / §5.4 一致）**：`YOUTUBE_VIDEO` 默认 **追加**，每个资产组最多 **15** 条；不可重复链接同一 `videoId`。仅当 `pmax-assets-update` 显式传 `replaceFieldTypes: ["YOUTUBE_VIDEO"]` 时才会先删后增（替换全部视频）。

| 场景          | 命令 / 接口                                                                                                        |
| ------------- | ------------------------------------------------------------------------------------------------------------------ |
| 创建时挂 1 条 | `pmax-create` JSON：`videoPath` 或 `youtubeUrlOrId`（二选一，单次最多 1 条）                                       |
| 追加 1 条     | `ad pmax-youtube-link` → `POST .../asset-group/{id}/youtube`                                                       |
| 批量追加多条  | `ad pmax-assets-update` → `PUT .../assets`，`assetsToLink` 中多条 `YOUTUBE_VIDEO`                                  |
| 取消链接      | `ad pmax-assets-update`，`assetGroupAssetResourceNamesToRemove`（取自 `pmax-get` 的 `assets[].assetResourceName`） |
| 替换全部视频  | `ad pmax-assets-update`，`replaceFieldTypes: ["YOUTUBE_VIDEO"]` + 新的 `assetsToLink`                              |

**创建时自动链接**

- **`videoPath`**：本地 `.mp4` 等；`pmax-create` 经 **GoogleAdsPyAPI** `POST {googleApiUrl}/pyapi/video/upload` 上传，轮询 `GET .../upload/status` 得 `video_id`，再 `POST .../asset-group/{id}/youtube` 链接（与 `youtubeUrlOrId` 二选一）。
- **`youtubeUrlOrId`**：已有 YouTube URL 或 11 位 ID；创建成功后自动链接。

**已创建系列追加视频**（`ad pmax-youtube-link`）：

```bash
# 已有 YouTube URL / ID
siluzan-tso ad pmax-youtube-link -a <id> --asset-group-id <agId> --campaign-id <cid> \
  --youtube "https://www.youtube.com/watch?v=xxxxx"

# 本地视频（PyAPI 上传后追加）
siluzan-tso ad pmax-youtube-link -a <id> --asset-group-id <agId> --campaign-id <cid> \
  --video-path ./promo-v2.mp4 --video-title "宣传视频 2"
```

**批量追加**（`ad pmax-assets-update --config-file ./pmax-videos.json`）：

```json
{
  "account": "6326027735",
  "campaignId": "12345678901",
  "assetGroupId": "98765432101",
  "assetsToLink": [
    { "fieldType": "YOUTUBE_VIDEO", "youtubeVideoId": "dQw4w9WgXcQ", "assetName": "Promo1" },
    {
      "fieldType": "YOUTUBE_VIDEO",
      "youtubeVideoId": "https://youtu.be/jNQXAC9IVRw",
      "assetName": "Promo2"
    }
  ]
}
```

`youtubeVideoId` 接受 11 位 ID 或完整 URL。模板见 `assets/pmax-assets-update-template.json`。

---

## Brand Guidelines（品牌手册，Google v21+）

Google v21+ 新建 PMax **默认开启** BG：`businessName` / Logo 挂在 **Campaign**（`brandAssets[]`），全活动共用；首个 AssetGroup 的 `assets[]` **不含** 品牌。

### Agent 决策（必读）

1. **任何编辑前先** `ad pmax-get --json-out` → 读 `_brandGuidelinesActive`（或 `_agentBrandHint`）
2. BG 生效 → 改品牌用 `ad pmax-brand-assets-edit`；追加 AG **省略** 品牌字段
3. BG 未生效 → 改品牌在 AssetGroup 上用 `ad pmax-assets-update`；或 `ad pmax-brand-guidelines-enable` 启用 BG

| 场景               | 命令                                                                              |
| ------------------ | --------------------------------------------------------------------------------- |
| 创建（默认 BG 开） | `pmax-create` JSON 仍必填 `businessName`+Logo；可省略 `brandGuidelinesEnabled`    |
| 创建（旧路径）     | JSON 加 `"brandGuidelinesEnabled": false`                                         |
| 改 Campaign 级品牌 | `ad pmax-brand-assets-edit -a <id> --campaign-id <cid> --patch-file ./brand.json` |
| 存量启用 BG        | `ad pmax-brand-guidelines-enable --config-file ./enable-bg.json`                  |
| 追加资产组         | `pmax-asset-group-create`（CLI 自动判断，BG 下无需 Logo/商家名）                  |

**禁止**：BG 生效时对 AssetGroup 执行 `pmax-assets-update` 链接 `BUSINESS_NAME`/`LOGO`/`LANDSCAPE_LOGO`（CLI 预检阻断，网关亦 400）。

模板：`assets/pmax-brand-assets-template.md`、`pmax-brand-guidelines-enable-template.md`。

---

## 编辑流程

1. `ad pmax-get` 拉详情（读 `_brandGuidelinesActive`）
2. 改系列 → `ad pmax-edit` 或 `--patch-file`
3. **改品牌** → BG 生效：`ad pmax-brand-assets-edit`；未生效：`ad pmax-assets-update` 或先 `pmax-brand-guidelines-enable`
4. 改资产组 → `ad pmax-asset-group-edit`
5. 改 AG 内素材 → `ad pmax-assets-update`（`campaignId` 必填；勿改品牌 fieldType 若 BG 生效）
6. 改信号 → `ad pmax-signals-get` → `ad pmax-audiences` → `ad pmax-signals-set`（一次带齐两类数组）

---

## 删除

- **系列**：`ad campaign-delete -a <id> --id <campaignId>`
- **资产组**：`ad pmax-asset-group-edit --status REMOVED`
- **资产**：`ad pmax-assets-update` 的 `unlink`（见模板）

---

## 边界

- 勿对 PMax 使用 `ad campaign-edit`（会 **400**）
- 新建勿用 `ad campaign-create`；用 `ad pmax-create`
