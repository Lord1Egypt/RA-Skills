---
name: add-preset
description: "使用预设片段（preset）把已上传的预设模板插入到草稿并替换其中元素。适用于模板化替换素材、快速复用复杂包装效果。用户提到“预设片段/套预设”时必须优先使用本技能。"
---

# Add Preset Skill

用于在 VectCut 草稿中使用“预设片段（preset）”。预设是提前在剪映里编辑好的模板，可由图片、视频、文字、关键帧、音效等组合而成。`add-preset` 只负责“使用已上传预设”，不负责上传预设文件。

官方文档：
- https://docs.vectcut.com/372375099e0

接口地址：
- `POST https://open.vectcut.com/cut_jianying/add_preset`

## 何时使用

- 用户需要基于模板替换某些素材（图、视频、文案等）
- 用户只想单独使用一个预设并替换单个字段（如 `preset_id=xxx`，把 `text1` 改为 `"123"`）
- 用户要通过多个预设叠加实现复杂效果（如口播字幕、画中画、特效组合）

## 预设上传边界（必须遵守）

- 预设上传必须在客户端完成，`add-preset` 不提供上传能力
- 当用户还没有 `preset_id` 时，必须先引导用户去客户端上传并拿到 `preset_id`
- 只有拿到有效 `preset_id` 后，才进入预设使用流程

## 使用前置（必须）

- 检查 `VECTCUT_API_KEY`，缺失或失效时先走 `vectcut-login`
- 请求前先阅读官方文档：https://docs.vectcut.com/372375099e0
- 严格按文档确认该 `preset_id` 支持替换的元素类型与参数结构

## 核心输入

- 必填：`preset_id`（客户端上传后返回的预设 ID）
- 可选：`draft_id`（目标草稿 ID；为空时由接口默认创建新草稿）
- 可选：预设片段插入到草稿轨道上的目标时间`target_start`, 原始预设片段的截取时间`start`, `end`
- 可选：预设内元素替换参数（如图片/视频/文字替换映射）

说明：
- 不同预设允许替换的元素和字段不同，必须按照用户要求的字段进行替换

## 调用示例

`curl` 示例：

```bash
curl --location 'https://open.vectcut.com/cut_jianying/add_preset' \
  --header "Authorization: Bearer ${VECTCUT_API_KEY}" \
  --header 'Content-Type: application/json' \
  --data '{
    "preset_id": "b795a680-a581-4965-84b1-9e9ad313b522",
    "replacements": [
      {"text1": "流光剪辑"},
      {"image1": "https://player.install-ai-guider.top/example/mao.webp"},
      {"video1": "https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?file=092faf3c94244973ab752ee1280ba76f.mp4"}
    ],
    "target_start": 2,
    "draft_id": "draft_456",
    "transform_x": 0.5,
    "transform_y": 0.5,
    "rotation": 0,
    "scale_x": 1.0,
    "scale_y": 1.0,
    "track_name": "my_preset_track",
    "width": 1080,
    "height": 1920
  }'
```

脚本调用示例（推荐统一用脚本）：

```bash
python <skill-path>/scripts/add_preset.py \
  "/tmp/add_preset_payload.json" \
  --output "./add_preset_result.json"
```

单独使用预设（仅替换 `text1`，不传 `draft_id` 由接口新建草稿）示例：

```json
{
  "preset_id": "xxx",
  "replacements": [
    {"text1": "123"}
  ]
}
```

## 失败处理建议

- 无 `preset_id`：明确告知先去客户端上传预设，再返回继续执行
-  New segment overlaps错误，这表示目标轨道的目标时间范围已经有素材占位了，通常你需要设置track_name将当前预设放到其他轨道。
