# 去背景工作流

将此工作流用于透明人物、道具、图标和 UI 资产。

## 为抠图生成素材

模型无法可靠生成透明通道时，要求使用不出现在主体中的纯色抠图背景。背景不得包含
场景、纹理、阴影、渐变、边框或棋盘格。保留主体精细边缘和预期的内部镂空。不得要求
烘焙在图片中的透明棋盘格，它可能成为最终图像的一部分。

## CLI 处理

对于生成图片，不需要保留原始交付物时使用 `--post-process remove-background`：

```bash
seagames-cli image generate \
  --model nano_banana_pro \
  --prompt "纯净平整的抠图背景上的玻璃瓶；保留精细边缘" \
  --post-process remove-background \
  --output ./assets/bottle.png
```

对于已有资源：

```bash
seagames-cli image remove-background \
  --resource-id res_generated_image \
  --output ./assets/transparent.png
```

后续命令需要资源或任务 ID 时使用 `--json`。可能需要审核或重新生成时，将原始交付物和处理结果都保留在暂存目录中。

## 审核

在浅色和深色背景上检查结果。重点检查头发、缝线、手指、细小配饰、帽檐、纽扣、面部线条和预期的内部孔洞。去背景造成主体像素丢失、留下彩边或将内部线条变为透明时，拒绝结果并改用其他抠图背景色重新生成。

不得对整张图片全局色键或手工扩大蒙版。透明结果通过审核后，才可执行立绘对齐。

## 超强 AI 抠图（0.3.1）

用户明确要求“超强 AI 抠图”时使用 `image strong-cutout`。它与 `image remove-background` 是不同功能；`--post-process remove-background` 仍使用普通抠图。

输入为一张已上传图片的资源 ID。本地图片先使用 `image upload --file PATH --json` 上传并获取资源 ID；本命令不依赖画布。模型、提示词、质量、透明背景及处理尺寸由服务端固定，不传 `--model` 或 `--prompt`。不要根据普通生图价格推算费用；报价与启用状态以实时服务为准。

先查询报价，不创建生成任务：

```bash
seagames-cli image strong-cutout --resource-id RESOURCE_ID --quote-only --json
```

提交、等待并下载透明 WebP：

```bash
seagames-cli image strong-cutout --resource-id RESOURCE_ID --output ./art_output/cutout.webp --json
```

支持 `--wait`、`--download`、`--output`、`--overwrite`、`--poll-interval`、`--timeout`、`--project-id`、`--idempotency-key`、`--api-url`、`--session-file` 和 `--json`。`--quote-only` 始终返回 JSON，不能与等待或下载参数组合。`--output` 隐含等待和下载；输出请用 `.webp`。原图保持不变，检查透明通道和主体边缘后再使用结果。

CLI 在提交前输出幂等键，接受任务后输出任务 ID。提交响应丢失或等待超时时保留这些信息；有任务 ID 时用 `image task get --task-id TASK_ID` 查询，不要重新生成。没有任务 ID 时先核对历史任务，禁止换一个新幂等键盲目重试。同一个幂等键只用于同一次请求。
