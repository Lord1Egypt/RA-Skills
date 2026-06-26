---
name: video-content-analyzer
description: 下载视频并用AI分析内容 - 支持B站/抖音/YouTube等平台，提取语音内容并分析视频结构
version: "1.1.0"
author: laipishe
license: MIT
category: marketing
tags:
  - 视频分析
  - 内容理解
  - 语音转文字
  - B站
  - 抖音
  - YouTube
department: Marketing

allowed-tools: Exec

models:
  recommended:
    - minimax/MiniMax-M2.5
    - claude-sonnet-4
  compatible:
    - gpt-4o

languages:
  - zh

capabilities:
  - video_download
  - audio_extraction
  - speech_to_text
  - content_analysis
  - feishu_wiki_report
  - supabase_storage

related_skills:
  - viral-video-analysis
  - openai-whisper-api
  - feishu-wiki
  - supabase
  - google-search

dependencies:
  - yt-dlp (视频下载)
  - ffmpeg (音频提取)
  - openai-whisper-api (语音转文字)
---

# 视频内容分析器

自动下载视频并用AI分析内容，提取完整的语音文案，分析视频结构和节奏。

## 功能

1. **视频下载** - 支持B站、抖音、YouTube等主流平台
2. **音频提取** - 用ffmpeg提取视频中的音频
3. **语音转写** - 用OpenAI Whisper API转写为文字
4. **内容分析** - AI分析视频结构、节奏、钩子等

## 前置要求

### 必须安装的工具

```bash
# 安装 yt-dlp (视频下载)
pip3 install --break-system-packages yt-dlp

# 安装 ffmpeg (音频处理)
# Mac: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

### API Key

需要设置 OpenAI API Key（用于Whisper转写）：
```bash
export OPENAI_API_KEY="your-api-key"
```

或在 `~/.openclaw/openclaw.json` 中配置：
```json
{
  "skills": {
    "openai-whisper-api": {
      "apiKey": "your-api-key"
    }
  }
}
```

## 使用方法

### 输入

用户提供视频链接，例如：
- B站: `https://www.bilibili.com/video/BV1xuPYzcEdo`
- 抖音: `https://www.douyin.com/video/xxx`
- YouTube: `https://www.youtube.com/watch?v=xxx`

### 输出

完整的分析报告，包括：
1. 📝 完整文案（语音转写）
2. 🎬 视频结构分析（章节/时间节点）
3. 🪝 钩子分析
4. ⏱️ 节奏分析
5. 💡 内容总结

---

## 工作流程

```
1. 输入视频链接
        ↓
2. yt-dlp 下载视频
        ↓
3. 获取视频时长，计算关键帧数量
        ↓
4. ffmpeg 提取关键帧（每30秒1帧）
        ↓
5. 获取弹幕数据（若有）
        ↓
6. Whisper API 转写（若有API）
        ↓
7. Google Search 补充调研（搜索视频相关背景信息）
        ↓
8. AI 分析画面+弹幕+文案+搜索背景
        ↓
9. 存储视频元数据到 Supabase
        ↓
10. 输出完整报告 / 写入飞书 Wiki
```

---

## 关键帧提取（优化版）

### 自动提取策略

```bash
# 视频时长 / 30 = 关键帧数量
# 例如：8分钟视频 → 16-17张关键帧

# 提取关键帧（每30秒1帧）
ffmpeg -ss 00:00:00 -i video.mp4 -vframes 1 -q:v 2 frame_001.jpg -y
ffmpeg -ss 00:00:30 -i video.mp4 -vframes 1 -q:v 2 frame_002.jpg -y
ffmpeg -ss 00:01:00 -i video.mp4 -vframes 1 -q:v 2 frame_003.jpg -y
# ... 以此类推
```

### 帧数建议

| 视频时长 | 建议帧数 | 间隔 |
|---------|---------|------|
| < 3 分钟 | 6-8 帧 | 每20-30秒 |
| 3-10 分钟 | 12-20 帧 | 每30秒 |
| 10-30 分钟 | 30-60 帧 | 每30秒 |

### 批量提取脚本

