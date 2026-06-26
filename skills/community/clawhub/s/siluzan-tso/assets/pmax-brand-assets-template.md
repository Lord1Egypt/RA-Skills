# `ad pmax-brand-assets-edit` PATCH JSON

Brand Guidelines（BG）**已开启**时，改商家名 / Logo / 主色字体走 Campaign 级接口。

```bash
siluzan-tso ad pmax-get -a <accountId> --campaign-id <cid> --json-out ./snap
# 确认 _brandGuidelinesActive === true 后：
siluzan-tso ad pmax-brand-assets-edit -a <accountId> --campaign-id <cid> \
  --patch-file ./brand-patch.json --json-out ./snap
```

模板：[`pmax-brand-assets-template.json`](pmax-brand-assets-template.json)

| 字段                                                                                  | 说明               |
| ------------------------------------------------------------------------------------- | ------------------ |
| `businessName`                                                                        | 商家名（≤25 字符） |
| `logoImageAssetId` / `logoImageBase64` / `imagePaths.logo`                            | Logo 三选一        |
| `landscapeLogoImageAssetId` / `landscapeLogoImageBase64` / `imagePaths.landscapeLogo` | 可选横版 Logo      |
| `brandGuidelines.mainColor` / `accentColor`                                           | 须成对             |
| `brandGuidelines.predefinedFontFamily`                                                | 如 `Roboto`        |

**至少传一项**。改完后 `ad pmax-get` 刷新，品牌读 `brandAssets[]`。
