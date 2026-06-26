---
name: video-download-transcribe
description: |
  多平台视频下载 + 本地转录 + 视觉增强理解。
  
  **新增能力**：视频关键帧截取 + MiniMax 图片理解，融合文字+视觉做深度分析。
  
  **触发词**：
- 文字类：这个视频说了什么、视频内容是什么、帮我看这个视频、下载这个视频、视频转录、字幕提取、帮我转录
- 平台链接：直接发送视频链接即触发（无需手动输入触发词）

**自动检测的 URL 模式**：
| 平台 | URL 模式 |
|------|---------|
| B站 | `bilibili.com/video`、`b23.tv`、`BV` 开头的视频号 |
| YouTube | `youtube.com`、`youtu.be` |
| 抖音 | `douyin.com`、`v.douyin.com` |
| TikTok | `tiktok.com` |
| 小红书 | `xiaohongshu.com`、`xhslink.com` |
| 微博 | `weibo.com`、`m.weibo.cn` |
| 快手 | `kuaishou.com`、`ksurl.cn` |

> 💡 **只要消息中包含上表中的任意 URL，直接触发本 skill，无需手动输入触发词**

  **支持平台**：B站/抖音/TikTok/YouTube/小红书/微博/快手
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires":
          {
            "bins": ["ffmpeg", "yt-dlp"],
          },
      },
  }
---

# 多平台视频下载 + 本地转录

## 功能特点

- ✅ **纯浏览器下载（免费）** — 抖音用 Playwright 无水印抓取，无需 API Key
- ✅ **MLX Whisper** — Apple Silicon 原生 Metal GPU 加速（Mac M系列首选）
- ✅ **faster-whisper** — CPU/CUDA 通用兜底（非 Apple Silicon 也能用）
- ✅ **短视频同步转录** — <5 分钟视频直接返回完整结果
- ✅ **长视频后台转录** — ≥5 分钟自动后台运行，返回 transcript_id 可查询
- ✅ **可检索** — 转录结果支持关键词查询相关片段 + 时间戳

## 支持的平台

| 平台 | 检测关键词 | 下载方式 |
|------|-----------|---------|
| B站 | bilibili.com/video, b23.tv, BV号 | yt-dlp |
| 抖音 | douyin.com, v.douyin.com | Playwright 浏览器抓取 或 TikHub |
| TikTok | tiktok.com | TikHub |
| YouTube | youtube.com, youtu.be | yt-dlp |
| 小红书 | xiaohongshu.com, xhslink.com | TikHub |
| 微博 | weibo.com, m.weibo.cn | TikHub |
| 快手 | kuaishou.com, ksurl.cn | TikHub |

---

## 🚀 一键完整 pipeline（推荐）

**下载 + 转录 + 视觉增强理解**，一行命令搞定：

```bash
python3 ~/.openclaw/workspace/skills/video-download-transcribe/video_full_pipeline.py "<视频URL或本地路径>" [--keep-video]
```

**自动检测平台**：B站/抖音/YouTube/TikTok/小红书/微博/快手/本地文件

**输出**：
- 视频综合理解（文字+视觉融合）
- 自动识别需要视觉辅助的节点并截图分析

**示例**：
```bash
# 分析 B站视频
python3 video_full_pipeline.py "https://www.bilibili.com/video/BVxxx"

# 分析本地视频
python3 video_full_pipeline.py "/path/to/video.mp4"

# 保留中间文件（视频+转录JSON）
python3 video_full_pipeline.py "<url>" --keep-video
```

> 💡 **什么时候用完整 pipeline vs 两步走？**
> - 完整 pipeline：想要最终综合理解，懒得分步
> - 两步走：转录后还需额外处理，或只想单独转录

---

---

## 🔑 核心原则

### 所有平台统一两步走

> **获取下载链接 → curl/yt-dlp 下载 → mlx_whisper 转录**

**原因**：
- `analyze_video` 把下载+转录绑在一起，长视频容易超时
- 两步走每步都 <10秒，稳定可控
- 每步可单独排错

