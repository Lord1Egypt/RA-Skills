# Video Generation 模块

从图片、文字提示或参考素材生成视频。

## 支持的任务类型

| 类型 | 说明 | 必需参数 |
|------|-------------|-----------------|
| `i2v` | **图片转视频 V2** — 从首帧/尾帧图片生成视频 | `--first-frame` 或 `--ref-images` |
| `t2v` | **文字转视频** — 纯文字提示生成视频 | `--model`, `--prompt` |
| `omni` | **Omni 参考** — 从参考图片/视频 + 提示词生成视频 | `--model`, `--prompt` |

## 子命令

| 子命令 | 使用场景 | 轮询？ |
|------------|-------------|--------|
| `run` | **默认。** 新请求，从提交到完成 | 是 — 等待至完成 |
| `submit` | 批量：提交多个任务不等待 | 否 — 立即退出 |
| `query` | 恢复：对已有的 `taskId` 继续轮询 | 是 — 等待至完成 |
| `list-models` | 查看模型、约束条件和音频支持 | 否 |
| `estimate-cost` | 执行前估算积分费用 | 否 |

## 用法

```bash
python {baseDir}/scripts/video_gen.py <subcommand> --type <i2v|t2v|omni> [options]
```

## 示例

### 列出模型

```bash
python {baseDir}/scripts/video_gen.py list-models --type t2v
python {baseDir}/scripts/video_gen.py list-models --type i2v --json
```

### 图片转视频 (i2v)

```bash
python {baseDir}/scripts/video_gen.py run \
  --type i2v \
  --first-frame <fileId_or_local_path> \
  --prompt "产品在纯白背景上缓缓旋转" \
  --model "Seedance 1.5 Pro" \
  --resolution 1080 \
  --duration 5
```

使用首帧 + 尾帧：

```bash
python {baseDir}/scripts/video_gen.py run \
  --type i2v \
  --first-frame <fileId> \
  --end-frame <fileId> \
  --prompt "场景之间平滑过渡" \
  --resolution 1080
```

### 文字转视频 (t2v)

```bash
python {baseDir}/scripts/video_gen.py run \
  --type t2v \
  --model "Seedance 1.5 Pro" \
  --prompt "未来都市夜景，霓虹灯倒映在潮湿的街道上" \
  --aspect-ratio "16:9" \
  --resolution 1080 \
  --duration 5 \
  --sound on
```

### Omni 参考

```bash
python {baseDir}/scripts/video_gen.py run \
  --type omni \
  --model "Standard" \
  --prompt "将 <<<Image1>>> 的风格应用到 <<<Video1>>> 的运动中" \
  --input-images '[{"fileId":"file_style","name":"Image1"}]' \
  --input-videos '[{"fileId":"file_motion","name":"Video1"}]' \
  --aspect-ratio "9:16" \
  --resolution 720
```

### 费用估算

```bash
python {baseDir}/scripts/video_gen.py estimate-cost \
  --model "Seedance 1.5 Pro" --resolution 1080 --duration 5 --sound on --count 2
```

### 恢复 / 批量

```bash
TASK_ID=$(python {baseDir}/scripts/video_gen.py submit \
  --type t2v --model "Seedance 1.5 Pro" --prompt "海面上的日落" -q)

python {baseDir}/scripts/video_gen.py query \
  --type t2v --task-id <taskId> --timeout 1200
```

## 通用选项

| 选项 | 说明 |
|--------|-------------|
| `--type` | 任务类型：`i2v`、`t2v`、`omni`（必需） |
| `--model` | 模型 **display name**（t2v/omni 必需） |
| `--prompt` | 文字提示词（t2v/omni 必需） |
| `--aspect-ratio` | 宽高比，如 `"16:9"` |
| `--resolution` | `480`、`540`、`720`、`768`、`1080` 或 `2160` |
| `--duration` | 视频时长，单位秒 |
| `--sound` | 原生音频：`"on"` / `"off"` |
| `--count` | 视频数量（1-4） |
| `--board-id` | 看板 ID |
| `--timeout` | 最大轮询时间（默认：600） |
| `--interval` | 轮询间隔（默认：5） |
| `--output-dir` | 将结果视频下载到指定目录 |
| `--json` | 输出完整 JSON 响应 |
| `-q, --quiet` | 静默模式，抑制状态消息 |

### 仅 i2v

| 选项 | 说明 |
|--------|-------------|
| `--first-frame` | 首帧图片：fileId 或本地路径。例如 `--first-frame abc123` 或 `--first-frame photo.png` |
| `--end-frame` | 尾帧图片：fileId 或本地路径。例如 `--end-frame def456` 或 `--end-frame end.jpg` |
| `--ref-images` | 参考图片（多图参考，>=2）：多个 fileId 或本地路径，用空格分隔。例如 `--ref-images img1.png img2.png` |

