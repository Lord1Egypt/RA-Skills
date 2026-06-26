# `ad pmax-brand-guidelines-enable` JSON

存量 PMax 活动启用 Brand Guidelines（**不可关闭**）。

```bash
siluzan-tso ad pmax-get -a <accountId> --campaign-id <cid> --json-out ./snap
# _brandGuidelinesActive === false 时：
siluzan-tso ad pmax-brand-guidelines-enable --config-file ./enable-bg.json --json-out ./snap
```

模板：[`pmax-brand-guidelines-enable-template.json`](pmax-brand-guidelines-enable-template.json)

| 字段                      | 必填 | 说明                                                           |
| ------------------------- | :--: | -------------------------------------------------------------- |
| `account`                 |  ✅  | 媒体客户 ID                                                    |
| `campaignId`              |  ✅  | 活动 ID                                                        |
| `autoPopulateBrandAssets` |      | 默认 `false`；`true` 时 Google 自动选品牌资产                  |
| `businessName`            | 条件 | `autoPopulateBrandAssets=false` 时必填                         |
| Logo 相关                 | 条件 | `autoPopulateBrandAssets=false` 时必填（同 brand-assets 模板） |
| `brandGuidelines`         |      | 可选样式                                                       |

启用后：`pmax-asset-group-create` 可省略 `businessName`/Logo；改品牌用 `pmax-brand-assets-edit`。
