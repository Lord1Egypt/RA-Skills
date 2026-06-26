# vod_upload — 详细参数与示例

> 此文件对应脚本：`scripts/vod_upload.py`
>
> 🚨 **强制规则**：本地文件上传使用 `vod_upload.py upload`；从 URL 拉取上传**推荐且优先**使用专用脚本 `vod_pull_upload.py`（无子命令，直接跟参数）。`vod_upload.py` 也有 `pull` 子命令可用，但推荐使用专用脚本。

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `--media-type image` | （不传 `--media-type`） | 媒体类型从扩展名自动推断 |
| `--url ...` | `vod_pull_upload.py --url ...` | 拉取上传用专用脚本 `vod_pull_upload.py` |
| （上传时未指定分类） | `upload --file xxx.mp4 --class-id <分类ID>` | **指定媒体分类时必须加 `--class-id`**，默认为 0（其他分类） |

## 参数说明

### 通用参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--region` | string | 地域，默认 `ap-guangzhou` |
| `--sub-app-id` | int | VOD 子应用 ID（2023-12-25 后开通的必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--app-name` | string | 通过应用名称/描述模糊匹配子应用（与 `--sub-app-id` 互斥） |
| `--json` | flag | JSON 格式输出完整响应 |
| `--dry-run` | flag | 预览参数，不调用 API |
| `--verbose` | flag | 显示详细上传信息 |

### upload 参数（本地文件上传）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file` | path | ✅ | 本地文件路径（必需） |
| `--media-name` | string | - | 媒体名称（默认使用文件名，不含扩展名） |
| `--media-type` | string | - | 媒体类型（如 mp4、mp3、jpg，默认根据文件扩展名自动推断） |
| `--cover-file` | path | - | 本地封面文件路径 |
| `--cover-type` | string | - | 封面类型（如 jpg、png，默认从封面文件扩展名推断） |
| `--class-id` | int | - | 分类 ID（默认 0） |
| `--procedure` | string | - | 任务流模板名（上传完成后自动发起任务流） |
| `--expire-time` | string | - | 过期时间（ISO 8601 格式，如 `2025-12-31T23:59:59Z`） |
| `--storage-region` | string | - | 存储园区（如 `ap-chongqing`） |
| `--source-context` | string | - | 来源上下文（透传用户请求信息，最长 250 字符） |
| `--concurrent-upload-number` | int | - | 分片并发上传数（针对大文件有效） |
| `--media-storage-path` | string | - | 媒体存储路径（以 `/` 开头，仅 FileID+Path 模式子应用可用） |

### 支持的媒体类型

**视频格式**：mp4、flv、avi、mkv、mov、wmv、webm、ts、m3u8、mpg、mpeg

**音频格式**：mp3、aac、flac、wav、ogg、m4a、wma

**图片格式**：jpg、jpeg、png、gif、bmp、webp

### API 接口对应关系

| 功能 | API 接口 | 文档链接 |
|------|---------|---------|
| 申请上传 | `ApplyUpload` | https://cloud.tencent.com/document/api/266/31767 |
| 确认上传 | `CommitUpload` | https://cloud.tencent.com/document/api/266/31766 |
| URL 拉取上传 | `PullUpload` | https://cloud.tencent.com/document/api/266/35575 |
| 查询任务状态 | `DescribeTaskDetail` | https://cloud.tencent.com/document/api/266/33431 |

### 上传流程说明

#### 本地文件上传流程
1. 调用 `ApplyUpload` 获取临时凭证和存储信息（StorageBucket、StorageRegion、MediaStoragePath、VodSessionKey）
2. 使用 COS SDK 将文件上传到指定路径
3. 调用 `CommitUpload` 确认上传，返回 FileId 和播放地址

### 错误码说明

| 错误类型 | 原因 | 处理建议 |
|---------|------|---------|
| 文件不存在 | 本地文件路径错误 | 检查文件路径是否正确 |
| 申请上传失败 | 参数错误或权限不足 | 检查 MediaType、SubAppId 等参数 |
| 上传到 COS 失败 | 临时凭证过期或网络问题 | 临时凭证有效期通常较短（< 1 小时），需重新申请 |
| 确认上传失败 | VodSessionKey 无效 | 使用 ApplyUpload 返回的 VodSessionKey |

