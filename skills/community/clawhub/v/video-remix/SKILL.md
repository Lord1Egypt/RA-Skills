---
name: video-remix
description: YouTube 视频处理助手 - Gemini 智能分析 + 下载 + 剪辑 + 配音 + 硬字幕合成 + 局域网 HTTP 分享
---

# 🎬 Video Remix Skill (V6 - Browser 自动化完整版)

YouTube 视频处理技能，采用 **Gemini First** 流程：先用 Gemini 智能分析获取时间戳和文案，再精准下载、剪辑、配音、合成硬字幕，**自动对齐音频时长**，最后通过**局域网 HTTP**分享。

## ✨ 触发条件

当用户提到以下关键词时自动触发：
- YouTube 视频处理
- 视频剪辑
- 自动配音
- 视频转录
- 下载 YouTube 视频
- 制作视频解说
- 视频文案生成
- AI 配音视频
- 硬字幕合成
- 局域网分享视频

## 🧠 Gemini 提示词模板

### 可复制提示词

将 `{VIDEO_URL}` 替换为实际链接：

```text
请分析这个 YouTube 视频：{VIDEO_URL}

我需要你帮我提取精彩片段并生成抖音风格的解说文案。

可选参数（如未提供则忽略）：
- 期望总时长（秒）：{TARGET_DURATION}

## 📋 任务要求

### 1. 片段提取
- 片段数量由你决定（以叙事完整、节奏顺畅为准；宁可少而精）
- 每个片段只讲**一个核心动作/场景**，不要堆砌多个事件
- 片段之间要有**逻辑连贯性**，形成完整的故事线（开头→发展→高潮→结尾）
- 若提供“期望总时长（秒）”，请使所有片段总时长 Σ(end - start) ≈ 该值（允许 ±10%）
- 若未提供期望总时长，则由你根据内容密度与节奏自行决定合理总时长（通常 20–60 秒），并据此规划片段

### 2. 文案创作
- 用**中文**写抖音风格解说（口语化、有情绪、有梗）
- 每段文案只说清楚：**"发生了什么 + 什么感受"**
- 开头要抓人（用"看好了！""家人们！"等吸引注意）
- 避免模糊描述（不要说"这个操作很厉害"，要说清楚哪里厉害）

### 3. 时长匹配（重要！）
- 语速约 3 字/秒（舒适语速）
- 字数公式：`字数 ≈ (end - start) × 3`
- 参考：
  - 5 秒片段 → 约 15 字
  - 10 秒片段 → 约 30 字
  - 15 秒片段 → 约 45 字

### 4. 质量标准

  - 每个片段简单清晰，只讲一件事
  - 文案明确具体，一听就懂
  - 故事完整连贯，有起承转合
  - 字数匹配时长，语速舒适

### 5. 避免的问题

  - 一个片段里塞进太多信息
  - 文案模糊不清
  - 片段之间跳跃太大
  - 文案过长导致语速过快
  - **不要选择出现人脸的片段**（优先选择景物、动作、物体特写）
  - **不要选择有明显水印/Logo 的片段**（避免平台水印、品牌标识等）
  - **不要选择带字幕的片段**

## 📤 输出格式

请**严格**按以下 JSON 格式返回（不要多余的解释）：

{
  "douyin_title": "抖音爆款标题（15-25 字，强钩子，口语化）",
  "douyin_tags": ["#爆款标签1", "#爆款标签2", "#爆款标签3", "#爆款标签4", "#爆款标签5"],
  "youtube_url": "视频 URL",
  "clips": [
    {
      "start": 0,
      "end": 5,
      "script": "文案内容（20-25 字）"
    },
    {
      "start": 5,
      "end": 12,
      "script": "文案内容（约 30 字）"
    }
  ]
}

```

---

**将 Gemini 返回的 JSON 保存到 `temp/gemini_result.json`，然后运行脚本。**

## 📋 使用示例

### 示例 1：DIY 手工视频

```json
{
  "douyin_title": "几块钱的 PVC 管，居然能做出顶级钓鱼神器？看完我人傻了！",
  "douyin_tags": ["#钓鱼", "#DIY手工", "#硬核改造", "#生活妙招", "#涨知识"],
  "youtube_url": "https://www.youtube.com/shorts/KV-TLUADEs0",
  "clips": [
    {
      "start": 0,
      "end": 20,
      "script": "看好了！大神教你用几块钱的 PVC 管，手工打造顶级钓鱼神器，这骚操作简直太硬核了，钓友们赶紧集合围观！"
    },
    {
      "start": 21,
      "end": 45,
      "script": "第一步先给管子精准加热，千万别眨眼，看这手法多稳，通过火烤让塑料变软，这是制作钓鱼握把的关键一步。"
    },
    {
      "start": 46,
      "end": 75,
      "script": "接下来是细节处理，反复加热塑形，每一个弧度都得经过精雕细琢，这就是传说中的纯手工温度，新手一看就能学会。"
    },
    {
      "start": 76,
      "end": 105,
      "script": "开始组装核心部件，再次加热扩口处理，看这契合度，比买的还要强，这动手能力我只能说真心给跪了！"
    },
    {
      "start": 106,
      "end": 120,
      "script": "大功告成！超实用的 DIY 钓鱼装备新鲜出炉，拿着它去河边，你就是整条街最靓的仔，学会的家人们记得点赞收藏！"
    }
  ]
}
```