```python
import subprocess
import os

def extract_frames(video_path, output_dir, interval=30):
    """提取视频关键帧
    
    Args:
        video_path: 视频文件路径
        output_dir: 输出目录
        interval: 帧间隔（秒），默认30秒
    """
    # 获取视频时长
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 
           'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', 
           video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    duration = float(result.stdout.strip())
    
    # 计算帧数
    num_frames = int(duration // interval) + 1
    
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(num_frames):
        seconds = i * interval
        mins = seconds // 60
        secs = seconds % 60
        ts = f'{mins:02d}:{secs:02d}'
        out = f'{output_dir}/frame_{i+1:03d}.jpg'
        
        cmd = ['ffmpeg', '-ss', ts, '-i', video_path, 
               '-vframes', '1', '-q:v', '2', out, '-y']
        subprocess.run(cmd, capture_output=True)
        print(f'✓ Extracted {out}')
    
    return num_frames

# 使用示例
extract_frames('/tmp/video.mp4', '/tmp/frames', interval=30)
```

---

## 命令行示例

### 手动下载B站视频

```bash
# 下载B站视频（仅音频）
yt-dlp -x --audio-format mp3 -o "%(title)s.%(ext)s" "https://www.bilibili.com/video/BV1xuPYzcEdo"

# 下载视频（最佳画质）
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "%(title)s.%(ext)s" "https://www.bilibili.com/video/BV1xuPYzcEdo"

# 仅下载字幕
yt-dlp --write-subs --skip-download -o "%(title)s" "https://www.bilibili.com/video/BV1xuPYzcEdo"
```

### 提取音频

```bash
# 从视频提取音频
ffmpeg -i input.mp4 -vn -acodec libmp3lame -q:a 2 output.mp3

# 或直接用yt-dlp
yt-dlp -x --audio-format mp3 "https://www.bilibili.com/video/BV1xuPYzcEdo"
```

---

## 输出模板

```markdown
# 📹 视频内容分析报告

**视频**: [标题]
**链接**: [URL]
**时长**: [时长]
**平台**: [B站/抖音/YouTube]
**关键帧数**: [数量]

---

## 📝 完整文案

[Whisper转写的完整语音文案]

---

## 🎬 视频结构（基于关键帧）

| 时间 | 画面内容 | 阶段 |
|------|---------|------|
| 0:00 | [第1帧描述] | 钩子 |
| 0:30 | [第2帧描述] | 铺垫 |
| 1:00 | [第3帧描述] | 主题展开 |
| ... | ... | ... |

---

## 🪝 钩子分析

[开头画面的钩子设计分析]

---

## 🎯 内容分层

- **开头 (0-1分钟)**:
- **中段 (1-5分钟)**:
- **高潮 (5-7分钟)**:
- **结尾 (7-分钟)**:

---

## 💡 爆款元素

| 元素 | 分析 |
|------|------|
| 情感点 | [弹幕高频情感词] |
| 互动点 | [弹幕互动热点] |
| 记忆点 | [金句/名场面] |

---

## 📊 弹幕热点词

```
[从danmaku.xml提取的高频弹幕]
```

---

## 🔥 成功原因总结

1. [核心爆款因素]
2. [情感共鸣点]
3. [创新/独特之处]

---

## 总结

[视频的核心内容和亮点]

---

## 📎 参考来源

> ⚠️ 写入飞书 Wiki 时，以下链接必须使用 `text_run.link` 属性，不能用 Markdown 语法

1. [来源1标题](https://example.com/page1)
2. [来源2标题](https://example.com/page2)
```

---

## Google Search 引用链接处理

分析视频时，可使用 Google Search 补充背景信息（如创作者资料、相关事件、数据来源等）。

### ⚠️ 飞书 Wiki 引用链接格式

飞书 Wiki **不支持 Markdown 链接语法** `[text](url)`。写入飞书 Wiki 时，引用链接必须使用飞书 docx API 的 `text_run` + `link` 属性：

```json
{
  "block_type": 2,
  "text": {
    "elements": [
      {"text_run": {"content": "来源："}},
      {
        "text_run": {
          "content": "Google搜索结果标题",
          "link": {"url": "https://example.com/full-url"}
        }
      }
    ]
  }
}
```

### 引用链接写入步骤

1. 用 `web_search` 工具搜索视频相关背景信息
2. 从搜索结果中提取 `url`（必须是完整的 `https://` 开头的URL，**不要**使用相对路径或省略协议）
3. 写入飞书 Wiki 时，每个引用链接使用 `text_run` + `link` 属性
4. 引用区块放在报告末尾，标题为「📎 参考来源」

### 常见错误

| 错误 | 原因 | 修复 |
|------|------|------|
| 链接显示为纯文本 `[text](url)` | 使用了 Markdown 语法 | 改用 `text_run` + `link` 属性 |
| 链接点击后 404 | URL 不完整（缺少协议或路径） | 确保使用搜索结果返回的完整 URL |
| 链接指向搜索结果页而非原始页面 | 使用了搜索引擎跳转链接 | 提取实际目标页面的 URL |

---

