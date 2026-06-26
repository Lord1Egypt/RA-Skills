# TikTok Creator Pipeline (v6)

> **主方案**：MCP（mcporter）— 零依赖，支持 7 大平台  
> **备用方案**：Python SDK（tikhub）— 仅在 MCP 不可用时使用

## ⚠️ 首次必读

### MCP 配置（MCP 服务器已配置，无需额外操作）

MCP 配置在 `~/.openclaw/workspace/config/mcporter.json`，已包含以下服务器：

| Server | 平台 | 工具数 |
|--------|------|--------|
| `tikhub-bilibili` | B站 | 41 |
| `tikhub-douyin` | 抖音 | 245 |
| `tikhub-tiktok` | TikTok | 204 |
| `tikhub-youtube` | YouTube | 37 |
| `tikhub-xiaohongshu` | 小红书 | 71 |
| `tikhub-weibo` | 微博 | 64 |
| `tikhub-kuaishou` | 快手 | 33 |

### API Key

存储在 `~/.openclaw/workspace/.env` → `TIKHUB_API_KEY`

### 计费说明

TikHub API 并非完全免费：
- **余额**：`$4.98`（当前）
- **缓存机制**：结果缓存 24 小时，重复调用走缓存不收费
- **价格参考**：查询接口便宜（约几分钱），下载直链接口稍贵

---

## 核心操作（MCP 方案）

### B站视频 → 完整字幕 + 内容分析

**Step 1：获取视频信息**
```bash
mcporter call tikhub-bilibili.bilibili_web_fetch_one_video bv_id="BV号"
```

**Step 2：获取 AI 字幕（完整文字稿）**
```bash
# 先获取字幕 URL
mcporter call tikhub-bilibili.bilibili_web_fetch_video_subtitle a_id="av号" c_id="cid"

# 下载字幕文件（JSON 格式，含时间戳）
curl -sL "字幕URL" -H "User-Agent: Mozilla/5.0" -o subtitle.json
```

**Step 3：获取弹幕**
```bash
mcporter call tikhub-bilibili.bilibili_web_fetch_video_danmaku cid="cid"
```

**Step 4：获取下载直链（分段 m4s，需 ffmpeg 合并）**
```bash
mcporter call tikhub-bilibili.bilibili_web_fetch_video_playurl bv_id="BV号" cid="cid"
```

### 抖音视频 → 文字稿

**Step 1：从链接提取 aweme_id**
```bash
# 短链接解析
curl -sI "https://v.douyin.com/xxx" | grep -i location

# 完整链接直接截取末尾数字
```

**Step 2：获取视频信息**
```bash
mcporter call tikhub-douyin.douyin_web_fetch_one_video aweme_id="aweme_id"
```

**Step 3：获取下载直链（MP4）**
```bash
mcporter call tikhub-douyin.douyin_app_v3_fetch_video_high_quality_play_url aweme_id="aweme_id"
```

**Step 4：字幕/弹幕**
```bash
# 字幕（需视频有字幕）
# 弹幕
mcporter call tikhub-douyin.douyin_web_fetch_one_video_danmaku item_id="aweme_id" duration=秒数 end_time=时间戳 start_time=0
```

### TikTok 视频

```bash
mcporter call tikhub-tiktok.tiktok_web_fetch_one_video aweme_id="视频ID"
mcporter call tikhub-tiktok.tiktok_web_fetch_video_play_url aweme_id="视频ID"
```

### YouTube 视频

```bash
mcporter call tikhub-youtube.youtube_web_fetch_one_video video_id="视频ID"
mcporter call tikhub-youtube.youtube_web_fetch_video_captions video_id="视频ID"
```

---

## 常用工具速查

### 平台视频信息获取

| 平台 | 方法 | 参数 |
|------|------|------|
| B站 | `tikhub-bilibili.bilibili_web_fetch_one_video` | `bv_id` |
| 抖音 | `tikhub-douyin.douyin_web_fetch_one_video` | `aweme_id` |
| TikTok | `tikhub-tiktok.tiktok_web_fetch_one_video` | `aweme_id` |
| YouTube | `tikhub-youtube.youtube_web_fetch_one_video` | `video_id` |
| 小红书 | `tikhub-xiaohongshu.xiaohongshu_web_fetch_one_note` | `note_id` |

### 视频直链获取

| 平台 | 方法 | 说明 |
|------|------|------|
| B站 | `bilibili_web_fetch_video_playurl` | 分段 m4s，需合并 |
| 抖音 | `douyin_app_v3_fetch_video_high_quality_play_url` | MP4 直链 ✅ |
| TikTok | `tiktok_web_fetch_video_play_url` | MP4 直链 |
| YouTube | `youtube_web_fetch_video_play_url` | 直链 |