### 仅 omni

| 选项 | 说明 |
|--------|-------------|
| `--input-images` | 输入图片的 JSON 数组。每项包含 `fileId`（fileId 或本地路径，本地文件会自动上传）和 `name`（在 prompt 中以 `<<<Name>>>` 引用）。例如 `--input-images '[{"fileId":"abc123","name":"Image1"}]'` 或使用本地文件：`--input-images '[{"fileId":"/path/to/photo.jpg","name":"Image1"}]'` |
| `--input-videos` | 输入视频的 JSON 数组，格式同 `--input-images`。例如 `--input-videos '[{"fileId":"vid123","name":"Video1"}]'` |
| `--internet-search` | 启用互联网搜索（仅 Standard/Fast） |

## 原生音频 (`--sound`)

- 仅 `nativeAudio=True` 的模型支持此功能 — 通过 `list-models` 检查
- 开启音频可能会增加费用，取决于模型

## Omni 提示词语法

使用 `<<<ImageN>>>` 或 `<<<VideoN>>>` 引用输入素材：

```
"Apply the color style from <<<Image1>>> to <<<Video1>>>"
```

## 模型推荐

> **说明：** 地表最强模型S2.0-白名单版（支持上传真人图）和地表最强模型S2.0 Fast-白名单版（支持上传真人图）是顶级模型，具有业界领先的视觉质量、原生音频和最长 15 秒时长。支持所有三种任务类型（i2v、t2v、omni）。追求最佳画质用前者；追求速度用 Fast 版本。
>
> 向用户展示模型时使用展示名称，构造命令时使用 API 名称。完整映射见 [model_mapping.md](model_mapping.md)。

**按优先级：**

| 优先级 | 推荐模型（展示名） | 对应 API 名称 | 原因 |
|----------|--------------------|----|-----|
| **最佳画质** | 地表最强模型S2.0-白名单版（支持上传真人图）, 可灵 O3, 电影级画质模型 V3.1, 拟真世界模型 2 Pro | `Standard`, `Kling O3`, `Veo 3.1`, `Sora 2 Pro` | 顶级视觉保真度 |
| **快速出片** | 地表最强模型S2.0 Fast-白名单版（支持上传真人图）, Seedance 1.0 Pro Fast, 电影级画质模型 V3.1 fast | `Fast`, `Seedance 1.0 Pro Fast`, `Veo 3.1 Fast` | 更快、更低费用 |
| **长片段 (10s+)** | 地表最强模型S2.0-白名单版（支持上传真人图）/ 地表最强模型S2.0 Fast-白名单版（支持上传真人图）(15s), 可灵 V3/O3 (15s), Vidu Q3 Pro (16s) | `Standard`/`Fast`, `Kling V3`/`Kling O3`, `Vidu Q3 Pro` | 支持更长时长 |
| **4K** | 电影级画质模型 V3.1, 电影级画质模型 V3.1 fast | `Veo 3.1`, `Veo 3.1 Fast` | 唯一支持 2160p 的模型 |
| **原生音频** | 地表最强模型S2.0-白名单版（支持上传真人图）/ 地表最强模型S2.0 Fast-白名单版（支持上传真人图）, 可灵 O3/V3, 电影级画质模型 V3.1, Vidu Q3 Pro | `Standard`/`Fast`, `Kling O3`/`Kling V3`, `Veo 3.1`, `Vidu Q3 Pro` | 环境声音 |

**按发布渠道：**

| 渠道 | 宽高比 | 推荐模型（展示名） | 对应 API 名称 |
|---------|-------------|-------------|---|
| TikTok / Reels | 9:16 | 地表最强模型S2.0-白名单版（支持上传真人图）, 可灵 V3 | `Standard`, `Kling V3` |
| YouTube | 16:9 | 地表最强模型S2.0-白名单版（支持上传真人图）, 可灵 O3, 电影级画质模型 V3.1 | `Standard`, `Kling O3`, `Veo 3.1` |
| Instagram | 3:4 或 1:1 | 地表最强模型S2.0-白名单版（支持上传真人图）, Seedance 1.5 Pro | `Standard`, `Seedance 1.5 Pro` |

**默认选择**（用户无偏好时）：
- t2v → 地表最强模型S2.0-白名单版（支持上传真人图）（API: `Standard`）
- i2v → 地表最强模型S2.0-白名单版（支持上传真人图）或可灵 V3（API: `Standard` 或 `Kling V3`）
- omni → 地表最强模型S2.0-白名单版（支持上传真人图）（API: `Standard`）

## 提示词技巧

**结构：** 主体 + 动作 + 环境 + 风格 + 镜头

**镜头关键词：** "static shot"、"slow pan left"、"dolly forward"、"tracking shot"、"orbit around"、"zoom in"、"crane shot rising"、"shallow depth of field"
