---
name: sound-split
description: 智能音频分离工具，一键将任意音频或视频分离出人声、伴奏、鼓、贝斯、钢琴等独立音轨。适用于音乐人翻唱伴奏提取、歌曲 Remix 制作、播客人声降噪、视频配乐替换、音乐教学素材准备等场景。当用户需要「分离人声和伴奏」「提取伴奏」「去除人声」「拆分音轨」「vocal split」「stem splitter」等操作时触发此技能。
---

# Sound Split — AI 智能音频分离工具

## 一句话说明

上传一段音频或视频，AI 自动将其中的**人声、伴奏、鼓点、贝斯、钢琴**等音轨一一分离出来，支持在线预览每条音轨并单独下载。

---

## 附件文件说明

本 Skill 附带完整的核心实现代码（位于 `rules/` 目录）：

| 文件 | 内容 | 说明 |
|------|------|------|
| `rules/server.py` | FastAPI Web 服务主程序（498 行）| 全部 API 路由、后台分离逻辑、进度追踪、历史管理 |
| `rules/app-page.html` | 工具主操作页面（59KB）| 上传 + 配置 + 分离 + 结果展示的完整 UI |
| `rules/editor-page.html` | 音频裁剪编辑器（31KB）| 波形可视化 + 时间选区 + 片段导出 |

> 这些文件是纯文本，可直接复制到本地使用。部署方式见下方「使用流程」。

---

## 核心能力一览

| 能力 | 说明 | 典型用途 |
|------|------|----------|
| **人声 / 伴奏分离** | 从歌曲中提取纯净人声或纯伴奏 | 翻唱、Remix、混音 |
| **多轨分轨提取** | 一首歌拆为 2~5 条独立音轨 | 编曲学习、乐队分谱、混音练习 |
| **视频直接处理** | 上传视频自动提取音频并分离 | 视频配乐替换、BGM 提取 |
| **实时进度反馈** | 分离过程中实时进度条 | 了解处理状态，无需盲等 |
| **片段裁剪下载** | 对分离后的音轨精确裁剪起止时间 | 只导出需要的片段 |
| **历史记录管理** | 保留完整任务历史，随时回溯下载 | 重复使用之前的结果 |

---

## 前置条件

### 环境要求