## 🚀 调用方式

### 流程总览（输入/输出一目了然）

```
阶段 0：依赖检查/安装
  输入：本机环境
  输出：ffmpeg、yt-dlp、edge-tts 就绪（含 libass）

阶段 1：片段规划（优先 Gemini，失败则离线）
  输入：YouTube URL（必填）、期望总时长秒数{TARGET_DURATION}（可选）
  输出：temp/gemini_result.json
        ├─ douyin_title（可选）
        ├─ douyin_tags（可选）
        └─ clips[]: { start, end, script }

阶段 2：视频处理脚本
  输入：temp/gemini_result.json
  输出：output/final_hardsub.mp4、output/full_voiceover.mp3、output/subtitles.srt、HTTP 分享地址
```

---

### 阶段 0：依赖检查与安装（先执行）

```bash
# 0.1 基础工具
command -v python3 >/dev/null || { echo "缺少 python3"; exit 1; }
command -v pip3 >/dev/null || { echo "缺少 pip3"; exit 1; }

# 0.2 平台依赖（macOS）
if [[ "$OSTYPE" == "darwin"* ]]; then
  command -v brew >/dev/null || {
    echo "未检测到 Homebrew，请先安装：https://brew.sh/";
    exit 1;
  }
  for pkg in ffmpeg-full yt-dlp libass; do
    brew list --versions "$pkg" >/dev/null 2>&1 || brew install "$pkg";
  done
  # 注意：包名是 ffmpeg-full，但安装后可执行文件仍然是 `ffmpeg`
fi

# 0.3 平台依赖（Ubuntu/Debian）
if command -v apt >/dev/null 2>&1; then
  sudo apt update -y
  sudo apt install -y ffmpeg yt-dlp libass-dev
fi

# 0.4 Python 依赖（幂等安装）
pip3 show edge-tts >/dev/null 2>&1 || pip3 install edge-tts
pip3 show yt-dlp   >/dev/null 2>&1 || pip3 install yt-dlp

# 0.5 FFmpeg 是否支持 libass（硬字幕需要）
if ! ffmpeg -version 2>&1 | grep -qi libass; then
  echo "⚠️ 当前 ffmpeg 不包含 libass，硬字幕可能失败。请安装包含 libass 的 ffmpeg。"
  echo "macOS 建议：brew install ffmpeg-full（并确保 libass 已安装：brew install libass）"
fi
```

---

**顺序要求（强制）：**
- 完成阶段 0 依赖检查后，**必须立即执行阶段 1（片段规划）** 产出 `temp/gemini_result.json`
- 阶段 1 有两种路径：**1A Gemini**（优先）或 **1B 离线**（Gemini 不可用时）
- 仅当 `temp/gemini_result.json` 存在且为有效 JSON 时，才允许进入阶段 2
- **禁止**在没有 `temp/gemini_result.json` 的情况下直接进入阶段 2

---

### 阶段 1A：Gemini 智能分析（浏览器自动化，强制）

**触发时机：** 用户提供 YouTube URL 后 **立即执行**


**执行内容：**
```python
# 1. 启动浏览器
browser(action="start", profile="openclaw")

# 2. 打开 Gemini
browser(action="navigate", url="https://gemini.google.com/")

# 3. 捕获页面元素（获取输入框 ref）
snapshot = browser(action="snapshot", refs="aria")

# 4. 构建完整提示词（替换 {VIDEO_URL}）
prompt = """请分析这个 YouTube 视频：{VIDEO_URL}
...（完整提示词）...
请严格按以下 JSON 格式返回（不要多余的解释）："""

# 5. 输入提示词
browser(action="act", kind="type", ref="e12", text=prompt)

# 6. 发送
browser(action="act", kind="press", key="Enter")

# 7. 等待生成（Gemini 通常需要 5-15 秒）
browser(action="act", kind="wait", timeMs=10000)

# 8. 再次捕获页面（获取响应）
snapshot = browser(action="snapshot", refs="aria")

# 9. 提取响应内容
json_text = browser(action="act", kind="evaluate", 
                    fn="() => document.querySelector('[aria-label*=\"Response\"]').innerText")

# 10. 解析并保存 JSON
import json
data = json.loads(json_text)
with open("temp/gemini_result.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 11. 关闭浏览器
browser(action="close", targetId=snapshot["targetId"])
 

---

### 阶段 2：视频处理脚本

**触发时机：** 确认 `temp/gemini_result.json` 已生成后

**前置检查：**
```bash
# 检查 JSON 是否存在
if [ ! -f temp/gemini_result.json ]; then
    echo "❌ 错误：gemini_result.json 不存在，请先执行阶段 1"
    exit 1