### 字幕/弹幕

| 平台 | 字幕 | 弹幕 |
|------|------|------|
| B站 | `bilibili_web_fetch_video_subtitle` | `bilibili_web_fetch_video_danmaku` |
| 抖音 | ❌ 大多无字幕 | `douyin_web_fetch_one_video_danmaku` |
| TikTok | `tiktok_web_fetch_video_caption` | - |
| YouTube | `youtube_web_fetch_video_captions` | - |

---

## 备用方案：Python SDK

> 仅在 MCP 调用失败时使用，或需要 SDK 特有功能时使用

### 安装依赖
```bash
pip3 install tikhub --user
```

### API Key 配置
```python
import os
os.environ["TIKHUB_API_KEY"] = "你的KEY"  # 从 .env 读取
os.environ["TIKHUB_BASE_URL"] = "https://api.tikhub.dev"
```

### SDK vs MCP 对照

| 功能 | SDK 方法 | MCP 工具 |
|------|---------|---------|
| 抖音视频信息 | `client.DouyinWeb.fetch_one_video` | `douyin_web_fetch_one_video` |
| 抖音无水印下载 | `client.DouyinAppV3.fetch_one_video` | `douyin_app_v3_fetch_video_high_quality_play_url` |
| B站视频信息 | ❌ 不支持 | `bilibili_web_fetch_one_video` |
| 查询余额 | `client.TikHubUser.get_user_info()` | - |

### SDK 完整示例（抖音 → 文字稿）

```python
import asyncio
import subprocess
import whisper
from tikhub import Client

async def douyin_to_text(aweme_id: str, output_dir="/tmp"):
    async with Client(api_key=os.getenv("TIKHUB_API_KEY"), base_url="https://api.tikhub.dev") as client:
        # 1. 获取视频信息
        info = await client.DouyinWeb.fetch_one_video(aweme_id=aweme_id)
        aweme = info["data"]["aweme_detail"]
        desc = aweme["desc"]

        # 2. 获取下载直链（SDK 无水印，MCP 只返回直链）
        dl_resp = await client.DouyinAppV3.fetch_one_video(aweme_id=aweme_id)
        video_url = dl_resp["data"]["video_data"]["video_url"]["url_list"][0]

        # 3. 下载视频
        video_path = f"{output_dir}/{aweme_id}.mp4"
        subprocess.run([
            "curl", "-sL", "-o", video_path, video_url,
            "-H", "User-Agent: Mozilla/5.0",
            "-H", "Referer: https://www.douyin.com/"
        ], check=True)

        # 4. 提取音频
        audio_path = f"{output_dir}/{aweme_id}.wav"
        subprocess.run([
            "ffmpeg", "-i", video_path, "-vn",
            "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
            audio_path, "-y"
        ], check=True)

        # 5. 转写（需安装 whisper）
        model = whisper.load_model("small", device="cpu")
        result = model.transcribe(audio_path, language="zh")

        return {"desc": desc, "text": result["text"]}
```

---

## 查询余额

```bash
python3 -c "
import asyncio
import httpx

async def check():
    key = open('/Users/kk/.openclaw/workspace/.env').read().split('TIKHUB_API_KEY=')[1].split('\n')[0]
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get('https://api.tikhub.dev/api/v1/tikhub/user/get_user_info', headers={'Authorization': f'Bearer {key}'})
        d = r.json()
        print('余额:', d['user_data']['balance'], '美元')

asyncio.run(check())
"
```

---

## 已知问题

1. **B站下载直链是分段 m4s** — 需要 ffmpeg 合并，非点开即用
2. **TikHub 不是完全免费** — 注意余额，建议善用缓存机制
3. **抖音大部分视频无字幕** — 弹幕可作为内容参考
4. **MCP 响应较慢** — 首次连接需 5-10 秒，耐心等待

---

## 平台覆盖总结

| 平台 | 信息 | 字幕/弹幕 | 下载直链 | 备注 |
|------|------|----------|---------|------|
| B站 | ✅ | ✅ AI字幕 + 弹幕 | ✅ 分段直链 | 最完整 |
| 抖音 | ✅ | ✅ 弹幕 | ✅ MP4直链 | 无字幕 |
| TikTok | ✅ | ✅ 字幕 | ✅ MP4直链 | 需梯子 |
| YouTube | ✅ | ✅ 字幕 | ✅ 直链 | 需梯子 |
| 小红书 | ✅ | ❌ | ✅ | 图文为主 |
| 微博 | ✅ | ❌ | ✅ | 视频为主 |
| 快手 | ✅ | ❌ | ✅ | - |
