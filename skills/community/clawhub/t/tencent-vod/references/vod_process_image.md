# vod_process_image — 详细参数与示例

> 此文件对应脚本：`scripts/vod_process_image.py`
>
> 支持子命令：`super-resolution`（图片超分增强）、`understand`（图片理解）

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `vod_process_image_async.py --url ...` | `vod_process_image.py super-resolution --file-id ...` | 不存在 `vod_process_image_async.py`，也没有 `async` 子命令，超分用 `super-resolution`，图片理解用 `understand` |
| `vod_process_image.py async --template-id 7` | `vod_process_image.py super-resolution --template-id 7` | 没有 `async` 子命令，直接用 `super-resolution --template-id` 指定模板 |
| `--priority 5` | `--tasks-priority 5` | **🚨 任务优先级参数名是 `--tasks-priority`，不是 `--priority`** |

## 参数说明

### super-resolution 参数（图片超分增强）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 图片文件 FileId（必填） |
| `--sub-app-id` | int | - | VOD 子应用 ID（2023-12-25 后开通的必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--mode` | enum | - | 超分模式：`percent`（倍率放大，默认）/ `fixed`（固定分辨率）/ `aspect`（比例适配） |
| `--percent` | float | - | 放大倍率（`mode=percent` 时有效，默认 2.0） |
| `--width` | int | - | 目标宽度（`mode=fixed` 或 `mode=aspect` 时有效） |
| `--height` | int | - | 目标高度（`mode=fixed` 或 `mode=aspect` 时有效） |
| `--sr-type` | enum | - | 超分类型：`standard`（通用超分，速度快）/ `super`（高级超分，画质更好，默认） |
| `--output-format` | enum | - | 输出格式：`JPEG`/ `PNG`/ `BMP`/ `WebP` |
| `--quality` | int | - | 输出图片质量（JPEG/WebP 有效，1-100） |
| `--template-id` | int | - | 直接指定已有超分模板 ID（与 `--mode`/`--percent` 等互斥） |
| `--template-name` | string | - | 自定义模板名称（创建新模板时使用） |
| `--template-comment` | string | - | 自定义模板描述 |
| `--session-id` | string | - | 去重识别码（三天内相同 ID 的请求会返回错误） |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |
| `--region` | string | - | 地域（默认 `ap-guangzhou`） |
| `--no-wait` | flag | - | 仅提交任务，不等待结果（默认自动等待） |
| `--max-wait` | int | - | 最大等待时间（秒，默认 300） |
| `--json` | flag | - | JSON 格式输出 |
| `--dry-run` | flag | - | 预览请求参数，不实际执行 |

> 目标分辨率不超过 4096x4096。

---

### understand 参数（图片理解）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | - | 图片文件 FileId（与 `--url`、`--base64` **三选一必填**） |
| `--url` | string | - | 图片 URL（与 `--file-id`、`--base64` **三选一必填**） |
| `--base64` | string | - | 图片 Base64 编码（与 `--file-id`、`--url` **三选一必填**，文件需 <4MB） |
| `--sub-app-id` | int | ✅ | VOD 子应用 ID（必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--prompt` | string | - | 自定义提示词（默认"理解这张图片"） |
| `--model` | string | - | 模型：`gemini-2.5-flash`/ `gemini-2.5-flash-lite`/ `gemini-2.5-pro`/ `gemini-3-flash`/ `gemini-3-pro` |
| `--output-name` | string | - | 输出文件名称 |
| `--class-id` | int | - | 分类 ID |
| `--expire-time` | string | - | 过期时间（ISO 8601 格式，如 `2025-12-31T23:59:59Z`） |
| `--session-id` | string | - | 去重识别码，三天内相同 ID 的请求会返回错误 |
| `--session-context` | string | - | 来源上下文，透传用户请求信息 |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |
| `--ext-info` | string | - | 扩展信息（JSON 字符串，如指定模型名称） |
| `--region` | string | - | 地域（默认 `ap-guangzhou`） |
| `--no-wait` | flag | - | 仅提交任务，不等待结果（默认自动等待） |
| `--max-wait` | int | - | 最大等待时间（秒，默认 120） |
| `--json` | flag | - | JSON 格式输出 |
| `--dry-run` | flag | - | 预览请求参数，不实际执行 |

---

## 使用示例

### super-resolution 示例

```bash
# 默认 2 倍高级超分（自动等待完成）
python scripts/vod_process_image.py super-resolution \
    --file-id <file-id> --sub-app-id <sub-app-id>

# 固定分辨率超分到 1920x1080，JPEG 输出
python scripts/vod_process_image.py super-resolution \
    --file-id <file-id> --sub-app-id <sub-app-id> \
    --mode fixed --width 1920 --height 1080 --output-format JPEG

# 3 倍通用超分，PNG 输出，指定图片质量
python scripts/vod_process_image.py super-resolution \
    --file-id <file-id> --sub-app-id <sub-app-id> \
    --percent 3.0 --sr-type standard --output-format PNG --quality 90

# 不等待，立即返回任务 ID
python scripts/vod_process_image.py super-resolution \
    --file-id <file-id> --sub-app-id <sub-app-id> \
    --json
```

### understand 示例

```bash
# 图片理解（默认提示词）
python scripts/vod_process_image.py understand \
    --file-id <file-id> --sub-app-id 1500046154

# 自定义提示词图片理解
python scripts/vod_process_image.py understand \
    --file-id <file-id> --sub-app-id 1500046154 \
    --prompt "描述图片中的人物表情和动作"

# 通过 URL 输入 + 指定模型
python scripts/vod_process_image.py understand \
    --url "https://example.com/image.jpg" --sub-app-id 1500046154 \
    --model gemini-2.5-pro --prompt "分析构图和色彩"

# 不等待（立即返回任务 ID）
python scripts/vod_process_image.py understand \
    --file-id <file-id> --sub-app-id 1500046154 \
    --json
```

---

## API 接口

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 图片超分（创建模板） | `CreateProcessImageAsyncTemplate` | https://cloud.tencent.com/document/product/266/127862 |
| 图片超分（发起任务）/ 图片理解 / 异步处理 | `ProcessImageAsync` | https://cloud.tencent.com/document/api/266/127858 |