### 排错核心原则

> **当一个工具失败时，不要放弃！找替代方案。**

---

## 初始化安装（首次使用）

### 抖音 Playwright Chromium 安装

```bash
# 运行 setup.sh 自动安装
cd ~/.openclaw/workspace/skills/video-download-transcribe/douyin-mcp/
./setup.sh
```

setup.sh 会：
1. 检测系统环境
2. 查找或安装 Chromium（使用国内 npmmirror 镜像）
3. 设置 `DOUYIN_CHROMIUM_PATH` 环境变量
4. 测试浏览器抓取是否正常

**手动安装**（如果 setup.sh 失败）：
```bash
# 方式 A：用 openclaw-media 的 playwright 安装 chromium
git clone https://github.com/openclaw/openclaw-media ~/openclaw-media 2>/dev/null || true
PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright \
  ~/openclaw-media/.venv/bin/playwright install chromium

# 方式 B：自行安装 playwright
pip install playwright
PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright playwright install chromium
```

**环境变量**（运行 AI 助手前设置）：
```bash
export DOUYIN_CHROMIUM_PATH="$HOME/Library/Caches/ms-playwright/chromium-1105/chrome-mac/Chromium.app/Contents/MacOS/Chromium"
```

---

## 工作流程（统一两步走）

### 第一步：获取下载链接

```bash
# ========== 抖音 ==========

# 方式 A：douyin-analyzer 浏览器抓取（免费，需 Chromium）
mcporter call douyin-analyzer.get_douyin_download_link share_link:"https://v.douyin.com/xxx/"

# 方式 B：tikhub-douyin 获取实时 CDN 地址（更可靠，需 API Key）
mcporter call tikhub-douyin.douyin_web_fetch_video_high_quality_play_url share_url:"https://v.douyin.com/xxx/"

# ========== B站/YouTube/其他平台 ==========

# 用 yt-dlp 直接下载（会自动处理重定向和 Cookie）
yt-dlp -o "/tmp/video.mp4" "https://www.bilibili.com/video/BVxxx"

# ========== TikTok/小红书/微博/快手 ==========

# tikhub-douyin 获取下载链接
mcporter call tikhub-douyin.douyin_web_fetch_one_video_by_share_url share_url:"<链接>"
```

### 第二步：下载 + 转录

```bash
# 用 curl 下载（抖音/TikTok 获取的 CDN 地址）
curl -L -o /tmp/video.mp4 "https://cdn.example.com/video.mp4"

# 转录（本地 mlx_whisper）
python3 << 'PYEOF'
import mlx_whisper  # 首次运行直接 import，不加 HF_HUB_OFFLINE=1

result = mlx_whisper.transcribe(
    "/tmp/video.mp4",
    path_or_hf_repo="mlx-community/whisper-small-mlx",
    verbose=True
)
for seg in result.get("segments", []):
    print(f"[{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}")
PYEOF

### 长视频（≥5分钟，后台转录）

```bash
# 用 analyze_video 获取 transcript_id（后台转录中）
mcporter call douyin-analyzer.analyze_video url:"https://..." --timeout 300000

# 等待 1-2 分钟后获取结果
mcporter call douyin-analyzer.get_transcript transcript_id:"xxx"
```

---

## MCP 工具

### douyin-analyzer（本地进程，免费）

```bash
# 获取无水印下载链接（浏览器抓取）
mcporter call douyin-analyzer.get_douyin_download_link share_link:"https://v.douyin.com/xxx/"

# 解析视频基本信息
mcporter call douyin-analyzer.parse_douyin_video_info share_link:"https://v.douyin.com/xxx/"

# 通用分析（仅用于获取 transcript_id，后台转录）
mcporter call douyin-analyzer.analyze_video url:"https://..." --timeout 300000

# 获取长视频后台转录结果
mcporter call douyin-analyzer.get_transcript transcript_id:"xxx"

