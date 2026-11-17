# 产品定价

## 当前可用产品

| product_id | 服务内容 | 单价 |
|------------|----------|------|
| `video-generation` | WorkRally视频生成 | 6.88 元/次 |

## 价格说明

- **定价方**：SkillHub 后台（价格以平台后台配置为准）
- **单位**：人民币元；下单时以分为单位（1 元 = 100 分）
- **次数**：每次生成任务对应一次扣费；当前每次固定生成 1 个结果

## 生成规格（云端设定）

- **时长 / 分辨率**：720p / 默认 10 秒。调用方无需指定 `model`，即使传入也会被云端配置覆盖
- **时长**：仅当用户明确指定秒数时传 `duration`；未指定时默认 10 秒
- **参考图**：单图生视频时传 `single_image_url`，本地图片以 `data:image/<ext>;base64,<...>` 内联（云端自动上传）；也可传 WorkRally 产出的短链（如 `result_url`）。纯文生视频省略
- **每次生成数量**：固定 1 条
- 调用 `invoke` 时只需传 `product_id` + `prompt`（及可选的 `duration` / `single_image_url`）

## 后续规划（暂未开放）

| product_id | 服务内容 |
|------------|----------|
| `subject-to-video` | 参考主体生视频 |

未开放的 `product_id` 调用 `invoke` 会返回 400（`INVALID_PRODUCT_ID`）。
图片生成属于独立的 `workrally-image` Skill，请使用 `image-generation` product_id。
