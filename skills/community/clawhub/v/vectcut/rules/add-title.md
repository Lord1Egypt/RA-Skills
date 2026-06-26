---
name: add-title
description: "使用 add_text 接口在视频中添加固定位置标题（通常位于口播画面下方标题位），支持字体与颜色规范化选择。用户提到“加标题”“视频标题条”“口播标题固定位置”“给草稿加标题文案”时必须使用本技能。"
---

# Add Title Skill

用于调用 VectCut `add_text` 接口在视频草稿里添加标题文本，默认采用固定标题位参数，适合口播、带货、讲解视频的主标题覆盖。

官方接口文档：
- https://docs.vectcut.com/321240978e0

## 何时使用

- 用户要求给视频加标题/主标题
- 用户要做固定位置标题栏
- 用户已有 `draft_id`，只需要补一条标题文字轨道

## 鉴权前置（必须）

- 检查 `VECTCUT_API_KEY`
- 缺失或疑似失效时，先调用 `vectcut-login`

## 默认布局（固定标题位）

基于你给的示例，默认参数如下：
- `track_name=text_title`
- `start=0.0`
- `transform_y_px=1240`
- `fixed_width=0.6`
- `shadow_enabled=true`
- `font_size=18`

## 字体与颜色规范

字体（建议从以下集合选择）：
- `思源粗宋`
- `俪金黑`
- `研宋体`
- `细体`

颜色（十六进制）：
- `#ffffff`
- `#ffa800`
- `#b71c1c`
- `#18893e`

## 执行方式

先准备请求 JSON，例如：

```json
{
  "draft_id": "dfd_xxx",
  "text": "新款上线",
  "end": 12.5,
  "font": "思源粗宋",
  "font_color": "#ffffff"
}
```

执行：

```bash
python <skill-path>/scripts/add_title.py \
  "/tmp/add_title_payload.json" \
  --output "./add_title_result.json"
```

## 输入说明

- 必填：
  - `draft_id`
  - `text`
  - `end`
- 可选：
  - `start`（默认 `0.0`）
  - `track_name`（默认 `text_title`）
  - `font`（默认 `思源粗宋`）
  - `font_color`（默认 `#ffffff`）
  - `font_size`（默认 `18`）
  - `transform_y_px`（默认 `1240`）
  - `fixed_width`（默认 `0.6`）
  - `shadow_enabled`（默认 `true`）

## 输出结果

默认输出 `add_title_result.json`，核心字段：
- `meta.endpoint`
- `meta.draft_id`
- `request_payload`
- `result.raw_response`

## 失败处理建议

- `draft_id` 缺失：先创建草稿或传入已有草稿
- `end <= start`：修正时间区间
- 字体/颜色不在建议集合：按技能推荐值回退