# 检索转录内容
mcporter call douyin-analyzer.query_transcript transcript_id:"xxx" query:"关键词" top_k:3
```

**返回结构（get_douyin_download_link）：**
```json
{
  "video_id": "xxx",
  "download_url": "https://www.iesdouyin.com/aweme/v1/play/?video_id=xxx",
  "share_link": "https://v.douyin.com/xxx/"
}
```

> ⚠️ `download_url` 是 `iesdouyin.com` 重定向 URL，有时效性，建议立即使用。

### tikhub-douyin（远程服务，需认证）

```bash
# 获取视频信息+播放链接（所有平台通用）
mcporter call tikhub-douyin.douyin_web_fetch_one_video_by_share_url share_url:"<链接>"

# 获取最高画质 CDN 地址（推荐，最可靠）
mcporter call tikhub-douyin.douyin_web_fetch_video_high_quality_play_url share_url:"<链接>"
```

**返回字段：**
```json
{
  "data": {
    "original_video_url": "https://cdn.example.com/..."
  }
}
```

---

## ❗️ 排错流程

```
1. 工具返回 error/失败
   ↓
2. 抖音：换一个 MCP（douyin-analyzer ↔ tikhub-douyin）
       B站/YouTube：检查 yt-dlp 是否支持
       TikTok/其他：检查 tikhub-douyin 是否可用
   ↓
3. 抖音：检查 Chromium 是否安装 + DOUYIN_CHROMIUM_PATH 是否设置
   ↓
4. 如果都失败 → 找图文/文字版内容
```

### 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `download_url` 为空 | Playwright Chromium 未安装 | 运行 setup.sh 或手动安装 |
| `DOUYIN_CHROMIUM_PATH` 警告 | 环境变量未设置 | 设置 `export DOUYIN_CHROMIUM_PATH=...` |
| curl 下载失败 | 抖音 URL 已过期 | 改用 TikHub 获取实时 CDN |
| TikHub 返回 401 | API 认证失败 | 检查 mcporter.json 的 TikHub Token |
| yt-dlp 下载失败（B站） | Cookie/地区限制 | 加代理或用 TikHub |
| `analyze_video` 超时 | 视频较大 | 改用两步走 |

### Chromium 安装（国内镜像）

```bash
# 检查是否已安装
ls ~/Library/Caches/ms-playwright/

# 国内镜像安装
PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright \
  ~/openclaw-media/.venv/bin/playwright install chromium
```

---

## 本地转录（mlx_whisper）

```python
import os
# os.environ["HF_HUB_OFFLINE"] = "1"  # 首次运行不能加！需联网下载模型

import mlx_whisper

result = mlx_whisper.transcribe(
    "/path/to/video.mp4",
    path_or_hf_repo="mlx-community/whisper-small-mlx",
    verbose=True
)

for seg in result.get("segments", []):
    print(f"[{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}")