## Supabase 元数据存储

分析完成后，将视频元数据存储到 Supabase 以便后续查询和统计。

### 前置配置

在 `~/.openclaw/openclaw.json` 中配置 Supabase：
```json
{
  "skills": {
    "supabase": {
      "url": "https://your-project.supabase.co",
      "anonKey": "your-anon-key"
    }
  }
}
```

### 数据库表结构

```sql
CREATE TABLE video_analyses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  video_url TEXT NOT NULL,
  platform TEXT NOT NULL,          -- bilibili/douyin/youtube
  title TEXT,
  duration_seconds INTEGER,
  view_count BIGINT,
  like_count BIGINT,
  comment_count BIGINT,
  danmaku_count INTEGER,
  transcript TEXT,
  analysis_summary JSONB,         -- AI分析结果摘要
  key_frames_count INTEGER,
  feishu_wiki_url TEXT,            -- 飞书Wiki报告链接
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 写入示例

```bash
# 使用 Supabase REST API 写入元数据
curl -s -X POST "${SUPABASE_URL}/rest/v1/video_analyses" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "video_url": "https://www.bilibili.com/video/BV1xuPYzcEdo",
    "platform": "bilibili",
    "title": "视频标题",
    "duration_seconds": 480,
    "view_count": 100000,
    "like_count": 5000,
    "comment_count": 300,
    "danmaku_count": 2000,
    "transcript": "完整转写文本...",
    "analysis_summary": {"hook": "...", "structure": "..."},
    "key_frames_count": 16
  }'
```

### ⚠️ 常见写入失败原因

| 错误 | 原因 | 修复 |
|------|------|------|
| 401 Unauthorized | `anonKey` 未配置或过期 | 检查 `openclaw.json` 中的 Supabase 配置 |
| 403 Forbidden | RLS 策略阻止写入 | 在 Supabase Dashboard 添加 INSERT 策略 |
| 422 Validation | 字段类型不匹配 | 确保 `duration_seconds` 是整数，`view_count` 是大整数 |
| `danmaku_count` 为 null | B站弹幕未提取 | 检查 yt-dlp 是否成功下载弹幕 XML |
| `analysis_summary` 写入失败 | JSONB 字段格式错误 | 确保传入有效 JSON 对象，非字符串 |

---

## 飞书 Wiki 报告写入

分析完成后可将报告写入飞书 Wiki 知识库。参考 `feishu-wiki` 技能获取 token 和创建页面。

### 写入流程

1. 获取 `tenant_access_token`
2. 获取目标 Wiki 空间的 `space_id`
3. 创建页面节点，获取 `obj_token`
4. 逐块写入报告内容（使用 docx blocks API）

### 关键：链接块格式

飞书 Wiki 的 docx API 中，**所有超链接必须使用 `text_run.link` 属性**，不能使用 Markdown 语法：

```bash
# 正确：写入带链接的引用来源
curl -s -X POST \
  "https://open.feishu.cn/open-apis/docx/v1/documents/${OBJ_TOKEN}/blocks/${OBJ_TOKEN}/children" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [{
      "block_type": 2,
      "text": {
        "elements": [
          {"text_run": {"content": "📎 参考来源\n"}},
          {"text_run": {"content": "1. "}},
          {"text_run": {"content": "搜索结果标题", "link": {"url": "https://example.com/page1"}}},
          {"text_run": {"content": "\n2. "}},
          {"text_run": {"content": "另一个来源", "link": {"url": "https://example.com/page2"}}}
        ]
      }
    }],
    "index": -1
  }'
```

---

## 注意事项

1. 📡 **网络** - 下载视频需要稳定的网络
2. 💰 **费用** - Whisper API按分钟计费（~$0.006/分钟）
3. ⏱️ **时间** - 完整分析需要3-5分钟
4. 📏 **长度** - 建议视频时长 < 30分钟
5. 🔐 **版权** - 仅供学习分析使用，勿用于商业目的
6. 🔗 **飞书链接** - 写入飞书 Wiki 时，链接必须用 `text_run.link` 属性，不能用 Markdown `[text](url)` 语法
7. 🗄️ **Supabase** - 确保 RLS 策略允许写入，字段类型与表结构匹配

---

## 故障排除

### 下载失败
- 检查网络连接
- 尝试使用代理
- B站可能需要Cookie认证

### Whisper转写失败
- 确认OPENAI_API_KEY正确设置
- 检查API余额
- 音频文件是否损坏

### ffmpeg问题
- 确认ffmpeg已安装: `ffmpeg -version`
- Mac用户: `brew install ffmpeg`
```