fi

# 验证 JSON 格式
python3 -c "import json; json.load(open('temp/gemini_result.json'))" || \
    { echo "❌ 错误：JSON 格式无效"; exit 1; }

# 可选：快速依赖自检（确保阶段 0 已完成）
command -v ffmpeg >/dev/null || { echo "缺少 ffmpeg（请安装 ffmpeg-full 或确保 ffmpeg 含 libass）"; exit 1; }
command -v yt-dlp >/dev/null || { echo "缺少 yt-dlp"; exit 1; }
python3 -c "import edge_tts" 2>/dev/null || { echo "缺少 edge-tts（pip3 install edge-tts）"; exit 1; }
```

**执行脚本：**
```bash
cd /Users/admin/.openclaw/workspace/skills/video-remix
python3 scripts/gemini_first_remix.py
```

**脚本会自动完成：**
- 读取 `temp/gemini_result.json`
- 下载 YouTube 视频（完整原视频；视频很长也没关系，耐心等待即可）
- 剪辑片段
- 生成 TTS 配音
- 合成硬字幕
- 启动 HTTP 服务器

**输入：**
- `temp/gemini_result.json`

**输出：**
- `output/final_hardsub.mp4`
- `output/full_voiceover.mp3`
- `output/subtitles.srt`
- 局域网 HTTP 分享地址（端口 8888）

**✅ 阶段 2 完成标志：**
- `output/final_hardsub.mp4` 生成，HTTP 服务启动

### 支持的功能

1. **Gemini 智能分析** - 直接获取精彩片段时间戳 + 抖音风格文案
2. **文案时长估算** - 自动计算文案字数是否匹配片段时长（4.5 字/秒）
3. **下载** - 使用 yt-dlp 通过代理下载 YouTube 视频
4. **剪辑** - 根据时间戳精准裁剪片段
5. **配音** - 使用 Edge-TTS 生成中文配音（免费，无需 API）
6. **音频自动对齐** - 如果音频比视频长，自动加速匹配视频时长
7. **字幕** - 自动生成 SRT 字幕文件（基于视频时长）
8. **硬字幕合成** - FFmpeg 烧录硬字幕到视频
9. **局域网 HTTP 分享** - 自动启动 HTTP 服务器，生成可访问链接

## ⚙️ 配置说明

### 环境变量

```bash
# 输出目录
export VR_OUTPUT_DIR="./output"

# 临时文件目录
export VR_TEMP_DIR="./temp"

# 代理配置（YouTube 下载必需）
export HTTP_PROXY=http://127.0.0.1:10808
export HTTPS_PROXY=http://127.0.0.1:10808

# TTS 声音 (xiaoxiao/yunxi/yunjian/xiaoyi/yunyang 等)
export VR_TTS_VOICE="xiaoxiao"
```

### Gemini 元数据格式

`temp/gemini_result.json` 示例：

```json
{
  "douyin_title": "这里填抖音爆款标题",
  "douyin_tags": ["#标签1", "#标签2", "#标签3", "#标签4", "#标签5"],
  "youtube_url": "https://youtube.com/watch?v=VIDEO_ID",
  "clips": [
    {
      "start": 0,
      "end": 5,
      "script": "家人们谁懂啊！本来只想安安静静钓个鱼..."
    },
    {
      "start": 5,
      "end": 12,
      "script": "好家伙，这哪是钓鱼，这是在喂祖宗啊！..."
    }
  ]
}
```

**文案字数建议：**
- 5 秒片段 → 约 20-25 字
- 10 秒片段 → 约 40-50 字
- 公式：`字数 ≈ 时长 × 4.5`

## 🎤 可用声音

| 声音 | 描述 | 适用场景 |
|------|------|----------|
| xiaoxiao | 女声，温暖亲切 | 新闻、解说（最常用） |
| yunxi | 男声，平静稳重 | 正式内容 |
| yunjian | 男声，充满活力 | 体育、热血 |
| xiaoyi | 女声，活泼开朗 | 轻松内容 |
| yunyang | 男声，专业播报 | 新闻、正式 |

## 📝 输出说明

处理完成后输出：
- `final_hardsub.mp4` - 硬字幕版本（字幕烧录到视频）
- `full_voiceover.mp3` - 完整配音音频（已加速对齐）
- `subtitles.srt` - SRT 字幕文件

所有文件保存在 `output/` 目录。

**HTTP 访问地址：**
```
http://<局域网 IP>:8888/final_hardsub.mp4
http://<局域网 IP>:8888/  (浏览所有文件)
```

## ⚠️ 注意事项

- **执行顺序**：严格按 `## 🚀 调用方式` 的阶段 0 → 1 → 2 执行。
- **不要跳过 Gemini**：阶段 2 的剪辑与文案完全依赖 `temp/gemini_result.json`，不支持先下载再“随便剪”。
- **Browser 自动化**：
  - Gemini 输出可能需要等待（建议 `wait timeMs >= 10000`）。
  - 页面更新会导致 aria-ref 变化，需要重新 snapshot。
  - 结束后记得关闭标签页，避免残留会话。