```

### 推荐 Whisper 模型

| 模型 | 参数量 | 速度 | 精度 |
|------|--------|------|------|
| whisper-small-mlx | 244M | 快 | 中等 |
| whisper-base | 74M | 中 | 中 |
| whisper-large-v3-turbo | 809M | 慢 | 高 |

---

## 踩坑记录

### 2026-04-08 抖音下载修复

**问题**：douyin-analyzer 无法获取下载链接

**排查过程**：
1. 官方 API Cookie 失效（`tt_webid=xxx` 是假的）
2. 第三方 API (`liuxingw.com`) 返回 HTML 而非 JSON，已失效
3. TikHub API 需要认证，公共接口返回 401
4. Playwright Chromium 未安装（网络问题导致安装超时）
5. Chromium 版本不匹配（1.58 需要 chromium-1208，镜像只有 1105）
6. subprocess 中的 chromium 路径变量无法传递到代码字符串
7. `iesdouyin.com` 重定向 URL 有时效性

**最终解决方案**：
- 使用 `openclaw-media` 的 playwright 1.42.0（chromium-1105）
- 在 subprocess 代码字符串中硬编码 chromium 路径
- 用 `DOUYIN_CHROMIUM_PATH` 环境变量配置路径
- 两步走替代 `analyze_video`（下载+转录分离）

**教训**：
- 当工具失败时，列出所有 MCP 找替代方案
- MCP 内部变量无法传递到 subprocess 字符串代码
- `analyze_video` 把下载+转录绑在一起容易超时，**两步走更稳定**
- TikHub 返回 `original_video_url` 是真实 CDN 地址，比 `iesdouyin.com` 重定向 URL 更可靠
- f-string 中的 `{{` 会先被外层 f-string 处理，需用 `dict()` 代替字典字面量

### 2026-04-19 mlx_whisper 模型未缓存 / 转录失败

**问题**：mlx_whisper 转录时报 `LocalEntryNotFoundError`，模型从未下载

**排查过程**：
1. `HF_HUB_OFFLINE=1` 阻止了首次下载（HuggingFace Hub 请求被拦截）
2. 网络不通 huggingface.co（Mac mini 无代理）
3. 配置代理后首次运行仍失败（`HF_HUB_OFFLINE=1` 在代码里被设置）
4. 去掉 `HF_HUB_OFFLINE=1` 后成功下载模型并转录

**根因**：
- `HF_HUB_OFFLINE=1` 是为了防止 import 时意外联网，但 mlx_whisper 首次运行需要联网下载模型
- 首次运行后模型会缓存到 `~/.cache/huggingface/hub/`，之后加 `HF_HUB_OFFLINE=1` 才能正常工作

**正确用法**：
```python
# 首次运行（需要网络，下载模型）
import mlx_whisper
result = mlx_whisper.transcribe("/path/video.mp4", path_or_hf_repo="mlx-community/whisper-base-mlx")

# 后续运行（离线模式，加回 HF_HUB_OFFLINE=1）
import os
os.environ["HF_HUB_OFFLINE"] = "1"  # 放 import 之前
import mlx_whisper
result = mlx_whisper.transcribe("/path/video.mp4", ...)
```

**教训**：
- mlx_whisper 模型（mlx-community/whisper-xxx）必须联网下载一次，之后才能离线使用
- 已在代码中全局设置 `HF_HUB_OFFLINE=1` 的环境会阻止首次下载，需临时去掉
- 建议：mlx_whisper 的首次转录不要设置 `HF_HUB_OFFLINE=1`

---

## 🖼️ 视觉增强理解（可选升级）

### 核心思路

视频转录只能获取音频信息，但很多内容**必须看画面才能理解**：
- 图表/数据可视化（说话说"如图所示"但没说具体数值）
- 代码演示（没说具体代码，但画面在展示）
- 文字内容（幻灯片、界面、文档）
- 动画/过渡效果
- 模糊指代（"这里"、"它"、"那样"）

**视觉增强 pipeline**：
1. **智能检测** — 分析转录文本，找出"需要视觉辅助"的节点
2. **精准截帧** — 在关键时间点用 ffmpeg 截取视频帧
3. **图片理解** — MiniMax AI 分析截帧内容
4. **融合输出** — 文字 + 视觉合并 → 最终综合理解

### 使用方法

```bash
# 直接传入视频路径 + 转录结果（JSON格式）
python3 ~/.openclaw/workspace/skills/video-download-transcribe/video_visual_understanding.py \
  /tmp/video.mp4 \
  /tmp/transcript.json

# 或者在转录完成后，将 segments 作为 JSON 传入
python3 ~/.openclaw/workspace/skills/video-download-transcribe/video_visual_understanding.py \
  /tmp/video.mp4 \
  '{"segments": [{"start": 0.0, "end": 5.0, "text": "今天给大家介绍..."}]}'
```

### 工作原理详解

#### 1. 视觉需求检测（analyze_transcript_for_visual_needs）

两种模式并行：

**LLM 模式**（优先）：发送完整转录给 LLM，让它找出需要视觉辅助的节点，输出结构化 JSON。

**规则模式**（fallback）：基于关键词和启发式规则检测：
| 视觉类型 | 触发关键词 | 置信度 |
|----------|-----------|--------|
| chart | 图、表、图表、曲线、数据、趋势 | 0.65 |
| code | 代码、terminal、命令行 | 0.65 |
| text_display | 屏幕上、显示、打印、console | 0.65 |
| demo | 演示、操作、点击、运行、效果 | 0.65 |
| diagram | 结构、框架、流程、architecture | 0.65 |
| animation | 动画、GIF、过渡、转场 | 0.65 |
| unclear_reference | 这个/那/它/当时（密集出现+短文本）| 0.70 |

去重策略：相同 `visual_type` 在 5 秒内只保留一个。

#### 2. 精准截帧（extract_frames_at_times）

```python
# 时间点 = 段落开始 + 持续时间 × 0.6
# 原因：说话提到视觉内容时，画面已经展示了 一段时间
mid_time = start + duration * 0.6
```

```bash
ffmpeg -y -ss 12.5 -i video.mp4 -vframes 1 -q:v 2 frame.jpg
```
- `-ss 12.5`：从 12.5 秒开始
- `-vframes 1`：只取一帧
- `-q:v 2`：JPEG 质量（1=最高，2=高，3=普通）

#### 3. MiniMax 图片理解（call_minimax_image）

每种视觉类型使用专用 prompt：

| visual_type | MiniMax prompt 策略 |
|-------------|-------------------|
| chart | "详细描述图表内容：标题、坐标轴、数据、趋势" |
| code | "描述代码内容：语言、关键代码行、输出、错误" |
| text_display | "提取屏幕上所有可见文字：界面、按钮、输入框" |
| demo | "描述演示内容：界面状态、操作步骤、可见结果" |
| diagram | "描述图示结构：标签、箭头、连接关系" |
| unclear_reference | "描述画面最突出内容，特别是可能被模糊指代的部分" |

#### 4. 融合输出（build_visual_understanding_prompt）

最终 prompt 包含：
- 完整转录（音频）
- 每个关键帧的分析（视觉）
- 时间对应关系

发送给 LLM 时要求：
- 融合而非割裂
- 视觉内容给出具体数值/代码/文字
- 音频矛盾时以视觉为准

### 输出示例

```
=== 视频综合理解（融合文字+视觉） ===

--- [15s 截帧 | 类型: chart] ---
视觉分析: 这是一张折线图，标题为"2024年Q1-Q4营收趋势"，
         X轴是季度，Y轴是营收（亿元），
         Q1: 12亿 → Q2: 18亿 → Q3: 25亿 → Q4: 32亿，
         整体呈上升趋势，Q3到Q4增速最快。
相关音频: "可以看到这个增长是很快的"

--- [45s 截帧 | 类型: code] ---
视觉分析: Python 代码片段，使用 FastAPI 框架，
         关键代码：@app.post("/api/users")
         函数返回 JSON: {"id": 1, "name": "Alice"}
相关音频: "这里用装饰器定义一个接口"

[综合分析]
这张视频介绍了公司年度营收，...
...
```

### 与原 pipeline 的关系

| 阶段 | 原 pipeline | 视觉增强 pipeline |
|------|------------|-----------------|
| 下载 | ✅ | ✅ |
| 转录 | ✅ | ✅ |
| 分析 | ❌ 纯音频 | ✅ 音频 + 视觉融合 |
| 适用场景 | 新闻/播客/纯语音 | 教程/演示/图表/代码/PPT |

### 限制与注意事项

- **需要 ffmpeg**：`brew install ffmpeg`
- **截帧数量**：建议每次不超过 10 个关键节点（MiniMax API 调用成本）
- **时间精度**：ffmpeg 截帧可能有 ±0.5 秒误差
- **长视频**：建议先截取关键片段再分析，避免处理整个视频