### pull 参数（URL 拉取上传，建议使用 vod_pull_upload.py）

> 💡 `vod_upload.py pull` 与 `vod_pull_upload.py` 功能相同。推荐使用专用脚本 `vod_pull_upload.py`（无需子命令），参数完全一致，详见 `vod_pull_upload.md`。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--url` | string | ✅ | 媒体 URL（必需） |
| `--media-name` | string | - | 媒体名称 |
| `--media-type` | string | - | 媒体类型（如 mp4、mp3，默认根据 URL 自动推断） |
| `--cover-url` | string | - | 封面 URL |
| `--class-id` | int | - | 分类 ID（默认 0） |
| `--procedure` | string | - | 任务流模板名 |
| `--expire-time` | string | - | 过期时间（ISO 8601 格式） |
| `--storage-region` | string | - | 存储园区（如 `ap-chongqing`） |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10，默认 0） |
| `--session-context` | string | - | 会话上下文（透传用户请求信息，最长 1000 字符） |
| `--session-id` | string | - | 去重识别码（最长 50 字符，三天内相同 ID 返回错误） |
| `--ext-info` | string | - | 保留字段，特殊用途时使用 |
| `--source-context` | string | - | 来源上下文（透传用户请求信息，最长 250 字符） |
| `--media-storage-path` | string | - | 媒体存储路径（以 `/` 开头，仅 FileID+Path 模式子应用可用） |
| `--sub-app-id` | int | - | VOD 子应用 ID（也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--app-name` | string | - | 通过应用名称/描述模糊匹配子应用（与 `--sub-app-id` 互斥） |
| `--region` | string | - | 地域（默认 `ap-guangzhou`） |
| `--no-wait` | flag | - | 仅提交任务，不等待结果（默认自动等待） |
| `--max-wait` | int | - | 最大等待时间（秒，默认 600） |
| `--json` | flag | - | JSON 格式输出完整响应 |
| `--dry-run` | flag | - | 预览请求参数，不实际执行 |

---

## 使用示例

### 本地文件上传

#### 基础上传（自动推断媒体类型）
```bash
python scripts/vod_upload.py upload --file /path/to/video.mp4
```

#### 指定媒体名称
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --media-name "我的精彩视频"
```

#### 指定媒体类型
```bash
python scripts/vod_upload.py upload \
    --file video.mov \
    --media-type mp4 \
    --media-name "转换格式"
```

#### 上传时同时指定封面
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --cover-file /path/to/cover.jpg
```

#### 指定分类
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --class-id 10
```

#### 上传后自动执行任务流
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --procedure "LongVideoPreset"
```

#### 指定存储园区
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --storage-region ap-beijing
```

#### 指定存储路径（仅 FileID+Path 模式）
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --media-storage-path "/videos/2026-03/my-video.mp4"
```

#### 透传上下文信息
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --source-context "client:app_v1"
```

#### JSON 格式输出
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --json
```

#### 详细输出
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --verbose
```

#### dry-run 预览参数
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --media-name "我的视频" \
    --dry-run
```

---

### 不同媒体类型示例

#### 上传音频文件
```bash
python scripts/vod_upload.py upload \
    --file /path/to/audio.mp3 \
    --media-name "背景音乐"
```

#### 上传图片文件
```bash
python scripts/vod_upload.py upload \
    --file /path/to/image.jpg \
    --media-name "封面图片"
```

---

### 高级用法

#### 批量上传（使用 shell 循环）
```bash
for f in /path/to/videos/*.mp4; do
    python scripts/vod_upload.py upload --file "$f"
done
```

#### 上传并保存结果到文件
```bash
python scripts/vod_upload.py upload \
    --file /path/to/video.mp4 \
    --json > upload_result.json
```

#### 条件判断上传成功
```bash
RESULT=$(python scripts/vod_upload.py upload --file video.mp4 --json)
FILE_ID=$(echo "$RESULT" | jq -r '.commit.FileId')
if [ "$FILE_ID" != "null" ]; then
    echo "上传成功，FileId: $FILE_ID"
else
    echo "上传失败"
fi
```

> 🚨 **URL 拉取上传请使用 `vod_pull_upload.py`**，参数详见 `vod_pull_upload.md`。