- **代理**：YouTube 下载通常需要代理（`HTTP_PROXY/HTTPS_PROXY` 指向可用代理）。
- **硬字幕**：macOS 推荐安装 `ffmpeg-full`，并用 `ffmpeg -version | grep libass` 确认支持 libass。
- **HTTP 服务**：脚本会常驻运行 HTTP 服务，`Ctrl+C` 才会停止。

## 🎯 文案时长参考

| 片段时长 | 建议字数 | 示例 |
|---------|---------|------|
| 3 秒 | 10-15 字 | "这操作太秀了！" |
| 5 秒 | 20-25 字 | "家人们谁懂啊！本来只想钓个鱼..." |
| 10 秒 | 40-50 字 | "好家伙，这哪是钓鱼，这是在喂祖宗啊！..." |
| 15 秒 | 60-70 字 | 完整场景描述 + 情绪渲染 |

**超出建议字数的处理：**
- 脚本会自动检测并提示
- 后期会加速音频匹配视频时长
- 加速超过 2.0x 时可能影响音质，建议优化文案

---

## 🔧 故障排查

### ❌ 最常见错误：阶段 2 执行时 JSON 不存在

**症状：**
```bash
$ python3 scripts/gemini_first_remix.py
📖 加载 Gemini 元数据：temp/gemini_result.json
Traceback (most recent call last):
  FileNotFoundError: [Errno 2] No such file or directory: 'temp/gemini_result.json'
```

**原因：** 阶段 1（Gemini 分析）未执行或未完成

**解决方案：**
```bash
# 1. 检查 JSON 是否存在
ls -la temp/gemini_result.json

# 2. 如不存在，先执行阶段 1（browser 访问 Gemini）
# 3. 确认 JSON 生成后，再运行脚本
```

**预防方法：** 在运行脚本前添加前置检查：
```bash
if [ ! -f temp/gemini_result.json ]; then
    echo "❌ 错误：gemini_result.json 不存在，请先执行阶段 1（Gemini 分析）"
    exit 1
fi
python3 scripts/gemini_first_remix.py
```

---

### Browser 自动化失败（阶段 1）

| 问题 | 解决方案 |
|------|----------|
| Gemini 页面无法打开 | 检查网络连接，确认 `browser(action=start)` 成功 |
| 输入框 ref 找不到 | 重新 `snapshot` 获取最新 aria-refs |
| 响应超时 | 增加 `wait timeMs` 到 15000 或更长 |
| 返回非 JSON 内容 | Gemini 可能拒绝分析，重试或更换 URL |
| 浏览器残留 | 手动 `browser(action=stop)` 清理会话 |

### 脚本执行失败（阶段 2）

| 问题 | 解决方案 |
|------|----------|
| `temp/gemini_result.json` 不存在 | **先执行阶段 1（Gemini 分析）** |
| JSON 格式无效 | 检查 Gemini 返回内容，确保是有效 JSON |
| clips 数组为空 | Gemini 未提取到片段，重试或更换视频 |
| yt-dlp 下载失败 | 检查代理配置 `HTTP_PROXY=http://127.0.0.1:10808` |
| FFmpeg libass 不支持 | 运行 `brew install libass` 或下载完整版 FFmpeg |
| 音频加速失真 | 优化文案减少字数，或接受 1.5x 以内加速 |
| HTTP 服务器无法启动 | 检查端口 8888 是否被占用 |

### 快速诊断命令

```bash
# 检查 FFmpeg libass 支持
ffmpeg -version 2>&1 | grep libass

# 检查代理
curl -x http://127.0.0.1:10808 https://www.youtube.com -I

# 检查 Python 依赖
pip3 list | grep -E "edge-tts|yt-dlp"

# 检查 temp 目录
ls -la temp/
```
