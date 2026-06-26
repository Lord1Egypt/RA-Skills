# vod_process_media — 详细参数与示例
> 此文件由 references 拆分生成，对应脚本：`scripts/vod_process_media.py`

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `transcode --template same` | `transcode --quality same` | 极速高清转码用 `--quality` |
| `scene-transcode --resolution 720` | `transcode --quality hd` | 极速高清（TESHD）用 `transcode --quality`；场景转码用 `scene-transcode --scene` |
| `process --file-id <id> --animated-graphic-task-set ...` | `gif --file-id <id> --definition 10` | 转 GIF 用专用 `gif` 子命令，不存在 `process` 子命令 |
| `tccli vod ProcessMedia --AiAnalysisTask ...` | `python scripts/vod_process_media.py ai-analysis --file-id <id> --definition <id>` | AI 内容分析必须用 `ai-analysis` 子命令，**禁止使用 tccli**；`--definition` 是必填参数 |
| `tccli vod ProcessMedia --AiRecognitionTask ...` | `python scripts/vod_process_media.py ai-recognition --file-id <id> --definition <id>` | AI 内容识别必须用 `ai-recognition` 子命令，**禁止使用 tccli**；`--definition` 是必填参数 |
| `adaptive-streaming --subtitle-ids "z8gnlH,abc123"` | `adaptive-streaming --subtitle-set "z8gnlH,abc123"` | **🚨 自适应码流绑定字幕用 `--subtitle-set`，不是 `--subtitle-ids`** |

---

## 目录