| 依赖项 | 版本要求 | 安装方式 | 必要性 |
|--------|----------|----------|--------|
| Python | ≥ 3.8 | 系统自带或 [python.org](https://python.org) 下载 | 必须 |
| FFmpeg | 任意稳定版 | `brew install ffmpeg`（Mac）/ `apt install ffmpeg`（Linux） | 必须，用于音频提取与转码 |

### Python 包安装（必须执行一次）

```bash
pip install fastapi uvicorn demucs ffmpeg-python
```

> ⚠️ **首次运行时会自动下载 AI 分离模型**（约 300~500MB），请确保网络通畅。下载完成后会缓存到本地 `~/.cache/demucs/` 目录，后续运行不再重复下载。

### 验证环境是否就绪

```bash
# 1. 验证 FFmpeg 安装
ffmpeg -version | head -1

# 2. 验证 demucs 可用（首次会触发模型下载）
python3 -m demucs --version

# 3. 如果以上两个命令都正常输出，说明环境已就绪
```

---

## 使用流程（完整操作步骤）

### 第一步：启动服务

```bash
cd <skill_path>/audio-separator
python3 server.py
```

**预期结果**：终端显示以下内容说明启动成功：

```
╔══════════════════════════════════════════════╗
║   🎵 音频分离工具 - AI 智能分轨              ║
║   http://127.0.0.1:8765                       ║
╚══════════════════════════════════════════════╝
[init] 已从历史记录恢复 N 个任务
```

服务监听地址：**`http://127.0.0.1:8765`**

**失败处理**：
- 若报错 `ModuleNotFoundError: No module named 'demucs'` → 先执行 `pip install demucs` 再重启
- 若报错 `ffmpeg not found` → 先安装 FFmpeg 再重启
- 若端口 8765 被占用 → 终端执行 `lsof -i :8765 | grep LISTEN | awk '{print $2}' | xargs kill -9` 释放端口后重试

---

### 第二步：打开操作页面

浏览器访问以下地址：

| 页面 | 地址 | 功能 |
|------|------|------|
| **工具主页面（推荐）** | `http://127.0.0.1:8765/app.html` | 上传文件 + 选择模式 + 分离操作 + 预览下载 |
| **音频编辑器** | `http://127.0.0.1:8765/editor` | 对已完成分离的音轨进行裁剪，导出指定时间段 |
| **产品介绍页** | `http://127.0.0.1:8765/` | 产品功能展示与 Demo 试听（非必需） |

> 💡 **推荐直接使用 `/app.html` 主页面**，所有核心操作都在一个界面完成。

---

### 第三步：上传文件并配置参数

在主页面（app.html）上按以下顺序操作：

1. **点击上传区域或拖拽文件到虚线框内**
   - 支持格式：MP3, WAV, FLAC, OGG, M4A（音频）；MP4, MOV, AVI, MKV, FLV（视频）
   - 文件大小建议 ≤ 100MB
   - 音频时长建议 ≤ 10 分钟（过长会显著增加处理时间）

2. **选择分离轨道数**
   - **2 轨道**（默认）：输出「人声」+「伴奏」，适合翻唱、去人声场景
   - **4 轨道**：输出「人声」+「鼓」+「贝斯」+「其他」，适合编曲分析、混音练习
   - **5 轨道**：输出「人声」+「鼓」+「贝斯」+「钢琴」+「其他」，适合专业音乐制作

3. **选择处理精度**
   - **推荐模式**（默认）：均衡质量与速度，适合大多数场景
   - **高品质模式**：更精细的分离效果，处理时间稍长
   - **经典模式**：基础分离能力，速度最快
   - **增强模式**：针对特定类型优化

4. **点击「开始分离」按钮**

---

### 第四步：等待处理完成

- 页面会自动显示**进度条**（0% ~ 100%）
- 进度阶段说明：

| 进度范围 | 含义 | 说明 |
|----------|------|------|
| 0~15% | 初始化 | 视频文件正在提取音频流；音频文件跳过此阶段 |
| 15~20% | 加载模型 | AI 模型加载到内存（仅首次较慢，后续有缓存加速） |
| 20~85% | 正在分离 | AI 逐段分析音频并拆分音轨，耗时取决于文件长度 |
| 85~100% | 整理输出 | 将分离结果整理为标准 MP3 文件 |

- **典型耗时参考**：
  - 3 分钟歌曲（2 轨道）：约 30~60 秒
  - 5 分钟歌曲（5 轨道）：约 1~3 分钟
  - 10 分钟视频（4 轨道）：约 3~8 分钟
  - > 10 分钟的文件不推荐，可能需要 10 分钟以上

- **异常情况处理**：
  - 进度卡住超过 5 分钟无变化 → 刷新页面后在历史记录中查看任务是否已完成
  - 显示错误信息 → 查看终端 server.py 的错误日志，常见原因：文件损坏、磁盘空间不足、FFmpeg 未安装

---

### 第五步：预览与下载

分离完成后页面自动展示结果：

**每条音轨提供以下操作：**

| 操作 | 说明 |
|------|------|
| ▶ 播放按钮 | 点击即时在浏览器中试听该音轨效果 |
| 📥 下载按钮 | 下载该音轨的 MP3 文件（320kbps 高品质） |
| ✂️ 裁剪 | 跳转到编辑器，选择起止时间后导出指定片段 |

**输出文件位置**：`<skill_path>/audio-separator/outputs/{task_id}/` 下包含各音轨的 MP3 文件

**输出文件命名规则**：

| 轨道数 | 输出文件名 |
|--------|-----------|
| 2stems | `vocals.mp3`（人声）、`accompaniment.mp3`（伴奏）|
| 4stems | `vocals.mp3`、`drums.mp3`、`bass.mp3`、`other.mp3` |
| 5stems | `vocals.mp3`、`drums.mp3`、`bass.mp3`、`piano.mp3`、`other.mp3` |

---

## API 接口详细说明

如需通过程序调用（而非浏览器界面），本工具提供完整的 RESTful API：

### 接口清单总览

| 接口路径 | 方法 | 功能 |
|----------|------|------|
| `/api/separate` | POST | 上传文件并启动分离任务 |
| `/api/status/{task_id}` | GET | 查询任务进度和结果 |
| `/api/download/{task_id}/{track_name}` | GET | 下载指定音轨文件 |
| `/api/trim` | POST | 裁剪音轨片段 |
| `/api/history` | GET | 获取历史任务列表 |
| `/api/cleanup/{task_id}` | DELETE | 清理任务的输出文件 |

---

### 1. 上传并分离 — POST /api/separate

**请求格式**：

```
POST /api/separate
Content-Type: multipart/form-data
```

**请求参数**：

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| file | File | ✅ 是 | 无 | 要处理的音频或视频文件 |
| model | string | 否 | htdemucs | 处理精度模式（见下方可选值表）|
| stems | string | 否 | 2stems | 输出轨道数（2stems / 4stems / 5stems）|

**model 可选值**：

| model 值 | 效果 |
|----------|------|
| htdemucs | 推荐，均衡质量与速度 |
| htdemucs_ft | 高品质，更精细分离 |
| demucs | 经典模式，速度最快 |
| mdx | 人声增强模式 |
| mdx_extra | 全面增强模式 |

**成功响应**（HTTP 200）：

```json
{
  "task_id": "a1b2c3d4e5f6",
  "status": "pending",
  "message": "任务已提交，请用 task_id 轮询进度"
}
```

**错误响应**：

- HTTP 400：`不支持的模式: xxx` 或 `不支持的轨道数: xxx` — 检查 model 和 stems 参数值
- HTTP 500：服务器内部错误 — 查看 server.py 终端日志

---

### 2. 查询任务状态 — GET /api/status/{task_id}

**请求**：`GET /api/status/a1b2c3d4e5f6`

**成功响应示例**（处理中）：

```json
{
  "status": "processing",
  "progress": 65,
  "message": "Separating... 65% (30 lines processed)",
  "model": "htdemucs",
  "stems": "2stems",
  "filename": "song.mp3",
  "result": null
}
```

**成功响应示例**（完成）：

```json
{
  "status": "completed",
  "progress": 100,
  "message": "Done!",
  "model": "htdemucs",
  "stems": "2stems",
  "filename": "song.mp3",
  "result": {
    "tracks": {
      "vocals": "vocals.mp3",
      "accompaniment": "accompaniment.mp3"
    },
    "output_dir": "outputs/a1b2c3d4e5f6"
  }
}
```

**状态字段含义**：

| status 值 | 含义 | 建议操作 |
|-----------|------|----------|
| pending | 任务排队中等待开始 | 等待几秒后再次查询 |
| processing | 正在分离中 | 每 2~3 秒轮询一次 progress |
| completed | 分裂完成 | 用 tracks 字段的文件名去 download 接口下载 |
| error | 处理出错 | 查看 message 字段获取具体错误信息 |

**错误响应**：HTTP 404 `{ "detail": "任务不存在" }` — 检查 task_id 是否正确

---

### 3. 下载音轨 — GET /api/download/{task_id}/{track_name}

**请求示例**：

```
GET /api/download/a1b2c3d4e5f6/vocals
GET /api/download/a1b2c3d4e5f6/accompaniment
```

**响应**：直接返回对应音轨的 MP3 文件（Content-Type: audio/mpeg）

**错误响应**：
- HTTP 404：任务目录不存在或音轨文件不存在 — 先确认任务已完成且 track_name 正确

---

### 4. 裁剪音轨片段 — POST /api/trim

**请求格式**：

```
POST /api/trim
Content-Type: application/x-www-form-urlencoded
```

**请求参数**：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| task_id | string | ✅ | 已完成的分离任务 ID |
| track_name | string | ✅ | 要裁剪的音轨名称（vocals / accompaniment / drums 等）|
| start_time | float | ✅ | 开始时间，单位秒（例如 30.5 表示 30 秒 500 毫秒）|
| end_time | float | ✅ | 结束时间，单位秒（必须大于 start_time）|

**请求示例**：

```
POST /api/trim
task_id=a1b2c3d4e5f6&track_name=vocals&start_time=30&end_time=90
```

**响应**：返回裁剪后的 MP3 文件，文件名格式为 `{track_name}_{起始时间}_{结束时间}.mp3`（例如 `vocals_0030_0130.mp3`）

**错误响应**：
- HTTP 400：缺少必要参数，或 `end_time <= start_time`
- HTTP 404：task_id 或 track_name 对应的文件不存在
- HTTP 500：FFmpeg 裁剪过程出错

---

### 5. 获取历史记录 — GET /api/history

**响应示例**：

```json
[
  {
    "task_id": "a1b2c3d4e5f6",
    "filename": "song.mp3",
    "model": "htdemucs",
    "stems": "2stems",
    "status": "completed",
    "track_count": 2,
    "created_at": "2026-04-15T11:30:00",
    "exists": true
  }
]
```

其中 `exists: true/false` 表示该任务的输出文件在磁盘上是否仍然存在（可能已被清理删除）。

---

### 6. 清理任务文件 — DELETE /api/cleanup/{task_id}

**响应**：`{ "message": "已清理 N 个文件" }`

> ⚠️ 此操作会**永久删除**该任务的所有输出文件和原始上传文件，不可恢复。建议仅在确认不再需要结果时使用。

---

## 项目文件结构

```
sound-split/
├── SKILL.md                          # 本说明文档
├── audio-separator/                  # ★ 主程序目录（核心实现全部在此）
│   ├── server.py                     # ★ Web 服务主程序（FastAPI 应用）
│   │                                 #   包含：API 路由、后台分离逻辑、
│   │                                 #   历史管理、进度追踪、FFmpeg 调用
│   ├── static/
│   │   ├── index.html                # ★ 工具主操作页面（上传 + 配置 + 分离 + 结果展示）
│   │   ├── editor.html               # ★ 音频裁剪编辑器（波形可视化 + 时间选区 + 导出）
│   │   └── landing.html              # 产品介绍页（Demo 试听 + 场景说明）
│   ├── uploads/                      # 上传文件临时存储目录（运行时自动创建）
│   ├── outputs/                      # 分离结果输出目录（每个任务一个子文件夹）
│   ├── trims/                        # 裁剪片段临时存储目录
│   └── history.json                  # 任务历史持久化记录（最多保留 50 条）
├── scripts/                          # 技能脚本目录
└── assets/                           # 技能资源目录
```

> 标记 ★ 的为核心实现文件，缺一不可。其余目录均为运行时自动创建，不需要手动准备。

---

## 关键约束与注意事项

1. **隐私安全**：所有音频处理均在**本地机器**完成，数据不会上传到任何外部服务器。AI 模型仅在本地运行。

2. **资源需求**：
   - 内存：建议至少 4GB RAM（处理长音频时峰值可达 2~3GB）
   - 磁盘空间：模型缓存 ~500MB + 输出文件（每首歌曲约 10~50MB）
   - CPU/GPU：优先使用 GPU 加速（需 NVIDIA CUDA），无 GPU 时自动回退 CPU 运行（速度慢 3~10 倍）

3. **并发限制**：同一时间只处理一个任务。提交新任务时会排队等待当前任务完成。

4. **文件限制**：
   - 单文件大小：建议 ≤ 100MB
   - 单次时长：建议 ≤ 10 分钟
   - 超出限制不会报错但可能导致处理极慢或内存不足

5. **输出格式**：固定输出 MP3（320kbps），不支持自定义码率或格式（如需 WAV 可通过 FFmpeg 手动转码）。

6. **服务生命周期**：关闭终端窗口或 Ctrl+C 会停止服务。已完成的任务结果保存在 outputs/ 和 history.json 中，重启服务后会自动恢复。

---

## 常见问题排查

| 问题现象 | 可能原因 | 解决方法 |
|----------|----------|----------|
| 启动报 `ModuleNotFoundError` | Python 包未安装 | 执行 `pip install fastapi uvicorn demucs ffmpeg-python` |
| 启动报 `ffmpeg not found` | FFmpeg 未安装 | Mac: `brew install ffmpeg`; Linux: `apt install ffmpeg` |
| 首次运行非常慢 | 正在下载 AI 模型 | 仅首次发生，模型会缓存到 ~/.cache/demucs/ |
| 上传后一直显示 pending | 后台进程未启动 | 刷新页面，查看 server.py 终端是否有错误输出 |
| 进度卡在某个百分比不动 | 大文件正常处理中 | 5 分钟以上无变化则可能是死锁，重启服务重试 |
| 下载的文件无法播放 | 分离过程中出错 | 检查 outputs/ 对应目录下的 .mp3 文件大小是否 > 0 |
| 视频上传后只有画面没有声音 | 视频编码特殊导致 FFmpeg 提取失败 | 先用 FFmpeg 手动提取音频再上传：`ffmpeg -i video.mp4 -vn -acodec mp3 audio.mp3` |

---

## 适用场景举例

### 场景一：翻唱伴奏提取
1. 打开 `http://127.0.0.1:8765/app.html`
2. 上传原唱歌曲 MP3
3. 选择 **2 轨道** + **推荐模式**
4. 点击「开始分离」，等待完成
5. 下载 `accompaniment.mp3` 作为伴奏使用

### 场景二：视频 BGM 替换
1. 打开工具页面
2. 直接上传 MP4 视频文件（无需预先提取音频）
3. 选择 **2 轨道**
4. 完成后下载 `accompaniment.mp3`（原背景音乐）
5. 在视频剪辑软件中替换为自己的 BGM

### 场景三：编曲学习分析
1. 上传想学习的歌曲
2. 选择 **5 轨道** + **高品质模式**（更精准的乐器分离）
3. 分别下载 `drums.mp3`（鼓点）、`bass.mp3`（贝斯线）、`piano.mp3`（钢琴部分）
4. 反复聆听单轨，学习每种乐器的编排方式
