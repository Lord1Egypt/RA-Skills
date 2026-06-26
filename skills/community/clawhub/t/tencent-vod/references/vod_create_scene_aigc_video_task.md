# vod_create_scene_aigc_video_task — 详细参数与示例
> 此文件由 references 拆分生成，对应脚本：`scripts/vod_create_scene_aigc_video_task.py`

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `--storage-mode Permanent` | `--output-storage-mode Permanent` | 存储模式参数名以 `--output-` 开头 |
| `--scene-type showcase` | `--scene-type product_showcase` | 场景类型必须使用完整枚举值 |
| `--camera ZoomIn` | `--camera-movement ZoomIn` | 镜头运动参数名为 `--camera-movement` |
| `--duration 10` | `--duration 4/6/8` | 视频时长只支持 4、6、8 秒三档 |
| `--aspect-ratio 1:1` | `--aspect-ratio 16:9 或 9:16` | 产品展示场景仅支持 16:9 和 9:16 |
| 未提供 FileId 直接生成 | 先上传图片获取 FileId | 用户未提供图片时必须追问，不得使用占位符 |

## 参数说明


基于 `CreateSceneAigcVideoTask` API，支持产品360度展示等场景化视频生成。

### 通用参数（`generate` 子命令）

> ⚠️ `--sub-app-id`、`--region`、`--no-wait`、`--max-wait` 仅 `generate` 子命令支持；`--json`、`--dry-run` 在 `generate` 和 `query` 子命令中均支持。

| 参数 | 类型 | 说明 |
|------|------|------|
| `--sub-app-id` | int | 点播应用 ID（**必填**，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--region` | string | 地域，默认 `ap-guangzhou` |
| `--json` | flag | JSON 格式输出 |
| `--dry-run` | flag | 预览请求参数，不调用 API |
| `--no-wait` | flag | 仅提交任务，不等待结果（默认自动等待） |
| `--max-wait` | int | 最大等待时间（秒，默认 1800） |

### generate 参数（创建场景化生视频任务）

#### 必需参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--scene-type` | enum | ✅ | AI生视频场景类型：`product_showcase`（产品360度展示） |

#### 输入文件参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--input-files` | string list | - | 输入图片列表，格式：`File:FileId` 或 `Url:URL` |

> **输入图片要求**：
> - 支持的图片格式：jpg、jpeg、png、webp
> - 推荐使用小于 7M 的图片

#### 产品展示场景参数（scene-type=product_showcase）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--camera-movement` | enum | - | 镜头运动方式：`AutoMatch`（自动匹配）、`ZoomIn`（推进）、`ZoomOut`（拉远）、`GlideRight`（右移）、`GlideLeft`（左移）、`CraneDown`（下降） |

#### 输出配置参数（OutputConfig）

| 参数 | 类型 | 说明 |
|------|------|------|
| `--output-storage-mode` | enum | 存储模式：`Permanent`（永久存储）、`Temporary`（临时存储，默认） |
| `--media-name` | string | 输出文件名（最长 64 字符） |
| `--class-id` | int | 分类 ID（默认 0） |
| `--expire-time` | string | 过期时间（ISO 8601 格式，如 `2026-12-31T23:59:59+08:00`） |
| `--aspect-ratio` | enum | 视频宽高比：`16:9`、`9:16` |
| `--duration` | int | 视频时长（秒）：`4`、`6`、`8` |

#### 其他可选参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--prompt` | string | 用户自定义 prompt |
| `--session-id` | string | 用于去重的识别码（最长 50 字符，3天内重复会返回错误） |
| `--session-context` | string | 来源上下文，用于透传用户请求信息（最长 1000 字符） |
| `--tasks-priority` | int | 任务优先级（-10 到 10，数值越大优先级越高，默认 0） |
| `--ext-info` | string | 保留字段，特殊用途时使用 |

