# `ad pmax-asset-group-create` JSON

在同一 PMax 活动下追加资产组。

```bash
siluzan-tso ad pmax-get -a <accountId> --campaign-id <cid> --json-out ./snap
siluzan-tso ad pmax-asset-group-create --config-file ./ag.json --json-out ./snap
```

模板：[`pmax-asset-group-template.json`](pmax-asset-group-template.json)

## Brand Guidelines 分支（Agent 必读）

CLI **自动** GET 活动详情，无需手填开关：

| `_brandGuidelinesActive`（来自 pmax-get） | JSON 要求                                                               |
| ----------------------------------------- | ----------------------------------------------------------------------- |
| `true`                                    | **省略** `businessName`、`logoImage*`、`imagePaths.logo`（仅横图+方图） |
| `false`                                   | **必填** `businessName` + Logo（三图齐全）                              |

若 JSON 在 BG 生效时仍含品牌字段，CLI 会警告并忽略（不阻断）。

## 字段

与 `pmax-create` 资产组部分相同（`name`、`finalUrls`、标题/描述、营销图）。`campaignId` 必填。
