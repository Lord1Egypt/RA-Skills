---
name: generate-ai-image
description: "提交异步文生图/图生图任务并自动轮询结果，支持 compose_draft 分支（入草稿或仅返回图片）。当用户提到文生图、图生图、AI 生成图片、参考图生成、多图融合、按模型尺寸生成图片时必须使用本技能。"
---

# Generate AI Image Skill

用于调用 VectCut 异步生图接口，覆盖文生图、单图参考图生图、多图参考组合生成。

原始接口文档（必须作为本技能引用依据）：
- https://docs.vectcut.com/443760774e0
- https://docs.vectcut.com/443760775e0


## 何时使用

- 用户要“文生图”或“图生图”
- 用户要指定模型、分辨率、参考图数量
- 用户要异步提交任务并轮询拿最终图片
- 用户要决定是否把结果自动写入草稿（`compose_draft`）

## 前置条件

- Python 3
- 已安装 `requests`
- 环境变量 `VECTCUT_API_KEY` 可用
- 若 `VECTCUT_API_KEY` 缺失或失效，先调用 `vectcut-login`

## 关键行为

1. 读取请求 JSON 并做参数校验：
   - `prompt`、`model`、`size` 必填
   - 模型/分辨率按 `references/ai-image-model_capabilities.json` 校验
   - 参考图数量 `< 14`
   - 单张参考图必须使用 `reference_image`
   - 多张参考图必须使用 `reference_images`
   - 不支持参考图的模型禁止传参考图
2. `POST /llm/image/submit_task/generate` 提交异步任务
3. `GET /llm/image/submit_task/task_status?task_id=...` 轮询到 `success|failed`
4. 输出统一结果 JSON（图片 URL、草稿信息、原始返回）

## compose_draft 规则

- 默认 `compose_draft=true`：服务端会将生成图片添加进草稿（新建或复用 `draft_id`）
- 当 `compose_draft=true` 时，`start`、`end` 为必填
- `compose_draft=false`：只生成图片并返回结果，不写入草稿
- 当 `compose_draft=false` 时，与“加图进草稿”相关参数会被忽略（脚本会自动剔除并记录）

## 模型与分辨率枚举

为避免模型/尺寸校验逻辑过于分散，本技能提供独立枚举文件：
- `references/ai-image-model_capabilities.json`

用途：
- 统一维护模型别名（如 `gemini-3.1-flash-image` -> `nano_banana_2`）
- 每个模型支持的分辨率集合
- 是否支持参考图

如需同步新模型，只更新该枚举文件即可。

## 执行方式

先准备 payload 文件（示例：`/tmp/generate_ai_image_payload.json`）：

```json
{
  "prompt": "天空中一只老鹰飞过",
  "model": "seedream-5.0",
  "size": "1440x2560",
  "compose_draft": false
}
```

执行：

```bash
python <skill-path>/scripts/generate_ai_image_async.py \
  "/tmp/generate_ai_image_payload.json" \
  --output "./generated_ai_image_result.json"
```

可选参数：
- `--poll-interval`：轮询间隔秒数，默认 `2.0`
- `--timeout`：总超时秒数，默认 `600`
- `--capabilities`：模型能力枚举文件路径，默认使用内置文件

## 输出结果

默认输出 `generated_ai_image_result.json`，核心字段：
- `meta.task_id`
- `request_payload`
- `result.image`
- `result.draft_id`
- `result.draft_url`
- `result.raw_result`

## 与 add_image API 的关系

- `compose_draft=true` 时，服务端会按生图请求中的草稿参数完成“生图 + 入草稿”；这组草稿参数的字段定义、语义和取值规则与 `add_image` 接口一致（如 `start/end`、`track_name`、`transform_*`、`scale_*`、动画、转场、蒙版等）
- 若你已有现成图片 URL，需要单独加到草稿，请直接参考官方 API 文档：`https://docs.vectcut.com/320460206e0`

## 常见错误

- `缺少必要参数: prompt`：补齐提示词
- 模型或分辨率不匹配：调整 `model`/`size` 组合
- 参考图数量超限：减少到 `< 14`
- `VECTCUT_API_KEY` 缺失：先走 `vectcut-login`