### query 参数（查询任务）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--task-id` | string | ✅ | 任务 ID |
| `--sub-app-id` | int | - | 子应用 ID（也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--region` | string | - | 地域，默认 `ap-guangzhou` |
| `--json` | flag | - | JSON 格式输出 |
| `--dry-run` | flag | - | 预览请求参数，不调用 API |

### 数据结构说明

#### SceneInfo 场景信息

```json
{
  "Type": "product_showcase",
  "ProductShowcaseConfig": {
    "CameraMovement": "AutoMatch"
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `Type` | string | 场景类型：`product_showcase` |
| `ProductShowcaseConfig` | object | 产品展示配置（Type=product_showcase 时有效） |

#### ProductShowcaseConfig 产品展示配置

| 字段 | 类型 | 说明 |
|------|------|------|
| `CameraMovement` | string | 镜头运动方式：`AutoMatch`、`ZoomIn`、`ZoomOut`、`GlideRight`、`GlideLeft`、`CraneDown` |

#### FileInfos 文件信息

```json
[
  {"Type": "File", "FileId": "3704211xxx509819"},
  {"Type": "Url", "Url": "https://example.com/img.jpg"}
]
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `Type` | string | 类型：`File`（点播媒体文件）、`Url`（可访问的 URL） |
| `FileId` | string | 媒体文件 ID（Type=File 时必填） |
| `Url` | string | 文件 URL（Type=Url 时必填） |

#### OutputConfig 输出配置

```json
{
  "StorageMode": "Temporary",
  "MediaName": "output.mp4",
  "ClassId": 0,
  "ExpireTime": "2026-12-31T23:59:59+08:00",
  "AspectRatio": "16:9",
  "Duration": 6
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `StorageMode` | string | 存储模式 |
| `MediaName` | string | 输出文件名 |
| `ClassId` | int | 分类 ID |
| `ExpireTime` | string | 过期时间 |
| `AspectRatio` | string | 视频宽高比：`16:9`、`9:16` |
| `Duration` | int | 视频时长（秒）：4、6、8 |

### 任务状态说明

| 状态 | 说明 |
|------|------|
| `PROCESSING` | 处理中 |
| `SUCCESS` | 成功 |
| `FAIL` | 失败 |

### API 接口对应关系

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 创建场景化 AIGC 视频任务 | `CreateSceneAigcVideoTask` | https://cloud.tencent.com/document/api/266/127542 |
| 查询任务详情 | `DescribeTaskDetail` | https://cloud.tencent.com/document/api/266/33431 |

### 错误码说明

| 错误类型 | 原因 | 处理建议 |
|---------|------|---------|
| MissingParameter | 缺少必需参数 | 检查 SubAppId 和 SceneInfo 是否提供 |
| InvalidParameterValue.SceneType | 场景类型不支持 | 使用支持的场景类型：product_showcase |
| InvalidParameterValue.AspectRatio | 宽高比不支持 | 产品展示场景支持 16:9、9:16 |
| InvalidParameterValue.Duration | 视频时长不支持 | 支持 4、6、8 秒 |
| InvalidParameterValue.CameraMovement | 镜头运动方式不支持 | 使用支持的值：AutoMatch/ZoomIn/ZoomOut/GlideRight/GlideLeft/CraneDown |
| InvalidParameterValue.FileInfos | 输入图片格式错误 | 检查图片格式是否为 jpg/jpeg/png/webp |
| InvalidParameter | 参数格式错误 | 检查 FileInfos 格式是否为 Type:Value |
| LimitExceeded | 频率限制 | 默认 20次/秒 |

---


---


## 使用示例


基于 `CreateSceneAigcVideoTask` API，支持产品360度展示等场景化视频生成。

### 产品360度展示场景

#### 基础产品展示（自动镜头）
```bash
python scripts/vod_create_scene_aigc_video_task.py generate \
    --sub-app-id 251007502 \
    --scene-type product_showcase \
    --input-files "File:3704211509819" \
    --camera-movement AutoMatch
```

#### 推进镜头效果
```bash
python scripts/vod_create_scene_aigc_video_task.py generate \
    --sub-app-id 251007502 \
    --scene-type product_showcase \
    --input-files "File:3704211509819" \
    --camera-movement ZoomIn \
    --aspect-ratio 16:9 \
    --duration 6
```

#### 拉远镜头效果
```bash
python scripts/vod_create_scene_aigc_video_task.py generate \
    --sub-app-id 251007502 \
    --scene-type product_showcase \
    --input-files "File:3704211509819" \
    --camera-movement ZoomOut \
    --aspect-ratio 9:16 \
    --duration 8
```

#### 左右平移镜头
```bash
# 右移
python scripts/vod_create_scene_aigc_video_task.py generate \
    --sub-app-id 251007502 \
    --scene-type product_showcase \
    --input-files "File:3704211509819" \
    --camera-movement GlideRight \
    --aspect-ratio 16:9

# 左移
python scripts/vod_create_scene_aigc_video_task.py generate \
    --sub-app-id 251007502 \
    --scene-type product_showcase \
    --input-files "File:3704211509819" \
    --camera-movement GlideLeft \
    --aspect-ratio 16:9
```

#### 下降镜头效果
```bash
python scripts/vod_create_scene_aigc_video_task.py generate \
    --sub-app-id 251007502 \
    --scene-type product_showcase \
    --input-files "File:3704211509819" \
    --camera-movement CraneDown \
    --aspect-ratio 9:16 \
    --duration 4
```

#### 使用 URL 图片
```bash
python scripts/vod_create_scene_aigc_video_task.py generate \
    --sub-app-id 251007502 \
    --scene-type product_showcase \
    --input-files "Url:https://example.com/product.jpg" \
    --camera-movement AutoMatch \
    --aspect-ratio 16:9
```

#### 永久存储生成的视频
```bash
python scripts/vod_create_scene_aigc_video_task.py generate \
    --sub-app-id 251007502 \
    --scene-type product_showcase \
    --input-files "File:3704211509819" \
    --camera-movement AutoMatch \
    --aspect-ratio 16:9 \
    --duration 6 \
    --output-storage-mode Permanent \
    --media-name "产品360展示视频" \
    --class-id 100
```

#### 指定过期时间
```bash
python scripts/vod_create_scene_aigc_video_task.py generate \
    --sub-app-id 251007502 \
    --scene-type product_showcase \
    --input-files "File:3704211509819" \
    --camera-movement ZoomIn \
    --aspect-ratio 16:9 \
    --duration 6 \
    --expire-time "2026-12-31T23:59:59+08:00"
```

#### 添加自定义 Prompt
```bash
python scripts/vod_create_scene_aigc_video_task.py generate \
    --sub-app-id 251007502 \
    --scene-type product_showcase \
    --input-files "File:3704211509819" \
    --camera-movement AutoMatch \
    --aspect-ratio 16:9 \
    --duration 6 \
    --prompt "高端产品展示，专业灯光效果"
```

---

### 查询任务

#### 基础查询
```bash
python scripts/vod_create_scene_aigc_video_task.py query \
    --task-id "251441341-AigcVideoTask-abc123"
```

#### 指定子应用查询
```bash
python scripts/vod_create_scene_aigc_video_task.py query \
    --task-id "251441341-AigcVideoTask-abc123" \
    --sub-app-id 251007502
```

#### JSON 格式输出
```bash
python scripts/vod_create_scene_aigc_video_task.py query \
    --task-id "251441341-AigcVideoTask-abc123" \
    --json
```

---

