# 产品定价

## 当前可用产品

| product_id | 服务内容 | 单价 |
|------------|----------|------|
| `image-generation` | WorkRally图片生成 | 0.36 元/次 |

## 价格说明

- **定价方**：SkillHub 后台（价格以平台后台配置为准）
- **单位**：人民币元；下单时以分为单位（1 元 = 100 分）
- **次数**：每次生成任务对应一次扣费；当前每次固定生成 1 个结果

## 生成规格（云端设定）

- **模型 / 分辨率**：由云端统一设定；图片规格为 1K。调用方无需指定，即使传入 `model` / `resolution` 也会被云端配置覆盖
- **宽高比**：默认 `16:9`；调用方可通过 `aspect_ratio` 传 `1:1` / `9:16` 等其他比例
- **参考图**：图生图/改图时传 `input_images`，本地图片以 `data:image/<ext>;base64,<...>` 内联（云端自动上传）；也可传 WorkRally 产出的短链（如 `result_url`）。纯文生图省略
- **每次生成数量**：固定 1 张
- 调用 `invoke` 时只需传 `product_id` + `prompt`（及可选的 `aspect_ratio` / `input_images`）

视频生成属于独立的 `workrally-video` Skill，请使用 `video-generation` product_id。
