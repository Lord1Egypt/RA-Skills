# vod_pull_upload — 详细参数与示例

> 此文件对应脚本：`scripts/vod_pull_upload.py`
>
> 🚨 **强制规则**：从 URL 拉取上传，**推荐且优先**使用此专用脚本（无子命令，直接跟参数）。`vod_upload.py` 也有 `pull` 子命令可用，但推荐使用本专用脚本。

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `vod_pull_upload.py pull --url ...` | `vod_pull_upload.py --url ...` | **无子命令**，直接 `--url` |
| `vod_upload.py --url ...` | `vod_pull_upload.py --url ...` | 拉取上传用专用脚本 `vod_pull_upload.py` |

### 📌 媒体名称（--media-name）推断规则

> 🚨 **强制规则**：当用户提供的"媒体名称"实际上是一个 URL（如 `https://example.com/video.mp4`）时，**不得追问**，应自动从 URL 路径末尾提取文件名作为媒体名称（如 `video.mp4`），直接生成命令。
>
> | 用户表述 | 处理方式 |
> |---------|---------|
> | `指定媒体名称 https://example.com/video.mp4` | 自动提取 `video.mp4` 作为 `--media-name` |
> | `媒体名称为 https://example.com/my-clip.mp4` | 自动提取 `my-clip.mp4` 作为 `--media-name` |
> | `媒体名称为"产品宣传片"` | 直接使用用户提供的名称 |

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--url` | string | ✅ | 媒体 URL（必需） |
| `--media-name` | string | - | 媒体名称 |
| `--media-type` | string | - | 媒体类型（如 mp4、mp3，默认根据 URL 自动推断） |
| `--cover-url` | string | - | 封面 URL |
| `--class-id` | int | - | 分类 ID（默认 0） |
| `--procedure` | string | - | 任务流模板名（拉取完成后自动发起任务流） |
| `--expire-time` | string | - | 过期时间（ISO 8601 格式，如 `2025-12-31T23:59:59Z`） |
| `--storage-region` | string | - | 存储园区（如 `ap-chongqing`） |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10，默认 0） |
| `--session-context` | string | - | 会话上下文，透传用户请求信息（最长 1000 字符） |
| `--session-id` | string | - | 去重识别码，三天内相同 ID 的请求会返回错误（最长 50 字符） |
| `--source-context` | string | - | 来源上下文，透传用户请求信息（最长 250 字符） |
| `--ext-info` | string | - | 保留字段，特殊用途时使用 |
| `--media-storage-path` | string | - | 媒体存储路径（以 `/` 开头，仅 FileID+Path 模式子应用可用） |
| `--sub-app-id` | int | - | VOD 子应用 ID（2023-12-25 后开通的必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--app-name` | string | - | 通过应用名称/描述模糊匹配子应用（与 `--sub-app-id` 互斥） |
| `--region` | string | - | 地域（默认 `ap-guangzhou`） |
| `--no-wait` | flag | - | 仅提交任务，不等待结果（默认自动等待） |
| `--max-wait` | int | - | 最大等待时间（秒，默认 600） |
| `--json` | flag | - | JSON 格式输出完整响应 |
| `--dry-run` | flag | - | 预览请求参数，不实际执行 |

---

## 使用示例

#### 基础拉取上传
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4"
```

#### 指定媒体名称
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
    --media-name "拉取的视频"
```

#### 指定媒体类型（URL 无扩展名时）
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video" \
    --media-type mp4
```

#### 指定封面
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
    --cover-url "https://example.com/cover.jpg"
```

#### 拉取后自动执行任务流
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
    --procedure "MyProcedure"
```

#### 等待任务完成
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \

```

#### 等待任务完成（自定义超时）
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
 \

```

#### 设置任务优先级
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
    --tasks-priority 5
```

#### 去重识别码（防止重复提交）
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
    --session-id "my-unique-id-001"
```

#### JSON 格式输出（含等待结果）
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
 \
    --json
```

#### dry-run 预览参数
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.mp4" \
    --media-name "拉取视频" \
 \
    --dry-run
```

#### 拉取 HLS 流
```bash
python scripts/vod_pull_upload.py \
    --url "https://example.com/video.m3u8" \
    --media-name "HLS流"
```

---

## API 接口

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| URL 拉取上传 | `PullUpload` | https://cloud.tencent.com/document/api/266/35575 |
| 查询任务状态 | `DescribeTaskDetail` | https://cloud.tencent.com/document/api/266/33431 |