- [通用参数](#通用参数所有子命令共享)
- [procedure — 任务流处理](#procedure-参数任务流处理)
- [transcode — 极速高清转码](#transcode-参数极速高清转码)
- [remux — 转封装](#remux-参数转封装)
- [enhance — 视频增强](#enhance-参数视频增强)
- [snapshot — 截图](#snapshot-参数截图)
- [gif — 转动图](#gif-参数转动图)
- [cover-by-snapshot — 截图做封面](#cover-by-snapshot-参数截图做封面)
- [adaptive-streaming — 自适应码流](#adaptive-streaming-参数自适应码流)
- [sample-snapshot — 采样截图](#sample-snapshot-参数采样截图)
- [image-sprite — 雪碧图](#image-sprite-参数雪碧图)
- [ai-review — AI 内容审核](#ai-review-参数ai-内容审核)
- [ai-analysis — AI 内容分析](#ai-analysis-参数ai-内容分析)
- [ai-recognition — AI 内容识别](#ai-recognition-参数ai-内容识别)
- [scene-transcode — 场景转码](#scene-transcode-参数场景转码)
- [使用示例](#使用示例)

---

## 参数说明

> 子命令列表：`procedure`、`transcode`、`remux`、`enhance`、`scene-transcode`、`snapshot`、`gif`、`sample-snapshot`、`image-sprite`、`cover-by-snapshot`、`adaptive-streaming`、`ai-review`、`ai-analysis`、`ai-recognition`

### 通用参数（所有子命令共享）

> 以下参数在所有子命令中均可使用，各子命令参数表不再重复列出。

| 参数 | 类型 | 说明 |
|------|------|------|
| `--sub-app-id` | int | 子应用 ID（2023-12-25 后开通的必填，也可通过环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 设置） |
| `--region` | string | 地域（默认 `ap-guangzhou`） |
| `--no-wait` | flag | 仅提交任务，不等待结果（默认自动等待） |
| `--max-wait` | int | 最大等待时间（秒，默认 600） |
| `--json` | flag | JSON 格式输出 |
| `--verbose` / `-v` | flag | 输出详细信息（含完整 API 响应） |
| `--dry-run` | flag | 预览请求参数，不实际执行 |

---

### procedure 参数（任务流处理）

> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--procedure` | string | ✅ | 任务流名称 |
| `--media-storage-path` | string | - | 媒体存储路径（仅 FileID+Path 模式子应用可用） |
| `--tasks-notify-mode` | enum | - | 任务流状态变更通知模式：`Finish` / `Change` / `None` |
| `--session-id` | string | - | 去重识别码（三天内重复会返回错误） |
| `--ext-info` | string | - | 扩展信息 |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |

---

### transcode 参数（极速高清转码）

> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--quality` | enum | - | 转码质量：`same`（同源，默认）/ `flu`（流畅 360P）/ `sd`（标清 540P）/ `hd`（高清 720P） |
| `--watermark-set` | string | - | 水印模板 ID 列表（逗号分隔，如 `10001,10002`） |
| `--session-context` | string | - | 透传来源上下文（最长 1000 字符） |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |

---

### remux 参数（转封装）

> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--target-format` | enum | ✅ | 目标封装格式：`mp4` / `hls` |
| `--session-context` | string | - | 来源上下文，用于透传用户请求信息 |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |

---

### enhance 参数（视频增强）

> 大模型增强V2，支持降噪+超分+综合增强，适用于通用/漫剧/真人短剧场景，720P 至 4K。  
> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--file-id` | string | ✅ | - | 媒体文件 ID |
| `--scene` | enum | - | `general` | 增强场景：`general`（通用）/ `anime`（漫剧）/ `live_action`（真人/短剧） |
| `--resolution` | enum | - | `1080` | 目标分辨率：`720` / `1080` / `2k` / `4k` |
| `--session-context` | string | - | - | 来源上下文（最长 1000 字符） |
| `--tasks-priority` | int | - | - | 任务优先级（-10 到 10） |

**场景说明：**

| 场景标识 | 适用内容 |
|---------|---------|
| `general` | 通用视频（默认） |
| `anime` | 漫剧/动漫 |
| `live_action` | 真人/短剧/影视 |

---

### snapshot 参数（截图）

> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--definition` | int | ✅ | 截图模板 ID |
| `--ext-time-offset-set` | string | - | 截图时间点列表（逗号分隔，如 `5s,10s,15s` 或 `10pct,20pct`） |
| `--watermark-set` | string | - | 水印模板 ID 列表（逗号分隔） |
| `--media-storage-path` | string | - | 媒体存储路径（仅 FileID+Path 模式子应用可用） |
| `--session-id` | string | - | 去重识别码（三天内重复会返回错误） |
| `--ext-info` | string | - | 扩展信息 |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |
| `--tasks-notify-mode` | enum | - | 通知模式：`Finish` / `Change` / `None` |

---

### gif 参数（转动图）

> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--definition` | int | ✅ | 转动图模板 ID |
| `--start-time` | float | - | 开始时间偏移（秒） |
| `--end-time` | float | - | 结束时间偏移（秒） |
| `--media-storage-path` | string | - | 媒体存储路径（仅 FileID+Path 模式子应用可用） |
| `--session-id` | string | - | 去重识别码 |
| `--ext-info` | string | - | 扩展信息 |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |
| `--tasks-notify-mode` | enum | - | 通知模式：`Finish` / `Change` / `None` |

---

### cover-by-snapshot 参数（截图做封面）

> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--definition` | int | ✅ | 截图模板 ID |
| `--position-type` | enum | ✅ | 截图方式：`Time`（时间点）/ `Percent`（百分比） |
| `--position-value` | float | ✅ | 截图位置（Time 方式单位为秒，Percent 方式为 0-100） |
| `--watermark-set` | string | - | 水印模板 ID 列表（逗号分隔） |
| `--media-storage-path` | string | - | 媒体存储路径（仅 FileID+Path 模式子应用可用） |
| `--session-id` | string | - | 去重识别码 |
| `--ext-info` | string | - | 扩展信息 |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |
| `--tasks-notify-mode` | enum | - | 通知模式：`Finish` / `Change` / `None` |

---

### adaptive-streaming 参数（自适应码流）

> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--definition` | int | ✅ | 自适应码流模板 ID |
| `--subtitle-set` | string | - | 字幕 ID 列表（逗号分隔）⚠️ 不是 `--subtitle-ids` |
| `--media-storage-path` | string | - | 媒体存储路径（仅 FileID+Path 模式子应用可用） |
| `--session-id` | string | - | 去重识别码 |
| `--ext-info` | string | - | 扩展信息 |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |
| `--tasks-notify-mode` | enum | - | 通知模式：`Finish` / `Change` / `None` |

---

### sample-snapshot 参数（采样截图）

> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--definition` | int | ✅ | 采样截图模板 ID |
| `--watermark-set` | string | - | 水印模板 ID 列表（逗号分隔） |
| `--media-storage-path` | string | - | 媒体存储路径（仅 FileID+Path 模式子应用可用） |
| `--session-id` | string | - | 去重识别码 |
| `--ext-info` | string | - | 扩展信息 |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |
| `--tasks-notify-mode` | enum | - | 通知模式：`Finish` / `Change` / `None` |

---

### image-sprite 参数（雪碧图）

> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--definition` | int | ✅ | 雪碧图模板 ID |
| `--watermark-set` | string | - | 水印模板 ID 列表（逗号分隔） |
| `--media-storage-path` | string | - | 媒体存储路径（仅 FileID+Path 模式子应用可用） |
| `--session-id` | string | - | 去重识别码 |
| `--ext-info` | string | - | 扩展信息 |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |
| `--tasks-notify-mode` | enum | - | 通知模式：`Finish` / `Change` / `None` |

---

### ai-review 参数（AI 内容审核）

> ⚠️ 不建议使用，推荐使用 `ReviewAudioVideo` 接口。  
> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--definition` | int | ✅ | 音视频审核模板 ID |
| `--media-storage-path` | string | - | 媒体存储路径（仅 FileID+Path 模式子应用可用） |
| `--session-id` | string | - | 去重识别码 |
| `--ext-info` | string | - | 扩展信息 |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |
| `--tasks-notify-mode` | enum | - | 通知模式：`Finish` / `Change` / `None` |

---

### ai-analysis 参数（AI 内容分析）

> **必须通过 `--definition` 指定内容分析模板 ID**，禁止使用 tccli。  
> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--definition` | int | ✅ | 视频内容分析模板 ID |
| `--media-storage-path` | string | - | 媒体存储路径（仅 FileID+Path 模式子应用可用） |
| `--session-id` | string | - | 去重识别码 |
| `--ext-info` | string | - | 扩展信息 |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |
| `--tasks-notify-mode` | enum | - | 通知模式：`Finish` / `Change` / `None` |

---

### ai-recognition 参数（AI 内容识别）

> **必须通过 `--definition` 指定智能识别模板 ID**，禁止使用 tccli。  
> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file-id` | string | ✅ | 媒体文件 ID |
| `--definition` | int | ✅ | 视频智能识别模板 ID |
| `--media-storage-path` | string | - | 媒体存储路径（仅 FileID+Path 模式子应用可用） |
| `--session-id` | string | - | 去重识别码 |
| `--ext-info` | string | - | 扩展信息 |
| `--tasks-priority` | int | - | 任务优先级（-10 到 10） |
| `--tasks-notify-mode` | enum | - | 通知模式：`Finish` / `Change` / `None` |

---

### scene-transcode 参数（场景转码）

> 基于极速高清技术，针对短剧/电商/信息流场景定向优化。  
> 通用参数见上方[通用参数](#通用参数所有子命令共享)。

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--file-id` | string | ✅ | - | 媒体文件 ID |
| `--scene` | enum | ✅ | - | 场景：`short_drama`（短剧）/ `ecommerce`（电商）/ `feed`（信息流） |
| `--resolution` | enum | - | `1080` | 输出分辨率：`1080` / `720` / `480` |
| `--priority` | enum | - | `best` | 转码策略：`best`（综合最佳）/ `quality`（画质优先）/ `bitrate`（码率优先） |
| `--session-context` | string | - | - | 来源上下文（最长 1000 字符） |
| `--tasks-priority` | int | - | - | 任务优先级（-10 到 10） |

**场景说明：**

| 场景 | 标识 | 核心优化 |
|------|------|----------|
| 短剧 | `short_drama` | 提升人物辨识度，优化视频大小 |
| 电商 | `ecommerce` | 高效压缩，降低存储和分发成本 |
| 信息流 | `feed` | 提升播放流畅性，降低加载耗时 |

**场景转码模板 ID（供参考，脚本自动选择）：**

| 场景 | 分辨率 | best | quality | bitrate |
|------|--------|------|---------|---------|
| short_drama | 1080P | 101300 | 101301 | 101302 |
| short_drama | 720P | 101303 | 101304 | 101305 |
| short_drama | 480P | 101306 | 101307 | 101308 |
| ecommerce | 1080P | 101309 | 101310 | 101311 |
| ecommerce | 720P | 101312 | 101313 | 101314 |
| ecommerce | 480P | 101315 | 101316 | 101317 |
| feed | 1080P | 101318 | 101319 | 101320 |
| feed | 720P | 101321 | 101322 | 101323 |
| feed | 480P | 101324 | 101325 | 101326 |

---

## 使用示例

### 模板 ID 速查

#### 极速高清转码（transcode）

| `--quality` | 模板 ID | 分辨率 |
|-------------|---------|--------|
| `same`（默认） | 100800 | 同源 |
| `flu` | 100810 | 360P |
| `sd` | 100820 | 540P |
| `hd` | 100830 | 720P |

#### 转封装（remux）

| `--target-format` | 模板 ID |
|-------------------|---------|
| `mp4` | 875 |
| `hls` | 876 |

#### 视频增强（enhance）

| 场景 | 分辨率 | 模板 ID |
|------|--------|---------|
| `general` | 720P | 101410 |
| `general` | 1080P | 101430 |
| `general` | 2K | 101450 |
| `general` | 4K | 101470 |
| `anime` | 720P | 101510 |
| `anime` | 1080P | 101530 |
| `anime` | 2K | 101550 |
| `anime` | 4K | 101570 |
| `live_action` | 720P | 101520 |
| `live_action` | 1080P | 101540 |
| `live_action` | 2K | 101560 |
| `live_action` | 4K | 101580 |

---

### 极速高清转码（transcode）

> ⚠️ 极速高清用 `transcode --quality`；场景转码（短剧/电商/信息流）用 `scene-transcode --scene`，两者完全不同。

```bash
# 同源（默认，高画质低码率）
python scripts/vod_process_media.py transcode --file-id <FileId>

# 高清 720P
python scripts/vod_process_media.py transcode --file-id <FileId> --quality hd

# 标清 540P（省成本）
python scripts/vod_process_media.py transcode --file-id <FileId> --quality sd

# 流畅 360P（省流量）
python scripts/vod_process_media.py transcode --file-id <FileId> --quality flu

# JSON 输出
python scripts/vod_process_media.py transcode --file-id <FileId> --quality hd --json
```

---

### 转封装（remux）

> ⚠️ **参数区分**：
> - `--target-format`：**必填**，目标封装格式（`mp4` 或 `hls`）
> - `--tasks-priority`：任务优先级（-10 到 10），**注意不是 `--priority`**，`--priority` 是 scene-transcode 专用参数

```bash
# 转封装为 MP4
python scripts/vod_process_media.py remux --file-id 5145403721233902989 --target-format mp4

# 转封装为 HLS
python scripts/vod_process_media.py remux --file-id 5145403721233902989 --target-format hls

# 转封装为 HLS + 设置任务优先级 + 透传来源上下文
python scripts/vod_process_media.py remux --file-id 5145403721233902989 \
    --target-format hls --tasks-priority 5 --session-context "remux-ctx"

# JSON 输出
python scripts/vod_process_media.py remux --file-id 5145403721233902989 --target-format mp4 --json
```

---

### 视频增强（enhance）

```bash
# 通用场景 1080P（默认）
python scripts/vod_process_media.py enhance --file-id 5145403721233902989

# 真人/短剧场景 720P
python scripts/vod_process_media.py enhance --file-id 5145403721233902989 --scene live_action --resolution 720

# 真人/短剧场景 4K
python scripts/vod_process_media.py enhance --file-id 5145403721233902989 --scene live_action --resolution 4k

# 漫剧场景 2K
python scripts/vod_process_media.py enhance --file-id 5145403721233902989 --scene anime --resolution 2k

# 透传上下文 + 设置优先级
python scripts/vod_process_media.py enhance --file-id 5145403721233902989 --scene live_action --resolution 4k \
    --session-context "enhance-ctx" --tasks-priority 3 --json
```

---

### 场景转码（scene-transcode）

> 规律：`--scene` 必填，`--resolution` 默认 `1080`，`--priority` 默认 `best`，脚本自动选择对应模板 ID。

```bash
# 短剧 1080P 综合最佳（全部默认）
python scripts/vod_process_media.py scene-transcode --file-id 5285485487985271487 --scene short_drama

# 电商 720P 码率优先
python scripts/vod_process_media.py scene-transcode --file-id 5285485487985271487 \
    --scene ecommerce --resolution 720 --priority bitrate

# 信息流 480P 画质优先
python scripts/vod_process_media.py scene-transcode --file-id 5285485487985271487 \
    --scene feed --resolution 480 --priority quality

# 指定子应用 + JSON 输出
python scripts/vod_process_media.py scene-transcode --file-id 5285485487985271487 \
    --scene short_drama --sub-app-id 251007502 --json

# dry-run 预览请求
python scripts/vod_process_media.py scene-transcode --file-id 5285485487985271487 \
    --scene short_drama --resolution 1080 --priority best --dry-run
```

---

### AI 内容分析（ai-analysis）

```bash
# 基础分析
python scripts/vod_process_media.py ai-analysis --file-id 5145403721233902989 --definition 10

# 指定子应用 + JSON 输出
python scripts/vod_process_media.py ai-analysis --file-id 5145403721233902989 --definition 10 \
    --sub-app-id 251007502 --json

# 仅提交不等待
python scripts/vod_process_media.py ai-analysis --file-id 5145403721233902989 --definition 10 --no-wait
```

---

### AI 内容识别（ai-recognition）

```bash
# 基础识别
python scripts/vod_process_media.py ai-recognition --file-id 5145403721233902989 --definition 10

# 指定子应用 + JSON 输出
python scripts/vod_process_media.py ai-recognition --file-id 5145403721233902989 --definition 10 \
    --sub-app-id 251007502 --json
```

---

### 截图（snapshot）

```bash
# 基础截图
python scripts/vod_process_media.py snapshot --file-id 5145403721233902989 --definition 10

# 多水印 + 指定截图时间点
python scripts/vod_process_media.py snapshot --file-id 5145403721233902989 --definition 10 \
    --ext-time-offset-set "5s,10s,15s" --watermark-set "10001,10002"
```

---

### 错误码说明（场景转码）

| 错误类型 | 原因 | 处理建议 |
|---------|------|---------|
| `InvalidParameterValue.Definition` | 模板 ID 无效 | 检查场景/分辨率/策略组合是否有效 |
| `ResourceNotFound.FileId` | 文件不存在 | 检查 FileId 是否正确 |
| `FailedOperation` | 任务提交失败 | 检查账户权限和余额 |
| `LimitExceeded` | 频率限制 | 默认 20次/秒 |
