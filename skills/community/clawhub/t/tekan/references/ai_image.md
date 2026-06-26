# AI Image 模块

从文字提示生成图片，或使用 AI 模型编辑现有图片。

## 支持的任务类型

| 类型 | 说明 | 必需参数 |
|------|-------------|-----------------|
| `text2image` | **文字生图** — 从文字提示生成图片 | `--model`, `--prompt`, `--aspect-ratio` |
| `image_edit` | **图片编辑** — 通过提示词 + 参考图片编辑图片 | `--model`, `--prompt`, `--aspect-ratio`, `--input-images` |

## 子命令

| 子命令 | 使用场景 | 轮询？ |
|------------|-------------|--------|
| `run` | **默认。** 新请求，从提交到完成 | 是 — 等待至完成 |
| `submit` | 批量：提交多个任务不等待 | 否 — 立即退出 |
| `query` | 恢复：对已有的 `taskId` 继续轮询 | 是 — 等待至完成 |
| `list-models` | 查看模型、约束条件和支持的宽高比 | 否 |
| `estimate-cost` | 执行前估算积分费用 | 否 |

## 用法

```bash
python {baseDir}/scripts/ai_image.py <subcommand> --type <text2image|image_edit> [options]
```

## 示例

### 列出模型

```bash
python {baseDir}/scripts/ai_image.py list-models --type text2image
python {baseDir}/scripts/ai_image.py list-models --type image_edit --json
```

### 文字生图

```bash
python {baseDir}/scripts/ai_image.py run \
  --type text2image \
  --model "Nano Banana 2" \
  --prompt "黄昏时分的未来都市天际线，霓虹灯倒映在潮湿的街道上" \
  --aspect-ratio "16:9" \
  --resolution "2K" \
  --count 2
```

固定价格模型（无需指定分辨率）：

```bash
python {baseDir}/scripts/ai_image.py run \
  --type text2image \
  --model "GPT Image 1.5" \
  --prompt "一只猫的水彩画" \
  --aspect-ratio "1:1"
```

### 图片编辑

```bash
python {baseDir}/scripts/ai_image.py run \
  --type image_edit \
  --model "Nano Banana 2" \
  --prompt "将背景替换为雪山风景" \
  --aspect-ratio "auto" \
  --resolution "2K" \
  --input-images photo.jpg
```

多图参考：

```bash
python {baseDir}/scripts/ai_image.py run \
  --type image_edit \
  --model "Nano Banana 2" \
  --prompt "融合两张图片的风格" \
  --aspect-ratio "1:1" \
  --resolution "2K" \
  --input-images style.jpg content.jpg \
  --count 2
```

### 费用估算

```bash
python {baseDir}/scripts/ai_image.py estimate-cost \
  --type text2image --model "Nano Banana 2" --resolution "2K" --count 2
```

### 下载结果

```bash
python {baseDir}/scripts/ai_image.py run \
  --type text2image --model "Nano Banana 2" \
  --prompt "北极光" --aspect-ratio "16:9" --resolution "2K" \
  --output-dir ./results
```

## 选项

| 选项 | 说明 |
|--------|-------------|
| `--type` | `text2image` 或 `image_edit`（必需） |
| `--model` | 模型 **display name**（必需） |
| `--prompt` | 文字提示词（必需） |
| `--aspect-ratio` | 宽高比（必需），如 `"16:9"`、`"1:1"`、`"auto"` |
| `--resolution` | `"512p"`、`"1K"`、`"2K"`、`"4K"` — 取决于模型 |
| `--count` | 图片数量（1-4，默认：1） |
| `--board-id` | 看板 ID |
| `--input-images` | 参考图片 fileId 或本地路径，多个用空格分隔（仅 image_edit）。例如 `--input-images photo.jpg` 或 `--input-images style.jpg content.jpg` |
| `--timeout` | 最大轮询时间（默认：300） |
| `--interval` | 轮询间隔（默认：3） |
| `--output-dir` | 将结果下载到指定目录 |
| `--json` | 输出完整 JSON 响应 |
| `-q, --quiet` | 静默模式，抑制 stderr 状态消息 |

## 模型推荐

> **全能图片模型 V2 是所有图片任务的首选推荐。**
> 综合画质最佳，支持 14 种宽高比、最高 4K、编辑时支持 14 张参考图。
>
> 向用户展示模型时使用展示名称，构造命令时使用 API 名称。完整映射见 [model_mapping.md](model_mapping.md)。

| 使用场景 | 推荐模型（展示名） | 对应 API 名称 | 原因 |
|----------|--------------------|---|-----|
| **综合最佳（默认）** | **全能图片模型 V2** | `Nano Banana 2` | 综合最强模型 |
| **低预算** | Seedream 4.0 (0.15/张) | `Seedream 4.0` | 最低费用 |
| **无需指定分辨率** | 强语义理解模型 V1.5, 强上下文一致性模型 pro | `GPT Image 1.5`, `Kontext-Pro` | 无需 resolution 参数 |
| **自动宽高比** | Seedream 5.0, Seedream 4.5 | `Seedream 5.0`, `Seedream 4.5` | 支持 `auto` ratio |

**默认选择：**
- text2image → 全能图片模型 V2（API: `Nano Banana 2`）
- image_edit → 全能图片模型 V2（API: `Nano Banana 2`）

## 注意事项

- `aspectRatio` 始终必需；image_edit 模型额外支持 `"auto"`
- `resolution` 部分模型必需，部分模型禁止 — 通过 `list-models` 检查
- **照片级写实模型 V4**（API: `Imagen 4`）仅支持 text2image，不支持 image_edit
